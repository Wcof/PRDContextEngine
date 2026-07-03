# HTML 原型模板集

> 由 `/pm-sketch --prototype` 根据技术栈决策结果选用的 HTML 模板。详见 `SKILL.md` 的「Step 0：技术栈决策」和「HTML 原型」节。

## 一、技术栈模板

### Vue3 CDN 模板

当检测到 Vue3 或新项目推荐 Vue3 时使用。

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>原型: <需求名></title>
  <script src="https://unpkg.com/vue@3/dist/vue.global.prod.js"></script>
  <style>
    /* 布局：响应式网格 */
    /* 颜色：从 PMContext 的品牌色提取，无品牌色用 #2563eb 默认蓝 */
    /* 字体：系统字体栈 -apple-system, BlinkMacSystemFont, 'Segoe UI' */
    /* 组件：按钮/卡片/表单/导航 四个原语，使用 Vue 的 class/style 绑定 */
  </style>
</head>
<body>
  <div id="app">
    <nav>
      <a v-for="page in pages" :key="page.id" :href="'#' + page.id">{{ page.name }}</a>
    </nav>
    <section v-for="page in pages" :key="page.id" :id="page.id">
      <h1>{{ page.title }}</h1>
    </section>
  </div>
  <script>
    const { createApp, ref, computed } = Vue
    const app = createApp({
      setup() {
        const pages = ref([/* 从 PMContext 提取的页面数据 */])
        return { pages }
      }
    })
    app.mount('#app')
  </script>
</body>
</html>
```

### React CDN 模板

当检测到 React 或新项目推荐 React 时使用。

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>原型: <需求名></title>
  <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
  <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
  <style>
    /* 布局：响应式网格 */
    /* 颜色：从 PMContext 的品牌色提取，无品牌色用 #2563eb 默认蓝 */
    /* 字体：系统字体栈 -apple-system, BlinkMacSystemFont, 'Segoe UI' */
    /* 组件：按钮/卡片/表单/导航 四个原语 */
  </style>
</head>
<body>
  <div id="root"></div>
  <script type="text/babel">
    const { useState, useEffect } = React
    const pages = [/* 从 PMContext 提取的页面数据 */]

    const App = () => (
      <>
        <nav>
          {pages.map(p => <a key={p.id} href={'#'+p.id}>{p.name}</a>)}
        </nav>
        {pages.map(p => (
          <section key={p.id} id={p.id}>
            <h1>{p.title}</h1>
          </section>
        ))}
      </>
    )

    ReactDOM.createRoot(document.getElementById('root')).render(<App />)
  </script>
</body>
</html>
```

### Plain HTML 兜底模板

当检测到 Angular / 无框架 / 技术栈冲突或 CDN 不可达时使用。

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>原型: <需求名></title>
  <style>
    /* 布局：响应式网格 */
    /* 颜色：从 PMContext 的品牌色提取，无品牌色用 #2563eb 默认蓝 */
    /* 字体：系统字体栈 -apple-system, BlinkMacSystemFont, 'Segoe UI' */
    /* 组件：按钮/卡片/表单/导航 四个原语 */
  </style>
</head>
<body>
  <nav>
    <a href="#page1">页面1</a>
    <a href="#page2">页面2</a>
  </nav>
  <section id="page1">
    <h1>页面1: <名称></h1>
  </section>
  <section id="page2">
    <h1>页面2: <名称></h1>
  </section>
  <script>
    // 交互：页面切换、表单验证、状态切换（可选）
  </script>
</body>
</html>
```

---

## 二、Design Token CSS 片段

所有 HTML 原型必须使用 CSS 自定义属性定义 Design Token，禁止裸 `#hex` 色值。

