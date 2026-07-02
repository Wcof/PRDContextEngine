---
name: pm-ost
description: 从 PMContext 生成机会方案树（OST）——Mermaid graph 表达四层结构（期望结果→机会→方案→实验），含机会优先级评分（Importance × (1-Satisfaction)）+ 每机会 ≥3 方案对比。Use when the user asks for opportunity solution tree or discovery structuring, mentions 机会方案树、OST、opportunity solution tree、Teresa Torres、continuous discovery、机会优先级、方案对比、assumption testing.
---

# /pm-ost

> 你是一位产品发现教练，正在从 PMContext 中构建机会方案树。**直接跳到方案是产品发现最大的坑——先映射机会空间，再发散方案，驱散机会空间的"迷雾"（未探索的机会、未验证的假设）。**

从 PMContext 输出机会方案树。四层结构（期望结果→机会→方案→实验）+ 机会优先级评分 + 每机会 ≥3 方案对比。

## Purpose

从 PMContext 输出机会方案树。OST 防止团队跳过机会空间直接定方案。每个机会追溯到 PMContext 用户场景/摩擦力，每个方案从 PM/设计/工程三视角发散。

## Context

PMContext 中有用户场景、现状平替与摩擦力。本 skill 提取这些信息构建 OST。OST 是 PMContext 的下游 View，和 PRD/草图平级，用于结构化产品发现。

## Instructions

- [ ] PMContext 已读取且非空（不存在则 STOP 提示运行 /pm-need）
- [ ] "用户场景"维度已提取（作为期望结果来源）
- [ ] "现状平替与摩擦力"已提取（作为机会来源）
- [ ] "价值验证度量"已提取（作为期望结果量化）
- [ ] 期望结果已定义（单一可量化业务结果）
- [ ] 3-7 个机会已识别（客户视角，非功能）
- [ ] 每个机会用 Opportunity Score 优先级评分
- [ ] 聚焦 Top 2-3 机会，每机会 ≥3 方案
- [ ] 最有希望方案配 1-2 个实验（假设/方法/指标/成功阈值）
- [ ] OST Mermaid 图已生成
- [ ] 每层在"来源"列标注追溯到的 PMContext 项
- [ ] 产物落盘到 `docs/pm-context/ost.md`

## Thinking Protocol

本 Skill 承载 PM Thinking Loop 的步骤 2-3（建模/方案）的发现结构化部分：

| 步骤 | 本 Skill 的职责 | 产出（是否回灌 PMContext） |
|------|---------------|--------------------------|
| 2. 建模 | 从 PMContext 用户场景/摩擦力映射机会空间 | 不回灌（产出 View） |
| 3. 方案 | 每机会发散 ≥3 方案 + 实验设计 | 不回灌（产出 View） |

执行时必须依次完成上述步骤，不可跳步。步骤产出写入 `.loop/ost-step2.md`、`.loop/ost-step3.md`。

**产出约束**：
- 期望结果必须单一可量化（来自 PMContext 价值验证度量）
- 机会必须客户视角（"我挣扎于...""我希望..."），非功能描述
- 每机会必须 ≥3 方案，避免"第一个想法"陷阱
- 方案必须从 PM/设计/工程三视角发散

**依赖检查**：机会是否客户视角？每机会是否 ≥3 方案？实验是否有成功阈值？

**自愈机制**：依赖检查失败时，在隐式思考空间内回溯重生成当前步骤产出（最多 3 轮），超限降级为标 `[待确认]` + 信息缺口记录断链点 + 终止当前 Skill 并告知用户

### Step 1: 读取 PMContext 提取 OST 素材

读取 `docs/pm-context/pm-context.md`，提取：
- "价值验证度量"维度 → 期望结果
- "用户场景" + "现状平替与摩擦力" → 机会
- "边界条件" → 方案约束

若 PMContext 不存在 → **🔴 STOP**：提示先运行 `/pm-need`。

### Step 2: 定义期望结果

从 PMContext 价值验证度量提炼单一可量化业务结果（树顶）：
```
期望结果: 月度会员续费率从 60% 提升到 75% ← PMContext 价值验证度量
```

### Step 3: 映射机会（3-7 个）

