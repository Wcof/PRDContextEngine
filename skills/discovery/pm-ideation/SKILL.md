---
name: pm-ideation
description: 从 PMContext 按新旧场景 brainstorm 假设与实验方案——现有产品新方案（optimize）vs 新产品新方案（explore）+ 每方案给最便宜验证 + 联动 pm-assumption/pm-experiment。Use when the user asks for brainstorm or ideation, mentions 头脑风暴、brainstorm、ideation、创意、实验方案、experiment ideas、新旧场景、optimize vs explore、方案发散.
---

# /pm-ideation

> 你是一位发现教练。摆在你面前的是 PMContext。你的任务发散 ≥5 个方案——区分"优化现有"与"探索新场景"，每方案给最便宜验证，而不是只给 1 个"做个推荐功能"交差。

从 PMContext brainstorm 方案——新旧场景分类 + 每方案最便宜验证。

## Purpose

把 PMContext 发散为可验证的方案集。借鉴 pm-skills/pm-product-discovery/brainstorm-experiments-existing + brainstorm-experiments-new 收敛进 PMSkill，与 pm-assumption（风险）+ pm-experiment（验证）联动。

## Context

PMContext"用户场景"定义方案方向；"现状平替"定义优化空间；"边界条件"定义方案约束。方案集是 PMContext 下游 View，回灌 PMContext 方案候选段。

## Instructions

- [ ] PMContext 已读取（不存在则 STOP）
- [ ] 区分 optimize（现有产品新方案）vs explore（新场景方案）
- [ ] ≥5 个方案（optimize ≥2 + explore ≥2）
- [ ] 每方案给假设 + 最便宜验证（pm-grill 成本阶梯）
- [ ] 方案间不重复（去重）
- [ ] 回灌 PMContext 方案候选段
- [ ] 产物落盘 `docs/pm-context/ideation.md`

## Thinking Protocol

本 Skill 承载步骤 3（方案）的发散部分：

| 步骤 | 本 Skill 的职责 | 产出（是否回灌 PMContext） |
|------|---------------|--------------------------|
| 3. 方案 | ≥5 方案发散 + 新旧分类 + 验证 | 回灌方案候选 |

**产出约束**：
- ≥5 方案（<5 发散不足），optimize/explore 各 ≥2
- 每方案必须给假设 + 最便宜验证（无验证=空想）
- 方案间去重（相似方案合并）

**依赖检查**：方案是否 ≥5？optimize/explore 各 ≥2？每方案有验证？去重？

**自愈机制**：失败回溯（最多 3 轮），超限降级标 `[待确认]` + 终止

### Step 1: 读取 PMContext + 区分新旧场景

- optimize：现有产品改进（PMContext 用户场景已覆盖）
- explore：新场景拓展（PMContext 用户场景未覆盖的相邻 JTBD）

### Step 2: 发散 ≥5 方案

| # | 类型 | 方案 | 假设 | 最便宜验证 | 追溯 |
|---|------|------|------|-----------|------|
| 1 | optimize | 智能排期优化 | 用户会用 | 5 用户访谈 | PMContext 用户场景 |
| 2 | optimize | 断更预警增强 | 预警降断更 | 已有数据分析 | PMContext 现状平替 |
| 3 | explore | 团队协作版 | 小团队有需求 | landing page waitlist | PMContext 边界条件 |
| 4 | explore | 企业版 | 企业有采购需求 | 5 企业访谈 | 推断 |
| 5 | explore | API 开放 | 开发者会集成 | 社区调研 | 推断 |

### Step 2.5: 方案对比矩阵（借鉴 superpowers/brainstorming "2-3 approaches with trade-offs"）

> 发散不对比=把选择负担甩给 PM。必须给对比矩阵 + 推荐 + 理由，让 PM 在"有依据的选择"而非"罗列"上决策。

