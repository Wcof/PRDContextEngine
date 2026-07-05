# PINNED — /pm-sketch

> 绝不可被稀释的核心约束（供运行时置顶加载）。冗长示例见 references/。

1. 输入仅读 PMContext，草图节点必须对应 PMContext 中的页面/功能/步骤
2. 双模式：简单模式（CDN 单 HTML，L3，< 280KB）/ Scaffold 模式（React+TS+Vite+Tailwind v4，L4）
3. DESIGN.md 是视觉事实源（可选），与 PMContext 冲突时标 `[冲突]` 不强行收敛
4. 生成后必须跑对应验收级别（V1/V2/V3），未验收不得打 ✅
5. 产物落盘到**配置块声明的产物目录下的 `sketch/`**（默认 `docs/pm-context/sketch/`，以 `## PMSkill` 块的 `产物目录` 项为准）
