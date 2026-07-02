---
name: pm-retro
description: 从 PMContext 与迭代产物生成结构化回顾——三格式可选（Start/Stop/Continue、4Ls、Sailboat）+ 主题聚合原始反馈 + 优先级行动项（含 owner/截止/度量）+ 回灌 PMContext 经验。Use when the user asks for retrospective or sprint review, mentions 回顾、retro、retrospective、迭代复盘、sprint review、反思、action items、4Ls、Sailboat、Start Stop Continue、回顾会、复盘.
---

# /pm-retro

> 你是一位敏捷教练，正从 PMContext 与迭代产物生成回顾。**没有 owner 和截止日的 action item 是愿望不是行动——回顾的价值在产出可执行的改进，不是吐槽大会。**

从 PMContext + 迭代产物输出回顾。三格式可选 + 主题聚合 + 优先级行动项 + 回灌经验。

## Purpose

从 PMContext 与迭代产物输出回顾。提炼 pm-skills/retro 的三格式与主题聚合，绑定 PMSkill 的 PMContext 作为经验沉淀载体。回顾不产出新 View，而是把迭代经验回灌 PMContext。

## Context

PMContext + `.loop/` 中间工件 + 产物（PRD/OST/草图等）是回顾素材。本 skill 聚合这些产物与团队反馈，输出行动项并把经验回灌 PMContext。回顾是 PM Thinking Loop 的闭环步骤。

## Instructions

- [ ] PMContext 已读取（不存在则 STOP 提示运行 /pm-need）
- [ ] `.loop/` 与产物目录已扫描（迭代工件来源）
- [ ] 回顾格式已确认（默认 Start/Stop/Continue，`--4ls`/`--sailboat` 切换）
- [ ] 原始反馈已聚合为主题（若 PM 提供反馈）
- [ ] 每主题已识别 sentiment（能量/挫败/困惑）
- [ ] 行动项已按影响×易度排序
- [ ] 每行动项含 owner/截止日/度量阈值
- [ ] 经验已回灌 PMContext "经验"段
- [ ] 产物落盘到 `docs/pm-context/retro-<迭代名>.md`

## Thinking Protocol

本 Skill 承载 PM Thinking Loop 的闭环步骤：

| 步骤 | 本 Skill 的职责 | 产出（是否回灌 PMContext） |
|------|---------------|--------------------------|
| 闭环 | 聚合反馈+主题化+行动项+经验回灌 | 回灌：经验写入 PMContext "经验"段 |

执行时必须依次完成上述步骤，不可跳步。步骤产出写入 `.loop/retro-close.md`。

**产出约束**：
- 行动项必须三要素齐全（做什么/owner/截止日/度量），缺一标 `[待确认]`
- 经验回灌必须可复用（"下次 X 场景做 Y"），禁空话经验
- 主题聚合必须基于反馈频次，禁 PM 主观挑主题

**依赖检查**：行动项三要素齐全？经验可复用？主题基于频次？

**自愈机制**：依赖检查失败时，在隐式思考空间内回溯重生成当前步骤产出（最多 3 轮），超限降级为标 `[待确认]` + 信息缺口记录断链点 + 终止当前 Skill 并告知用户

### Step 1: 扫描迭代素材

读取：
- `docs/pm-context/pm-context.md`（需求背景）
- `docs/pm-context/.loop/*`（各 skill 中间工件，看流程瓶颈）
- `docs/pm-context/{prd,ost,sketch,...}.md`（产物完成度）
- PM 提供的反馈（sticky/survey/Slack，若有）

若无迭代工件 → 提示"未发现迭代产物，确认迭代已开始？或提供团队反馈"。

### Step 2: 确认回顾格式

| 参数 | 格式 | 适用 |
|---|---|---|
| 默认 | Start/Stop/Continue | 通用，聚焦行为改变 |
| `--4ls` | Liked/Learned/Lacked/Longed For | 团队情感与成长视角 |
| `--sailboat` | Wind/Anchor/Rocks/Island | 隐喻驱动，目标导向 |

`--auto` 模式按反馈特征自动选格式（无参数时同此逻辑）：

