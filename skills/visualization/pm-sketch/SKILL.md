---
name: pm-sketch
description: 从 PMContext 生成全部草图（线框/信息架构/状态机/流程图/客户旅程）+ 交互原型（--prototype）。若 runtime 提供 Pencil MCP，优先用 Pencil MCP 生成/更新原型系统；否则回退原有 Simple/Scaffold 技术栈。支持 --auto 零确认模式与单图模式（--wireframe/--ia/--state/--flow）。Use when generating sketches or prototypes from PMContext, or the user mentions 草图、sketch、线框、原型、可视化、prototype、交互原型、Mermaid、Pencil MCP.
---

# /pm-sketch

> 核心约束见 PINNED.md（供运行时置顶加载）

> 你是一位资深产品设计师，PMContext 已在手。你的任务是把 PMContext 中的页面定义、状态转移、流程步骤，变成**看得见的草图**——**所有草图的"追光灯"必须照回 PMContext，不可凭空增删页面/状态/流程。** Mermaid 图让团队快速理解，交互原型让用户直接体验；若 Pencil MCP 可用则优先交给 Pencil MCP 实现原型系统，否则走本 skill 原有技术栈。

从 PMContext 生成全部可视化物。支持两种产出模式：
- **Mermaid 草图** — 线框、信息架构、状态机、流程图、客户旅程图，写入 `sketch/*.md`
- **交互原型**（`--prototype`）— 优先 Pencil MCP；无可用 Pencil MCP 时回退 Simple/Scaffold 本地技术栈（简单模式 CDN 单 HTML / Scaffold 模式 React + TS + Vite + Tailwind v4 工程）

## Purpose

从 PMContext 生成全部可视化物：Mermaid 草图 + 交互原型。`--prototype` 先执行 Pencil MCP 实现门：可用则用 Pencil MCP 生成/更新原型系统；不可用或失败则回退原有 Simple/Scaffold 本地技术栈。草图是 PMContext 的 View——每个图元必须可追溯到 PMContext 事实项。Scaffold 模式对齐 Axhub-Make `beginner-guide` 工程级实物水准，含 V2/V3 验收闭环。

## Context

PMContext 已沉淀页面定义、状态转移、流程步骤。本 skill 将这些转化为看得见的草图。**原型实现三段门**：
- Pencil MCP 模式：runtime 暴露可用 Pencil MCP 且具备创建/更新/导出/持久化能力时，优先用 MCP 生成原型系统
- 设计风格增强门：所有原型实现前读取 `references/design-style.md`，写 `sketch/prototype-design-profile.json`，把风格家族、视觉拨盘、token、布局/UE 约束注入 Pencil MCP / Simple / Scaffold
- 简单模式（CDN HTML）：无 Pencil MCP 时，已有代码项目自动检测技术栈，新项目推荐当前流行技术栈
- Scaffold 模式（Vite 工程）：无 Pencil MCP 时，固定 React + TS + Vite + Tailwind v4，对齐 Axhub-Make `beginner-guide` 工程级实物水准

## Instructions

读取 `<产物目录>/pm-context.md`（先读 Agent 规则文件中 `## PMSkill` 块取 `产物目录`，块不存在回退默认 `docs/pm-context/`）。**stamp 互校**：若 `<产物目录>/.pmskill-setup.stamp` 存在且 `pmcontext_exists: false`，提示"stamp 显示 PMContext 未生成但文件已存在——以文件为准"。若不存在：
- 如果有 `$ARGUMENTS` → 自动调用 `/pm-need $ARGUMENTS` 全链路后回到草图生成
- 如果没有 → 🔴 STOP：提示先运行 `/pm-need`

- [ ] PMContext 已读取且非空
- [ ] 页面定义/状态转移/流程步骤/实体关系全部提取
- [ ] 调用 /pm-wireframe 生成线框图
- [ ] 调用 /pm-ia 生成信息架构图
- [ ] 调用 /pm-state 生成状态机图
- [ ] 调用 /pm-flow 生成流程图
- [ ] 调用 /pm-journey 生成客户旅程图（与流程图同源，刻画跨页面/跨状态的用户动线）
- [ ] `--prototype` 前已完成 Pencil MCP 实现门（Step -0.75），不可用时才进入本地模式判断（简单/Scaffold，Step -1）
- [ ] Pencil MCP 模式：已写 manifest + 导出/保存结果；本地简单模式：技术栈决策完成（新项目推荐 / 老项目检测）；本地 Scaffold 模式：固定 React + TS + Vite + Tailwind v4
- [ ] 已读取 `references/design-style.md` 并写入 `sketch/prototype-design-profile.json`；Pencil MCP brief / Simple CSS / Scaffold style.css 均已消费该视觉 profile
- [ ] DESIGN.md 派生 Token 已生成（存在则派生，不存在回退默认）
- [ ] [假设] 图元显式标注不伪装为确认设计
- [ ] 每个图元可追溯到 PMContext 事实项
- [ ] Pencil MCP 模式必须完成导出/保存验收；Scaffold 模式生成后必须运行验收（V2/V3），不静默撒谎

## Thinking Protocol

本 Skill 承载 PM Thinking Loop 的步骤 6（交付）的草图编排职责：

| 步骤 | 本 Skill 的职责 | 产出（是否回灌 PMContext） |
|------|---------------|--------------------------|
| 6. 交付（草图） | 编排 5 个子 Skill 生成全部草图（IA/State/Flow/Wireframe/Journey），确保每个图元追溯到 PMContext 实体/关系 | 不回灌（产出 View） |

执行时依次调用 /pm-ia → /pm-state → /pm-flow → /pm-wireframe → /pm-journey。子 Skill 各自写入 `process/` 中间工件。

**产出约束**：
- 每个图元必须对应 PMContext 中的实体/关系，无法对应的标 `[假设]`
- 步骤 5 的 Launch-Blocking Tiger 涉及的实体必须在草图中有对应图元
- 必须产出**草图交付物清单**：5 个 Mermaid 文件路径 + [假设] 图元数 + 未覆盖 Tiger 实体数
- 交互原型（--prototype）：优先 Pencil MCP，失败/不可用才走本地双模式；三种实现都必须先消费 `prototype-content-plan.json` 与 `prototype-design-profile.json`——
  - Pencil MCP 模式：用 MCP 创建/更新原型系统，写 `sketch/pencil/pencil-prototype-manifest.json`，必须有页面覆盖、交互覆盖、导出/持久化证明、design_profile 记录
  - 简单模式：CDN 单 HTML < 280KB（超限自动拆分懒加载），L3 交互，V1 验收
  - Scaffold 模式：React + TS + Vite + Tailwind v4 工程，L4 交互，V2/V3 验收，无体积上限

