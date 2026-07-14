# 交互原型模板集

> 由 `/pm-sketch --prototype` 根据 Pencil MCP 实现门与本地模式/技术栈决策结果选用。详见 `SKILL.md` 的「Step -0.85：设计风格编译门」「Step -0.75：Pencil MCP 实现门」「Step -1：复杂度判断」「Step 0：技术栈决策」「DESIGN.md 派生 Token 协议」节。

## 模式总览

| 维度 | Pencil MCP 模式 | 简单模式 (Simple / CDN) | Scaffold 模式 (Vite 工程) |
|------|-----------------|------------------------|--------------------------|
| 产物 | `docs/pm-context/sketch/pencil/` + `pencil-prototype-manifest.json` | 单 HTML `docs/pm-context/sketch/prototype.html` | 工程目录 `docs/pm-context/sketch/prototype/` |
| 实现方式 | 调用 runtime 暴露的 Pencil MCP create/update/export/persist 能力 | Vue3 / React / Plain HTML（CDN，Step 0 检测/推荐） | 固定 React + TS + Vite + Tailwind v4 |
| 体积门 | 由 MCP 导出格式决定；必须有 manifest 和导出/持久化证明 | 单 HTML < 280KB（超限自动拆分懒加载） | 无上限 |
| 交互底线 | 页面 screen + 可点 flow/state edge + manifest traceability | L3（hash 多页路由 + 表单跳转 + 状态切换） | L4（L3 + 角色/权限/四态/错误恢复） |
| 数据嵌入 | 以 MCP artifact + manifest 保存输入映射 | E1 静态嵌入（强制） | E1（默认）+ E2 fetch（V3 验收可选） |
| 验收级别 | MCP 质量门（页面覆盖/交互覆盖/导出持久化） | V1（AI 自检 + 体积检查） | V2 / V3（按 Acceptance Tier） |
| 文档预览 | manifest 记录 PMContext/DESIGN/PRD 输入；MCP 支持则生成文档 screen | 内联 overlay（E1） | DocOverlay 组件（E1 + 可选 E2） |
| 视觉/UE | brief 必须携带 `prototype-design-profile.json` | `:root` token + 页面布局骨架来自 design profile | `src/style.css` token + 组件布局/动效策略来自 design profile |
| 视觉可见性审计 | manifest 引用 `visual-audit-report.json`；不可解析时 `needs-manual-review` | 运行 `scripts/visual_audit_prototype.py prototype.html`，失败不得打 ✅ | V2/V3 运行静态 + headless computed style / screenshot 审计，失败不得打 ✅ |

Pencil MCP 模式是 `--prototype` 的优先实现通道；未命中、用户显式 `--no-mcp`、MCP 缺导出/持久化能力或调用失败时，回退到原有 Simple/Scaffold 本地实现。Simple/Scaffold 共享的公共组件：Design Token、Device Toolbar、PRD Panel、文档 overlay、Toast / Modal。简单模式内联实现，Scaffold 模式拆为独立 React 组件。

---

## 负一、Design Style Profile（视觉/UE 数据契约）

所有 `--prototype` 模式在进入 Pencil MCP / Simple / Scaffold 前，必须读取 `references/design-style.md` 并写 `docs/pm-context/sketch/prototype-design-profile.json`。此文件是视觉事实源的编译结果，不能只停留在提示词里。

### -1.1 最小 schema

```ts
type PrototypeDesignProfile = {
  mode: 'prototype-design-profile'
  design_read: string
  style_family: 'Enterprise Calm' | 'AI Native Dark' | 'Data Cockpit' | 'Premium Consumer' | 'Trust First' | 'Developer Tool' | string
  secondary_style?: string
  dials: { design_variance: number; motion_intensity: number; visual_density: number }
  tokens: {
    theme: 'light' | 'dark' | 'auto'
    accent: string
    radius_scale: string
    shadow_style: string
    type_scale: string
    spacing_scale: string
  }
  layout_patterns: string[]
  interaction_patterns: string[]
  anti_patterns_banned: string[]
}
```

### -1.2 消费规则

- Pencil MCP：把完整 `PrototypeDesignProfile` 放进 MCP brief；manifest 写 `design_profile`、`style_family`、`ue_coverage`。
- Simple：把 tokens 映射为 `:root` / `[data-theme=dark]` CSS 变量；按 `layout_patterns` 选择页面骨架。
- Scaffold：把 tokens 写入 `src/style.css`；按 `layout_patterns` 分配页面组件，按 `interaction_patterns` 实现状态反馈、错误恢复和审计抽屉。
- 与 DESIGN.md 冲突时，DESIGN.md 是视觉事实源，profile 记录 `[冲突]` 与 fallback，不得静默改色。

### -1.3 反默认审美闸

若原型出现以下任一项，V1/V2/V3 均不得打 ✅：

- 没有 `prototype-design-profile.json`
- 只有默认紫蓝渐变、毛玻璃和三张空卡片
- 所有页面长得一样，只替换标题
- 假截图/假图表没有真实可点交互或 trace
- 为了视觉效果删掉 PMContext 规则/验收/状态

### -1.4 Visual Audit Report（视觉可见性数据契约）

所有模式必须生成 `docs/pm-context/sketch/visual-audit-report.json`，用于捕获“代码里有元素，但用户看不见”的问题。

```ts
type VisualAuditReport = {
  mode: 'visual-audit'
  status: 'passed' | 'failed' | 'needs-manual-review'
  source: 'Pencil export' | 'prototype.html' | 'prototype/'
  token_digest: string
  checks: {
    token_contrast_pairs: { passed: number; failed: number }
    interactive_visibility: { passed: number; failed: number }
    state_visibility: { passed: number; failed: number }
    focus_visible: { passed: number; failed: number }
    empty_clickable_overlay: { passed: number; failed: number }
  }
  findings: Array<{ severity: 'error' | 'warn'; code: string; target: string; detail: string }>
  repair_actions: string[]
}
```

最低门槛：

- `--color-text` / `--color-text-secondary` 对 `--color-bg`、`--color-bg-secondary`、`--color-bg-tertiary` 必须可读。
- `--color-on-primary` 对 `--color-primary` 必须可读。
- 所有 `button`、`a[href]`、`[role=button]`、表格操作项和菜单项必须有可见文字/图标/边框/焦点态。
- 任何“字体颜色与背景色相同/接近”“点击区域存在但视觉空白”的问题，判定为 Failure。

---

## 零、Pencil MCP Manifest 模板

当 `/pm-sketch --prototype` 检测到可用 Pencil MCP 时，不直接生成本地 HTML/Scaffold，而是调用 MCP 创建或更新原型系统，并在本地写 manifest 作为可审计证据。manifest 是 Pencil MCP 模式的硬交付物。

```json
{
  "mode": "pencil-mcp",
  "server": "<detected pencil mcp server/tool>",
  "inputs": [
    "docs/pm-context/pm-context.md",
    "docs/pm-context/sketch/entity-dictionary.md",
    "docs/pm-context/prd/ai-prd.md",
    "docs/pm-context/prd/human-prd.md",
    "docs/design/DESIGN.md?",
    "docs/pm-context/sketch/prototype-content-plan.json",
    "docs/pm-context/sketch/prototype-design-profile.json"
  ],
  "design_profile": "docs/pm-context/sketch/prototype-design-profile.json",
  "style_family": "<selected style family>",
  "visual_audit": {"status": "passed | failed | needs-manual-review", "report": "docs/pm-context/sketch/visual-audit-report.json", "contrast_failures": 0, "invisible_interactive_count": 0},
  "ue_coverage": {
    "primary_cta_pages": 0,
    "state_feedback_pages": 0,
    "rule_visible_pages": 0,
    "error_recovery_pages": 0
  },
  "pages": [
    {
      "pmcontext_heading": "<PMContext page heading>",
      "screen_id": "<pencil screen id>",
      "trace_uuid": "<entity/page UUID>",
      "assumption_status": "fact | [假设] | [待确认] | [冲突]"
    }
  ],
  "components": [
    {"name": "<component name>", "source": "<PMContext rule/acceptance/source anchor>"}
  ],
  "interactions": [
    {"from": "<screen id>", "to": "<screen id>", "source": "<state/flow edge>"}
  ],
  "exports": ["<local export path or remote artifact id>"],
  "status": "passed",
  "fallback_reason": ""
}
```

### 0.1 Pencil MCP 输入包

传给 MCP 的 brief 必须包含：

- 页面清单：PMContext `## <页面>` heading、事实、规则、验收、风险标记。
- Entity Dictionary：规范名、UUID、禁用同义词。
- 行为线索：state/flow/journey 的关键节点与边。
- 文档源：PMContext、AI PRD、Human PRD、DESIGN.md（如有）。
- 质量门：页面覆盖、交互覆盖、规则/验收可见、导出/持久化。
- 视觉/UE profile：`prototype-design-profile.json` 的 style_family、dials、tokens、layout_patterns、interaction_patterns、anti_patterns_banned。

### 0.2 Pencil MCP fallback manifest

若检测到 Pencil MCP 但调用失败，仍写 manifest 记录失败，然后回退本地实现：

```json
{
  "mode": "pencil-mcp",
  "server": "<detected pencil mcp server/tool>",
  "inputs": ["docs/pm-context/pm-context.md"],
  "design_profile": "docs/pm-context/sketch/prototype-design-profile.json",
  "style_family": "<selected style family>",
  "visual_audit": {"status": "passed | failed | needs-manual-review", "report": "docs/pm-context/sketch/visual-audit-report.json", "contrast_failures": 0, "invisible_interactive_count": 0},
  "ue_coverage": {},
  "pages": [],
  "components": [],
  "interactions": [],
  "exports": [],
  "status": "fallback-local",
  "fallback_reason": "<MCP missing export capability | MCP call failed | coverage gate failed>"
}
```

---

## 零点五、Prototype Content Plan（反空壳数据契约）

`/pm-sketch --prototype` 在调用 Pencil MCP 或生成本地 HTML/Scaffold 之前，必须先写 `docs/pm-context/sketch/prototype-content-plan.json`。后续模板只能从该文件渲染页面，不能临时拼一个只有 `id/title` 的 routes 数组。

