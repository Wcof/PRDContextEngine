# PMSkill

Skills are organized into bucket folders under `skills/`:

- `setup/` — 初始化配置（含知识库路径）
- `discovery/` — 需求发现（collect + refine → PMContext，全自动，PM 只需审计）
- `delivery/` — 交付（PRD 生成 + Pre-Mortem 风险分析）
- `visualization/` — 可视化（草图生成）
- `utility/` — 通用支撑（汇总、合规、局部冲突修复）

Every skill must have a reference in the top-level `README.md`. Each bucket folder has a `README.md` that lists every skill with a one-line description, grouped into **User-invoked** and **Model-invoked**.

Every `SKILL.md` is either user-invoked (`disable-model-invocation: true`, reachable only by the human) or model-invoked (model- or user-reachable). A user-invoked skill may invoke model-invoked skills, but never another user-invoked one.

**Key change**: /pm-need supports dual refine modes. Default mode (追问模式): Agent asks PM one dimension at a time, each question with a 3-part recommended answer. `--auto` mode (自主推断模式): Agent auto-infers all 8 dimensions, zero PM involvement, advances straight to PRD + prototype + summary docs. PM's intervention points: per-dimension answers in default mode, audit gate in `--auto` mode.

## Domain docs

Single-context: `CONTEXT.md` + `docs/adr/` at repo root.


**Incremental change**: When PMContext already exists, /pm-need must use Argument-first incremental routing and default Downstream Fan-out to refresh PRD, stories, sketch prototype, and summary docs. Use `--context-only` only when the user wants to skip downstream views.

**Sketch anti-shell rule**: /pm-sketch --prototype must first create `sketch/prototype-content-plan.json`; all route pages must render business content with `data-trace-page` and `data-trace-ref`, not just navigation shells.

## Prototype Design Profile

`/pm-sketch --prototype` must read `skills/visualization/pm-sketch/references/design-style.md` and write `docs/pm-context/sketch/prototype-design-profile.json` before Pencil MCP / Simple / Scaffold implementation. Pencil MCP briefs and manifests must carry this profile; local prototypes must map it to CSS tokens, layout patterns, and UE checks.

## Runtime Completion Gate

`/pm-sketch --prototype` and `/pm-need --auto` must run `python3 hooks/post_generation.py` with their skill name and configured artifact root before claiming completion. A non-zero exit is fail-closed: report findings, keep the run incomplete, fix, and rerun the Hook.
