# 过程文档索引（Process Artifacts）

本目录记录 PMSkill 全链路的过程产物，供 PM 事后审计。阅读顺序：

1. `01-collect-understand.md` — 问题重构 + 四源材料聚合
2. `02-refine-model.md` — 领域模型（实体/关系/不变量）
3. `03-refine-options.md` — 方案候选（激进 vs 保守）
4. `04-refine-tradeoff.md` — 决策表（选了什么/为什么/代价）
5. `05-premortem-risk.md` — 风险清单 + Tiger 三分 + 行动计划
6. `06-*-delivery.md` / `06-sketch-*.md` — 交付物与图元追溯
7. `conflict-log.json` — 局部退火差分修复日志（由 `/pm-conflict-resolver` 写入）

历史版本归档在 `.archive/<timestamp>/`（不进版本库）。纯技术缓存在 `../.cache/`（断点续跑 JSON 分片，不进版本库，重跑时清空）。

> 显性化背景见 [../../adr/0016-explicit-process-artifacts.md](../../adr/0016-explicit-process-artifacts.md)。