**依赖检查**：是否有未追溯到 PMContext 的图元？步骤 5 的 Tiger 实体是否在草图中覆盖？交互原型是否通过质量清单（Pencil MCP 导出/持久化、或本地 V1/V2/V3）？

## 启动模式

```
/pm-sketch                         → 正常模式：出全部五种 Mermaid 草图，停在审计门
/pm-sketch --prototype             → 交互原型（先查 Pencil MCP；有则用 MCP，无则自动判断简单/Scaffold；Step -0.5 命中前端框架声明时硬触发 Scaffold）
/pm-sketch --prototype --simple    → 强制简单模式（CDN 单 HTML < 280KB）——**仅当 PMContext §8 无前端框架声明时有效**；§8 含 Vue/React/Next/Nuxt/Svelte/Angular/Electron 或 Vite+TypeScript 时此 flag 视为无效，仍走 Scaffold（防 Agent 自降级）
/pm-sketch --prototype --scaffold  → 强制本地 Scaffold 模式（React + TS + Vite + Tailwind v4 工程；若 Pencil MCP 可用仍优先 Pencil，除非加 --no-mcp）
/pm-sketch --prototype --rebuild      → 全量重生成原型（覆盖已有页面，非 --auto 时需确认）
/pm-sketch --prototype --no-mcp     → 跳过 Pencil MCP 检查，强制走原有本地技术栈（Simple/Scaffold）
/pm-sketch --prototype --dark      → 暗色主题（覆盖 prefers-color-scheme 检测，仅 --prototype 模式下有效）
/pm-sketch --prototype --design <path> → 指定 DESIGN.md 路径（视觉事实源，默认扫描 docs/design/DESIGN.md）
/pm-sketch --prototype --auto      → 自动模式：pm-need → premortem → PRD → 原型 零确认一气呵成
/pm-sketch --wireframe             → 只出线框图
/pm-sketch --ia                    → 只出信息架构图
/pm-sketch --state                 → 只出状态机图
/pm-sketch --flow                  → 只出流程图
/pm-sketch <需求描述>              → 自动模式：从需求描述开始全链路到草图
```

## 流程

### 1. 读取 PMContext + 建立 Entity Dictionary

读取 `<产物目录>/pm-context.md`，提取：
- 用户场景与目标
- 所有页面/功能定义（事实、规则、验收）
- 实体/关系定义
- 状态与状态转移
- 流程与步骤

**Entity Dictionary（实体映射表，防止跨图名词混淆）**：

> 不同子 Skill（IA/Flow/State/Wireframe）各自绘图时，容易把同一实体写成不同名字（IA 用 "User"、Flow 用 "End User"、State 用 "Account"）——导致跨图对照困难。本步建立全局实体映射表，所有子 Skill 必须使用映射表中的规范名。

扫描 PMContext，提取所有名词实体建立 `UUID-Entity` 映射，写入 `docs/pm-context/sketch/entity-dictionary.md`：

```markdown
| UUID | 规范名 | PMContext 来源 | 同义词（禁用） | 类型 |
|------|--------|-------------|--------------|------|
| E001 | User | 用户场景段 | End User/Account/用户 | 实体 |
| E002 | Order | 实体关系段 | 订单/订单记录 | 实体 |
| E003 | 支付流程 | 流程段 | 付款/结算 | 流程 |
```

**纪律**：
- 所有子 Skill 必须读 `entity-dictionary.md` 后再绘图，使用规范名
- 若子 Skill 发现 PMContext 中出现新实体（不在字典中）→ 加新行 + 标 `[待补充]`
- 禁止在图中使用同义词列中的禁用名（如禁用 "End User"，必须用 "User"）
- Entity Dictionary 是子 Skill 的**前置依赖**，不读字典直接绘图=违规

若 PMContext 不存在且 `$ARGUMENTS` 不为空 → 自动调用 `/pm-need $ARGUMENTS` → 完成后继续。

### 2. 生成草图

#### 模式 A：Mermaid 草图（默认）

Run 五个子 Skill（按依赖顺序）：
1. `/pm-ia` → 信息架构：实体/页面关系
2. `/pm-state` → 状态机：状态转移
3. `/pm-flow` → 流程：步骤与分支
4. `/pm-wireframe` → 线框：页面布局
5. `/pm-journey` → 客户旅程：跨页面/跨状态的用户动线

若 PMContext 中没有页面定义，信息架构图以实体关系为主体，跳过线框。

#### 模式 B：交互原型（`--prototype`）

先执行内容与视觉编译门（见 Step -0.9 / Step -0.85），再执行 Pencil MCP 实现门（见 Step -0.75）。若 Pencil MCP 可用，生成/更新 `docs/pm-context/sketch/pencil/`；若不可用或失败，再根据 PMContext 复杂度自动判断本地输出模式（见 Step -1）：

- **Pencil MCP 模式**：通过 MCP 创建/更新原型系统，输出 `docs/pm-context/sketch/pencil/` + `pencil-prototype-manifest.json`
- **简单模式 (Simple / CDN 模式)**：单 HTML，CDN 引框架，L3 交互，< 280KB。输出 `docs/pm-context/sketch/prototype.html`
- **Scaffold 模式**：可运行前端工程脚手架（React + TS + Vite + Tailwind v4），L4 交互，无体积上限，纯前端 mock。输出 `docs/pm-context/sketch/prototype/`

**Step -0.9：原型内容编译门（--prototype 模式专用，先于 MCP/本地实现跑）**

目标：先把 PMContext 编译成可渲染的页面内容计划，避免模型只生成 hash 路由/菜单/空 section。DeepSeek/长指令模型尤其容易忘业务内容，本门把「要画什么」固化为数据契约，再进入 Pencil MCP / Simple / Scaffold 实现。

**必须写入** `<产物目录>/sketch/prototype-content-plan.json`：

```json
{
  "source": "pm-context.md",
  "mode": "content-plan",
  "pages": [
    {
      "heading": "<PMContext ## heading>",
      "page_id": "<kebab-id>",
      "primary_job": "<本页用户要完成的核心任务>",
      "scenario": "<用户场景原文或推断>",
      "facts": ["<事实字段/数据/角色>"],
      "rules": ["<业务规则，必须可见渲染>"],
      "acceptances": ["<验收标准，必须可见渲染>"],
      "fields": [{"name": "<表单/表格字段>", "source": "<PMContext 锚点>"}],
      "actions": [{"label": "<可点击动作>", "effect": "<状态变化/跳转>", "source": "<flow/state/验收锚点>"}],
      "states": ["loading", "empty", "success", "error"],
      "trace_refs": ["<PMContext heading/rule/acceptance anchor>"]
    }
  ],
  "global_constraints": ["<全局约束>"],
  "unmapped_items": ["<无法映射的 PMContext 项，标 [待确认]>"]
}
```

