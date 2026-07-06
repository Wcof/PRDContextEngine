# PMSkill 质量看板 AI PRD

## 概述

为 PMSkill 项目生成一个 Skill 质量看板 Dashboard，自动从 `results.tsv` 读取所有 SKILL.md 的 9 维评分数据，展示评分卡、短板分析和趋势变化，帮助 PM 直观了解每个 skill 的质量水平和优化优先级。

## Agent Context

### 技术栈与约束
- 纯前端静态 HTML（无服务端）← PMContext: 全局约束
- 数据源：`.claude/skills/darwin-skill/results.tsv`
- 评分维度：9 维 rubric（d1-d9）
- 无需后端，git 仓库可直接打开预览

### 目录结构约定
```
docs/pm-context/
  pm-context.md          ← Entity
  prd/
    ai-prd.md            ← 本文件
    human-prd.md         ← 给人的 PRD
  sketch/
    dashboard.html       ← 看板原型（由本 PRD 驱动的产出）
```

### 关键模块位置
- 数据源：`.claude/skills/darwin-skill/results.tsv`
- skill 定义：`skills/*/SKILL.md`
- PMContext：`docs/pm-context/pm-context.md`

## 用户故事

1. As a PM, I want to see all skills displayed as score cards, so that I can quickly know the overall quality landscape. ← PMContext
2. As a PM, I want to sort skills by score (ascending), so that the weakest skills appear first. ← PMContext: 决策日志
3. As a PM, I want to see each skill's Top-3 weaknesses (lowest dimensions), so that I know what to improve. ← PMContext: 验收
4. As a PM, I want a 9-dimension radar chart for each skill, so that I can compare dimension scores at a glance. ← [假设] PMContext 未显式要求雷达图，推断自"维度评分"规则
5. As a PM, I want score trends if history exists, so that I can track improvement or regression. ← [假设] PMContext 未显式要求趋势，推断自"历史"数据模型
6. As a PM, I want to see bucket groupings (setup/discovery/delivery/visualization), so that I can evaluate by product area. ← PMContext: 数据模型.Bucket

## 实施规则

1. **数据自动加载** — 从 `results.tsv` 解析，无需手动配置 ← PMContext: 规则
2. **评分使用 9 维 rubric** — d1-d9 对应 darwin-skill 权重 ← PMContext: 规则
3. **排序默认升序** — 最弱 skill 排在最前 ← PMContext: 决策日志
4. **看板使用静态 HTML** — 嵌入 git 仓库直接访问，不依赖服务端 ← PMContext: 全局约束
5. **数据质量检查** — results.tsv 读不到时显示"等待首次评估"占位

## 数据模型

### Skill
- `name`: string — skill 名称（如 pm-need）
- `bucket`: setup/discovery/delivery/visualization
- `type`: user-invoked / model-invoked
- `description`: string — 来自 SKILL.md frontmatter

### Score
- `skill`: Skill — 关联 skill
- `total`: number — 总分 0-100
- `d1-d9`: number — 各维度得分
- `eval_mode`: full_test / dry_run
- `timestamp`: date — 评估时间
- `commit`: string — git commit hash

## 验收标准

### US-1: 评分卡展示
- **目标**: 打开看板能看到所有 13 个 skill 的评分卡
- **前置条件**: results.tsv 至少有 baseline 数据
- **预期结果**: 每个 skill 一张卡片，含名称、总分、类型、bucket 标签
- **边界场景**: results.tsv 为空 → 显示"等待 darwin-skill 首次评估"引导

### US-2: 按分数排序
- **目标**: 默认升序排列，最弱在前
- **操作**: 打开看板 → 检查默认排序
- **预期结果**: 分数最低的 skill 在列表最上方

### US-3: 短板分析
- **目标**: 每张卡片展示 Top-3 最弱维度
- **操作**: 查看任意评分卡
- **预期结果**: 卡片上显示"短板：d3(5/12) d4(4/6) d9(3/6)"

### US-6: Bucket 分组
- **目标**: 按 setup/discovery/delivery/visualization 分组展示
- **操作**: 看板顶部有 Bucket 切换标签
- **预期结果**: 切换标签只显示对应 bucket 的 skill

## 风险项
- [待确认] 看板是否需要支持手动 refresh 按钮 ← PMContext: 风险项
- [假设] 用户需要趋势图（置信度 7）← PMContext: 风险项

## 超出范围
- 服务端渲染 — 静态 HTML 足够，无需后端
- 细粒度权限 — 单用户使用场景
- 自动定时扫描 — 依赖 darwin-skill 的扫描流程