### 0.5.1 页面数据最小 schema

```ts
type PrototypePage = {
  heading: string
  page_id: string
  primary_job: string
  scenario: string
  facts: string[]
  rules: string[]
  acceptances: string[]
  fields: Array<{ name: string; kind?: 'text' | 'select' | 'number' | 'date' | 'table'; source: string }>
  actions: Array<{ label: string; effect: string; target_page?: string; source: string }>
  states: Array<'loading' | 'empty' | 'success' | 'error' | string>
  trace_refs: string[]
}
```

**禁止 schema**：

```json
[{"id":"home","title":"首页"}]
```

只有 `id/title` 的页面数组视为路由壳，不得进入模板渲染。

### 0.5.2 Route-to-Content 渲染合约

每个 route/page 必须渲染以下 6 个区域，且至少 5 个区域有可见内容：

1. `hero/scenario`：用户场景与本页核心任务。
2. `facts`：字段、实体、数据卡片或表格。
3. `rules`：`<p class="rule" data-trace-ref="...">`。
4. `acceptances`：`<ul class="acceptance" data-trace-ref="...">`。
5. `workbench`：至少一个表单 / 表格 / 列表 / 卡片组，内容来自 `fields` 或 `facts`。
6. `actions`：至少一个绑定 JS/React/Vue 事件的按钮，effect 是跳转、状态切换、提交、筛选、展开、错误恢复之一。

空字符串、`TODO`、`敬请期待`、`占位`、只有标题、只有菜单，全部判定为 Failure。

### 0.5.3 简单模式页面工厂（Vue/React/Plain HTML 均可照抄）

```javascript
function escapeHtml(v) {
  return String(v ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}

function renderTraceList(items, className, label) {
  const safe = Array.isArray(items) && items.length ? items : ['[待确认] PMContext 未提供' + label];
  return `<ul class="${className}" data-trace-ref="${label}">` +
    safe.map((x, i) => `<li data-trace-ref="${label}-${i}">${escapeHtml(x)}</li>`).join('') +
    `</ul>`;
}

function renderWorkbench(page) {
  const fields = Array.isArray(page.fields) && page.fields.length
    ? page.fields
    : (page.facts || []).slice(0, 4).map((fact, i) => ({ name: `字段${i + 1}`, source: fact }));
  return `<div class="workbench grid-2" data-trace-ref="${escapeHtml(page.heading)}-workbench">` +
    fields.map((f, i) => `
      <label class="field-card" data-trace-ref="${escapeHtml(f.source || page.heading)}">
        <span>${escapeHtml(f.name)}</span>
        <input value="${escapeHtml((f.source || '').slice(0, 24))}" aria-label="${escapeHtml(f.name)}" />
      </label>`).join('') +
    `</div>`;
}

function renderActions(page) {
  const actions = Array.isArray(page.actions) && page.actions.length
    ? page.actions
    : [{ label: '确认并进入下一步', effect: 'show-toast', source: page.heading }];
  return `<div class="actions">` + actions.map((a, i) => `
    <button type="button" data-action-index="${i}" data-trace-ref="${escapeHtml(a.source || page.heading)}">
      ${escapeHtml(a.label)}
    </button>`).join('') + `</div>`;
}

function renderPageSection(page) {
  return `<section id="page-${escapeHtml(page.page_id)}" data-trace-page="${escapeHtml(page.heading)}">
    <header class="page-hero">
      <p class="eyebrow">${escapeHtml(page.primary_job || '[待确认] 核心任务')}</p>
      <h1>${escapeHtml(page.heading)}</h1>
      <p>${escapeHtml(page.scenario || '[待确认] 用户场景')}</p>
    </header>
    <div class="facts grid-3" data-trace-ref="${escapeHtml(page.heading)}-facts">
      ${(page.facts || ['[待确认] 关键事实']).map(x => `<article class="fact-card" data-trace-ref="${escapeHtml(x)}">${escapeHtml(x)}</article>`).join('')}
    </div>
    <div class="rules-block">
      <h2>业务规则</h2>
      ${renderTraceList(page.rules, 'rule-list', page.heading + '-rules')}
    </div>
    <div class="acceptance-block">
      <h2>验收标准</h2>
      ${renderTraceList(page.acceptances, 'acceptance', page.heading + '-acceptances')}
    </div>
    ${renderWorkbench(page)}
    ${renderActions(page)}
    <div class="state-strip" data-trace-ref="${escapeHtml(page.heading)}-states">
      ${(page.states || ['success']).map(s => `<button type="button" class="state-chip" data-state="${escapeHtml(s)}">${escapeHtml(s)}</button>`).join('')}
    </div>
  </section>`;
}

function bindPageInteractions(root = document) {
  root.querySelectorAll('[data-action-index]').forEach(btn => {
    btn.addEventListener('click', () => {
      const page = btn.closest('section')?.dataset.tracePage || '当前页';
      window.__LAST_ACTION__ = { page, label: btn.textContent.trim(), at: new Date().toISOString() };
      document.body.dataset.lastAction = `${page}: ${btn.textContent.trim()}`;
      alert(`已执行：${btn.textContent.trim()}`);
    });
  });
  root.querySelectorAll('.state-chip').forEach(btn => {
    btn.addEventListener('click', () => btn.closest('section')?.setAttribute('data-active-state', btn.dataset.state));
  });
}
```

### 0.5.4 V1 route shell detector

生成后用肉眼/脚本都可执行的检查逻辑：

```javascript
function inspectRouteShell() {
  return Array.from(document.querySelectorAll('section[id^="page-"]')).map(sec => {
    const traced = sec.querySelectorAll('[data-trace-ref]').length;
    const interactive = sec.querySelectorAll('button,[onclick],[data-action-index],input,select,textarea').length;
    const text = sec.textContent.trim();
    const shellWords = /TODO|敬请期待|占位|coming soon|placeholder/i.test(text);
    return { id: sec.id, traced, interactive, textLength: text.length, passed: traced >= 3 && interactive >= 1 && text.length >= 120 && !shellWords };
  });
}
```

`inspectRouteShell().some(x => !x.passed)` 为 true 时，禁止打 ✅；先补业务内容，或升 Scaffold。

## 一、DESIGN.md 派生 Token 协议

PMContext 是业务事实源，`docs/design/DESIGN.md` 是视觉事实源（可选）。两源冲突标 `[冲突]` 不强行收敛。

### 1.1 扫描路径（优先级递减）

1. `--design <path>` 显式指定 → 用指定路径
2. 默认检测 `docs/design/DESIGN.md` → 存在则用
3. 都不存在 → 回退 pm-sketch 自带默认 token 表

### 1.2 字段映射规则

DESIGN.md 采用与 Axhub-Make `theme-guide.md` 对齐的结构，字段 → CSS 变量映射：

| DESIGN.md 字段 | CSS 变量 | 默认值 |
|---------------|---------|--------|
| `colors.primary` | `--color-primary` | `#2563eb` |
| `colors.ink` | `--color-text` | `#1f2937` |
| `colors.ink-muted` | `--color-text-secondary` | `#6b7280` |
| `colors.ink-subtle` | `--color-text-muted` | `#9ca3af` |
| `colors.canvas` | `--color-bg` | `#ffffff` |
| `colors.surface-1` | `--color-bg-secondary` | `#f9fafb` |
| `colors.surface-2` | `--color-bg-tertiary` | `#f3f4f6` |
| `colors.hairline` | `--color-border` | `#e5e7eb` |
| `colors.success` | `--color-success` | `#10b981` |
| `colors.on-success` | `--color-on-success` | `#052e16` |
| `colors.warning` | `--color-warning` | `#f59e0b` |
| `colors.on-warning` | `--color-on-warning` | `#422006` |
| `colors.danger` | `--color-danger` | `#ef4444` |
| `colors.on-danger` | `--color-on-danger` | `#280000` |
| `colors.info` | `--color-info` | `#3b82f6` |
| `colors.accent` | `--color-accent` | `#f59e0b` |
| `spacing.xxs` | `--space-xs` | `4px` |
| `spacing.xs` | `--space-sm` | `8px` |
| `spacing.md` | `--space-md` | `16px` |
| `spacing.lg` | `--space-lg` | `24px` |
| `spacing.xl` | `--space-xl` | `32px` |
| `spacing.xxl` | `--space-2xl` | `48px` |
| `rounded.xs` | `--radius-xs` | `2px` |
| `rounded.sm` | `--radius-sm` | `4px` |
| `rounded.md` | `--radius-md` | `8px` |
| `rounded.lg` | `--radius-lg` | `12px` |
| `rounded.xl` | `--radius-xl` | `16px` |
| `typography.body.fontSize` | `--font-size-base` | `1rem` |
| `typography.body-sm.fontSize` | `--font-size-sm` | `0.875rem` |
| `typography.body-lg.fontSize` | `--font-size-lg` | `1.125rem` |
| `typography.body.fontFamily` | `--font-sans` | `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif` |
| `typography.mono.fontFamily` | `--font-mono` | `'SF Mono', 'Fira Code', monospace` |

### 1.3 缺失字段处理

- DESIGN.md 存在但某字段缺失 → 该字段用默认值，token 注释中标 `[假设]`
- DESIGN.md 存在但全无 `typography` 节 → typography 全部回退默认
- `rounded` / `spacing` 同上逐字段回退

### 1.4 冲突处理

PMContext 品牌色与 DESIGN.md 不一致时：
- `--color-primary` 使用 DESIGN.md 值（视觉事实源优先）
- PMContext 值写入 `--color-primary-alt`，旁注 `/* [冲突] PMContext: #xxx */`

---

## 二、Design Token CSS 完整表（默认值）

所有模式必须使用 CSS 自定义属性定义 Design Token，禁止裸 `#hex` 色值。以下为无 DESIGN.md 时的默认 token 表，AI 生成时按 1.2 映射规则代入 DESIGN.md 派生值。

