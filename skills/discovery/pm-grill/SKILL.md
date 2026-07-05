---
name: pm-grill
description: 对 PMContext 做 relentless 质询压力测试——红队攻击承重假设（steelman-then-attack 三段式：先述最强版本再攻击）+ 八维置信度盘问 + 用户/市场/可行性/度量四面逼问，产出致命缺口清单与最便宜证伪测试。Use when the user asks to stress-test or pressure-test PMContext, mentions 质询、压力测试、红队、red team、grill、盘问、挑刺、stress test、challenge assumptions、攻击假设、承重假设、kill criteria、最便宜测试、steelman.
metadata:
  internal: true
---

# /pm-grill

> 你是一位不留情面的红队审问者，正对 PMContext 发起 relentless 质询——**找出"承重墙"（若假则计划死的承重假设），筑 strongest steelman 后全力攻击，返回最便宜的证伪测试。** 计划只经历过客气反馈就上会等于裸奔。

对 PMContext 输出质询压力测试。承重假设攻击 + 八维置信度盘问 + 四面逼问 + 致命缺口清单。

## Purpose

从 PMContext 输出质询压力测试。融合 superpowers/grilling 的 relentless 面试与 pm-skills/strategy-red-team 的承重假设攻击，针对 PMContext 而非泛泛计划。目标是更锐利的决策，不是更长的风险清单——5 个真实致命缺口胜过 20 条通用风险。

## Context

PMContext 是被审对象。本 skill 是 PMContext 的质量门，不产出新 View 而是产出"缺口清单 + 证伪测试"。与 pm-premortem 区别：premortem 假设已失败倒推原因，grill 攻击当下承重假设逻辑。与 pm-experiment 区别：experiment 构建验证闭环，grill 只找致命缺口不设计完整实验。

## Instructions

- [ ] PMContext 已读取且非空（不存在则 STOP 提示运行 /pm-need）
- [ ] 承重假设已提取（若假则计划死的，与装饰性假设分离）
- [ ] 每承重假设已 steelman（最强版本）后攻击
- [ ] 每失败模式已写"Fails if ___"（具体可证伪）
- [ ] 八维置信度已盘问（每维标置信度 + 缺口）
- [ ] 用户/市场/可行性/度量四面逼问已完成
- [ ] 按 impact×likelihood×cheapness-to-test 排序
- [ ] Top 缺口已配"本周最便宜测试 + kill criterion"
- [ ] 自我反驳（不制造计划没有的弱点，强论证如实承认）
- [ ] 产物落盘到 `docs/pm-context/grill.md`

## Thinking Protocol

本 Skill 承载 PM Thinking Loop 的步骤 1（理解）的审计部分：

| 步骤 | 本 Skill 的职责 | 产出（是否回灌 PMContext） |
|------|---------------|--------------------------|
| 1. 理解 | 攻击承重假设 + 盘问置信度 + 逼问缺口 | 回灌：致命缺口标入 PMContext 信息缺口 |

执行时必须依次完成上述步骤，不可跳步。步骤产出写入 `.loop/grill-step1.md`。

**产出约束**：
- 只攻击承重假设（若假则计划死），装饰性假设不浪费时间
- 必须 steelman 后攻击，攻击稻草人无效
- 默认"风险真实"，但计划已引证据反驳时如实承认强论证
- 不制造计划没有的弱点（red-team 造疑与 rubber-stamp 同样无用）
- Top 5 致命缺口即可，不为凑数堆 20 条

**依赖检查**：是否只攻承重假设？是否 steelman？是否自我反驳？是否聚焦 Top 5？

**Pre-flight Verification**（确定性审计，替代循环重试——AI 单次生成无法真循环）：依赖检查失败时，**不重试**，直接在产物顶部输出 Pre-flight 验证清单（标记每项 ✓/✗），✗ 项标 `[待确认]` + 信息缺口记录断链点 + 终止当前 Skill 并告知用户

### Step 1: 读取 PMContext 提取承重假设

读取 `<产物目录>/pm-context.md`（先读 `## PMSkill` 块取 `产物目录`，块不存在回退默认 `docs/pm-context/`），列出它断言为真的一切（关于用户/市场/约束/机制/时间线/度量）。分离**承重假设**（若假则计划死）与装饰性假设。只攻击承重假设。

若 PMContext 不存在 → **🔴 STOP**：提示先运行 `/pm-need`。

### Step 2: steelman 后攻击

对每承重假设，按 **steelman-then-attack 三段式**（借鉴 skills/grill-me relentless 纪律）：

```
假设: <承重假设>
Steelman（最强版本，3-5 句为它辩护）:
  <用计划支持者最强论据重述此假设为何为真——非稻草人，是最难驳的版本>
Attack（攻击那个最强版本）:
  <针对 steelman 的论据逐条攻击，指出它在何条件下崩塌>
Fails if（精确可证伪的失败条件）:
  <具体可观测的事件/数据，发生即假设死>
```

