# PM Prototype Design Style System

> `/pm-sketch --prototype` 的内置视觉与 UE 增强协议。它借鉴「anti-slop frontend skill」类方法论的核心思想：先读场景，再定审美方向、密度、动效和组件语言；但本文件面向 PMSkill 的多页产品原型、后台、工具、工作流、仪表盘和 AI Native 系统，不是外部 skill 的复制件，也不依赖联网或安装外部包。

## 0. 适用范围

本协议用于提升原型系统的样式、信息层级和交互体验。它不是替代 PMContext 的新需求源，不能新增未经 PMContext 支撑的功能。

适用：
- SaaS / B2B / 后台管理 / 业务系统
- AI Native 工具 / agent 工作台 / workflow builder
- 数据分析 / 监控 / 仪表盘
- 消费者产品 / 移动 Web 原型
- 官网、营销页、产品介绍页中的原型级页面

不适用：
- 用审美替代需求决策
- 为了“好看”删掉 PMContext 中的规则、验收、状态和边界
- 生成无法追溯、无法点击、只有视觉壳的页面

## 1. Design Read：先读场景，再定风格

生成任何原型前，必须基于 PMContext、DESIGN.md 和用户显式风格要求输出一行 Design Read：

```text
Reading this as: <产品类型> for <核心用户/使用场景>, with a <视觉语言>, leaning toward <组件/布局体系>.
```

中文输出时可写：

```text
设计读取：这是面向 <核心用户/场景> 的 <产品类型>，采用 <视觉语言>，倾向 <组件/布局体系>。
```

读取信号优先级：
1. 用户本轮显式要求：如“深色、AI Native、Linear 风、苹果感、企业级、极简、Awwwards、赛博、可信、政府风”。
2. `docs/design/DESIGN.md`：品牌色、字体、视觉气质、禁用项。
3. PMContext：用户、场景、复杂度、页面类型、风险/合规/信任要求。
4. 默认风格库：仅当前三者不足时使用。

## 2. 三个视觉拨盘

为防止模型默认生成“紫色渐变 + 三张卡片 + 毛玻璃”，每次必须显式设置三个拨盘并写入 `prototype-design-profile.json`：

| 拨盘 | 取值 | 含义 |
|---|---:|---|
| `design_variance` | 1-10 | 1=高度标准化，10=强表达/非对称/实验感 |
| `motion_intensity` | 1-10 | 1=几乎静态，10=强动效/电影感 |
| `visual_density` | 1-10 | 1=留白很大，10=信息密集/控制台感 |

默认推荐：
- 企业 SaaS / 管理后台：`4 / 3 / 7`
- AI Native 工具：`7 / 5 / 6`
- 数据仪表盘：`5 / 4 / 8`
- 可信/合规/金融/政务：`3 / 2 / 6`
- 消费者产品：`7 / 6 / 4`
- 营销页/品牌页：`8 / 6 / 3`

## 3. 风格家族

根据 Design Read 选择一个主风格，最多一个辅助风格。禁止同一原型里混用多套视觉语言。

### 3.1 Enterprise Calm

适合：B2B SaaS、CRM、ERP、权限/审批、供应链、内部工具。

视觉：浅色或中性深色、清晰分区、克制阴影、可靠的表单/表格、明确状态色。

UE：强调效率、批量操作、可恢复、可追踪；不要做大面积炫技动效。

### 3.2 AI Native Dark

适合：Agent 工作台、AI 网关、Prompt/Workflow 管理、模型监控、自动化编排。

视觉：深色底、分层面板、状态光点、命令式工具栏、工作流节点、代码/日志/会话混合布局。

UE：强调“输入 → 推理 → 工具调用 → 结果 → 审计”的链路可见；避免只有聊天框和紫色光晕。

### 3.3 Data Cockpit

适合：BI、监控、指标、A/B、队列分析、运营面板。

视觉：高密度但分组明确；图表、筛选器、摘要指标、异常列表并列。

UE：必须有筛选、排序、时间范围、空态、异常态和 drill-down 入口。

### 3.4 Premium Consumer

适合：电商、生活方式、会员、内容、创作者工具。

视觉：更强品牌感、更大图像区、更少边框、更强字体层级。

