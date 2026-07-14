#!/usr/bin/env python3
"""Deterministic visual visibility checks for PMSkill prototypes.

This script is dependency-free and intentionally conservative: it catches obvious
invisible/near-invisible text and clickable controls caused by foreground and
background colors being identical or too close. It is not a replacement for a
browser-based accessibility audit, but it provides a stable local gate for V1 and
a fallback gate for V2/V3/Pencil exports.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

HEX_RE = re.compile(r"#([0-9a-fA-F]{3}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})\b")
RGB_RE = re.compile(r"rgba?\(([^)]+)\)", re.I)
VAR_RE = re.compile(r"--([a-zA-Z0-9_-]+)\s*:\s*([^;}{]+)")
INLINE_STYLE_RE = re.compile(r"<(a|button|input|select|textarea|summary|[^>]+role=['\"]button['\"][^>]*)\b[^>]*style=['\"]([^'\"]+)['\"]", re.I)
INTERACTIVE_RE = re.compile(r"<(?:a\b[^>]*href=|button\b|input\b|select\b|textarea\b|[^>]+role=['\"]button['\"])", re.I)
INTERACTIVE_OPEN_TAG_RE = re.compile(
    r"<(?P<tag>a|button|input|select|textarea|summary)\b(?P<attrs>[^>]*)>",
    re.I,
)
EMPTY_CLICKABLE_RE = re.compile(r"<(?:a|button)\b[^>]*>\s*</(?:a|button)>", re.I)
FOCUS_RE = re.compile(r":focus(?:-visible)?\b", re.I)
CSS_RULE_RE = re.compile(r"([^{}]+)\{([^{}]*)\}", re.S)

REQUIRED_TOKEN_PAIRS = [
    ("color-text", "color-bg", 4.5, "body text on page background"),
    ("color-text-secondary", "color-bg", 4.5, "secondary text on page background"),
    ("color-text-muted", "color-bg", 3.0, "muted text on page background"),
    ("color-text", "color-bg-secondary", 4.5, "body text on secondary surface"),
    ("color-text-secondary", "color-bg-secondary", 4.5, "secondary text on secondary surface"),
    ("color-text-muted", "color-bg-secondary", 3.0, "muted text on secondary surface"),
    ("color-text", "color-bg-tertiary", 4.5, "body text on tertiary surface"),
    ("color-primary", "color-bg", 3.0, "primary interactive color on page background"),
    ("color-border", "color-bg", 3.0, "visible borders on page background"),
]
STATE_TOKEN_PAIRS = [
    ("color-on-success", "color-success", "success state"),
    ("color-on-danger", "color-danger", "error state"),
    ("color-on-error", "color-error", "error state"),
    ("color-on-warning", "color-warning", "warning state"),
    ("color-success", "color-success-bg", "success state"),
    ("color-error", "color-error-bg", "error state"),
    ("color-warning", "color-warning-bg", "warning state"),
]

@dataclass
class Finding:
    severity: str
    code: str
    message: str
    foreground: str | None = None
    background: str | None = None
    ratio: float | None = None
    threshold: float | None = None


def parse_color(raw: str) -> tuple[int, int, int] | None:
    raw = raw.strip().strip('"\'')
    m = HEX_RE.search(raw)
    if m:
        h = m.group(1)
        if len(h) == 3:
            h = ''.join(c * 2 for c in h)
        if len(h) == 8:
            h = h[:6]
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))  # type: ignore[return-value]
    m = RGB_RE.search(raw)
    if m:
        parts = [p.strip() for p in m.group(1).split(',')[:3]]
        vals = []
        for p in parts:
            if p.endswith('%'):
                vals.append(round(float(p[:-1]) * 2.55))
            else:
                vals.append(round(float(p)))
        if len(vals) == 3 and all(0 <= v <= 255 for v in vals):
            return tuple(vals)  # type: ignore[return-value]
    return None


def srgb_channel(c: int) -> float:
    x = c / 255
    return x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4


def luminance(rgb: tuple[int, int, int]) -> float:
    r, g, b = (srgb_channel(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(a: tuple[int, int, int], b: tuple[int, int, int]) -> float:
    la, lb = luminance(a), luminance(b)
    lighter, darker = max(la, lb), min(la, lb)
    return (lighter + 0.05) / (darker + 0.05)


def read_targets(paths: Iterable[Path]) -> str:
    chunks: list[str] = []
    for p in paths:
        if p.is_dir():
            for ext in ("*.html", "*.css", "*.tsx", "*.jsx", "*.ts", "*.js"):
                for f in p.rglob(ext):
                    if "node_modules" not in f.parts and f.is_file():
                        chunks.append(f"\n/* FILE: {f} */\n" + f.read_text(encoding="utf-8", errors="ignore"))
        elif p.is_file():
            chunks.append(f"\n/* FILE: {p} */\n" + p.read_text(encoding="utf-8", errors="ignore"))
    return "\n".join(chunks)


def collect_vars(text: str) -> dict[str, str]:
    vars_: dict[str, str] = {}
    for name, value in VAR_RE.findall(text):
        vars_[name] = value.strip()
    return vars_


def resolve_var(value: str, vars_: dict[str, str], depth: int = 0) -> str:
    if depth > 5:
        return value
    m = re.search(r"var\(--([a-zA-Z0-9_-]+)(?:,\s*([^)]*))?\)", value)
    if not m:
        return value
    repl = vars_.get(m.group(1), m.group(2) or "")
    return resolve_var(value[:m.start()] + repl + value[m.end():], vars_, depth + 1)


def interactive_elements(text: str) -> list[tuple[str, set[str], str | None]]:
    """Return the tag, classes, and id for statically inspectable controls."""
    elements: list[tuple[str, set[str], str | None]] = []
    for match in INTERACTIVE_OPEN_TAG_RE.finditer(text):
        attrs = match.group("attrs")
        class_match = re.search(r"\bclass(?:Name)?\s*=\s*['\"]([^'\"]*)['\"]", attrs, re.I)
        id_match = re.search(r"\bid\s*=\s*['\"]([^'\"]+)['\"]", attrs, re.I)
        classes = set(class_match.group(1).split()) if class_match else set()
        elements.append((match.group("tag").lower(), classes, id_match.group(1) if id_match else None))
    return elements


def selector_matches_control(selector: str, controls: list[tuple[str, set[str], str | None]]) -> bool:
    """Conservatively match a CSS selector's target compound to a control."""
    for part in selector.split(","):
        target = re.split(r"\s+|(?=[>+~])|(?<=[>+~])", part.strip())[-1]
        target = re.sub(r"::?[a-zA-Z-]+(?:\([^)]*\))?", "", target)
        tag_match = re.match(r"^([a-zA-Z][\w-]*)", target)
        required_tag = tag_match.group(1).lower() if tag_match else None
        required_classes = set(re.findall(r"\.([a-zA-Z_][\w-]*)", target))
        id_match = re.search(r"#([a-zA-Z_][\w-]*)", target)
        required_id = id_match.group(1) if id_match else None
        if not (required_tag or required_classes or required_id):
            continue
        for tag, classes, element_id in controls:
            if required_tag and required_tag != tag:
                continue
            if required_classes and not required_classes.issubset(classes):
                continue
            if required_id and required_id != element_id:
                continue
            return True
    return False


