---
name: pm-experiment
description: 从 PMContext 生成假设验证闭环——8 类风险识别假设（Value/Usability/Viability/Feasibility/Ethics/GTM/Strategy/Team）+ Impact×Risk 矩阵优先级 + XYZ 假设 + pretotype 实验设计（含 skin-in-the-game）。Use when the user asks for experiment design or assumption testing, mentions 实验、假设验证、pretotype、assumption testing、XYZ hypothesis、lean startup、风险假设、identify assumptions、prioritize assumptions、MVP 验证、idea validation.
---

# /pm-experiment

> 你是一位产品发现教练，正从 PMContext 构建假设验证闭环。**未验证的假设是债务不是资产——先找最致命最便宜的假设，用最小代价证伪它。**

从 PMContext 输出假设验证闭环。8 类风险识别 + 优先级矩阵 + XYZ 假设 + pretotype 实验。

## Purpose

从 PMContext 输出假设验证闭环。把 pm-skills 的 identify-assumptions/prioritize-assumptions/brainstorm-experiments 三个分散 skill 收敛为单一 skill，按"识别→排序→假设→实验"四步递进。每个假设追溯到 PMContext，杜绝凭空列风险。

## Context

PMContext 中有用户场景、价值验证度量、边界条件、竞品/市场。本 skill 提取这些信息构建假设清单。实验设计是 PMContext 的下游 View，和 OST 平级，用于验证决策。

## Instructions

- [ ] PMContext 已读取且非空（不存在则 STOP 提示运行 /pm-need）
- [ ] "用户场景"已提取（Value/Usability 假设来源）
- [ ] "价值验证度量"已提取（实验成功阈值来源）
- [ ] "边界条件"已提取（Feasibility/GTM 假设来源）
- [ ] "竞品/市场"已提取（Strategy/GTM 假设来源）
- [ ] 8 类风险假设已识别（每类 ≥1，无则标"该类无显著风险"）
- [ ] Impact×Risk 矩阵已分类（四象限）
- [ ] Top 假设已转 XYZ 形式（At least X% of Y will do Z）
- [ ] Top 假设配 pretotype 实验（方法/指标/成功阈值/skin-in-the-game）
- [ ] 每条假设在"来源"列标注追溯到的 PMContext 项
- [ ] 产物落盘到 `docs/pm-context/experiment.md`

## Thinking Protocol

本 Skill 承载 PM Thinking Loop 的步骤 1-3（理解/建模/方案）的验证部分：

| 步骤 | 本 Skill 的职责 | 产出（是否回灌 PMContext） |
|------|---------------|--------------------------|
| 1. 理解 | 从 PMContext 提取 8 类风险假设 | 不回灌（产出 View） |
| 2. 建模 | Impact×Risk 矩阵排序 | 不回灌（产出 View） |
| 3. 方案 | XYZ 假设 + pretotype 实验 | 不回灌（产出 View） |

执行时必须依次完成上述步骤，不可跳步。步骤产出写入 `.loop/experiment-step1.md` 至 `step3.md`。

**产出约束**：
- 假设必须可证伪（"Fails if ___"形式），禁"市场可能不接受"等不可证伪表述
- 实验必须有 skin-in-the-game（真实代价：时间/金钱/声誉），纯意见验证不算
- 成功阈值必须来自 PMContext 价值验证度量，禁拍脑袋定阈值
- 三视角（PM/设计/工程）各识别假设，禁只从 PM 视角

**依赖检查**：假设是否可证伪？实验是否有 skin-in-the-game？阈值是否有依据？三视角是否覆盖？

**Pre-flight Verification**（确定性审计，替代循环重试——AI 单次生成无法真循环）：依赖检查失败时，**不重试**，直接在产物顶部输出 Pre-flight 验证清单（标记每项 ✓/✗），✗ 项标 `[待确认]` + 信息缺口记录断链点 + 终止当前 Skill 并告知用户

### Step 1: 8 类风险假设识别

从三视角（PM/设计/工程）各思考"为什么可能失败"，识别 8 类假设：

| 风险类 | 核心问题 | 来源 |
|---|---|---|
| Value | 用户会持续用吗？ | PMContext 用户场景 |
| Usability | 用户能用明白吗？onboarding 够快吗？ | PMContext 用户场景 |
| Viability | 能卖/赚钱/融资吗？成本划算吗？能合规吗？ | PMContext 边界条件 |
| Feasibility | 现有技术做得了吗？集成可行吗？能扩展吗？ | PMContext 边界条件 |
| Ethics | 应该做吗？对用户有伦理风险吗？ | PMContext [需评估] |
| Go-to-Market | 能触达/说服用户试用吗？时机/渠道对吗？ | PMContext 竞品/市场 |
| Strategy | 别人能复制吗？PESTLE 因素考虑了吗？ | PMContext 竞品/市场 |
| Team | 团队配置/工具/稳定性能撑住吗？ | PMContext [假设] |

