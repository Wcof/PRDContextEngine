# ADR 0013：pm-metrics 与 pm-northstar 确认为递进关系，保留并存

- 状态：Accepted
- 日期：2026-07-04
- 决策者：PMSkill 整改复审（奥卡姆剃刀轮）

## 背景

`pm-metrics` 与 `pm-northstar` 都产出"北极星指标 + Input Metrics 星座"，疑似重复。

## 决策

**确认是递进关系而非重复，保留两者。**

## 理由

| 维度 | pm-metrics | pm-northstar |
|------|-----------|--------------|
| 定位 | 北极星指标的"首次提炼" | 北极星指标的"深化" |
| 触发时机 | PMContext 尚无北极星时，从 0 到 1 提炼 | 已有北极星雏形，需深化校验 + guardrail + 指标树 |
| 产物 | 北极星 + Input Metrics 星座 + 分类业务游戏 + 七准则校验 + 指标树 Mermaid | 深化北极星 + 3-5 input metric 星座 + guardrail 健康指标 + 指标树 |
| 关键差异 | 侧重"提炼与首次校验" | 侧重"深化、加 guardrail、对照 PMContext 价值验证度量" |

- 二者输出形态相似，但职责是同一指标体系的"建立"与"深化"两个阶段。
- `pm-metrics` 偏从 0 到 1（提炼 + 首校验），`pm-northstar` 偏从 1 到 N（深化 + guardrail + 与价值验证度量对齐）。

## 后果

- 维护两套技能，调用方按"是否已有北极星雏形"自然命中。
- 未来若产物模板出现实质重叠，可考虑将 `pm-northstar` 作为 `pm-metrics` 的 `--deepen` 子模式收编；当前阶段保持独立以保留递进语义。