```css
:root {
  /* 品牌色 */
  --color-primary: #2563eb;
  --color-primary-light: #60a5fa;
  --color-primary-dark: #1d4ed8;
  --color-accent: #f59e0b;

  /* 语义色 */
  --color-success: #10b981;
  --color-on-success: #052e16;
  --color-warning: #f59e0b;
  --color-on-warning: #422006;
  --color-danger: #ef4444;
  --color-on-danger: #280000;
  --color-info: #3b82f6;

  /* 中性色 */
  --color-text: #1f2937;
  --color-text-secondary: #6b7280;
  --color-text-muted: #9ca3af;
  --color-bg: #ffffff;
  --color-bg-secondary: #f9fafb;
  --color-bg-tertiary: #f3f4f6;
  --color-border: #e5e7eb;
  --color-border-light: #f3f4f6;

  /* 间距 */
  --space-xs: 4px; --space-sm: 8px; --space-md: 16px;
  --space-lg: 24px; --space-xl: 32px; --space-2xl: 48px;

  /* 圆角 */
  --radius-xs: 2px; --radius-sm: 4px; --radius-md: 8px;
  --radius-lg: 12px; --radius-xl: 16px; --radius-full: 9999px;

  /* 阴影 */
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
  --shadow-md: 0 4px 6px rgba(0,0,0,0.07);
  --shadow-lg: 0 10px 15px rgba(0,0,0,0.1);

  /* 字体 */
  --font-sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-mono: 'SF Mono', 'Fira Code', monospace;
  --font-size-sm: 0.875rem; --font-size-base: 1rem;
  --font-size-lg: 1.125rem; --font-size-xl: 1.25rem; --font-size-2xl: 1.5rem;
}

@media (prefers-color-scheme: dark) {
  :root {
    --color-text: #f3f4f6; --color-text-secondary: #9ca3af; --color-text-muted: #6b7280;
    --color-bg: #111827; --color-bg-secondary: #1f2937; --color-bg-tertiary: #374151;
    --color-border: #374151; --color-border-light: #4b5563;
  }
}
:root.dark {
  --color-text: #f3f4f6; --color-text-secondary: #9ca3af; --color-text-muted: #6b7280;
  --color-bg: #111827; --color-bg-secondary: #1f2937; --color-bg-tertiary: #374151;
  --color-border: #374151; --color-border-light: #4b5563;
}
```

---

## 三、5 档响应式断点

### 3.1 简单模式（手写 @media）

```css
/* Desktop-XL: ≥ 1440px — 默认布局，不写 media query */
@media (max-width: 1439px) { /* Desktop: 稍有缩窄，布局不变 */ }
@media (max-width: 1279px) { /* Tablet: 3→2 列，导航不变 */
  .grid-3 { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 1023px) { /* Mobile-Lg: 2→1 列，导航 hamburger */
  .grid-3 { grid-template-columns: 1fr; }
  nav.inline { display: none; }
  nav.hamburger { display: flex; }
}
@media (max-width: 767px) { /* Mobile: 单列，字号缩小，touch target 增大 */
  h1 { font-size: clamp(1.5rem, 5vw, 2rem); }
}
```

### 3.2 Scaffold 模式（Tailwind v4 响应式前缀）

| Tailwind 断点 | 最小宽度 | 对齐 5 档 | 用途 |
|--------------|---------|----------|------|
| `sm:` | 640px | Mobile | 手机 |
| `md:` | 768px | Mobile-Lg | 手机横屏 / 小平板 |
| `lg:` | 1024px | Tablet | 平板 |
| `xl:` | 1280px | Desktop | 桌面 |
| `2xl:` | 1536px | Desktop-XL | 大屏桌面 |

Scaffold 模式使用 Tailwind 前缀，简单模式使用手写 `@media`。底层布局必须真断点，不靠 Device Toolbar 缩放作弊。

---

## 四、公共组件：Device Toolbar

Device Toolbar 三端一键切换演示（1440 / 820 / 393 px）。

### 4.1 简单模式（内联 HTML + JS）

```html
<div id="device-toolbar">
  <style>
    #device-toolbar {
      position: fixed; top: 0; left: 0; right: 0; z-index: 9999;
      background: var(--color-bg-secondary, #f9fafb);
      border-bottom: 1px solid var(--color-border, #e5e7eb);
      padding: var(--space-sm, 8px) var(--space-md, 16px);
      display: flex; align-items: center; gap: var(--space-sm, 8px);
      font-family: var(--font-sans, -apple-system, sans-serif);
      font-size: var(--font-size-sm, 0.875rem);
    }
    #device-toolbar .dt-label { color: var(--color-text-secondary, #6b7280); margin-right: var(--space-sm, 8px); }
    #device-toolbar button {
      padding: 4px 12px; border: 1px solid var(--color-border, #e5e7eb);
      background: var(--color-bg, #fff); color: var(--color-text, #1f2937);
      border-radius: var(--radius-sm, 4px); cursor: pointer;
    }
    #device-toolbar button.active { background: var(--color-primary, #2563eb); color: #fff; border-color: var(--color-primary, #2563eb); }
    #device-toolbar .dt-size { margin-left: auto; color: var(--color-text-muted, #9ca3af); font-family: var(--font-mono, monospace); }
    #prototype-content { margin-top: 42px; transition: max-width 0.3s, margin 0.3s; margin-left: auto; margin-right: auto; }
    #prototype-content.view-desktop { max-width: 100%; }
    #prototype-content.view-tablet  { max-width: 820px; }
    #prototype-content.view-mobile  { max-width: 393px; }
  </style>
  <span class="dt-label">📱 Device:</span>
  <button data-device="desktop" class="active">Desktop</button>
  <button data-device="tablet">Tablet</button>
  <button data-device="mobile">Mobile</button>
  <span class="dt-size" id="dt-size">1440px</span>
</div>
<script>
  (function() {
    const toolbar = document.getElementById('device-toolbar');
    const content = document.getElementById('prototype-content');
    const sizeLabel = document.getElementById('dt-size');
    if (!toolbar || !content) return;
    const sizes = { desktop: 1440, tablet: 820, mobile: 393 };
    toolbar.querySelectorAll('button[data-device]').forEach(btn => {
      btn.addEventListener('click', function() {
        toolbar.querySelectorAll('button[data-device]').forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        const device = this.dataset.device;
        content.className = 'view-' + device;
        sizeLabel.textContent = sizes[device] + 'px';
      });
    });
  })();
</script>
```

### 4.2 Scaffold 模式（React 组件）

见第七节 `src/components/DeviceToolbar.tsx`。

---

## 五、公共组件：PRD Panel

PRD Panel 展示 PMContext 中的事实/规则/验收/假设/待确认项，内嵌在原型右侧（桌面）或底部抽屉（移动）。D1 强化：批注可展开对应 PMContext 原文段落（heading + 上下文）。

### 5.1 简单模式（内联 HTML + JS）

```html
<div id="prd-panel">
  <style>
    #prd-panel-toggle {
      position: fixed; bottom: 16px; right: 16px; z-index: 9998;
      width: 44px; height: 44px; border-radius: var(--radius-full, 9999px);
      background: var(--color-primary, #2563eb); color: #fff;
      border: none; font-size: 20px; cursor: pointer;
      box-shadow: var(--shadow-lg, 0 10px 15px rgba(0,0,0,0.1));
    }
    #prd-panel-drawer {
      position: fixed; top: 42px; right: 0; bottom: 0; z-index: 9997;
      width: 380px; background: var(--color-bg, #fff);
      border-left: 1px solid var(--color-border, #e5e7eb);
      box-shadow: var(--shadow-lg, 0 10px 15px rgba(0,0,0,0.1));
      transform: translateX(100%); transition: transform 0.3s;
      overflow-y: auto; font-family: var(--font-sans, -apple-system, sans-serif);
      font-size: var(--font-size-sm, 0.875rem);
    }
    #prd-panel-drawer.open { transform: translateX(0); }
    #prd-panel-drawer .prd-header {
      padding: var(--space-md, 16px); border-bottom: 1px solid var(--color-border, #e5e7eb);
      font-weight: 600; color: var(--color-text, #1f2937);
      display: flex; justify-content: space-between; align-items: center;
    }
    #prd-panel-drawer .prd-header button { background: none; border: none; font-size: 18px; cursor: pointer; color: var(--color-text-muted, #9ca3af); }
    #prd-panel-drawer .prd-section { padding: var(--space-sm, 8px) var(--space-md, 16px); border-bottom: 1px solid var(--color-border-light, #f3f4f6); }
    #prd-panel-drawer .prd-section h4 { margin: var(--space-sm, 8px) 0; color: var(--color-text, #1f2937); font-size: var(--font-size-base, 1rem); cursor: pointer; }
    #prd-panel-drawer .prd-item { padding: 4px 0; color: var(--color-text-secondary, #6b7280); display: flex; gap: 6px; }
    #prd-panel-drawer .prd-item .tag { display: inline-block; padding: 1px 6px; border-radius: var(--radius-sm, 4px); font-size: 0.75rem; font-weight: 500; flex-shrink: 0; }
    #prd-panel-drawer .prd-source { display: none; padding: var(--space-xs, 4px) var(--space-sm, 8px); background: var(--color-bg-tertiary, #f3f4f6); border-radius: var(--radius-sm, 4px); margin: 4px 0; font-family: var(--font-mono, monospace); font-size: 0.75rem; white-space: pre-wrap; color: var(--color-text-secondary, #6b7280); }
    #prd-panel-drawer .prd-section.expanded .prd-source { display: block; }
    .tag-fact { background: #dbeafe; color: #1d4ed8; }
    .tag-rule { background: #fef3c7; color: #b45309; }
    .tag-accept { background: #d1fae5; color: #047857; }
    .tag-assump { background: #e0e7ff; color: #4338ca; }
    .tag-tbc { background: #fce7f3; color: #be185d; }
    .prd-empty { padding: var(--space-xl, 32px) var(--space-md, 16px); text-align: center; color: var(--color-text-muted, #9ca3af); }
    @media (max-width: 640px) {
      #prd-panel-drawer { width: 100%; top: auto; bottom: 0; height: 60vh; border-left: none; border-top: 1px solid var(--color-border, #e5e7eb); }
    }
  </style>
  <button id="prd-panel-toggle">📋</button>
  <div id="prd-panel-drawer">
    <div class="prd-header"><span>📋 PRD 批注</span><button id="prd-panel-close">✕</button></div>
    <div id="prd-panel-body"></div>
  </div>
</div>
<script>
  (function() {
    const toggle = document.getElementById('prd-panel-toggle');
    const drawer = document.getElementById('prd-panel-drawer');
    const close = document.getElementById('prd-panel-close');
    const body = document.getElementById('prd-panel-body');
    if (!toggle || !drawer || !close || !body) return;
    toggle.addEventListener('click', () => drawer.classList.toggle('open'));
    close.addEventListener('click', () => drawer.classList.remove('open'));
    const PRD_DATA = window.PRD_DATA || null;

    function renderPRD(data) {
      if (!data || (!data.pages && !data.facts)) {
        body.innerHTML = '<div class="prd-empty">⏳ 等待 pm-need 运行后填充<br><small>运行 /pm-need 生成 PMContext 后重试</small></div>';
        return;
      }
      let html = '';
      if (data.pages && data.pages.length > 0) {
        data.pages.forEach(page => {
          html += '<div class="prd-section" data-page="' + (page.id || '') + '">';
          html += '<h4 onclick="this.parentElement.classList.toggle(\'expanded\')">📄 ' + (page.name || page.title) + ' ▸</h4>';
          if (page.source) { html += '<div class="prd-source">' + page.source + '</div>'; }
          if (page.items) {
            page.items.forEach(item => {
              html += '<div class="prd-item"><span class="tag tag-' + item.type + '">' + item.label + '</span><span>' + item.text + '</span></div>';
            });
          }
          html += '</div>';
        });
      } else {
        ['facts','rules','acceptances','assumptions','tbc'].forEach(key => {
          const items = data[key];
          if (!items || items.length === 0) return;
          const labels = { facts: '事实', rules: '规则', acceptances: '验收', assumptions: '假设', tbc: '待确认' };
          const tags = { facts: 'fact', rules: 'rule', acceptances: 'accept', assumptions: 'assump', tbc: 'tbc' };
          html += '<div class="prd-section"><h4>' + labels[key] + '</h4>';
          items.forEach(text => { html += '<div class="prd-item"><span class="tag tag-' + tags[key] + '">' + labels[key] + '</span><span>' + text + '</span></div>'; });
          html += '</div>';
        });
      }
      body.innerHTML = html || '<div class="prd-empty">暂无批注数据</div>';
    }
    renderPRD(PRD_DATA);
  })();
</script>
```

