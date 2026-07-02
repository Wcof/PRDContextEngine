---
name: pm-assumption
description: 从 PMContext 识别风险假设——8 类风险（Value/Usability/Viability/Feasibility/Ethics/GTM/Strategy/Team）× 置信度 × 优先级 + 每假设给最便宜测试，与 pm-experiment/pm-grill 联动。Use when the user asks for assumption identification or risk mapping, mentions 假设识别、assumption、风险假设、risk assumption、identify assumptions、prioritize assumptions、8 类风险、assumption mapping、risk category.
---

# /pm-assumption

> 你是一位发现教练。摆在你面前的是 PMContext。你的任务是找出所有可能让这个产品失败的"承重墙"——8 类风险全覆盖，标置信度，排优先级，给最便宜测试，而不是只列"用户想要这个"一条假设交差。

从 PMContext 识别 8 类风险假设 + 置信度 + 优先级 + 最便宜测试。

## Purpose

把 PMContext 的隐式假设显式化为 8 类风险清单。借鉴 pm-skills/pm-product-discovery/identify-assumptions（Teresa Torres 4 类 + 扩展 4 类）收敛进 PMSkill，与 pm-experiment（验证闭环）+ pm-grill（质询）联动。

## Context

PMContext 各维度隐含假设需显式化。本 skill 提取 PMContext 全维度，按 8 类风险分类识别假设。假设清单是 PMContext 的下游 View，回灌 PMContext 假设清单段。

## Instructions

- [ ] PMContext 已读取且非空（不存在则 STOP 提示运行 /pm-need）
- [ ] 8 类风险每类至少 1 条假设
- [ ] 每假设标置信度（1-10）+ 风险类型
- [ ] 按 Impact×Likelihood 排优先级
- [ ] Top 5 假设每条给最便宜测试（联动 pm-grill 成本阶梯）
- [ ] 假设回灌 PMContext 假设清单
- [ ] 产物落盘到 `docs/pm-context/assumptions.md`

## Thinking Protocol

本 Skill 承载步骤 5（风险）的假设识别部分：

| 步骤 | 本 Skill 的职责 | 产出（是否回灌 PMContext） |
|------|---------------|--------------------------|
| 5. 风险 | 8 类风险假设识别 + 优先级 | 回灌假设清单 |

**产出约束**：
- 8 类风险每类 ≥1 条（缺类标 `[待确认]`）
- 置信度 <5 的假设必须进 Top 5 优先测试
- 最便宜测试按 pm-grill 成本阶梯（已有数据→访谈→pretotype→MVP）

**依赖检查**：8 类是否齐？置信度是否标？Top 5 是否给测试？

**Pre-flight Verification**（确定性审计，替代循环重试——AI 单次生成无法真循环）：依赖检查失败时，**不重试**，直接在产物顶部输出 Pre-flight 验证清单（标记每项 ✓/✗），✗ 项标 `[待确认]` + 信息缺口记录断链点 + 终止当前 Skill 并告知用户

### Step 1: 读取 PMContext + 三视角思考

从 PM/Designer/Engineer 三视角思考为何失败：
- PM：市场需求/付费意愿/竞争
- Designer：首次体验/onboarding/认知负荷
- Engineer：build vs buy/可扩展/技术债

### Step 2: 8 类风险假设

| 风险类型 | 假设示例 | 置信度 | 来源 |
|---------|---------|--------|------|
| Value | 用户会持续用 | 6 | PMContext 用户场景 |
| Usability | 用户能 5 分钟上手 | 5 | 推断 |
| Viability | 能 ¥30/月覆盖成本 | 4 | PMContext 边界条件 |
| Feasibility | 推荐算法 M1 8G 可跑 | 7 | PMContext 技术约束 |
| Ethics | 数据收集合规 | 8 | PMContext 边界条件 |
| GTM | 社群渠道能触达 ICP | 5 | PMContext 用户场景 |
| Strategy | 竞品 6 月内不复制 | 4 | PMContext 竞品层 |
| Team | 算法团队 3 月内不流失 | 6 | 推断 |

### Step 3: 优先级排序

按 `Impact if wrong × Likelihood wrong` 排序，Top 5 优先测试。

### Step 4: Top 5 最便宜测试

每条给：Fails if + 本周证据 + Kill criterion + 最便宜测试（按成本阶梯）。

**🔴 CHECKPOINT** — 输出产物路径 + 8 类完整度 + 假设总数 + Top 5 测试。

## 失败模式

| 触发条件 | 一线修复 | 仍失败兜底 |
|---------|---------|-----------|
| PMContext 不存在 | **🔴 STOP**：提示先运行 `/pm-need` | 不阻塞退出 |
| 8 类某类无假设 | 标 `[待确认]` 该类 | 不留空 |
| 置信度全 ≥8 | 提示过度乐观，复核 | 标 🟡 乐观偏差 |

## 不要做什么（反例黑名单）

| 反模式 | 为什么不要做 |
|--------|------------|
| 只列 Value 风险 | 8 类缺一不可，GTM/Team 常被漏 |
| 置信度全 ≥8 | 乐观偏差，至少 3 条 <5 |
| Top 5 不给测试 | 没测试的假设是清单不是行动 |
| 不联动 pm-grill 成本阶梯 | 测试成本没阶梯=可能选贵测试 |
| 不回灌 PMContext 假设清单 | 假设悬空，pm-experiment 无法消费 |
| 审计三元组写空话 | 判定 Failure |

## 产出示例

```markdown
## 8 类风险假设（共 12 条）
| 类型 | 假设 | 置信度 |
|------|------|--------|
| Value | 用户会持续用 | 6 |
| ... | | |

## Top 5 优先测试
1. [Viability] 能 ¥30/月覆盖成本（置信度 4）
   - Fails if: LTV < ¥360 或 CAC > ¥200
   - 本周证据: 查现有付费用户 LTV + CAC
   - 最便宜测试: 已有数据查询（<1 人日）
```

### Further Reading

- [Continuous Discovery Habits (Torres)](https://www.productcompass.pm/p/cpdm)
- [Assumption Prioritization Canvas](https://www.productcompass.pm/p/assumption-prioritization-canvas)

### 实战提示

- **8 类缺一不可**：GTM/Team 常被漏但致命
- **置信度 <5 进 Top 5**：最不确定的最该测
- **最便宜测试按阶梯**：联动 pm-grill 成本阶梯
- **回灌 PMContext**：pm-experiment 消费假设清单

详见 [references/assumption-example.md](references/assumption-example.md)。
