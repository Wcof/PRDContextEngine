# Engine Skills hidden from default discovery via metadata.internal

`npx skills@latest add` 的发现器（vercel-labs/skills `parseSkillMd`）扫文件树枚举所有 `SKILL.md`，与 `.claude-plugin/plugin.json` 的 `skills` 数组无屏蔽耦合——数组只追加搜索起点，不反向隐藏未列项。导致一键安装时 51 个 skill 全暴露在斜杠菜单，违背"使用的 skill 只有部分"的产品意图。

决定：给 46 个 Engine Skill 的 `SKILL.md` frontmatter 加 `metadata.internal: true`。发现器遇此标记且未设 `INSTALL_INTERNAL_SKILLS=1` 时直接返回 null，skill 不进发现列表。engine 调用走 `use_skill` 工具按 name 直读 SKILL.md，不经过发现器，故不受影响——这正是"对用户斜杠可见的缩减，但不影响 engine 调用"的零成本收敛点。

User-facing 名单收敛到 6 个可见入口：`pm-setup` / `pm-need` / `pm-prd` / `pm-sketch` / `pm-premortem` / `pm-summary`。其中 `pm-setup` / `pm-need` 是 Human-only Entry；`pm-prd` / `pm-sketch` / `pm-premortem` / `pm-summary` 是 Hybrid Entry，既能被 `pm-need --auto` 等链路编排，也能被人类单独 `/触发` 增量更新产物——前置缺失时告知空产物不静默撒谎，故仍 User-facing。其余 46 个（含 `pm-collect` / `pm-refine` / `pm-aiprd` / `pm-humanprd` / `pm-wireframe` / `pm-ia` / `pm-state` / `pm-flow` / `pm-journey` / `pm-conflict-resolver` 等链路中转，及 `pm-okr` / `pm-roadmap` / `pm-sprint` / `pm-sql` 等专业产物）皆 Engine，由 AI 按语义自主 `use_skill` 调起。

同步 `.claude-plugin/plugin.json` 和 `.codex-plugin/plugin.json` 的 `skills` 数组到这 6 个，与收敛结果对齐，避免 marketplace 渠道错配误导后人。编排关系仍由 `CONTEXT.md` 的 Skill 调用关系表单点维护，frontmatter 不重复写 `orchestrated-by`，避免双真源漂移。