每类 ≥1 假设，无显著风险标"该类无显著风险"并说明理由。

### Step 2: Impact×Risk 优先级矩阵

对每假设评两维：
- **Impact** = 验证后创造的价值 × 影响客户数（ICE: Opportunity Score × #Customers）
- **Risk** = (1 − Confidence) × Effort

四象限分类：

| 象限 | Impact | Risk | 处置 |
|---|---|---|---|
| 高影响低风险 | 高 | 低 | 直接实施（低风险高回报） |
| 高影响高风险 | 高 | 高 | **设计实验测试（本 skill 重点）** |
| 低影响低风险 | 低 | 低 | 暂缓，待更高优先假设处理 |
| 低影响高风险 | 低 | 高 | 拒绝（不值得投入） |

聚焦"高影响高风险"象限 Top 3-5 假设。

### Step 3: XYZ 假设转化

把 Top 假设转为 XYZ 形式（Alberto Savoia）：
```
At least X% of Y will do Z
- X%: 目标市场预期参与比例
- Y: 具体目标市场
- Z: 他们会如何参与（可观测行为）
```
例：At least 15% of 月活高频创作者会使用一键续费并完成支付。

### Step 4: pretotype 实验设计

对每 XYZ 假设设计 1-2 个 pretotype 实验：

| 实验要素 | 内容 | 来源 |
|---|---|---|
| 方法 | landing page / explainer video / 预售 waitlist / concierge MVP / 灰度 | <选最便宜能证伪的> |
| 指标 | 可观测行为（非意见） | XYZ 的 Z |
| 成功阈值 | <阈值> | PMContext 价值验证度量 |
| skin-in-the-game | 用户付出时间/金钱/声誉 | 必须，否则降级为意见验证 |
| 最小代价 | <最便宜能跑的方式> | 优先选最便宜的 |
| kill criterion | <阈值> 达不到则停/改方向 | 必须，否则实验无退出条件 |

### Step 4.5: RED-GREEN-REFACTOR 验证循环（借鉴 superpowers/test-driven-development）

> 实验设计落盘后还不是"可执行"——参照 TDD 的 RED-GREEN-REFACTOR，确保实验先看见"没验证前假设不可信"（RED），再设计验证方式（GREEN），最后根据结果修正假设（REFACTOR）。

**RED 阶段**（先看 baseline——不带实验设计的假设本身是否可信）：
```
for each XYZ 假设:
  1. 问："不用这实验，当前凭什么信它？"
  2. 已有数据支持 → 标 `[已有证据]`，不实验
  3. 纯直觉/竞品做了/领导说的 → 标 `[Baseline RED]`，必须实验
  4. 记录 baseline 置信度（0-10），备实验后对比
```

**GREEN 阶段**（Step 4 的 pretotype 设计必须过"可执行"门）：
- 实验可在一周内跑完？ → 否标 🟡 退回 Step 4 缩范围
- 成功阈值可观测？ → 否标 🟡 改成功阈值为可观测行为
- skin-in-the-game 真实？ → 否标 🟡 加真实代价
- 三问全过 → 标 `[GREEN]` 可执行

**REFACTOR 阶段**（实验结果回灌本步修正假设）：
```
实验结果回来后：
- 假设证伪（Fails if 触发）→ 标 `[证伪]`，回灌 PMContext 风险段
- 假设验证（成功阈值达成）→ 标 `[验证]`，回灌 PMContext 事实段
- 结果模糊 ← 标 `[待再次验证]` 建议重设计实验
```

**纪律**（借鉴 TDD 铁律）：
- 禁跳过 RED 直接设计 GREEN——没 baseline 的验证是盲测
- REFACTOR 后假设状态必须回灌 PMContext（事实/风险/待验证三选一）
- 实验运行中不超前修改假设——等结果回来再 REFACTOR

### Step 5: 写入产物

写入 `docs/pm-context/experiment.md`，含 8 类假设表 + Impact×Risk 矩阵 + XYZ 假设 + pretotype 实验表 + 追溯列。

**🔴 CHECKPOINT** — 输出产物路径 + 假设总数 + 高影响高风险象限数 + 实验数 + `[假设]` 项数。等待 PM 确认或自动进入下一步（`--auto` 模式）。

## 流程链落盘

步骤 1-3 产出完成后，写入中间工件：
- `docs/pm-context/.loop/experiment-step1.md`（8 类假设 + 审计三元组）
- `docs/pm-context/.loop/experiment-step2.md`（Impact×Risk 矩阵 + 审计三元组）
- `docs/pm-context/.loop/experiment-step3.md`（XYZ+pretotype + 审计三元组）

## 关联增强

在"来源"列标注每假设追溯到的 PMContext 项。无来源的标 `[假设]`。与 pm-ost 交叉验证：

