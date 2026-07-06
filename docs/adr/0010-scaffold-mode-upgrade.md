# ADR 0010: /pm-sketch Scaffold 模式升级——从多文件 HTML 到前端工程脚手架

## Status

Accepted (2026-07-03). Grilling 会话 7 轮完成，所有待定项已锁定。

## Context

/pm-sketch 的复杂模式原先定义为"bundle 文件夹"：`index.html` + `app.js` + `styles.css` + `prd-data.js` + `mock-data.js` + `README.md`，本质上仍是多文件 HTML/CSS/JS，受 `index.html < 30KB` 体积门约束，采用 CDN script tag 引框架。

参考 Axhub-Make (`/Users/ldh/Downloads/project/Axhub-Make-main`) 的 `beginner-guide` 原型实物后，发现其产物水准远超 pm-sketch 现有复杂模式：
- **真实 React + TS + Vite 工程**，不是 CDN script tag 拼凑
- **用 Tailwind v4**，不是手写 CSS
- **`useHashPage` hook + `defineHashPageRoute`** 实现多页路由，不是 hash 锚点裸切换
- **真实 snapshot 图片 assets** 静态 import，不是 URL 占位
- **章节级组件拆分**（`InstallAgentChapter`/`ChooseModelChapter`/`GiveInstructionsChapter`……），不是 `<section>` 平铺
- **验收脚本** `check-app-ready.mjs` 把关，不是 AI 自检打 ✅

用户明确要求"在让在生成原型系统的时候，有完善的交互，规范的样式，以及能够适配分辨率和移动端，甚至提供相关文档的预览查看"。现有的 bundle 模式产物质量不足以达到这个期望。

### 核心矛盾

1. **CDN vs 工程**：复杂模式若仍走 CDN script tag，不可能产出 `beginner-guide` 级别的交互和结构——没有 router、没有 TS 类型检查、没有 `npm run build` 验证
2. **体积门 vs 丰富度**：30KB index.html 体积门与 L4（角色/权限/多态/错误恢复）交互底线直接冲突
3. **AI 自检 vs 验收闭环**：现有质量清单是 AI 读代码打 ✅，Axhub-Make 是跑 `check-app-ready.mjs`，不跑 dev server 无法验证项目能否启动

### 已权衡的等价模式组合

本 ADR 的七个决策维度各有等价方案，详见 CONTEXT.md「/pm-sketch 升级决策（2026-07-03）」节。

## Decision

### 1. 产物模式重定义

| 旧术语 | 新术语 | 定义 |
|--------|--------|------|
| 简单模式（保留） | 简单模式 (Simple / CDN 模式) | 单 HTML，CDN 引框架，L3 交互，< 280KB |
| 复杂模式（旧）→ **Scaffold 模式** | Scaffold 模式 | 可运行前端工程脚手架。固定 React + TS + Vite + Tailwind v4。L4 交互。无体积上限。纯前端 mock，不输出后端/schema/真实 API |

### 2. 交互底线

- 简单模式 → **L3**：hash 多页路由（`#page=xxx`），表单提交后跳下一页并带状态，状态机图里画的状态在原型中点选切换
- Scaffold 模式 → **L4**：L3 全部 + 角色切换 + 权限分支 + 错误恢复路径 + 加载/空/成功/失败四态全覆盖

### 3. 视觉规范（S2）

- PMContext = 业务事实源，`docs/design/DESIGN.md` = 视觉事实源（可选）
- DESIGN.md 存在时严格派生 CSS token；不存在时回退 pm-sketch 自带 Design Token；冲突标 `[冲突]`
- `prototype-templates.md` 新增「DESIGN.md 派生 token 协议」

### 4. 响应式

- 5 档断点：1440/1280/1024/768/480 px
- R3（手势/swipe/pull-to-refresh）仅 Scaffold 模式 + PMContext 含移动端角色时启用

### 5. 文档预览

- D1：PRD Panel 强化——批注可展开 PMContext 原文段落
- D2：新增文档预览 overlay（spec-template 风格 `<pre>` 渲染），文件树含业务 + 视觉两区
- 放弃 D3：不接 `@axhub/annotation` 私有包

### 6. 验收级别判定（Acceptance Tier）

正交于复杂度判断的新维度：

