---
name: pm-abtest
description: 从 PMContext 与实验数据做 A/B 测试统计分析——样本量/时长/SRM 验证 + 显著性计算（p 值/CI/lift）+ guardrail 检查 + ship/extend/stop 决策，每结论附 PMContext 度量追溯。Use when the user asks for A/B test analysis or experiment results interpretation, mentions A/B 测试、ab test、split test、实验结果、显著性、statistical significance、p-value、confidence interval、置信区间、lift、SRM、样本比例失调、guardrail、ship or stop、实验决策.
---

# /pm-abtest

> 你是一位实验分析师。摆在你面前的是一组 A/B 测试结果——对照组与变体组的转化数据、运行时长、流量切分。你的任务是用统计 rigor 把数字翻译成 ship/extend/stop 决策，而不是用"看起来涨了"糊弄过去。

从 PMContext 与实验数据做 A/B 测试统计分析。验证实验设置 → 计算显著性 → 检查 guardrail → 输出决策建议。

## Purpose

把 A/B 测试原始数字翻译成可执行的产品决策。pm-skills 的 ab-test-analysis 收敛进 PMSkill 体系：从 PMContext 价值验证度量提取实验假设与 guardrail，结论追溯 PMContext 度量项，杜绝"看数字下结论"。

## Context

PMContext 中"价值验证度量"定义了实验应移动的指标与阈值；"边界条件"定义了 guardrail（不可退化的指标）；"用户场景"定义了实验人群。本 skill 提取这些信息构建统计 rigor 的实验分析。A/B 测试分析是 PMContext 的下游 View，和 PRD/草图平级。

## Instructions

- [ ] PMContext 已读取且非空（不存在则 STOP 提示运行 /pm-need）
- [ ] "价值验证度量"已提取（实验主指标 + 阈值来源）
- [ ] "边界条件"已提取（guardrail 指标来源）
- [ ] "用户场景"已提取（实验人群定义来源）
- [ ] 实验设置四项验证完成（样本量/时长/随机化/SRM/新鲜效应）
- [ ] 显著性四项计算完成（转化率/lift/p-value/95% CI）
- [ ] guardrail 指标退化检查完成
- [ ] ship/extend/stop 决策已输出，附理由
- [ ] 每结论在"来源"列标注追溯到的 PMContext 度量项
- [ ] 产物落盘到 `docs/pm-context/abtest.md`

## Thinking Protocol

本 Skill 承载 PM Thinking Loop 的步骤 5（风险）+ 步骤 6（交付）的实验分析部分：

| 步骤 | 本 Skill 的职责 | 产出（是否回灌 PMContext） |
|------|---------------|--------------------------|
| 5. 风险 | guardrail 退化检查 + SRM 验证（实验效度风险） | 回灌实验结论到决策日志 |
| 6. 交付 | ship/extend/stop 决策建议 | 不回灌（产出 View） |

执行时必须依次完成上述步骤，不可跳步。步骤产出写入 `.loop/abtest-step5.md`、`.loop/abtest-step6.md`。

**产出约束**：
- 样本量必须用公式 `n = ((Z_α/2 + Z_β)² × 2 × p × (1-p)) / MDE²` 验证是否达到 80% power（Z_β 对应 80% power = 0.84），不足则标 🔴 underpowered
- p-value 必须用 two-tailed z-test 或 chi-squared 计算，禁只看转化率差值
- 95% CI 必须给出，lift 必须区分 statistical significance（p<0.05）与 practical significance（业务意义）
- guardrail 任一退化则 ship 决策降级为 extend/stop

**依赖检查**：样本量是否足够？SRM 是否存在？guardrail 是否退化？

**Pre-flight Verification**（确定性审计，替代循环重试——AI 单次生成无法真循环）：依赖检查失败时，**不重试**，直接在产物顶部输出 Pre-flight 验证清单（标记每项 ✓/✗），✗ 项标 `[待确认]` + 信息缺口记录断链点 + 终止当前 Skill 并告知用户

