# PINNED — /pm-sketch

> 绝不可被稀释的核心约束（供运行时置顶加载）。冗长示例见 references/。

1. 输入仅读 PMContext，草图节点必须对应 PMContext 中的页面/功能/步骤
2. 三段实现门：Pencil MCP 优先（create/update + export/persist）→ Simple 本地模式（CDN 单 HTML，L3，< 280KB）→ Scaffold 本地模式（React+TS+Vite+Tailwind v4，L4）
3. DESIGN.md 是视觉事实源（可选），与 PMContext 冲突时标 `[冲突]` 不强行收敛
4. 生成后必须跑对应验收级别（V1/V2/V3），未验收不得打 ✅
5. 产物落盘到**配置块声明的产物目录下的 `sketch/`**（默认 `docs/pm-context/sketch/`，以 `## PMSkill` 块的 `产物目录` 项为准）
6. `--prototype` 必须先写 `sketch/prototype-content-plan.json`，后续页面只能从该内容计划渲染；禁止只输出路由/菜单/空 section
7. `--prototype` 必须读取 `references/design-style.md` 并写 `sketch/prototype-design-profile.json`，用于约束 Pencil MCP / Simple / Scaffold 的视觉风格与 UE
8. 每个原型页面必须有 `data-trace-page` 与 ≥3 个 `data-trace-ref` 业务元素，并通过路由空壳检测
9. Pencil MCP 命中时必须把 `prototype-content-plan.json` + `prototype-design-profile.json` 一并传给 MCP；失败/不可用必须写 fallback-local 并回退本地技术栈