每失败模式写"Fails if ___"（具体可证伪）：
- 好：Fails if 激活率其实不是当前约束
- 坏：执行风险

**steelman 质量校验**（防稻草人攻击）：
- steelman 是否用了计划支持者会认可的最强论据？（若支持者说"这不是我的论点"=稻草人）
- attack 是否针对 steelman 而非原假设的弱版本？（攻击弱版本=无效）
- Fails if 是否可观测可证伪？（"用户不接受"不可证伪，"D7 留存 < 15%"可证伪）

### Step 2.5: 逐项追问模式（relentless interview — 借鉴 skills/grilling）

> 默认模式（Step 2）是全景扫描——一次性列出所有承重假设并攻击。但有些假设相互依赖，扫完不能停。**追问模式**（本步）走决策树——每次问一项、等 PM 反馈、再继续，确保依赖关系不会被跳跃。

**触发条件**：当 PMContext 中承重假设之间存在显式依赖链（如"假设 A 为真才可假设 B"+"用户增长假设依赖定价假设"）→ 自动进入追问模式，不能全景扫完一次给。

**追问模式执行**：
```
for each 承重假设分支（按依赖排序）:
  1. 只问当前分支最关键的 1 个问题
  2. 提供推荐答案（"我们建议认为 X，因为 PMContext 证据 Y"）
  3. 等 PM 反馈（多问一起=让人困惑）
     - PM 确认 → 采信，推进
     - PM 否认 → 重估假设，可能改分支路径
     - PM 不确定 → 标 `[待确认]` 继续，但标注风险
  4. 能查代码/数据的则不问（"不要问如果可以直接查"）
```

追问模式不走标准 Step 3-4，走完 Step 2.5 后直接进入 Step 5 排序。

**纪律**（借鉴 grilling 的 "one at a time"）：
- 一次只问 1 个问题，禁合并提问
- 每问附带推荐答案，禁让 PM 从零回答
- 可查的直接查，不制造无意义的问题
- 依赖分支走完即止，不走完全部分支也可退出

### Step 3: 八维置信度盘问

对 PMContext 八维逐盘问，标置信度（高/中/低）+ 缺口：

| 维度 | 盘问问题 | 置信度 | 缺口 |
|---|---|---|---|
| 用户场景 | 场景是观察到的还是想象的？样本量？ | | |
| 现状平替 | 平替真的在被用吗？还是假设？ | | |
| 摩擦力 | 摩擦力是用户说的还是你猜的？ | | |
| 价值验证度量 | 度量能真反映价值吗？还是虚荣指标？ | | |
| 竞品/市场 | 竞品数据时效性？市场份额来源？ | | |
| 边界条件 | 约束是硬约束还是自设的？ | | |
| 技术栈 | 技术选型有验证吗？还是惯性？ | | |
| 假设清单 | 假设都显式了吗？有无隐性假设？ | | |

### Step 4: 四面逼问

| 面 | 逼问 |
|---|---|
| 用户面 | 谁具体会用？不是"中小企业"而是"某规模某行业某角色"。他们现在怎么活？为什么换？ |
| 市场面 | 市场够大吗？增长还是萎缩？时机为什么是现在不是三年前/后？ |
| 可行性面 | 团队做得出来吗？时间够吗？依赖的外部条件成立吗？ |
| 度量面 | 成功怎么量化？阈值有依据吗？达不到会停吗？还是"再优化一下"？ |

### Step 5: 排序与最便宜测试

按 `(impact if wrong) × (likelihood wrong) × (cheapness to test)` 排序。Top 即本周该测的——高影响、可能错、便宜查。

对每存活致命缺口给运营者可做的事：
- **Fails if**：精确破坏条件
- **本周证据**：能廉价确认/杀死的具体数据/查询/对话
- **Kill criterion**：停/改的阈值
- **最便宜测试**：最小代价移动信念的实验

**"最便宜"判定标准**（按成本阶梯选最低档）：
1. 已有数据查询（1 条 SQL/分析，<1 人日）→ 首选
2. 用户对话（5-20 次访谈，<1 周人力）→ 次选
3. 轻量 pretotype（landing page/waitlist/灰度，<2 周人力）→ 再次
4. 超 1 周人力或需全量 MVP → 标 `[需评估成本]`，不默认推荐

### Step 6: 自我反驳 + 写入产物

逐条检查：这条风险是计划真有的，还是我造的？计划已引证据反驳的，如实说"此风险计划已较好应对"。不制造疑虑。

写入 `docs/pm-context/grill.md`，含承重假设表 + steelman 攻击 + 八维置信度 + 四面逼问 + Top 5 致命缺口 + 最便宜测试 + 追溯列。致命缺口回灌 PMContext 信息缺口段。

**🔴 CHECKPOINT** — 输出产物路径 + 承重假设数 + 致命缺口 Top5 + 本周最便宜测试数。等待 PM 确认或自动进入下一步（`--auto` 模式）。

## 流程链落盘

