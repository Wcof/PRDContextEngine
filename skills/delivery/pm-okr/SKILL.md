---
name: pm-okr
description: 从 PMContext 拆解 OKR——定性 Objective（鼓舞+方向+时间窗）+ 3 个定量 Key Results（可测、60-70% 信心、对齐公司战略）+ 三套候选对比 + KR 与 KPI/NSM 关系澄清，每 KR 附 PMContext 度量追溯。Use when the user asks for OKR or quarterly goals, mentions OKR、目标与关键结果、Objective、Key Results、季度目标、quarterly goals、KR、战略对齐、stretch goals、ambitious goals.
---

# /pm-okr

> 你是一位产品负责人。摆在你面前的是 PMContext 与公司战略。你的任务是把愿景拆成季度可执行的 OKR——一个鼓舞的 Objective + 3 个可测的 Key Results，而不是堆一堆 KPI 当 KR。

从 PMContext 拆解 OKR。Objective（定性鼓舞）+ 3 个 Key Results（定量可测）+ 三套候选对比。

## Purpose

把 PMContext 的价值验证度量与用户场景拆成季度 OKR。pm-skills 的 brainstorm-okrs 收敛进 PMSkill 体系：从 PMContext 度量定义对齐 KR 口径，与 pm-metrics 的 NSM/KPI 关系显式澄清，杜绝"KR 与 KPI 混淆"。

## Context

PMContext 中"价值验证度量"定义了可测指标与阈值（KR 候选来源）；"用户场景"定义了 Objective 的方向（为谁解决什么）；"全局约束"定义了时间窗与资源边界。本 skill 提取这些信息构建 OKR。OKR 是 PMContext 的下游 View，和 PRD/草图平级。

## Instructions

- [ ] PMContext 已读取且非空（不存在则 STOP 提示运行 /pm-need）
- [ ] "价值验证度量"已提取（KR 候选指标来源）
- [ ] "用户场景"已提取（Objective 方向来源）
- [ ] "全局约束"已提取（时间窗/资源边界来源）
- [ ] 公司战略已确认（用户提供或标 `[假设]`）
- [ ] 三套 OKR 候选已生成，每套含 1 Objective + 3 KR
- [ ] 每个 KR 满足四性：可测/有阈值/60-70% 信心/对齐公司战略
- [ ] KR 与 KPI/NSM 关系已显式澄清（借鉴 Wodtke 框架）
- [ ] 每套 OKR 标注追溯到的 PMContext 度量项
- [ ] 产物落盘到 `docs/pm-context/okr.md`

## Thinking Protocol

本 Skill 承载 PM Thinking Loop 的步骤 4（权衡）+ 步骤 6（交付）的 OKR 拆解部分：

| 步骤 | 本 Skill 的职责 | 产出（是否回灌 PMContext） |
|------|---------------|--------------------------|
| 4. 权衡 | 三套 OKR 候选对比 + 信心度评估 | 回灌选定 OKR 到决策日志 |
| 6. 交付 | 最终 OKR 文档 | 不回灌（产出 View） |

执行时必须依次完成上述步骤，不可跳步。步骤产出写入 `.loop/okr-step4.md`、`.loop/okr-step6.md`。

**产出约束**：
- Objective 必须定性、鼓舞、有时间窗（如"Q3 让新用户在 20 分钟内体验到核心价值"），禁写成指标
- 每个 KR 必须可测（有数字 + 阈值），禁写"提升用户体验"等不可测表述
- KR 信心度必须 60-70%（stretch 但非不可能），>80% 太保守、<50% 太冒险
- KR 与 KPI/NSM 关系必须显式标注（KR 可引用 KPI/NSM 作为度量）

**依赖检查**：Objective 是否定性鼓舞？KR 是否可测？信心度是否在 60-70%？是否对齐公司战略？

**Pre-flight Verification**（确定性审计，替代循环重试——AI 单次生成无法真循环）：依赖检查失败时，**不重试**，直接在产物顶部输出 Pre-flight 验证清单（标记每项 ✓/✗），✗ 项标 `[待确认]` + 信息缺口记录断链点 + 终止当前 Skill 并告知用户

### Step 1: 读取 PMContext 提取 OKR 素材

读取 `docs/pm-context/pm-context.md`，提取：
- "价值验证度量" → KR 候选指标 + 阈值
- "用户场景" → Objective 方向（为谁解决什么）
- "全局约束" → 时间窗（季度）+ 资源边界

若 PMContext 不存在 → **🔴 STOP**：提示先运行 `/pm-need`。

### Step 2: 确认公司战略对齐

公司战略来源：
- 用户提供 → 直接采用
- 未提供 → 标 `[假设]` 从 PMContext 推断战略方向，提示 PM 确认

### Step 3: 生成三套 OKR 候选

每套含 1 Objective + 3 KR：

```
Objective: <定性鼓舞+方向+时间窗>
Key Results:
- KR1: <可测指标> 从 <基线> 到 <目标>（信心度 X%）
- KR2: <可测指标> 从 <基线> 到 <目标>（信心度 X%）
- KR3: <可测指标> 从 <基线> 到 <目标>（信心度 X%）
```

三套候选应覆盖不同战略侧重（如：增长导向 vs 留存导向 vs 体验导向），禁三套雷同。

### Step 4: KR 与 KPI/NSM 关系澄清

借鉴 Wodtke 框架显式标注（避免 KR/KPI/NSM 混淆）：

