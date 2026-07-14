# PINNED — /pm-sketch

> 绝不可被稀释的核心约束（供运行时置顶加载）。冗长示例见 references/。

1. 输入仅读 PMContext，草图节点必须对应 PMContext 中的页面/功能/步骤
2. 三段实现门：Pencil MCP 优先（create/update + export/persist）→ Simple 本地模式（CDN 单 HTML，L3，< 280KB）→ Scaffold 本地模式（React+TS+Vite+Tailwind v4，L4）
3. 视觉事实源必须先解析：`--design <path>`、`docs/design/DESIGN.md`、`docs/design/**`、`docs/designs/**`、`Designs/**`、`design-system/**`、`style-guide/**` 中命中的规范均可作为设计事实源；用户显式提到 Designs/设计规范时，找不到必须标失败或请求补源，不得静默回退默认审美
4. 生成后必须跑对应验收级别（V1/V2/V3）与 `python3 hooks/post_generation.py --skill pm-sketch --artifact-root <产物目录>`，任一非零不得打 ✅
5. 产物落盘到**配置块声明的产物目录下的 `sketch/`**（默认 `docs/pm-context/sketch/`，以 `## PMSkill` 块的 `产物目录` 项为准）
6. `--prototype` 必须先写 `sketch/prototype-content-plan.json`，后续页面只能从该内容计划渲染；禁止只输出路由/菜单/空 section
7. `--prototype` 必须读取 `references/design-style.md` 并写 `sketch/prototype-design-profile.json` + `sketch/design-source-manifest.json`；profile 必须包含具体 token、组件规则、布局蓝图与禁用项，而不只是抽象 style_family
8. 每个原型页面必须有 `data-trace-page` 与 ≥3 个 `data-trace-ref` 业务元素，并通过路由空壳检测
9. Pencil MCP 命中时必须把 `prototype-content-plan.json` + `prototype-design-profile.json` + `design-source-manifest.json` + token/component contract 一并传给 MCP；manifest 必须记录 `token_digest`、`component_coverage`、`design_violation_count`、`ue_coverage`，未达标必须重试或 fallback-local
10. `--prototype` 必须执行视觉可见性审计：生成 `sketch/visual-audit-report.json`，检查文字/背景、按钮文字/按钮底色、导航/表格/卡片等关键色彩对比；出现“字体颜色≈背景色”“可点击元素不可见”“opacity/display 导致不可见”时判 Failure，不得打 ✅