**编译硬门**：
- 页面数必须等于 PMContext `## <页面/功能>` heading 数；无法解析的 heading 写入 `unmapped_items`，不得丢弃。
- 每页必须至少有 `primary_job`、`scenario`、`rules`、`acceptances`、`actions` 五类信息；缺失则从 PMContext 相邻段推断并标 `[假设]`，仍不得留空。
- 每页至少 1 个 action，且 action 必须有明确 effect（跳转、状态切换、表单提交、筛选、展开、错误恢复之一）。
- 后续所有实现都只能从 `prototype-content-plan.json` 渲染页面；不得另起一套路由清单。

输出：`✅ 原型内容编译: 页面 <N> / 规则 <R> / 验收 <A> / 动作 <K> | 未映射 <M>`。若 N=0 或任一页面完全无规则/验收/动作，禁止进入实现，先回修 PMContext 或把缺口标 `[待确认]`。

**Step -0.85：设计风格编译门（--prototype 模式专用，先于 Pencil MCP/本地实现跑）**

目标：把 PMContext 与 DESIGN.md 编译成稳定的视觉与 UE 契约，降低模型输出“普通、丑、套模板、空卡片”的概率。此门内置 `references/design-style.md`，参考 anti-slop frontend skill 的“先读场景再定风格”思想，但面向 PMSkill 的多页产品原型，不依赖外部 repo 或联网。

**必须读取** `skills/visualization/pm-sketch/references/design-style.md`，并写入 `<产物目录>/sketch/prototype-design-profile.json`：

```json
{
  "mode": "prototype-design-profile",
  "design_read": "设计读取：这是面向 <用户/场景> 的 <产品类型>，采用 <视觉语言>，倾向 <布局/组件体系>。",
  "style_family": "Enterprise Calm | AI Native Dark | Data Cockpit | Premium Consumer | Trust First | Developer Tool",
  "secondary_style": "<最多一个辅助风格，没有则为空>",
  "dials": {"design_variance": 1, "motion_intensity": 1, "visual_density": 1},
  "tokens": {
    "theme": "light | dark | auto",
    "accent": "<单一主强调色语义名>",
    "radius_scale": "<sm-md | md-lg | sharp>",
    "shadow_style": "<flat | soft | layered>",
    "type_scale": "<compact-product | editorial | data-dense>",
    "spacing_scale": "<4px | 8px | 12px grid>"
  },
  "layout_patterns": ["<每类页面采用的布局骨架>"],
  "interaction_patterns": ["<反馈/错误恢复/审计/抽屉/命令面板等 UE 模式>"],
  "anti_patterns_banned": ["empty route shell", "random purple glow", "fake screenshot div"]
}
```

**风格硬门**：
- 必须先输出一行 Design Read，再生成任何原型代码或 Pencil MCP brief。
- 主风格家族只能有一个，辅助风格最多一个；禁止一页一个风格。
- 三个拨盘必须有 1-10 数值，并与产品类型/用户场景对应。
- `prototype-design-profile.json` 必须被三种实现消费：
  - Pencil MCP：作为 brief 输入，并写入 manifest 的 `design_profile`、`style_family`、`ue_coverage` 字段。
  - Simple：作为 `:root` / `[data-theme=dark]` token 和页面布局选择来源。
  - Scaffold：作为 `src/style.css` token、页面组件布局、motion/reduced-motion 策略来源。
- 视觉增强不得覆盖追溯要求：每页仍必须从 `prototype-content-plan.json` 渲染规则/验收/动作，并保留 `data-trace-ref` 或 manifest source。
- 禁止默认审美：随机紫蓝渐变、全页毛玻璃、三张等宽空卡、假截图矩形、只有标题图标的一句话卡片。

输出：`✅ 设计风格: <style_family> | 拨盘 <variance>/<motion>/<density> | profile: <产物目录>/sketch/prototype-design-profile.json`。

**Step -0.75：Pencil MCP 实现门（--prototype 模式专用，先于 Step -0.5 跑）**

目标：当 runtime 已接入 Pencil MCP 时，用 MCP 生成/更新原型系统；否则保持原有 Simple/Scaffold 技术栈不变。

**检测顺序**：
1. 若 `$ARGUMENTS` 含 `--no-mcp` → 跳过 MCP 检查，输出 `⏭️ Pencil MCP: 用户显式 --no-mcp → 使用本地技术栈`，继续 Step -0.5。
2. 查看当前 runtime 暴露的工具/能力清单（MCP servers / tools / namespaces）。大小写不敏感匹配以下任一信号：
   - server/name/namespace 含 `pencil`
   - tool 名含 `pencil` 且能力含 `create` / `update` / `render` / `export` / `prototype` / `wireframe` 任一
   - tool namespace 形如 `mcp__pencil__*`、`pencil.*`、`pencil_*`
3. 仅当 Pencil MCP 同时具备**创建或更新**与**导出或持久化**能力时，判为可用；只有只读/查询能力时视为不可用，继续本地技术栈。
4. 若 runtime 不提供工具清单或 Agent 看不到 MCP 能力，不得假装已检测到；输出 `⚠️ Pencil MCP: 未暴露工具清单/未检测到 → 使用本地技术栈`。

**Pencil MCP 命中后的执行协议**：
- 仍然先生成 5 类 Mermaid 草图与 Entity Dictionary；Pencil MCP 只替代 `--prototype` 的原型实现，不替代 PMContext、PRD、草图追溯。
- 将以下输入打包给 Pencil MCP：`prototype-content-plan.json`、`prototype-design-profile.json`、PMContext 页面清单、Entity Dictionary、状态/流程/旅程摘要、PRD_DATA、DOC_DATA、DESIGN.md token、`[假设]`/`[待确认]`/`[冲突]` 标记。
- 用 Pencil MCP 创建或更新原型系统，要求每个 PMContext 页面至少一个可导航 screen，每条关键状态转移至少一个可点交互，每条规则/验收有可见表达。
- 导出或保存到 `<产物目录>/sketch/pencil/`；若 MCP 返回远端 artifact id，也必须写本地 manifest，不得只在对话里报一个 id。
- 写 `<产物目录>/sketch/pencil/pencil-prototype-manifest.json`：

