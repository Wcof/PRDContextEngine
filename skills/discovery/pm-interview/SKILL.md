---
name: pm-interview
description: 从 PMContext 生成结构化用户访谈脚本——JTBD 探查 + The Mom Test 纪律（问过去不问未来、问生活不问想法、不 pitch），含暖场/核心探索/收尾三段式 + 记录模板。Use when the user asks for interview script or user research, mentions 访谈脚本、interview、用户访谈、user research、Mom Test、JTBD 探查、discovery research、客户访谈、qualitative research.
---

# /pm-interview

> 你是一位用户研究员，正在从 PMContext 中提取访谈目标，生成可执行的访谈脚本——**通过对话驱散"迷雾"，探查用户真实 JTBD 而非预设答案。** 问"上次你具体怎么做的"才有信息，问"你会用 X 吗"只会听到客套话。

从 PMContext 输出用户访谈脚本。基于 PMContext 的用户场景/现状平替/摩擦力，生成暖场 + 核心探索 + 收尾三段式脚本 + 记录模板。

## Purpose

从 PMContext 输出用户访谈脚本。脚本遵循 The Mom Test 纪律（问过去不问未来、问生活不问想法、不 pitch），核心探索段用 JTBD 框架探查真实行为。每个问题追溯到 PMContext 中的具体项。

## Context

PMContext 中有用户场景定义和现状平替/摩擦力描述。本 skill 提取这些信息，生成针对目标用户的访谈脚本。脚本产出后，PM 拿去对真实用户访谈，访谈结果回灌 `/pm-collect` 作为新材料。

## Instructions

- [ ] PMContext 已读取且非空（不存在则 STOP 提示运行 /pm-need）
- [ ] "用户场景"维度已提取（谁在什么场景下用）
- [ ] "现状平替与摩擦力"维度已提取（用户目前用什么土办法、最痛苦的点）
- [ ] "边界条件"中的异常场景已提取（作为探查边缘行为的素材）
- [ ] 访谈目标已定义（本次访谈要回答什么决策问题）
- [ ] 目标受访者画像已从 PMContext 用户角色提取
- [ ] 脚本含暖场/核心探索/收尾三段
- [ ] 核心探索段用 JTBD 四象限探查（当前行为/痛点/期望结果/愿意付出）
- [ ] 所有问题遵守 The Mom Test 四规则
- [ ] 含记录模板（Participant/Key Jobs/Current Solution/Biggest Pain/Desired Outcome/Willingness to Pay/Surprise Finding）
- [ ] 每个问题在"来源"列标注追溯到的 PMContext 项
- [ ] 产物落盘到 `docs/pm-context/interview-script.md`

## Thinking Protocol

本 Skill 承载 PM Thinking Loop 的步骤 1（理解）的访谈素材准备：

| 步骤 | 本 Skill 的职责 | 产出（是否回灌 PMContext） |
|------|---------------|--------------------------|
| 1. 理解（访谈准备） | 从 PMContext 用户场景/摩擦力提取访谈目标，生成结构化脚本 | 不回灌（产出 View） |

执行时必须依次完成上述步骤，不可跳步。步骤产出写入 `.loop/interview-step1.md`。

**产出约束**：
- 访谈目标必须对应 PMContext 中的信息缺口或待验证假设
- 每个问题必须追溯到 PMContext 中的具体项，无追溯的问题标 `[假设]`
- 问题必须遵守 The Mom Test 四规则（见下方）

**依赖检查**：是否有未追溯到 PMContext 的问题？是否有违反 Mom Test 规则的问题？

**Pre-flight Verification**（确定性审计，替代循环重试——AI 单次生成无法真循环）：依赖检查失败时，**不重试**，直接在产物顶部输出 Pre-flight 验证清单（标记每项 ✓/✗），✗ 项标 `[待确认]` + 信息缺口记录断链点 + 终止当前 Skill 并告知用户

### Step 1: 读取 PMContext 提取访谈素材

读取 `docs/pm-context/pm-context.md`，提取：
- "用户场景"维度：谁在什么场景下用？达到什么目的？
- "现状平替与摩擦力"维度：用户目前用什么土办法？最痛苦的点？
- "边界条件"中的异常场景
- "假设清单与验证计划"中置信度 ≤ 6 的假设（优先访谈验证）

若 PMContext 不存在 → **🔴 STOP**：提示先运行 `/pm-need`。

### Step 2: 定义访谈目标