```css
/* ========================================
   Design Token — 原型级变量
   使用方式：var(--color-primary)
   ======================================== */

/* 品牌色（从 PMContext 品牌色提取，无可识别品牌色时使用默认蓝） */
:root {
  --color-primary: #2563eb;
  --color-primary-light: #60a5fa;
  --color-primary-dark: #1d4ed8;
  --color-accent: #f59e0b;
  --color-accent-light: #fbbf24;

  /* 语义色 */
  --color-success: #10b981;
  --color-warning: #f59e0b;
  --color-danger: #ef4444;
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
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;
  --space-2xl: 48px;

  /* 圆角 */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-full: 9999px;

  /* 阴影 */
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
  --shadow-md: 0 4px 6px rgba(0,0,0,0.07);
  --shadow-lg: 0 10px 15px rgba(0,0,0,0.1);

  /* 字体 */
  --font-sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  --font-mono: 'SF Mono', 'Fira Code', 'Fira Mono', monospace;
  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.125rem;
  --font-size-xl: 1.25rem;
  --font-size-2xl: 1.5rem;

  /* 断点（仅参考，CSS 变量不参与 media query）:
     Mobile:  ≤ 640px
     Tablet:  641px - 1024px
     Desktop: ≥ 1025px
     实际响应用 @media (max-width: 640px) / (min-width: 1025px) */
}

/* 暗色主题 */
@media (prefers-color-scheme: dark) {
  :root {
    --color-text: #f3f4f6;
    --color-text-secondary: #9ca3af;
    --color-text-muted: #6b7280;
    --color-bg: #111827;
    --color-bg-secondary: #1f2937;
    --color-bg-tertiary: #374151;
    --color-border: #374151;
    --color-border-light: #4b5563;
    --shadow-sm: 0 1px 2px rgba(0,0,0,0.3);
    --shadow-md: 0 4px 6px rgba(0,0,0,0.4);
    --shadow-lg: 0 10px 15px rgba(0,0,0,0.5);
  }
}

/* --dark 参数强制暗色（由 JS 注入 .dark 类覆盖） */
:root.dark {
  --color-text: #f3f4f6;
  --color-text-secondary: #9ca3af;
  --color-text-muted: #6b7280;
  --color-bg: #111827;
  --color-bg-secondary: #1f2937;
  --color-bg-tertiary: #374151;
  --color-border: #374151;
  --color-border-light: #4b5563;
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.3);
  --shadow-md: 0 4px 6px rgba(0,0,0,0.4);
  --shadow-lg: 0 10px 15px rgba(0,0,0,0.5);
}
```

---

## 三、Device Toolbar HTML + JS

Device Toolbar 用于在原型中切换桌面端（1440px）/ 平板（820px）/ 手机（393px）预览。

