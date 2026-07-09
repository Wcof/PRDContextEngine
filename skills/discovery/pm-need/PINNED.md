# PINNED — /pm-need

> 绝不可被稀释的核心约束（供运行时置顶加载）。冗长示例见 references/。

1. 生成任何 PMContext JSON 之前必须先做输入信息熵自检（Step 0.5，--auto 强制）
2. 高熵输入且无任何背景源时必须举手反问，禁止直接生成 PMContext
3. 单一事实源是**配置块声明的 PMContext 路径**（默认 `docs/pm-context/pm-context.md`，以 `## PMSkill` 块的 `产物目录` 项为准），PRD/草图均为其下游 View
4. `--auto` 零确认：PM 零介入，未补全维度全标 `[待确认]` 记入信息缺口
5. 失败子 skill 不回滚已落盘部分，失败项单独标注
6. PMContext 已存在时进入增量模式必须先做 Argument-first 路由，先看本次用户输入是新增/调整/补全，不能只扫标记后静默退出
7. 增量成功后默认 Downstream Fan-out 刷新 PRD/stories/sketch prototype/summary；只有 `--context-only` 才跳过下游 View
8. `/pm-need --auto` 末尾必须调用 `/pm-summary --auto`，把散件文档合并成 5 份汇总文档
