---
name: pm-skillauthor
description: Use when the user asks to write or create a new skill, mentions 写 skill、create skill、author skill、新 skill、skill 编写、TDD for skills、RED GREEN REFACTOR、skill development.
metadata:
  internal: true
---

# /pm-skillauthor

> 你是一位 skill 作者。摆在你面前的是一个待文档化的产品能力。你的任务用 TDD 范式写 skill——先看 agent 不带 skill 怎么错的，再写 SKILL.md 让它做对，再闭漏洞，而不是直接写一份"看起来不错"的文档。

用 TDD 范式（RED-GREEN-REFACTOR）为 PMSkill 写新 skill。

## Purpose

为 PMSkill 生态写新 skill 时用 TDD 范式保证质量。借鉴 superpowers/writing-skills + skills/write-a-skill + writing-great-skills 收敛进 PMSkill，与 darwin-skill 联动（darwin 优化，本 skill 创建）。

## Context

PMSkill 需扩展新能力时用本 skill。新 skill 必须符合 Anthropic 规范 + PMSkill 风格（frontmatter + Purpose/Context/Instructions/Thinking Protocol/失败模式三段式/反例黑名单/产出示例 + references + test-prompts + evals）。

### 建不建 skill 的决策门（借鉴 superpowers/writing-skills "When to Create a Skill"）

> 不是所有能力都该建 skill——机械约束用自动化，项目约定写 instructions，一次性方案不建文档。

| 该建 skill | 不该建 skill |
|-----------|-------------|
| 技术非直觉（你不假思索做不对的） | 一次性方案（用完不再用） |
| 跨项目复用（非项目特定） | 项目特定约定（写 .atomcode.md/AGENTS.md） |
| 模式广泛适用（他人受益） | 标准实践已有良好文档（重复造轮子） |
| 需要判断调用（非机械） | 机械约束可用 regex/校验自动化的（自动化，省文档） |

**决策门**：待文档化能力命中"该建"≥3 且"不该建"=0 → 建；否则不建，走对应替代（自动化/instructions/不建）。

### Skill 类型（借鉴 writing-skills Skill Types）

| 类型 | 定义 | PMSkill 示例 |
|------|------|-------------|
| Technique | 有步骤的具体方法 | pm-align, pm-triage, pm-grill |
| Pattern | 思考问题的方式 | pm-ideation, pm-refine, pm-premortem |
| Reference | API/语法/工具文档 | pm-sql, pm-abtest（含指标定义参考） |

新 skill 建前先定类型——Technique 重步骤可执行性，Pattern 重思维框架，Reference 重查得准。类型定错会导致 dim2/dim5 失分。

## Instructions

- [ ] 待文档化能力已确认（用户描述或 PMContext 推导）
- [ ] RED：跑 baseline 看 agent 不带 skill 怎么错
- [ ] GREEN：写 SKILL.md（Anthropic 规范 + PMSkill 风格）让 agent 做对
- [ ] REFACTOR：闭漏洞（跑压力测试找 rationalization）
- [ ] frontmatter 规范（name + description ≤1024 + Use when 触发词）
- [ ] 三段式失败模式表
- [ ] 反例黑名单章节
- [ ] test-prompts.json ≥2 + evals ≥1（建议 ≥3）
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

**Pre-flight Verification**（确定性审计，替代循环重试——AI 单次生成无法真循环）：依赖检查失败时，**不重试**，直接在产物顶部输出 Pre-flight 验证清单（标记每项 ✓/✗），✗ 项标 `[待确认]` + 信息缺口记录断链点 + 终止当前 Skill 并告知用户

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

### Step 2.5: Skill 写作最佳实践（借鉴 skills/writing-great-skills）

GREEN 阶段按以下最佳实践精炼 SKILL.md 质量：

| 实践 | 说明 | 检查 |
|------|------|------|
| **Leading Words** | 用紧凑概念锚定行为（如"追光灯""迷雾""承重墙"），代替散装说明 | 全文是否有一个重复出现的核心隐喻？ |
| **渐进披露** | 信息层级：in-skill step → in-skill reference → external reference，SKILL.md 保持精干 | 每段是否必须 inline？能否推入 references/？ |
| **Completion Criterion** | 每 Step 结束时给出可检查的完成条件（禁"完成 X"写"每修改文件已追溯，gap=0"） | 每 Step 末尾是否有可断言的条件？ |
| **Premature Completion 防御** | 后续步骤在视野内会诱使 agent 提前结束当前步 | 长 Step 是否需隐藏后续步（sequence split）？ |
| **No-op 裁剪** | 逐句跑 no-op 测试——删掉那句话输出会变吗？不会=删 | 每段是否有不可替代的信息？ |
| **Single Source of Truth** | 同一概念只在一处定义，不重复 | 规则/定义是否出现在多处？ |

**Leading Word 示例**（PMSkill 生态可用的 compact concepts）：
- **"追光灯"**：PMContext 是唯一 Entity，所有 View 追光它（防止 View 脱离 PMContext 凭空生成）
- **"承重墙"**：PMContext 中承重假设，打掉产品结构就塌（关联 pm-grill 红队攻击目标）
- **"迷雾"**：信息缺口/`[待确认]` 项，PMContext 中待驱散的区域

GREEN 产出必须过 Step 2.5 至少 4 项检查，不过标 🟡 需精炼。

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

## 产出示例 · 实战提示

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

**实战铁律**（落盘前对照）：

- **RED 先跑**：没 baseline 的 skill 是猜测（Iron Law）
- **GREEN 针对 RED**：不写泛泛指导
- **REFACTOR 跑压力测试**：时间/权威/沉没成本
- **规范齐全**：frontmatter + 三段式 + 反例 + evals（≥1，建议 ≥3）
- **联动 darwin-skill**：本 skill 创建，darwin 优化

详见 [references/skillauthor-example.md](references/skillauthor-example.md)。

### Further Reading

- [Writing Skills (superpowers)](https://github.com/obra/superpowers)
- [Anthropic Skill Authoring Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Writing Great Skills (skills project)](https://github.com/obra/skills)
