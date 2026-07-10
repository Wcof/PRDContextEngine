#!/usr/bin/env python3
"""Deterministic visual visibility checks for PMSkill prototypes.

This script is dependency-free and intentionally conservative: it catches obvious
invisible/near-invisible text and clickable controls caused by foreground and
background colors being identical or too close. It is not a replacement for a
browser-based accessibility audit, but it provides a stable local gate for V1 and
a fallback gate for V2/V3/Pencil exports.
"""
from __future__ import annotations

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


def add_pair_finding(findings: list[Finding], code: str, label: str, fg_name: str, bg_name: str, fg_raw: str, bg_raw: str, threshold: float) -> None:
    fg = parse_color(fg_raw)
    bg = parse_color(bg_raw)
    if fg is None or bg is None:
        findings.append(Finding("warn", code, f"Cannot parse color pair: {label}", fg_raw, bg_raw, None, threshold))
        return
    ratio = round(contrast_ratio(fg, bg), 2)
    if ratio < threshold:
        findings.append(Finding("error", code, f"Low contrast: {label} ({fg_name} on {bg_name})", fg_raw, bg_raw, ratio, threshold))


def audit(text: str) -> dict[str, object]:
    findings: list[Finding] = []
    vars_ = collect_vars(text)

    for fg, bg, threshold, label in REQUIRED_TOKEN_PAIRS:
        if fg in vars_ and bg in vars_:
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

    errors = [f for f in findings if f.severity == "error"]
    return {
        "status": "failed" if errors else "passed",
        "summary": {"errors": len(errors), "warnings": len(findings) - len(errors), "token_count": len(vars_)},
        "findings": [f.__dict__ for f in findings],
    }


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: visual_audit_prototype.py <prototype.html|prototype_dir> [more files...]", file=sys.stderr)
        sys.exit(2)
    paths = [Path(arg) for arg in sys.argv[1:]]
    text = read_targets(paths)
    result = audit(text)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["status"] != "passed":
        sys.exit(1)


if __name__ == "__main__":
    main()
