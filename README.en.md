# PMSkill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/Skills-49-blue.svg)](#skill-list)
[![CI](https://img.shields.io/badge/CI-passing-brightgreen.svg)](.github/workflows/ci.yml)
[![Spec](https://img.shields.io/badge/Anthropic-Agent%20Skills-orange.svg)](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)

> A Skill toolkit for product managers working in Agents.

From fuzzy ideas or user requests, a single command completes the full pipeline: **PMContext (sole source) → PRD (for AI + for human) → visual sketches + interactive HTML prototype**.

---

## Overview

PMSkill encapsulates the core workflows of product managers in Agent environments into 49 callable Skills, covering three domains: requirement discovery, delivery, and visualization. All Skills follow the [Anthropic Agent Skills specification](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview), using YAML frontmatter progressive disclosure and third-person trigger descriptions.

### Key Features

- **Single Source of Truth**: PMContext is the sole Entity; PRD and sketches are its downstream Views. Downstream Skills read one file to obtain the full picture.
- **Full-Pipeline Automation**: A single command completes collect → refine → PRD → prototype, with a zero-confirmation `--auto` mode.
- **Dual-Form PRD**: An executable PRD for AI (with Agent Context) and a review-friendly PRD for humans.
- **Tech-Stack Awareness**: HTML prototypes auto-adapt to the project's actual tech stack and work offline.
- **Progressive Disclosure**: Three-level loading (Level 1/2/3) with on-demand references to control token cost.
- **Traceability**: Risks are marked inline (`[待确认]` / `[假设]` / `[冲突]`) with single-level traceability.

---

## Quick Start

### 1. Install

```bash
npx skills@latest add Wcof/PMSkill --all
```

### 2. Initialize (once)

```text
/pm-setup
```

### 3. One-Command Full Pipeline (recommended)

```text
/pm-need <requirement>           # Normal mode: refine asks PM dimension by dimension
/pm-need <requirement> --auto    # Zero-confirmation mode: refine auto-infers, fully automatic
```

### 4. Step-by-Step

```text
/pm-need              # Collect → refine Q&A → audit gate
/pm-need --auto       # Collect → refine auto-inference → PRD → prototype
/pm-prd               # Generate PRD from PMContext (for AI + for human)
/pm-prd --auto        # Zero-confirmation: produce PRD directly
/pm-sketch            # Generate all sketches
/pm-sketch --prototype # Generate sketches + interactive HTML prototype
```

---

## Main Flow

```
Fuzzy ideas / user requests
        │
  /pm-need ─── {--auto: zero-confirm} ───→ PMContext (sole Entity)
        │                                   │
  ┌─────┴─────┐                    ┌────────┴────────┐
  │           │                    │                 │
/pm-prd  /pm-premortem       /pm-sketch      /pm-sketch --prototype
  │           │                    │                 │
  ▼           ▼                    ▼                 ▼
prd/*.md  premortem.md       sketch/*.md     prototype.html
```

---

## Skill List

### Setup — Initialization

| Skill | Invocation | Purpose |
|---|---|---|
| `/pm-setup` | user-invoked | First-time project configuration (output dir / language / knowledge base / Agent rules) |

### Discovery — Requirement Discovery

| Skill | Invocation | Purpose |
|---|---|---|
| `/pm-need` | user-invoked | Main entry: collect → refine → audit; `--auto` zero-confirm straight to PRD + prototype |
| `/pm-collect` | model-invoked | Deep scan (code / git / URL / knowledge base), 4-source deduplication |
| `/pm-refine` | model-invoked | 8-dimension inference (P0 user scenarios / boundaries / conflicts → P1 priority / terminology / friction → P2 tech constraints / metrics) |
| `/pm-interview` | model-invoked | Structured user interview script (JTBD + The Mom Test) |
| `/pm-metrics` | model-invoked | North Star metric + Input Metrics constellation |
| `/pm-ost` | model-invoked | Opportunity Solution Tree (OST) |
| `/pm-strategy` | model-invoked | Strategy analysis (SWOT / Porter's Five Forces / Ansoff / Lean Canvas) |
| `/pm-market` | model-invoked | Market analysis (TAM/SAM/SOM + competitor matrix) |
| `/pm-vision` | model-invoked | Product vision + stakeholder communication plan |
| `/pm-grill` | model-invoked | Red-team interrogation (attack load-bearing assumptions) |
| `/pm-persona` | model-invoked | User personas (JTBD-based) |
| `/pm-businessmodel` | model-invoked | Business Model Canvas (BMC) |
| `/pm-positioning` | model-invoked | Value proposition + differentiation positioning |
| `/pm-assumption` | model-invoked | Risk assumption identification + cheapest test |
| `/pm-northstar` | model-invoked | North Star metric deepening |
| `/pm-ideation` | model-invoked | Solution divergence (optimize + explore) |
| `/pm-parallel` | model-invoked | Parallel agent dispatch |
| `/pm-skillauthor` | model-invoked | TDD-style skill authoring |

### Delivery — Delivery

| Skill | Invocation | Purpose |
|---|---|---|
| `/pm-prd` | model-invoked | Orchestrate dual-form PRD output (`--auto` / `--skip-ai` / `--skip-human`) |
| `/pm-aiprd` | model-invoked | AI PRD (executable rules + Agent Context) |
| `/pm-humanprd` | model-invoked | Human PRD (review-friendly) |
| `/pm-premortem` | model-invoked | Pre-Mortem risk analysis |
| `/pm-stories` | model-invoked | User stories (3C + INVEST) |
| `/pm-gtm` | model-invoked | Go-to-market strategy |
| `/pm-experiment` | model-invoked | Hypothesis validation loop |
| `/pm-retro` | model-invoked | Retrospective (Start/Stop/Continue, etc.) |
| `/pm-prioritize` | model-invoked | Prioritization (6 frameworks by scenario) |
| `/pm-pricing` | model-invoked | Pricing + monetization |
| `/pm-release` | model-invoked | Release package |
| `/pm-align` | model-invoked | Intent-vs-implementation alignment audit |
| `/pm-triage` | model-invoked | Issue triage |
| `/pm-handoff` | model-invoked | Session handoff document |
| `/pm-abtest` | model-invoked | A/B test statistical analysis |
| `/pm-cohort` | model-invoked | Cohort analysis |
| `/pm-sql` | model-invoked | Natural language → multi-dialect SQL |
| `/pm-okr` | model-invoked | OKR decomposition |
| `/pm-sprint` | model-invoked | Sprint planning |
| `/pm-meeting` | model-invoked | Meeting notes structuring |
| `/pm-roadmap` | model-invoked | output → outcome roadmap conversion |
| `/pm-battlecard` | model-invoked | Competitive battle card |

### Visualization — Visualization

| Skill | Invocation | Purpose |
|---|---|---|
| `/pm-sketch` | model-invoked | Main entry: all sketches + HTML prototype (`--prototype`, tech-stack auto-adapted) |
| `/pm-wireframe` | model-invoked | UI wireframe |
| `/pm-ia` | model-invoked | Information architecture diagram |
| `/pm-state` | model-invoked | State machine diagram |
| `/pm-flow` | model-invoked | Flowchart |
| `/pm-journey` | model-invoked | Customer journey map |

---

## Invocation Rules

- **user-invoked**: Triggered only by humans (`disable-model-invocation: true`); may invoke model-invoked sub-skills.
- **model-invoked**: Triggered autonomously by Agent or orchestrated by user-invoked skills.
- user-invoked **cannot** invoke another user-invoked skill.
- All user-invoked skills support the `--auto` zero-confirmation flag.

---

## Output Directory

```
docs/pm-context/
  pm-context.md          ← Sole Entity (source)
  collect/               ← Organized raw materials
  prd/
    ai-prd.md            ← AI PRD (Agent-executable)
    human-prd.md         ← Human PRD (review-friendly)
  sketch/
    wireframe.md         ← UI wireframe
    ia.md                ← Information architecture
    state.md             ← State machine
    flow.md              ← Flowchart
    prototype.html       ← Interactive HTML prototype (--prototype mode)
```

---

## Project Structure

```
PMSkill/
├── skills/                  ← Skill sources (bucketed by domain)
│   ├── setup/               ← Initialization
│   ├── discovery/           ← Requirement discovery
│   ├── delivery/            ← Delivery
│   ├── visualization/       ← Visualization
│   └── utility/             ← Utilities
├── evals/                   ← Evaluation suite (scenarios + rubrics + fixtures)
├── docs/
│   ├── adr/                 ← Architecture Decision Records
│   └── pm-context/          ← Runtime output directory
├── .github/
│   ├── workflows/ci.yml     ← CI pipeline
│   ├── ISSUE_TEMPLATE/      ← Issue templates
│   └── PULL_REQUEST_TEMPLATE.md
├── CLAUDE.md                ← Agent instructions
├── CONTEXT.md               ← Domain glossary
├── INSTALL.md               ← Local install entry
└── README.md                ← This file
```

Each Skill follows a uniform structure: `SKILL.md` (Level 1+2 progressive disclosure) + `references/` (Level 3 on-demand) + `test-prompts.json` (test cases).

---

## Evaluation

Following the "build evals before docs" principle, each skill has ≥3 evaluation scenarios with deterministic rubrics under `evals/`.

```bash
bash evals/run-evals.sh --dry-run                 # Structural validation (CI-reproducible)
bash evals/run-evals.sh --dry-run --skill pm-prd  # Single skill
bash evals/run-evals.sh --live                    # Live model scoring (requires claude/codex CLI)
```

See [evals/README.md](evals/README.md) for details.

---

## Development & Testing

### Prerequisites

- Node.js ≥ 18
- A skills-compatible runtime (Claude Code, Codex, Cursor, etc.)

### Local Development

```bash
git clone https://github.com/Wcof/PMSkill.git
cd PMSkill
```

### Running Tests

```bash
# Structural validation (used by CI, no API key required)
bash evals/run-evals.sh --dry-run

# Single skill
bash evals/run-evals.sh --dry-run --skill pm-prd

# Live model scoring (requires claude/codex CLI)
bash evals/run-evals.sh --live
```

### CI

GitHub Actions (`.github/workflows/ci.yml`) runs `--dry-run` structural validation on every Pull Request.

---

## Compatibility

Supports all skills-compatible runtimes: Claude Code, Codex, Cursor, Trae, OpenClaw, Hermes, etc. The install command auto-adapts; no manual path specification required.

---

## FAQ

**Can PMContext be updated?** Yes. PMContext is a living document. Re-invoking `/pm-refine` infers only the new parts and incrementally updates.

**Can I skip collect and go straight to refine?** Yes. Both `/pm-collect` and `/pm-refine` can be called independently.

**What's the difference between `--auto` and normal mode?** Normal mode pauses at the audit gate after producing PMContext for PM confirmation; `--auto` lands everything in one pass and produces a one-stop report for post-hoc audit.

**Which Agents are supported?** All skills-compatible runtimes; the install command auto-adapts.

---

## Further Reading

- [Anthropic Agent Skills Specification](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Continuous Discovery Habits — Teresa Torres](https://www.productcompass.pm/p/cpdm)
- [A Proven AI PRD Template — Miqdad Jaffer (OpenAI)](https://www.productcompass.pm/p/ai-prd-template)
- [Pre-Mortem: Meta/Instagram Practice](https://www.productcompass.pm/p/how-to-run-pre-mortem-template)
- [Mermaid Official Docs](https://mermaid.js.org/)

---

## Contributing

Contributions via Issues and Pull Requests are welcome.

- **Issues**: Use the templates in [.github/ISSUE_TEMPLATE/](.github/ISSUE_TEMPLATE/) (bug report / feature request).
- **Pull Requests**: Follow [.github/PULL_REQUEST_TEMPLATE.md](.github/PULL_REQUEST_TEMPLATE.md); ensure CI passes (`bash evals/run-evals.sh --dry-run` exits 0).
- **New Skills**: Follow the 9-section template (Purpose / Context / Instructions / Thinking Protocol / Relate / Failure Modes / Anti-patterns / Output Examples / Further Reading) and include ≥3 evaluation scenarios.
- **Code of Conduct**: See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
- **Security Reports**: See [SECURITY.md](SECURITY.md).

---

## Acknowledgements

This project is inspired by:

- [PM Compass — Product Discovery Guide](https://www.productcompass.pm/)
- [PM Skills Marketplace](https://github.com/phuryn/pm-skills)
- [Teresa Torres — Continuous Discovery Habits](https://www.productcompass.pm/p/cpdm)
- [Miqdad Jaffer (OpenAI) — AI PRD Template](https://www.productcompass.pm/p/ai-prd-template)
- [Anthropic — Agent Skills Specification](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)

Thanks to all [contributors](https://github.com/Wcof/PMSkill/graphs/contributors).

---

## License

Released under the [MIT License](LICENSE).

Copyright (c) 2026 PMSkill Contributors.
