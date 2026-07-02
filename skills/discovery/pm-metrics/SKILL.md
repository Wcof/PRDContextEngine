---
name: pm-metrics
description: 首次从 PMContext 定义北极星指标 + 3-5 个 Input Metrics 组成的指标星座——分类业务游戏（注意力/交易/生产力）+ 七准则校验 + 指标树 Mermaid 图。Use when the user needs initial north star and metrics framework setup, mentions 北极星指标、north star、NSM、input metric、指标体系、metrics framework、OMTM、核心指标、价值度量、指标星座.
---

# /pm-metrics

> 你是一位度量策略师，正在从 PMContext 中提炼产品的北极星指标。**北极星不是营收指标——它反映客户从产品获得的价值，是驱散产品表现"迷雾"的先行指标。**

从 PMContext 输出北极星指标 + Input Metrics 星座。分类业务游戏 + 七准则校验 + 指标树 Mermaid 图。

## Purpose

从 PMContext 输出北极星指标框架。NSM 必须客户中心（非营收）、单一可量化、可行动、先行指标。配 3-5 个 Input Metrics 形成指标星座。每个指标追溯到 PMContext 价值验证度量。

## Context

PMContext 中有"价值验证度量"维度和用户场景。本 skill 提取这些信息，定义北极星指标框架。指标框架是 PMContext 的下游 View，指导上线后度量。

## Instructions

- [ ] PMContext 已读取且非空（不存在则 STOP 提示运行 /pm-need）
- [ ] "价值验证度量"维度已提取（作为 NSM 候选来源）
- [ ] "用户场景"维度已提取（作为业务游戏分类依据）
- [ ] 业务游戏已分类（注意力/交易/生产力）
- [ ] NSM 已定义并通过七准则校验
- [ ] 3-5 个 Input Metrics 已定义（可直接驱动 NSM）
- [ ] 指标树 Mermaid 图已生成
- [ ] 每个指标在"来源"列标注追溯到的 PMContext 项
- [ ] NSM 非营收指标（客户中心校验）
- [ ] 产物落盘到 `docs/pm-context/metrics.md`

## Thinking Protocol

本 Skill 承载 PM Thinking Loop 的步骤 4（权衡）的度量设计部分：

| 步骤 | 本 Skill 的职责 | 产出（是否回灌 PMContext） |
|------|---------------|--------------------------|
| 4. 权衡（度量） | 从 PMContext 价值验证度量定义 NSM + Input Metrics | 不回灌（产出 View） |

执行时必须依次完成上述步骤，不可跳步。步骤产出写入 `.loop/metrics-step4.md`。

**产出约束**：
- NSM 必须通过七准则全部校验，任一不满足换候选
- Input Metrics 必须可直接驱动 NSM（短期可动、直接贡献）
- 每个指标必须追溯到 PMContext 价值验证度量或用户场景

**依赖检查**：NSM 是否通过七准则？Input Metrics 是否 ≤ 5 个？指标是否有追溯？

**Pre-flight Verification**（确定性审计，替代循环重试——AI 单次生成无法真循环）：依赖检查失败时，**不重试**，直接在产物顶部输出 Pre-flight 验证清单（标记每项 ✓/✗），✗ 项标 `[待确认]` + 信息缺口记录断链点 + 终止当前 Skill 并告知用户

### Step 1: 读取 PMContext 提取度量素材

读取 `docs/pm-context/pm-context.md`，提取：
- "价值验证度量"维度 → NSM 候选
- "用户场景"维度 → 业务游戏分类依据
- "现状平替与摩擦力" → 度量基线参考

若 PMContext 不存在 → **🔴 STOP**：提示先运行 `/pm-need`。

### Step 2: 分类业务游戏

从 PMContext 用户场景判断产品玩哪种游戏：

| 游戏 | 核心问题 | 典型产品 | NSM 方向 |
|---|---|---|---|
| **注意力游戏** | 用户花多少时间用产品？ | Facebook/Spotify/YouTube/TikTok | 时长/会话数/活跃天数 |
| **交易游戏** | 平台促成多少交易？ | Amazon/Uber/Airbnb/PayPal | 交易量/GMV/成功订单 |
| **生产力游戏** | 用户多高效完成工作？ | Canva/Dropbox/Loom/Notion | 任务完成数/效率提升 |

