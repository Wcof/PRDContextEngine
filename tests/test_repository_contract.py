from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def skill_name(path: Path) -> str:
    return next(
        line.removeprefix("name: ")
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.startswith("name: ")
    )


class RepositoryContractTests(unittest.TestCase):
    @classmethod
    def skill_paths(cls) -> list[Path]:
        return sorted((ROOT / "skills").glob("*/*/SKILL.md"))

    def test_post_generation_hook_exists(self) -> None:
        self.assertTrue((ROOT / "hooks" / "post_generation.py").is_file())

    def test_every_skill_has_three_formal_evals(self) -> None:
        for skill in self.skill_paths():
            name = skill_name(skill)
            eval_path = ROOT / "evals" / f"{name}.json"
            self.assertTrue(eval_path.is_file(), name)
            if eval_path.is_file():
                data = json.loads(eval_path.read_text(encoding="utf-8"))
                self.assertGreaterEqual(len(data), 3, name)

    def test_descriptions_are_trigger_only(self) -> None:
        for skill in self.skill_paths():
            description = next(
                line.removeprefix("description: ")
                for line in skill.read_text(encoding="utf-8").splitlines()
                if line.startswith("description: ")
            )
            self.assertTrue(description.startswith("Use when "), skill)
            self.assertLessEqual(len(description), 500, skill)

    def test_bucket_readmes_cover_every_skill_once(self) -> None:
        for bucket in sorted(path for path in (ROOT / "skills").iterdir() if path.is_dir()):
            readme = bucket / "README.md"
            self.assertTrue(readme.is_file(), bucket.name)
            if not readme.is_file():
                continue
            text = readme.read_text(encoding="utf-8")
            for skill in sorted(bucket.glob("*/SKILL.md")):
                name = skill_name(skill)
                self.assertEqual(len(re.findall(rf"\[{re.escape(name)}\]", text)), 1, name)

    def test_only_human_only_entries_are_documented_as_user_invoked(self) -> None:
        expected = {"pm-setup", "pm-need"}
        actual: set[str] = set()
        for readme in (ROOT / "skills").glob("*/README.md"):
            text = readme.read_text(encoding="utf-8")
            section = text.partition("## User-invoked")[2].partition("## Model-invoked")[0]
            actual.update(re.findall(r"\[([a-z0-9-]+)\]", section))
        self.assertEqual(actual, expected)

    def test_auto_mode_never_pauses_for_entropy(self) -> None:
        text = (ROOT / "skills/discovery/pm-need/SKILL.md").read_text(encoding="utf-8")
        self.assertNotIn("高熵 且 无任何背景源 | 🔴 举手：暂停生成", text)
        self.assertIn("--auto` 模式下 PM 零介入", text)

    def test_hybrid_entries_do_not_call_human_only_need(self) -> None:
        for rel in ("skills/delivery/pm-prd/SKILL.md", "skills/visualization/pm-sketch/SKILL.md"):
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertNotRegex(text, r"自动调用 `/pm-need|调用 `/pm-need \$ARGUMENTS|自动 run `/pm-need")

    def test_scaffold_contract_requires_trace_gate(self) -> None:
        text = (ROOT / "skills/visualization/pm-sketch/references/prototype-templates.md").read_text(encoding="utf-8")
        scaffold = text.partition("### 13.2 Scaffold 模式")[2].partition("### 13.3")[0]
        self.assertIn("data-trace-page", scaffold)
        self.assertIn("data-trace-ref", scaffold)
        self.assertIn("路由空壳", scaffold)

    def test_ci_runs_runtime_and_repository_gates(self) -> None:
        text = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
        self.assertIn("python3 -m unittest", text)
        self.assertIn("tests.test_post_generation_hook", text)
        self.assertIn("tests.test_repository_contract", text)

    def test_live_evals_do_not_silently_downgrade(self) -> None:
        text = (ROOT / "evals/run-evals.sh").read_text(encoding="utf-8")
        self.assertNotIn('MODE="dry-run"\nfi', text)
        self.assertIn("--live is not implemented", text)


if __name__ == "__main__":
    unittest.main()
