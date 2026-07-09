# PINNED — /pm-refine

> 绝不可被稀释的核心约束（供运行时置顶加载）。冗长示例见 references/。

1. 8 维推断全覆盖，P0（用户场景/边界/冲突）三维必须有结论
2. 每项标注四态之一：事实 / `[假设]` / `[待确认]` / `[冲突]`
3. 置信度 < 8 一律标 `[假设]`；无来源的项自动标 `[假设]`
4. --auto 模式 PM 零介入，未补全维度标 `[待确认]` 不臆造
5. PMContext 落盘到**配置块声明的产物目录下的 `pm-context.md`**（默认 `docs/pm-context/pm-context.md`，以 `## PMSkill` 块的 `产物目录` 项为准），单文件自包含
6. 追问模式必走 Step 0 建决策依赖树（落 `process/02-refine-deps-tree.md`），按拓扑序问不按 P0→P1→P2 固定序
7. 追问过程术语随问随记 `process/02-refine-glossary.md`（只记 PM 已确认版，含推断痕迹）
