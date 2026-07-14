from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / "hooks" / "post_generation.py"
VISUAL_AUDIT = ROOT / "scripts" / "visual_audit_prototype.py"


class PostGenerationHookTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.artifact_root = Path(self.tempdir.name) / "pm-context"
        self.sketch = self.artifact_root / "sketch"
        self.sketch.mkdir(parents=True)
        (self.artifact_root / "pm-context.md").write_text("# PMContext\n\n## Home\n", encoding="utf-8")

    def run_hook(self, skill: str = "pm-sketch", *, auto: bool = False, root: Path | None = None) -> subprocess.CompletedProcess[str]:
        command = [
            sys.executable,
            str(HOOK),
            "--skill",
            skill,
            "--artifact-root",
            str(root or self.artifact_root),
        ]
        if auto:
            command.append("--auto")
        return subprocess.run(command, cwd=ROOT, text=True, capture_output=True)

    def write_shared_jsons(self) -> None:
        content_plan = {
            "source": "pm-context.md",
            "mode": "content-plan",
            "pages": [
                {
                    "heading": "Home",
                    "page_id": "home",
                    "primary_job": "完成会员续费",
                    "scenario": "会员在到期前续费并确认权益",
                    "facts": ["当前套餐", "到期日"],
                    "rules": ["续费后立即生效"],
                    "acceptances": ["支付成功后显示新到期日"],
                    "fields": [{"name": "套餐", "source": "Home#套餐"}],
                    "actions": [{"label": "确认续费", "effect": "submit", "source": "Home#续费"}],
                    "states": ["loading", "empty", "success", "error"],
                    "trace_refs": ["Home#套餐", "Home#续费", "Home#验收"],
                }
            ],
            "global_constraints": [],
            "unmapped_items": [],
        }
        design_source = {
            "mode": "design-source-manifest",
            "sources": [{"path": "DESIGN.md", "type": "tokens", "hash": "source-hash"}],
            "resolved_tokens": {"color_bg": "#ffffff", "color_text": "#111827", "color_accent": "#1d4ed8"},
            "component_contract": {"button": {"states": ["default", "focus"]}},
            "token_digest": "digest-1",
            "status": "resolved",
        }
        design_profile = {
            "mode": "prototype-design-profile",
            "design_read": "会员续费采用清晰可信的事务界面",
            "style_family": "Trust First",
            "dials": {"design_variance": 3, "motion_intensity": 2, "visual_density": 5},
            "design_source_manifest": "sketch/design-source-manifest.json",
            "token_digest": "digest-1",
            "tokens": design_source["resolved_tokens"],
            "component_contract": design_source["component_contract"],
            "layout_patterns": ["transaction form"],
            "interaction_patterns": ["inline validation"],
            "anti_patterns_banned": ["empty route shell"],
        }
        visual_report = {
            "mode": "visual-audit",
            "status": "passed",
            "source": "prototype.html",
            "token_digest": "digest-1",
            "checks": {
                "token_contrast_pairs": {"passed": 4, "failed": 0},
                "interactive_visibility": {"passed": 1, "failed": 0},
                "state_visibility": {"passed": 1, "failed": 0},
                "focus_visible": {"passed": 1, "failed": 0},
                "empty_clickable_overlay": {"passed": 1, "failed": 0},
            },
            "findings": [],
            "repair_actions": [],
        }
        for name, data in {
            "prototype-content-plan.json": content_plan,
            "design-source-manifest.json": design_source,
            "prototype-design-profile.json": design_profile,
            "visual-audit-report.json": visual_report,
        }.items():
            (self.sketch / name).write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    @staticmethod
    def complete_page() -> str:
        return """<!doctype html>
<html><body>
<section id="page-home" data-trace-page="Home">
  <h1>会员续费工作台</h1>
  <p data-trace-ref="Home#场景">会员在套餐到期前核对价格、权益和新的到期日期，并完成安全续费。</p>
  <article data-trace-ref="Home#套餐">当前套餐：专业版</article>
  <article data-trace-ref="Home#到期日">当前到期日：2026-08-01</article>
  <form data-trace-ref="Home#续费"><label>套餐<select><option>专业版</option></select></label></form>
  <ul data-trace-ref="Home#规则"><li>续费支付成功后权益立即生效</li></ul>
  <table data-trace-ref="Home#验收"><tr><td>新到期日</td><td>2027-08-01</td></tr></table>
  <button type="button" data-action="submit" data-trace-ref="Home#动作">确认续费</button>
</section>
</body></html>"""

    def test_missing_artifact_root_is_invocation_error(self) -> None:
        result = self.run_hook(root=self.artifact_root / "missing")
        self.assertEqual(result.returncode, 2)
        self.assertIn("ARTIFACT_ROOT_MISSING", result.stdout)

    def test_empty_prototype_fails_closed(self) -> None:
        self.write_shared_jsons()
        (self.sketch / "prototype.html").write_text("", encoding="utf-8")
        result = self.run_hook()
        self.assertEqual(result.returncode, 1)
        self.assertIn("PROTOTYPE_EMPTY", result.stdout)

    def test_route_shell_fails(self) -> None:
        self.write_shared_jsons()
        (self.sketch / "prototype.html").write_text(
            '<section data-trace-page="Home"><h1>Home</h1></section>', encoding="utf-8"
        )
        result = self.run_hook()
        self.assertEqual(result.returncode, 1)
        self.assertIn("ROUTE_SHELL", result.stdout)

    def test_content_plan_rejects_blank_required_items(self) -> None:
        self.write_shared_jsons()
        plan_path = self.sketch / "prototype-content-plan.json"
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
        plan["pages"][0]["rules"] = [""]
        plan_path.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
        (self.sketch / "prototype.html").write_text(self.complete_page(), encoding="utf-8")
        result = self.run_hook()
        self.assertEqual(result.returncode, 1)
        self.assertIn("CONTENT_PAGE_INCOMPLETE", result.stdout)

    def test_complete_simple_prototype_passes(self) -> None:
        self.write_shared_jsons()
        (self.sketch / "prototype.html").write_text(self.complete_page(), encoding="utf-8")
        result = self.run_hook()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('"status": "passed"', result.stdout)

    def test_shared_design_artifacts_require_full_schema(self) -> None:
        self.write_shared_jsons()
        (self.sketch / "design-source-manifest.json").write_text(
            json.dumps({"token_digest": "digest-1"}), encoding="utf-8"
        )
        (self.sketch / "prototype.html").write_text(self.complete_page(), encoding="utf-8")
        result = self.run_hook()
        self.assertEqual(result.returncode, 1)
        self.assertIn("DESIGN_SOURCE_SCHEMA", result.stdout)

    def test_invalid_utf8_json_returns_structured_finding(self) -> None:
        self.write_shared_jsons()
        (self.sketch / "design-source-manifest.json").write_bytes(b"\xff\xfe")
        (self.sketch / "prototype.html").write_text(self.complete_page(), encoding="utf-8")
        result = self.run_hook()
        self.assertEqual(result.returncode, 1)
        self.assertIn("JSON_ARTIFACT_INVALID", result.stdout)
        self.assertNotIn("Traceback", result.stderr)

    def test_simple_dead_button_is_not_an_interaction(self) -> None:
        self.write_shared_jsons()
        dead = self.complete_page().replace(' data-action="submit"', "")
        (self.sketch / "prototype.html").write_text(dead, encoding="utf-8")
        result = self.run_hook()
        self.assertEqual(result.returncode, 1)
        self.assertIn("interactions=0", result.stdout)

    def test_scaffold_page_without_trace_attributes_fails(self) -> None:
        self.write_shared_jsons()
        page = self.sketch / "prototype" / "src" / "pages" / "Home.tsx"
        page.parent.mkdir(parents=True)
        page.write_text("export default () => <main><h1>Home</h1><button>Go</button></main>", encoding="utf-8")
        result = self.run_hook()
        self.assertEqual(result.returncode, 1)
        self.assertIn("SCAFFOLD_ROUTE_SHELL", result.stdout)

    def test_scaffold_trace_page_must_match_planned_heading(self) -> None:
        self.write_shared_jsons()
        page = self.sketch / "prototype" / "src" / "pages" / "Home.tsx"
        page.parent.mkdir(parents=True)
        page.write_text(
            """export default function Home() { return <section data-trace-page="Wrong">
<h1>Home</h1><article data-trace-ref="a">套餐</article><article data-trace-ref="b">日期</article>
<form data-trace-ref="c"><input /></form><ul><li>规则</li></ul><table><tbody><tr><td>验收</td></tr></tbody></table>
<button onClick={() => true}>确认</button></section> }""",
            encoding="utf-8",
        )
        result = self.run_hook()
        self.assertEqual(result.returncode, 1)
        self.assertIn("SCAFFOLD_ROUTE_SHELL", result.stdout)
        self.assertIn("trace_heading=False", result.stdout)

    def test_scaffold_placeholder_attribute_is_not_shell_text(self) -> None:
        self.write_shared_jsons()
        page = self.sketch / "prototype" / "src" / "pages" / "Home.tsx"
        page.parent.mkdir(parents=True)
        page.write_text(
            """export default function Home() { return <section data-trace-page="Home">
<h1>Home</h1><article data-trace-ref="a">套餐</article><article data-trace-ref="b">日期</article>
<form data-trace-ref="c"><input placeholder="Account name" /></form><ul><li>规则</li></ul>
<table><tbody><tr><td>验收</td></tr></tbody></table><button onClick={() => true}>确认</button>
</section> }""",
            encoding="utf-8",
        )
        result = self.run_hook()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_scaffold_does_not_count_content_after_route_root(self) -> None:
        self.write_shared_jsons()
        page = self.sketch / "prototype" / "src" / "pages" / "Home.tsx"
        page.parent.mkdir(parents=True)
        page.write_text(
            """export default function Home() { return <>
<section data-trace-page="Home"><h1>Home</h1></section>
<section><article data-trace-ref="a">套餐</article><article data-trace-ref="b">日期</article>
<form data-trace-ref="c"><input /></form><ul><li>规则</li></ul>
<table><tbody><tr><td>验收</td></tr></tbody></table><button onClick={() => true}>确认</button></section>
</> }""",
            encoding="utf-8",
        )
        result = self.run_hook()
        self.assertEqual(result.returncode, 1)
        self.assertIn("SCAFFOLD_ROUTE_SHELL", result.stdout)
        self.assertIn("trace_refs=0", result.stdout)

    def test_pencil_manifest_without_export_fails(self) -> None:
        self.write_shared_jsons()
        pencil = self.sketch / "pencil"
        pencil.mkdir()
        manifest = {
            "mode": "pencil-mcp",
            "token_digest": "digest-1",
            "visual_audit": {"status": "passed"},
            "pages": [{"pmcontext_heading": "Home", "screen_id": "screen-1", "trace_uuid": "Home#screen"}],
            "interactions": [{"from": "screen-1", "to": "screen-1", "source": "Home#续费"}],
            "components": [{"name": "button", "source": "Home#续费"}],
            "component_coverage": {name: True for name in ("button", "card", "table", "form", "navigation", "modal_drawer")},
            "exports": [],
            "status": "passed",
        }
        (pencil / "pencil-prototype-manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        result = self.run_hook()
        self.assertEqual(result.returncode, 1)
        self.assertIn("PENCIL_EXPORT_MISSING", result.stdout)

    def test_pencil_manifest_requires_contract_metadata(self) -> None:
        self.write_shared_jsons()
        pencil = self.sketch / "pencil"
        pencil.mkdir()
        manifest = {
            "mode": "pencil-mcp",
            "status": "passed",
            "token_digest": "digest-1",
            "visual_audit": {"status": "passed"},
            "pages": [{"pmcontext_heading": "Home", "screen_id": "screen-1", "trace_uuid": "Home#screen"}],
            "interactions": [{"from": "screen-1", "to": "screen-1", "source": "Home#续费"}],
            "component_coverage": {name: True for name in ("button", "card", "table", "form", "navigation", "modal_drawer")},
            "exports": ["artifact-1"],
        }
        (pencil / "pencil-prototype-manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        result = self.run_hook()
        self.assertEqual(result.returncode, 1)
        self.assertIn("PENCIL_SCHEMA", result.stdout)

    def test_pencil_fallback_manifest_allows_valid_local_output(self) -> None:
        self.write_shared_jsons()
        (self.sketch / "prototype.html").write_text(self.complete_page(), encoding="utf-8")
        pencil = self.sketch / "pencil"
        pencil.mkdir()
        (pencil / "pencil-prototype-manifest.json").write_text(
            json.dumps({"mode": "pencil-mcp", "status": "fallback-local", "fallback_reason": "export unavailable"}),
            encoding="utf-8",
        )
        result = self.run_hook()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_complete_pencil_manifest_passes(self) -> None:
        self.write_shared_jsons()
        pencil = self.sketch / "pencil"
        pencil.mkdir()
        manifest = {
            "mode": "pencil-mcp",
            "status": "passed",
            "design_profile": "sketch/prototype-design-profile.json",
            "design_source_manifest": "sketch/design-source-manifest.json",
            "token_digest": "digest-1",
            "style_family": "Trust First",
            "component_coverage": {name: True for name in ("button", "card", "table", "form", "navigation", "modal_drawer")},
            "design_violation_count": 0,
            "visual_audit": {"status": "passed", "contrast_failures": 0, "invisible_interactive_count": 0},
            "ue_coverage": {"primary_cta_pages": 1, "state_feedback_pages": 1, "rule_visible_pages": 1, "error_recovery_pages": 1},
            "pages": [{"pmcontext_heading": "Home", "screen_id": "screen-1", "trace_uuid": "Home#screen"}],
            "components": [{"name": "button", "source": "Home#续费"}],
            "interactions": [{"from": "screen-1", "to": "screen-1", "source": "Home#续费"}],
            "exports": [{"artifact_id": "pencil-artifact-1"}],
        }
        (pencil / "pencil-prototype-manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        result = self.run_hook()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_visual_report_with_zero_inspection_fails(self) -> None:
        self.write_shared_jsons()
        report_path = self.sketch / "visual-audit-report.json"
        report = json.loads(report_path.read_text(encoding="utf-8"))
        for value in report["checks"].values():
            value["passed"] = 0
        report_path.write_text(json.dumps(report), encoding="utf-8")
        (self.sketch / "prototype.html").write_text(self.complete_page(), encoding="utf-8")
        result = self.run_hook()
        self.assertEqual(result.returncode, 1)
        self.assertIn("VISUAL_CHECK_EMPTY", result.stdout)

    def test_need_auto_missing_summaries_fails(self) -> None:
        self.write_shared_jsons()
        (self.sketch / "prototype.html").write_text(self.complete_page(), encoding="utf-8")
        result = self.run_hook("pm-need", auto=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("AUTO_ARTIFACT_MISSING", result.stdout)

    def test_need_hook_requires_auto_flag(self) -> None:
        result = self.run_hook("pm-need")
        self.assertEqual(result.returncode, 2)
        self.assertIn("AUTO_FLAG_REQUIRED", result.stdout)

    def test_visual_audit_emits_hook_compatible_report(self) -> None:
        prototype = self.sketch / "prototype.html"
        prototype.write_text(
            """<style>
:root { --color-text:#111827; --color-text-secondary:#374151; --color-text-muted:#4b5563;
--color-bg:#ffffff; --color-bg-secondary:#f3f4f6; --color-bg-tertiary:#e5e7eb;
--color-primary:#1d4ed8; --color-on-primary:#ffffff; --color-border:#6b7280;
--color-success:#10b981; --color-on-success:#052e16;
--color-danger:#ef4444; --color-on-danger:#280000;
--color-warning:#f59e0b; --color-on-warning:#422006; }
button:focus-visible { outline: 3px solid #1d4ed8; }
</style><button type="button">确认</button>""",
            encoding="utf-8",
        )
        result = subprocess.run(
            [sys.executable, str(VISUAL_AUDIT), "--token-digest", "digest-1", str(prototype)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["token_digest"], "digest-1")
        self.assertEqual(set(report["checks"]), {
            "token_contrast_pairs",
            "interactive_visibility",
            "state_visibility",
            "focus_visible",
            "empty_clickable_overlay",
        })
        self.assertTrue(all(value["passed"] > 0 for value in report["checks"].values()))

    def test_visual_audit_rejects_invisible_state_colors(self) -> None:
        prototype = self.sketch / "prototype.html"
        prototype.write_text(
            """<style>
:root { --color-text:#111827; --color-bg:#ffffff; --color-primary:#1d4ed8;
--color-on-primary:#ffffff; --color-success:#ffffff; --color-on-success:#ffffff; }
button:focus-visible { outline: 3px solid #1d4ed8; }
</style><button type="button">确认</button>""",
            encoding="utf-8",
        )
        result = subprocess.run(
            [sys.executable, str(VISUAL_AUDIT), "--token-digest", "digest-1", str(prototype)],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 1)
        report = json.loads(result.stdout)
        self.assertGreater(report["checks"]["state_visibility"]["failed"], 0)
        self.assertIn("LOW_STATE_CONTRAST", result.stdout)

    def test_visual_audit_rejects_unparseable_required_colors(self) -> None:
        prototype = self.sketch / "prototype.html"
        prototype.write_text(
            """<style>:root { --color-text:oklch(20% .02 250); --color-bg:oklch(98% .01 250);
--color-primary:#1d4ed8; --color-on-primary:#ffffff; --color-success:#10b981;
--color-on-success:#052e16; } button:focus-visible { outline:3px solid #1d4ed8; }</style>
<button data-action="submit">确认</button>""",
            encoding="utf-8",
        )
        result = subprocess.run(
            [sys.executable, str(VISUAL_AUDIT), "--token-digest", "digest-1", str(prototype)],
            cwd=ROOT, text=True, capture_output=True,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("UNPARSEABLE_COLOR", result.stdout)

    def test_visual_audit_rejects_hidden_interactive_rule(self) -> None:
        prototype = self.sketch / "prototype.html"
        prototype.write_text(
            """<style>:root { --color-text:#111827; --color-bg:#ffffff; --color-primary:#1d4ed8;
--color-on-primary:#ffffff; --color-success:#10b981; --color-on-success:#052e16; }
button { display:none; color:#fff; background:#fff; } button:focus-visible { outline:3px solid #1d4ed8; }</style>
<button data-action="submit">确认</button>""",
            encoding="utf-8",
        )
        result = subprocess.run(
            [sys.executable, str(VISUAL_AUDIT), "--token-digest", "digest-1", str(prototype)],
            cwd=ROOT, text=True, capture_output=True,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("HIDDEN_INTERACTIVE_STYLE", result.stdout)

    def test_visual_audit_rejects_class_rules_applied_to_control(self) -> None:
        prototype = self.sketch / "prototype.html"
        prototype.write_text(
            """<style>:root { --color-text:#111827; --color-bg:#ffffff; --color-primary:#1d4ed8;
--color-on-primary:#ffffff; --color-success:#10b981; --color-on-success:#052e16; }
.hidden { display:none; } .cta { color:#fff; background:#fff; }
button:focus-visible { outline:3px solid #1d4ed8; }</style>
<button class="hidden cta" data-action="submit">确认</button>""",
            encoding="utf-8",
        )
        result = subprocess.run(
            [sys.executable, str(VISUAL_AUDIT), "--token-digest", "digest-1", str(prototype)],
            cwd=ROOT, text=True, capture_output=True,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("HIDDEN_INTERACTIVE_STYLE", result.stdout)
        self.assertIn("LOW_CSS_INTERACTIVE_CONTRAST", result.stdout)

    def test_legacy_visual_audit_rejects_empty_input(self) -> None:
        result = subprocess.run(
            [sys.executable, str(VISUAL_AUDIT), "/dev/null"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("INPUT_MISSING_OR_EMPTY", result.stdout)


if __name__ == "__main__":
    unittest.main()
