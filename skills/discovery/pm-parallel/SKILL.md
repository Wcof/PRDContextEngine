---
name: pm-parallel
description: Use when the user asks for parallel agent dispatch or concurrent tasks, mentions 并行、parallel、并发、concurrent、多 agent、dispatch agents、subagent、任务分片、task partition、独立性校验.
metadata:
  internal: true
---

# /pm-parallel

> 你是一位任务调度师。摆在你面前的是 ≥2 个独立任务（如"同时调研 3 个竞品"+"同时生成 4 类草图"）。你的任务是分派并行子 agent——校验独立性、分片、合并结果、标冲突，而不是串行一个个跑浪费时间。

当 ≥2 独立任务时分派并行子 agent 执行。

## Purpose

把 PMSkill 的可并行任务加速。借鉴 superpowers/dispatching-parallel-agents + subagent-driven-development 收敛进 PMSkill，与 pm-sketch/pm-market 等多产物 skill 联动。

## Context

PMSkill 多 skill 场景（如 pm-sketch 生成 4 类草图、pm-market 调研多竞品）可并行。本 skill 校验独立性后分派，合并结果。

## Instructions

- [ ] 任务数 ≥2（<2 不需并行）
- [ ] 独立性校验：任务间无共享状态/无顺序依赖
- [ ] 每任务分派子 agent + 明确输入/输出
- [ ] 结果合并 + 冲突标 `[冲突]`
- [ ] 失败子 agent 不阻塞其他
- [ ] 输出并行执行报告

## Thinking Protocol

本 Skill 承载步骤 6（交付）的并行编排部分：

| 步骤 | 本 Skill 的职责 | 产出（是否回灌 PMContext） |
|------|---------------|--------------------------|
| 6. 交付 | 任务分片 + 并行调度 + 合并 | 不回灌（编排 View） |

**产出约束**：
- 独立性校验必须显式（任务间共享状态=不可并行）
- 每子 agent 输入/输出必须明确（避免重叠）
- 失败子 agent 隔离，不阻塞其他
- 合并时冲突标 `[冲突]` 不静默覆盖

**依赖检查**：任务是否 ≥2？独立性是否校验？输入/输出是否明确？

**Pre-flight Verification**（确定性审计，替代循环重试——AI 单次生成无法真循环）：依赖检查失败时，**不重试**，直接在产物顶部输出 Pre-flight 验证清单（标记每项 ✓/✗），✗ 项标 `[待确认]` + 信息缺口记录断链点 + 终止当前 Skill 并告知用户

### Step 1: 任务识别 + 独立性校验

| 任务 | 输入 | 输出 | 与其他任务共享状态? |
|------|------|------|-------------------|
| 调研竞品 X | PMContext 竞品层 | battlecard-x.md | 无 |
| 调研竞品 Y | PMContext 竞品层 | battlecard-y.md | 无（读同一源不冲突） |

任一任务共享可变状态 → **🔴 STOP** 不可并行，改串行。

### Step 2: 分派子 agent（隔离上下文，借鉴 superpowers/dispatching-parallel-agents）

> **核心原则**：子 agent **不得继承当前会话上下文/历史**——你精确构造它需要的最小上下文。继承会话历史会让子 agent 被无关信息干扰 + 挤占其 context window。你保留自己的 context 做协调，子 agent 拿到的应是"刚好够完成这一任务"的纯净输入。

每子 agent 明确：

| 字段 | 内容 | 为什么 |
|------|------|--------|
| 任务描述 | 一句话目标（如"调研竞品 X 的定价策略"） | 聚焦，不发散 |
| 输入文件 | 精确路径（如 `docs/pm-context/pm-context.md` 竞品段） | 不让它自己找，避免读偏 |
| 输出文件 | 精确路径（如 `docs/pm-context/battlecard-x.md`） | 避免输出重叠覆盖 |
| skill 调用 | 具体命令（如 `/pm-battlecard --competitor X`） | 不让子 agent 猜该用哪个 skill |
| 边界 | 不做什么（如"只调研定价，不调研功能"） | 防子 agent 越界扩张任务 |

