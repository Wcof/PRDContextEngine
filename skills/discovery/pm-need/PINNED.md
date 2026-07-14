# PINNED — /pm-need

> 绝不可被稀释的核心约束（供运行时置顶加载）。冗长示例见 references/。

1. 生成任何 PMContext JSON 之前必须先做输入信息熵自检（Step 0.5，--auto 强制）
2. `--auto` 高熵且无背景源时不得暂停或追问；继续纯推断，未知维度全标 `[待确认]`、低置信度并记入信息缺口
3. 单一事实源是**配置块声明的 PMContext 路径**（默认 `docs/pm-context/pm-context.md`，以 `## PMSkill` 块的 `产物目录` 项为准），PRD/草图均为其下游 View
4. `--auto` 零确认：PM 零介入，未补全维度全标 `[待确认]` 记入信息缺口
5. 失败子 skill 不回滚已落盘部分，失败项单独标注
6. PMContext 已存在时进入增量模式必须先做 Argument-first 路由，先看本次用户输入是新增/调整/补全，不能只扫标记后静默退出
7. 增量成功后默认 Downstream Fan-out 刷新 PRD/stories/sketch prototype/summary；只有 `--context-only` 才跳过下游 View
8. `/pm-need --auto` 末尾必须调用 `/pm-summary --auto`，再运行 `python3 hooks/post_generation.py --skill pm-need --artifact-root <产物目录> --auto`；Hook 非零不得标完成
9. `--auto` 调起任何 subagent/Task/parallel agent 时，必须注入 **PMSkill Runtime Capsule**：根级 `CONTEXT.md`/Agent 规则、调用方 `SKILL.md+PINNED.md`、目标 skill `SKILL.md+PINNED.md`、产物目录/stamp、PMContext 路径、输入产物、输出契约、硬门、失败策略；子 agent 不得依赖父会话记忆或软性口头描述
10. `pm-sketch`/Pencil 子任务必须额外注入 `prototype-content-plan.json`、`prototype-design-profile.json`、已解析的设计事实源、token/component 覆盖门；无法注入则禁止并行，回到父 agent 串行执行或本地 fallback