### Step 3: 定义北极星指标

从价值验证度量候选中选 NSM，必须通过七准则校验：

1. **易懂** — 全员都能理解定义
2. **客户中心** — 反映客户获得的价值，非营收/活跃度
3. **可持续价值** — 反映习惯和长期参与
4. **愿景对齐** — 代表向愿景的有意义进展
5. **可量化** — 数字追踪
6. **可行动** — 团队可通过产品/营销/运营直接影响
7. **先行指标** — 预测未来业务成功和营收增长

任一不满足 → 换下一个候选。

### Step 4: 定义 Input Metrics

定义 3-5 个 Input Metrics（先行指标），每个：
- 短期更容易动
- 直接贡献 NSM
- 帮定位优化发力点

### Step 5: 生成指标树并写入产物

写入 `docs/pm-context/metrics.md`，格式：

```markdown
# 北极星指标框架

> 来源: PMContext <需求名>
> 业务游戏: <注意力/交易/生产力> | NSM: <指标> | Input Metrics: N 个

## 业务游戏分类
<游戏> ← 来源: PMContext 用户场景
理由: <为什么是这个游戏>

## 北极星指标（NSM）
**NSM:** <指标名> = <定义/计算公式>
<一句话解释为什么是这个指标>

### 七准则校验
| 准则 | 通过 | 说明 | 来源 |
|---|---|---|---|
| 易懂 | ✓ | <说明> | PMContext 价值验证度量 |
| 客户中心 | ✓ | <说明> | - |
| 可持续价值 | ✓ | <说明> | PMContext 用户场景 |
| 愿景对齐 | ✓ | <说明> | - |
| 可量化 | ✓ | <说明> | - |
| 可行动 | ✓ | <说明> | - |
| 先行指标 | ✓ | <说明> | - |

## Input Metrics（3-5 个）

​```mermaid
flowchart TD
  NSM[NSM: <指标>] --> IM1[Input 1: <指标>]
  NSM --> IM2[Input 2: <指标>]
  NSM --> IM3[Input 3: <指标>]
  NSM:::nsm
  classDef nsm fill:#fff3cd,stroke:#856404,stroke-width:3px
​```

| Input Metric | 定义 | 如何驱动 NSM | 来源 |
|---|---|---|---|
| <指标1> | <定义> | <驱动关系> | PMContext 价值验证度量 |
| <指标2> | <定义> | <驱动关系> | PMContext [假设, 7/10] |

## 度量采集计划
| 指标 | 采集方式 | 采集时机 | 阈值 | 来源 |
|---|---|---|---|---|
| NSM | <方式> | 上线后第 N 天 | <阈值> | PMContext 价值验证度量 |
| Input 1 | <方式> | <时机> | <阈值> | - |
```

**🔴 CHECKPOINT** — 输出产物路径 + 业务游戏 + NSM + Input Metrics 数 + `[假设]` 项数。等待 PM 确认或自动进入下一步（`--auto` 模式）。

## 流程链落盘

步骤 4（权衡）产出完成后，写入中间工件：
- `docs/pm-context/.loop/metrics-step4.md`（指标追溯映射 + 审计三元组）

## 关联增强

在"来源"列标注每个指标追溯到的 PMContext 项。无来源的指标标 `[假设]`。

## 失败模式

