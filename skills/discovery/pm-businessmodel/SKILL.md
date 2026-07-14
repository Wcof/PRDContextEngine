---
name: pm-businessmodel
description: Use when the user asks for business model or revenue model, mentions 商业模式、business model、BMC、商业模式画布、business model canvas、收入模型、revenue model、如何赚钱、monetization model、key partners、价值主张、客户细分.
metadata:
  internal: true
---

# /pm-businessmodel

> 你是一位商业模式策略师。摆在你面前的是 PMContext。你的任务是画出 9 模块 BMC——谁 partnered、做什么 activity、用什么 resource、给谁什么价值、怎么触达、怎么收费、成本在哪，而不是只写"卖会员赚钱"。

从 PMContext 生成商业模式画布（BMC）+ 业务游戏分类 + 收入/成本结构。

## Purpose

把 PMContext 的用户场景与价值度量结构化为 BMC 9 模块。借鉴 pm-skills/pm-product-strategy/business-model + Lean Canvas + Startup Canvas 收敛进 PMSkill 体系，与 pm-strategy 互补（pm-strategy 做战略定位，本 skill 做商业模式建模）。

## Context

PMContext"用户场景"定义客户细分与价值主张；"价值验证度量"定义收入流依据；"边界条件"定义成本结构与关键资源约束；"现状平替"定义竞争替代。BMC 是 PMContext 的下游 View，与 pm-strategy 平级。

## Instructions

- [ ] PMContext 已读取且非空（不存在则 STOP 提示运行 /pm-need）
- [ ] "用户场景"已提取（客户细分+价值主张来源）
- [ ] "价值验证度量"已提取（收入流依据）
- [ ] "边界条件"已提取（成本+资源约束来源）
- [ ] 业务游戏已分类（注意力/交易/生产力）
- [ ] BMC 9 模块已填写且每模块追溯 PMContext
- [ ] 收入流 ≥2 条 + 成本结构（固定/变动）
- [ ] 关键假设标注（每模块 `[假设]`/`[待确认]`）
- [ ] 产物落盘到 `docs/pm-context/business-model.md`

## Thinking Protocol

本 Skill 承载 PM Thinking Loop 步骤 2（建模）+ 步骤 4（权衡）的商业模式部分：

| 步骤 | 本 Skill 的职责 | 产出（是否回灌 PMContext） |
|------|---------------|--------------------------|
| 2. 建模 | BMC 9 模块建模 + 业务游戏分类 | 回灌关键假设到假设清单 |
| 4. 权衡 | 收入流优先级 + 成本权衡 | 不回灌（产出 View） |

执行时依次完成，步骤产出写入 `process/02-bm-model.md`、`process/04-bm-tradeoff.md`。

**产出约束**：
- BMC 9 模块缺一不可，缺模块标 `[待确认]` 不留空
- 业务游戏分类必须选 1 个（注意力/交易/生产力），禁"混合"
- 收入流 ≥2 条（单收入流=脆弱），每条标注 `[假设]`/事实
- 关键假设必须回灌 PMContext 假设清单

**依赖检查**：9 模块是否齐？业务游戏是否选定？收入流是否 ≥2？假设是否标注？

**Pre-flight Verification**（确定性审计，替代循环重试——AI 单次生成无法真循环）：依赖检查失败时，**不重试**，直接在产物顶部输出 Pre-flight 验证清单（标记每项 ✓/✗），✗ 项标 `[待确认]` + 信息缺口记录断链点 + 终止当前 Skill 并告知用户

### Step 1: 读取 PMContext + 业务游戏分类

读取 `<产物目录>/pm-context.md`（先读 `## PMSkill` 块取 `产物目录`，块不存在回退默认 `docs/pm-context/`）。按 PMContext 用户场景分类：

