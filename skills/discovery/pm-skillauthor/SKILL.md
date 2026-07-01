---
name: pm-skillauthor
description: 用 TDD 范式（RED-GREEN-REFACTOR）为 PMSkill 写新 skill——先跑 baseline 看 agent 不带 skill 怎么错的（RED）→ 写 SKILL.md（GREEN）→ 闭漏洞（REFACTOR），符合 Anthropic skill 规范。Use when the user asks to write or create a new skill, mentions 写 skill、create skill、author skill、新 skill、skill 编写、TDD for skills、RED GREEN REFACTOR、skill development.
---

# /pm-skillauthor

> 你是一位 skill 作者。摆在你面前的是一个待文档化的产品能力。你的任务用 TDD 范式写 skill——先看 agent 不带 skill 怎么错的，再写 SKILL.md 让它做对，再闭漏洞，而不是直接写一份"看起来不错"的文档。

用 TDD 范式（RED-GREEN-REFACTOR）为 PMSkill 写新 skill。

## Purpose

为 PMSkill 生态写新 skill 时用 TDD 范式保证质量。借鉴 superpowers/writing-skills + skills/write-a-skill + writing-great-skills 收敛进 PMSkill，与 darwin-skill 联动（darwin 优化，本 skill 创建）。

## Context

PMSkill 需扩展新能力时用本 skill。新 skill 必须符合 Anthropic 规范 + PMSkill 风格（frontmatter + Purpose/Context/Instructions/Thinking Protocol/失败模式三段式/反例黑名单/产出示例 + references + test-prompts + evals）。

## Instructions

- [ ] 待文档化能力已确认（用户描述或 PMContext 推导）
- [ ] RED：跑 baseline 看 agent 不带 skill 怎么错
- [ ] GREEN：写 SKILL.md（Anthropic 规范 + PMSkill 风格）让 agent 做对
- [ ] REFACTOR：闭漏洞（跑压力测试找 rationalization）
- [ ] frontmatter 规范（name + description ≤1024 + Use when 触发词）
- [ ] 三段式失败模式表
- [ ] 反例黑名单章节
- [ ] test-prompts.json ≥2 + evals ≥3
- [ ] references 按需加载
- [ ] 产物落盘 skills/<bucket>/<skill-name>/

## Thinking Protocol

本 Skill 承载步骤 6（交付）的 skill 创作部分：

| 步骤 | 本 Skill 的职责 | 产出（是否回灌 PMContext） |
|------|---------------|--------------------------|
| 6. 交付 | TDD 范式 skill 文档 | 不回灌（创建 skill） |

**产出约束**（借鉴 superpowers/writing-skills Iron Law）：
- **NO SKILL WITHOUT FAILING TEST FIRST**——没看过 baseline 失败的 skill 不知道教的对不对
- RED 必须记录 agent 的 verbatim rationalization（不是总结，是原文）
- GREEN 的 SKILL.md 必须针对 RED 记录的具体违规，不写泛泛指导
- REFACTOR 必须跑压力测试（时间/权威/沉没成本压力）找新 rationalization

**依赖检查**：RED 是否跑？GREEN 是否针对 RED？REFACTOR 是否跑压力测试？规范是否齐全？

**自愈机制**：失败回溯（最多 3 轮），超限降级标 `[待确认]` + 终止

### Step 1: RED — 跑 baseline

设计压力场景，让 agent 不带 skill 执行，记录 verbatim 失败：
- 做了什么选择？
- 用了什么 rationalization（原文）？
- 哪些压力触发违规？

### Step 2: GREEN — 写 SKILL.md

针对 RED 记录的具体违规写 SKILL.md（Anthropic 规范 + PMSkill 风格）：
- frontmatter（name + description + Use when）
- Purpose/Context/Instructions/Thinking Protocol
- 三段式失败模式表
- 反例黑名单（针对 RED 的 rationalization）
- 产出示例 + references

### Step 3: REFACTOR — 闭漏洞

跑压力测试（时间/权威/沉没成本），找新 rationalization，补 SKILL.md。

**🔴 CHECKPOINT** — 输出新 skill 路径 + RED 记录 + REFACTOR 漏洞数。

## 失败模式

| 触发条件 | 一线修复 | 仍失败兜底 |
|---------|---------|-----------|
| 待文档化能力不清 | **🔴 STOP**：提示用户描述能力 | 不臆造 skill |
| 跳过 RED 直接写 | **🔴 STOP**：没 baseline 的 skill 是猜测 | 必须先 RED |
| GREEN 不针对 RED | 重写针对 RED 具体违规 | 标 🟡 泛泛指导 |
| REFACTOR 漏压力测试 | 补时间/权威/沉没成本压力 | 标 `[待确认]` |

## 不要做什么（反例黑名单）

| 反模式 | 为什么不要做 |
|--------|------------|
| 跳过 RED 直接写 SKILL.md | 没 baseline 的 skill 不知道教的对不对（superpowers Iron Law） |
| GREEN 写泛泛指导 | 必须针对 RED 的具体 rationalization |
| REFACTOR 漏压力测试 | 没压力测试的 skill 在真实场景会崩 |
| frontmatter 缺触发词 | Agent 无法路由到 skill |
| 缺三段式失败模式 | 不符合 PMSkill 风格，dim3 扣分 |
| 缺反例黑名单 | 不符合 dim9，skill 无"不要做什么" |
| 审计三元组写空话 | 判定 Failure |

## 产出示例

```markdown
## RED baseline 记录
场景: 让 agent 做 A/B 测试分析
agent 不带 skill 的失败:
- 只看转化率差值不看 p-value（rationalization: "差值大就是显著"）
- 跳过 guardrail（rationalization: "主指标赢了就行"）

## GREEN SKILL.md
[针对上述违规写 pm-abtest SKILL.md，反例黑名单含"只看差值不看 p-value"]

## REFACTOR
压力测试: 时间紧迫（"PM 催结果"）
新 rationalization: "先给结论 p-value 之后再补"
→ 补反例: "p-value 未算完不下结论"
```

### Further Reading

- [Writing Skills (superpowers)](https://github.com/obra/superpowers)
- [Anthropic Skill Authoring Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Writing Great Skills (skills project)](https://github.com/obra/skills)

### 实战提示

- **RED 先跑**：没 baseline 的 skill 是猜测（Iron Law）
- **GREEN 针对 RED**：不写泛泛指导
- **REFACTOR 跑压力测试**：时间/权威/沉没成本
- **规范齐全**：frontmatter + 三段式 + 反例 + evals
- **联动 darwin-skill**：本 skill 创建，darwin 优化

详见 [references/skillauthor-example.md](references/skillauthor-example.md)。