### Step 1: 读取 PMContext 提取实验素材

读取 `<产物目录>/pm-context.md`（先读 `## PMSkill` 块取 `产物目录`，块不存在回退默认 `docs/pm-context/`），提取：
- "价值验证度量" → 实验主指标（primary metric）+ 阈值
- "边界条件" → guardrail 指标（revenue/engagement/latency 等）
- "用户场景" → 实验人群定义

若 PMContext 不存在 → **🔴 STOP**：提示先运行 `/pm-need`。

### Step 2: 实验设置验证

| 验证项 | 标准 | 失败处理 |
|--------|------|---------|
| 样本量 | 达到 80% power（公式验证） | 标 🔴 underpowered，建议延长实验 |
| 运行时长 | ≥ 1-2 个完整业务周期 | 标 🟡 周期不足，结论谨慎 |
| 随机化 | 无 sample ratio mismatch（SRM） | SRM 存在则 🔴 STOP，结论不可信 |
| 新鲜/首因效应 | 已 wash out 初始行为变化 | 不足则标 🟡 可能受新鲜效应影响 |

### Step 3: 显著性计算

```
转化率（control）= cc / cn
转化率（variant）= vc / vn
相对 lift = (vc/vn - cc/cn) / (cc/cn) × 100%
p-value = two-tailed z-test 或 chi-squared
95% CI = [lift - 1.96×SE, lift + 1.96×SE]
统计显著 = p < 0.05
业务显著 = lift ≥ PMContext 阈值
```

若用户提供原始数据，生成并运行 Python 脚本计算。

### Step 4: guardrail 检查

| guardrail 指标 | control | variant | 退化? | 决策影响 |
|---------------|---------|---------|------|---------|
| <PMContext 边界条件中的指标> | | | 是/否 | 退化则 ship 降级 |

主指标赢但 guardrail 退化 = 不是真赢。

### Step 5: 决策矩阵

| 主指标结果 | guardrail | 决策 | 后续动作 |
|-----------|-----------|------|---------|
| 统计+业务显著 | 无退化 | **Ship** | 全量发布，监测 1-2 周防回退 |
| 统计显著但业务不显著 | 无退化 | **Extend** | 延长实验或调高 MDE 重设 |
| 不显著 | 无退化 | **Stop** | 假设证伪，记录学习回灌 PMContext |
| 显著 | guardrail 退化 | **Stop 或 Extend** | 查退化原因，不可直接 ship |
| 显著但 underpowered | 无退化 | **Extend** | 延长至达标样本量再判 |

### Step 6: 写入产物

写入 `docs/pm-context/abtest.md`，含设置验证表 + 显著性计算 + guardrail 表 + 决策矩阵 + 追溯列。

**🔴 CHECKPOINT** — 输出产物路径 + 决策（ship/extend/stop）+ 主指标 lift + p-value + guardrail 状态。等待 PM 确认或自动进入下一步（`--auto` 模式）。

## 流程链落盘

步骤 5-6 产出完成后，写入中间工件：
- `docs/pm-context/.loop/abtest-step5.md`（guardrail+SRM 验证 + 审计三元组）
- `docs/pm-context/.loop/abtest-step6.md`（决策矩阵 + 审计三元组）

## 关联增强

在"来源"列标注每结论追溯到的 PMContext 度量项。实验结论与 pm-experiment 的假设清单交叉验证（实验结果应回填到对应假设的验证状态）。

## 失败模式

