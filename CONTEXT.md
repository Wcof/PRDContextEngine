# PMSkill Context

产品经理在 Agent 里工作的 Skill 工具箱。从模糊想法/用户诉求出发，沉淀成清晰的 PMContext，
再转成可交付的 PRD（给 AI 或给人）和草图（多种可视化形态）。

## Language

**PM（产品经理）**:
在 Agent（Claude/Codex/Trae 等）里工作的产品经理，自己用 Agent 协作完成需求工作。
_Avoid_: 只写文档不协作的 PM、纯对接工程的 PM

**User-facing Skill**:
默认对斜杠菜单可见、人类会主动 `/触发` 的 skill。`metadata.internal` 不设或为 `false`。前置缺失时不静默撒谎——读取 PMContext 空就告知"空产物"。两条触发路径都成立：被编排自动跑 / 人类手动 `/触发` 增量更新。
_Avoid_: 对外 skill、可见 skill

**Engine Skill**:
不进斜杠发现列表、由编排 skill 在链路中 `use_skill` 调起、或人类显式 `INSTALL_INTERNAL_SKILLS=1` / `--skill <name>` 才能取到的 skill。`metadata.internal: true`。引擎直读 SKILL.md 不受影响——本标记只作用于发现器（`npx skills` 的 `parseSkillMd`）。
_Avoid_: 内部 skill、隐藏 skill

**Skill 可见性判据**:
若该 skill 的产物**人类会单独想要**（一份 PRD、一张草图、一个风险清单）且为人类入口 → User-facing。
若该 skill 是链路中转、其产物是给下游 skill 消费而非人类直接读，或由 AI 自主按语义触发调用 → Engine。
当前 User-facing 名单（5 个）：`pm-setup` / `pm-need` / `pm-prd` / `pm-sketch` / `pm-premortem`。其余皆为 Engine。

**PMContext Frozen 段**:
PMContext 中已确认段（无 `[待确认]` `[假设]` `[冲突]` 标记的段）一经落盘即 Frozen。增量更新仅可扫有标记的段重跑，已确认段不得改。
_Avoid_: 已确认段、定型段

**pm-need 入口判据**:
`/pm-need` 入口扫产物目录自判模式——PMContext 不存在或为空 = 0→1 全链路；存在且非空 = 增量模式。不问"是否覆盖"，0→1 vs 增量由文件现状硬判，不靠用户记 flag。
增量模式细分为**三条路径**：补全型（扫标记段重跑）、新增型（追加新 heading，已有段 Frozen）、调整型（`--update §N` 显式解冻已确认段）。
_Avoid_: --incremental flag（已删，入口自判）

**技术栈硬约束**:
PMContext §8 若含前端框架声明（Vue/React/Next/Nuxt/Svelte/Angular/Electron，或 Vite+TypeScript 同时出现），即从 PMContext 的"建议"升格为下游 skill 必须遵守的硬约束——下游据此触发 Scaffold 模式，防 Agent 自降级到简单模式。样式工具（Tailwind/UnoCSS/Less/Sass）单独出现不触发。
_Avoid_: 技术栈建议（弱语气已废除，凡声明即硬约束）

**汇总文档（Summary）**:
`/pm-summary` 是只读汇总层，按阅读主题把散件产出拼装成几份大文档——`SUMMARY-需求.md`（上下文+市场+用户+战略+指标+风险）、`SUMMARY-交付.md`（PRD+故事+发布+roadmap+OKR+sprint+干系人）、`SUMMARY-可视化.md`（线框+IA+状态机+流程+旅程+实体字典）、`SUMMARY-验证.md`（实验+A/B+队列+审计+回顾+合规）、`INDEX.md`（总索引，每份原产物一行：路径+标题+来源 skill+摘要+已汇总到哪份）。落到产物目录最外层，与 `pm-context.md` 同级。原产物零改动——不改写只嵌入、每段标来源锚点、缺失不臆造、幂等可重刷。不进 auto 链路，PM 主动触发；conflict-resolver 仍改原产物不改汇总。
_Avoid_: 汇总报告、总览文档（弱语气已废除，按阅读主题拼装是硬约定）


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