def add_pair_finding(findings: list[Finding], code: str, label: str, fg_name: str, bg_name: str, fg_raw: str, bg_raw: str, threshold: float) -> None:
    fg = parse_color(fg_raw)
    bg = parse_color(bg_raw)
    if fg is None or bg is None:
        findings.append(Finding("error", "UNPARSEABLE_COLOR", f"Cannot parse required color pair: {label}", fg_raw, bg_raw, None, threshold))
        return
    ratio = round(contrast_ratio(fg, bg), 2)
    if ratio < threshold:
        findings.append(Finding("error", code, f"Low contrast: {label} ({fg_name} on {bg_name})", fg_raw, bg_raw, ratio, threshold))


def audit(text: str) -> dict[str, object]:
    findings: list[Finding] = []
    vars_ = collect_vars(text)
    controls = interactive_elements(text)
    inspected = 0

    for fg, bg, threshold, label in REQUIRED_TOKEN_PAIRS:
        if fg in vars_ and bg in vars_:
            inspected += 1
            add_pair_finding(
                findings,
                "LOW_TOKEN_CONTRAST",
                label,
                f"--{fg}",
                f"--{bg}",
                resolve_var(vars_[fg], vars_),
                resolve_var(vars_[bg], vars_),
                threshold,
            )

    # Button/on-primary contract. If --color-on-primary is absent, assume white and still check.
    if "color-primary" in vars_:
        inspected += 1
        on_primary = vars_.get("color-on-primary", "#ffffff")
        add_pair_finding(
            findings,
            "LOW_CONTROL_CONTRAST",
            "button label on primary button",
            "--color-on-primary|#ffffff",
            "--color-primary",
            resolve_var(on_primary, vars_),
            resolve_var(vars_["color-primary"], vars_),
            4.5,
        )

    # Inline interactive controls with explicit color/background.
    for m in INLINE_STYLE_RE.finditer(text):
        tag, style = m.group(1), m.group(2)
        color_m = re.search(r"(?:^|;)\s*color\s*:\s*([^;]+)", style, re.I)
        bg_m = re.search(r"(?:^|;)\s*background(?:-color)?\s*:\s*([^;]+)", style, re.I)
        if color_m and bg_m:
            add_pair_finding(
                findings,
                "LOW_INLINE_INTERACTIVE_CONTRAST",
                f"inline interactive element <{tag.split()[0]}> label",
                "inline color",
                "inline background",
                resolve_var(color_m.group(1), vars_),
                resolve_var(bg_m.group(1), vars_),
                4.5,
            )
        opacity_m = re.search(r"(?:^|;)\s*opacity\s*:\s*([0-9.]+)", style, re.I)
        if opacity_m and float(opacity_m.group(1)) < 0.2:
            findings.append(Finding("error", "INVISIBLE_INTERACTIVE_OPACITY", f"Interactive element <{tag.split()[0]}> has opacity < 0.2"))

    # Static CSS fallback: catch direct interactive selectors and class/id rules
    # that apply to an inspectable control.
    for selector, declarations in CSS_RULE_RE.findall(text):
        direct_control_selector = re.search(
            r"\b(?:button|input|select|textarea|summary)\b|\ba(?:\b|\[|:)|\[role\s*=",
            selector,
            re.I,
        )
        if not direct_control_selector and not selector_matches_control(selector, controls):
            continue
        hidden = re.search(r"(?:^|;)\s*(?:display\s*:\s*none|visibility\s*:\s*hidden)(?:\s*!important)?\s*(?:;|$)", declarations, re.I)
        opacity = re.search(r"(?:^|;)\s*opacity\s*:\s*([0-9.]+)", declarations, re.I)
        if hidden or (opacity and float(opacity.group(1)) < 0.2):
            findings.append(Finding("error", "HIDDEN_INTERACTIVE_STYLE", f"Interactive selector is hidden: {selector.strip()}"))
        color_m = re.search(r"(?:^|;)\s*color\s*:\s*([^;]+)", declarations, re.I)
        bg_m = re.search(r"(?:^|;)\s*background(?:-color)?\s*:\s*([^;]+)", declarations, re.I)
        if color_m and bg_m:
            add_pair_finding(
                findings,
                "LOW_CSS_INTERACTIVE_CONTRAST",
                f"interactive selector {selector.strip()}",
                "CSS color",
                "CSS background",
                resolve_var(color_m.group(1), vars_),
                resolve_var(bg_m.group(1), vars_),
                4.5,
            )

    if inspected == 0:
        findings.append(
            Finding(
                "error",
                "NO_VISUAL_TOKENS_INSPECTED",
                "No required visual token pairs were found; the visual gate cannot prove the prototype is usable.",
            )
        )

    interactive_count = len(INTERACTIVE_RE.findall(text))
    interactive_errors = sum(
        1
        for f in findings
        if f.code in {
            "LOW_INLINE_INTERACTIVE_CONTRAST",
            "LOW_CSS_INTERACTIVE_CONTRAST",
            "INVISIBLE_INTERACTIVE_OPACITY",
            "HIDDEN_INTERACTIVE_STYLE",
        }
    )
    if interactive_count == 0:
        interactive_errors = 1
        findings.append(Finding("error", "NO_INTERACTIVE_ELEMENTS", "No interactive element was inspected"))

    state_count = 0
    for foreground, background, label in STATE_TOKEN_PAIRS:
        if foreground in vars_ and background in vars_:
            state_count += 1
            add_pair_finding(
                findings,
                "LOW_STATE_CONTRAST",
                label,
                f"--{foreground}",
                f"--{background}",
                resolve_var(vars_[foreground], vars_),
                resolve_var(vars_[background], vars_),
                4.5,
            )
    state_errors = sum(1 for f in findings if f.code == "LOW_STATE_CONTRAST" and f.severity == "error")
    if state_count == 0:
        findings.append(Finding("error", "NO_STATE_TOKENS", "No success/error/warning state token was inspected"))

    focus_count = len(FOCUS_RE.findall(text))
    if focus_count == 0:
        findings.append(Finding("error", "MISSING_FOCUS_VISIBLE", "No :focus or :focus-visible rule was found"))

    empty_clickables = len(EMPTY_CLICKABLE_RE.findall(text))
    if empty_clickables:
        findings.append(Finding("error", "EMPTY_CLICKABLE_OVERLAY", f"Found {empty_clickables} empty clickable element(s)"))

    token_errors = sum(1 for f in findings if f.code in {"LOW_TOKEN_CONTRAST", "LOW_CONTROL_CONTRAST"} and f.severity == "error")
    errors = [f for f in findings if f.severity == "error"]
    return {
        "status": "failed" if errors else "passed",
        "checks": {
            "token_contrast_pairs": {"passed": max(inspected - token_errors, 0), "failed": token_errors},
            "interactive_visibility": {"passed": max(interactive_count - interactive_errors, 0), "failed": interactive_errors},
            "state_visibility": {"passed": max(state_count - state_errors, 0), "failed": state_errors if state_count else 1},
            "focus_visible": {"passed": focus_count, "failed": 0 if focus_count else 1},
            "empty_clickable_overlay": {"passed": 1 if empty_clickables == 0 else 0, "failed": empty_clickables},
        },
        "summary": {
            "errors": len(errors),
            "warnings": len(findings) - len(errors),
            "token_count": len(vars_),
            "inspected_check_count": inspected,
        },
        "findings": [f.__dict__ for f in findings],
        "repair_actions": [],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--token-digest", default="")
    parser.add_argument("paths", nargs="+")
    args = parser.parse_args()
    paths = [Path(arg) for arg in args.paths]
    try:
        text = read_targets(paths)
    except OSError as exc:
        print(
            json.dumps(
                {
                    "mode": "visual-audit",
                    "status": "failed",
                    "source": ", ".join(str(path) for path in paths),
                    "token_digest": args.token_digest,
                    "checks": {},
                    "findings": [
                        {
                            "severity": "error",
                            "code": "INPUT_READ_ERROR",
                            "message": str(exc),
                        }
                    ],
                    "repair_actions": [],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        sys.exit(2)
    if not text.strip():
        print(
            json.dumps(
                {
                    "mode": "visual-audit",
                    "status": "failed",
                    "source": ", ".join(str(path) for path in paths),
                    "token_digest": args.token_digest,
                    "checks": {
                        "token_contrast_pairs": {"passed": 0, "failed": 1},
                        "interactive_visibility": {"passed": 0, "failed": 1},
                        "state_visibility": {"passed": 0, "failed": 1},
                        "focus_visible": {"passed": 0, "failed": 1},
                        "empty_clickable_overlay": {"passed": 0, "failed": 1},
                    },
                    "summary": {
                        "errors": 1,
                        "warnings": 0,
                        "token_count": 0,
                        "inspected_check_count": 0,
                    },
                    "findings": [
                        {
                            "severity": "error",
                            "code": "INPUT_MISSING_OR_EMPTY",
                            "message": "Input paths are missing, empty, or contain no readable prototype source.",
                        }
                    ],
                    "repair_actions": [],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        sys.exit(1)
    result = audit(text)
    result["mode"] = "visual-audit"
    result["source"] = ", ".join(str(path) for path in paths)
    result["token_digest"] = args.token_digest
    if not args.token_digest:
        result["status"] = "failed"
        findings = result["findings"]
        if isinstance(findings, list):
            findings.append(
                {
                    "severity": "error",
                    "code": "TOKEN_DIGEST_MISSING",
                    "message": "Pass --token-digest from design-source-manifest.json",
                    "foreground": None,
                    "background": None,
                    "ratio": None,
                    "threshold": None,
                }
            )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["status"] != "passed":
        sys.exit(1)


if __name__ == "__main__":
    main()
