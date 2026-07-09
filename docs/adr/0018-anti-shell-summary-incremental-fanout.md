# ADR 0018: Prototype Anti-Shell, Summary Auto-Finalizer, and Incremental Fan-out

## Status

Accepted

## Context

Recent usage exposed three failure modes:

1. Some models, especially long-instruction runtimes, can satisfy `/pm-sketch --prototype` superficially by generating a single HTML file with hash routes and empty page bodies.
2. The product artifacts are intentionally decomposed by skill, but users expect a few reading-oriented aggregate documents after a 0→1 run.
3. After a 0→1 prototype exists, a later `/pm-need 增加页面` must continue the product incrementally instead of stopping at PMContext or silently finding no marked gaps.

The previous design had most of the pieces, but too many guarantees lived only as prose in large entry skills. That made constraints easy to forget and hard to validate.

## Decision

### 1. Add a hard Prototype Content Plan before any prototype implementation

`/pm-sketch --prototype` must first write:

```text
docs/pm-context/sketch/prototype-content-plan.json
```

The file compiles PMContext pages into renderable content: page id, primary job, scenario, facts, rules, acceptances, fields, actions, states, and trace refs. Pencil MCP, Simple HTML, and Scaffold implementations must render from this content plan. A routes array with only `id/title` is invalid.

Each page must render business content with `data-trace-page` and at least three `data-trace-ref` elements. Route-only shells, TODO pages, placeholders, and title-only sections fail the V1 anti-shell gate.

### 2. Make `/pm-summary --auto` a read-only finalizer

`/pm-summary` remains a Hybrid Entry and remains read-only, but it is now part of the `/pm-need --auto` tail and incremental Fan-out. It does not participate in PM Thinking Loop and never modifies original artifacts. It only overwrites `SUMMARY-*.md` and `INDEX.md`.

### 3. Make incremental `/pm-need` argument-first and view-refreshing

When PMContext exists, `/pm-need` must first classify the new user input as add / update / complete. It must not scan markers first and exit when no markers exist.

After a PMContext delta lands, the default is:

```text
/pm-prd --auto --incremental
→ /pm-stories --auto --incremental
→ /pm-sketch --prototype --auto --incremental --no-fallback
→ /pm-summary --auto
```

Only `--context-only` skips downstream view refresh.

## Consequences

- The visible skill count stays stable: 6 visible / 52 total.
- `pm-sketch` still owns prototype orchestration, but the actual content contract is now a separate Level 3 reference and a deterministic artifact.
- `/pm-need --auto` creates both detailed original artifacts and high-level summary documents by default.
- Existing prototypes are preserved in incremental mode; new pages are appended and route/menu/data are patched.
- Structural validation now checks for anti-shell, summary auto-finalizer, incremental Fan-out, and mojibake filenames.