| 触发条件 | 一线修复 | 仍失败兜底 |
|---------|---------|-----------|
| `docs/pm-context/pm-context.md` 不存在 | **🔴 STOP**：输出"未找到 PMContext，先运行 `/pm-need <需求>`" | 不阻塞，提示后退出 |
| PMContext "价值验证度量"为空 | **🔴 STOP**：输出"无实验主指标定义，先运行 `/pm-refine` 补度量" | 不臆造主指标 |
| 用户未提供实验数据 | 提示用户提供 control/variant 的转化数与样本量 | 不编造数据 |
| 样本量不足（underpowered） | 标 🔴 underpowered，建议延长实验 | 不下 ship 结论 |
| SRM 存在（样本比例失调） | **🔴 STOP**：输出"SRM 检测到随机化失败，结论不可信，排查分流逻辑" | 不输出显著性结论 |
| guardrail 数据缺失 | 标 `[待确认]`，决策降级为 extend（不可 ship 未验证 guardrail 的实验） | 不静默跳过 guardrail |
| p-value 计算脚本失败 | 改用查表法近似（z 分布表） | 仍失败则标 `[待确认]` 让 PM 手算 |
| 实验结论与 pm-experiment 假设冲突 | 标 `[冲突]` 让 PM 裁决 | 不静默合并 |

## 不要做什么（反例黑名单）

| 反模式 | 为什么不要做 |
|--------|------------|
| 只看转化率差值不看 p-value | 差值可能是噪声，p<0.05 才算信号 |
| 不计算 95% CI | 没有置信区间的 lift 不知道不确定性范围 |
| 混淆统计显著与业务显著 | p<0.05 但 lift 0.1% 对业务无意义，不能 ship |
| 跳过 guardrail 检查直接 ship | 主指标赢但 guardrail 退化是假赢 |
| SRM 存在仍下结论 | 随机化失败意味着两组不可比，任何结论都是错的 |
| underpowered 实验下 ship 结论 | 样本不足可能漏掉真实效应或放大噪声 |
| 不追溯 PMContext 度量项 | 实验结论悬空，无法回填到假设验证状态 |
| 审计三元组转换操作写"基于上述依据产出" | 空话，未阐明具体推导逻辑，判定为 Failure |

## 产出示例 · 实战提示

会员产品 A/B 测试分析片段：

```markdown
## 实验设置验证
| 验证项 | 结果 | 状态 |
|--------|------|------|
| 样本量 | control 5023 / variant 4987，MDE 3% 需 4800（80% power, α=0.05, Z_α/2=1.96, Z_β=0.84） | ✅ 达标 |
| 运行时长 | 14 天（2 个完整周周期） | ✅ |
| SRM | 期望 5000/5000，实际 5023/4987，χ²=0.13, p=0.72 | ✅ 无 SRM |
| 新鲜效应 | 前 3 天剔除后趋势稳定 | ✅ |

## 显著性
- 转化率：control 12.3% → variant 13.8%
- 相对 lift：+12.3%
- p-value：0.0246（< 0.05 统计显著）
- 95% CI：[+1.6%, +23.1%]
- PMContext 阈值：+10% → ✅ 业务显著

## guardrail
| 指标 | control | variant | 退化? |
|------|---------|---------|------|
| 人均收入 | ¥45.2 | ¥44.8 | 否（-0.9%，p=0.45） |
| 7 日留存 | 68% | 67% | 否（p=0.32） |

## 决策：Ship
理由：统计+业务双显著，guardrail 无退化。全量发布，监测 2 周。
```

详见 [references/abtest-example.md](references/abtest-example.md)（完整 A/B 测试分析示例含 Python 计算脚本）。

**实战铁律**（落盘前对照）：

- **SRM 是第一道闸门**：SRM 存在则一切结论作废，先修分流
- **统计显著≠业务显著**：p<0.05 但 lift 低于 PMContext 阈值不 ship
- **guardrail 退化即停**：主指标赢但 guardrail 输是假赢，查原因
- **underpowered 不下结论**：样本不足延长实验，不要硬判
- **结论回填假设**：实验结果要回灌 pm-experiment 的假设验证状态

### Further Reading

- [A/B Testing Statistical Significance](https://www.productcompass.pm/p/ab-testing-statistical-significance)
- [The Product Analytics Playbook: AARRR, HEART, Cohorts & Funnels](https://www.productcompass.pm/p/the-product-analytics-playbook-aarrr)
- [Sample Ratio Mismatch Detection](https://www.productcompass.pm/p/srm-detection)