### Step 2.1: PMSkill Runtime Capsule（强制注入）

> 子 agent 不继承当前会话上下文是对的，但**不能因此丢失 Skill 运行规范**。每个子 agent 必须拿到一份最小、完整、可审计的 Runtime Capsule；没有 capsule 的派单视为违规，必须改串行或补齐后再派。

每个子 agent prompt 必须以如下 capsule 开头（按实际路径填充，不得只写“请遵守 PMSkill”）：

```yaml
pmskill_runtime_capsule:
  project_root: <repo root>
  agent_rules:
    - CONTEXT.md
    - .atomcode.md | CLAUDE.md | AGENTS.md | README.md 中存在者
  caller_skill:
    name: <发起方 skill>
    skill_file: <caller/SKILL.md>
    pinned_file: <caller/PINNED.md，如存在>
  target_skill:
    name: <目标 skill>
    skill_file: <target/SKILL.md>
    pinned_file: <target/PINNED.md，如存在>
  artifact_root: <产物目录，如 docs/pm-context/>
  pmcontext: <artifact_root>/pm-context.md
  required_inputs:
    - <本任务必须读取的源文件/缓存/设计规范>
  required_outputs:
    - path: <必须落盘的文件>
      contract: <格式/字段/验收标准>
  hard_gates:
    - <不得跳过的检查点，如 content-plan/design-profile/V1-V3 验收>
  failure_policy: <失败不伪装成功；写失败原因；必要时 fallback 或交回父 agent>
  isolation_policy: 子 agent 不读父会话历史，只读 capsule 指定文件
```

**Pencil / 原型类子任务额外字段**：

```yaml
prototype_capsule:
  content_plan: <artifact_root>/sketch/prototype-content-plan.json
  design_profile: <artifact_root>/sketch/prototype-design-profile.json
  design_source_manifest: <artifact_root>/sketch/design-source-manifest.json
  token_contract: <resolved concrete tokens / token_digest>
  component_contract: <button/table/form/card/nav/modal 等组件规范>
  required_manifest_fields:
    - design_profile
    - token_digest
    - component_coverage
    - design_violation_count
    - ue_coverage
```

子 agent 返回结果必须包含 `capsule_ack`：已读取哪些 capsule 文件、哪些硬门通过、哪些未通过。父 agent 合并时若 `capsule_ack` 缺失或未读取目标 `PINNED.md/SKILL.md`，该子任务判失败，不得合并为成功产物。

**反模式**（借鉴 dispatching-parallel-agents "never inherit session context"）：
- ❌ "你去调研下竞品"（无输入/输出/边界，子 agent 会乱跑）
- ✅ "读 pm-context.md §竞品X 段，用 /pm-battlecard 生成 battlecard-x.md，只覆盖定价不覆盖功能"

**上下文构造检查**：派单前自检——子 agent 拿到「任务 5 字段 + Runtime Capsule」能否不读会话历史就完成？不能=构造不足，补全再派。

### Step 2.5: 任务审查（借鉴 superpowers/subagent-driven-development "per-task review"）

> 每子 agent 任务完成后必须加审查环节——不是"并行的结果合起来看看"，而是**每任务独立审查**：是否满足 spec、代码质量是否达标。不审查的并行=可能批量出错。

**审查规格**（每子 agent 完成自检）：