| 游戏类型 | 判定 | NSM 方向 |
|---------|------|---------|
| 注意力 | 用户花时间消费内容 | 时长/频次 |
| 交易 | 用户完成交易 | 交易数/GMV |
| 生产力 | 用户高效完成任务 | 任务完成率/效率提升 |

### Step 2: BMC 9 模块

```
左（创造价值）: Key Partners / Key Activities / Key Resources
中: Value Propositions
右（传递价值）: Customer Relationships / Channels / Customer Segments
底: Cost Structure / Revenue Streams
```

每模块填写并标注追溯。

### Step 3: 收入流与成本结构

| 收入流 | 类型 | 定价 | `[假设]`/事实 | 追溯 |
|--------|------|------|-------------|------|
| 会员订阅 | 经常性 | ¥30/月 | 事实 | PMContext 价值度量 |
| 增值服务 | 一次性 | ¥99/项 | `[假设]` | 推断 |

成本结构：固定（人力/服务器）+ 变动（获客/支付手续费）。

### Step 3.5: 货币化策略成熟度（借鉴 pm-product-strategy/monetization-strategy）

> 收入流 ≥2 条是底线但不够——还需评估当前货币化策略的成熟度，给升级路径。

**货币化成熟度阶梯**：

| 阶段 | 特征 | 收入流典型形态 | PMSkill 层判定 |
|------|------|--------------|---------------|
| L1 单一收费 | 单一付费模式，无分层 | 仅订阅/仅买断 | 脆弱，标 🟡 需多元化 |
| L2 分层收费 | 按用量/功能/服务分层 | 基础免费+Pro 订阅+企业版 | 健康，建议加固 |
| L3 生态收费 | 平台侧+需求侧双边变现 | 订阅+交易抽成+数据增值 | 成熟，建议监控 |
| L4 网络效应 | 用户量→价值→变现正循环 | 订阅+广告+增值+API 开放 | 理想，但需维护壁垒 |

**加速策略**（当前层到下一层的最短路径）：

| 当前层 | 下一层 | 加速策略 | 验证 |
|--------|--------|---------|------|
| L1 单一 | L2 分层 | 加免费层引流+Pro 层变现 | 3 月看免费→Pro 转化率 |
| L2 分层 | L3 生态 | 引入交易抽成或 marketplace | 6 月看 GMV 分成收入 |
| L3 生态 | L4 网络 | 开放 API/平台化 | 12 月看开发者生态规模 |

**货币化纪律**：
- 收入流 ≥2 条是底线，L1 标 🟡 提示 PM 分层
- 加速策略必须验证（无验证路径的加速=猜测）
- 货币化成熟度应纳入 BMC 假设中，与 pm-grill 联动（假设"用户愿付分层价"可被攻击）

### Step 3.75: 竞争护城河 + 取舍声明（借鉴 pm-product-strategy/startup-canvas "Can't/Won't test + Trade-offs"）

> BMC 画出"做什么"，但没画"凭什么别人做不了"和"我们选择不做什么"。竞争护城河回答前者，取舍声明回答后者——两者合起来才是完整的商业模式风险图。

**Can't/Won't 测试**（什么阻止竞争对手复制你的模式）：
- "竞争对手为什么会难复制？"——不是"我们做得好"而是"他们复制会付出什么代价"
- 类型：技术秘密/网络效应/规模经济/品牌信任/法规壁垒/生态锁定/数据飞轮
- 若复制成本低→标 🟡 商业模式脆弱，需加固护城河

| 护城河类型 | 本产品依赖度 | 可持续性 | 风险 |
|-----------|------------|---------|------|
| <网络效应/品牌/…> | <高/中/低> | <长期/中期/短期> | <风险描述> |

**取舍声明**（我们选择不做什么——选择不做的事定义战略）：
- "我们的客户细分是 X，所以我们选择不做 Y 那群用户"
- "我们选自助服务，所以不做白手套实施"
- "我们选年付，所以不强推月付"