从 PMContext 信息缺口和低置信度假设中，提炼本次访谈要回答的 3-5 个决策问题：
```
访谈目标：
1. 验证 [假设: 用户流失与续费流程负相关, 6/10]
2. 探查 [待确认] 当前续费转化率基线
3. 了解现状平替中"手动记录到期日"的真实操作
```

### Step 3: 生成三段式脚本

#### 暖场（2-3 分钟）
- 自我介绍 + 访谈目的（学习而非推销）
- 设定预期："没有对错答案，我们想了解你的真实经历"
- 确认可用时间

#### 核心探索：JTBD 四象限（15-20 分钟）

**当前行为（过去时，具体实例）**：
- "跟我讲讲上次你 [做某事] 的经过，发生了什么？"
- "你用了什么工具或方法？"
- "花了多长时间？还有谁参与？"

**痛点与挫败（观察而非引导）**：
- "那件事最难的部分是什么？"
- "如果有个魔法棒，你会改变什么？"
- "你试过什么解决办法？结果怎样？"

**期望结果（用他们的话，不是你的）**：
- "对你来说'好'是什么样？"
- "你怎么知道这件事运作良好？"

**愿意付出（skin in the game）**：
- "你目前在这件事上花多少时间/钱？"
- "你找过更好的解决方案吗？找到了什么？"
- "要解决这个问题你会放弃什么？"

#### 收尾（3-5 分钟）
- "有没有我没问但你觉得重要的？"
- "我还该找谁聊？"
- 感谢 + 后续步骤

### Step 4: 生成记录模板

```markdown
## 访谈记录

**Participant:** [姓名 / 编号]
**Date:** [日期]
**访谈目标:** [本次要回答的决策问题]

**Key Jobs:** [他们想完成什么]
**Current Solution:** [目前用什么]
**Biggest Pain:** [第一挫败点]
**Desired Outcome:** [成功是什么样]
**Willingness to Pay:** [投入多少 / 愿投入多少]
**Surprise Finding:** [意外发现]
**Follow-up:** [后续步骤]

**强情绪信号:** [出现强情绪的话题——真实痛点/愉悦的信号]
```

### Step 5: 写入产物

写入 `docs/pm-context/interview-script.md`，格式：

```markdown
# 访谈脚本

> 来源: PMContext <需求名>
> 访谈目标: N 个 | 目标受访者: <画像> | 预计时长: 30-40 分钟

## 访谈目标
1. <目标1> ← PMContext [假设: ...]
2. <目标2> ← PMContext [待确认]: ...

## 目标受访者
<画像描述> ← PMContext 用户场景

## 脚本

### 暖场（2-3 分钟）
- <问题1> ← 来源: 暖场标准流程
- <问题2>

### 核心探索：JTBD（15-20 分钟）

#### 当前行为
- <问题> ← 来源: PMContext 现状平替与摩擦力
- <问题> ← 来源: PMContext 用户场景

#### 痛点与挫败
- <问题> ← 来源: PMContext 摩擦力
- <问题> ← 来源: PMContext [假设: ...]

#### 期望结果
- <问题> ← 来源: PMContext 用户场景
- <问题> ← 来源: PMContext [待确认]: 价值验证

#### 愿意付出
- <问题> ← 来源: PMContext [假设: ...]

### 收尾（3-5 分钟）
- <问题>

## 探查技巧
- "多说一点那个" — 打开任何话题
- "为什么？"（轻问，2-3 次）— 到达根因
- "能给个具体例子吗？" — 从观点到事实
- "然后呢？" — 跟着故事走
- "那让你感觉如何？" — 捕捉情绪强度

## The Mom Test 规则（访谈时遵守）
- 问他们的生活，不问你的想法
- 问过去，不问未来（"你会用 X 吗？"没用）
- 少说多听，目标 80/20
- 访谈中绝不 pitch
- 找强情绪信号——真实痛点或愉悦
- 客套是噪音——"听起来很酷！"没信息量

## 记录模板
<上方记录模板>

## 访谈后回灌
访谈完成后，将记录丢给 `/pm-collect` 作为新材料（来源标注 `访谈: <参与者编号>`），再调用 `/pm-refine --incremental` 增量精炼。
```

**🔴 CHECKPOINT** — 输出产物路径 + 访谈目标数 + 问题数 + `[假设]` 项数。等待 PM 确认或自动进入下一步（`--auto` 模式）。

## 流程链落盘

步骤 1（理解）产出完成后，写入中间工件：
- `docs/pm-context/.loop/interview-step1.md`（访谈目标追溯映射 + 审计三元组）

