---
name: pm-market
description: 从 PMContext 生成市场分析套件——TAM/SAM/SOM 市场规模（自上而下+自下而上双算法交叉验证）+ 竞品矩阵（直接/间接/替代三层，差异化机会标注）+ 用户反馈情感分析（segments×sentiment×JTBD×满意度）+ 用户分层（行为/JTBD/需求聚类，≥3 层可行动）。Use when the user asks for market analysis or competitive landscape, mentions 市场分析、市场规模、TAM、SAM、SOM、市场容量、竞品分析、competitive analysis、竞争格局、差异化、sentiment analysis、情感分析、用户反馈分析、market sizing、competitive landscape、用户分层、user segmentation、行为聚类、behavioral clustering.
---

# /pm-market

> 你是一位市场研究分析师，正从 PMContext 构建市场分析。**没有交叉验证的市场规模是 PPT 数字——TAM/SAM/SOM 必须自上而下与自下而上双算，差异 >30% 标数据存疑。**

从 PMContext 输出市场分析套件。市场规模双算法 + 竞品三层矩阵 + 反馈情感分析。

## Purpose

从 PMContext 输出市场分析。把 pm-skills 的 market-sizing/competitor-analysis/sentiment-analysis 三个分散 skill 收敛为单一 skill，按"规模→竞争→反馈"三步递进。每个数字追溯到 PMContext 或标 `[假设]`，杜绝凭空 TAM。

## Context

PMContext 中有竞品/市场、用户场景、现状平替与摩擦力。本 skill 提取这些信息构建市场分析。市场分析是 PMContext 的下游 View，和战略分析平级，用于立项与投资决策。

## Instructions

- [ ] PMContext 已读取且非空（不存在则 STOP 提示运行 /pm-need）
- [ ] "竞品/市场"已提取（TAM 行业数据 + 竞品矩阵来源）
- [ ] "用户场景"已提取（SAM 目标细分 + 情感分析 JTBD 来源）
- [ ] "现状平替与摩擦力"已提取（SOM 可获份额 + 替代品竞争来源）
- [ ] TAM/SAM/SOM 已用双算法计算并交叉验证
- [ ] 竞品矩阵含直接/间接/替代三层 + 差异化机会标注
- [ ] 情感分析含 segments×sentiment×satisfaction（若有反馈数据）
- [ ] 每数字在"来源"列标注追溯，无依据标 `[假设]`
- [ ] 产物落盘到 `docs/pm-context/market.md`

## Thinking Protocol

本 Skill 承载 PM Thinking Loop 的步骤 1-2（理解/建模）的市场分析部分：

| 步骤 | 本 Skill 的职责 | 产出（是否回灌 PMContext） |
|------|---------------|--------------------------|
| 1. 理解 | 从 PMContext 竞品/市场提取市场素材 | 不回灌（产出 View） |
| 2. 建模 | 双算法规模 + 三层竞品矩阵 + 情感分析 | 不回灌（产出 View） |

执行时必须依次完成上述步骤，不可跳步。步骤产出写入 `.loop/market-step1.md`、`.loop/market-step2.md`。

**产出约束**：
- TAM/SAM/SOM 必须双算法（自上而下 + 自下而上），单算法结果标 `[单算法存疑]`
- 两算法差异 >30% 标 `[数据存疑]` 并提示 PM 核查数据源
- 竞品必须三层（直接/间接/替代），缺层标 `[待补]` 不臆造竞品
- 情感分析仅在有反馈数据时做，无数据标 `[无反馈数据]` 不臆造 sentiment

**依赖检查**：双算法是否都做？差异是否标注？竞品三层是否齐？情感是否有数据依据？

**Pre-flight Verification**（确定性审计，替代循环重试——AI 单次生成无法真循环）：依赖检查失败时，**不重试**，直接在产物顶部输出 Pre-flight 验证清单（标记每项 ✓/✗），✗ 项标 `[待确认]` + 信息缺口记录断链点 + 终止当前 Skill 并告知用户