| 选择 | 放弃 | 理由 | 风险（放弃的代价） |
|------|------|------|------------------|
| 自助服务 | 白手套实施 | 规模经济，不适合高接触 | 可能失去不愿自服务的客户 |

**纪律**：
- 护城河≥1 种类型，无护城河标 🟡 提示 PM 建壁垒
- 取舍≥2 条（少于 2 条说明战略没选择），缺取舍标 🟡 战略模糊
- 护城河与取舍回灌 PMContext 假设清单（护城河不是事实是假设，需验证）

### Step 4: 关键假设回灌

每模块 `[假设]` 项回灌 PMContext 假设清单，置信度标注。

**🔴 CHECKPOINT** — 输出产物路径 + 业务游戏 + 9 模块完整度 + 收入流数 + `[假设]` 项数。等待 PM 确认或自动进入下一步（`--auto` 模式）。

## 失败模式

| 触发条件 | 一线修复 | 仍失败兜底 |
|---------|---------|-----------|
| PMContext 不存在 | **🔴 STOP**：提示先运行 `/pm-need` | 不阻塞，提示后退出 |
| 用户场景为空 | **🔴 STOP**：提示先 `/pm-collect` 补用户研究 | 不臆造客户细分 |
| 业务游戏无法判定 | 标 `[待确认]` 从边界条件推断 | 标 `[假设]` 默认生产力 |
| 收入流仅 1 条 | 提示补 ≥2 条（单收入流脆弱） | 标 🟡 单收入流风险 |
| BMC 模块缺失 | 标 `[待确认]` 不留空 | 提示补材料 |

## 不要做什么（反例黑名单）

| 反模式 | 为什么不要做 |
|--------|------------|
| BMC 模块留空 | 9 模块缺一不可，缺则标 `[待确认]` 不留空 |
| 业务游戏选"混合" | 必须选 1 个主导游戏，混合=没选 |
| 单收入流不警示 | 单收入流=脆弱，必须提示补 ≥2 条 |
| 收入流不标假设 | 没假设标注的收入流是许愿不是建模 |
| 不追溯 PMContext | BMC 悬空，无法验证是否对齐用户研究 |
| 审计三元组写"基于上述依据产出" | 空话，判定 Failure |

## 产出示例 · 实战提示

```markdown
## 业务游戏：生产力（创作者高效产出内容）

## BMC
| 模块 | 内容 | 追溯 |
|------|------|------|
| Key Partners | 内容平台分发/支付通道 | PMContext 边界条件 |
| Key Activities | 内容推荐算法/会员服务 | 推断 |
| Key Resources | 算法团队/内容库 | PMContext 边界条件 |
| Value Propositions | 让创作者稳定高效产出 | PMContext 用户场景 |
| Customer Relationships | 自助+社区 | 推断 |
| Channels | 应用商店/社群 | PMContext 用户场景 |
| Customer Segments | 高频创作者/小工作室 | PMContext 用户场景 |
| Cost Structure | 固定：算法团队¥X/月；变动：获客¥Y/人 | PMContext 边界条件 |
| Revenue Streams | 会员订阅¥30/月（事实）；增值服务¥99/项（[假设]） | PMContext 价值度量 |

## 关键假设回灌
- 增值服务付费意愿 [假设 6/10] → 回灌 PMContext 假设清单
```

**实战铁律**（落盘前对照）：

- **9 模块缺一不可**：缺则标 `[待确认]` 不留空
- **业务游戏必选 1**：注意力/交易/生产力，禁混合
- **收入流 ≥2**：单收入流脆弱
- **假设回灌 PMContext**：BMC 假设进假设清单联动 pm-grill

详见 [references/bm-example.md](references/bm-example.md)。

### Further Reading

- [Business Model Canvas (Osterwalder)](https://www.productcompass.pm/p/business-model-canvas)
- [The Three Business Games](https://www.productcompass.pm/p/business-games)
