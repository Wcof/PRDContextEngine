# TDD 范式写 Skill 完整示例

## 场景

为 PMSkill 写一个新 skill 教 agent 做"用户访谈纪要结构化"。

## RED — 跑 baseline

设计压力场景：让 agent 不带 skill 处理一段用户访谈转录（时间紧迫压力：PM 催结果）。

**agent verbatim 失败记录**：
1. 只总结对话不做结构化（rationalization 原文："PM 催得急，先给总结"）
2. 漏掉关键引言（rationalization："总结里说到了用户痛点就行，原话不重要"）
3. 不区分事实与推断（rationalization："都是用户说的，不用区分"）
4. 不给跟进问题（rationalization："PM 没问这个"）

## GREEN — 写 SKILL.md

针对 RED 的 4 个具体违规写 SKILL.md：

```markdown
---
name: pm-interview-notes
description: 结构化用户访谈纪要——事实/推断/引言三分+每痛点给跟进问题+时间紧迫压力下不偷工。Use when...
---
# /pm-interview-notes
## 反例黑名单（针对 RED 的 rationalization）
| 反模式 | 为什么不要做 |
|--------|------------|
| 只总结不结构化（"PM 催先给总结"） | 结构化才能驱动行动，总结是流水账 |
| 漏掉关键引言（"原话不重要"） | 引言是证据，没引言的痛点是断言 |
| 不区分事实与推断（"都是用户说的"） | 事实 vs 推断置信度不同，混淆会误导决策 |
| 不给跟进问题（"PM 没问"） | 跟进问题是下次访谈的输入，不给=断链 |
```

## REFACTOR — 闭漏洞

跑压力测试找新 rationalization：

| 压力类型 | 场景 | 新 rationalization | 补救 |
|---------|------|-------------------|------|
| 时间紧迫 | PM 催结果 | "先给结论引言之后补" | 补反例：引言未提取不下结论 |
| 权威压力 | 资深 PM 说"这样够了" | "资深 PM 说够就够" | 补反例：PM 满意≠质量达标，跑自检 |
| 沉没成本 | 已花 30 分钟 | "再花时间不划算" | 补反例：结构化是纪要价值底线，不可省 |

## 规范齐全校验

| 规范项 | 状态 |
|--------|------|
| frontmatter（name+description+Use when） | ✅ |
| Purpose/Context/Instructions/Thinking Protocol | ✅ |
| 三段式失败模式表 | ✅ |
| 反例黑名单（针对 RED） | ✅ |
| 产出示例 | ✅ |
| test-prompts.json ≥2 | ✅ |
| evals ≥3 | ✅ |
| references 按需加载 | ✅ |

## 与 darwin-skill 联动

- pm-skillauthor：创建新 skill（TDD 范式）
- darwin-skill：优化已有 skill（9 维 rubric）

## 审计三元组

`<依据集: [待文档化能力"访谈纪要结构化"+RED baseline 4 违规]> → [工具: /pm-skillauthor, 规则: RED-GREEN-REFACTOR TDD] → [转换: 从 baseline 失败推导 SKILL.md 反例黑名单，从压力测试推导 REFACTOR 补救，多对多实体映射：违规→反例→压力测试→补救] → <产出: pm-interview-notes SKILL.md+4 反例+3 REFACTOR 补救+规范齐全>`