### 5.2 Scaffold 模式

见第七节 `src/components/PrdPanel.tsx`。

---

## 六、简单模式完整模板

### 6.1 Vue3 CDN 模板

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>原型: {{PROJECT_NAME}}</title>
  <script src="https://unpkg.com/vue@3.4.0/dist/vue.global.prod.js"></script>
  <style>
    /* ===== Design Token（来自 DESIGN.md 或默认） ===== */
    :root { /* 见第二节默认 token 表，AI 代入 DESIGN.md 派生值 */ }
    @media (prefers-color-scheme: dark) { :root { /* dark token */ } }
    :root.dark { /* dark token */ }
    /* ===== 5 档断点（见第三节 3.1） ===== */
    /* ===== 组件样式：按钮/卡片/表单/导航/表格 ===== */
  </style>
</head>
<body>
  <!-- Device Toolbar (见第四节 4.1) -->
  <!-- PRD Panel (见第五节 5.1) -->
  <!-- 文档 overlay (见第九节) -->
  <div id="prototype-content">
    <nav>
      <a v-for="page in pages" :key="page.page_id" :href="'#page=' + page.page_id">{{ page.heading }}</a>
    </nav>
    <div id="pages-root"><!-- 由 renderPageSection(PROTOTYPE_CONTENT_PLAN.pages) 注入，禁止空 section --></div>
  </div>
  <script>
    // 必须内联第 0.5.3 节的 escapeHtml/renderPageSection/bindPageInteractions 函数
    const { createApp, ref, computed } = Vue;
    createApp({
      setup() {
        const contentPlan = {{PROTOTYPE_CONTENT_PLAN}};
        const pages = ref(contentPlan.pages || []);
        const currentPage = ref(location.hash.replace('#page=', '') || pages.value[0]?.page_id || 'home');
        window.PRD_DATA = {{PRD_DATA}};
        window.DOC_DATA = {{DOC_DATA}};
        window.PROTOTYPE_CONTENT_PLAN = contentPlan;
        const root = document.getElementById('pages-root');
        root.innerHTML = pages.value.map(renderPageSection).join('');
        bindPageInteractions(root);
        function syncRoute() {
          const id = location.hash.replace('#page=', '') || pages.value[0]?.page_id;
          currentPage.value = id;
          root.querySelectorAll('section[id^="page-"]').forEach(s => { s.style.display = s.id === 'page-' + id ? '' : 'none'; });
        }
        window.addEventListener('hashchange', syncRoute); syncRoute();
        return { pages, currentPage };
      }
    }).mount('#prototype-content');
  </script>
</body>
</html>
```

### 6.2 React CDN 模板

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>原型: {{PROJECT_NAME}}</title>
  <script src="https://unpkg.com/react@18.3.1/umd/react.production.min.js"></script>
  <script src="https://unpkg.com/react-dom@18.3.1/umd/react-dom.production.min.js"></script>
  <script src="https://unpkg.com/@babel/standalone@7.24.0/babel.min.js"></script>
  <style>/* 同 6.1 */</style>
</head>
<body>
  <div id="root"></div>
  <script type="text/babel">
    // 必须内联第 0.5.3 节的 escapeHtml/renderPageSection/bindPageInteractions 函数
    const { useState, useEffect } = React;
    const contentPlan = {{PROTOTYPE_CONTENT_PLAN}};
    const pages = contentPlan.pages || [];
    window.PROTOTYPE_CONTENT_PLAN = contentPlan;
    window.PRD_DATA = {{PRD_DATA}};
    window.DOC_DATA = {{DOC_DATA}};
    const App = () => {
      const [page, setPage] = useState(location.hash.replace('#page=', '') || pages[0]?.page_id || 'home');
      useEffect(() => {
        const root = document.getElementById('pages-root');
        bindPageInteractions(root);
        const sync = () => {
          const id = location.hash.replace('#page=', '') || pages[0]?.page_id;
          setPage(id);
          root.querySelectorAll('section[id^=\"page-\"]').forEach(s => { s.style.display = s.id === 'page-' + id ? '' : 'none'; });
        };
        window.addEventListener('hashchange', sync); sync();
        return () => window.removeEventListener('hashchange', sync);
      }, []);
      return (
        <div id="prototype-content">
          <nav>{pages.map(p => <a key={p.page_id} href={'#page=' + p.page_id}>{p.heading}</a>)}</nav>
          <div id="pages-root" dangerouslySetInnerHTML={{__html: pages.map(renderPageSection).join('')}} />
          {/* useEffect 中必须调用 bindPageInteractions(document.getElementById('pages-root'))，并按 hash 隐藏/显示 section，禁止空 section */}
        </div>
      );
    };
    ReactDOM.createRoot(document.getElementById('root')).render(<App />);
  </script>
</body>
</html>
```

### 6.3 Plain HTML 兜底模板

当检测到 Angular / 无框架 / 技术栈冲突或 CDN 不可达时使用。

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>原型: {{PROJECT_NAME}}</title>
  <style>/* 同 6.1 */</style>
</head>
<body>
  <div id="prototype-content">
    <nav id="prototype-nav"></nav>
    <div id="pages-root"></div>
  </div>
  <script>
    // 必须内联第 0.5.3 节的 escapeHtml/renderPageSection/bindPageInteractions 函数
    window.PROTOTYPE_CONTENT_PLAN = {{PROTOTYPE_CONTENT_PLAN}};
    window.PRD_DATA = {{PRD_DATA}};
    window.DOC_DATA = {{DOC_DATA}};
    const pages = window.PROTOTYPE_CONTENT_PLAN.pages || [];
    document.getElementById('prototype-nav').innerHTML = pages.map(p => `<a href="#page=${p.page_id}">${escapeHtml(p.heading)}</a>`).join('');
    document.getElementById('pages-root').innerHTML = pages.map(renderPageSection).join('');
    bindPageInteractions(document.getElementById('pages-root'));
    // L3: hash 路由 + section 切换 + 表单交互，section 已由 content plan 渲染
    function showPage(id) {
      const fallback = pages[0]?.page_id || 'home';
      const pageId = id || fallback;
      document.querySelectorAll('section[id^="page-"]').forEach(s => s.style.display = s.id === 'page-' + pageId ? '' : 'none');
    }
    const initial = location.hash.replace('#page=', '') || pages[0]?.page_id || 'home';
    showPage(initial);
    window.addEventListener('hashchange', () => showPage(location.hash.replace('#page=', '') || pages[0]?.page_id));
  </script>
</body>
</html>
```

### 6.4 体积超限自动拆分（仅简单模式）

E1 静态嵌入数据导致单 HTML 超 280KB 总上限时自动拆分：入口只保留目录索引 + 摘要，正文懒加载独立 `.js` chunk。

```
docs/pm-context/sketch/
├── prototype.html          # 入口：导航 + 摘要 + 拆分后的 chunk 引用
└── chunks/
    ├── page-home.js        # 单页内容 chunk
    ├── page-detail.js
    └── ...
```

```javascript
// prototype.html 中懒加载
async function loadPageChunk(pageId) {
  const mod = await import('./chunks/page-' + pageId + '.js');
  return mod.render(document.getElementById('prototype-content'));
}
```

> ⚠️ 拆分后单 HTML 仍需双击可打开（`file://` 协议下 ES module import 受 CORS 限制时退化为 `fetch` + `eval` 兜底，或在产物清单中提示需启动 HTTP server）。Scaffold 模式无体积上限，全部静态嵌入。

---

## 七、Scaffold 模式各文件模板

