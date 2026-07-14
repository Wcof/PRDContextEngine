# PMSkill Runtime Gate Design

## Goal

Make the repository contract and runtime result agree: invalid or incomplete PMSkill artifacts must fail deterministically before an Agent reports completion, while the same checks remain runnable in CI.

## Scope

This remediation covers the audit findings:

- make `/pm-need` default and `--auto` modes unambiguous;
- remove Hybrid-to-Human-only automatic back-calls;
- enforce prototype anti-shell and visual checks for Simple, Scaffold, and Pencil outputs;
- repair bucket README coverage and invocation classification;
- require a formal eval file with at least three scenarios for every Skill;
- make frontmatter descriptions trigger-only and `Use when...`-first;
- replace keyword-only confidence with executable checks;
- add one runtime post-generation Hook without adding Git hooks.

Existing user changes in the dirty worktree remain in place and are edited only where this remediation overlaps them.

## Architecture

Use one executable Python entry point, `hooks/post_generation.py`, as both the Harness Hook and the artifact validator. It uses only the Python standard library, accepts the generated artifact root and completed skill, prints a JSON report, and exits non-zero on a hard-gate failure.

CI invokes the same file through deterministic fixture tests. `scripts/validate_pmskill.py` remains the repository-structure validator and gains checks for Hook presence, bucket README completeness/classification, eval coverage, and trigger-only frontmatter. No pre-commit or pre-push hook is added.

This keeps the Harness/Skill boundary from ADR 0009: Skills declare when the Hook must run and how failure is reported; the Hook owns mechanical enforcement.

## Hook Interface

```text
python3 hooks/post_generation.py \
  --skill pm-sketch|pm-need \
  --artifact-root <path> \
  [--auto]
```

Output is JSON with `status`, `skill`, `artifact_root`, `checks`, and `findings`. Exit codes:

- `0`: all applicable hard gates passed;
- `1`: artifacts exist but violate one or more hard gates;
- `2`: invocation is invalid or the artifact root/input cannot be inspected.

The Hook is fail-closed: empty files, missing paths, unparseable JSON, absent required fields, and zero inspected pages are failures.

## Validation Rules

### Shared

- `pm-context.md` exists and is non-empty.
- Every required JSON artifact parses to an object.
- Token digests agree across design source, design profile, visual report, and Pencil manifest when present.
- A report cannot pass with zero inspected tokens/pages/checks.

### `pm-sketch`

- `prototype-content-plan.json`, `prototype-design-profile.json`, `design-source-manifest.json`, and `visual-audit-report.json` exist and satisfy their required schemas.
- The content plan has at least one page; every page has a job, scenario, facts/rules/acceptances/actions/states, at least one action, and trace references.
- At least one supported implementation is inspectable:
  - Simple HTML: every planned page has `data-trace-page`, at least three `data-trace-ref` elements, at least five business elements, an interaction, and no shell placeholder.
  - Scaffold: the same per-page checks are applied to route/page source files, not only build success.
  - Pencil: the manifest covers every planned page and records source anchors, interactions, matching token digest, passed visual audit, and an export/persist artifact.
- `visual-audit-report.json.status` is `passed`, required check groups exist, and each group inspected at least one item with zero failures.

### `/pm-need --auto`

- Run all shared and `pm-sketch` checks.
- Require the collect/refine/premortem process files, both PRDs, stories, five sketch views, four summary documents, and `INDEX.md`.
- Any missing artifact prevents a completion marker but does not delete successful artifacts.

## Skill Contract Corrections

- Default refine mode asks for confirmation of all eight dimension-level decisions, one question at a time, using `推荐/依据/备选`. Existing evidence becomes the recommendation instead of suppressing the dimension question; redundant factual subquestions remain forbidden.
- `--auto` never pauses for high-entropy input. It uses available sources, marks unresolved dimensions `[待确认]`, lowers confidence, and proceeds to PRD/prototype/summary.
- `pm-prd` and `pm-sketch` never automatically invoke Human-only `pm-need`. Missing PMContext produces a recoverable STOP with the exact human command to run.
- Local Simple and Scaffold routes must carry DOM trace attributes. Pencil screens use equivalent manifest source anchors because they are not DOM routes.
- Every affected Skill invokes the post-generation Hook before reporting success; Hook failure is printed verbatim and completion is withheld.

## Documentation and Eval Consistency

- Each bucket has a README and lists every Skill once under the invocation class defined by frontmatter. Hybrid entries are listed under Model-invoked and labelled Hybrid.
- Every Skill has a formal eval file with at least three scenarios covering normal, boundary/failure, and counterexample behavior.
- Eval documentation reports generated counts from repository reality; `--live` remains explicitly described as unavailable until implemented.
- Frontmatter descriptions contain only trigger conditions and begin with `Use when`.

## Error Handling

The Hook accumulates findings instead of stopping at the first artifact error, so the Agent receives one repair list. Unexpected filesystem/JSON errors become deterministic findings without a traceback in normal output. The Hook never edits generated artifacts.

## Testing

Use standard-library `unittest` and temporary directories.

Required failing baselines before implementation:

- empty and nonexistent prototypes currently pass visual audit;
- a route-only Simple prototype currently has no executable repository gate;
- Scaffold pages without trace attributes currently pass structural validation;
- missing eval files and bucket README entries currently pass `validate_pmskill.py`;
- `--auto` pause language and Hybrid-to-Human-only back-calls currently pass validation.

Required passing cases after implementation:

- a minimal complete Simple prototype passes;
- equivalent broken Simple, Scaffold, Pencil, and `pm-need --auto` fixtures fail with stable finding codes;
- all 52 Skill eval files contain at least three scenarios;
- repository structural validation, Hook unit tests, JSON parsing, and shell syntax checks pass.

## Non-goals

- no Git Hook installation;
- no new dependency or Hook framework;
- no browser automation dependency in the deterministic baseline;
- no automatic repair or mutation of user artifacts;
- no redesign of existing prototype templates beyond closing audited gaps.