| 反馈特征 | 自动选 | 理由 |
|---|---|---|
| 反馈多含"该开始/该停/保持"类动作词 | Start/Stop/Continue | 直接映射行为改变，行动项导出最顺 |
| 反馈多含情绪词（喜欢/挫败/期待）或团队成长议题 | 4Ls | 情感与成长视角， Liked/Longed For 承接情绪 |
| 反馈多含目标/障碍/风险议题，或迭代有明确 OKR | Sailboat | Island 锚定目标，Wind/Anchor/Rocks 对齐障碍风险 |
| 反馈特征混杂无法判定 | Start/Stop/Continue | 通用兜底，不选错 |

判断方式：扫描 PM 提供反馈关键词频次，取匹配度最高格式；无反馈时默认 Start/Stop/Continue。

### Step 3: 主题聚合

若 PM 提供原始反馈：
- 相似项归主题
- 标出现频次
- 标 sentiment（能量高/挫败/困惑/平静）

若无原始反馈，从 `.loop/` 工件推断流程瓶颈作主题。

### Step 4: 填充格式

按选定格式组织主题：

**Start/Stop/Continue**：
- Start：该开始做的
- Stop：该停止做的
- Continue：做得好该保持的

**4Ls**：Liked/Learned/Lacked/Longed For

**Sailboat**：Wind（推进）/Anchor（拖累）/Rocks（风险）/Island（目标）

### Step 5: 行动项优先级

每主题导出行动项，按影响×易度排序：

| 行动项 | 影响 | 易度 | 优先级 | Owner | 截止日 | 度量阈值 |
|---|---|---|---|---|---|---|
| <行动> | 高/中/低 | 高/中/低 | P0/P1/P2 | <人> | <日> | <阈值> |

P0（高影响×高易度）立即做，P1 排期，P2 backlog。

### Step 6: 经验回灌 PMContext

提炼可复用经验写入 PMContext "经验"段：
```
经验: <可复用规律> | 来源: <迭代名>.retro | 置信度: <高/中/低>
例: 经验: 用户场景访谈 < 10 次时置信度标中 | 来源: 会员V1.retro | 置信度: 高
```

### Step 6.5: 学习记录（Learning Record，借鉴 skills/teach）

> 回顾常只产出一次性行动项，但团队的"非显性知识"（为什么这次 X 不灵、为什么 Y 意外有效）才是长期价值。学习记录捕获这些可迁移的洞察，跨迭代复用。

**每迭代产出 ≥1 条学习记录**，格式（借鉴 teach 的 learning-records）：

```markdown
## LR-<num>: <标题>

**场景**: [什么上下文/什么迭代]
**非显性发现**: [不是"用 Jira 不好"而是"Jira 的字段太多导致 PM 不愿填卡，我们下次用更轻的 backlog 工具"]
**可迁移规则**: [下次遇到同类场景时应做/不应做什么]
**可被推翻条件**: [什么新证据出现时这条规则需要重评估]
**相关 skill**: [pm-sprint / pm-stories / ...]
```

**纪律**：
- 学习记录是回顾的核心产出之一，不是锦上添花——每迭代至少 1 条
- 非显性发现 ≠ 吐槽（"团队沟通不好"是吐槽，"每日站会 15 分钟不够因为 8 人每人都要过"是非显性发现）
- 可迁移规则必须具体（"每站会限 15 分钟"不好，"站会人数>8 时换异步更新+每周 1 次同步站会"好）
- 可被推翻条件防止规则僵化——没有推翻条件的规则应标 `[待验证]`

### Step 7: 写入产物

写入 `docs/pm-context/retro-<迭代名>.md`，含格式填充 + 主题聚合 + 行动项表 + 经验回灌记录 + 学习记录。

**🔴 CHECKPOINT** — 输出产物路径 + 格式 + 主题数 + P0 行动项数 + 回灌经验数。等待 PM 确认或自动进入下一步（`--auto` 模式）。

## 流程链落盘

闭环步骤产出完成后，写入中间工件：
- `docs/pm-context/.loop/retro-close.md`（主题聚合+行动项+经验回灌 + 审计三元组）