输出工程目录 `docs/pm-context/sketch/prototype/`，固定 React + TS + Vite + Tailwind v4。

### 7.1 目录结构（对齐 Axhub-Make + CONTEXT.md Q9）

```
docs/pm-context/sketch/prototype/
├── index.html              # Vite 入口 HTML
├── package.json
├── vite.config.ts
├── tsconfig.json
├── README.md               # 本地启动说明
└── src/
    ├── main.tsx            # ReactDOM.createRoot 挂载
    ├── App.tsx             # 主组件：路由 + 工具条 + 文档 overlay + PRD Panel
    ├── style.css           # @import "tailwindcss"; + Design Token CSS 变量
    ├── components/
    │   ├── DeviceToolbar.tsx
    │   ├── PrdPanel.tsx
    │   ├── DocOverlay.tsx
    │   ├── Toast.tsx
    │   ├── Modal.tsx
    │   └── PageShell.tsx   # 页面骨架（导航 + 角色帽 + 面包屑）
    ├── pages/
    │   ├── PageHome.tsx
    │   └── PageXxx.tsx     # 按 PMContext 页面定义生成
    ├── hooks/
    │   └── useHashPage.ts  # 对齐 Axhub useHashPage
    ├── data/
    │   ├── prd-data.ts     # PMContext 序列化（E1）
    │   ├── pages-config.ts # 页面配置列表
    │   └── mock-data.ts    # 表格/图表 mock
    └── assets/             # 原型专属图片
```

- 多页面通过 URL hash `#page=<pageId>` 定位（对齐 Axhub `useHashPage` hook）
- `pageId` 命名使用小写字母、数字、连字符
- 入口 `index.tsx` 顶部包含中文 `@name` 注释，用于预览列表展示

### 7.2 `package.json`

```json
{
  "name": "prototype-{{PROJECT_KEBAB}}",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "preview": "vite preview",
    "typecheck": "tsc --noEmit"
  },
  "dependencies": {
    "react": "^19.0.0",
    "react-dom": "^19.0.0"
  },
  "devDependencies": {
    "@tailwindcss/vite": "^4.0.0",
    "@types/react": "^19.0.0",
    "@types/react-dom": "^19.0.0",
    "@vitejs/plugin-react": "^4.0.0",
    "tailwindcss": "^4.0.0",
    "typescript": "^5.7.0",
    "vite": "^6.0.0"
  }
}
```

> 版本用 `^` 范围，随 npm 解析最新兼容版本，不锁定 patch。

### 7.3 `vite.config.ts`

```ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  base: './',   // 支持 file:// 协议直接打开产物
})
```

### 7.4 `tsconfig.json`

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "isolatedModules": true,
    "moduleDetection": "force",
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": false,
    "noUnusedParameters": false,
    "noFallthroughCasesInSwitch": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src"]
}
```

### 7.5 `index.html`

```html
<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>原型: {{PROJECT_NAME}}</title>
    <link rel="stylesheet" href="/src/style.css" />
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

### 7.6 `src/main.tsx`

```tsx
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App'
import './style.css'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>
)
```

### 7.7 `src/style.css`

```css
@import "tailwindcss";

/* === Design Token — 来自 DESIGN.md 或默认 === */
:root {
  --color-primary: {{COLOR_PRIMARY}};
  --color-primary-light: {{COLOR_PRIMARY_LIGHT}};
  --color-primary-dark: {{COLOR_PRIMARY_DARK}};
  --color-accent: {{COLOR_ACCENT}};
  --color-success: {{COLOR_SUCCESS}};
  --color-on-success: {{COLOR_ON_SUCCESS}};
  --color-warning: {{COLOR_WARNING}};
  --color-on-warning: {{COLOR_ON_WARNING}};
  --color-danger: {{COLOR_DANGER}};
  --color-on-danger: {{COLOR_ON_DANGER}};
  --color-info: {{COLOR_INFO}};
  --color-text: {{COLOR_TEXT}};
  --color-text-secondary: {{COLOR_TEXT_SECONDARY}};
  --color-text-muted: {{COLOR_TEXT_MUTED}};
  --color-bg: {{COLOR_BG}};
  --color-bg-secondary: {{COLOR_BG_SECONDARY}};
  --color-bg-tertiary: {{COLOR_BG_TERTIARY}};
  --color-border: {{COLOR_BORDER}};
  --color-border-light: {{COLOR_BORDER_LIGHT}};
  --space-xs: 4px; --space-sm: 8px; --space-md: 16px;
  --space-lg: 24px; --space-xl: 32px; --space-2xl: 48px;
  --radius-sm: 4px; --radius-md: 8px; --radius-lg: 12px; --radius-full: 9999px;
  --font-sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-mono: 'SF Mono', 'Fira Code', monospace;
}
@media (prefers-color-scheme: dark) {
  :root { /* dark token，同第二节 */ }
}
```

### 7.8 `src/hooks/useHashPage.ts`

对齐 Axhub-Make `src/common/useHashPage.ts` 接口，简化为原型内部使用版（去掉 host postMessage）。

```ts
import { useCallback, useEffect, useState } from 'react'

const PAGE_ID_RE = /^[a-z0-9-]+$/u

function normalizePageId(value: unknown): string {
  const id = typeof value === 'string' ? value.trim() : ''
  return PAGE_ID_RE.test(id) ? id : ''
}

function parseHashPage(hash: string): string | null {
  const raw = String(hash || '').replace(/^#/, '')
  return normalizePageId(new URLSearchParams(raw).get('page')) || null
}

export function useHashPage(defaultPage: string = 'home') {
  const normalizedDefault = normalizePageId(defaultPage) || 'home'
  const [page, setPageState] = useState<string>(() => {
    if (typeof window === 'undefined') return normalizedDefault
    return parseHashPage(window.location.hash) ?? normalizedDefault
  })

  useEffect(() => {
    if (typeof window === 'undefined') return undefined
    const onHashChange = () => {
      setPageState(parseHashPage(window.location.hash) ?? normalizedDefault)
    }
    window.addEventListener('hashchange', onHashChange)
    return () => window.removeEventListener('hashchange', onHashChange)
  }, [normalizedDefault])

  const setPage = useCallback((pageId: string) => {
    const next = normalizePageId(pageId)
    if (next && typeof window !== 'undefined') {
      window.location.hash = `page=${next}`
    }
  }, [])

  return { page, setPage }
}
```

### 7.9 `src/App.tsx`

```tsx
/**
 * @name {{PROJECT_NAME}}
 */
import { useHashPage } from './hooks/useHashPage'
import DeviceToolbar from './components/DeviceToolbar'
import PrdPanel from './components/PrdPanel'
import DocOverlay from './components/DocOverlay'
import { PAGES } from './data/pages-config'
import PageHome from './pages/PageHome'
// 其余页面按需 import

export default function App() {
  const { page, setPage } = useHashPage(PAGES[0]?.id || 'home')

  return (
    <div className="min-h-screen bg-[var(--color-bg)] text-[var(--color-text)]">
      <DeviceToolbar />
      {/* 导航：≤5 页 inline，>5 页 hamburger */}
      <nav className="flex gap-4 p-4 border-b border-[var(--color-border)]">
        {PAGES.map(p => (
          <a
            key={p.id}
            href={`#page=${p.id}`}
            className={page === p.id ? 'font-semibold text-[var(--color-primary)]' : 'text-[var(--color-text-secondary)]'}
          >
            {p.title}
          </a>
        ))}
      </nav>
      <main id="prototype-content" className="mx-auto max-w-7xl p-6 transition-all">
        {page === PAGES[0]?.id && <PageHome />}
        {/* 其余页面按需渲染 */}
      </main>
      <PrdPanel />
      <DocOverlay />
    </div>
  )
}
```

### 7.10 `src/components/DeviceToolbar.tsx`

```tsx
import { useState } from 'react'

const SIZES = { desktop: 1440, tablet: 820, mobile: 393 } as const
type Device = keyof typeof SIZES

export default function DeviceToolbar() {
  const [device, setDevice] = useState<Device>('desktop')

  return (
    <div className="fixed top-0 inset-x-0 z-[9999] flex items-center gap-2 px-4 py-2 bg-[var(--color-bg-secondary)] border-b border-[var(--color-border)] text-sm">
      <span className="text-[var(--color-text-secondary)] mr-2">📱 Device:</span>
      {(Object.keys(SIZES) as Device[]).map(d => (
        <button
          key={d}
          onClick={() => setDevice(d)}
          className={`px-3 py-1 rounded border cursor-pointer ${
            device === d
              ? 'bg-[var(--color-primary)] text-white border-[var(--color-primary)]'
              : 'bg-[var(--color-bg)] text-[var(--color-text)] border-[var(--color-border)]'
          }`}
        >
          {d.charAt(0).toUpperCase() + d.slice(1)}
        </button>
      ))}
      <span className="ml-auto text-[var(--color-text-muted)] font-mono">{SIZES[device]}px</span>
    </div>
  )
}
```

> Device Toolbar 仅作演示切换预览宽度。底层布局必须用 Tailwind 响应式前缀（`sm:`/`md:`/`lg:`/`xl:`/`2xl:`）真断点实现，不靠缩放作弊。

### 7.11 `src/components/PrdPanel.tsx`

```tsx
import { useState } from 'react'
import { PRD_DATA, PrdPage } from '../data/prd-data'

