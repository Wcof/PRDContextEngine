# ADR 0019: 原型设计风格 Profile 与 Pencil MCP Brief 强化

## Status

Accepted

## Context

`/pm-sketch --prototype` 已经有 Pencil MCP 优先门、`prototype-content-plan.json` 反空壳门和本地 Simple/Scaffold fallback。但运行中仍可能出现两类问题：

1. 即使页面内容不空，视觉与 UE 仍容易回到模型默认模板：紫蓝渐变、毛玻璃、三张空卡片、所有页面长得一样。
2. Pencil MCP 命中时，如果 brief 只传页面清单而不传视觉与 UE 契约，MCP 可能生成“有 screen 但没有 PM 产品气质”的泛化原型。

用户希望内置类似 `Leonxlnx/taste-skill` 的设计风格增强能力，用于提高原型系统的样式和 UE，但 PMSkill 的适用场景包含多页产品原型、后台、AI Native 系统和仪表盘，不能直接把偏营销页/作品集的外部 skill 作为执行源。

## Decision

新增 `skills/visualization/pm-sketch/references/design-style.md`，作为 PMSkill 自有的视觉/UE 增强协议。

`/pm-sketch --prototype` 新增 **Step -0.85 设计风格编译门**：

1. 读取 PMContext、DESIGN.md 和用户显式风格要求。
2. 输出一行 Design Read。
3. 写 `docs/pm-context/sketch/prototype-design-profile.json`，包含：
   - `style_family`
   - `secondary_style`
   - 三拨盘：`design_variance` / `motion_intensity` / `visual_density`
   - `tokens`
   - `layout_patterns`
   - `interaction_patterns`
   - `anti_patterns_banned`
4. Pencil MCP 模式必须把 `prototype-content-plan.json` 与 `prototype-design-profile.json` 一并传入 brief，并在 manifest 中记录 `design_profile` / `style_family` / `ue_coverage`。
5. Simple 模式把 profile 转为 `:root` / dark token 和页面布局骨架。
6. Scaffold 模式把 profile 转为 `src/style.css` token、组件布局和 UE 规则。

同步修正 `pm-sketch/PINNED.md`：运行时置顶约束从“Simple/Scaffold 双模式”更新为“Pencil MCP 优先 + 本地 Simple/Scaffold fallback + design profile 必填”。

## Consequences

- Pencil MCP 的设置确认不再只存在于长文 SKILL.md，也进入 PINNED、模板、eval、validator。
- 视觉质量从软提示变成可检查的结构产物。
- `prototype-content-plan.json` 解决“有没有内容”，`prototype-design-profile.json` 解决“是否像一个有审美和 UE 的产品原型”。
- 外部 taste-skill 作为方法论参考，不作为 vendored dependency；PMSkill 可离线运行，避免外部 repo 变化导致漂移。

## Validation

`scripts/validate_pmskill.py` 新增检查：

- `pm-sketch/SKILL.md` 包含 Step -0.85、design-style、prototype-design-profile、design_profile。
- `prototype-templates.md` 包含 Design Style Profile、`{{DESIGN_PROFILE}}`、Pencil MCP manifest 设计字段。
- `references/design-style.md` 包含 Design Read、三拨盘、AI Native Dark、Pencil MCP brief、ue_coverage。
- `pm-sketch/PINNED.md` 包含 Pencil MCP 优先、prototype-content-plan、prototype-design-profile、fallback-local。