### Step 1: 读取 PMContext 提取市场素材

读取 `docs/pm-context/pm-context.md`，提取：
- "竞品/市场" → TAM 行业规模数据、竞品清单
- "用户场景" → SAM 目标细分特征
- "现状平替与摩擦力" → SOM 可获份额约束、替代品
- PM 提供的反馈数据（reviews/survey，若有）→ 情感分析输入

若 PMContext 不存在 → **🔴 STOP**：提示先运行 `/pm-need`。

### Step 2: TAM/SAM/SOM 双算法市场规模

**自上而下**（Top-down）：
```
TAM = 行业总规模 × 目标细分占比  ← PMContext 竞品/市场
SAM = TAM × 可触达比例（地理/渠道约束）  ← PMContext 边界条件
SOM = SAM × 可获份额（3 年内现实）  ← PMContext 现状平替
```

**自下而上**（Bottom-up）：
```
TAM = 目标用户数 × ARPU × 年  ← PMContext 用户场景 + [假设]ARPU
SAM = 可触达用户数 × ARPU × 年
SOM = 可获用户数 × ARPU × 年
```

交叉验证表：

| 指标 | 自上而下 | 自下而上 | 差异% | 结论 |
|---|---|---|---|---|
| TAM | <值> | <值> | <X%> | 一致/[数据存疑] |
| SAM | | | | |
| SOM | | | | |

差异 >30% → 标 `[数据存疑]`，列出两边假设差异点让 PM 核查。

### Step 3: 竞品三层矩阵

| 层 | 竞品 | 解决方案 | 优势 | 劣势 | 差异化机会 | 来源 |
|---|---|---|---|---|---|---|
| 直接竞争 | <竞品> | <方案> | <优势> | <劣势> | <机会> | PMContext <项> |
| 间接竞争 | <竞品> | ... | | | | |
| 替代品 | <平替> | <方案> | | | | PMContext 现状平替 |

每层至少 1 个，缺层标 `[待补]` 提示先 /pm-collect 补竞品扫描。差异化机会必须基于 PMContext 用户场景中竞品未满足的摩擦力。

### Step 4: 用户反馈情感分析（若有数据）

若 PM 提供反馈数据（reviews/survey/访谈记录）：
- 按用户 segment 分组
- 每段标 sentiment（正/中/负）+ 频次
- 提取 JTBD + 满意度评分
- 识别满意度模式（哪段最不满、不满集中点）

| Segment | Sentiment | 频次 | JTBD | 满意度 | 不满集中点 | 来源 |
|---|---|---|---|---|---|---|

若无反馈数据 → 标 `[无反馈数据]`，提示先 /pm-collect 收集，不臆造 sentiment。

### Step 4.5: 用户分层（User Segmentation，行为聚类）

借鉴 pm-skills/user-segmentation：从反馈数据按行为/JTBD/需求聚类，识别 ≥3 个用户层（禁仅按 demographics 分层）。

**分层规则**：
- 按 **行为 + JTBD + 未满足需求** 聚类，禁只按 demographics（年龄/性别/地域）
- 每层必须可行动（不同层应有不同产品/GTM 策略，不可行动=无效分层）
- 层数 ≥3（少于 3 层说明聚类粗糙），≤7（多于 7 层无法聚焦）

| 层 | 名称 | 规模占比 | 核心行为 | JTBD | 未满足需求 | 可行动策略 | 来源 |
|----|------|---------|---------|------|-----------|-----------|------|
| 1 | <命名> | <占比> | <使用模式> | <待办任务> | <痛点> | <对应产品/GTM 动作> | PMContext 用户场景 |
| 2 | ... | | | | | | |
| 3 | ... | | | | | | |

