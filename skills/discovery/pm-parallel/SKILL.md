---
name: pm-parallel
description: 当 PMSkill 工作面临 ≥2 个独立任务（如多 skill 并行生成、多竞品调研）时，分派并行子 agent 执行——任务分片 + 独立性校验 + 结果合并 + 冲突标 [冲突]。Use when the user asks for parallel agent dispatch or concurrent tasks, mentions 并行、parallel、并发、concurrent、多 agent、dispatch agents、subagent、任务分片、task partition、独立性校验.
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

**自愈机制**：失败回溯（最多 3 轮），超限降级标 `[待确认]` + 终止

### Step 1: 任务识别 + 独立性校验

| 任务 | 输入 | 输出 | 与其他任务共享状态? |
|------|------|------|-------------------|
| 调研竞品 X | PMContext 竞品层 | battlecard-x.md | 无 |
| 调研竞品 Y | PMContext 竞品层 | battlecard-y.md | 无（读同一源不冲突） |

任一任务共享可变状态 → **🔴 STOP** 不可并行，改串行。

### Step 2: 分派子 agent

每子 agent 明确：输入文件 + 输出文件 + skill 调用。

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
| 失败子 agent 阻塞其他 | 一个失败全卡，违背并行初衷 |
| 冲突静默覆盖 | 丢失信息，必须标 `[冲突]` |
| 任务 <2 强并行 | 并行开销 > 收益，串行更优 |
| 审计三元组写空话 | 判定 Failure |

## 产出示例

```markdown
## 并行任务（3 个，独立性 ✅）
| 任务 | 子 agent | 输出 | 状态 |
|------|---------|------|------|
| 调研竞品 X | agent-1 | battlecard-x.md | ✅ |
| 调研竞品 Y | agent-2 | battlecard-y.md | ✅ |
| 生成线框图 | agent-3 | wireframe.md | 🟡 超时标 [待确认] |
冲突: 0
```

### Further Reading

- [Dispatching Parallel Agents (superpowers)](https://github.com/obra/superpowers)
- [Subagent-Driven Development](https://github.com/obra/superpowers)

### 实战提示

- **独立性是底线**：共享可变状态=不可并行
- **输入/输出明确**：避免重叠覆盖
- **失败隔离**：一个失败不阻塞其他
- **冲突标注**：不静默覆盖

详见 [references/parallel-example.md](references/parallel-example.md)。
