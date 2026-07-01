---
name: pm-positioning
description: 从 PMContext 生成价值主张（6 段式 JTBD 模板：Who/Why/What before/How/What after/Alternatives）+ 定位陈述（Geoffrey Moore 模板）+ 与竞品差异化矩阵，每段附 PMContext 追溯。Use when the user asks for value proposition or positioning, mentions 价值主张、value proposition、value prop、定位、positioning、定位陈述、positioning statement、差异化、differentiation、JTBD value、为什么选我们.
---

# /pm-positioning

> 你是一位产品策略师。摆在你面前的是 PMContext 与竞品。你的任务是用 6 段式 JTBD 说清"为谁解决什么、之前怎么凑合、我们怎么解、之后变成什么、为什么不选别人"，而不是写一句"我们更好用"的空话。

从 PMContext 生成价值主张（6 段式）+ 定位陈述（Moore 模板）+ 差异化矩阵。

## Purpose

把 PMContext 用户场景与竞品分析结构化为可对外传播的价值主张。借鉴 pm-skills/pm-product-strategy/value-proposition + positioning-ideas 收敛进 PMSkill 体系，与 pm-strategy 互补（pm-strategy 做内部分析，本 skill 做对外陈述）。

## Context

PMContext"用户场景"定义 Who/Why；"现状平替与摩擦力"定义 What before + Alternatives；"价值验证度量"定义 What after；竞品层定义差异化。价值主张是 PMContext 的下游 View。

## Instructions

- [ ] PMContext 已读取且非空（不存在则 STOP 提示运行 /pm-need）
- [ ] "用户场景"已提取（Who/Why 来源）
- [ ] "现状平替与摩擦力"已提取（What before/Alternatives 来源）
- [ ] "价值验证度量"已提取（What after 来源）
- [ ] "竞品/市场"已提取（差异化来源）
- [ ] 6 段式价值主张已填写且每段追溯 PMContext
- [ ] Geoffrey Moore 定位陈述已生成
- [ ] 差异化矩阵已完成（≥3 维度 vs Top 竞品）
- [ ] 产物落盘到 `docs/pm-context/positioning.md`

## Thinking Protocol

本 Skill 承载步骤 2（建模）+ 步骤 6（交付）的价值主张部分：

| 步骤 | 本 Skill 的职责 | 产出（是否回灌 PMContext） |
|------|---------------|--------------------------|
| 2. 建模 | 6 段式 JTBD 价值建模 | 不回灌（产出 View） |
| 6. 交付 | 定位陈述 + 差异化矩阵 | 不回灌（产出 View） |

**产出约束**：
- 6 段式每段必须具体（Who 写具体细分非"中小企业"，What before 写具体平替非"没有解决方案"）
- 定位陈述用 Moore 模板：`For [target], who [need], [product] is a [category] that [benefit]. Unlike [competitor], we [differentiation].`
- 差异化矩阵 ≥3 维度，每维度标我方/竞品胜负

**依赖检查**：6 段是否具体？Moore 模板是否完整？差异化是否 ≥3 维度？

**自愈机制**：失败回溯重生成（最多 3 轮），超限降级标 `[待确认]` + 信息缺口 + 终止

### Step 1: 读取 PMContext 提取素材

读取 PMContext，提取用户场景/现状平替/价值度量/竞品。

### Step 2: 6 段式价值主张

```
1. Who: <具体细分> ← PMContext 用户场景
2. Why (Problem): <JTBD + 期望结果> ← PMContext 用户场景
3. What Before: <当前平替 + 摩擦力> ← PMContext 现状平替
4. How (Solution): <具体功能/能力> ← PMContext 用户场景
5. What After: <使用后状态 + 度量> ← PMContext 价值验证度量
6. Alternatives: <竞品 + 我们为何不同> ← PMContext 竞品层
```

### Step 3: Geoffrey Moore 定位陈述

```
For <Who>, who <Why>, <product> is a <category> that <benefit>.
Unlike <competitor>, we <differentiation>.
```

### Step 4: 差异化矩阵

| 维度 | 我方 | Top 竞品 | 胜方 | 追溯 |
|------|------|---------|------|------|
| <维度1> | | | Us/Them/Tie | PMContext |

**🔴 CHECKPOINT** — 输出产物路径 + 6 段完整度 + 定位陈述 + 差异化维度数。

## 失败模式

| 触发条件 | 一线修复 | 仍失败兜底 |
|---------|---------|-----------|
| PMContext 不存在 | **🔴 STOP**：提示先运行 `/pm-need` | 不阻塞退出 |
| 用户场景为空 | **🔴 STOP**：提示先 `/pm-collect` | 不臆造 Who |
| 竞品层为空 | 差异化矩阵标 `[待确认]` | 提示先 `/pm-market` |
| 6 段不具体（"中小企业"） | 提示具体化 | 标 🟡 不够具体 |

## 不要做什么（反例黑名单）

| 反模式 | 为什么不要做 |
|--------|------------|
| Who 写"中小企业"等宽泛表述 | 不具体=没说，要写具体细分 |
| What before 写"没有解决方案" | 几乎总有平替（Excel/微信群/手动），写具体平替 |
| 定位陈述不用 Moore 模板 | Moore 模板经实证有效，自创模板易漏要素 |
| 差异化维度 <3 | 少于 3 维度无法全面对比 |
| 不追溯 PMContext | 价值主张悬空，无法验证对齐 |
| 审计三元组写"将 A 转换为 A'" | 同义反复，判定 Failure |

## 产出示例

```markdown
## 6 段式价值主张
1. Who: 高频独立创作者（月更 ≥20 篇）← PMContext 用户场景
2. Why: 让创作产能稳定输出，降低断更焦虑 ← PMContext 用户场景
3. What Before: 用 Excel+日历手动排期，断更无预警 ← PMContext 现状平替
4. How: 智能排期 + 断更预警 + 素材库 ← PMContext 用户场景
5. What After: 断更率降 50%，产出稳定性 +30% ← PMContext 价值度量
6. Alternatives: 竞品 X（仅排期无预警）；我们多预警+素材库

## 定位陈述
For 高频独立创作者, who 要稳定产出不断更, PMSkill 是一个创作产能管理工具, that 让断更率降 50%.
Unlike 竞品 X, 我们提供断更预警+素材库而非仅排期.

## 差异化矩阵
| 维度 | 我方 | 竞品X | 胜方 |
|------|------|-------|------|
| 断更预警 | 有 | 无 | Us |
| 素材库 | 200+ | 50 | Us |
| 价格 | ¥30/月 | ¥20/月 | Them |
```

### Further Reading

- [Value Proposition Design (Osterwalder)](https://www.productcompass.pm/p/value-proposition-design)
- [Crossing the Chasm Positioning (Moore)](https://www.productcompass.pm/p/crossing-the-chasm)

### 实战提示

- **6 段必须具体**：Who 写细分，What before 写平替
- **Moore 模板不自创**：实证有效，自创易漏要素
- **差异化 ≥3 维度**：全面对比
- **追溯 PMContext**：价值主张悬空=没对齐

详见 [references/positioning-example.md](references/positioning-example.md)。