从 PMContext 用户场景/摩擦力提取客户机会（needs/pains/desires），用客户视角表述：
```
机会1: "我总是忘记会员到期日" ← PMContext 摩擦力"手动记录到期日"
机会2: "续费时要重新填所有信息太麻烦" ← PMContext 摩擦力"续费太麻烦"
机会3: "我不知道会员权益值不值" ← PMContext [假设, 6/10]
```

### Step 4: 机会优先级评分

用 Opportunity Score 排序：`Importance × (1 - Satisfaction)`，归一化到 0-1：
```
| 机会 | Importance | Satisfaction | Opportunity Score |
|---|---|---|---|
| 忘记到期日 | 0.9 | 0.2 | 0.72 |
| 重新填信息 | 0.95 | 0.1 | 0.855 |
| 权益价值不清 | 0.7 | 0.4 | 0.42 |
```
聚焦 Top 2-3。

### Step 5: 发散方案（每机会 ≥3）

对 Top 机会，从 PM/设计/工程三视角各发散方案：
```
机会2（重新填信息）:
  方案A（PM 视角）: 一键续费预填历史信息
  方案B（设计视角）: 渐进式表单，分步填写降低认知负荷
  方案C（工程视角）: OAuth 支付令牌，无需重新授权
```

### Step 6: 设计实验

对最有希望方案，设计 1-2 个快速实验：
```
方案A 实验:
  假设: 一键续费将续费完成率从 40% 提升到 70%
  方法: 对 20% 用户灰度发布一键续费入口
  指标: 续费页完成率
  成功阈值: 实验组完成率 ≥ 65%
```

### Step 7: 生成 OST 并写入产物

写入 `docs/pm-context/ost.md`，格式：

```markdown
# 机会方案树（OST）

> 来源: PMContext <需求名>
> 期望结果: <结果> | 机会: N 个 | 方案: M 个 | 实验: K 个 | [假设] 项: L 个

## 期望结果
<单一可量化业务结果> ← 来源: PMContext 价值验证度量

## OST 结构图

​```mermaid
flowchart TD
  OR[期望结果: <结果>]
  OR --> O1[机会1: <描述>]
  OR --> O2[机会2: <描述>]
  OR --> O3[机会3: <描述>]
  O2 --> S2A[方案A: <描述>]
  O2 --> S2B[方案B: <描述>]
  O2 --> S2C[方案C: <描述>]
  S2A --> E2A1[实验: <假设>]
  O2:::focus
  classDef focus fill:#fff3cd,stroke:#856404,stroke-width:2px
​```

## 机会清单与优先级
| 机会（客户视角） | Importance | Satisfaction | Score | 聚焦 | 来源 |
|---|---|---|---|---|---|
| <机会1> | 0.9 | 0.2 | 0.72 | ✓ Top2 | PMContext 摩擦力 |
| <机会2> | 0.95 | 0.1 | 0.855 | ✓ Top1 | PMContext 摩擦力 |

## 聚焦机会的方案对比

### 机会: <描述>

| 方案 | 视角 | 适用条件 | 代价 | 来源 |
|---|---|---|---|---|
| 方案A | PM | <条件> | <代价> | PMContext 规则 |
| 方案B | 设计 | <条件> | <代价> | PMContext [假设] |
| 方案C | 工程 | <条件> | <代价> | PMContext 技术约束 |

## 实验设计

### 方案 <X> 实验
- **假设:** <可量化假设>
- **方法:** <实验方式>
- **指标:** <观测指标>
- **成功阈值:** <阈值> ← 来源: PMContext 价值验证度量
```

**🔴 CHECKPOINT** — 输出产物路径 + 期望结果 + 机会数 + 方案数 + 实验数 + `[假设]` 项数。等待 PM 确认或自动进入下一步（`--auto` 模式）。

## 流程链落盘

步骤 2-3 产出完成后，写入中间工件：
- `docs/pm-context/.loop/ost-step2.md`（机会空间映射 + 审计三元组）
- `docs/pm-context/.loop/ost-step3.md`（方案对比 + 实验设计 + 审计三元组）

## 关联增强

在"来源"列标注每层追溯到的 PMContext 项。无来源的标 `[假设]`。

