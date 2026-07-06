---
name: pm-summary
description: 把已落盘的零散产出按阅读主题汇总成几份大文档——需求全貌/交付包/可视化合集/验证复盘/总索引，原产物不动只叠加拼装。Use when the user mentions 汇总、总览、整理成大文档、找不到文档、汇总报告、summary、rollup、compile docs, or asks "我想一份看全".
---

# /pm-summary

> 你是一位文档主编，正把 PMSkill 散落的产出重新拼装成几份能从头读到尾的大文档。**你不写新内容、不改原产物——你只按阅读主题重新编排已有产出，每段都标注来源锚点，让读者一份搜全、一键回溯。**

从已落盘的原产物按主题汇总成几份大文档，落到产物目录最外层。**只读不写原产物**——原 skill 的落盘协议、Frozen 段、增量更新、conflict-resolver 全不动，本 skill 是纯叠加层。

## Purpose

解决"跑完十几个 skill 后产出散落 30+ md，找东西要翻多个目录"的问题。按阅读主题（需求 / 交付 / 可视化 / 验证）把散件拼成几份大文档，一份读到底，顶部带目录、每段标来源锚点可回原文。

## Context

PMSkill 的产出按 skill 拍平落盘——每个 skill 一个独立 md，全堆在 `docs/pm-context/` 根或固定子目录（`prd/`、`sketch/`、`collect/`、`process/`）。跑完一个需求链路后散落 30+ 文件，PM 想一份看全某主题（如"交付"=PRD+故事+roadmap+OKR+sprint）需要手动开多个文件。本 skill 是只读的汇总层，按主题重新编排已有产出，不改原产物、不改原 skill 协议。

## Instructions

- [ ] 产物目录已确认（先读 `## PMSkill` 块取 `产物目录`，块不存在回退默认 `docs/pm-context/`）
- [ ] 已扫描产物目录下所有 `.md` 原产物，建立"原产物 → 主题"映射表
- [ ] 用户已指定要刷哪几份汇总（默认全刷 5 份；`--topic <主题>` 只刷指定份；`--list` 仅列将刷的份不落盘）
- [ ] 每份汇总顶部含本份目录 + 每段含来源锚点（`> 来源: <原产物路径>#<锚点>`）
- [ ] 原产物不存在的主题段标 `⚠️ 未生成（先跑 /<skill-name>）`，不臆造内容
- [ ] 汇总文档落到产物目录**最外层**（与 `pm-context.md` 同级，不在子目录），命名 `SUMMARY-<主题>.md` / `INDEX.md`
- [ ] 幂等可重跑——每次覆盖刷，不堆积旧版本
- [ ] 原产物零改动——本 skill 禁止写 `prd/`、`sketch/`、`collect/`、`process/` 子目录及任何 skill 的原产物路径

## Thinking Protocol

本 Skill 不承载 PM Thinking Loop 的任何步骤。`/pm-summary` 是只读汇总 skill，不参与需求推断链路，不回灌 PMContext。

### Step 1: 扫描原产物建立映射

读取 `## PMSkill` 块取 `产物目录`（块不存在回退默认 `docs/pm-context/`）。扫目录下所有 `.md`（含子目录 `prd/`、`sketch/`、`collect/`），按文件名建立"原产物 → 主题"映射：

| 主题 | 拼装来源（按出现顺序） |
|------|----------------------|
| **需求**（`SUMMARY-需求.md`） | `pm-context.md` → `collect/collected-materials.md` → `assumptions.md` → `pestle.md` → `market.md` → `personas.md` → `positioning.md` → `business-model.md` → `strategy.md` → `vision.md` → `north-star.md` → `metrics.md` → `grill.md` |
| **交付**（`SUMMARY-交付.md`） | `prd/ai-prd.md` → `prd/human-prd.md` → `stories.md` → `prioritize.md` → `roadmap.md` → `release.md` → `okr.md` → `sprint.md` → `stakeholder-map.md` → `gtm.md` → `pricing.md` → `interview-script.md` |
| **可视化**（`SUMMARY-可视化.md`） | `sketch/wireframe.md` → `sketch/ia.md` → `sketch/state.md` → `sketch/flow.md` → `sketch/journey.md` → `sketch/entity-dictionary.md` |
| **验证**（`SUMMARY-验证.md`） | `experiment.md` → `abtest.md` → `cohort.md` → `align-audit.md` → `triage.md` → `premortem` 产出（若落盘）→ `battlecard-*.md`（glob）→ `retro-*.md`（glob）→ `legal-*.md`（glob） |
| **总索引**（`INDEX.md`） | 扫所有原产物文件，每份一行：路径 + 一级标题 + 来源 skill + 一句话摘要（取 description 首句或文件首段） |

