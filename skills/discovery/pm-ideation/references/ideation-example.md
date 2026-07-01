# 方案发散完整示例

## 场景

会员产品从 PMContext 发散 ≥5 方案。

## 新旧场景分类

- optimize：现有产品改进（PMContext 用户场景已覆盖的"创作者产能管理"）
- explore：新场景拓展（PMContext 未覆盖的相邻 JTBD）

## 5 个方案

| # | 类型 | 方案 | 假设 | 最便宜验证 | 追溯 |
|---|------|------|------|-----------|------|
| 1 | optimize | 智能排期优化（基于历史数据推荐选题时间） | 用户会采纳推荐时间 | 5 用户访谈（pm-interview） | PMContext 用户场景 |
| 2 | optimize | 断更预警增强（提前 5 天+多渠道触达） | 提前预警降断更更多 | 已有数据分析（pm-cohort） | PMContext 现状平替 |
| 3 | explore | 团队协作版（多用户共享排期+审批） | 小团队有协作需求 | landing page waitlist | PMContext 边界条件 |
| 4 | explore | 企业版（数据看板+批量采购+SLA） | 企业有采购需求 | 5 企业访谈 | 推断 |
| 5 | explore | API 开放（让开发者集成排期能力） | 开发者会集成 | 社区调研（Reddit/V2EX） | 推断 |

## 去重校验

| 方案对 | 重叠? | 处理 |
|--------|------|------|
| 1 vs 2 | 无（排期 vs 预警） | 保留 |
| 3 vs 4 | 部分（都涉团队） | 保留（3=小团队协作，4=企业管理，细分不同） |
| 5 vs 其他 | 无（API 是新形态） | 保留 |

无重复方案，5 个全保留。

## 回灌 PMContext

5 方案候选回灌 PMContext 方案候选段，联动：
- pm-assumption：每方案的假设进 8 类风险清单
- pm-experiment：每方案的最便宜验证进实验 backlog
- pm-grill：方案 3/4 的 `[假设]` 需质询

## 审计三元组

`<依据集: [PMContext 用户场景+现状平替+边界条件]> → [工具: /pm-ideation, 规则: optimize/explore≥5+最便宜验证] → [转换: 从用户场景推导 optimize，从边界条件推导 explore，同义词推导：PM 说"协作"→映射 explore 方案 3] → <产出: 5 方案（2 optimize+3 explore）+验证+去重+回灌>`