## 失败模式

| 触发条件 | 一线修复 | 仍失败兜底 |
|---------|---------|-----------|
| `docs/pm-context/pm-context.md` 不存在 | **🔴 STOP**：输出"未找到 PMContext，先运行 `/pm-need <需求>`" | 不阻塞，提示后退出 |
| PMContext 中"价值验证度量"为空 | **🔴 STOP**：输出"期望结果无依据，先运行 `/pm-refine` 补全 P2 维度" | 不臆造期望结果 |
| 机会描述是功能而非客户视角（"做一键续费"） | 改写为客户视角（"我希望续费不用重新填信息"） | 仍无法改写则标 `[假设]` |
| 某机会 < 3 个方案 | 从第三个视角（PM/设计/工程）补充方案 | 仍不足则标注"方案空间待扩展" |
| Opportunity Score 数据缺失（无 Importance/Satisfaction） | 从 PMContext 用户反馈推断，标 `[假设]` | 完全无依据则用定性排序替代定量评分 |
| 实验无成功阈值 | 从 PMContext 价值验证度量提取阈值 | 无依据则标 `[待确认]` 让 PM 定 |

## 不要做什么（反例黑名单）

| 反模式 | 为什么不要做 |
|--------|------------|
| 跳过机会空间直接定方案 | OST 核心价值就是先映射机会，跳过等于失去发现结构 |
| 机会用功能描述（"做 X 功能"）而非客户视角 | 机会是客户需求/痛点，不是功能，功能描述会限制方案发散 |
| 每机会只给 1 个方案 | "第一个想法"陷阱，必须 ≥3 方案对比才有选择 |
| 方案只从 PM 视角发散 | Product Trio（PM+设计+工程）三视角发散，"好点子常来自工程师" |
| 期望结果非量化 | 期望结果必须可量化，来自 PMContext 价值验证度量 |
| 实验无成功阈值 | 无阈值的实验无法判断假设是否成立 |
| 机会不追溯到 PMContext | 机会与用户场景脱节，变成凭空想象 |
| 审计三元组转换操作写"将 A 转换为 A'" | 同义反复，无推理密度，判定为 Failure（ADR 0008 §11） |
| 审计三元组转换操作写"基于上述依据产出" | 空话，未阐明具体推导逻辑，判定为 Failure（ADR 0008 §11） |

## 产出示例

会员续费 OST 片段：

```markdown
## 期望结果
月度会员续费率从 60% 提升到 75% ← PMContext 价值验证度量

## 聚焦机会
| 机会（客户视角） | Score | 来源 |
|---|---|---|
| "续费时要重新填所有信息太麻烦" | 0.855 | PMContext 摩擦力 |

## 机会方案对比
| 方案 | 视角 | 代价 |
|---|---|---|
| 一键续费预填历史 | PM | 支付信息过期需兜底 |
| 渐进式表单分步 | 设计 | 开发量大 |
| OAuth 支付令牌 | 工程 | 依赖支付平台支持 |

## 实验
- 假设: 一键续费将完成率 40%→70%
- 方法: 20% 用户灰度
- 指标: 续费页完成率
- 成功阈值: ≥ 65%
```

### Further Reading

- [The Extended Opportunity Solution Tree](https://www.productcompass.pm/p/the-extended-opportunity-solution-tree)
- [Continuous Discovery Habits (Teresa Torres)](https://www.productcompass.pm/p/cpdm)
- [Product Trio: Beyond the Obvious](https://www.productcompass.pm/p/product-trio)

## 产出示例 · 延伸参考 · 实战提示

详见 [references/ost-example.md](references/ost-example.md)（完整 OST 示例 + Opportunity Score 计算表）。

### 实战提示

- **机会空间先于方案**：OST 的核心纪律，跳过机会直接定方案是最大反模式
- **客户视角表述机会**："我希望/我挣扎于"而非"做 X 功能"
- **≥3 方案是底线**：第一个想法几乎从不是最优，对比才有选择
- **Product Trio 发散**：PM/设计/工程三视角，好点子常来自工程师
- **实验要有 skin in the game**：偏好有真实代价的实验，而非纯意见验证