| 方案 | 成本 | 预期收益 | 风险 | 验证周期 | 推荐? |
|------|------|---------|------|---------|------|
| 智能排期优化 | 中 | 中 | 低（改现有） | 1 周 | ⭐ 推荐先做（低成本快验证） |
| 断更预警增强 | 低 | 中 | 低 | 3 天 | ⭐ 推荐同做（成本最低） |
| 团队协作版 | 高 | 高 | 中（新场景） | 2 周 | 备选（需 waitlist 验证后） |
| 企业版 | 高 | 高 | 高（销售周期长） | 4 周 | 暂缓（验证成本过高） |
| API 开放 | 中 | 中 | 高（生态依赖） | 3 周 | 暂缓（需开发者社区基础） |

**对比纪律**（借鉴 brainstorming trade-offs）：
- 每方案必须标成本/收益/风险/周期四维，缺一扣 🟡
- 必须给 ≥1 个推荐 + 理由（"推荐先做 X 因成本最低快验证"），禁"根据情况选择"空话
- 推荐理由必须可追溯到 PMContext（如"成本低因复用现有排期模块"）

<HARD-GATE>
发散 + 对比矩阵完成并经 PM 确认推荐方案前，**不得进入 pm-experiment 验证或 pm-prd 实现**。"简单方案不需要对比"是反模式——简单方案正是未审视假设浪费工时最多的地方（借鉴 brainstorming anti-pattern）。
</HARD-GATE>

### Step 3: 去重 + 回灌

相似方案合并，方案候选回灌 PMContext。

**🔴 CHECKPOINT** — 输出产物路径 + 方案数 + optimize/explore 分布。

## 失败模式

| 触发条件 | 一线修复 | 仍失败兜底 |
|---------|---------|-----------|
| PMContext 不存在 | **🔴 STOP**：提示先运行 `/pm-need` | 不阻塞退出 |
| 方案 <5 | 继续发散 | 标 `[待确认]` 发散不足 |
| 全 optimize 无 explore | 提示补 explore（新场景） | 标 🟡 缺探索 |
| 方案无验证 | 每方案补最便宜验证 | 标 `[待确认]` |

## 不要做什么（反例黑名单）

| 反模式 | 为什么不要做 |
|--------|------------|
| 只给 1 个方案 | 单方案=没选择，发散 ≥5 |
| 全 optimize 无 explore | 缺探索=只优化现有不找新增长 |
| 方案无验证 | 没验证的方案是空想 |
| 不去重 | 相似方案堆叠=假发散 |
| 发散不对比（缺 Step 2.5 矩阵） | 罗列甩选择负担给 PM，必须给对比+推荐+理由 |
| 推荐理由写"根据情况选择" | 空话，必须可追溯 PMContext（如"成本低因复用现有模块"） |
| 跳过对比直接进 pm-experiment（违反 HARD-GATE） | 未审视假设的方案验证=浪费工时，简单方案尤甚 |
| 审计三元组写空话 | 判定 Failure |

## 产出示例

```markdown
## 方案集（5 个）
| # | 类型 | 方案 | 验证 |
|---|------|------|------|
| 1 | optimize | 智能排期优化 | 5 用户访谈 |
| 2 | optimize | 断更预警增强 | 已有数据分析 |
| 3 | explore | 团队协作版 | landing page |
| 4 | explore | 企业版 | 5 企业访谈 |
| 5 | explore | API 开放 | 社区调研 |
```

### Further Reading

- [Continuous Discovery Habits (Torres)](https://www.productcompass.pm/p/cpdm)
- [Brainstorming Experiments](https://www.productcompass.pm/p/brainstorm-experiments)

### 实战提示

- **≥5 方案**：单方案=没选择
- **optimize/explore 各 ≥2**：优化+探索双轨
- **每方案必验证**：无验证=空想
- **联动 pm-assumption/pm-experiment**：假设→验证闭环

详见 [references/ideation-example.md](references/ideation-example.md)。