> Harness/Skill 边界见 [docs/adr/0009-harness-skill-boundary.md](docs/adr/0009-harness-skill-boundary.md)。冻结/差分持久化、CoT flush、双通道 Pinned-Sliding、会话 fork 隔离属 Harness 控制层职责，不由 SKILL.md 承载。

| Skill | 调用方式 | 可被编排 | 可见性 |
|---|---|---|---|
| `/pm-need` | user-invoked | —（人类入口，编排下游 pm-prd/pm-stories/pm-sketch/pm-premortem） | User-facing |
| `/pm-setup` | user-invoked | —（首次配置，独立运行） | User-facing |
| `/pm-prd` | model-invoked | 可被 pm-need --auto 编排 | User-facing |
| `/pm-premortem` | model-invoked | 可被 pm-need --auto 编排 | User-facing |
| `/pm-sketch` | model-invoked | 可被 pm-need --auto 编排 | User-facing |
| `/pm-stories` | model-invoked | 可被 pm-need --auto 编排（在 pm-prd 之后、pm-sketch 之前） | Engine |
| `/pm-aiprd` `/pm-humanprd` | model-invoked | 被 pm-prd 编排 | Engine |
| `/pm-wireframe` `/pm-ia` `/pm-state` `/pm-flow` `/pm-journey` | model-invoked | 被 pm-sketch 编排 | Engine |
| `/pm-conflict-resolver` | model-invoked | 被 pm-need 在节点失败时编排；亦被 pm-need 增量模式内联调做差分合并 | Engine |
| 其余 pm-* | model-invoked | Agent 自主触发或人工显式调用 | Engine |

调用规则：user-invoked 不可调用另一 user-invoked skill；user-invoked 可编排 model-invoked 子 skill。所有 user-invoked 技能支持 `--auto` 零确认。可见性判据见上文『Skill 可见性判据』。

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

### 过程文档产物布局（ADR 0016 — 显性化）

过程文档**显性落盘**到 `docs/pm-context/process/`（进版本库，PM 可直接查看审计），重跑时**归档而非删除**到 `process/.archive/<timestamp>/`。纯技术缓存（断点续跑 JSON 分片）落 `.cache/`，不进版本库，重跑时清空。

| 目录 | 用途 | 版本库 |
|------|------|--------|
| `process/` | 过程文档（问题重构/领域模型/决策表/风险清单/交付追溯） | ✅ 进 |
| `process/.archive/<ts>/` | 重跑归档区，保留历史供审计 | ❌ 不进 |
| `.cache/` | 纯技术缓存（nodeN-*.json 分片，断点续跑用） | ❌ 不进 |

**双层注入模型术语对齐**：流程层（Process Chain）落盘路径从旧 `.loop/`（点前缀隐藏 + gitignore + Wipe 删除）迁至 `process/`（显性 + 进版本库 + 重跑归档），可见性由「PM 主路径不可见」升为「PM 可直接查看审计」。中间工件默认留存，不再视作可丢弃构建快照。详见 ADR 0016。
```

## 审计三元组反模式（共享定义）

下列三条反模式在所有 PMSkill 的"不要做什么"表中统一引用本节，不重复展开：

| 反模式 | 为什么不要做 | 判定 |
|--------|------------|------|
| 审计三元组转换操作写"将 A 转换为 A'" | 同义反复，无推理密度 | Failure |
| 审计三元组转换操作写"基于上述依据产出" | 空话，未阐明具体推导逻辑 | Failure |
| 审计三元组转换操作写"经过分析得到" | 空话，必须写明是同义词推导/多对多实体映射/边界隔离分析之一 | Failure |

各 skill 反例表中该三条统一改为"审计三元组反模式——见 CONTEXT.md『审计三元组反模式（共享定义）』"。