UE：强调首屏吸引、决策路径、信任背书、转化动作。

### 3.5 Trust First

适合：金融、医疗、政务、合规、安全、法务。

视觉：低饱和、清晰文本、可解释状态、可靠边框、少动效。

UE：必须突出权限、审计、风险、确认和可撤销。

### 3.6 Developer Tool

适合：API、CLI、DevOps、SDK、日志、配置、规则引擎。

视觉：代码区、命令面板、文档旁栏、状态徽章、结构化配置。

UE：强调复制、测试、验证、版本、diff 和回滚。

## 4. Token 生成协议

从 Design Read 派生 token，写入 `prototype-design-profile.json` 并注入 Simple/Scaffold/Pencil MCP brief：

```json
{
  "mode": "prototype-design-profile",
  "design_read": "...",
  "style_family": "AI Native Dark",
  "secondary_style": "Developer Tool",
  "dials": {"design_variance": 7, "motion_intensity": 5, "visual_density": 6},
  "tokens": {
    "theme": "dark",
    "accent": "electric-blue",
    "radius_scale": "md-lg",
    "shadow_style": "layered-soft",
    "type_scale": "compact-product",
    "spacing_scale": "8px grid"
  },
  "layout_patterns": ["command-shell", "split-workbench", "status-timeline"],
  "interaction_patterns": ["inline-run", "toast-result", "error-recovery", "audit-drawer"],
  "anti_patterns_banned": ["empty route shell", "fake glass cards", "random purple glow"]
}
```

### 4.1 CSS Token 底线

Simple 模式：token 必须内联在 `:root` 和 `[data-theme="dark"]` 中。

Scaffold 模式：token 必须写入 `src/style.css`，放在 `@import "tailwindcss";` 后。

Pencil MCP 模式：token 必须作为 MCP brief 的设计 profile 输入，并在 manifest 的 `design_profile` 字段中记录。

### 4.2 禁止默认审美

以下默认一律禁止，除非 PMContext 或 DESIGN.md 明确要求：
- 随机紫蓝渐变作为所有项目默认主视觉
- 全页面毛玻璃卡片
- 三张等宽 feature card 反复堆叠
- 只有图标 + 标题 + 一句话的空卡片
- 假截图矩形块、假图表、假终端但无真实交互
- 动效过多导致主任务不清晰

## 5. 页面布局协议

每个页面从 `prototype-content-plan.json` 渲染时，必须选择一个结构化页面骨架，而不是只堆卡片。

| 页面类型 | 推荐布局 |
|---|---|
| 工作台 / 控制台 | 顶部全局状态 + 左侧任务/导航 + 主工作区 + 右侧详情/审计抽屉 |
| 表单 / 创建流程 | 步骤条 + 表单主体 + 规则提示 + 预览/风险面板 |
| 列表 / 管理页 | 筛选栏 + 批量动作 + 数据表/卡片 + 空态/异常态 + 详情抽屉 |
| 详情页 | 标题状态区 + 摘要指标 + 分组信息 + 时间线/日志 + 下一步动作 |
| 流程 / 编排页 | 节点画布 + 属性面板 + 执行日志 + 验证结果 |
| 仪表盘 | 北极星指标 + 关键趋势 + 分组图表 + 异常/行动建议 |
| 营销/介绍页 | 场景首屏 + 真实产品预览 + 价值证明 + 机制解释 + CTA |

## 6. UE 质量规则

每页至少体现以下 5 类 UE 元素中的 4 类：
1. 主任务 CTA：用户下一步做什么非常明确。
2. 状态反馈：成功、加载、失败、空态至少覆盖一个真实业务状态。
3. 规则可见：把 PMContext 中的规则/验收转成可见提示、校验、badge、清单或限制说明。
4. 信息层级：标题、摘要、主体、辅助信息的视觉权重不同。
5. 错误恢复：失败时给出下一步，而不是只显示“错误”。
6. 审计/来源：能看到数据或决策来自哪个 PMContext/PRD 锚点。

## 7. Pencil MCP 设计 brief 协议