```json
{
  "mode": "pencil-mcp",
  "server": "<detected pencil mcp server/tool>",
  "inputs": ["pm-context.md", "entity-dictionary.md", "prd/ai-prd.md", "prd/human-prd.md", "docs/design/DESIGN.md?", "sketch/prototype-content-plan.json", "sketch/prototype-design-profile.json"],
  "design_profile": "sketch/prototype-design-profile.json",
  "style_family": "<selected style family>",
  "ue_coverage": {"primary_cta_pages": 0, "state_feedback_pages": 0, "rule_visible_pages": 0, "error_recovery_pages": 0},
  "pages": [{"pmcontext_heading": "<heading>", "screen_id": "<pencil-screen-id>", "trace_uuid": "<UUID>"}],
  "components": [{"name": "<component>", "source": "<PMContext rule/acceptance>"}],
  "interactions": [{"from": "<screen>", "to": "<screen>", "source": "<state/flow edge>"}],
  "exports": ["<local file path or remote artifact id>"],
  "status": "passed | fallback-local | failed",
  "fallback_reason": "<only when fallback-local>"
}
```

**Pencil MCP 质量门**：
- 页面覆盖率：Pencil screen 数 ≥ PMContext 页面 heading 数。
- 交互覆盖率：关键 flow/state edge 均有可点路径或 manifest 中说明 `[待确认]`。
- 规则/验收映射：每页规则/验收要么在 screen 中可见，要么在 manifest 中列为 `[待确认]`，不得只画空壳。
- 导出/持久化：必须有本地文件路径或远端 artifact id，并写入 manifest。
- 失败诚实：MCP 调用失败、缺导出能力、页面覆盖不足且无法修复 → 输出原因并继续 Step -0.5 / Step -1 本地 fallback，不得打 Pencil 成功标。

输出：`✅ Pencil MCP: 命中 <server/tool> → 使用 MCP 原型 | ⚠️ 未命中/不可用/失败 <原因> → 使用本地技术栈`

**Step -0.5：PMContext §8 技术栈硬门（--prototype 模式专用，先于 Step -1 跑）**

扫描 PMContext §8（技术栈段）全文，匹配前端框架声明清单：

| 信号（命中任一即硬触发 Scaffold） | 说明 |
|---|---|
| `Vue` / `React` / `Next` / `Nuxt` / `Svelte` / `Angular` / `Electron`（单独出现即触发） | 前端框架名，工程化诉求明确 |
| `Vite` + `TypeScript` 同时出现 | 工程化构建链组合信号 |

**不触发的样式工具**（单独出现不触发）：`Tailwind` `UnoCSS` `Less` `Sass`——它们 CDN 也能用，不构成工程化诉求。

**硬门规则**：
- 命中任一信号 → **强制 Scaffold 模式**，跳过 Step -1 的简单信号判断；`--simple` flag 视为无效，仍走 Scaffold（防 Agent 自降级——AiGateway 事故根因）
- 未命中 → 进 Step -1 正常复杂度判断
- 输出：`✅ 技术栈硬门: 命中 <信号列表> → 强制 Scaffold | 未命中 → 进 Step -1`

**Step -1：复杂度判断（--prototype 模式专用）**

读取 PMContext，判断输出模式。**heading 计数容错**：解析 `## <页面>` heading 时，遇到异常/损坏字符（如乱码、不可见字符）不会导致漏计页面——按行首 `^## ` 正则匹配，跳过无法渲染为合法页面名的 entry；若损坏字符导致段无法解析，该段计入"未解析段"清单并在判断摘要中公示。

| 判断维度 | 简单模式信号 | Scaffold 模式信号 |
|---------|------------|----------------|
| PMContext `## <页面>` heading 数量 | ≤ 4 | > 4 |
| 是否含独立「数据模型」章节 | 否 | 是 |
| 用户角色数（从用户场景推断） | ≤ 2 | > 2 |
| state.md 中状态节点数 | ≤ 8 | > 8 |
| **各页 `### 规则` 条数（新增）** | ≤ 8 | > 8 |
| **各页 `### 验收` 条数（新增）** | ≤ 10 | > 10 |
| **flow.md 步骤数（新增）** | ≤ 10 | > 10 |

- 全部为简单信号 → **简单模式**（CDN 单 HTML，输出路径：`docs/pm-context/sketch/prototype.html`）
- 任一为 Scaffold 信号 → **Scaffold 模式**（Vite 工程，输出路径：`docs/pm-context/sketch/prototype/`）
- 判定规则：**任一 Scaffold 触发 → Scaffold；否则计算综合复杂度分，业务信号总量过阈值也升 Scaffold**。歧义时**保守偏 Scaffold**。

输出复杂度判断摘要：`✅ 原型模式: 简单/Scaffold（依据: <命中信号列表 + 综合分>）`

**Step 0：技术栈决策（按模式分区）**

**模板强制加载指令（所有模式，防即兴空壳 + 防丑默认）**：生成原型前必须先读取 `references/prototype-templates.md` 对应模式模板与 `references/design-style.md` 视觉协议；未读取禁止生成。读取后必须把 `prototype-content-plan.json` 作为唯一页面数据源注入模板，把 `prototype-design-profile.json` 作为唯一视觉/UE 数据源注入 Pencil MCP / Simple / Scaffold，禁止只生成 `id/title` 路由数组或套默认紫色空卡片。

技术栈决策按模式分区，两模式不再共用同一选型逻辑：

| 模式 | 框架决策 |
|------|---------|
| 简单模式（CDN HTML） | 保留现有 Step 0 逻辑——检测/推荐 Vue3 或 React，用 CDN script tag |
| Scaffold 模式（Vite 工程） | **固定 React + TS + Vite + Tailwind v4，不检测不推荐** |

**简单模式 Step 0**：扫描项目已有代码（`package.json` / `vite.config.ts` / `next.config.js` / `angular.json` 等），检测到已有技术栈则用其 CDN 版本；未检测到代码（新项目）按"业务复杂度 + 产品类型"双维度推荐技术栈。

**业务复杂度感知**（不仅仅看 package.json，更看 PMContext 业务特征）：

