#!/usr/bin/env python3
"""Deterministic structural checks for PMSkill.

This is intentionally model-free: it catches repository drift that natural-language
skill constraints alone cannot enforce.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_TOTAL = 52
EXPECTED_VISIBLE = {
    "pm-setup": "skills/setup/pm-setup",
    "pm-need": "skills/discovery/pm-need",
    "pm-prd": "skills/delivery/pm-prd",
    "pm-premortem": "skills/delivery/pm-premortem",
    "pm-summary": "skills/utility/pm-summary",
    "pm-sketch": "skills/visualization/pm-sketch",
}
EXPECTED_HUMAN_ONLY = {"pm-setup", "pm-need"}
EXPECTED_ENGINE_COUNT = 46


def fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    sys.exit(1)


def read(path: str | Path) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def check_no_mojibake_paths() -> None:
    bad_tokens = ["┬", "╠", "╬", "Γ", "�"]
    for path in ROOT.rglob("*"):
        rel = path.relative_to(ROOT).as_posix()
        if any(tok in rel for tok in bad_tokens):
            fail(f"mojibake/corrupted path name detected: {rel}")


def frontmatter(path: Path) -> tuple[dict[str, object], list[str], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail(f"{path} missing YAML frontmatter")
    parts = text.split("---", 2)
    if len(parts) < 3:
        fail(f"{path} malformed YAML frontmatter")
    raw = parts[1].strip("\n")
    keys: list[str] = []
    data: dict[str, object] = {}
    current_key: str | None = None
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if not line.startswith(" "):
            key = line.split(":", 1)[0].strip()
            keys.append(key)
            current_key = key
            value = line.split(":", 1)[1].strip() if ":" in line else ""
            if value:
                if value in {"true", "false"}:
                    data[key] = value == "true"
                else:
                    data[key] = value.strip('"')
            else:
                data[key] = {}
        elif current_key == "metadata":
            m = re.match(r"\s+([^:]+):\s*(.*)$", line)
            if m:
                meta = data.setdefault("metadata", {})
                if not isinstance(meta, dict):
                    fail(f"{path} metadata is not a map")
                val = m.group(2).strip()
                meta[m.group(1).strip()] = val == "true" if val in {"true", "false"} else val
    dupes = [k for k, n in Counter(keys).items() if n > 1]
    if dupes:
        fail(f"{path} duplicate frontmatter keys: {dupes}")
    return data, keys, raw


def check_skills() -> None:
    skill_paths = sorted((ROOT / "skills").rglob("SKILL.md"))
    if len(skill_paths) != EXPECTED_TOTAL:
        fail(f"expected {EXPECTED_TOTAL} skills, found {len(skill_paths)}")

    names: list[str] = []
    visible: dict[str, str] = {}
    internal: list[str] = []
    human_only: set[str] = set()

    for path in skill_paths:
        fm, _, _ = frontmatter(path)
        name = fm.get("name")
        desc = fm.get("description")
        if not isinstance(name, str) or not name:
            fail(f"{path} missing name")
        if not isinstance(desc, str) or len(desc) < 30:
            fail(f"{path} description too short/missing")
        names.append(name)
        metadata = fm.get("metadata", {})
        is_internal = isinstance(metadata, dict) and metadata.get("internal") is True
        rel_dir = path.parent.relative_to(ROOT).as_posix()
        if is_internal:
            internal.append(name)
        else:
            visible[name] = rel_dir
        if fm.get("disable-model-invocation") is True:
            human_only.add(name)

    dup_names = [n for n, c in Counter(names).items() if c > 1]
    if dup_names:
        fail(f"duplicate skill names: {dup_names}")
    if visible != EXPECTED_VISIBLE:
        fail(f"visible skill set drifted: {visible}")
    if len(internal) != EXPECTED_ENGINE_COUNT:
        fail(f"expected {EXPECTED_ENGINE_COUNT} engine skills, found {len(internal)}")
    if human_only != EXPECTED_HUMAN_ONLY:
        fail(f"human-only entry set drifted: {sorted(human_only)}")


def check_plugins() -> None:
    expected_paths = list(EXPECTED_VISIBLE.values())
    expected_plugin = [f"./{p}" for p in expected_paths]
    for fname in [".claude-plugin/plugin.json", ".codex-plugin/plugin.json"]:
        data = json.loads(read(fname))
        skills = data.get("skills")
        if skills != expected_plugin:
            fail(f"{fname} skills mismatch: {skills} != {expected_plugin}")
        for skill_path in skills:
            if not (ROOT / skill_path[2:] / "SKILL.md").exists():
                fail(f"{fname} references missing skill path: {skill_path}")


def check_docs_and_routes() -> None:
    context = read("CONTEXT.md")
    for term in ["Human-only Entry", "Hybrid Entry", "pm-summary", "当前 User-facing 名单（6 个）"]:
        if term not in context:
            fail(f"CONTEXT.md missing {term}")

    need = read("skills/discovery/pm-need/SKILL.md")
    if "/pm-sketch --prototype --auto --no-fallback" not in need:
        fail("pm-need auto route must call pm-sketch with --no-fallback")
    for token in ["pm-premortem", "pm-prd", "pm-stories", "pm-sketch", "pm-summary"]:
        if token not in need:
            fail(f"pm-need route missing {token}")
    for token in [
        "Argument-first 增量路由",
        "Downstream Fan-out",
        "--context-only",
        "/pm-summary --auto",
    ]:
        if token not in need:
            fail(f"pm-need missing incremental/summary constraint: {token}")

    sketch = read("skills/visualization/pm-sketch/SKILL.md")
    for token in [
        "Step -0.75：Pencil MCP 实现门",
        "pencil-prototype-manifest.json",
        "--no-mcp",
        "fallback-local",
        "继续 Step -0.5 / Step -1 本地 fallback",
        "5 个 Mermaid 文件路径",
        "Step -0.9：原型内容编译门",
        "Step -0.85：设计风格编译门",
        "references/design-style.md",
        "prototype-content-plan.json",
        "prototype-design-profile.json",
        "design_profile",
        "data-trace-ref",
        "路由空壳检测",
    ]:
        if token not in sketch:
            fail(f"pm-sketch missing Pencil/route/content constraint: {token}")

    templates = read("skills/visualization/pm-sketch/references/prototype-templates.md")
    for token in [
        "Pencil MCP Manifest 模板",
        "status=fallback-local",
        "### 13.0 Pencil MCP 模式",
        "Design Style Profile（视觉/UE 数据契约）",
        "prototype-design-profile.json",
        "{{DESIGN_PROFILE}}",
        "Prototype Content Plan（反空壳数据契约）",
        "PROTOTYPE_CONTENT_PLAN",
        "renderPageSection",
        "inspectRouteShell",
    ]:
        if token not in templates:
            fail(f"prototype templates missing {token}")

    design_style = read("skills/visualization/pm-sketch/references/design-style.md")
    for token in [
        "PM Prototype Design Style System",
        "Design Read",
        "design_variance",
        "AI Native Dark",
        "Pencil MCP 设计 brief 协议",
        "ue_coverage",
    ]:
        if token not in design_style:
            fail(f"design-style reference missing {token}")

    pinned = read("skills/visualization/pm-sketch/PINNED.md")
    for token in ["Pencil MCP 优先", "prototype-design-profile.json", "prototype-content-plan.json", "fallback-local"]:
        if token not in pinned:
            fail(f"pm-sketch PINNED missing runtime-critical token: {token}")

    context = read("CONTEXT.md")
    for token in ["Prototype Design Profile", "references/design-style.md", "prototype-design-profile.json"]:
        if token not in context:
            fail(f"CONTEXT.md missing design profile constraint: {token}")

    summary = read("skills/utility/pm-summary/SKILL.md")
    for token in ["`--auto` 模式", "只读终局汇总器", "不参与需求推断", "原产物不动"]:
        if token not in summary:
            fail(f"pm-summary missing auto finalizer constraint: {token}")


def check_evals() -> None:
    for path in sorted((ROOT / "evals").glob("pm-*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            fail(f"{path} JSON parse failed: {exc}")
        if not isinstance(data, list) or not data:
            fail(f"{path} must be a non-empty list")
        for idx, sc in enumerate(data, 1):
            if not sc.get("skills") or not sc.get("query"):
                fail(f"{path} scenario {idx} missing skills/query")
            eb = sc.get("expected_behavior")
            if not isinstance(eb, list) or not eb:
                fail(f"{path} scenario {idx} missing expected_behavior")
            for fixture in sc.get("files", []):
                if not (ROOT / "evals" / fixture).exists():
                    fail(f"{path} scenario {idx} missing fixture {fixture}")


def main() -> None:
    check_no_mojibake_paths()
    check_skills()
    check_plugins()
    check_docs_and_routes()
    check_evals()
    print("PASS: PMSkill structural constraints hold")


if __name__ == "__main__":
    main()
