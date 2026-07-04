# ADR 0011：pm-strategy 与 pm-businessmodel 保留并存

- 状态：Accepted
- 日期：2026-07-04
- 决策者：PMSkill 整改复审（奥卡姆剃刀轮）

## 背景

发现侧 `pm-strategy` 与 `pm-businessmodel` 存在语义重叠：前者 Lean Canvas 框架涉及商业模式假设，后者产出 9 模块 BMC，二者都触及"商业模式"。

## 决策

**保留两者，不合并。**

## 理由

| 维度 | pm-strategy | pm-businessmodel |
|------|-------------|------------------|
| 主框架 | SWOT / Porter 五力 / Ansoff / Lean Canvas 四框架组合 | 9 模块 BMC 单一框架 |
| 视角 | 战略选择（现状→行业→增长→商业模式四阶） | 商业模式画布的完整结构化呈现 |
| Lean Canvas 在 pm-strategy 中的角色 | 仅作"商业模式假设"一阶的轻量框架，与其他三框架并列可选 | 不涉及，专注 BMC 深化 |

- `pm-strategy` 是"战略分析套件"，按四阶路径选框架组合，商业模式只是其中一阶且可跳过。
- `pm-businessmodel` 是"商业模式画布"的专项深化，输出 9 模块 + 业务游戏分类 + 收入/成本结构，深度远超 Lean Canvas 一阶。
- 合并会使 `pm-strategy` 同时承担"四框架战略分析"与"9 模块 BMC 深化"两套异构产物，违反单一职责。

## 后果

- 维护两套技能，但各自产物边界清晰，调用方按"要战略选择还是要商业模式画布"自然命中。
- 若未来 Lean Canvas 一阶与 BMC 出现产物级冲突，再行复审。