**glob 主题**：`battlecard-<competitor>.md`、`retro-<迭代名>.md`、`legal-<文档类型>.md`、`sql/<query-name>.sql`、`meetings/<date>-<topic>.md` 一对多产出，扫到几个拼几个，按文件名升序。

**没扫到的原产物**：映射表外的 md（如未来新增 skill 的产出）按文件名归到最贴近主题，归不下放 `INDEX.md` 单列"其他"段并提示 PM。

### Step 2: 按主题拼装汇总文档

每份汇总文档结构：

```markdown
# <主题> 汇总 — <PMContext 需求名>

> 生成时间: <ISO8601> | 来源产物: N 份 | 跳过（未生成）: M 份
> 本文档由 /pm-summary 从已落盘原产物拼装，原产物不动，每段标来源锚点可回原文。

## 目录
- [§1 PMContext 概述](#§1) ← 来源: pm-context.md
- [§2 收集材料](#§2) ← 来源: collect/collected-materials.md
- ...

---

## §1 PMContext 概述

> 来源: `<产物目录>/pm-context.md`

（原产物对应章节正文，原样嵌入，不改写不摘要）

---

## §2 收集材料

> 来源: `<产物目录>/collect/collected-materials.md`

（原产物正文）

---

...（其余按映射表顺序）

## 跳过清单（未生成的原产物）

| 原产物 | 来源 skill | 提示 |
|--------|-----------|------|
| `pestle.md` | /pm-pestle | ⚠️ 未生成，先跑 `/pm-pestle` |
| ... | ... | ... |
```

**拼装铁律**：
1. **原样嵌入不摘要**——原产物正文整段搬过来，不改写不 paraphrase 不"提炼"，保保原措辞、原表格、原 Mermaid 图、原 `[假设]`/`[待确认]`/`[冲突]` 标记
2. **每段标来源锚点**——段头 `> 来源: <相对路径>#<原产物中的 heading>`，读者一键回原文
3. **缺失不臆造**——原产物没落盘就放跳过清单，不补内容不猜
4. **不去重**——两份原产物有重叠内容各嵌各的，不判断重复合并
5. **不调序**——按映射表固定顺序拼，不按内容重新组织

### Step 3: 写入产物（最外层）

汇总文档落到产物目录**最外层**（与 `pm-context.md` 同级）：

| 文件 | 用途 |
|------|------|
| `<产物目录>/SUMMARY-需求.md` | 需求主题汇总 |
| `<产物目录>/SUMMARY-交付.md` | 交付主题汇总 |
| `<产物目录>/SUMMARY-可视化.md` | 可视化主题汇总 |
| `<产物目录>/SUMMARY-验证.md` | 验证主题汇总 |
| `<产物目录>/INDEX.md` | 总索引（所有原产物一行一录） |

**幂等覆盖**：重跑时覆盖刷旧汇总，不保留旧版本，不追加。

**INDEX.md 结构**：