**分层质量校验**：
- 层间是否互斥？（同一用户不应属 2 层，否则聚类维度混淆）
- 层内是否同质？（同层用户行为/JTBD 应相似，否则聚类粗糙）
- 每层是否有可行动策略？（无策略=无效分层，应合并或重分层）

**失败模式（分层特有）**：

| 触发条件 | 一线修复 | 仍失败兜底 |
|---------|---------|-----------|
| 反馈数据不足以分层（<10 条） | 标 `[待确认]` 需补数据 | 降级为"已知用户群"不分层 |
| 分层仅按 demographics | 重新按行为/JTBD 聚类 | 标 🟡 仅 demographics 分层，结论谨慎 |
| 层间不互斥（重叠 >20%） | 重新选聚类维度 | 合并重叠层 |
| 每层无可行动策略 | 补策略或合并层 | 标 `[待确认]` 需 PM 定策略 |

**反例**：按"男/女"或"25-34/35-44"分层——这是 demographics 切片不是用户分层，无法驱动不同产品策略。

### Step 4.75: NSM 与市场规模交叉验证（借鉴 pm-marketing-growth/north-star-metric）

> 市场规模的假设应反映在北极星指标的信噪验证中——如果 SOM 太大但 NSM 设计太小（或相反），说明规模估算或 NSM 设计至少一个不准。

| 检查 | 问题 | 不一致信号 | 处置 |
|------|------|-----------|------|
| SOM 的获客假设 ↔ NSM Input Metrics | SOM 假设月获 1 万用户，但 NSM Input Metrics 未含获客渠道指标 | NSM 无法支撑 SOM 目标 | 补 Input Metrics 或共识 SOM |
| ARPU 假设 ↔ NSM 的 AARRR 付费节点 | SOM 用 ARPU ¥100，但 NSM guardrail 含"免费不可用" | ARPU 假设与产品体验冲突 | 校准 ARPU 或改 guardrail 设计 |
| 行业增速假设 ↔ NSM 周期性 | SOM 假设年增 50% 但 NSM 设计为季度脉冲式增长 | 增速假设与 NSM 节奏不匹配 | 对齐增速假设与 NSM 节奏 |
| 目标细分 ↔ pm-northstar 输出 | SAM 定义的目标细分与 pm-northstar 产出中"核心用户"定义不一致 | 两个 View 的目标用户不一致 | 标 `[冲突]` 让 PM 裁决 |

**纪律**：市场规模假设必须与 NSM（若 pm-northstar 已跑）交叉验证。不一致但不影响结论的标 🟢 可接受，直接影响结论的标 `[冲突]` 并提示 PM 统一。若 pm-northstar 尚未跑，跳过本步不阻塞。

### Step 5: 写入产物

写入 `docs/pm-context/market.md`，含双算法规模表 + 交叉验证 + 三层竞品矩阵 + 情感分析（或无数据标注）+ 用户分层 + 追溯列。

**🔴 CHECKPOINT** — 输出产物路径 + 双算法差异% + 竞品三层完成度 + 情感分析 segment 数 + `[假设]`/`[待补]` 项数。等待 PM 确认或自动进入下一步（`--auto` 模式）。

## 流程链落盘

步骤 1-2 产出完成后，写入中间工件：
- `docs/pm-context/.loop/market-step1.md`（市场素材提取 + 审计三元组）
- `docs/pm-context/.loop/market-step2.md`（双算法+竞品矩阵+情感 + 审计三元组）

## 关联增强

在"来源"列标注每数字追溯。与 pm-strategy 交叉验证（Porter 替代品威胁应 ⊆ 本 skill 替代品层，不一致标冲突）。与 pm-gtm 交叉（SAM 应 ⊇ Beachhead 细分规模）。

## 失败模式