| 触发条件 | 一线修复 | 仍失败兜底 |
|---------|---------|-----------|
| `docs/pm-context/pm-context.md` 不存在 | **🔴 STOP**：输出"未找到 PMContext，先运行 `/pm-need <需求>`" | 不阻塞，提示后退出 |
| PMContext 中"价值验证度量"维度为空 | **🔴 STOP**：输出"价值验证度量未精炼，先运行 `/pm-refine` 补全 P2 维度" | 不臆造指标 |
| NSM 候选全部不通过七准则 | 重新从 PMContext 用户场景提炼候选；若仍无则提示 PM 补充业务愿景 | 标 `[待确认]` 并提示"NSM 待定，需 PM 明确业务愿景" |
| NSM 是营收/LTV 指标 | 拒绝，改为客户中心指标（如任务完成率/留存率） | 仍无法找到客户中心指标则标 `[待确认]` |
| Input Metrics > 5 个 | 精简到 3-5 个最直接驱动 NSM 的 | 无法精简则按影响力排序取 Top 5 |
| Input Metrics 无法追溯到 PMContext | 标 `[假设]` 并提示"该 Input Metric 需 PM 确认" | 不阻塞，但 metrics.md 顶部加 ⚠️ |
| 业务游戏无法明确分类 | 列出候选游戏 + 各自理由，标 `[待确认]` 让 PM 决定 | 不阻塞，提示 PM 确认游戏类型 |

## 不要做什么（反例黑名单）

| 反模式 | 为什么不要做 |
|--------|------------|
| NSM 用营收/LTV/DAU 指标 | NSM 必须客户中心，反映客户获得的价值，营收是结果不是先行指标 |
| 定义多个 NSM | NSM 必须单一，多个 NSM 等于没 NSM，团队失去焦点 |
| Input Metrics 超过 5 个 | 过多 Input Metrics 稀释注意力，3-5 个是甜区 |
| NSM 不通过七准则就硬用 | 七准则是 NSM 质量门，任一不满足换候选，不要硬塞 |
| 指标不追溯到 PMContext | 指标与需求脱节，可能度量了不该度量的 |
| 用绝对值指标（总用户数）当 NSM | 优先比率型（转化率/留存率），绝对值不反映价值密度 |
| NSM 不可行动（团队无法直接影响） | 不可行动的指标是虚荣指标，无指导意义 |
| 审计三元组转换操作写"将 A 转换为 A'" | 同义反复，无推理密度，判定为 Failure |
| 审计三元组转换操作写"基于上述依据产出" | 空话，未阐明具体推导逻辑，判定为 Failure |

## 产出示例

会员续费场景 NSM 框架：

```markdown
## 业务游戏分类
**生产力游戏** ← 来源: PMContext 用户场景"会员管理是周期性运营任务"
理由: 用户用产品高效完成会员管理，非娱乐消磨时间

## 北极星指标（NSM）
**NSM:** 月度活跃会员续费率 = 当月成功续费会员数 / 当月到期会员数
反映会员对产品价值的持续认可，是营收的先行指标

### 七准则校验
| 准则 | 通过 | 说明 |
|---|---|---|
| 客户中心 | ✓ | 反映会员选择继续使用，非营收 |
| 先行指标 | ✓ | 续费率下降预示流失，先于营收下降 |

## Input Metrics
| Input Metric | 定义 | 如何驱动 NSM | 来源 |
|---|---|---|---|
| 到期提醒触达率 | 看到提醒的到期会员占比 | 提醒触达→续费意愿 | PMContext 规则: 到期提醒 |
| 续费流程完成率 | 进入续费页后完成支付的比例 | 流程顺畅→完成率高 | PMContext 摩擦力 |
| 续费页停留时长 | 用户在续费页平均停留时间 | 时长短→流程顺畅 | PMContext [假设, 7/10] |
```

### Further Reading

- [The North Star Framework 101](https://www.productcompass.pm/p/the-north-star-framework-101)
- [AARRR (Pirate) Metrics](https://www.productcompass.pm/p/aarrr-pirate-metrics)
- [Google HEART Framework](https://www.productcompass.pm/p/the-google-heart-framework)

## 产出示例 · 延伸参考 · 实战提示

详见 [references/metrics-example.md](references/metrics-example.md)（完整 NSM 框架示例 + 三业务游戏 NSM 对照表）。

### 实战提示

- **客户中心是底线**：NSM 反映客户价值，营收/LTV/DAU 都是结果指标，不是 NSM
- **单一 NSM 聚焦团队**：多个 NSM 等于没 NSM，团队需要单一北极星
- **Input Metrics 是杠杆**：短期可动的 Input Metrics 是团队日常发力点
- **七准则是质量门**：任一不满足换候选，不要硬塞
- **与 PMContext 价值验证度量互补**：PMContext 的度量是功能级，NSM 是产品级