## 关联增强

在"来源"列标注每个问题追溯到的 PMContext 项。无来源的问题标 `[假设]`。

## 失败模式

| 触发条件 | 一线修复 | 仍失败兜底 |
|---------|---------|-----------|
| `docs/pm-context/pm-context.md` 不存在 | **🔴 STOP**：输出"未找到 PMContext，先运行 `/pm-need <需求>`" | 不阻塞，提示后退出 |
| PMContext 中"用户场景"维度为空或全标 `[待确认]` | **🔴 STOP**：输出"用户场景未精炼，先运行 `/pm-refine` 补全 P0 维度" | 不臆造用户画像，提示 PM 先补全 |
| PMContext 中无"现状平替与摩擦力"描述 | 🟡 WARNING：核心探索段"当前行为"问题改为开放式，标 `[假设]` | 不阻塞，脚本中标注"摩擦力信息缺失，需访谈中探查" |
| 生成的问题违反 Mom Test 规则（如"你会用 X 吗？"） | 改写为过去时具体实例问法 | 仍无法改写则删除该问题，标信息缺口 |
| 访谈目标无法追溯到 PMContext 信息缺口或假设 | 重新从 PMContext 假设清单提取目标 | 目标确实无依据则标 `[假设]` 并提示 PM 确认 |
| PMContext 假设清单全为高置信度（≥8）无低置信度项 | 访谈目标转向信息缺口清单的 `[待确认]` 项 | 仍无目标则提示"PMContext 已较完整，访谈价值有限" |

## 不要做什么（反例黑名单）

| 反模式 | 为什么不要做 |
|--------|------------|
| 问"你会用 X 功能吗？" | 未来时态问题只会得到客套回答，The Mom Test 明确禁止 |
| 访谈中 pitch 产品想法 | pitch 会污染受访者反馈，得到的是恭维而非真实行为 |
| 一次问多个问题 | 增加受访者认知负荷，回答质量下降 |
| 问题不追溯到 PMContext | 访谈目标不聚焦，回收的素材无法回灌精炼 |
| 问未来时态（"你希望有什么功能？"） | 未来意愿≠过去行为，行为才是真实信号 |
| 忽略强情绪信号 | 强情绪（沮丧/兴奋/愤怒）标记真实痛点，是访谈最有价值产出 |
| 把客套话当需求信号 | "听起来很酷"是噪音，不是需求验证 |
| 审计三元组转换操作写"将 A 转换为 A'" | 同义反复，无推理密度，判定为 Failure |
| 审计三元组转换操作写"基于上述依据产出" | 空话，未阐明具体推导逻辑，判定为 Failure |

## 产出示例 · 实战提示

会员续费访谈脚本片段（完整脚本模板与记录模板详见 [references/interview-templates.md](references/interview-templates.md)）：

```markdown
### 核心探索：JTBD

#### 当前行为
- "跟我讲讲上次你续费会员的经过，从头到尾发生了什么？" ← 来源: PMContext 现状平替"手动续费"
- "你当时用了什么方式续费？App 里、网页、还是客服？" ← 来源: PMContext 用户场景

#### 痛点与挫败
- "续费过程最难的部分是什么？" ← 来源: PMContext 摩擦力"续费太麻烦，要重新填信息"
- "你试过什么办法避免重新填信息？" ← 来源: PMContext [假设: 用户流失与续费流程负相关, 6/10]
```

详见 [references/interview-example.md](references/interview-example.md)（完整访谈脚本示例 + Mom Test 问题改写对照表）。

**实战铁律**（落盘前对照）：

- **过去时 + 具体实例是金标准**："上次你具体怎么做的？"远胜"你通常怎么做？"
- **80/20 听说比**：受访者说 80%，访谈者说 20%，多说多听
- **"为什么"轻问 2-3 次**：到达根因，但别变成审讯
- **强情绪 = 真实信号**：受访者兴奋/沮丧/愤怒的地方就是真实痛点所在
- **访谈结果回灌 `/pm-collect`**：访谈记录是新素材，来源标 `访谈: <编号>`，再 `/pm-refine --incremental` 增量精炼

### Further Reading

- [The Mom Test (Rob Fitzpatrick)](https://www.momtestbook.com/)
- [User Interviews: The Ultimate Guide](https://www.productcompass.pm/p/interviewing-customers-the-ultimate)
- [Continuous Discovery Habits (Teresa Torres)](https://www.productcompass.pm/p/cpdm)