| 概念 | 定义 | 与本 OKR 的关系 |
|------|------|----------------|
| **Key Results** | 季度定量的进展度量 | 本 OKR 的 3 个 KR |
| **KPI** | 长期跟踪的关键指标 | KR1 引用 pm-metrics 的 NSM 作为度量 |
| **NSM（北极星）** | 单一客户中心 KPI | KR2 是 NSM 的 input metric |

### Step 5: 三套对比与选定

| 维度 | 套 A（增长导向） | 套 B（留存导向） | 套 C（体验导向） |
|------|----------------|----------------|----------------|
| 战略对齐 | | | |
| 信心度均值 | | | |
| 可测性 | | | |
| 与 pm-metrics NSM 一致性 | | | |

选定 1 套，标注放弃理由。

### Step 6: 写入产物

写入 `docs/pm-context/okr.md`，含三套候选 + 对比表 + 选定 OKR + KR/KPI/NSM 关系表 + 追溯列。

**🔴 CHECKPOINT** — 输出产物路径 + 选定 OKR + 3 个 KR + 信心度均值。等待 PM 确认或自动进入下一步（`--auto` 模式）。

## 流程链落盘

步骤 4、6 产出完成后，写入中间工件：
- `docs/pm-context/.loop/okr-step4.md`（三套对比+选定 + 审计三元组）
- `docs/pm-context/.loop/okr-step6.md`（最终 OKR + 审计三元组）

## 关联增强

在追溯列标注每 KR 追溯到的 PMContext 度量项。OKR 与 pm-metrics 交叉验证（KR 应引用 NSM 或其 input metric，不一致标 `[冲突]`）。

## 失败模式

| 触发条件 | 一线修复 | 仍失败兜底 |
|---------|---------|-----------|
| `docs/pm-context/pm-context.md` 不存在 | **🔴 STOP**：输出"未找到 PMContext，先运行 `/pm-need <需求>`" | 不阻塞，提示后退出 |
| PMContext "价值验证度量"为空 | **🔴 STOP**：输出"无可测指标，先运行 `/pm-refine` 补度量" | 不臆造 KR |
| 公司战略未提供 | 标 `[假设]` 从 PMContext 推断，提示 PM 确认 | 不阻塞 |
| KR 信心度 > 80% | 提高目标阈值（stretch 不足） | 标 🟡 太保守 |
| KR 信心度 < 50% | 降低目标阈值或拆分 KR | 标 🟡 太冒险 |
| 三套候选雷同 | 重新发散不同战略侧重 | 仍雷同则标 `[待确认]` 需 PM 给战略方向 |
| OKR 与 pm-metrics NSM 冲突 | 标 `[冲突]` 让 PM 裁决 | 不静默合并 |

## 不要做什么（反例黑名单）

| 反模式 | 为什么不要做 |
|--------|------------|
| Objective 写成指标（"提升 DAU 20%"） | Objective 是定性方向，指标是 KR 的事 |
| KR 不可测（"提升用户体验"） | 不可测的 KR 无法跟踪进度，等于没设目标 |
| KR 信心度 100% | 100% 信心=没 stretch，OKR 要 60-70% 才有挑战 |
| KR 堆 5+ 个 | KR 3 个足够，5+ 个分散焦点 |
| 三套候选雷同 | 候选应覆盖不同战略侧重，雷同等于没选择 |
| 混淆 KR 与 KPI | KR 是季度进展度量，KPI 是长期跟踪指标，关系要显式标注 |
| 不对齐公司战略 | 团队 OKR 必须 ladder up 到公司目标，否则各自为战 |
| 审计三元组转换操作写"基于上述依据产出" | 空话，未阐明具体推导逻辑，判定为 Failure |

## 产出示例 · 实战提示

会员产品 OKR 候选片段：

```markdown
## 套 A（增长导向）
Objective: Q3 让会员体系成为高频创作者的首选
Key Results:
- KR1: 月付会员数从 5K 到 8K（信心度 70%）← PMContext 价值验证度量"月付会员数"
- KR2: D30 留存从 22% 到 28%（信心度 65%）← PMContext 价值验证度量"D30留存"
- KR3: 续费率从 68% 到 75%（信心度 60%）← PMContext 价值验证度量"续费率"

## KR/KPI/NSM 关系
- KR2 引用 pm-metrics 的 NSM（"会员活跃度"）的 input metric"D30留存"
- KR1/KR3 是 KPI 但非 NSM

## 选定：套 A
放弃套 B（留存导向，与公司增长战略不一致）、套 C（体验导向，KR 可测性弱）。
```

详见 [references/okr-example.md](references/okr-example.md)（完整三套 OKR 候选对比示例含 KR/KPI/NSM 关系矩阵）。

**实战铁律**（落盘前对照）：

- **Objective 定性 KR 定量**：Objective 写"让用户 X"，KR 写"从 X 到 Y"
- **信心度 60-70% 是甜点**：太低冒险太高没挑战
- **KR ≤ 3 个**：多了分散焦点，少了不够全面
- **对齐 pm-metrics NSM**：KR 应引用 NSM 或其 input metric，不一致标冲突
- **三套候选要差异化**：增长/留存/体验三种导向，不要三套雷同

### Further Reading

- [Radical Focus - Christina Wodtke](https://www.productcompass.pm/p/radical-focus)
- [OKR vs KPI vs NSM 关系](https://www.productcompass.pm/p/okr-kpi-nsm)
- [Stretch Goals and OKR Confidence](https://www.productcompass.pm/p/stretch-goals)
