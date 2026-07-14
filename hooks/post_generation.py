#!/usr/bin/env python3
"""Fail-closed runtime gate for PMSkill generated artifacts."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


SUPPORTED_SKILLS = {"pm-sketch", "pm-need"}
REQUIRED_VISUAL_CHECKS = {
    "token_contrast_pairs",
    "interactive_visibility",
    "state_visibility",
    "focus_visible",
    "empty_clickable_overlay",
}
BUSINESS_TAGS = {"article", "button", "input", "select", "textarea", "table", "ul", "ol", "form"}
SHELL_WORDS = re.compile(r"TODO|敬请期待|占位|coming soon|placeholder", re.I)
ALLOWED_EFFECTS = {
    "navigate", "state-change", "submit", "filter", "expand", "recover", "show-toast",
    "跳转", "状态切换", "表单提交", "筛选", "展开", "错误恢复",
}


@dataclass(frozen=True)
class Finding:
    code: str
    path: str
    detail: str


@dataclass
class PageStats:
    trace_refs: int = 0
    business_elements: int = 0
    interactions: int = 0
    text: str = ""


class PrototypeParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.pages: dict[str, PageStats] = {}
        self._sections: list[str | None] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {name: value or "" for name, value in attrs}
        if tag == "section":
            page = values.get("data-trace-page") or None
            self._sections.append(page)
            if page:
                self.pages.setdefault(page, PageStats())
        page = next((item for item in reversed(self._sections) if item), None)
        if not page:
            return
        stats = self.pages[page]
        if "data-trace-ref" in values:
            stats.trace_refs += 1
        if tag in BUSINESS_TAGS:
            stats.business_elements += 1
        if (
            any(name.startswith("on") for name in values)
            or "data-action" in values
            or "data-action-index" in values
            or (tag == "a" and "href" in values)
        ):
            stats.interactions += 1

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag: str) -> None:
        if tag == "section" and self._sections:
            self._sections.pop()

    def handle_data(self, data: str) -> None:
        page = next((item for item in reversed(self._sections) if item), None)
        if page:
            self.pages[page].text += data


def load_json(path: Path, findings: list[Finding]) -> dict[str, Any] | None:
    if not path.is_file():
        findings.append(Finding("JSON_ARTIFACT_MISSING", str(path), "required JSON artifact is missing or empty"))
        return None
    try:
        raw = path.read_text(encoding="utf-8")
        if not raw.strip():
            findings.append(Finding("JSON_ARTIFACT_MISSING", str(path), "required JSON artifact is missing or empty"))
            return None
        data = json.loads(raw)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        findings.append(Finding("JSON_ARTIFACT_INVALID", str(path), str(exc)))
        return None
    if not isinstance(data, dict):
        findings.append(Finding("JSON_ARTIFACT_INVALID", str(path), "top-level value must be an object"))
        return None
    return data


def validate_artifact_schemas(
    paths: dict[str, Path],
    data: dict[str, dict[str, Any] | None],
    findings: list[Finding],
) -> None:
    source = data.get("source")
    if source:
        valid = (
            source.get("mode") == "design-source-manifest"
            and isinstance(source.get("sources"), list)
            and isinstance(source.get("resolved_tokens"), dict)
            and bool(source["resolved_tokens"])
            and isinstance(source.get("component_contract"), dict)
            and bool(source["component_contract"])
            and source.get("status") in {"resolved", "fallback-default", "missing-explicit-design-source"}
        )
        if not valid:
            findings.append(Finding("DESIGN_SOURCE_SCHEMA", str(paths["source"]), "required design source fields are missing or invalid"))

    profile = data.get("profile")
    if profile:
        dials = profile.get("dials")
        valid = (
            profile.get("mode") == "prototype-design-profile"
            and isinstance(profile.get("design_read"), str)
            and bool(profile["design_read"].strip())
            and isinstance(profile.get("style_family"), str)
            and bool(profile["style_family"].strip())
            and isinstance(dials, dict)
            and all(isinstance(dials.get(key), (int, float)) for key in ("design_variance", "motion_intensity", "visual_density"))
            and isinstance(profile.get("design_source_manifest"), str)
            and isinstance(profile.get("tokens"), dict)
            and bool(profile["tokens"])
            and isinstance(profile.get("component_contract"), dict)
            and bool(profile["component_contract"])
            and all(isinstance(profile.get(key), list) and bool(profile[key]) for key in ("layout_patterns", "interaction_patterns", "anti_patterns_banned"))
        )
        if not valid:
            findings.append(Finding("DESIGN_PROFILE_SCHEMA", str(paths["profile"]), "required design profile fields are missing or invalid"))

    visual = data.get("visual")
    if visual:
        valid = (
            visual.get("mode") == "visual-audit"
            and isinstance(visual.get("source"), str)
            and bool(visual["source"].strip())
            and isinstance(visual.get("findings"), list)
            and isinstance(visual.get("repair_actions"), list)
        )
        if not valid:
            findings.append(Finding("VISUAL_REPORT_SCHEMA", str(paths["visual"]), "required visual report fields are missing or invalid"))


def validate_shared(root: Path) -> list[Finding]:
    path = root / "pm-context.md"
    if not path.is_file() or not path.read_text(encoding="utf-8", errors="ignore").strip():
        return [Finding("PMCONTEXT_MISSING", str(path), "pm-context.md is missing or empty")]
    return []


def validate_content_plan(path: Path, data: dict[str, Any] | None, findings: list[Finding]) -> list[dict[str, Any]]:
    if data and not (
        data.get("mode") == "content-plan"
        and isinstance(data.get("source"), str)
        and bool(data["source"].strip())
        and isinstance(data.get("global_constraints"), list)
        and isinstance(data.get("unmapped_items"), list)
    ):
        findings.append(Finding("CONTENT_PLAN_SCHEMA", str(path), "required content plan fields are missing or invalid"))
    pages = data.get("pages") if data else None
    if not isinstance(pages, list) or not pages:
        findings.append(Finding("CONTENT_PLAN_EMPTY", str(path), "pages must be a non-empty array"))
        return []
    required_text = {"heading", "page_id", "primary_job", "scenario"}
    required_text_lists = {"facts", "rules", "acceptances", "states", "trace_refs"}
    valid: list[dict[str, Any]] = []
    for index, page in enumerate(pages):
        if not isinstance(page, dict):
            findings.append(Finding("CONTENT_PAGE_INVALID", str(path), f"pages[{index}] must be an object"))
            continue
        missing = sorted(key for key in required_text if not isinstance(page.get(key), str) or not page[key].strip())
        missing += sorted(
            key
            for key in required_text_lists
            if not isinstance(page.get(key), list)
            or not page[key]
            or any(not isinstance(item, str) or not item.strip() for item in page[key])
        )
        if not isinstance(page.get("actions"), list) or not page["actions"]:
            missing.append("actions")
        if missing:
            findings.append(Finding("CONTENT_PAGE_INCOMPLETE", str(path), f"pages[{index}] missing: {', '.join(missing)}"))
        actions = page.get("actions")
        if isinstance(actions, list) and not all(
            isinstance(action, dict)
            and isinstance(action.get("label"), str)
            and bool(action["label"].strip())
            and action.get("effect") in ALLOWED_EFFECTS
            and isinstance(action.get("source"), str)
            and bool(action["source"].strip())
            for action in actions
        ):
            findings.append(Finding("CONTENT_ACTION_INVALID", str(path), f"pages[{index}] actions need label, allowed effect, and source"))
        valid.append(page)
    return valid


def validate_visual_report(path: Path, data: dict[str, Any] | None, findings: list[Finding]) -> None:
    if not data:
        return
    if data.get("status") != "passed":
        findings.append(Finding("VISUAL_AUDIT_FAILED", str(path), f"status is {data.get('status')!r}"))
    checks = data.get("checks")
    if not isinstance(checks, dict):
        findings.append(Finding("VISUAL_CHECKS_MISSING", str(path), "checks must be an object"))
        return
    for name in sorted(REQUIRED_VISUAL_CHECKS):
        check = checks.get(name)
        if not isinstance(check, dict):
            findings.append(Finding("VISUAL_CHECK_MISSING", str(path), name))
            continue
        passed, failed = check.get("passed"), check.get("failed")
        if not isinstance(passed, int) or not isinstance(failed, int) or passed + failed <= 0:
            findings.append(Finding("VISUAL_CHECK_EMPTY", str(path), name))
        elif failed:
            findings.append(Finding("VISUAL_CHECK_FAILED", str(path), f"{name}: {failed} failure(s)"))


def validate_digests(artifacts: dict[str, tuple[Path, dict[str, Any] | None]], findings: list[Finding]) -> str | None:
    values: dict[str, str] = {}
    for label, (path, data) in artifacts.items():
        if data and isinstance(data.get("token_digest"), str) and data["token_digest"].strip():
            values[label] = data["token_digest"]
        else:
            findings.append(Finding("TOKEN_DIGEST_MISSING", str(path), label))
    if values and len(set(values.values())) > 1:
        findings.append(Finding("TOKEN_DIGEST_MISMATCH", ", ".join(str(path) for path, _ in artifacts.values()), json.dumps(values, ensure_ascii=False)))
    return next(iter(values.values()), None)


def route_shell_reason(stats: PageStats) -> str | None:
    text = " ".join(stats.text.split())
    failures: list[str] = []
    if stats.trace_refs < 3:
        failures.append(f"trace_refs={stats.trace_refs}")
    if stats.business_elements < 5:
        failures.append(f"business_elements={stats.business_elements}")
    if stats.interactions < 1:
        failures.append(f"interactions={stats.interactions}")
    if len(text) < 80:
        failures.append(f"text_length={len(text)}")
    if SHELL_WORDS.search(text):
        failures.append("shell placeholder text")
    return ", ".join(failures) if failures else None


def validate_simple(path: Path, pages: list[dict[str, Any]], findings: list[Finding]) -> None:
    text = path.read_text(encoding="utf-8", errors="ignore") if path.is_file() else ""
    if not text.strip():
        findings.append(Finding("PROTOTYPE_EMPTY", str(path), "prototype.html is empty"))
        return
    parser = PrototypeParser()
    parser.feed(text)
    for page in pages:
        heading = str(page.get("heading", ""))
        stats = parser.pages.get(heading)
        if not stats:
            findings.append(Finding("ROUTE_PAGE_MISSING", str(path), heading))
            continue
        reason = route_shell_reason(stats)
        if reason:
            findings.append(Finding("ROUTE_SHELL", str(path), f"{heading}: {reason}"))


def extract_trace_root(text: str, attribute_start: int) -> str:
    """Extract the balanced HTML/JSX element carrying data-trace-page."""
    opening_start = text.rfind("<", 0, attribute_start)
    if opening_start < 0:
        return ""
    opening = re.match(r"<\s*([A-Za-z][\w.-]*)\b[^>]*>", text[opening_start:], re.S)
    if not opening:
        return ""
    tag = opening.group(1)
    token_pattern = re.compile(rf"<\s*(/?)\s*{re.escape(tag)}\b[^>]*>", re.I | re.S)
    depth = 0
    for token in token_pattern.finditer(text, opening_start):
        raw = token.group(0)
        if token.group(1):
            depth -= 1
            if depth == 0:
                return text[opening_start:token.end()]
        elif not raw.rstrip().endswith("/>"):
            depth += 1
    return ""


def validate_scaffold(path: Path, pages: list[dict[str, Any]], findings: list[Finding]) -> None:
    page_files = [
        file
        for pattern in ("*.tsx", "*.jsx", "*.html")
        for file in (path / "src" / "pages").rglob(pattern)
        if file.is_file()
    ] if (path / "src" / "pages").is_dir() else []
    if not page_files:
        findings.append(Finding("SCAFFOLD_PAGES_MISSING", str(path), "src/pages has no inspectable page files"))
        return
    for page in pages:
        heading = str(page.get("heading", ""))
        heading_pattern = re.compile(
            rf"data-trace-page\s*=\s*(?:[\"']{re.escape(heading)}[\"']|\{{\s*[\"']{re.escape(heading)}[\"']\s*\}})"
        )
        file_texts = [(candidate, candidate.read_text(encoding="utf-8", errors="ignore")) for candidate in page_files]
        file = next((candidate for candidate, source in file_texts if heading_pattern.search(source)), None)
        if file is None:
            file = next((candidate for candidate, source in file_texts if heading in source), None)
        if not file:
            findings.append(Finding("SCAFFOLD_PAGE_MISSING", str(path), heading))
            continue
        text = file.read_text(encoding="utf-8", errors="ignore")
        heading_match = heading_pattern.search(text)
        trace_heading = heading_match is not None
        segment = extract_trace_root(text, heading_match.start()) if heading_match else ""
        trace_refs = len(re.findall(r"data-trace-ref\s*=", segment))
        business = len(re.findall(r"<(?:article|button|input|select|textarea|table|ul|ol|form)\b", segment))
        interactive = len(
            re.findall(
                r"on(?:Click|Submit|Change|Input)\s*=|data-action(?:-index)?\s*=|href\s*=|navigate\s*\(|set[A-Z]\w*\s*\(",
                segment,
            )
        )
        rendered_text = " ".join(re.findall(r">\s*([^<{][^<]*)<", segment))
        if not trace_heading or trace_refs < 3 or business < 5 or interactive < 1 or SHELL_WORDS.search(rendered_text):
            findings.append(Finding(
                "SCAFFOLD_ROUTE_SHELL",
                str(file),
                f"{heading}: trace_heading={trace_heading}, trace_refs={trace_refs}, business_elements={business}, interactions={interactive}",
            ))


def validate_pencil(
    path: Path,
    data: dict[str, Any] | None,
    pages: list[dict[str, Any]],
    digest: str | None,
    findings: list[Finding],
) -> None:
    if not data:
        return
    manifest_pages = data.get("pages") if isinstance(data.get("pages"), list) else []
    interactions = data.get("interactions") if isinstance(data.get("interactions"), list) else []
    exports = data.get("exports") if isinstance(data.get("exports"), list) else []
    components = data.get("components") if isinstance(data.get("components"), list) else []
    audit = data.get("visual_audit")
    ue_coverage = data.get("ue_coverage")
    schema_valid = (
        data.get("mode") == "pencil-mcp"
        and data.get("status") == "passed"
        and isinstance(data.get("design_profile"), str)
        and bool(data["design_profile"].strip())
        and isinstance(data.get("design_source_manifest"), str)
        and bool(data["design_source_manifest"].strip())
        and isinstance(data.get("style_family"), str)
        and bool(data["style_family"].strip())
        and isinstance(data.get("design_violation_count"), int)
        and data.get("design_violation_count") == 0
        and isinstance(ue_coverage, dict)
        and all(isinstance(ue_coverage.get(key), int) and ue_coverage[key] >= 0 for key in ("primary_cta_pages", "state_feedback_pages", "rule_visible_pages", "error_recovery_pages"))
        and all(
            isinstance(item, dict)
            and all(isinstance(item.get(key), str) and item[key].strip() for key in ("pmcontext_heading", "screen_id", "trace_uuid"))
            for item in manifest_pages
        )
        and all(
            isinstance(item, dict)
            and all(isinstance(item.get(key), str) and item[key].strip() for key in ("from", "to", "source"))
            for item in interactions
        )
        and bool(components)
        and all(
            isinstance(item, dict)
            and all(isinstance(item.get(key), str) and item[key].strip() for key in ("name", "source"))
            for item in components
        )
        and all(
            (isinstance(item, str) and bool(item.strip()))
            or (isinstance(item, dict) and any(isinstance(item.get(key), str) and item[key].strip() for key in ("path", "artifact_id")))
            for item in exports
        )
        and isinstance(audit, dict)
        and audit.get("status") == "passed"
        and audit.get("contrast_failures") == 0
        and audit.get("invisible_interactive_count") == 0
    )
    if not schema_valid:
        findings.append(Finding("PENCIL_SCHEMA", str(path), "required Pencil manifest evidence is missing or invalid"))
    headings = {item.get("pmcontext_heading") for item in manifest_pages if isinstance(item, dict) and item.get("trace_uuid")}
    missing = [str(page.get("heading")) for page in pages if page.get("heading") not in headings]
    if missing:
        findings.append(Finding("PENCIL_PAGE_MISSING", str(path), ", ".join(missing)))
    if not interactions:
        findings.append(Finding("PENCIL_INTERACTION_MISSING", str(path), "interactions must be non-empty"))
    if not exports:
        findings.append(Finding("PENCIL_EXPORT_MISSING", str(path), "exports must be non-empty"))
    if digest and data.get("token_digest") != digest:
        findings.append(Finding("PENCIL_TOKEN_DIGEST_MISMATCH", str(path), "manifest digest differs from design artifacts"))
    coverage = data.get("component_coverage")
    required = {"button", "card", "table", "form", "navigation", "modal_drawer"}
    if not isinstance(coverage, dict) or any(coverage.get(name) is not True for name in required):
        findings.append(Finding("PENCIL_COMPONENT_COVERAGE", str(path), "required components are not fully covered"))
    if not isinstance(audit, dict) or audit.get("status") != "passed":
        findings.append(Finding("PENCIL_VISUAL_AUDIT", str(path), "visual_audit.status must be passed"))


def validate_sketch(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    sketch = root / "sketch"
    paths = {
        "content": sketch / "prototype-content-plan.json",
        "profile": sketch / "prototype-design-profile.json",
        "source": sketch / "design-source-manifest.json",
        "visual": sketch / "visual-audit-report.json",
    }
    data = {name: load_json(path, findings) for name, path in paths.items()}
    validate_artifact_schemas(paths, data, findings)
    pages = validate_content_plan(paths["content"], data["content"], findings)
    validate_visual_report(paths["visual"], data["visual"], findings)
    digest = validate_digests(
        {name: (paths[name], data[name]) for name in ("profile", "source", "visual")},
        findings,
    )

    implementations = 0
    simple = sketch / "prototype.html"
    scaffold = sketch / "prototype"
    pencil = sketch / "pencil" / "pencil-prototype-manifest.json"
    if simple.exists():
        implementations += 1
        validate_simple(simple, pages, findings)
    if scaffold.exists():
        implementations += 1
        validate_scaffold(scaffold, pages, findings)
    if pencil.exists():
        pencil_data = load_json(pencil, findings)
        if pencil_data and pencil_data.get("status") == "fallback-local":
            if (
                pencil_data.get("mode") != "pencil-mcp"
                or not isinstance(pencil_data.get("fallback_reason"), str)
                or not pencil_data["fallback_reason"].strip()
            ):
                findings.append(Finding("PENCIL_FALLBACK_SCHEMA", str(pencil), "fallback-local requires mode=pencil-mcp and fallback_reason"))
        else:
            implementations += 1
            validate_pencil(pencil, pencil_data, pages, digest, findings)
    if not implementations:
        findings.append(Finding("PROTOTYPE_IMPLEMENTATION_MISSING", str(sketch), "no Simple, Scaffold, or Pencil output found"))
    return findings


def validate_need_auto(root: Path) -> list[Finding]:
    required = [
        "process/01-collect-understand.md",
        "process/02-refine-model.md",
        "process/03-refine-options.md",
        "process/04-refine-tradeoff.md",
        "process/05-premortem-risk.md",
        "prd/ai-prd.md",
        "prd/human-prd.md",
        "stories.md",
        "sketch/wireframe.md",
        "sketch/ia.md",
        "sketch/state.md",
        "sketch/flow.md",
        "sketch/journey.md",
        "SUMMARY-需求.md",
        "SUMMARY-交付.md",
        "SUMMARY-可视化.md",
        "SUMMARY-验证.md",
        "INDEX.md",
    ]
    return [
        Finding("AUTO_ARTIFACT_MISSING", str(root / rel), "required auto-chain artifact is missing or empty")
        for rel in required
        if not (root / rel).is_file() or not (root / rel).read_text(encoding="utf-8", errors="ignore").strip()
    ]


def make_report(status: str, skill: str, root: Path, findings: list[Finding]) -> dict[str, Any]:
    return {
        "status": status,
        "skill": skill,
        "artifact_root": str(root),
        "checks": {"finding_count": len(findings)},
        "findings": [asdict(finding) for finding in findings],
    }


def validate(skill: str, root: Path, auto: bool = False) -> tuple[int, dict[str, Any]]:
    if skill not in SUPPORTED_SKILLS:
        findings = [Finding("SKILL_UNSUPPORTED", skill, f"supported skills: {', '.join(sorted(SUPPORTED_SKILLS))}")]
        return 2, make_report("invalid", skill, root, findings)
    if not root.is_dir():
        findings = [Finding("ARTIFACT_ROOT_MISSING", str(root), "artifact root is not a directory")]
        return 2, make_report("invalid", skill, root, findings)
    if skill == "pm-need" and not auto:
        findings = [Finding("AUTO_FLAG_REQUIRED", skill, "pm-need completion gate is only defined for --auto runs")]
        return 2, make_report("invalid", skill, root, findings)
    findings = validate_shared(root)
    if skill == "pm-sketch" or auto:
        findings.extend(validate_sketch(root))
    if skill == "pm-need":
        findings.extend(validate_need_auto(root))
    return (1 if findings else 0), make_report("failed" if findings else "passed", skill, root, findings)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill", required=True)
    parser.add_argument("--artifact-root", required=True, type=Path)
    parser.add_argument("--auto", action="store_true")
    args = parser.parse_args()
    try:
        code, result = validate(args.skill, args.artifact_root, args.auto)
    except (OSError, UnicodeError) as exc:
        findings = [Finding("INSPECTION_ERROR", str(args.artifact_root), str(exc))]
        code, result = 2, make_report("invalid", args.skill, args.artifact_root, findings)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(code)


if __name__ == "__main__":
    main()
