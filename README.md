# PMSkill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/Skills-49-blue.svg)](#skill-清单)
[![CI](https://img.shields.io/badge/CI-passing-brightgreen.svg)](.github/workflows/ci.yml)
[![Spec](https://img.shields.io/badge/Anthropic-Agent%20Skills-orange.svg)](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)

> 面向 Agent 环境的产品经理 Skill 工具箱。

从模糊想法或用户诉求出发，经一条命令完成全链路沉淀：**PMContext（唯一源）→ PRD（给 AI + 给人）→ 可视化草图 + HTML 可交互原型**。

---

## 概述

PMSkill 将产品经理在 Agent 中的核心工作流程封装为 49 个可调用的 Skill，覆盖需求发现、交付与可视化三大领域。所有 Skill 遵循 [Anthropic Agent Skills 规范](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)，采用 YAML frontmatter 渐进披露与第三人称触发描述。

### 核心特性

- **单一数据源**：PMContext 是唯一 Entity，PRD 与草图均为其下游 View，下游 Skill 读取一个文件即可获得全貌。
- **全链路自动化**：一条命令完成 collect → refine → PRD → 原型，支持零确认 `--auto` 模式。
- **双形态 PRD**：面向 AI 的可执行 PRD（含 Agent Context）与面向人类的评审友好 PRD。
- **技术栈感知**：HTML 原型根据项目实际技术栈自动适配，断网可预览。
- **渐进披露**：Level 1/2/3 三层加载，按需引用，控制 Token 开销。
- **可追溯性**：风险以显式标记（`[待确认]` / `[假设]` / `[冲突]`）内嵌于正文，单级追溯。

---

## 快速开始

### 1. 安装

```bash
npx skills@latest add Wcof/PMSkill --all
```

### 2. 初始化（仅一次）

```text
/pm-setup
```

### 3. 一键全链路（推荐）

```text
/pm-need <需求描述>           # 正常模式：refine 逐维追问 PM
/pm-need <需求描述> --auto    # 零确认模式：refine 自主推断，全自动走完
```

### 4. 分步执行

```text
/pm-need              # 收集材料 → refine 追问 → 审计门
/pm-need --auto       # 收集材料 → refine 自主推断 → PRD → 原型
/pm-prd               # 从 PMContext 生成 PRD（给 AI + 给人）
/pm-prd --auto        # 零确认：直接出 PRD
/pm-sketch            # 生成全部草图
/pm-sketch --prototype # 生成草图 + HTML 可交互原型
```

---

## 主链路

```
模糊想法 / 用户诉求
        │
  /pm-need ─── {--auto: 零确认} ───→ PMContext (唯一 Entity)
        │                                   │
  ┌─────┴─────┐                    ┌────────┴────────┐
  │           │                    │                 │
/pm-prd  /pm-premortem       /pm-sketch      /pm-sketch --prototype
  │           │                    │                 │
  ▼           ▼                    ▼                 ▼
prd/*.md  premortem.md       sketch/*.md     prototype.html
```

---

## Skill 清单

### Setup — 初始化

| Skill | 调用方式 | 作用 |
|---|---|---|
| `/pm-setup` | user-invoked | 首次配置项目（产物目录 / 语言 / 知识库 / Agent 规则） |

### Discovery — 需求发现

| Skill | 调用方式 | 作用 |
|---|---|---|
| `/pm-need` | user-invoked | 🏆 主入口：collect → refine → audit 全自动；`--auto` 零确认直达 PRD + 原型 |
| `/pm-collect` | model-invoked | 主动深扫描（代码 / git / URL / 知识库），4 源去重 |
| `/pm-refine` | model-invoked | 8 维度推断（P0 用户场景 / 边界 / 冲突 → P1 优先级 / 术语 / 摩擦力 → P2 技术约束 / 度量） |
| `/pm-interview` | model-invoked | 结构化用户访谈脚本（JTBD + The Mom Test） |
| `/pm-metrics` | model-invoked | 北极星指标 + Input Metrics 指标星座 |
| `/pm-ost` | model-invoked | 机会方案树（OST） |
| `/pm-strategy` | model-invoked | 战略分析（SWOT / Porter 五力 / Ansoff / Lean Canvas） |
| `/pm-market` | model-invoked | 市场分析（TAM/SAM/SOM + 竞品矩阵） |
| `/pm-vision` | model-invoked | 产品愿景与利益相关者沟通计划 |
| `/pm-grill` | model-invoked | 红队质询（攻击承重假设） |
| `/pm-persona` | model-invoked | 用户画像（基于 JTBD） |
| `/pm-businessmodel` | model-invoked | 商业模式画布（BMC） |
| `/pm-positioning` | model-invoked | 价值主张与差异化定位 |
| `/pm-assumption` | model-invoked | 风险假设识别与最便宜测试 |
| `/pm-northstar` | model-invoked | 北极星指标深化 |
| `/pm-ideation` | model-invoked | 方案发散（optimize + explore） |
| `/pm-parallel` | model-invoked | 并行 agent 分派 |
| `/pm-skillauthor` | model-invoked | TDD 范式撰写 skill |

### Delivery — 交付

| Skill | 调用方式 | 作用 |
|---|---|---|
| `/pm-prd` | model-invoked | 编排双形态 PRD 输出（`--auto` / `--skip-ai` / `--skip-human`） |
| `/pm-aiprd` | model-invoked | 给 AI 的 PRD（可执行规则 + Agent Context） |
| `/pm-humanprd` | model-invoked | 给人的 PRD（评审友好） |
| `/pm-premortem` | model-invoked | Pre-Mortem 风险分析 |
| `/pm-stories` | model-invoked | 用户故事（3C + INVEST） |
| `/pm-gtm` | model-invoked | GTM 策略 |
| `/pm-experiment` | model-invoked | 假设验证闭环 |
| `/pm-retro` | model-invoked | 回顾（Start/Stop/Continue 等） |
| `/pm-prioritize` | model-invoked | 优先级排序（6 框架场景推荐） |
| `/pm-pricing` | model-invoked | 定价与变现 |
| `/pm-release` | model-invoked | 发布包 |
| `/pm-align` | model-invoked | 意图-实现对齐审计 |
| `/pm-triage` | model-invoked | 问题分流 |
| `/pm-handoff` | model-invoked | 会话交接文档 |
| `/pm-abtest` | model-invoked | A/B 测试统计分析 |
| `/pm-cohort` | model-invoked | 队列分析 |
| `/pm-sql` | model-invoked | 自然语言 → 多方言 SQL |
| `/pm-okr` | model-invoked | OKR 拆解 |
| `/pm-sprint` | model-invoked | 迭代规划 |
| `/pm-meeting` | model-invoked | 会议纪要结构化 |
| `/pm-roadmap` | model-invoked | output → outcome roadmap 转换 |
| `/pm-battlecard` | model-invoked | 竞品作战卡 |

### Visualization — 可视化

| Skill | 调用方式 | 作用 |
|---|---|---|
| `/pm-sketch` | model-invoked | 🏆 主入口：输出全部草图 + HTML 原型（`--prototype`，技术栈自动适配） |
| `/pm-wireframe` | model-invoked | 界面线框图 |
| `/pm-ia` | model-invoked | 信息架构图 |
| `/pm-state` | model-invoked | 状态机图 |
| `/pm-flow` | model-invoked | 流程图 |
| `/pm-journey` | model-invoked | 客户旅程地图 |

---

## 调用规则

- **user-invoked**：仅由人类触发（`disable-model-invocation: true`），可调用 model-invoked 子 skill。
- **model-invoked**：可由 Agent 自主触发或由 user-invoked 编排调用。
- user-invoked **不可**调用另一个 user-invoked skill。
- 所有 user-invoked 技能均支持 `--auto` 零确认参数。

---

## 产物目录

```
docs/pm-context/
  pm-context.md          ← 唯一 Entity（源）
  collect/               ← 整理后的原始材料
  prd/
    ai-prd.md            ← 给 AI 的 PRD（Agent 可执行）
    human-prd.md         ← 给人的 PRD（评审友好）
  sketch/
    wireframe.md         ← 界面线框图
    ia.md                ← 信息架构图
    state.md             ← 状态机图
    flow.md              ← 流程图
    prototype.html       ← HTML 可交互原型（--prototype 简单模式，单文件）
    prototype/           ← HTML 可交互原型（--prototype 复杂模式，前端 bundle）
      index.html         ← 入口壳（双击可打开基础版）
      app.js             ← 完整交互逻辑
      styles.css         ← Design Token + 响应式
      prd-data.js        ← PMContext 内容注入
      mock-data.js       ← 图表/列表 mock 数据
      README.md          ← 本地启动说明
```

---

## 目录结构

```
PMSkill/
├── skills/                  ← Skill 源码（按领域分桶）
│   ├── setup/               ← 初始化
│   ├── discovery/           ← 需求发现
│   ├── delivery/            ← 交付
│   ├── visualization/       ← 可视化
│   └── utility/             ← 工具类
├── evals/                   ← 评估集（场景 + rubric + 夹具）
├── docs/
│   ├── adr/                 ← 架构决定记录
│   └── pm-context/          ← 运行时产物目录
├── .github/
│   ├── workflows/ci.yml     ← CI 流水线
│   ├── ISSUE_TEMPLATE/      ← Issue 模板
│   └── PULL_REQUEST_TEMPLATE.md
├── CLAUDE.md                ← Agent 指令
├── CONTEXT.md               ← 领域术语表
├── INSTALL.md               ← 本地安装入口
└── README.md                ← 本文件
```

每个 Skill 目录结构统一：`SKILL.md`（Level 1+2 渐进披露）+ `references/`（Level 3 按需加载）+ `test-prompts.json`（测试用例）。

---

## 评估

遵循「先建评估再写文档」原则，每个 skill 在 `evals/` 下配有 ≥3 个评估场景与可判定 rubric。

```bash
bash evals/run-evals.sh --dry-run                 # 结构校验（CI 可复现）
bash evals/run-evals.sh --dry-run --skill pm-prd  # 单 skill
bash evals/run-evals.sh --live                    # 真实模型跑分
```

详见 [evals/README.md](evals/README.md)。

---

## 开发与测试

### 环境要求

- Node.js ≥ 18
- 支持 skills-compatible runtime（Claude Code、Codex、Cursor 等）

### 本地开发

```bash
git clone https://github.com/Wcof/PMSkill.git
cd PMSkill
```

### 运行测试

```bash
# 结构校验（CI 使用，无需 API key）
bash evals/run-evals.sh --dry-run

# 单 skill 校验
bash evals/run-evals.sh --dry-run --skill pm-prd

# 真实模型跑分（需 claude/codex CLI）
bash evals/run-evals.sh --live
```

### CI

仓库配置了 GitHub Actions（`.github/workflows/ci.yml`），对每个 Pull Request 自动执行 `--dry-run` 结构校验。

---

## 兼容性

支持所有 skills-compatible runtime：Claude Code、Codex、Cursor、Trae、OpenClaw、Hermes 等。安装命令自动适配，无需手动指定路径。

---

## 常见问题

**PMContext 可以更新吗？** 可以。PMContext 是活文档，再次调用 `/pm-refine` 仅推断新增部分并增量写入。

**可以跳过 collect 直接 refine 吗？** 可以。`/pm-collect` 与 `/pm-refine` 均可独立调用。

**`--auto` 与正常模式的区别？** 正常模式产出 PMContext 后停在审计门等待 PM 确认；`--auto` 不等待，一气呵成全部落盘，并出具一站式报告供事后审计。

**支持哪些 Agent？** 所有 skills-compatible runtime，安装命令自动适配。

---

## 延伸参考

- [Anthropic Agent Skills 规范](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Continuous Discovery Habits — Teresa Torres](https://www.productcompass.pm/p/cpdm)
- [A Proven AI PRD Template — Miqdad Jaffer (OpenAI)](https://www.productcompass.pm/p/ai-prd-template)
- [Pre-Mortem: Meta/Instagram 实践](https://www.productcompass.pm/p/how-to-run-pre-mortem-template)
- [Mermaid 官方文档](https://mermaid.js.org/)

---

## 贡献

欢迎通过 Issue 与 Pull Request 参与贡献。

- 提交 Issue：使用 [.github/ISSUE_TEMPLATE/](.github/ISSUE_TEMPLATE/) 中的模板（bug 报告 / 功能请求）。
- 提交 PR：遵循 [.github/PULL_REQUEST_TEMPLATE.md](.github/PULL_REQUEST_TEMPLATE.md)，确保通过 CI（`bash evals/run-evals.sh --dry-run` 退出码为 0）。
- 新增 Skill：遵循 9 段式模板（Purpose / Context / Instructions / Thinking Protocol / 关联增强 / 失败模式 / 禁止做什么 / 产出示例 / Further Reading），并配套 ≥3 个评估场景。
- 行为准则：参见 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)。
- 安全漏洞报告：参见 [SECURITY.md](SECURITY.md)。

---

## 致谢

本项目受以下资源启发：

- [PM Compass — Product Discovery Guide](https://www.productcompass.pm/)
- [PM Skills Marketplace](https://github.com/phuryn/pm-skills)
- [Teresa Torres — Continuous Discovery Habits](https://www.productcompass.pm/p/cpdm)
- [Miqdad Jaffer (OpenAI) — AI PRD Template](https://www.productcompass.pm/p/ai-prd-template)
- [Anthropic — Agent Skills 规范](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)

感谢所有 [贡献者](https://github.com/Wcof/PMSkill/graphs/contributors)。

---

## License

本项目基于 [MIT License](LICENSE) 发布。

Copyright (c) 2026 PMSkill Contributors.