步骤 1 产出完成后，写入中间工件：
- `docs/pm-context/.loop/grill-step1.md`（承重假设攻击 + 八维盘问 + 四面逼问 + 审计三元组）

## 关联增强

致命缺口回灌 PMContext "信息缺口"段。与 pm-premortem 互补（grill 攻当下逻辑，premortem 倒推失败）。与 pm-experiment 衔接（grill 的 Top 缺口 → experiment 的 Top 假设）。

## 失败模式

| 触发条件 | 一线修复 | 仍失败兜底 |
|---------|---------|-----------|
| `docs/pm-context/pm-context.md` 不存在 | **🔴 STOP**：输出"未找到 PMContext，先运行 `/pm-need <需求>`" | 不阻塞，提示后退出 |
| PMContext 过于稀疏无承重假设可攻 | **🔴 STOP**：输出"PMContext 信息不足，先运行 `/pm-refine` 补全" | 不强行攻击空内容 |
| 攻击了稻草人（非最强版本） | 退回 steelman 重写攻击 | 仍攻稻草人则该条作废标 `[无效攻击]` |
| 制造计划没有的弱点 | 删除该条，如实承认计划强论证 | 不为凑数造疑 |
| Top 缺口 > 5 个 | 按排序截断到 Top 5 | 不堆砌，5 个真实胜过 20 条通用 |
| 最便宜测试不便宜（成本超一周人力） | 重新设计更小代价测试 | 无法降本则标 `[需评估成本]` |
| 缺口与 pm-experiment 假设重复 | 标交叉引用，不重复展开 | grill 只找不设计完整实验 |

## 不要做什么（反例黑名单）

| 反模式 | 为什么不要做 |
|--------|------------|
| 攻击稻草人（非最强版本） | 攻击弱版本无效，必须先 steelman 再攻那个强版本 |
| 制造计划没有的弱点 | red-team 造疑与 rubber-stamp 同样无用，只找真弱点 |
| 攻击装饰性假设 | 装饰性假设假了计划不死，浪费时间，只攻承重假设 |
| 失败模式写"执行风险" | 不可证伪，必须写"Fails if <具体条件>" |
| 堆 20 条通用风险 | 目标是更锐利决策非更长清单，5 个致命胜过 20 条通用 |
| 最便宜测试要全量 MVP | 最便宜测试是最小代价移动信念，能用对话/查询别做 MVP |
| 跳过自我反驳 | 不自我反驳的 red-team 会造疑，失去公信力 |
| 与 pm-premortem 混用 | grill 攻当下承重假设逻辑，premortem 倒推失败叙事，定位不同 |
| 审计三元组转换操作写"基于上述依据产出" | 空话，未阐明具体推导逻辑，判定为 Failure |

## 产出示例 · 实战提示

会员产品 grill 片段：

```markdown
## 承重假设攻击（节选）
| 承重假设 | Steelman | 攻击 | Fails if |
|---|---|---|---|
| 高频创作者愿为稳定输出付费 | 创作者收入依赖稳定输出，工具成本低 | 但免费替代品（日历提醒+模板）已达 80% 功能 | Fails if 免费平替的 80% 功能使付费意愿 < 15% |

## 八维置信度（节选）
| 维度 | 置信度 | 缺口 |
|---|---|---|
| 用户场景 | 中 | 场景来自 5 次访谈，样本量偏小 |
| 价值验证度量 | 低 | 续费率是虚荣指标？应看 NRR |

## 四面逼问（度量面）
成功怎么量化？续费率 60%→75%。阈值有依据吗？无竞品基准。达不到会停吗？未定义 kill criterion——这是致命缺口。

## Top 5 致命缺口（节选）
1. **Fails if** 免费平替使付费意愿 < 15%
   - 本周证据：访谈 20 个用免费平替的创作者问付费意愿
   - Kill criterion：付费意愿 < 10% 则停
   - 最便宜测试：20 次对话，<1 周人力
2. **Fails if** 续费率不是价值真指标（应看 NRR）
   - 本周证据：拉现有会员 NRR 与续费率相关性
   - Kill criterion：相关性 < 0.5 则换指标
   - 最便宜测试：1 条 SQL 查询
```

**实战铁律**（落盘前对照）：

- **只攻承重假设**：若假则计划死，装饰性假设不浪费时间
- **steelman 是底线**：攻稻草人无效，先述最强版再攻那个最强版
- **自我反驳保公信**：计划强论证如实承认，造疑的 red-team 没人信
- **5 个致命胜过 20 条通用**：目标是更锐利决策非更长清单
- **最便宜测试优先**：能用对话/查询别做 MVP，本周能跑的最便宜最该先做
- **与 experiment 衔接**：grill 找致命缺口，experiment 设计完整验证闭环

### Further Reading

- [Strategy Red-Team: Attack Assumptions Before Reality](https://www.productcompass.pm/p/strategy-red-team)
- [The Premortem vs The Red-Team](https://www.productcompass.pm/p/premortem-vs-redteam)
- [Relentless Interview for Plans (grilling)](https://www.productcompass.pm/p/grilling)
