# pm-need 自动增量 + pm-sketch 技术栈硬门 + pm-aiprd 承接 §8

AiGateway 事故暴露两处失守：①`pm-need` 缺更新机制——`--incremental` flag 存在但需用户显式记，Agent 自造此 flag 写进 report 但下游不认，PMContext 已存在时还问"是否覆盖"打断增量；②Agent 偷懒自降级——PMContext §8 明写 Vue 3 + Vite，但 pm-aiprd 没承接 §8，pm-sketch 顺势降到简单模式 HTML 壳子，report 还自吹"✅ 原型完成"系统性撒谎。

决定三件事：

1. **pm-need 删 `--incremental` flag，入口自动判 0→1 vs 增量**——扫产物目录，`pm-context.md` 不存在或为空 = 0→1 全链路；存在且非空 = 增量模式。增量仅扫 `[待确认]` `[假设]` `[冲突]` 标记段 + 信息缺口段重跑 collect/refine，已确认段 Frozen 不动；合并必须内联调 `/pm-conflict-resolver`（PMContext 差分修改唯一合法主体），resolver 仅改有标记段硬保 Frozen。用户 `$ARGUMENTS` 显式指 `--update §8` / `--update GAP-01` = 定点增量。

2. **pm-aiprd 承接 §8 转写硬约束**——Instructions checklist 加「技术栈硬约束转写」步骤：扫 PMContext §8 若含前端框架声明，转写为 AI PRD 的「技术栈契约」段，从 PMContext 的"建议"升格为 Agent 必须遵守的硬约束。反例表加「§8 有前端框架声明但 ai-prd 未承接 = Failure」。

3. **pm-sketch 加 Step -0.5 技术栈硬门**——先于 Step -1 跑，扫 PMContext §8 命中前端框架声明清单（Vue/React/Next/Nuxt/Svelte/Angular/Electron，或 Vite+TypeScript 同时出现）即硬触发 Scaffold，跳过 Step -1 简单信号判断；`--simple` flag 此场景视为无效仍走 Scaffold（防 Agent 自降级）。样式工具（Tailwind/UnoCSS/Less/Sass）单独出现不触发。反例表加降级禁止行。

前端框架声明清单范围经盘问钉死：`Vue` `React` `Next` `Nuxt` `Svelte` `Angular` `Electron`（单独出现即触发）+ `Vite`+`TypeScript` 组合信号。样式工具不触发——CDN 也能用，不构成工程化诉求。

CONTEXT.md 增三条术语：`PMContext Frozen 段` / `pm-need 入口判据` / `技术栈硬约束`，单真源不变。