| PMContext 业务特征 | 推荐技术栈 | 依据 |
|------------------|-----------|------|
| 大量表单 + 复杂校验（如后台管理/CRM/ERP） | Vue3 + Element Plus | Element Plus 表单/校验生态成熟，开发效率高 |
| 大量实时状态变化（如协作工具/IM/仪表盘） | React + Zustand/Signal | React 生态对实时状态管理更成熟 |
| 纯内容展示（官网/营销页/博客） | Tailwind + 原生 HTML | 无需框架，Tailwind 足够，体积最小 |
| 大量数据可视化（BI/分析平台） | Vue3 + ECharts/D3 | ECharts 与 Vue3 集成成熟 |
| 跨平台同代码（Web + 桌面） | Electron + Vue3 | 桌面端生态最成熟 |

**新项目技术栈推荐规则**（业务复杂度 + 产品类型双维度，业务复杂度优先）：

| 产品类型（从 PMContext 推断） | 业务复杂度信号 | 推荐技术栈 |
|---------------------------|--------------|-----------|
| 业务管理系统 / 后台管理 | 表单多+校验多 | Vue3 + Vite + TypeScript + Element Plus |
| 前端页面 / 官网 / 营销页 | 纯展示 | Vue3 + Vite + TailwindCSS + TypeScript（或纯 Tailwind + HTML） |
| 协作工具 / IM / 仪表盘 | 实时状态多 | React + Vite + TypeScript + Zustand |
| 数据分析 / BI 平台 | 图表多 | Vue3 + Vite + TypeScript + ECharts |
| 桌面客户端应用 | 跨平台 | Electron + Vue3 + Vite + TypeScript |
| 移动端 App | — | Flutter / React Native（HTML 原型不适用，输出设计说明） |
| 全栈 Web 应用 | — | Vue3 + Nuxt + TypeScript / React + Next.js + TypeScript |
| 微前端架构 | — | Vue3 + Vite + Module Federation + TypeScript |
| 默认（无法推断） | — | Vue3 + Vite + TypeScript（最通用） |

**Scaffold 模式 Step 0**：固定 React + TS + Vite + Tailwind v4，不检测不推荐。理由：对齐 Axhub-Make `beginner-guide` 工程级实物水准，L4 交互（角色/权限/四态/错误恢复）需要 router + TS 类型检查 + `npm run build` 验证，CDN script tag 拼凑无法维护。

**Step 0.3：DESIGN.md 派生 Token（两种本地模式共用，--prototype 模式专用）**

PMContext 是业务事实源，`docs/design/DESIGN.md` 是视觉事实源（可选）。扫描优先级：
1. `--design <path>` 显式指定 → 用指定路径
2. 默认检测 `docs/design/DESIGN.md` → 存在则用
3. 都不存在 → 回退 pm-sketch 自带默认 Design Token

