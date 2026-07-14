# PMSkill Runtime Gate Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add one fail-closed post-generation Hook and align PMSkill contracts, documentation, eval coverage, and CI with the audited behavior.

**Architecture:** `hooks/post_generation.py` is the only runtime artifact gate and uses Python standard library APIs. `scripts/validate_pmskill.py` remains the repository structure gate. Unit tests cover runtime artifacts; structural validation covers skill metadata, routes, README inventory, and eval completeness.

**Tech Stack:** Python 3.11 standard library, `unittest`, Bash/GitHub Actions, Markdown and JSON Skill assets.

---

### Task 1: Establish failing runtime and repository gates

**Files:**
- Create: `tests/test_post_generation_hook.py`
- Create: `tests/test_repository_contract.py`
- Read: `scripts/visual_audit_prototype.py`
- Read: `scripts/validate_pmskill.py`

- [x] **Step 1: Write runtime Hook tests before the Hook exists**

Create `tests/test_post_generation_hook.py` using `unittest`, `tempfile.TemporaryDirectory`, and `subprocess.run`. Include these assertions:

```python
def test_missing_artifact_root_is_invocation_error(self):
    result = self.run_hook("pm-sketch", self.root / "missing")
    self.assertEqual(result.returncode, 2)
    self.assertIn("ARTIFACT_ROOT_MISSING", result.stdout)

def test_empty_prototype_fails_closed(self):
    self.write_shared_jsons(page_count=1)
    (self.sketch / "prototype.html").write_text("", encoding="utf-8")
    result = self.run_hook("pm-sketch", self.root)
    self.assertEqual(result.returncode, 1)
    self.assertIn("PROTOTYPE_EMPTY", result.stdout)

def test_route_shell_fails(self):
    self.write_shared_jsons(page_count=1)
    (self.sketch / "prototype.html").write_text(
        '<section data-trace-page="Home"><h1>Home</h1></section>', encoding="utf-8"
    )
    result = self.run_hook("pm-sketch", self.root)
    self.assertEqual(result.returncode, 1)
    self.assertIn("ROUTE_SHELL", result.stdout)

def test_complete_simple_prototype_passes(self):
    self.write_shared_jsons(page_count=1)
    (self.sketch / "prototype.html").write_text(self.complete_page("Home"), encoding="utf-8")
    result = self.run_hook("pm-sketch", self.root)
    self.assertEqual(result.returncode, 0, result.stdout)
```

Add equivalent negative tests for Scaffold missing trace attributes, Pencil missing export/token coverage, visual reports with zero inspected checks, and `pm-need --auto` missing summaries.

- [x] **Step 2: Write repository contract tests**

Create `tests/test_repository_contract.py` with direct repository invariants that currently fail:

```python
def test_post_generation_hook_exists(self):
    self.assertTrue((ROOT / "hooks/post_generation.py").is_file())

def test_every_skill_has_three_formal_evals(self):
    for skill in (ROOT / "skills").glob("*/*/SKILL.md"):
        name = next(line.removeprefix("name: ") for line in skill.read_text().splitlines() if line.startswith("name: "))
        eval_path = ROOT / "evals" / f"{name}.json"
        self.assertTrue(eval_path.is_file(), name)
        self.assertGreaterEqual(len(json.loads(eval_path.read_text())), 3, name)

def test_descriptions_are_trigger_only(self):
    for skill in (ROOT / "skills").glob("*/*/SKILL.md"):
        description = next(line.removeprefix("description: ") for line in skill.read_text().splitlines() if line.startswith("description: "))
        self.assertTrue(description.startswith("Use when "), skill)
```

Add bucket README coverage/classification and forbidden-contract assertions for auto pauses and Hybrid-to-Human-only back-calls. The RED reasons must be missing Hook/incomplete eval and contract drift, not Python import errors.

- [x] **Step 3: Run RED tests**

Run: `python3 -m unittest tests.test_post_generation_hook tests.test_repository_contract -v`

Expected: runtime tests fail because `hooks/post_generation.py` does not exist; repository contract assertions fail for missing Hook/evals, stale descriptions, README inventory, and contradictory Skill text.

