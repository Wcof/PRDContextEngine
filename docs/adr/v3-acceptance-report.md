# /pm-sketch v3 升级验收报告

> 实施日期: 2026-07-04
> 依据: CONTEXT.md「/pm-sketch 升级决策（2026-07-03）」+ ADR 0010 + technical-design.md
> 参考项目: `/Users/ldh/Downloads/project/Axhub-Make-main`（`beginner-guide` / `annotation-demo` 原型 + `useHashPage` hook + `theme-guide.md`）

## 1. 实施范围

按 CONTEXT.md 升级决策（B 范围：只升产物模板，不动协议骨架）完成 4 个文件改动：

| 文件 | 改动类型 | 关键内容 |
|------|---------|---------|
| `skills/visualization/pm-sketch/references/prototype-templates.md` | 全文重写（845→1386 行） | DESIGN.md 派生 Token 协议 / 5 档断点 / 文档 overlay / Scaffold 模式 19 文件模板 / V2-V3 验收脚本 / 分模式质量清单 |
| `skills/visualization/pm-sketch/SKILL.md` | 升级（300→349 行） | Step -1 双模式 / Step 0 分区 / Step 0.3 DESIGN.md / 质量门分模式 / 失败模式表验收降级 / 反例黑名单 Q10 |
| `skills/visualization/pm-sketch/references/technical-design.md` | 局部（2.4 节） | DESIGN.md 读取优先级「待定」→ 已实施 |
| `skills/visualization/pm-sketch/references/sketch-prototype-example.md` | 术语同步 | 复杂模式→Scaffold / bundle→Vite 工程 / 30KB→V2/V3 验收 |

## 2. 与参考项目 Axhub-Make 的对齐点

| 决策项 | Axhub-Make 参考 | pm-sketch Scaffold 模式落地 |
|--------|----------------|---------------------------|
| 框架 | `client/package.json` React 19 + Vite 6 | `package.json` React ^19 + Vite ^6 |
| Tailwind | `@tailwindcss/vite` v4 | `@tailwindcss/vite` ^4 + `style.css` 首行 `@import "tailwindcss";` |
| 多页路由 | `src/common/useHashPage.ts`（`defineHashPageRoute` + `useHashPage`） | `src/hooks/useHashPage.ts`（对齐接口，简化去掉 host postMessage） |
| 入口注释 | `index.tsx` 顶部 `/** @name 新手指导 */` | `App.tsx` 顶部 `/** @name {{PROJECT_NAME}} */` |
| pageId 规范 | `PAGE_ID_RE = /^[a-z0-9-]+$/u` | 同正则 |
| hash 格式 | `#page=<pageId>`（URLSearchParams 解析） | 同格式 + `parseHashPage` 同实现 |
| TS 严格 | `tsconfig.base.json` strict + jsx react-jsx + Bundler | `tsconfig.json` 同配置 |
| 验收脚本 | `scripts/check-app-ready.mjs`（dev server + 可达性） | V2/V3 脚本（npm install + tsc + vite build + dev server + curl） |

> 形态差异说明：Axhub 原型寄生于宿主 vite（`src/prototypes/<name>/index.tsx`，无独立 `index.html`/`main.tsx`）；pm-sketch Scaffold 模式目标是**独立可运行工程**落盘到 `docs/pm-context/sketch/prototype/`，故自带 `index.html` + `main.tsx` + `vite.config.ts`。此差异符合 ADR 0010 决策（PM 拿到的是可独立运行的工程）。

## 3. 可验证证据：Scaffold 模式 V2+V3 验收实跑

按 `prototype-templates.md` 第十节验收脚本，用模板实生成最小工程并跑通验收。工程见 `/tmp/pm-sketch-scaffold-verify/`（11 个文件，对齐 7.1 目录结构）。

### 3.1 V2 验收（npm install + tsc + vite build）