1. 读取 `docs/pm-context/ost.md` 的"实验设计"段，列出 OST 已有实验集合 E_ost
2. 列出本 skill 实验清单 E_exp
3. 比对：E_ost ⊄ E_exp → 把 OST 独有实验补入本清单，标 `[交叉补充]`
4. 比对：E_exp 中有而 OST 无 → 在本清单标注"OST 未覆盖"，提示 PM 是否回写 OST
5. 不一致不静默合并，两清单各自保留并在产物头部汇总差异数

## 失败模式

| 触发条件 | 一线修复 | 仍失败兜底 |
|---------|---------|-----------|
| `docs/pm-context/pm-context.md` 不存在 | **🔴 STOP**：输出"未找到 PMContext，先运行 `/pm-need <需求>`" | 不阻塞，提示后退出 |
| 某风险类无假设可识别 | 标"该类无显著风险"+ 理由 | 不强行编造假设凑数 |
| 假设不可证伪（"市场可能不接受"） | 改写为"Fails if <具体条件>" | 仍不可证伪则标 `[待确认]` |
| 实验无 skin-in-the-game | 改设计加入真实代价（预售/时间投入/声誉） | 无法加则降级标注"意见验证，置信度低" |
| 成功阈值无 PMContext 依据 | 从价值验证度量提取 | 无依据则标 `[待确认]` 让 PM 定 |
| 实验无 kill criterion | 补充达不到阈值则停/改的明确条件 | 仍无则标 `[待确认]` |
| 与 pm-ost 实验清单遗漏 | 补入 OST 未覆盖的高影响高风险实验 | 标 `[交叉补充]` |

## 不要做什么（反例黑名单）

| 反模式 | 为什么不要做 |
|--------|------------|
| 假设不可证伪（"市场可能不接受"） | 不可证伪的假设无法实验验证，是废话不是假设 |
| 实验无 skin-in-the-game | 纯意见验证不可靠，用户说"会买"≠真会买，必须真实代价 |
| 成功阈值拍脑袋定 | 无依据的阈值无法判断假设是否成立，必须来自 PMContext 度量 |
| 只从 PM 视角识别假设 | PM/设计/工程三视角缺一不可，好点子常来自工程师视角 |
| 跳过排序直接全做实验 | 资源有限，Impact×Risk 矩阵先聚焦高影响高风险 |
| 实验无 kill criterion | 没退出条件的实验会陷入"再优化一下"泥潭，必须预设停损 |
| 选最贵而非最便宜的 pretotype | pretotype 精髓是最小代价证伪，能用 landing page 验证别做 MVP |
| 8 类风险每类硬凑多条 | 强凑等于稀释，每类 ≥1 真实假设即可，无风险就如实标 |
| 审计三元组转换操作写"将 A 转换为 A'" | 同义反复，无推理密度，判定为 Failure |

## 产出示例 · 实战提示

会员产品实验片段：

```markdown
## 8 类假设（节选）
| 风险类 | 假设（Fails if） | Impact | Risk | 象限 |
|---|---|---|---|---|
| Value | Fails if 一键续费用户 4 周留存 < 40% | 0.85 | 0.6 | 高影响高风险 |
| Feasibility | Fails if 支付令牌跨平台兼容率 < 80% | 0.7 | 0.5 | 高影响高风险 |
| Ethics | 该类无显著风险（无用户敏感数据） | - | - | - |

## XYZ 假设
At least 15% of 月活高频创作者会使用一键续费并完成支付。

## pretotype 实验
| 要素 | 内容 |
|---|---|
| 方法 | 20% 用户灰度一键续费入口 |
| 指标 | 续费页完成率（行为，非意见） |
| 成功阈值 | ≥ 65% ← PMContext 价值验证度量 |
| skin-in-the-game | 用户真实支付行为 |
| 最小代价 | 灰度而非全量，前端仅加按钮 |
| kill criterion | < 50% 则停，回退 OST 重选方案 |
```

**实战铁律**（落盘前对照）：

- **最致命最便宜优先**：先找高影响高风险里最便宜能证伪的假设
- **skin-in-the-game 是底线**：用户说"会买"≠真会买，真实代价才可靠
- **Fails if 形式**：假设必须可证伪，写成"Fails if <具体条件>"
- **三视角覆盖**：PM/设计/工程各识别，避免 PM 盲区
- **kill criterion 必须预设**：没退出条件的实验会无限"再优化"
- **pretotype ≠ MVP**：pretotype 是最小代价证伪，能用 landing page 别做 MVP

### Further Reading

- [The Right It (Alberto Savoia, pretotype)](https://www.productcompass.pm/p/the-right-it)
- [Continuous Discovery Habits Assumptions (Teresa Torres)](https://www.productcompass.pm/p/cpdm)
- [XYZ Hypotheses](https://www.productcompass.pm/p/xyz-hypotheses)