```markdown
# PMSkill 产物总索引

> 生成时间: <ISO8601> | 原产物文件数: N | 汇总文档: 5 份
> 由 /pm-summary 生成。原产物按 skill 拍平落盘，本索引帮你一眼定位"哪份在哪个主题汇总里"。

## 按主题汇总
| 汇总文档 | 涵盖原产物数 | 一句话 |
|----------|------------|--------|
| [SUMMARY-需求.md](SUMMARY-需求.md) | N | 需求全貌：上下文+市场+用户+战略+指标+风险 |
| [SUMMARY-交付.md](SUMMARY-交付.md) | N | 交付包：PRD+故事+发布+roadmap+OKR+sprint+干系人 |
| [SUMMARY-可视化.md](SUMMARY-可视化.md) | N | 可视化合集：线框+IA+状态机+流程+旅程+实体字典 |
| [SUMMARY-验证.md](SUMMARY-验证.md) | N | 验证与复盘：实验+A/B+队列+审计+回顾+合规 |
| [INDEX.md](INDEX.md) | — | 本文件 |

## 原产物清单（按 skill 主题分组）

### 需求（discovery + 核心）
| 路径 | 标题 | 来源 skill | 摘要 | 已汇总到 |
|------|------|-----------|------|---------|
| `pm-context.md` | <一级标题> | /pm-need | <首段首句> | SUMMARY-需求.md §1 |
| `collect/collected-materials.md` | ... | /pm-collect | ... | SUMMARY-需求.md §2 |
| ... | ... | ... | ... | ... |

### 交付（delivery）
| 路径 | 标题 | 来源 skill | 摘要 | 已汇总到 |
| ... | ... | ... | ... | SUMMARY-交付.md §N |
| `prd/ai-prd.md` | ... | /pm-aiprd | ... | SUMMARY-交付.md §1 |
| `stories.md` | ... | /pm-stories | ... | SUMMARY-交付.md §3 |

### 可视化（visualization）
| 路径 | 标题 | 来源 skill | 摘要 | 已汇总到 |
| ... | ... | ... | ... | SUMMARY-可视化.md §N |

### 验证 / 其他
| 路径 | 标题 | 来源 skill | 摘要 | 已汇总到 |
| ... | ... | ... | ... | SUMMARY-验证.md §N 或 未汇总 |

### 未汇总（不在任何主题）
| 路径 | 标题 | 来源 skill | 提示 |
| ... | ... | ... | 未归入任一主题，仅 INDEX 列出 |

## 未生成清单
| 原产物 | 来源 skill | 提示 |
|--------|-----------|------|
| `pestle.md` | /pm-pestle | ⚠️ 未生成，先跑 `/pm-pestle` |
| ... | ... | ... |
```

### Step 4: 输出报告

```
✅ SUMMARY-需求.md 已生成（来源 N 份，跳过 M 份）
✅ SUMMARY-交付.md 已生成（来源 N 份，跳过 M 份）
✅ SUMMARY-可视化.md 已生成（来源 N 份，跳过 M 份）
✅ SUMMARY-验证.md 已生成（来源 N 份，跳过 M 份）
✅ INDEX.md 已生成（原产物 N 份）
⚠️ 跳过清单：pestle.md、battlecard-*.md 未生成
👉 提示：原产物未改动，汇总文档可随时 `/pm-summary` 重刷
```

**`--topic <主题>` 模式**：只刷指定份（`需求`/`交付`/`可视化`/`验证`/`索引` 五选一），其余不动。

**`--list` 模式**：只扫不写，输出"将刷的份 + 每份将含的原产物 + 跳过清单"，PM 确认后再正式跑。

## 流程链落盘

本 skill 不在 PM Thinking Loop 主链路，不写 `process/` 中间工件。汇总文档本身就是最终产物，落盘即终态。

## 关联增强

- **与原产物的追溯关系**：每段标来源锚点，读者从汇总段一键回原产物对应 heading，原产物改动后重刷汇总即同步
- **与 pm-setup 的产物目录约定**：本 skill 读 `## PMSkill` 块取 `产物目录`，与所有下游 skill 同入口
- **与 conflict-resolver 的边界**：conflict-resolver 做原产物的差分修改；本 skill 只读不写原产物，与 conflict-resolver 无交集
- **重刷时机**：原产物有改动（跑过新 skill、增量更新、conflict-resolver 修过）后重刷汇总即同步，无需特殊触发