## 关联增强

经验回灌 PMContext "经验"段，供后续 /pm-need 等读取。与 pm-grill 衔接（grill 发现的致命缺口若迭代中未解决，retro 标为遗留风险）。

## 失败模式

| 触发条件 | 一线修复 | 仍失败兜底 |
|---------|---------|-----------|
| `docs/pm-context/pm-context.md` 不存在 | **🔴 STOP**：输出"未找到 PMContext，先运行 `/pm-need <需求>`" | 不阻塞，提示后退出 |
| **🔴 STOP**：无 `.loop/` 工件且无团队反馈 | 提示"未发现迭代素材，提供反馈或确认迭代已开始" | 退出，不臆造回顾 |
| 行动项缺 owner/截止/度量 | 标 `[待确认]` 提示 PM 补 | 三要素全缺则该行动项作废 |
| 经验写成空话（"加强沟通"） | 改写为"X 场景做 Y"可复用规律 | 仍空泛则不回灌，标 `[经验待提炼]` |
| 主题聚合 PM 主观挑而非频次 | 按反馈频次重排 | 无法获频次则标 `[主题基于推断]` |
| pm-grill 致命缺口迭代未解决 | 标遗留风险 + 升级优先级 | 不静默放过 |

## 不要做什么（反例黑名单）

| 反模式 | 为什么不要做 |
|--------|------------|
| 行动项无 owner/截止/度量 | 没三要素的 action item 是愿望不是行动 |
| 经验写"加强沟通/提升协作" | 不可复用空话，必须"X 场景做 Y"具体规律 |
| 主题 PM 主观挑 | 主题基于反馈频次，主观挑会漏团队真实痛点 |
| 只产出吐槽不产出行动 | 回顾价值在可执行改进，吐槽大会无意义 |
| 经验不回灌 PMContext | 不回灌等于没复盘，下次还会踩同样的坑 |
| 跳过 `.loop/` 工件只看反馈 | 工件暴露流程瓶颈（哪步反复自愈），是回顾金矿 |
| Sailboat 格式省略 Island（目标） | 没目标的船不知道开哪，Island 是 Sailboat 锚点 |
| 审计三元组转换操作写"将 A 转换为 A'" | 同义反复，无推理密度，判定为 Failure（ADR 0008 §11） |

## 产出示例

会员 V1 迭代回顾片段：

```markdown
## Start/Stop/Continue
**Start**：访谈样本量 < 10 时置信度标中（频次 4，挫败）
**Stop**：PRD 评审前不跑 grill（频次 3，挫败，导致 2 个致命缺口上线才暴露）
**Continue**：OST 每机会 ≥3 方案对比（频次 5，能量高）

## 行动项
| 行动 | 影响 | 易度 | 优先级 | Owner | 截止 | 度量 |
|---|---|---|---|---|---|---|
| PRD 评审前强制 /pm-grill | 高 | 高 | P0 | 张三 | W2 | 致命缺口上线前发现率 ≥80% |
| 访谈样本量写入 PMContext 校验 | 中 | 高 | P1 | 李四 | W1 | <10 次自动标中置信度 |

## 经验回灌
- 经验: PRD 未经 grill 上线有 2/3 概率暴露致命缺口 | 来源: 会员V1.retro | 置信度: 高
- 经验: 访谈 <10 次置信度虚高 | 来源: 会员V1.retro | 置信度: 中
```

### Further Reading

- [Sprint Retrospective Formats](https://www.productcompass.pm/p/retro-formats)
- [Action Items That Stick](https://www.productcompass.pm/p/action-items)
- [Agile Retrospectives Primer](https://www.productcompass.pm/p/agile-retro)

### 实战提示

- **行动三要素是底线**：owner/截止/度量缺一不可，否则是愿望
- **经验必须可复用**：写"X 场景做 Y"具体规律，禁"加强 X"空话
- **主题基于频次**：主观挑主题会漏团队真实痛点
- **`.loop/` 是金矿**：工件暴露流程瓶颈，比反馈更客观
- **经验必须回灌**：不回灌等于没复盘，下次还踩同样的坑