| 触发条件 | 一线修复 | 仍失败兜底 |
|---------|---------|-----------|
| **🔴 STOP**：`docs/pm-context/pm-context.md` 不存在 | 提示先运行 `/pm-need <需求>` | 不阻塞，提示后退出 |
| **🔴 STOP**：PMContext "竞品/市场"为空 | 提示先运行 `/pm-collect` 补竞品扫描 | 竞品矩阵标 `[待补]` 降级输出 |
| TAM 行业规模数据缺失 | 标 `[假设]` 用类比行业估算 | 完全无依据则标 `[待确认]` 不给数字 |
| 双算法差异 >30% | 标 `[数据存疑]` 列假设差异点 | 不静默取平均，让 PM 核查 |
| 竞品某层无数据 | 标 `[待补]` 提示 /pm-collect | 不臆造竞品补层 |
| 无反馈数据强做情感分析 | 标 `[无反馈数据]` 提示收集 | 不臆造 sentiment |
| ARPU 无依据 | 标 `[假设]` 用竞品定价估算 | 完全无依据则 SOM 标 `[待确认]` |

## 不要做什么（反例黑名单）

| 反模式 | 为什么不要做 |
|--------|------------|
| TAM 单算法拍脑袋 | 单算法无法交叉验证，必须双算差异检查 |
| 双算法差异 >30% 静默取平均 | 平均掩盖数据问题，必须标存疑让 PM 核查 |
| 竞品只列直接竞争忽略替代品 | 替代品常是最大威胁（用户用平替而非竞品），三层缺一不可 |
| 无反馈数据臆造 sentiment | 没数据的情感分析是编故事，必须标 `[无反馈数据]` |
| 差异化机会写"更好的体验" | 不可执行，必须基于 PMContext 竞品未满足的摩擦力 |
| SOM 写"获取 10% 份额"无路径 | SOM 必须有可获路径（渠道/触达），不是许愿 |
| 跳过交叉验证直接出规模 | 交叉验证是双算法意义，跳过等于单算法 |
| 审计三元组转换操作写"将 A 转换为 A'" | 同义反复，判定为 Failure |

## 产出示例 · 实战提示

会员产品市场分析片段：

```markdown
## 市场规模双算法
| 指标 | 自上而下 | 自下而上 | 差异% | 结论 |
|---|---|---|---|---|
| TAM | 创作者工具市场 50亿 × 会员细分 20% = 10亿 | 200万创作者 × 500元 = 10亿 | 0% | 一致 |
| SAM | 10亿 × 一二线触达 40% = 4亿 | 80万可触达 × 500 = 4亿 | 0% | 一致 |
| SOM | 4亿 × 3年获 5% = 2000万 | 4万可获 × 500 = 2000万 | 0% | 一致 |

## 竞品三层
| 层 | 竞品 | 差异化机会 |
|---|---|---|
| 直接 | A 会员、B 会员 | A 无高频权益，B 价格高 |
| 间接 | C 订阅制工具 | C 非创作者专精 |
| 替代 | 免费+日历提醒 | 平替无稳定输出保障 → 付费理由 |

## 情感分析
[无反馈数据] — 建议先 /pm-collect 收集用户 reviews
```

**实战铁律**（落盘前对照）：

- **双算法是底线**：单算法 TAM 无法交叉验证，必须自上而下+自下而上
- **差异 >30% 标存疑**：不静默取平均，列假设差异点让 PM 核查
- **竞品三层缺一不可**：替代品常是最大威胁，忽略等于盲区
- **无数据不臆造 sentiment**：标 `[无反馈数据]` 比编故事诚实
- **SOM 必须有路径**：不是许愿份额，要有可获路径（渠道/触达）
- **与 pm-strategy 交叉**：Porter 替代品 ⊆ 本 skill 替代品层

### Further Reading

- [TAM/SAM/SOM Done Right](https://www.productcompass.pm/p/tam-sam-som)
- [Competitive Analysis Three Layers](https://www.productcompass.pm/p/competitor-analysis)
- [Sentiment Analysis for PMs](https://www.productcompass.pm/p/sentiment-analysis)