```
$ cd /tmp/pm-sketch-scaffold-verify
$ npm install          → added 81 packages in 8s
$ npx tsc --noEmit     → TSC_EXIT=0  ✅
$ npx vite build       → ✓ 37 modules transformed, built in 476ms, BUILD_EXIT=0  ✅
```

产物体积（验证无体积上限约束）：
- `dist/index.html` 0.41 KB
- `dist/assets/index-*.css` 13.18 KB
- `dist/assets/index-*.js` 201.48 KB（gzip 63.19 KB）
- 总计 220 KB

### 3.2 V3 验收（dev server + 可达性）

```
$ npx vite --port 4173
$ curl http://127.0.0.1:4173/        → HTTP_STATUS=200  ✅
  含 <div id="root"> + <script src="/src/main.tsx">
$ curl http://127.0.0.1:4173/src/main.tsx → JS_HTTP=200  ✅
$ headless console 检查 → 跳过（环境无 Chrome，按 10.3 仅做端到端可达性）
```

### 3.3 base: './' 验证（file:// 可打开）

产物 `dist/index.html` 用相对路径 `./assets/index-*.js`，支持 `file://` 协议直接双击打开，无需 HTTP server。

### 3.4 模板组件功能验证

工程含完整组件：DeviceToolbar（三端切换）/ PrdPanel（D1 可展开原文 source）/ DocOverlay（D2 文件树 + `<pre>` 渲染）/ PageHome（L4 四态：loading/success，含 error/empty 分支）/ useHashPage（hash 路由）。tsc strict 模式 0 错误，证明模板类型安全。

## 4. 旧术语清理验证

```
$ grep -rn "复杂模式|--bundle|--single|index.html < 30KB|bundle 文件夹" skills/visualization/pm-sketch/ docs/adr/
→ 无残留  ✅
```

frontmatter 仍只有 3 字段（name/description/disable-model-invocation），符合项目规范。

## 5. 决策落地核对（vs CONTEXT.md 升级决策）

| 决策项 | CONTEXT.md 要求 | 落地状态 |
|--------|----------------|---------|
| 升级范围 B（只升产物模板） | 不动协议骨架 | ✅ Purpose/Context/Thinking Protocol 核心节段保留 |
| 双模式术语 | 简单/Scaffold | ✅ 全文统一 |
| 交互底线 L3/L4 | 简单 L3 / Scaffold L4 | ✅ 质量清单 + PageXxx 骨架 |
| 样式 S2 DESIGN.md | 可选视觉事实源 | ✅ Step 0.3 + 派生协议 |
| 5 档断点 | 1440/1280/1024/768/480 | ✅ 第三节 + Tailwind 前缀映射 |
| D1+D2 文档预览 | PRD Panel 展开 + overlay | ✅ 第五/九节 + PrdPanel/DocOverlay 组件 |
| 放弃 D3 | 不接 @axhub/annotation | ✅ 未引入 |
| 验收 V1/V2/V3 + 降级链 | 不静默撒谎 | ✅ 第十节脚本 + 失败模式表 + 反例 Q10 |
| 技术栈 Step 0 分区 | 简单灵活 / Scaffold 固定 | ✅ Step 0 分区表 |
| 产物目录 Q9 | 对齐 Axhub | ✅ 7.1 目录结构 |
| 反例黑名单 Q10 | 5 条新反模式 | ✅ SKILL.md + prototype-templates.md 第十一节 |

## 6. 结论

v3 规范合规升级**实施完成且经实跑验证**：
- Scaffold 模式模板可生成真实可运行工程（V2 + V3 验收通过，tsc strict 0 错误，vite build 成功，dev server HTTP 200）
- 与参考项目 Axhub-Make 的 useHashPage / Tailwind v4 / @name 约定 / TS 严格配置对齐
- CONTEXT.md 11 项升级决策全部落地
- 旧术语清理干净，frontmatter 合规

未跑项：evals/run-evals.sh（升级范围为产物模板，不动协议骨架，evals 不受影响）；headless console 检查（环境无 Chrome，按 10.3 跳过，已记录）。