| 触发条件 | 验收级别 |
|---------|---------|
| 初次生成 / 改动 > 3 页 / 文件 > 5 / 元素 > 10 | V3（npm install + tsc + vite build + dev server + headless + console） |
| 其余 | V2（npm install + tsc + vite build） |
| 简单模式（CDN HTML） | V1（AI 自检 + 体积） |

**降级链**：V3 → V2 → V1 → 输出"未验收工程 + 已知错误清单"，不静默撒谎。

### 7. 技术栈

- 简单模式 → 保留 Step 0 灵活选型（Vue3 / React / Plain HTML CDN）
- Scaffold 模式 → **固定 React + TS + Vite + Tailwind v4**，不再检测/推荐

## Alternatives Considered

### A. Scaffold 模式固定 Vue3

否决。理由：
1. Axhub-Make 所有可借鉴实物（`beginner-guide` 1055 行 React + `useHashPage` hook + 截图 import + 节级路由）全是 React，选 Vue3 等于放弃全部可抄资产
2. Vue3 版 Scaffold 模板无实物验证，质量不可控
3. Tailwind v4 与 React 集成生态（`beginner-guide/style.css` 第一行 `@import "tailwindcss"`）有现成参考，Vue3 版需从零摸索

### B. Scaffold 模式双模板（React + Vue3 两套）

否决。理由：
1. 模板维护翻倍，每次升级改两遍
2. AI 生成时需先选模板再生成，认知负担翻倍，出错率上升
3. Axhub-Make 自己也只维护 React 一套，不是双模板

### C. 保留 CDN 做 Scaffold 模式（只是去掉体积门）

否决。理由：
1. L4 交互需要 router + state store + 多态渲染，CDN script tag 拼凑的 JS 无法维护
2. 无 `tsc --noEmit` 验证，类型错误不会被捕获
3. 得不到 Axhub `beginner-guide` 工程级实物质量

### D. V3 作为唯一验收级别

否决。理由：
1. 环境依赖太重——agent 沙箱不一定有 Chrome，不一定能开端口
2. 简单模式（CDN HTML）跑 V3 是本末倒置（体积比验收成本低得多）
3. 分级验收已被 Axhub `check-app-ready.mjs` 实践验证——初次生成跑全量，增量改动跑差分

### E. 强制 DESIGN.md 作为原型视觉前提（S3）

否决。理由：
1. 违反 PMSkill 宪法（ADR 0004：PMContext 是唯一事实源）。引入强制第二事实源需全局修订 ADR 0004，代价与收益不匹配
2. 破坏 `pm-sketch --auto` 全链路零确认体验——auto 模式下用户期望一气呵成，突然 STOP 要 DESIGN.md 会打断流程
3. S2（可选）平衡得更好：有 DESIGN.md 就用，没有也能正常工作

## Consequences

**正向**：
- Scaffold 模式产物对齐 Axhub-Make `beginner-guide` 水准：React + TS + Vite + Tailwind v4 + 真实路由 + L4 交互
- 分级验收覆盖三种场景：轻量改动不跑 dev server（快）、初次生成跑全量（稳）、失败降级暴露错误（诚实）
- DESIGN.md 可选引入不破坏 PMSkill 现有宪法和 `--auto` 链路
- 5 档断点覆盖从 480px 手机到 1440px 桌面的真响应式，不靠 Device Toolbar 缩放作弊

**负向**：
- Scaffold 模式生成时间显著增加：npm install + vite build + 可能 dev server + headless，比现有 bundle 模式慢 3-5×
- CONTEXT.md 新增约 60 行术语/决策，尚未同步更新 `prototype-templates.md`、`SKILL.md` Step 0 和 Step -1、质量清单、失败模式表、反例黑名单
- 现有 `prototype-templates.md` 全篇需按新术语体系重写（第七节 Bundle 模式→Scaffold 模式，新增 DESIGN.md 派生 token 协议，新增 5 档断点 CSS，新增文档预览 overlay，新增 L4 交互模板）
- 改变量门迁移：SKILL.md 的 `index.html < 30KB` 约束仅保留给简单模式；质量清单的增强检查（Design Token / Device Toolbar / PRD Panel / 交互 / 暗色）需区分模式
- `skills-lock.json` 未记录此决策（不属于 npx skills@latest 管理的范围，不需更新）
