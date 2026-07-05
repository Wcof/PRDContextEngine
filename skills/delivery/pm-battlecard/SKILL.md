---
name: pm-battlecard
description: 从 PMContext 与竞品调研生成销售就绪竞品作战卡——公司概览+快速对比表+我方优势+对方优势+异议处理+地雷问题+赢/输模式，每对比项附 PMContext 追溯。Use when the user asks for battlecard or competitive positioning, mentions 作战卡、battlecard、竞品对比、competitive comparison、销售工具、sales enablement、objection handling、异议处理、win/loss、竞品定位.
---

# /pm-battlecard

> 你是一位竞争情报专家。摆在你面前的是 PMContext 与一个具体竞品。你的任务是给销售一份能在通话中秒查的作战卡——我们在哪赢、他们在哪赢、客户说"他们更便宜"怎么回，而不是写一份 50 页竞品报告没人看。

从 PMContext 与竞品调研生成销售就绪竞品作战卡。

## Purpose

把竞品分析浓缩成销售通话可用的作战卡。pm-skills 的 competitive-battlecard 收敛进 PMSkill 体系：从 PMContext 竞品/市场与用户场景推导差异化定位，每对比项追溯 PMContext。

## Context

PMContext"竞品/市场"定义竞品三层（直接/间接/替代）与差异化机会；"用户场景"定义我方优势的客户视角；"价值验证度量"定义可量化的赢点。本 skill 提取这些信息构建作战卡。作战卡是 PMContext 的下游 View，与 pm-market（市场分析）平级。

## Instructions

- [ ] PMContext 已读取且非空（不存在则 STOP 提示运行 /pm-need）
- [ ] "竞品/市场"已提取（竞品定位与差异化来源）
- [ ] "用户场景"已提取（我方优势客户视角来源）
- [ ] "价值验证度量"已提取（可量化赢点来源）
- [ ] 目标竞品已确认（用户提供或从 PMContext 竞品层选 Top 1）
- [ ] 竞品现状已调研（web search：产品/定价/定位/近期变化/评价）
- [ ] 公司概览已输出
- [ ] 快速对比表已完成（≥5 能力维度）
- [ ] 我方优势 ≥3 条（附证明点）
- [ ] 对方优势 ≥2 条（附反制定位）
- [ ] 异议处理表已完成（≥3 常见异议+回应）
- [ ] 地雷问题 ≥2 个（凸显竞品弱点的问题）
- [ ] 赢/输模式已输出
- [ ] 每对比项标注追溯到的 PMContext 项
- [ ] 产物落盘到 `docs/pm-context/battlecard-<competitor>.md`

## Thinking Protocol

本 Skill 承载 PM Thinking Loop 的步骤 2（建模）+ 步骤 6（交付）的作战卡构建部分：

| 步骤 | 本 Skill 的职责 | 产出（是否回灌 PMContext） |
|------|---------------|--------------------------|
| 2. 建模 | 竞品能力建模 + 差异化定位 | 不回灌（产出 View） |
| 6. 交付 | 销售就绪作战卡 | 不回灌（产出 View） |

执行时必须依次完成上述步骤，不可跳步。步骤产出写入 `.loop/battlecard-step2.md`、`.loop/battlecard-step6.md`。

**产出约束**：
- 对比表必须 ≥5 能力维度，每维度标"Us/Them/Tie"胜负
- 我方优势必须附证明点（客户证言/数据/具体能力），禁空话
- 对方优势必须附反制定位（如何 mitigate），禁只列弱点
- 异议处理必须给具体回应话术，禁"强调我们的价值"等空话
- 地雷问题必须能凸显竞品弱点，禁泛泛而问

**依赖检查**：对比维度是否 ≥5？优势是否附证明？异议是否给话术？地雷是否凸显弱点？

**Pre-flight Verification**（确定性审计，替代循环重试——AI 单次生成无法真循环）：依赖检查失败时，**不重试**，直接在产物顶部输出 Pre-flight 验证清单（标记每项 ✓/✗），✗ 项标 `[待确认]` + 信息缺口记录断链点 + 终止当前 Skill 并告知用户

### Step 1: 读取 PMContext + 确认目标竞品

读取 `<产物目录>/pm-context.md`（先读 `## PMSkill` 块取 `产物目录`，块不存在回退默认 `docs/pm-context/`），从"竞品/市场"层选目标竞品（或用户指定）。

若 PMContext 不存在 → **🔴 STOP**：提示先运行 `/pm-need`。

### Step 2: 竞品调研（web search）

调研：产品/功能、定价、定位、近期变化、客户评价（G2/Capterra/Reddit）。

### Step 3: 公司概览

```
成立时间/HQ/融资/收入（如公开）
目标市场与 ICP
一句话定位
```

### Step 4: 快速对比表

| 能力 | 我方 | 对方 | 胜方 |
|------|------|------|------|
| <维度1 from PMContext 用户场景> | <我方做法> | <对方做法> | Us/Them/Tie |
| ...（≥5 维度） | | | |

### Step 5: 我方优势（≥3，附证明）