### Task 2: Implement the single post-generation Hook

**Files:**
- Create: `hooks/post_generation.py`
- Modify: `scripts/visual_audit_prototype.py`
- Test: `tests/test_post_generation_hook.py`

- [x] **Step 1: Implement fail-closed CLI and report model**

Use dataclasses and argparse with this interface:

```python
@dataclass
class Finding:
    code: str
    path: str
    detail: str

def validate(skill: str, artifact_root: Path, auto: bool = False) -> tuple[int, dict[str, object]]:
    if not artifact_root.is_dir():
        return 2, report("invalid", skill, artifact_root, [Finding("ARTIFACT_ROOT_MISSING", str(artifact_root), "artifact root is not a directory")])
    findings = validate_shared(artifact_root)
    if skill in {"pm-sketch", "pm-need"}:
        findings.extend(validate_sketch(artifact_root))
    if skill == "pm-need" and auto:
        findings.extend(validate_need_auto(artifact_root))
    return (1 if findings else 0), report("failed" if findings else "passed", skill, artifact_root, findings)
```

Reject unsupported skills with exit code 2. Print one JSON object and no traceback for expected validation failures.

- [x] **Step 2: Implement shared JSON and digest checks**

Require non-empty `pm-context.md`; parse content plan, design profile, design source manifest, and visual report as JSON objects. Require non-empty page arrays, required page fields, required visual check groups, positive inspected counts, zero failures, and equal non-empty token digests.

- [x] **Step 3: Implement per-output anti-shell checks**

Use `html.parser.HTMLParser` for Simple HTML. Track each `data-trace-page` container, `data-trace-ref` count, business element count (`article`, `button`, `input`, `select`, `textarea`, `table`, `ul`, `ol`, `form`), interaction count, text length, and shell words.

For Scaffold, scan `src/pages/**/*.{tsx,jsx,html}` as text and require every planned heading to occur in a `data-trace-page` attribute with at least three trace attributes and one interactive element in that page file.

For Pencil, validate manifest `pages`, `interactions`, `exports`, `token_digest`, `component_coverage`, and `visual_audit.status`.

- [x] **Step 4: Make legacy visual audit fail closed**

In `scripts/visual_audit_prototype.py`, fail with `INPUT_MISSING_OR_EMPTY` when no readable content is collected and fail with `NO_VISUAL_TOKENS_INSPECTED` when no required token pair/control is inspected. Keep its existing contrast math.

- [x] **Step 5: Run GREEN runtime tests**

Run: `python3 -m unittest tests.test_post_generation_hook -v`

Expected: all runtime Hook tests pass, including the original empty/nonexistent false-positive cases.

### Task 3: Strengthen repository validation and repair inventories

**Files:**
- Modify: `scripts/validate_pmskill.py`
- Modify: `skills/setup/README.md`
- Modify: `skills/discovery/README.md`
- Modify: `skills/delivery/README.md`
- Create: `skills/utility/README.md`
- Modify: `skills/visualization/README.md`
- Test: `tests/test_repository_contract.py`

- [x] **Step 1: Add deterministic inventory checks**

Extend `validate_pmskill.py` to require:

```python
if not desc.startswith("Use when "):
    fail(f"{path} description must start with 'Use when '")

eval_path = ROOT / "evals" / f"{name}.json"
if not eval_path.exists() and name != "pm-legal":
    fail(f"missing formal eval for {name}")

if len(data) < 3:
    fail(f"{path} must contain at least 3 scenarios")
```

Also require `hooks/post_generation.py`, verify every bucket has a README, every Skill appears exactly once in its bucket README, and Human-only entries are the only entries under User-invoked.

- [x] **Step 2: Repair bucket README inventories**

Move `pm-prd`, `pm-handoff`, and `pm-sketch` into Model-invoked, label visible model-reachable entries as Hybrid, add `pm-stakeholder` and `pm-journey`, and create Utility README entries for `pm-legal`, `pm-conflict-resolver`, and Hybrid `pm-summary`.

- [x] **Step 3: Run repository contract test**