| 检查 | 标准 | 不过处理 |
|------|------|---------|
| 输出符合目标 | 产出是否满足任务描述的目标 | 标 `[待修复]` 退回子 agent |
| 输入完整使用 | 是否读了指定输入文件 | 标 `[漏读取]` 补读再产出 |
| 边界不越界 | 是否做到了"不做的事"（边界） | 标 `[越界]` 删越界内容 |
| 格式合规 | 输出格式是否匹配预期 | 标 `[格式不合]` 修正格式 |
| Skill 合规 | 是否读取并遵守 target `PINNED.md/SKILL.md`，是否返回 `capsule_ack` | 缺失则判失败，补 capsule 后重派或改串行 |
| 设计合规（原型任务） | 是否消费 design profile / design source manifest / token + component contract | 不合规则回退本地实现或重派 |

**不断续执行**（借鉴 subagent-driven-development continuous execution）：
- 子 agent 之间不中断等待 PM 确认——每任务完成后自动审查、自动流转到下一任务
- 仅当任务阻塞（无法自修复的依赖/歧义）或全部完成时才停
- "该继续吗？"类的确认提示浪费 PM 时间——直接执行

**审查报告模板**：
```
## 并行任务审查报告
| 任务 | 子 agent | 输出 | 审查 | 状态 |
|------|---------|------|------|------|
| 调研竞品X | agent-1 | battlecard-x.md | ✅ 全部通过 | ✅ 完成 |
| 调研竞品Y | agent-2 | battlecard-y.md | 🟡 [格式不合] 缺排版 | 🟡 需修正 |
| 生成线框图 | agent-3 | wireframe.md | 🟡 [越界] 加了 IA 内容 | 🟡 需剥离 |
```

### Step 3: 合并结果 + 冲突标注

子 agent 结果合并，冲突标 `[冲突]`。

**🔴 CHECKPOINT** — 输出并行报告 + 任务数 + 成功/失败数 + 冲突数。

## 失败模式

| 触发条件 | 一线修复 | 仍失败兜底 |
|---------|---------|-----------|
| 任务 <2 | **🔴 STOP**：不需并行，串行执行 | 不阻塞 |
| 独立性校验失败（共享状态） | **🔴 STOP**：改串行 | 不并行 |
| 子 agent 超时 | 隔离失败，其他继续 | 标 `[待确认]` 该任务 |
| 结果冲突 | 标 `[冲突]` 让 PM 裁决 | 不静默覆盖 |

## 不要做什么（反例黑名单）

| 反模式 | 为什么不要做 |
|--------|------------|
| 共享可变状态强并行 | 数据竞争，结果错乱 |
| 子 agent 输入/输出不明确 | 重叠输出=互相覆盖 |
| 子 agent 继承会话历史（违反隔离原则） | 无关信息干扰+挤占 context，必须构造纯净最小上下文 |
| 派单不标边界（"去调研竞品"） | 子 agent 越界扩张任务，必须标"只做什么不做什么" |
| 失败子 agent 阻塞其他 | 一个失败全卡，违背并行初衷 |
| 冲突静默覆盖 | 丢失信息，必须标 `[冲突]` |
| 任务 <2 强并行 | 并行开销 > 收益，串行更优 |
| 审计三元组写空话 | 判定 Failure |

## 产出示例 · 实战提示

```markdown
## 并行任务（3 个，独立性 ✅）
| 任务 | 子 agent | 输出 | 状态 |
|------|---------|------|------|
| 调研竞品 X | agent-1 | battlecard-x.md | ✅ |
| 调研竞品 Y | agent-2 | battlecard-y.md | ✅ |
| 生成线框图 | agent-3 | wireframe.md | 🟡 超时标 [待确认] |
冲突: 0
```

**实战铁律**（落盘前对照）：

- **独立性是底线**：共享可变状态=不可并行
- **输入/输出明确**：避免重叠覆盖
- **失败隔离**：一个失败不阻塞其他
- **冲突标注**：不静默覆盖

详见 [references/parallel-example.md](references/parallel-example.md)。

### Further Reading

- [Dispatching Parallel Agents (superpowers)](https://github.com/obra/superpowers)
- [Subagent-Driven Development](https://github.com/obra/superpowers)