export default function PrdPanel() {
  const [open, setOpen] = useState(false)
  const [expanded, setExpanded] = useState<string | null>(null)

  return (
    <>
      <button
        onClick={() => setOpen(o => !o)}
        className="fixed bottom-4 right-4 z-[9998] w-11 h-11 rounded-full bg-[var(--color-primary)] text-white text-xl shadow-lg cursor-pointer border-none"
      >
        📋
      </button>
      <div
        className={`fixed top-[42px] right-0 bottom-0 z-[9997] w-[380px] bg-[var(--color-bg)] border-l border-[var(--color-border)] shadow-lg overflow-y-auto transition-transform ${
          open ? 'translate-x-0' : 'translate-x-full'
        }`}
      >
        <div className="flex justify-between items-center p-4 border-b border-[var(--color-border)] font-semibold">
          <span>📋 PRD 批注</span>
          <button onClick={() => setOpen(false)} className="bg-none border-none text-lg cursor-pointer text-[var(--color-text-muted)]">✕</button>
        </div>
        <div>
          {PRD_DATA.pages?.length ? (
            PRD_DATA.pages.map((p: PrdPage) => (
              <div key={p.id} className="p-2 px-4 border-b border-[var(--color-border-light)]">
                <h4
                  onClick={() => setExpanded(e => e === p.id ? null : p.id)}
                  className="my-2 cursor-pointer text-[var(--color-text)]"
                >
                  📄 {p.name || p.title} ▸
                </h4>
                {expanded === p.id && p.source && (
                  <pre className="p-2 bg-[var(--color-bg-tertiary)] rounded text-xs font-mono whitespace-pre-wrap text-[var(--color-text-secondary)]">{p.source}</pre>
                )}
                {p.items?.map((item, i) => (
                  <div key={i} className="py-1 flex gap-1.5 text-[var(--color-text-secondary)]">
                    <span className={`tag tag-${item.type} inline-block px-1.5 rounded text-xs font-medium shrink-0`}>{item.label}</span>
                    <span>{item.text}</span>
                  </div>
                ))}
              </div>
            ))
          ) : (
            <div className="p-8 text-center text-[var(--color-text-muted)]">
              ⏳ 等待 pm-need 运行后填充<br /><small>运行 /pm-need 生成 PMContext 后重试</small>
            </div>
          )}
        </div>
      </div>
    </>
  )
}
```

### 7.12 `src/components/DocOverlay.tsx`（D2 文档预览 overlay）

```tsx
import { useState, useEffect } from 'react'
import { DOC_DATA } from '../data/prd-data'

type DocEntry = { name: string; type: 'business' | 'design'; content: string }

export default function DocOverlay() {
  const [open, setOpen] = useState(false)
  const [active, setActive] = useState<DocEntry | null>(null)
  const [fetchedContent, setFetchedContent] = useState<string | null>(null)

  // E2 可选：运行时 fetch（仅 V3 验收环境有 dev server 时）
  useEffect(() => {
    if (!open || !active || active.type !== 'business') return
    fetch('./pm-context.md')
      .then(r => r.text())
      .then(setFetchedContent)
      .catch(() => setFetchedContent(null))  // 回退 E1
  }, [open, active])

  const entries: DocEntry[] = DOC_DATA.documentTree || []

  return (
    <>
      <button
        onClick={() => setOpen(o => !o)}
        className="fixed bottom-4 right-20 z-[9998] w-11 h-11 rounded-full bg-[var(--color-info)] text-white text-xl shadow-lg cursor-pointer border-none"
      >
        📄
      </button>
      {open && (
        <div className="fixed inset-0 z-[10001] bg-black/40 flex items-center justify-center" onClick={() => setOpen(false)}>
          <div className="bg-[var(--color-bg)] rounded-lg shadow-lg w-[90%] max-w-4xl h-[80vh] flex" onClick={e => e.stopPropagation()}>
            <div className="w-[200px] border-r border-[var(--color-border)] overflow-y-auto p-2">
              <div className="text-xs font-semibold text-[var(--color-text-muted)] mt-2 mb-1">业务依据</div>
              {entries.filter(e => e.type === 'business').map(e => (
                <button key={e.name} onClick={() => { setActive(e); setFetchedContent(null) }} className="block w-full text-left px-2 py-1 text-sm rounded hover:bg-[var(--color-bg-tertiary)] cursor-pointer">{e.name}</button>
              ))}
              <div className="text-xs font-semibold text-[var(--color-text-muted)] mt-3 mb-1">视觉依据</div>
              {entries.filter(e => e.type === 'design').map(e => (
                <button key={e.name} onClick={() => { setActive(e); setFetchedContent(null) }} className="block w-full text-left px-2 py-1 text-sm rounded hover:bg-[var(--color-bg-tertiary)] cursor-pointer">{e.name}</button>
              ))}
            </div>
            <div className="flex-1 overflow-y-auto p-4">
              {active ? (
                <pre className="whitespace-pre-wrap text-sm font-mono text-[var(--color-text)]">{fetchedContent ?? active.content}</pre>
              ) : (
                <div className="text-center text-[var(--color-text-muted)] py-8">选择左侧文件查看原文</div>
              )}
            </div>
            <button onClick={() => setOpen(false)} className="absolute top-2 right-2 bg-none border-none text-xl cursor-pointer text-[var(--color-text-muted)]">✕</button>
          </div>
        </div>
      )}
    </>
  )
}
```

### 7.13 `src/components/Toast.tsx` / `Modal.tsx`

简化实现，按需引入。L4 交互中用于错误恢复提示与确认弹窗。

### 7.14 `src/components/PageShell.tsx`（L4 骨架）

```tsx
import { ReactNode } from 'react'

export default function PageShell({ title, role, breadcrumb, children }: {
  title: string; role?: string; breadcrumb?: string[]; children: ReactNode
}) {
  return (
    <section className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">{title}</h1>
        {role && <span className="px-2 py-1 rounded bg-[var(--color-bg-tertiary)] text-xs text-[var(--color-text-secondary)]">角色: {role}</span>}
      </div>
      {breadcrumb && <nav className="text-sm text-[var(--color-text-muted)]">{breadcrumb.join(' / ')}</nav>}
      {children}
    </section>
  )
}
```

### 7.15 `src/pages/PageXxx.tsx`（L4 页面骨架）

```tsx
import { useState, useEffect } from 'react'
import PageShell from '../components/PageShell'

type Status = 'loading' | 'empty' | 'success' | 'error'

export default function PageHome() {
  const [status, setStatus] = useState<Status>('loading')
  const [data, setData] = useState<any[]>([])
  // L3: 表单状态 + hash 导航
  const [formData, setFormData] = useState({ /* ... */ })

  // L4: 四态全覆盖
  useEffect(() => {
    setStatus('loading')
    // 模拟异步
    const t = setTimeout(() => {
      try {
        setData([/* mock */])
        setStatus(data.length === 0 ? 'empty' : 'success')
      } catch {
        setStatus('error')
      }
    }, 500)
    return () => clearTimeout(t)
  }, [])

  return (
    <PageShell title="页面标题" role="采购员" breadcrumb={['首页', '当前页']}>
      {status === 'loading' && <div className="text-[var(--color-text-muted)]">加载中...</div>}
      {status === 'empty' && <div className="text-[var(--color-text-muted)]">暂无数据</div>}
      {status === 'error' && (
        <div className="p-4 rounded bg-red-50 text-[var(--color-danger)]">
          加载失败 <button onClick={() => location.reload()} className="underline cursor-pointer">重试</button>
        </div>
      )}
      {status === 'success' && (
        <>
          {/* 表单/表格/卡片 + 交互按钮（L3 表单提交后 hash 跳转下一页） */}
          <button onClick={() => location.hash = 'page=detail'} className="px-4 py-2 bg-[var(--color-primary)] text-white rounded cursor-pointer">下一步</button>
        </>
      )}
    </PageShell>
  )
}
```

L4 增强要点：角色切换（App 顶部角色帽组件）+ 权限分支（按 role 渲染不同操作）+ 错误恢复路径（重试按钮）+ 加载/空/成功/失败四态。

### 7.16 `src/data/prd-data.ts`（E1 静态嵌入）

```ts
// 由 pm-sketch 在生成时从 PMContext + PRD + DESIGN.md 读取并序列化
// 来源：docs/pm-context/pm-context.md + docs/pm-context/prd/*.md + docs/design/DESIGN.md

export type PrdItemType = 'fact' | 'rule' | 'accept' | 'assump' | 'tbc'
export interface PrdItem { type: PrdItemType; label: string; text: string }
export interface PrdPage {
  id: string
  name: string
  title: string
  source?: string  // PMContext 原文段落（D1 展开用）
  items?: PrdItem[]
}
export interface DocEntry { name: string; type: 'business' | 'design'; content: string }

export const PRD_DATA: {
  projectName: string
  pages: PrdPage[]
  facts: string[]; rules: string[]; acceptances: string[]
  assumptions: string[]; tbc: string[]
} = {{PRD_DATA}}

export const DOC_DATA: {
  pmContext: string
  designMd: string
  documentTree: DocEntry[]
} = {{DOC_DATA}}
```

### 7.17 `src/data/pages-config.ts`

```ts
export interface PageConfig { id: string; title: string }
export const PAGES: PageConfig[] = {{PAGES_DATA}}
```

### 7.18 `src/data/mock-data.ts`

```ts
// 根据 PMContext 数据模型自动生成，供表格/图表展示
export const MOCK_DATA = {{MOCK_DATA}}
```

### 7.19 `README.md`（本地启动说明）

```markdown
# 原型预览说明

> 由 `/pm-sketch --prototype` 生成的 Scaffold 模式可交互原型（React + TS + Vite + Tailwind v4）。

## 本地启动