Run: `python3 -m unittest tests.test_repository_contract -v`

Expected: Hook-presence and bucket inventory assertions pass; description/eval/Skill-contract assertions remain RED until Task 4.

### Task 4: Align Skill contracts and formal eval coverage

**Files:**
- Modify: `skills/discovery/pm-need/SKILL.md`
- Modify: `skills/discovery/pm-refine/SKILL.md`
- Modify: `skills/delivery/pm-prd/SKILL.md`
- Modify: `skills/visualization/pm-sketch/SKILL.md`
- Modify: `skills/visualization/pm-sketch/references/prototype-templates.md`
- Modify: `AGENTS.md`
- Modify: `CLAUDE.md`
- Modify: `CONTEXT.md`
- Modify: all `skills/*/*/SKILL.md` frontmatter descriptions
- Create: missing `evals/pm-*.json` files
- Modify: `evals/README.md`
- Test: `tests/test_repository_contract.py`

- [x] **Step 1: Capture current behavioral pressure failures**

Before editing Skill text, run three pressure scenarios against the current instructions: high-entropy `--auto`, default refine with strong source evidence, and Scaffold generation under time pressure. Record whether the Agent pauses, skips a dimension question, or omits trace attributes.

- [x] **Step 2: Remove dual-mode contradictions and reverse calls**

Make `--auto` continue with `[待确认]` instead of pausing. Require one confirmation question for each of eight dimension-level decisions in default mode while suppressing redundant factual subquestions. Replace `pm-prd`/`pm-sketch` automatic calls to Human-only `pm-need` with a recoverable STOP and exact human command.

- [x] **Step 3: Apply Hook and anti-shell contracts**

Require `python3 hooks/post_generation.py --skill pm-sketch --artifact-root <产物目录>` before sketch completion and add `--skill pm-need --auto` at the auto-chain end. Add Scaffold route trace/content checks; keep Pencil manifest source anchors as the non-DOM equivalent.

- [x] **Step 4: Rewrite frontmatter descriptions mechanically**

For each Skill, retain its existing English `Use when...` trigger clause and remove the preceding workflow summary. Ensure the result starts with `Use when `, stays under 500 characters, and does not describe execution steps.

- [x] **Step 5: Add missing formal evals**

Add three scenarios per missing Skill: normal path, missing/invalid input, and a counterexample from its anti-pattern table. Update existing pm-need/refine/sketch scenarios for zero-intervention auto mode, eight dimension confirmations, Scaffold/Pencil anti-shell, and Hook failure behavior.

- [x] **Step 6: Run structural GREEN test**

Run: `python3 scripts/validate_pmskill.py`

Expected: `PASS: PMSkill structural constraints hold`.

Run: `python3 -m unittest tests.test_repository_contract -v`

Expected: repository contract tests pass.

### Task 5: Wire CI and verify the full remediation

**Files:**
- Modify: `.github/workflows/ci.yml`
- Modify: `README.md`
- Modify: `README.en.md`
- Modify: `evals/README.md`
- Verify: all files changed by Tasks 1-4

- [x] **Step 1: Add the test command to CI**

Add before structural eval checks:

```yaml
- name: Run deterministic unit tests
  run: |
    python3 -m unittest discover -s tests -v
```

- [x] **Step 2: Correct public documentation**

Document the post-generation Hook command, fail-closed behavior, and that `--live` remains a placeholder. Remove claims contradicted by repository reality and list all 52 formal evals via the eval README inventory.

- [x] **Step 3: Run full verification**

Run:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_pmskill.py
bash -n evals/run-evals.sh
bash evals/run-evals.sh --dry-run
python3 scripts/visual_audit_prototype.py /dev/null
git diff --check
```

Expected: unit tests and structural checks pass; visual audit on `/dev/null` exits non-zero with a stable failure code; `git diff --check` produces no output.

- [x] **Step 4: Review requirement coverage**

Compare the final diff against `docs/superpowers/specs/2026-07-14-pmskill-runtime-gate-design.md`. Confirm each scope bullet has either an executable test or deterministic validator check and that no unrelated user changes were removed.