1. <优势1>: <证明点/客户证言/数据> ← PMContext 用户场景
2. ...

### Step 6: 对方优势（≥2，附反制）

1. <对方优势1>: <我方反制定位>
2. ...

### Step 7: 异议处理表

| 客户说 | 回应话术 |
|--------|---------|
| "他们更便宜" | "<总拥有成本/ROI/隐性成本框架>" |
| "他们有 X 功能" | "<我方替代方案+为何对客户更好>" |
| ...（≥3 异议） | |

### Step 8: 地雷问题（≥2）

凸显竞品弱点的问题：
- "<我方强项>对你们团队多重要？"
- "<对方缺的能力>你们评估过吗？"

### Step 9: 赢/输模式

- 我方赢当：<模式>
- 我方输当：<模式>
- 竞争deal关键差异化：<什么倾斜天平>

### Step 10: 写入产物

写入 `docs/pm-context/battlecard-<competitor>.md`，保持可扫读（表格/粗体/短 bullet）。

**🔴 CHECKPOINT** — 输出产物路径 + 对比维度数 + 我方优势数 + 异议处理数。等待 PM 确认或自动进入下一步（`--auto` 模式）。

## 流程链落盘

步骤 2、6 产出完成后，写入中间工件：
- `docs/pm-context/.loop/battlecard-step2.md`（竞品建模+对比 + 审计三元组）
- `docs/pm-context/.loop/battlecard-step6.md`（作战卡 + 审计三元组）

## 关联增强

在追溯列标注每对比项追溯到的 PMContext 项。作战卡与 pm-market（竞品三层分析）交叉验证（作战卡聚焦单一竞品，pm-market 聚焦全局）。

## 失败模式

| 触发条件 | 一线修复 | 仍失败兜底 |
|---------|---------|-----------|
| `docs/pm-context/pm-context.md` 不存在 | **🔴 STOP**：输出"未找到 PMContext，先运行 `/pm-need <需求>`" | 不阻塞，提示后退出 |
| PMContext "竞品/市场"为空 | **🔴 STOP**：输出"无竞品分析，先运行 `/pm-market`" | 不臆造竞品 |
| 竞品调研无数据（web search 失败） | 标 `[待确认]` 竞品现状，提示 PM 提供资料 | 不臆造竞品信息 |
| 对比维度 < 5 | 从 PMContext 用户场景扩展维度 | 仍不足则标 `[待确认]` |
| 我方优势无证明点 | 提示补客户证言/数据 | 标 `[假设]` 优势 |
| 异议处理给空话 | 重写为具体话术 | 标 `[待确认]` 需销售反馈实际异议 |

## 不要做什么（反例黑名单）

| 反模式 | 为什么不要做 |
|--------|------------|
| 写 50 页竞品报告 | 销售通话中没人看，作战卡要可秒查 |
| 对比维度 < 5 | 维度太少无法全面对比，漏关键差异 |
| 我方优势不附证明 | 空话优势销售不敢用，要客户证言/数据 |
| 对方优势不附反制 | 只列对方弱点不教如何反制，销售遇到仍慌 |
| 异议处理给"强调价值"空话 | 销售要具体话术，不是策略口号 |
| 地雷问题泛泛而问 | 地雷要能凸显竞品弱点，"你们怎么看 X"是废话 |
| 不追溯 PMContext | 对比项悬空，无法验证差异化定位是否对齐 |
| 审计三元组转换操作写"基于上述依据产出" | 空话，判定为 Failure |

## 产出示例 · 实战提示

```markdown
## 竞品 X 公司概览
成立 2020/HQ 北京/B 轮/ICP: 中小企业

## 快速对比
| 能力 | 我方 | 对方 | 胜方 |
|------|------|------|------|
| 协作 | 实时多人 | 仅评论 | Us |
| 定价 | 按座位 | 按功能模块 | Them（小团队便宜） |
| ... | | | |

## 我方优势
1. 实时协作: 客户 A 证言"节省 40% 评审时间" ← PMContext 用户场景"多人协作"
2. ...

## 异议处理
| 客户说 | 回应 |
|--------|------|
| "他们更便宜" | "小团队他们便宜，但 >10 人按功能模块算总成本高 2 倍，我们按座位更划算" |
```

详见 [references/battlecard-example.md](references/battlecard-example.md)（完整作战卡示例含异议话术与赢/输模式）。

**实战铁律**（落盘前对照）：

- **可扫读第一**：销售通话中秒查，表格/粗体/短 bullet
- **优势附证明**：空话优势销售不敢用，要客户证言/数据
- **异议给话术**：具体回应不是策略口号
- **地雷凸显弱点**：问能逼出竞品短板的问题
- **追溯 PMContext**：差异化定位要有 PMContext 依据

### Further Reading

- [Competitive Battlecard Template](https://www.productcompass.pm/p/battlecard)
- [Win/Loss Analysis](https://www.productcompass.pm/p/win-loss-analysis)
- [Sales Enablement Guide](https://www.productcompass.pm/p/sales-enablement)