\`\`\`bash
npm install
npm run dev      # 开发模式，访问 http://localhost:5173
npm run build    # 生产构建
npm run preview  # 预览生产构建
\`\`\`

## 验收

\`\`\`bash
npm run typecheck   # tsc --noEmit
npm run build       # vite build
\`\`\`

## 文件说明

| 文件/目录 | 作用 |
|----------|------|
| `src/App.tsx` | 主组件：路由 + 工具条 + 文档 overlay + PRD Panel |
| `src/hooks/useHashPage.ts` | hash 路由 hook（对齐 Axhub-Make） |
| `src/components/` | DeviceToolbar / PrdPanel / DocOverlay / Toast / Modal / PageShell |
| `src/pages/` | 多页面原型页面组件 |
| `src/data/` | PRD 数据 + 页面配置 + mock 数据 |

## 注意事项

- 原型基于 PMContext 生成，所有 `<section>` 对应 PMContext 页面定义
- `[假设]` 标注的图元以灰色占位展示，表示尚未确认
- 多页面通过 `#page=<pageId>` 定位
```

---

## 八、Toast / Modal 组件

### 8.1 简单模式（内联）

```html
<style>
  #toast-container { position: fixed; top: 56px; right: 16px; z-index: 10000; display: flex; flex-direction: column; gap: 8px; }
  .toast { padding: 12px 16px; border-radius: var(--radius-md, 8px); font-family: var(--font-sans, sans-serif); font-size: var(--font-size-sm, 0.875rem); color: #fff; box-shadow: var(--shadow-md, 0 4px 6px rgba(0,0,0,0.07)); animation: toast-in 0.3s ease; max-width: 360px; }
  .toast.success { background: var(--color-success, #10b981); }
  .toast.error   { background: var(--color-danger, #ef4444); }
  .toast.warning { background: var(--color-warning, #f59e0b); }
  .toast.info    { background: var(--color-info, #3b82f6); }
  @keyframes toast-in { from { opacity: 0; transform: translateX(20px); } to { opacity: 1; transform: translateX(0); } }
</style>
<div id="toast-container"></div>
<script>
  function showToast(message, type = 'info', duration = 3000) {
    const container = document.getElementById('toast-container');
    if (!container) return;
    const el = document.createElement('div');
    el.className = 'toast ' + type;
    el.textContent = message;
    container.appendChild(el);
    setTimeout(() => el.remove(), duration);
  }
  function showModal(title, bodyHTML) {
    const overlay = document.createElement('div');
    overlay.className = 'modal-overlay';
    overlay.style.cssText = 'position:fixed;inset:0;z-index:10001;background:rgba(0,0,0,0.4);display:flex;align-items:center;justify-content:center;';
    overlay.innerHTML = '<div style="background:var(--color-bg,#fff);border-radius:var(--radius-lg,12px);box-shadow:var(--shadow-lg);max-width:560px;width:90%;max-height:80vh;overflow-y:auto;padding:var(--space-lg,24px);"><div style="font-weight:600;font-size:var(--font-size-lg,1.125rem);margin-bottom:var(--space-md,16px);">' + title + '</div><div>' + bodyHTML + '</div><button onclick="this.closest(\'.modal-overlay\').remove()" style="margin-top:var(--space-md,16px);padding:8px 16px;background:var(--color-primary,#2563eb);color:#fff;border:none;border-radius:var(--radius-sm,4px);cursor:pointer;">关闭</button></div>';
    overlay.addEventListener('click', function(e) { if (e.target === this) this.remove(); });
    document.body.appendChild(overlay);
  }
</script>
```

### 8.2 Scaffold 模式

`src/components/Toast.tsx` / `Modal.tsx` 简化为 React 组件，按需引入，用于 L4 错误恢复提示与确认弹窗。

---

## 九、文档预览 Overlay（D2）

### 9.1 简单模式（内联）

```html
<button id="doc-overlay-toggle" style="position:fixed;bottom:16px;right:80px;z-index:9998;width:44px;height:44px;border-radius:var(--radius-full,9999px);background:var(--color-info,#3b82f6);color:#fff;border:none;font-size:20px;cursor:pointer;box-shadow:var(--shadow-lg);">📄</button>
<div id="doc-overlay" style="display:none;position:fixed;inset:0;z-index:10001;background:rgba(0,0,0,0.4);align-items:center;justify-content:center;">
  <div style="background:var(--color-bg,#fff);border-radius:var(--radius-lg,12px);box-shadow:var(--shadow-lg);width:90%;max-width:960px;height:80vh;display:flex;position:relative;">
    <div id="doc-tree" style="width:200px;border-right:1px solid var(--color-border,#e5e7eb);overflow-y:auto;padding:8px;"></div>
    <div id="doc-content" style="flex:1;overflow-y:auto;padding:16px;"><pre id="doc-pre" style="white-space:pre-wrap;font-family:var(--font-mono,monospace);font-size:0.875rem;"></pre></div>
    <button onclick="document.getElementById('doc-overlay').style.display='none'" style="position:absolute;top:8px;right:8px;background:none;border:none;font-size:20px;cursor:pointer;color:var(--color-text-muted,#9ca3af);">✕</button>
  </div>
</div>
<script>
  (function() {
    const toggle = document.getElementById('doc-overlay-toggle');
    const overlay = document.getElementById('doc-overlay');
    const tree = document.getElementById('doc-tree');
    const pre = document.getElementById('doc-pre');
    if (!toggle || !overlay || !tree || !pre) return;
    toggle.addEventListener('click', () => overlay.style.display = overlay.style.display === 'none' ? 'flex' : 'none');
    overlay.addEventListener('click', e => { if (e.target === overlay) overlay.style.display = 'none'; });

    const DOC_DATA = window.DOC_DATA || { documentTree: [] };
    // 分区：业务依据 + 视觉依据
    const sections = { business: '业务依据', design: '视觉依据' };
    Object.entries(sections).forEach(([type, label]) => {
      const h = document.createElement('div');
      h.style.cssText = 'font-size:0.75rem;font-weight:600;color:var(--color-text-muted,#9ca3af);margin:8px 0 4px;';
      h.textContent = label;
      tree.appendChild(h);
      (DOC_DATA.documentTree || []).filter(e => e.type === type).forEach(e => {
        const btn = document.createElement('button');
        btn.textContent = e.name;
        btn.style.cssText = 'display:block;width:100%;text-align:left;padding:4px 8px;font-size:0.875rem;border:none;background:none;cursor:pointer;border-radius:var(--radius-sm,4px);';
        btn.onmouseenter = () => btn.style.background = 'var(--color-bg-tertiary,#f3f4f6)';
        btn.onmouseleave = () => btn.style.background = '';
        btn.onclick = () => { pre.textContent = e.content; };
        tree.appendChild(btn);
      });
    });
  })();
</script>
```

### 9.2 Scaffold 模式

见第七节 `src/components/DocOverlay.tsx`。E1 默认；E2（V3 验收环境可选）运行时 `fetch('./pm-context.md')`，失败回退 E1。

### 9.3 轻量 Markdown 渲染（不依赖外部库）

两模式均用纯字符串替换渲染（仅支持 `#`/`##`/`###` heading、`**bold**`、`` `code` ``、`- list`、段落）：

```javascript
function renderMarkdown(md) {
  return md
    .replace(/^### (.+)$/gm, '<h3>$1</h3>')
    .replace(/^## (.+)$/gm, '<h2>$1</h2>')
    .replace(/^# (.+)$/gm, '<h1>$1</h1>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/`(.+?)`/g, '<code>$1</code>')
    .replace(/^- (.+)$/gm, '<li>$1</li>')
    .replace(/\n\n/g, '</p><p>')
    .replace(/^([^<].+)$/gm, '<p>$1</p>');
}
```

> overlay 默认 `<pre>` 原文渲染（spec-template 风格），Markdown 渲染为可选增强。

---

## 十、验收脚本

### 10.1 V2 验收（Scaffold 模式默认）

```bash
cd "$PROTOTYPE_DIR"   # docs/pm-context/sketch/prototype
npm install 2>&1 || exit 1
npx tsc --noEmit 2>&1 || exit 2
npx vite build 2>&1 || exit 3
echo "✅ V2 验收通过"
```

### 10.2 V3 验收（Scaffold 模式初次生成 / 大改动）

```bash
cd "$PROTOTYPE_DIR"
npm install 2>&1 || exit 1
npx tsc --noEmit 2>&1 || exit 2
npx vite build 2>&1 || exit 3

# 启动 dev server 后台
npx vite --port 4173 &
VITE_PID=$!
sleep 3

# 端口可达性检查
curl -s -o /dev/null -w "%{http_code}" http://localhost:4173 || exit 4

# headless 浏览器查 console 错误（环境具备时）
if command -v chromium &>/dev/null || command -v google-chrome &>/dev/null; then
  CHROME=$(command -v chromium || command -v google-chrome)
  "$CHROME" --headless --no-sandbox --dump-dom http://localhost:4173 2>&1 \
    | grep -i "error\|uncaught\|exception" && exit 5
fi

kill $VITE_PID 2>/dev/null
echo "✅ V3 验收通过"
```

### 10.3 V3 环境检测

```bash
has_chrome=false
command -v chromium &>/dev/null && has_chrome=true
command -v google-chrome &>/dev/null && has_chrome=true
command -v curl &>/dev/null || { echo "❌ V3 需要 curl"; exit 1; }
# 无 headless 浏览器时跳过 console 检查，只做端到端可达性验证
```

### 10.4 降级输出格式

V3 → V2 → V1 各级均失败后输出：

```markdown
# ⚠️ 原型未验收 — 错误清单

> 验收流程: V3 → V2 → V1，各级均失败后降级输出，不静默撒谎

## 错误详情

| 步骤 | 状态 | 错误信息 |
|------|------|---------|
| npm install | ❌ | 依赖解析失败: xxx |
| tsc --noEmit | — | 未执行（前置失败） |
| vite build | — | 未执行（前置失败） |

## 已知问题

- 依赖 xxx 版本不兼容，建议手动检查 package.json
- 生成的文件已落盘至 `docs/pm-context/sketch/prototype/`，修复后可手动执行 `npm install && npm run build`

## 影响评估

- 简单演示: 部分可用（直接双击 index.html 查看基础布局）
- 完整功能: 不可用（需要修复构建问题）
```

---

## 十一、反例黑名单（新增，SKILL.md 同步）

| 反模式 | 为什么不要做 |
|--------|------------|
| Scaffold 模式生成后不运行验收即打 ✅ 标记完成 | 系统性撒谎——PM 拿到一个 `npm install` 都跑不起来的工程 |
| 简单模式超 280KB 不拆分不提示 | 体积门是质量底线，超限静默输出等于隐藏缺陷 |
| Scaffold 模式没有 package.json / vite.config.ts 就输出 `.tsx` 文件 | 与工程脚手架承诺不符，用户拿到的是不可运行的碎片 |
| 简单模式和 Scaffold 模式共用同一套 Design Token 模板 | 两模式 token 引入方式不同（inline vs CSS file + Tailwind），混用导致 Scaffold 工程出现 CDN script tag |
| V3 验收失败后直接跳过不降级（静默改打 ✅） | 与降级链契约矛盾，应诚实降级 |
| 简单模式只输出路由骨架不渲染页面内容（空壳） | 违反 L3 底线，等于交付未实施的需求，判定 Failure；必须从 `prototype-content-plan.json` 渲染 `data-trace-ref` 业务元素 |
| 页面覆盖率 < PMContext 页面数仍打 ✅ | 系统性撒谎，PM 拿到缺页原型 |
| 每页业务元素 < 5 且未标注原因 | 页面等于空壳，必须降级并记入信息缺口 |
| 增量迭代时全量重生成原型覆盖已开发页面 | 摧毁用户迭代成果，等于不支持增量 |
| 新增页面时不更新菜单/路由 | 新页面不可达，等于没加 |

---

## 十二、AI 生成约束

### 12.1 模板变量占位符

`prototype-templates.md` 中使用 `{{VARIABLE_NAME}}` 占位，AI 生成时替换：

| 占位符 | 来源 | 说明 |
|--------|------|------|
| `{{PROJECT_NAME}}` | PMContext 标题 | 原型标题 |
| `{{PROJECT_KEBAB}}` | PMContext 标题 kebab-case | package.json name |
| `{{COLOR_*}}` | DESIGN.md / `prototype-design-profile.json` / 默认 | 派生 token 值 |
| `{{DESIGN_PROFILE}}` | `prototype-design-profile.json` | Design Read、风格家族、三拨盘、layout/interaction patterns |
| `{{PAGES_DATA}}` | PMContext 页面定义 | JS/TS 数组，含页面 title/字段/规则/验收 |
| `{{PRD_DATA}}` | PMContext + PRD 文件 | PRD Panel 数据（含 source 字段供 D1 展开） |
| `{{DOC_DATA}}` | PMContext + DESIGN.md 原文 | 文档 overlay 数据 |
| `{{MOCK_DATA}}` | 数据模型推断 | 表格/图表 mock |

### 12.2 模板选择流程

```text
1. 执行 Step -1 复杂度判断 → 确定简单/Scaffold 模式
2. 执行 Step 0 技术栈决策：
   - 简单模式 → 检测/推荐 Vue3/React/Plain（CDN）
   - Scaffold 模式 → 固定 React + TS + Vite + Tailwind v4
3. 执行 design-style 编译 → 写 `prototype-design-profile.json`，再执行 DESIGN.md 扫描 → 派生 token 表（第一节协议）
4. 根据模式选择对应模板节：
   - 简单模式 → 第六节（6.1/6.2/6.3 按技术栈选）
   - Scaffold 模式 → 逐文件生成第七节各文件
5. 填写占位符 → 生成产物
6. 执行验收（按 Acceptance Tier）：
   - 简单模式 → V1
   - Scaffold 模式 → V2 / V3
```

---

## 十三、质量清单（分模式）

### 13.0 Pencil MCP 模式

- [ ] ✅ 已检测到可用 Pencil MCP，且具备 create/update 与 export/persist 能力
- [ ] ✅ `docs/pm-context/sketch/pencil/pencil-prototype-manifest.json` 存在
- [ ] ✅ manifest `pages` 覆盖 PMContext 页面 heading，screen 数 ≥ 页面数
- [ ] ✅ manifest `interactions` 覆盖关键 state/flow edge；未覆盖项显式标 `[待确认]`
- [ ] ✅ manifest `components` 中规则/验收均有来源锚点
- [ ] ✅ manifest `exports` 至少包含一个本地路径或远端 artifact id
- [ ] ✅ manifest `design_profile` 指向 `docs/pm-context/sketch/prototype-design-profile.json`
- [ ] ✅ manifest `style_family` / `ue_coverage` 存在，且 UE 覆盖不足项标 `[待确认]`
- [ ] ✅ MCP 失败时 manifest `status=fallback-local` 且本地 Simple/Scaffold fallback 已完成

### 13.1 简单模式（CDN HTML）— V1 硬校验

以下为 V1 硬校验，不满足禁止打 ✅，必须降级并列出缺失：

- [ ] ✅ **页面覆盖率闸**：原型内 `<section>`（或路由目标页）数量 **≥ PMContext `## <页面>` heading 数**。每个 PMContext 页面必须有对应可导航目标页
- [ ] ✅ **每页内容密度闸**：每个页面 `<section>` 内**非导航业务元素**（表单项 / 表格 / 列表 / 卡片 / 按钮，排除顶栏与菜单）节点数 **≥ 5**，其中至少 3 个带 `data-trace-ref`。不足 5 个须标注原因
- [ ] ✅ **交互底线闸（L3）**：每个 `<section>` 至少 1 个绑定 JS 事件的交互元素；hash 路由的每个目标页必须存在对应 section（不得指向空锚点）；`inspectRouteShell()` 必须全部 passed
- [ ] ✅ **PMContext 映射闸**：每个页面的「规则 / 验收」必须在对应页面渲染出可见元素（规则→`p.rule`，验收→`ul.acceptance`），不得只渲染标题
- [ ] ✅ 单 HTML < 280KB（超限自动拆分懒加载，见 6.4）
- [ ] ✅ 双击可打开（无跨域/CORS 问题）
- [ ] ✅ 使用 CDN 框架（检测/推荐的版本，不写 `latest`）
- [ ] ✅ Design Token CSS 变量（无裸 `#hex`，来自 DESIGN.md + prototype-design-profile 或默认）
- [ ] ✅ 5 档响应式断点（手写 `@media`）
- [ ] ✅ Device Toolbar 三端切换（1440/820/393）
- [ ] ✅ PRD Panel 展示批注（D1 可展开 PMContext 原文）
- [ ] ✅ 文档 overlay 可展开查看 PMContext / DESIGN.md
- [ ] ✅ 暗色主题适配（`@media prefers-color-scheme: dark` 或 `--dark`）
- [ ] ✅ V1 自检通过

**V1 反空壳自检输出块**（生成后必须打印，`--auto` 也打印即使不暂停）：
```
✅ 反空壳体检:
   - 页面覆盖率: 已实现 <M> / PMContext <N> 个页面
   - 每页交互元素计数: [页面A: x, 页面B: y, ...]
   - 未达标页面: <列表 或 无>
   - 路由空壳检测: <通过 / 失败，失败页列表>
```

### 13.2 Scaffold 模式（Vite 工程）

- [ ] ✅ 目录结构对齐 7.1（含 package.json / vite.config.ts / tsconfig.json）
- [ ] ✅ package.json 包含所有必要依赖（React 19 + Vite 6 + Tailwind v4 + TS 5.7）
- [ ] ✅ Vite + React + TS + Tailwind v4 配置完整
- [ ] ✅ Design Token + prototype-design-profile 在 `style.css` 中（`@import "tailwindcss";` 之后）
- [ ] ✅ 5 档断点（Tailwind 响应式前缀 `sm:`/`md:`/`lg:`/`xl:`/`2xl:`）
- [ ] ✅ Device Toolbar + PRD Panel + DocOverlay 三组件完整
- [ ] ✅ 多页 hash 路由（`useHashPage` hook，对齐 Axhub）
- [ ] ✅ L4 交互：角色切换 + 权限分支 + 错误恢复 + 加载/空/成功/失败四态
- [ ] ✅ 所有 route/page 对应 PMContext 页面定义，页面根节点带 `data-trace-page="<PMContext heading>"`
- [ ] ✅ 每页至少 3 个业务元素带 `data-trace-ref`，指向 `prototype-content-plan.json` 的 facts/rules/acceptances/actions 来源
- [ ] ✅ 每页至少 5 个非导航业务元素、1 个真实交互；`TODO` / `敬请期待` / `占位` / 只有标题或菜单均判定为**路由空壳**并阻断完成
- [ ] ✅ `index.tsx` 顶部含中文 `@name` 注释
- [ ] ✅ `README.md` 含本地启动命令
- [ ] ✅ V2/V3 验收通过或诚实降级（输出错误清单，不静默撒谎）

### 13.3 通用基础检查

- [ ] ✅ 技术栈决策有依据（新项目推荐 / 老项目扫描 `package.json`）
- [ ] ✅ `prototype-design-profile.json` 存在并被当前实现模式消费
- [ ] ✅ 所有页面/组件对应 PMContext 中的实体/关系，无法对应标 `[假设]`
- [ ] ✅ UTF-8 编码，中文字符正常显示
- [ ] ✅ Electron 或移动端适配标注已添加（如适用）

---

## 十四、适配标注片段

### 14.1 Electron 标注

检测到或推荐 Electron 时，在原型顶部加：

```html
<!-- 🖥 此原型推荐用 Electron 包装运行。Electron 主进程配置见 electron/main.js -->
```

### 14.2 移动端适配

检测到或推荐 Flutter / React Native 时，HTML 原型不适用，输出 `design-spec.md` 替代，包含屏幕设计说明 + 组件规范 + 交互描述。

### 14.3 R3 移动端手势（仅 Scaffold 模式 + PMContext 含移动端角色）

启用 swipe / pull-to-refresh / bottom tab 时，在对应页面组件中引入手势库（如 `@use-gesture/react`），并在 `package.json` 中声明依赖。简单模式不实现 R3。


## 十四、视觉可见性审计脚本

本仓库提供 `scripts/visual_audit_prototype.py` 作为本地确定性兜底。Simple 模式生成后必须运行：

```bash
python scripts/visual_audit_prototype.py --token-digest <design-source-manifest.token_digest> docs/pm-context/sketch/prototype.html > docs/pm-context/sketch/visual-audit-report.json
```

Scaffold 模式生成后必须运行：

```bash
python scripts/visual_audit_prototype.py --token-digest <design-source-manifest.token_digest> docs/pm-context/sketch/prototype > docs/pm-context/sketch/visual-audit-report.json
```

若脚本返回非 0，说明至少存在一处低对比或不可见交互元素；必须先修 token / 组件状态 / focus ring，再重新验收。该脚本是 V1 兜底，V3 场景应额外用 headless browser 读取 computed style 与截图，防止 class 合成后出现不可见状态。
