# PMSkill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/Skills-5%20visible%20%2F%2051%20total-blue.svg)](#skill-清单)
[![CI](https://img.shields.io/badge/CI-passing-brightgreen.svg)](.github/workflows/ci.yml)
[![Spec](https://img.shields.io/badge/Anthropic-Agent%20Skills-orange.svg)](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)

> 面向 Agent 环境的产品经理 Skill 工具箱。

从模糊想法或用户诉求出发，经一条命令完成全链路沉淀：**PMContext（唯一源）→ PRD（给 AI + 给人）→ 可视化草图 + HTML 可交互原型**。

---

## 概述

PMSkill 将产品经理在 Agent 中的核心工作流程封装为 **51 个 Skill**——5 个 User-facing（斜杠菜单可见，人类主动触发）+ 46 个 Engine（由 AI 按语义 `use_skill` 调起，默认隐藏不噪音）。覆盖需求发现、交付与可视化三大领域。所有 Skill 遵循 [Anthropic Agent Skills 规范](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)，采用 YAML frontmatter 渐进披露与第三人称触发描述。

### 核心特性

- **单一数据源**：PMContext 是唯一 Entity，PRD 与草图均为其下游 View，下游 Skill 读取一个文件即可获得全貌。
- **全链路自动化**：一条命令完成 collect → refine → PRD → 用户故事 → 原型，支持零确认 `--auto` 模式。
- **双形态 PRD**：面向 AI 的可执行 PRD（含 Agent Context）与面向人类的评审友好 PRD。
- **技术栈硬约束**：PMContext §8 声明前端框架（Vue/React/Next/Nuxt/Svelte/Angular/Electron 或 Vite+TypeScript）即升格为硬契约——pm-aiprd 转写「技术栈契约」段，pm-sketch Step -0.5 硬触发 Scaffold 模式，防 Agent 偷懒自降级到 HTML 壳子。
- **增量更新自判**：`/pm-need` 入口扫产物目录自动判 0→1 vs 增量——PMContext 空 = 全链路，非空 = 仅扫 `[待确认]` `[假设]` `[冲突]` 标记段重跑，已确认段 Frozen 不动，合并走 `/pm-conflict-resolver` 内联调。
- **渐进披露**：Level 1/2/3 三层加载，按需引用，控制 Token 开销。
- **可追溯性**：风险以显式标记（`[待确认]` / `[假设]` / `[冲突]`）内嵌于正文，单级追溯。
- **配置可循**：`/pm-setup` 落 `.pmskill-setup.stamp` 凭据，下游 Skill 读 `## PMSkill` 块取产物目录，块与 stamp 互校，不硬编码路径。

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
/pm-need              # 收集材料 → refine 追问 → 审计门（PMContext 空 = 0→1 全链路；非空 = 增量仅扫标记段）
/pm-need --auto       # 收集材料 → refine 自主推断 → PRD → 用户故事 → 原型
/pm-need --update §8  # 定点增量：仅重跑指定段，其余 Frozen
/pm-prd               # 从 PMContext 生成 PRD（给 AI + 给人）
/pm-prd --auto        # 零确认：直接出 PRD
/pm-stories           # 从 PMContext 生成用户故事/功能清单（3C + INVEST）
/pm-sketch            # 生成全部草图
/pm-sketch --prototype # 生成草图 + HTML 可交互原型（PMContext §8 含前端框架声明时硬触发 Scaffold）
```

---

## 主链路

```
模糊想法 / 用户诉求
        │
  /pm-need ─── {--auto: 零确认} ───→ PMContext (唯一 Entity)
        │                                   │
  ┌─────┴─────┐                    ┌────────┴─────────────────┐
  │           │                    │                          │
/pm-prd  /pm-premortem       /pm-stories        /pm-sketch --prototype
  │           │                    │                          │
  ▼           ▼                    ▼                          ▼
prd/*.md  premortem.md       stories.md        sketch/*.md + prototype.html
                                                  (简单模式: 单文件)
                                                  (Scaffold: prototype/ 工程)
```

### ⚠️ pm-sketch 产出定位

`/pm-sketch --prototype` 产出为**前端原型（mock）**，纯前端实现，不输出后端 API、数据 schema 或生产代码。Scaffold 模式为可运行 React + TS + Vite + Tailwind v4 工程，L4 交互（角色/权限/四态/错误恢复），但仍是**原型级可点 mock**，非生产实现。

### 增量迭代使用说明

PMSkill 支持增量迭代，无需每次全量重做：

| 场景 | 命令 | 行为 |
|------|------|------|
| 新增功能/页面 | `/pm-need 增加「XXX」页面` | 自动判为新增型，追加新 `## <页面>` 段，已有段 Frozen 不动 |
| 调整已确认需求 | `/pm-need --update §<页面名> <调整内容>` | 仅该段显式解冻重跑，其余 Frozen |
| 补充信息缺口 | `/pm-need 补充<具体缺口>` | 走补全型，仅扫标记段重跑 |
| 新增页面后更新原型 | `/pm-sketch --prototype` | 目标已有时自动进增量原型模式，仅生成新页面，不覆盖已有页 |
| 强制全量重生成 | `/pm-sketch --prototype --rebuild` | 覆盖已有原型 |

---

## Skill 清单

**斜杠可见 = 5 个 User-facing**（默认对人类菜单可见）；**Engine = 46 个**（`metadata.internal: true`，默认隐藏由 AI `use_skill` 调起，`INSTALL_INTERNAL_SKILLS=1` 可显式列出）。下方按领域分桶列出全部 51 个，括号标可见性。

### Setup — 初始化

| Skill | 调用方式 | 作用 |
|---|---|---|
| `/pm-setup` | user-invoked | 首次配置项目（产物目录 / 语言 / 知识库 / Agent 规则），落 `.pmskill-setup.stamp` 凭据 |

### Discovery — 需求发现

| Skill | 调用方式 | 作用 |
|---|---|---|
| `/pm-need` | user-invoked | 🏆 主入口：collect → refine → audit 全自动；`--auto` 零确认直达 PRD + 原型；**入口自判 0→1 vs 增量**（PMContext 空 = 全链路，非空 = 仅扫标记段，已确认段 Frozen） |
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
| `/pm-pestle` | model-invoked | PESTLE 宏观环境分析（六维 × 影响×概率矩阵） |

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
| `/pm-stakeholder` | model-invoked | 干系人地图（Power×Interest 四象限 + 沟通计划） |

### Utility — 工具

| Skill | 调用方式 | 作用 |
|---|---|---|
| `/pm-legal` | model-invoked | 产品合规文档（NDA / 隐私政策 / 合规差距分析） |
| `/pm-conflict-resolver` | model-invoked | 局部退火——节点报错时只对报错上下文+上游节点 JSON 做最小差分修复，不重写全局 PMContext |

### Visualization — 可视化

| Skill | 调用方式 | 作用 |
|---|---|---|
| `/pm-sketch` | model-invoked | 🏆 主入口：输出全部草图 + HTML 原型（`--prototype`，双模式 —— 简单模式 CDN 单 HTML / Scaffold 模式 React+TS+Vite+Tailwind v4 工程） |
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
  process/               ← 过程文档（显性，进版本库，供 PM 全程审计）
    README.md            ← 过程文档索引（阅读顺序）
    01-collect-understand.md  ← 问题重构 + 四源材料聚合
    02-refine-model.md         ← 领域模型（实体/关系/不变量）
    03-refine-options.md       ← 方案候选（激进 vs 保守）
    04-refine-tradeoff.md      ← 决策表（选了什么/为什么/代价）
    05-premortem-risk.md       ← 风险清单 + Tiger 三分 + 行动计划
    06-*-delivery.md           ← 各交付 Skill 的交付物与追溯
    06-sketch-*.md             ← 4 个子草图 Skill 的图元追溯
    conflict-log.json          ← 局部退火差分修复日志
    .archive/<timestamp>/      ← 重跑归档区（不进版本库）
  .cache/                ← 纯技术缓存（断点续跑 JSON 分片，不进版本库，重跑时清空）
  prd/
    ai-prd.md            ← 给 AI 的 PRD（Agent 可执行）
    human-prd.md         ← 给人的 PRD（评审友好）
  sketch/
    wireframe.md         ← 界面线框图
    ia.md                ← 信息架构图
    state.md             ← 状态机图
    flow.md              ← 流程图
    journey.md           ← 客户旅程图（跨页面/跨状态的用户动线）
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

两类 runtime 能力区分：

| runtime | metadata.internal 隐藏 | `use_skill` 自动编排 | `disable-model-invocation` | `--auto` 全链路 | 网络权限 |
|---------|:-:|:-:|:-:|:-:|:-:|
| **Claude Code / npx-skills / Codex / Cursor 等** | ✅ | ✅ | ✅ | ✅ 可跑通 | ✅ 可联网抓取 |
| **纯 Claude API** | ❌ 仅认 name/description | ❌ 编排字段被忽略 | ❌ | ⚠️ Skill 按独立能力触发，链路需手动串 | ❌ 沙箱无网络 |

纯 API 环境下降级表现：
- 46 个 Engine Skill 因 `metadata.internal` 被忽略，全部对 API �可见（噪音增加）
- 编排字段（`disable-model-invocation`、`use_skill`）被忽略，Skill 按独立能力触发，`/pm-need --auto` 链路需 PM 手动串联各 Skill
- 沙箱无网络、不能装包，`/pm-collect` 的 URL 抓取/联网扫描降级为「仅扫描已提供材料 + 对话上下文」，不静默假装抓取成功

支持所有 skills-compatible runtime：Claude Code、Codex、Cursor、Trae、OpenClaw、Hermes 等。安装命令自动适配，无需手动指定路径。

---

## 常见问题

**PMContext 可以更新吗？** 可以。`/pm-need` 入口扫产物目录自判——PMContext 空 = 0→1 全链路；非空 = 增量模式，仅扫 `[待确认]` `[假设]` `[冲突]` 标记段重跑 collect/refine，已确认段 Frozen 不动，合并走 `/pm-conflict-resolver` 内联调。`/pm-need --update §8` 定点增量指定段。

**斜杠菜单看不到某些 skill？** 46 个 Engine Skill 标了 `metadata.internal: true`，默认隐藏由 AI 按语义 `use_skill` 调起。`INSTALL_INTERNAL_SKILLS=1 npx skills add Wcof/PMSkill --list` 可显式列出；或 `--skill <name>` 按名取。

**可以跳过 collect 直接 refine 吗？** 可以。`/pm-collect` 与 `/pm-refine` 均可独立调用。

**`--auto` 与正常模式的区别？** 正常模式产出 PMContext 后停在审计门等待 PM 确认；`--auto` 不等待，一气呵成全部落盘，并出具一站式报告供事后审计。

**支持哪些 Agent？** 所有 skills-compatible runtime，安装命令自动适配。

**过程文档在哪看？** `docs/pm-context/process/` 显性落盘全部过程文档（问题重构 / 领域模型 / 决策表 / 风险清单 / 交付物清单 / 图元追溯），进版本库，PM 可全程审计。重跑时历史版本归档到 `process/.archive/<timestamp>/` 而非删除。纯技术缓存在 `../.cache/`（断点续跑 JSON 分片，不进版本库，重跑时清空）。详见 [docs/adr/0016-explicit-process-artifacts.md](docs/adr/0016-explicit-process-artifacts.md)。

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