```html
<!-- ========== Device Toolbar ========== -->
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
    #device-toolbar .dt-label {
      color: var(--color-text-secondary, #6b7280);
      margin-right: var(--space-sm, 8px);
    }
    #device-toolbar button {
      padding: 4px 12px; border: 1px solid var(--color-border, #e5e7eb);
      background: var(--color-bg, #fff); color: var(--color-text, #1f2937);
      border-radius: var(--radius-sm, 4px); cursor: pointer;
    }
    #device-toolbar button.active {
      background: var(--color-primary, #2563eb);
      color: #fff; border-color: var(--color-primary, #2563eb);
    }
    #device-toolbar .dt-size {
      margin-left: auto;
      color: var(--color-text-muted, #9ca3af);
      font-family: var(--font-mono, monospace);
    }
    /* 原型内容区适配 */
    #prototype-content {
      margin-top: 42px; transition: max-width 0.3s, margin 0.3s;
      margin-left: auto; margin-right: auto;
    }
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

---

## 四、PRD Panel HTML + JS

PRD Panel 展示 PMContext 中的事实/规则/验收/假设/待确认项，内嵌在原型右侧（桌面端）或底部抽屉（移动端）。

```html
<!-- ========== PRD Panel ========== -->
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
    #prd-panel-drawer .prd-header button {
      background: none; border: none; font-size: 18px; cursor: pointer; color: var(--color-text-muted, #9ca3af);
    }
    #prd-panel-drawer .prd-section {
      padding: var(--space-sm, 8px) var(--space-md, 16px);
      border-bottom: 1px solid var(--color-border-light, #f3f4f6);
    }
    #prd-panel-drawer .prd-section h4 {
      margin: var(--space-sm, 8px) 0; color: var(--color-text, #1f2937);
      font-size: var(--font-size-base, 1rem);
    }
    #prd-panel-drawer .prd-item {
      padding: 4px 0; color: var(--color-text-secondary, #6b7280);
      display: flex; gap: 6px;
    }
    #prd-panel-drawer .prd-item .tag {
      display: inline-block; padding: 1px 6px; border-radius: var(--radius-sm, 4px);
      font-size: 0.75rem; font-weight: 500; flex-shrink: 0;
    }
    .tag-fact  { background: #dbeafe; color: #1d4ed8; }
    .tag-rule  { background: #fef3c7; color: #b45309; }
    .tag-accept{ background: #d1fae5; color: #047857; }
    .tag-assump{ background: #e0e7ff; color: #4338ca; }
    .tag-tbc   { background: #fce7f3; color: #be185d; }
    .prd-empty {
      padding: var(--space-xl, 32px) var(--space-md, 16px);
      text-align: center; color: var(--color-text-muted, #9ca3af);
    }
    /* 移动端适配：底部抽屉取代侧边栏 */
    @media (max-width: 640px) {
      #prd-panel-drawer { width: 100%; top: auto; bottom: 0; height: 60vh; border-left: none; border-top: 1px solid var(--color-border, #e5e7eb); }
    }
  </style>
  <button id="prd-panel-toggle">📋</button>
  <div id="prd-panel-drawer">
    <div class="prd-header">
      <span>📋 PRD 批注</span>
      <button id="prd-panel-close">✕</button>
    </div>
    <div id="prd-panel-body">
      <!-- PRD_DATA 由 AI 在生成 HTML 时序列化内嵌 -->
    </div>
  </div>
</div>

<script>
  (function() {
    const toggle = document.getElementById('prd-panel-toggle');
    const drawer = document.getElementById('prd-panel-drawer');
    const close  = document.getElementById('prd-panel-close');
    const body   = document.getElementById('prd-panel-body');
    if (!toggle || !drawer || !close || !body) return;

    toggle.addEventListener('click', () => drawer.classList.toggle('open'));
    close.addEventListener('click', () => drawer.classList.remove('open'));

    // PRD_DATA 由生成时注入（见 SKILL.md Step 0.5）
    const PRD_DATA = window.PRD_DATA || null;

    function renderPRD(data) {
      if (!data || (!data.pages && !data.facts && !data.rules && !data.acceptances)) {
        body.innerHTML = '<div class="prd-empty">⏳ 等待 pm-need 运行后填充<br><small>运行 /pm-need 生成 PMContext 后重试</small></div>';
        return;
      }
      let html = '';
      // 按页面分组展示
      if (data.pages && data.pages.length > 0) {
        data.pages.forEach(page => {
          html += '<div class="prd-section">';
          html += '<h4>📄 ' + (page.name || page.title) + '</h4>';
          if (page.items) {
            page.items.forEach(item => {
              html += '<div class="prd-item"><span class="tag tag-' + item.type + '">' + item.label + '</span><span>' + item.text + '</span></div>';
            });
          }
          html += '</div>';
        });
      } else {
        // 平铺模式（旧格式兜底）
        ['facts','rules','acceptances','assumptions','tbc'].forEach(key => {
          const items = data[key];
          if (!items || items.length === 0) return;
          const labels = { facts: '事实', rules: '规则', acceptances: '验收', assumptions: '假设', tbc: '待确认' };
          const tags  = { facts: 'fact', rules: 'rule', acceptances: 'accept', assumptions: 'assump', tbc: 'tbc' };
          html += '<div class="prd-section"><h4>' + labels[key] + '</h4>';
          items.forEach(text => {
            html += '<div class="prd-item"><span class="tag tag-' + tags[key] + '">' + labels[key] + '</span><span>' + text + '</span></div>';
          });
          html += '</div>';
        });
      }
      body.innerHTML = html || '<div class="prd-empty">暂无批注数据</div>';
    }

    renderPRD(PRD_DATA);
  })();
</script>
```

---

## 五、Toast / Modal 组件

### Toast 通知

```html
<style>
  #toast-container {
    position: fixed; top: 56px; right: 16px; z-index: 10000;
    display: flex; flex-direction: column; gap: 8px;
  }
  .toast {
    padding: 12px 16px; border-radius: var(--radius-md, 8px);
    font-family: var(--font-sans, -apple-system, sans-serif);
    font-size: var(--font-size-sm, 0.875rem); color: #fff;
    box-shadow: var(--shadow-md, 0 4px 6px rgba(0,0,0,0.07));
    animation: toast-in 0.3s ease;
    max-width: 360px;
  }
  .toast.success { background: var(--color-success, #10b981); }
  .toast.error   { background: var(--color-danger, #ef4444); }
  .toast.warning { background: var(--color-warning, #f59e0b); }
  .toast.info    { background: var(--color-info, #3b82f6); }
  @keyframes toast-in { from { opacity: 0; transform: translateX(20px); } to { opacity: 1; transform: translateX(0); } }
  @keyframes toast-out { from { opacity: 1; } to { opacity: 0; transform: translateX(20px); } }
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
    setTimeout(() => {
      el.style.animation = 'toast-out 0.3s ease';
      setTimeout(() => el.remove(), 300);
    }, duration);
  }
</script>
```

### Modal 弹窗

```html
<style>
  .modal-overlay {
    position: fixed; inset: 0; z-index: 10001;
    background: rgba(0,0,0,0.4); display: flex;
    align-items: center; justify-content: center;
    animation: fade-in 0.2s;
  }
  .modal-box {
    background: var(--color-bg, #fff); border-radius: var(--radius-lg, 12px);
    box-shadow: var(--shadow-lg, 0 10px 15px rgba(0,0,0,0.1));
    max-width: 560px; width: 90%; max-height: 80vh; overflow-y: auto;
    font-family: var(--font-sans, -apple-system, sans-serif);
    animation: modal-in 0.2s;
  }
  .modal-header {
    padding: var(--space-md, 16px) var(--space-lg, 24px);
    border-bottom: 1px solid var(--color-border, #e5e7eb);
    font-weight: 600; font-size: var(--font-size-lg, 1.125rem);
    display: flex; justify-content: space-between; align-items: center;
  }
  .modal-body  { padding: var(--space-lg, 24px); }
  .modal-footer {
    padding: var(--space-md, 16px) var(--space-lg, 24px);
    border-top: 1px solid var(--color-border, #e5e7eb);
    display: flex; gap: 8px; justify-content: flex-end;
  }
  @keyframes fade-in { from { opacity: 0; } to { opacity: 1; } }
  @keyframes modal-in { from { opacity: 0; transform: translateY(-20px); } to { opacity: 1; transform: translateY(0); } }
</style>
<script>
  function showModal(title, bodyHTML, footerHTML) {
    const overlay = document.createElement('div');
    overlay.className = 'modal-overlay';
    overlay.innerHTML = '<div class="modal-box">' +
      '<div class="modal-header"><span>' + title + '</span><button onclick="this.closest(\'.modal-overlay\').remove()" style="background:none;border:none;font-size:20px;cursor:pointer;color:var(--color-text-muted)">✕</button></div>' +
      '<div class="modal-body">' + bodyHTML + '</div>' +
      (footerHTML ? '<div class="modal-footer">' + footerHTML + '</div>' : '') +
      '</div>';
    overlay.addEventListener('click', function(e) { if (e.target === this) this.remove(); });
    document.body.appendChild(overlay);
    return overlay;
  }
</script>
```

---

## 六、单 HTML 完整模板（简单模式）

简单模式使用单 HTML 文件，集成了 Design Token、Device Toolbar、PRD Panel、互动交互。

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>原型: <需求名></title>
  <style>
    /* ===== Design Token ===== */
    :root {
      --color-primary: #2563eb; --color-primary-light: #60a5fa; --color-primary-dark: #1d4ed8;
      --color-accent: #f59e0b; --color-success: #10b981; --color-warning: #f59e0b;
      --color-danger: #ef4444; --color-info: #3b82f6;
      --color-text: #1f2937; --color-text-secondary: #6b7280; --color-text-muted: #9ca3af;
      --color-bg: #ffffff; --color-bg-secondary: #f9fafb; --color-bg-tertiary: #f3f4f6;
      --color-border: #e5e7eb; --color-border-light: #f3f4f6;
      --space-xs: 4px; --space-sm: 8px; --space-md: 16px; --space-lg: 24px; --space-xl: 32px; --space-2xl: 48px;
      --radius-sm: 4px; --radius-md: 8px; --radius-lg: 12px; --radius-full: 9999px;
      --shadow-sm: 0 1px 2px rgba(0,0,0,0.05); --shadow-md: 0 4px 6px rgba(0,0,0,0.07); --shadow-lg: 0 10px 15px rgba(0,0,0,0.1);
      --font-sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
      --font-mono: 'SF Mono', 'Fira Code', 'Fira Mono', monospace;
    }
    @media (prefers-color-scheme: dark) {
      :root { --color-text: #f3f4f6; --color-text-secondary: #9ca3af; --color-text-muted: #6b7280; --color-bg: #111827; --color-bg-secondary: #1f2937; --color-bg-tertiary: #374151; --color-border: #374151; --color-border-light: #4b5563; }
    }
    /* ===== 基础布局 ===== */
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: var(--font-sans); color: var(--color-text); background: var(--color-bg); font-size: 14px; line-height: 1.6; }
    /* ... 其余样式与单 HTML 模式 content section 样式一致 ... */
  </style>
</head>
<body>
  <!-- Device Toolbar -->
  <!-- PRD Panel -->
  <!-- Toast Container -->
  <!-- 原型内容: <section> 页面列表 -->
  <div id="prototype-content">
    <!-- 从 PMContext 提取并生成的页面内容 -->
  </div>
  <script>
    // PRD_DATA 序列化数据
    window.PRD_DATA = { /* AI 从 PMContext 读取后序列化 */ };
    // Device Toolbar JS
    // PRD Panel JS
    // Toast / Modal JS
  </script>
</body>
</html>
```

---

## 七、Bundle 模式各文件模板

复杂模式输出 `docs/pm-context/sketch/prototype/` 文件夹。

### index.html（入口壳）

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>原型: <需求名></title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <div id="app">
    <!-- Vue3 CDN 或 React CDN 或 Plain HTML 挂载点 -->
    <nav id="nav-bar"></nav>
    <main id="page-content"></main>
  </div>
  <!-- 数据文件 -->
  <script src="prd-data.js"></script>
  <script src="mock-data.js"></script>
  <!-- 主逻辑 -->
  <script src="app.js"></script>
</body>
</html>
```

### styles.css（Design Token + 响应式）

```css
/* ========================================
   Design Token — Bundle 模式
   ======================================== */
:root {
  --color-primary: #2563eb; /* ... 完整 Design Token，同本章第二节 ... */
  --font-sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}
/* ========================================
   基础样式 + 页面组件
   ======================================== */
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: var(--font-sans); color: var(--color-text); background: var(--color-bg); }
/* 页面布局：导航栏 + 内容区 */
#nav-bar { /* ... */ }
#page-content { /* ... */ }
/* 响应式断点 */
@media (max-width: 640px) { /* Mobile */ }
@media (min-width: 641px) and (max-width: 1024px) { /* Tablet */ }
@media (min-width: 1025px) { /* Desktop */ }
```

### app.js（完整交互逻辑）

```javascript
// ========================================
// 原型主逻辑 — 根据技术栈选择实现方式
// ========================================

// 从 PMContext 提取的页面配置
// 由 AI 在生成时填充
const PAGES = [];  // [{ id, name, title, sections: [{type, content}] }]

// 导航渲染
function renderNav() { /* ... */ }

// 页面渲染
function renderPage(pageId) { /* ... */ }

// 交互事件绑定
function bindEvents() {
  document.querySelectorAll('[data-action]').forEach(el => {
    el.addEventListener('click', handleAction);
  });
}

// 工具函数
function handleAction(e) { /* ... */ }
function showToast(msg, type) { /* ... */ }
function openModal(title, content) { /* ... */ }

// 初始化
document.addEventListener('DOMContentLoaded', () => {
  renderNav();
  renderPage(PAGES[0]?.id);
  bindEvents();
});
```

### prd-data.js（PMContext 内容注入）

```javascript
// ========================================
// PRD Data — 由 pm-sketch 在生成 HTML 时从 PMContext 读取并序列化
// 来源：docs/pm-context/pm-context.md + docs/pm-context/prd/ai-prd.md + docs/pm-context/prd/human-prd.md
// ========================================
window.PRD_DATA = {
  "projectName": "<需求名>",
  "pages": [
    {
      "name": "页面名",
      "title": "页面标题",
      "items": [
        { "type": "fact", "label": "事实", "text": "字段/数据说明" },
        { "type": "rule", "label": "规则", "text": "业务逻辑规则" },
        { "type": "accept", "label": "验收", "text": "验收标准" },
        { "type": "assump", "label": "假设", "text": "假设项" },
        { "type": "tbc", "label": "待确认", "text": "待确认项" }
      ]
    }
  ],
  // 平铺格式兜底
  "facts": [],
  "rules": [],
  "acceptances": [],
  "assumptions": [],
  "tbc": []
};
// 若 PMContext 文件不存在，保留空结构，PRD Panel 展示空状态占位
```

### mock-data.js（图表/列表 mock 数据）

```javascript
// ========================================
// Mock Data — 供原型中的图表、表格、列表展示
// 根据 PMContext 数据模型自动生成
// ========================================
window.MOCK_DATA = {
  "tables": {
    "userList": [
      { "id": 1, "name": "张三", "role": "采购员", "department": "采购部" },
      { "id": 2, "name": "李四", "role": "需求人", "department": "研发部" }
    ],
    "orderList": [
      { "id": "PO-2026-001", "supplier": "ABC 科技", "amount": 28000, "status": "待确认" }
    ]
  },
  "charts": {
    "budgetTrend": {
      "labels": ["1月","2月","3月","4月","5月","6月"],
      "datasets": [
        { "label": "预算", "data": [100, 100, 100, 100, 100, 100] },
        { "label": "已用", "data": [45, 62, 58, 78, 85, 92] }
      ]
    },
    "supplierScore": {
      "labels": ["质量","交期","服务","价格"],
      "datasets": [{ "label": "ABC 科技", "data": [85, 78, 90, 70] }]
    }
  }
};
```

### README.md（本地启动说明）

```markdown
# 原型预览说明

> 由 `/pm-sketch --prototype --bundle` 生成的 HTML 可交互原型（复杂模式）。

## 本地启动

### 方式 1：npx serve（推荐，无需安装）

```bash
npx serve .
```

### 方式 2：Python

```bash
# Python 3
python -m http.server 8080

# Python 2
python -m SimpleHTTPServer 8080
```

### 方式 3：Node.js

```bash
npx live-server --port=8080
```

## 文件说明

| 文件 | 作用 |
|------|------|
| `index.html` | 入口壳，双击可直接打开基础版 |
| `app.js` | 完整交互逻辑 |
| `styles.css` | Design Token + 响应式样式 |
| `prd-data.js` | PMContext 内容注入（事实/规则/验收/假设） |
| `mock-data.js` | 图表/列表 mock 数据 |

## 注意事项

- 直接双击 `index.html` 可查看基础布局（L1），部分异步数据需启动 HTTP 服务后可用
- 原型基于 PMContext 生成，所有图元对应 PMContext 中的实体/关系
- `[假设]` 标注的图元以灰色占位展示，表示尚未确认
```

---

## 八、适配标注片段

### Electron 标注

当检测到或推荐 Electron 时，在原型顶部添加：

```html
<!-- 🖥 此原型推荐用 Electron 包装运行。Electron 主进程配置见 electron/main.js -->
```

### 移动端适配

当检测到或推荐 Flutter / React Native 时，HTML 原型不适用，输出 `design-spec.md` 替代，包含屏幕设计说明 + 组件规范 + 交互描述。

---

## 九、质量清单

生成后逐项检查（完整版，在 SKILL.md 内联版基础上延伸）：

### 基础检查（所有模式）

- [ ] ✅ 技术栈决策有依据（新项目推荐 / 老项目扫描检测 `package.json` 等）
- [ ] ✅ 使用推荐/检测到的技术栈 CDN 版本（Vue3 / React / Plain HTML 兜底）
- [ ] ✅ 响应式设计（移动端 ≤ 640px / 桌面端 ≥ 1024px 两套布局）
- [ ] ✅ 所有页面/组件都对应 PMContext 中的实体/关系
- [ ] ✅ 无法对应 PMContext 的图元标 `[假设]` 注释
- [ ] ✅ 交互可操作（点击/切换/表单输入等 demo 级别即可）
- [ ] ✅ UTF-8 编码，中文字符正常显示
- [ ] ✅ Electron 或移动端适配标注已添加

### 增强检查（v3 新增）

- [ ] ✅ Design Token 内嵌（CSS 变量，无硬编码 `#hex` 色值）
- [ ] ✅ Device Toolbar 可切换三端（1440 / 820 / 393 px）
- [ ] ✅ PRD Panel 展示 PMContext 批注（事实/规则/验收/假设/待确认）
- [ ] ✅ 每个 `<section>` 页面至少有 1 个 JS 交互事件（L3 底线）
- [ ] ✅ 暗色主题适配（`@media (prefers-color-scheme: dark)` 或 `--dark` 参数）

### 体积检查

- [ ] ✅ 简单模式单 HTML < 280KB（不含 CDN 外部资源），超出则提示精简或退化为 Mermaid 草图
- [ ] ✅ 复杂模式 index.html < 30KB（入口壳仅含 HTML 骨架 + 外部资源引用）

### 补充检查（复杂模式额外）

- [ ] ✅ bundle 文件夹中 prd-data.js 包含 PMContext 所有批注数据
- [ ] ✅ bundle 文件夹中 mock-data.js 包含图表/列表 mock 数据
- [ ] ✅ bundle 文件夹中 README.md 含本地启动命令
- [ ] ✅ prototype/index.html 双击可打开基础版（无 JS 报错）
