# PMSkill Context

产品经理在 Agent 里工作的 Skill 工具箱。从模糊想法/用户诉求出发，沉淀成清晰的 PMContext，
再转成可交付的 PRD（给 AI 或给人）和草图（多种可视化形态）。

## Language

**PM（产品经理）**:
在 Agent（Claude/Codex/Trae 等）里工作的产品经理，自己用 Agent 协作完成需求工作。
_Avoid_: 只写文档不协作的 PM、纯对接工程的 PM


## PMContext 模板

以下是不带实例内容的模板骨架。完整实例见各 SKILL.md 的产出示例。

```markdown
# PMContext: <需求名>
## 概述
### 问题与目标
### 现状平替与摩擦力
### 价值验证度量
## <页面/功能名>（如：用户登录）
### 事实
### 规则
### 验收
## <页面/功能名>（如：支付流程）
### 事实
### 规则
### 验收
## 全局约束
## 决策日志
## 假设清单与验证计划
## 风险项 [待确认] [假设] [冲突]
## 信息缺口
## Skill 调用关系

| Skill | 调用方式 | 可被编排 |
|---|---|---|
| `/pm-need` | user-invoked | —（人类入口，编排下游 pm-prd/pm-sketch/pm-premortem） |
| `/pm-setup` | user-invoked | —（首次配置，独立运行） |
| `/pm-prd` | model-invoked | 可被 pm-need --auto 编排 |
| `/pm-sketch` | model-invoked | 可被 pm-need --auto 编排 |
| `/pm-aiprd` `/pm-humanprd` | model-invoked | 被 pm-prd 编排 |
| `/pm-wireframe` `/pm-ia` `/pm-state` `/pm-flow` `/pm-journey` | model-invoked | 被 pm-sketch 编排 |
| 其余 pm-* | model-invoked | Agent 自主触发或人工显式调用 |

调用规则：user-invoked 不可调用另一 user-invoked skill；user-invoked 可编排 model-invoked 子 skill。所有 user-invoked 技能支持 `--auto` 零确认。

## Skill 目录结构

## /pm-sketch 升级决策（2026-07-03）

基于 grilling 会话 10 项决策 + domain-modeling 校验后的锁定项。来源：Axhub-Make (`/Users/ldh/Downloads/project/Axhub-Make-main`) 参考借鉴。

### 升级范围（B）

**只升产物模板，不动 /pm-sketch 协议骨架。** 所有改动限于 `prototype-templates.md` 和 `SKILL.md` 的质量门/失败模式表/Step 0 描述；不重写 SKILL.md 的 Purpose/Context/Instructions/Thinking Protocol 等核心节段。

### 产物模式

| 术语 | 定义 |
|------|------|
| **简单模式 (Simple / CDN 模式)** | 单 HTML，CDN 引框架，L3 交互，< 280KB。保留现有 Step 0 技术栈灵活选型 |
| **Scaffold 模式（原名复杂模式）** | 可运行前端工程脚手架（React + TS + Vite + Tailwind v4 + dev 脚本）。L4 交互。无体积上限。纯前端 mock，不输出后端/schema/真实 API |

### 交互底线

- **简单模式 → L3**：hash 多页路由（`#page=xxx`），表单提交后跳下一页并带状态，列表→详情→返回可走通，状态机图里画的状态在原型中点选切换
- **Scaffold 模式 → L4**：L3 全部 + 角色切换 + 权限分支 + 错误恢复路径 + 加载/空/成功/失败四态全覆盖

### 样式规范（S2）

- PMContext 是**业务事实源**，`docs/design/DESIGN.md` 是**视觉事实源**（可选）
- DESIGN.md 默认扫描路径：`docs/design/DESIGN.md`
- DESIGN.md 存在时严格按它派生 CSS token；不存在时回退 pm-sketch 自带 Design Token
- 双源冲突时标 `[冲突]` 不强行收敛
- `prototype-templates.md` 新增「DESIGN.md 派生 token 协议」