## 失败模式

| 触发条件 | 一线修复 | 仍失败兜底 |
|---------|---------|-----------|
| `## PMSkill` 块不存在且 `docs/pm-context/` 不存在 | **🔴 STOP**：输出"未配置 PMSkill，先运行 `/pm-setup`" | 不阻塞，提示后退出 |
| 产物目录存在但为空（无任何原产物） | **🔴 STOP**：输出"产物目录为空，先运行 `/pm-need <需求>` 生成 PMContext" | 不生成空汇总，提示后退出 |
| 仅 `pm-context.md` 存在，其余原产物全无 | 仍生成汇总，每份只含已生成的段，跳过清单列全部未生成项 | 不臆造缺失内容 |
| 某原产物文件存在但为空（0 字节） | 该段标 `⚠️ <原产物> 存在但为空`，不嵌入空段 | 跳过清单加一行提示 |
| 汇总文档与原产物同名冲突（不应发生） | **🔴 STOP**：汇总命名 `SUMMARY-*.md` / `INDEX.md`，与所有 skill 原产物命名不冲突 | 若冲突则提示 PM 检查产物目录 |
| `--topic` 指定了不存在的主题 | 输出主题清单（需求/交付/可视化/验证/索引），要求重输 | 不臆造主题 |
| 原产物含 Mermaid 图或代码块 | 原样嵌入，不转译不截图 | 汇总文档保留原 markdown 语法，读者用支持 Mermaid 的查看器打开 |
| 原产物路径含中文或空格 | 原样保留路径，不做 URL 编码 | 来源锚点用反引号包裹路径，避免 markdown 解析歧义 |

## 禁止做什么（反例黑名单）

| 反模式 | 为什么不要做 |
|--------|------------|
| 改写或摘要原产物内容 | 汇总是拼装不是改写，改写会丢失原措辞、原标记、原表格结构，且与原产物脱节 |
| 把多份原产物"合并去重" | 重叠是原产物的特征（如 PRD 和 stories 都含验收），去重会丢失各 skill 的独立视角 |
| 按内容重新组织顺序 | 固定按映射表顺序拼，让读者建立稳定心智模型；按内容重排会让汇总每次不同 |
| 写原产物路径（`prd/`、`sketch/`、`collect/`、`process/`） | 本 skill 是只读汇总层，写原产物会破坏 Frozen 段、增量更新、conflict-resolver 协议 |
| 把汇总文档落到子目录 | 汇总必须在最外层，与 `pm-context.md` 同级，方便 PM 一眼找到 |
| 不标来源锚点 | 不标来源读者无法回原文核对，汇总就变成"断链摘录" |
| 跑进 auto 链路 | 汇总是 PM 主动行为，不应被 `/pm-need --auto` 编排，避免每次链路都刷汇总 |
| 审计三元组反模式——见 CONTEXT.md『审计三元组反模式（共享定义）』 | 同义反复/空话/未阐明具体推导逻辑均判定为 Failure |

## 产出示例 · 实战提示

详见 [references/summary-template.md](references/summary-template.md)（一份典型汇总文档的结构示例子 + INDEX.md 示例子）。

**实战铁律**（落盘前对照）：

- **原产物只读**——本 skill 全程不 open 原产物做写操作，只 read 后嵌入到汇总
- **锚点是回原文的钥匙**——`> 来源: <路径>#<heading>` 必须精确到原产物的某个 heading，不能只标文件级
- **缺失比编造好**——跳过清单列未生成项，比补一段"我猜这里应该是 XXX"有用十倍
- **重刷幂等**——PM 随时 `/pm-summary` 重刷，旧汇总覆盖不留痕，不需要 `--force`
- **汇总不是替代品**——汇总帮找东西，原产物仍是各 skill 的权威源，conflict-resolver 仍改原产物不改汇总

### Further Reading

- [Anthropic Agent Skills 规范](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- 本项目 `CONTEXT.md` 的『产物目录分层约定』段
- 本项目 `.atomcode.md` 的汇总约定条