当 Pencil MCP 命中时，传入 MCP 的 brief 必须包含：
- `prototype-content-plan.json` 全量页面内容计划
- `prototype-design-profile.json` 视觉 profile
- 页面布局协议：每页选择的 layout pattern
- UE 质量规则：主任务、状态反馈、规则可见、错误恢复、审计来源
- 禁止项：空 route、假截图、无 trace 的装饰元素、只画导航不画业务内容

Pencil MCP 返回后，manifest 必须记录：

```json
{
  "design_profile": "docs/pm-context/sketch/prototype-design-profile.json",
  "style_family": "<selected family>",
  "ue_coverage": {
    "primary_cta_pages": 0,
    "state_feedback_pages": 0,
    "rule_visible_pages": 0,
    "error_recovery_pages": 0
  }
}
```

## 7.5 视觉可见性与对比度协议

原型系统验收不能只看“页面是否生成、元素是否存在”。如果元素存在但人眼不可见，同样判定失败。以下规则对 Pencil MCP、Simple、Scaffold 三种模式都生效：

### 7.5.1 必须生成的 token

设计 profile 与 design-source-manifest 至少要包含：

```json
{
  "color_bg": "#ffffff",
  "color_surface": "#f9fafb",
  "color_text": "#111827",
  "color_text_secondary": "#374151",
  "color_text_muted": "#6b7280",
  "color_accent": "#2563eb",
  "color_on_primary": "#ffffff",
  "color_border": "#d1d5db",
  "color_success": "#10b981",
  "color_on_success": "#052e16",
  "color_warning": "#f59e0b",
  "color_on_warning": "#422006",
  "color_danger": "#ef4444",
  "color_on_danger": "#280000"
}
```

禁止只给 `accent: electric-blue` 这类抽象语义名。抽象语义可以存在，但必须同步解析成具体颜色值。
供 V1 静态脚本验收的 required color token 必须归一化为 `#hex` 或 `rgb(a)`；`oklch()` 等其它格式应在写入审计输入前转换，否则按不可解析失败。

### 7.5.2 必查对比关系

- 正文 / 表单 / 表格 / 导航文字 vs 页面背景：≥ 4.5:1
- 正文 / 表单 / 表格 / 导航文字 vs 卡片/表格行/二级面板背景：≥ 4.5:1
- 大标题、弱提示、边框、图标、焦点环：≥ 3:1
- 主按钮文字 `color_on_primary` vs 主按钮背景 `color_accent`：≥ 4.5:1
- 错误/警告/成功状态文字 vs 状态底色：≥ 4.5:1

### 7.5.3 可点击元素可见性

所有 `button`、`a[href]`、`[role=button]`、菜单项、表格操作项、表单控件必须满足：

- 默认态可见；hover/active/disabled/loading 至少有文字、图标、边框、背景中的一种明显区分。
- 不能出现 `color` 与 `background` 相同或接近。
- 不能通过 `opacity < 0.2`、`visibility:hidden`、`display:none` 或透明 overlay 保留点击区域。
- focus ring 必须可见，且与周围背景对比 ≥ 3:1。

### 7.5.4 审计产物

每次生成原型都必须写 `sketch/visual-audit-report.json`。只有当 `status=passed` 且 `contrast_failures=0`、`invisible_interactive_count=0` 时，才能在最终报告中打 ✅。Pencil MCP 若无法提供可解析 artifact，只能标 `needs-manual-review`，不能伪装为已通过。

## 8. 自检清单

生成完成前必须自检：

- [ ] Design Read 已输出并落盘到 `prototype-design-profile.json`
- [ ] 主风格家族唯一，辅助风格不超过一个
- [ ] 三个拨盘有明确数值且与 PMContext 场景一致
- [ ] token 已进入对应实现模式（Pencil MCP / Simple / Scaffold）
- [ ] 已生成 `visual-audit-report.json`，且文字/背景、按钮、导航、表格、focus ring 对比度通过
- [ ] 没有“元素存在但人眼不可见”的按钮、链接、表单、菜单或表格操作项
- [ ] 每页不是同一张卡片模板复制，而是按页面类型选择布局
- [ ] 每页至少 4 类 UE 元素达标
- [ ] 禁止默认审美未出现
- [ ] 好看没有覆盖追溯：`data-trace-ref` / manifest source 仍完整