### 响应式策略（R1+R2+R3_scaffold）

- 5 档默认断点：1440 / 1280 / 1024 / 768 / 480 px，每档写明 key changes
- R3（移动端手势：swipe/pull-to-refresh/bottom tab）**仅 Scaffold 模式 + PMContext 含移动端角色时**启用
- Device Toolbar 保留（三端一键切换演示），但底层布局必须真断点，不靠缩放作弊

### 文档预览（D1+D2）

#### 数据嵌入策略（默认 E1 + 可选 E2）

| 模式 | 默认 | 备选 |
|------|------|------|
| 简单模式 | E1 静态嵌入（序列化到 JS 变量） | 无（无 server 环境） |
| Scaffold 模式 | E1 静态嵌入 | E2 运行时 fetch（仅 V3 验收环境，有 dev server 时追加 `.md` 源文件副本 + fetch 逻辑） |

**体积超限自动拆分**（仅简单模式）：E1 嵌入数据导致单 HTML 超 280KB 总上限时，自动拆分——入口只保留目录索引 + 摘要，正文懒加载独立 `.js` chunk。Scaffold 模式无体积上限，全部静态嵌入。

- **D1**：PRD Panel 强化——批注可展开对应 PMContext 原文段落（heading + 上下文）
- **D2**：新增文档预览 overlay（spec-template 风格 `<pre>` 渲染）。文件树含 `docs/pm-context/`（业务依据）+ `docs/design/DESIGN.md`（视觉依据），分区显示
- **放弃 D3**：不接 Axhub `@axhub/annotation` 私有包

### 验收级别判定（Acceptance Tier）

正交于复杂度判断的独立维度。

| 触发条件 | 验收级别 |
|---------|---------|
| 初次生成 / 改动 > 3 页 / 文件 > 5 / 元素 > 10 | V3 |
| 其余 | V2 |
| 简单模式（CDN HTML） | V1 |

降级链：V3 失败 → V2 → V1 → 输出"未验收工程 + 已知错误清单"，不静默撒谎。

| 级别 | 内容 |
|------|------|
| V3 | `npm install` + `tsc --noEmit` + `vite build` + dev server + headless 访问 + console 查错 |
| V2 | `npm install` + `tsc --noEmit` + `vite build` |
| V1 | AI 自检 + 体积检查，不强制命令 |

### 技术栈决策（Step 0 分区）

| 模式 | 框架决策 |
|------|---------|
| 简单模式（CDN HTML） | 保留现有 Step 0 逻辑——检测/推荐 Vue3 或 React，用 CDN script tag |
| Scaffold 模式（Vite 工程） | 固定 React + TS + Vite + Tailwind v4，不检测不推荐 |

### 产物目录（Q9 — 与 Axhub-Make 对齐）

Scaffold 模式产物目录结构：

```
docs/pm-context/sketch/prototype/
├── index.tsx              # 入口组件，export default Component
├── style.css              # @import "tailwindcss";
├── components/            # 原型内部共享组件
├── pages/                 # 多页面原型页面组件
├── assets/                # 原型专属素材（截图、图片等）
├── vite.config.ts
├── tsconfig.json
├── package.json
└── README.md              # 本地启动说明
```

- 多页面通过 URL hash 参数 `#page=<pageId>` 定位（对齐 Axhub `useHashPage` hook）
- `pageId` 命名使用小写字母、数字、连字符
- 入口 `index.tsx` 顶部包含中文 `@name` 注释，用于预览列表展示

### 反例黑名单（Q10 — 新增反模式）

在 /pm-sketch 的反例黑名单中新增：

| 反模式 | 为什么不要做 |
|--------|------------|
| Scaffold 模式生成后不运行验收即打 ✅ 标记完成 | 系统性撒谎——PM 拿到一个 npm install 都跑不起来的工程 |
| 简单模式超 280KB 不拆分不提示 | 体积门是质量底线，超限静默输出等于隐藏缺陷 |

```