DESIGN.md 存在时严格按它派生 CSS token；缺失字段逐字段回退默认并标 `[假设]`；PMContext 品牌色与 DESIGN.md 冲突时 `--color-primary` 用 DESIGN.md 值（视觉事实源优先），PMContext 值写入 `--color-primary-alt` 并标 `[冲突]`。若已存在 `prototype-design-profile.json`，Token 必须与其中的 `style_family` / `tokens` 协同，不得另起一套审美。完整派生协议见 [references/prototype-templates.md](references/prototype-templates.md#一designmd-派生-token-协议) 与 [references/design-style.md](references/design-style.md)。

输出：`✅ Design Token: <DESIGN.md 派生 | 默认>（依据：<路径 / 回退默认>）`

**交互原型模板**（完整协议/代码见 [references/prototype-templates.md](references/prototype-templates.md)，按 Pencil MCP 或本地模式与技术栈选择对应模板，不要偏离核心结构）：
- 简单模式 → Vue3 CDN / React CDN / Plain HTML 兜底（按简单模式 Step 0 选型）
- Scaffold 模式 → 固定 React + TS + Vite + Tailwind v4 工程脚手架（第七节各文件模板）

**Electron 适配**：生成 Vue3/React 版本，在原型顶部加 `<!-- 🖥 此原型推荐用 Electron 包装运行 -->`

**移动端适配**：Flutter/React Native → 输出 `design-spec.md` 替代 HTML 原型

**Step 0.5：PRD 内容读取（--prototype 模式专用）**

读取以下文件并序列化为 `PRD_DATA` JSON 对象，内嵌到原型中（简单模式内联 `<script>`，Scaffold 模式写入 `src/data/prd-data.ts`）：

| 文件 | 读取内容 | 为空时 |
|------|---------|--------|
| `docs/pm-context/pm-context.md` | 所有页面 heading 的事实/规则/验收/假设/待确认项 + heading 原文段落（D1 展开用 `source` 字段） | PRD Panel 展示空状态占位 |
| `docs/pm-context/prd/ai-prd.md` | 完整文件（Scaffold 模式）/ 摘要（简单模式，截断至 10KB） | 跳过，不影响原型生成 |
| `docs/pm-context/prd/human-prd.md` | 同上 | 跳过 |
| `docs/design/DESIGN.md` | 完整原文（D2 文档 overlay 视觉依据区） | 文档 overlay 仅显示业务依据区 |

同时序列化 `DOC_DATA`（PMContext + DESIGN.md 原文 + documentTree）供 D2 文档 overlay 使用。

**注意**：此为 pm-sketch 执行时直接读取文件，不调用任何其他 skill。完整模板见 [references/prototype-templates.md](references/prototype-templates.md#五公共组件prd-panel)。

**质量清单**（生成后逐项检查，分模式完整清单见 [references/prototype-templates.md](references/prototype-templates.md#十三质量清单分模式)）：

Pencil MCP 模式硬校验（不满足禁止打 ✅，必须本地 fallback 或列出失败）：
- ✅ `sketch/pencil/pencil-prototype-manifest.json` 存在且 `mode=pencil-mcp`
- ✅ manifest 中 `pages` 覆盖 PMContext 页面 heading；screen 数 ≥ 页面数
- ✅ manifest 中 `interactions` 覆盖关键 state/flow edge，未覆盖项标 `[待确认]`
- ✅ manifest 中 `exports` 至少包含一个本地路径或远端 artifact id
- ✅ manifest 中 `design_profile` 指向 `sketch/prototype-design-profile.json`，且记录 `style_family` / `ue_coverage`
- ✅ `[假设]` / `[待确认]` / `[冲突]` 在 screen 或 manifest 中显式标注
- ✅ 未命中/失败时已回退本地 Simple/Scaffold，不静默停在半成品

简单模式 V1 硬校验（不满足禁止打 ✅，必须降级并列出缺失）：
- ✅ 页面覆盖率闸：原型内 `<section>`（或路由目标页）数量 **≥ PMContext `## <页面>` heading 数**。每个 PMContext 页面必须有对应可导航目标页，且每个 `<section>` 必须带 `data-trace-page="<PMContext heading>"`
- ✅ 每页内容密度闸：每个页面 `<section>` 内**非导航业务元素**（表单项 / 表格 / 列表 / 卡片 / 按钮，排除顶栏与菜单）节点数 **≥ 5**，其中至少 3 个元素必须带 `data-trace-ref` 指向 PMContext 规则/验收/事实。不足 5 个须标注原因并不得打 ✅
- ✅ 交互底线闸（L3）：每个 `<section>` 至少 1 个绑定 JS 事件的交互元素；hash 路由的每个目标页必须存在对应 section（不得指向空锚点）
- ✅ PMContext 映射闸：每个页面的「规则 / 验收」必须在对应页面渲染出可见元素（规则→`p.rule[data-trace-ref]`，验收→`ul.acceptance[data-trace-ref]`），不得只渲染标题；`TODO` / `敬请期待` / `占位` / 空 `<section>` 视为 Failure
- ✅ 技术栈决策有依据（CDN 选型）
- ✅ 单 HTML < 280KB（超限自动拆分懒加载）
- ✅ Design Token CSS 变量（来自 DESIGN.md + prototype-design-profile 或默认，无裸 #hex）
- ✅ 5 档响应式断点（手写 @media）
- ✅ Device Toolbar 三端切换（1440/820/393px）
- ✅ PRD Panel 展示 PMContext 批注（D1 可展开原文）
- ✅ 文档 overlay 可展开查看 PMContext / DESIGN.md
- ✅ 暗色主题适配
- ✅ V1 自检通过：反空壳体检（见下方输出块）

**V1 反空壳自检输出块**（`--auto` 也必须打印，即使不暂停）：
```
✅ 反空壳体检:
   - 页面覆盖率: 已实现 <M> / PMContext <N> 个页面
   - 每页交互元素计数: [页面A: x, 页面B: y, ...]
   - 未达标页面: <列表 或 无>
   - 路由空壳检测: <通过 / 失败，失败页列表>
```

Scaffold 模式：
- ✅ 目录结构对齐（package.json / vite.config.ts / tsconfig.json / src/components / src/pages / src/hooks）
- ✅ React 19 + Vite 6 + Tailwind v4 + TS 5.7 配置完整
- ✅ Design Token + prototype-design-profile 在 `style.css` 中（`@import "tailwindcss";` 之后）
- ✅ 5 档断点（Tailwind 响应式前缀）
- ✅ Device Toolbar + PRD Panel + DocOverlay 三组件完整
- ✅ 多页 hash 路由（useHashPage hook，对齐 Axhub）
- ✅ L4 交互：角色/权限/四态/错误恢复
- ✅ `index.tsx` 顶部含中文 `@name` 注释
- ✅ README.md 含启动命令
- ✅ V2/V3 验收通过或诚实降级

**验收级别判定（Acceptance Tier，正交于复杂度判断）**：

| 触发条件 | 验收级别 |
|---------|---------|
| 初次生成 / 改动 > 3 页 / 文件 > 5 / 元素 > 10 | V3（npm install + tsc + vite build + dev server + headless + console） |
| 其余 Scaffold 模式 | V2（npm install + tsc + vite build） |
| 简单模式（CDN HTML） | V1（AI 自检 + 体积检查） |

降级链：V3 失败 → V2 → V1 → 输出"未验收工程 + 已知错误清单"，**不静默撒谎**。完整验收脚本见 [references/prototype-templates.md](references/prototype-templates.md#十验收脚本)。

**增量原型模式（--incremental 或目标已存在）**：
- 读取已有 `prototype-content-plan.json` / `prototype-design-profile.json` / `prototype.html` / `prototype/` / `pencil-prototype-manifest.json`，建立已实现页面清单与既有风格 profile。
- 对比最新 PMContext heading：`新增页面 = PMContext 有但原型无`，`保留页面 = 两边都有`，`孤儿页面 = 原型有但 PMContext 无`。
- 默认只追加新增页面、更新路由/菜单/页面数据；保留页面文件不重写、不格式化、不覆盖。孤儿页面标 `[待确认]`，除非用户 `--rebuild`。
- 输出固定块：`✅ 原型增量: 新增页面 <列表> | 保留页面 <数量> | 孤儿页面 <列表或无> | 汇总待刷新: 是`。
- 若发现已有原型是路由空壳（页面缺少 `data-trace-ref` 或业务元素 <5），本次必须先补实已有页面，再追加新页面；不得在坏壳上继续叠路由。

**从 PMContext 到 HTML 图元的映射规则**：
| PMContext 中的项 | HTML 中的表达 |
|----------------|-------------|
| 页面/功能 | `<section id="<page-name>">` 或 Vue `v-for` / React `map` |
| 事实（字段/数据） | `<table>` 或 `<dl>` 列表，或 Vue `v-for` / React `map` |
| 规则（业务逻辑） | `<p class="rule">` 带 🔴 标记 |
| 验收标准 | `<ul class="acceptance">` 清单 |
| 用户场景 | 页面顶部的场景描述文字 |
| 全局约束 | 页面底部的约束标注 |
| `[假设]` 项 | 标注 `--- [假设] 待确认 ---` 注释 |
| `[待确认]` 项 | 灰色占位 `<div class="placeholder">待确认: ...</div>` |

生成后自动输出：
- `✅ 原型实现: <Pencil MCP | 本地 Simple | 本地 Scaffold>（<依据 / fallback 原因>）`
- `✅ 设计风格: <style_family>（profile: docs/pm-context/sketch/prototype-design-profile.json）`
- `✅ 技术栈: <名称>（<依据>）`（Pencil MCP 模式下写 `Pencil MCP` 与检测到的 server/tool）
- `✅ 交互原型已生成: <Pencil MCP: docs/pm-context/sketch/pencil/ | 简单模式: docs/pm-context/sketch/prototype.html | Scaffold 模式: docs/pm-context/sketch/prototype/>`
- `✅ 验收: <V1 自检通过 | V2 验收通过 | V3 验收通过 | ⚠️ 未验收，错误清单见 ...>`（仅 --prototype 模式）

**增量原型模式（`--prototype` 专用，按页增量，不覆盖已开发页面）**

**入口自判**：若目标产物已存在（Pencil MCP 模式 `sketch/pencil/`，简单模式 `sketch/prototype.html`，Scaffold 模式 `sketch/prototype/`），进入**增量原型模式**（除非用户显式 `--rebuild`）。

**增量纪律**：
1. 读取现有原型的**页面清单**：简单模式扫描已有 `<section id>` / 路由表；Scaffold 模式扫描 `src/pages/*` 文件名
2. 与当前 PMContext 页面 diff：
   - 只为「PMContext 有但原型无」的新页面生成新 section/page 文件
   - 「两边都有」的页面默认保留，除非该页对应 PMContext 段本轮被 `--update` 改动（则只重生成该页）
3. 更新路由/菜单以纳入新页面；**不得删除或推倒重来用户已开发页面**
4. Pencil MCP 模式优先调用 MCP 的 update/patch screen 能力；Scaffold 优势：`src/pages/<pageId>.tsx` 分文件天然支持按页增量；单 HTML 增量按 section 锚点合并

**增量原型验收级别**：增量原型按"改动页数 / 文件数"套用现有 Acceptance Tier（改动 >3 页或文件 >5 → V3；否则 V2；简单模式增量仍为 V1），避免"只加一页也全量 V3"或"增量后不验收"。

输出：
```
✅ 原型增量: 新增页面 <列表> | 保留页面 <数量> | 因 --update 重生成 <列表>
```

### 3. 审计（仅非自动模式）

展示产出物清单：
- Mermaid 草图：5 个文件路径
- 交互原型（如有）：Pencil MCP manifest/导出路径，或本地 HTML/Scaffold 路径
- PMContext 中未覆盖的图元（标 `[假设]`）

**🔴 CHECKPOINT** — 等用户确认。
- 用户说"通过" → 完成
- 用户说"调整" → 重新生成对应草图
- 用户说"继续" → 进入下个环节

## 零确认模式（--auto）

当通过 `--auto` 或直接 `$ARGUMENTS` 调用时：
1. 若 PMContext 不存在 → 自动 run `/pm-need --auto $ARGUMENTS`
2. 自动生成全部草图 + 交互原型
3. 直接落盘完成，不等待确认
4. 输出产物清单 + 置信度摘要

## 关联增强

在「草图交付物清单」和交互原型的「图元追溯映射」中，每个图元/`<section>` 的"来源"列标注对应 PMContext 事实项的 UUID。无来源的标 `[假设]`；冲突项标 `[冲突]` 不强行收敛。Entity Dictionary（`entity-dictionary.md`）是跨子 Skill 的规范名基线，IA/State/Flow/Wireframe/Journey 五图与交互原型必须使用字典中的规范名，禁止使用同义词列中的禁用名。

`--prototype` 模式下，PRD Panel 注入的 PMContext 批注（事实/规则/验收/假设/待确认，含 `source` 原文段落供 D1 展开）与草图图元构成双向追溯：图元 → PMContext heading UUID → PRD Panel 同名锚点。D2 文档 overlay 提供文件树（业务依据 `docs/pm-context/` + 视觉依据 `docs/design/DESIGN.md` 分区显示）+ `<pre>` 原文渲染，供 PM 随时核对依据。DESIGN.md 与 PMContext 双源冲突标 `[冲突]` 不强行收敛。

**与用户故事（stories.md）对照差分**：若 `<产物目录>/stories.md` 存在（即 pm-stories 已先于本 skill 跑过），读取其故事清单，在草图交付物清单中追加"**与 stories 对照差分**"行：
- 列出 stories 中有但 PMContext 无对应页面定义的故事 → 标 `[待确认]` 提示 PM 补 PMContext 页面定义后重跑 sketch
- 列出 sketch 中有但 stories 无对应故事的页面 → 标 `[假设]` 提示 PM 补故事或确认该页面无独立故事价值
- 双方都没有的孤立项不列入，只列单向差分

## 失败模式

| 触发条件 | 一线修复 | 仍失败兜底 |
|---------|---------|-----------|
| `<产物目录>/pm-context.md` 不存在 且无 `$ARGUMENTS` | **🔴 STOP**：输出"未找到 PMContext，先运行 `/pm-need <需求>`" | 不阻塞，提示后退出 |
| PMContext 不存在但有 `$ARGUMENTS` 或 `--auto` | 自动调用 `/pm-need --auto $ARGUMENTS`（**仅当本次未被 pm-need 编排时**——即未收到 `--no-fallback` 标）生成 PMContext，结束后回到草图生成 | pm-need 失败则 STOP 并提示失败原因 |
| PMContext 中无页面/实体定义 | 跳过 wireframe/ia，只生成 state/flow（若有规则线索）；顶部加 `⚠️ 跳过 N 个图：PMContext 缺页面/实体定义` | 不阻塞，记入信息缺口清单 |
| 任一子 skill（pm-wireframe/ia/state/flow）失败 | 不阻塞其他子 skill，记录失败项到产物清单的"失败清单"章节 | 其他成功草图仍落盘 |
| `--prototype` 模式下未检测到 Pencil MCP 或 `$ARGUMENTS` 含 `--no-mcp` | 输出未命中/跳过原因，继续 Step -0.5 / Step -1 本地技术栈判断 | 不阻塞，保持原有 Simple/Scaffold 行为 |
| 检测到 Pencil MCP 但缺 create/update 或 export/persist 能力 | 视为不可用，写入 fallback 原因，继续本地技术栈 | 不假装已用 MCP |
| Pencil MCP 调用失败或导出失败 | 重试最多 2 次；仍失败则写 `pencil-prototype-manifest.json` 的 `status=fallback-local` + `fallback_reason`，继续本地技术栈 | 不打 Pencil 成功标 |
| `--prototype` 模式下无法检测到技术栈（无代码、无 package.json、无依赖） | 简单模式：按新项目推荐 Vue3 + Vite + TypeScript；Scaffold 模式：固定 React + TS + Vite + Tailwind v4，不检测 | 简单模式使用 Plain HTML 兜底模板 |
| `--prototype` 模式下检测到多个冲突框架（如 package.json 同时含 vue 和 react） | 简单模式标 `[冲突]` 并列出检测到的框架，推荐使用第一个；Scaffold 模式固定 React 不受影响 | 简单模式使用 Plain HTML 兜底模板 |
| `--prototype` 模式下推荐/检测到 Flutter / React Native（HTML 原型不适用） | 输出 `design-spec.md` 替代 HTML 原型，包含屏幕设计说明 + 组件规范 + 交互描述 | 不生成 prototype，在产物清单中标注 |
| `--prototype` 简单模式单 HTML > 280KB | 自动拆分：入口保留目录索引 + 摘要，正文懒加载独立 `.js` chunk（见 prototype-templates.md 6.4） | 拆分后仍超限则提示精简，退化为只输出 Mermaid 草图 |
| `--prototype` Scaffold 模式 V3 验收失败（dev server / headless / console 错误） | 按 V3 → V2 → V1 降级链降级，重试 3 次失败后输出"未验收工程 + 已知错误清单" | 不静默撒谎打 ✅，诚实标注未验收 |
| `--prototype` Scaffold 模式 V2 验收失败（npm install / tsc / vite build） | 按错误信息修复后重试；3 次失败后降级到 V1（AI 自检）并输出错误清单 | 文件已落盘，提示用户手动 `npm install && npm run build` |
| `--prototype` 模式下 CDN 版本不可用（如 unpkg CDN 域名被墙） | 简单模式使用备用 CDN（cdnjs / jsdelivr），或退化为 Plain HTML 兜底模板；Scaffold 模式不依赖 CDN 不受影响 | 简单模式退化为 Plain HTML 无框架版本 |
| `--auto` 模式下 pm-need 链路失败 | STOP 并输出一站式报告含失败原因 | 已生成部分仍落盘 |
| PMContext 中 `[冲突]` 项涉及核心图元 | 图元标 `[冲突]` 不强行选定方向 | 在产物清单汇总冲突项供 PM 决策 |
| PMContext 品牌色与 DESIGN.md 冲突 | `--color-primary` 用 DESIGN.md 值（视觉事实源优先），PMContext 值写入 `--color-primary-alt` 并标 `[冲突]` | 不强行收敛，在产物清单标注冲突项 |
| **`--prototype` 目标已存在且未加 `--rebuild`** | 进增量原型模式，仅加新页/改动页 | 不整体覆盖 |
| **现有原型页面与 PMContext 页面无法对齐** | 标 `[待确认]` 列出对不齐页面，保留旧页 | 不静默删页 |
| **用户显式 `--rebuild`** | 全量重生成并提示「将覆盖已开发页面」 | 需确认（非 --auto 时） |

## 不要做什么（反例黑名单）

| 反模式 | 为什么不要做 |
|--------|------------|
| 脱离 PMContext 凭感觉画图 | 图元无追溯，与需求脱节 |
| 把 `[假设]` 图元画成确定性内容 | 误导团队以为确认过 |
| 原型使用与推荐/检测技术栈无关的 CDN | 原型的目的是展示开发方向，用错技术栈给 PM 和工程团队错误预期 |
| 有现有代码时不检测技术栈，直接用默认模板 | 老项目已有可用的框架/组件库，用新技术栈生成的原型与实际开发脱节 |
| 新项目不推荐技术栈 | PM 需要技术方向建议来评估可行性和资源 |
| 草图嵌入 PRD 文件 | 草图是独立 View，不应嵌套 |
| `--auto` 遇子 skill 失败就全链路回滚 | 其他成功部分仍落盘，失败项单独标注 |
| 审计三元组反模式 | 见 CONTEXT.md『审计三元组反模式（共享定义）』——同义反复/空话/未阐明具体推导逻辑均判定为 Failure |
| 检测到可用 Pencil MCP 却仍直接走本地 HTML/Scaffold（未显式 `--no-mcp`） | 违反 MCP 优先门，用户希望有 Pencil MCP 时由 MCP 实现原型系统 |
| Pencil MCP 只返回远端 id 而不写本地 manifest | 下游无法审计输入、页面映射和 fallback 状态，约束不可验证 |
| 未检测到 Pencil MCP 却声称“已用 MCP 生成” | 静默撒谎；看不到工具清单/能力时必须本地 fallback |
| PMContext §8 含前端框架声明（Vue/React/Next/Nuxt/Svelte/Angular/Electron，或 Vite+TypeScript）时降级到简单模式 | Agent 偷懒自降级——AiGateway 事故就是此失守，PMContext 明写 Vue 3+Vite 却产出 HTML 壳子；Step -0.5 硬门兜底，`--simple` flag 此场景视为无效 |
| Scaffold 模式生成后不运行验收即打 ✅ 标记完成 | 系统性撒谎——PM 拿到一个 `npm install` 都跑不起来的工程，毁信任 |
| 简单模式超 280KB 不拆分不提示 | 体积门是质量底线，超限静默输出等于隐藏已知缺陷 |
| Scaffold 模式没有 package.json / vite.config.ts 就输出 `.tsx` 文件 | 与工程脚手架承诺不符，用户拿到的是不可运行的碎片 |
| 简单模式和 Scaffold 模式共用同一套 Design Token 模板 | 两模式 token 引入方式不同（inline vs CSS file + Tailwind），混用导致 Scaffold 工程出现 CDN script tag |
| V3 验收失败后直接跳过不降级（静默改打 ✅） | 与降级链契约矛盾，V3 失败应诚实降级，不得撒谎 |
| **简单模式只输出路由骨架不渲染页面内容（空壳）** | 违反 L3 底线，等于交付未实施的需求，判定 Failure |
| **页面覆盖率 < PMContext 页面数仍打 ✅** | 系统性撒谎，PM 拿到缺页原型 |
| **每页业务元素 < 5 且未标注原因** | 页面等于空壳，必须降级并记入信息缺口 |
| **Scaffold 模式增量迭代时全量重生成原型覆盖已开发页面** | 摧毁用户迭代成果，等于不支持增量 |
| **新增页面时不更新菜单/路由** | 新页面不可达，等于没加 |
| **只生成导航/路由/空 section，不从 `prototype-content-plan.json` 渲染事实/规则/验收/动作** | 用户看到的是单 HTML 壳子，不是原型系统；判定 Failure，必须回修或升 Scaffold |
| **增量时只追加菜单项不追加页面业务内容** | 会造成“有路由没核心内容”，必须同步追加页面 section/component + data-trace + 交互动作 |
| **未读取 `references/design-style.md` 或未写 `prototype-design-profile.json` 就生成原型** | 视觉/UE 约束没有进入执行链路，模型会回到默认丑模板；判定 Failure |
| **Pencil MCP brief 未携带 `prototype-design-profile.json`** | MCP 只收到页面清单，容易画成空壳或默认风格；必须重新调用或本地 fallback |
| **为了好看删掉规则/验收/状态/trace** | 审美不能覆盖产品事实源；必须保留追溯与可见规则 |

---

## 产出示例 · 实战提示

详见 [references/sketch-prototype-example.md](references/sketch-prototype-example.md)（草图 + 交互原型联动产出示例与质量检查技巧）。

### Further Reading

- [Mermaid stateDiagram-v2 docs](https://mermaid.js.org/syntax/stateDiagram.html)
- [Mermaid flowchart docs](https://mermaid.js.org/syntax/flowchart.html)
