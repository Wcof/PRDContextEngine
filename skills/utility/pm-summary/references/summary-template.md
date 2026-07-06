# 汇总文档结构示例子

本文展示 `/pm-summary` 输出的汇总文档典型结构，供 skill 开发对照与 PM 阅读参考。示例子为虚拟项目「Geek AI 运营平台」。

## 示例 A：SUMMARY-需求.md

```markdown
# 需求 汇总 — Geek AI 运营平台

> 生成时间: 2026-07-06T19:53+08:00 | 来源产物: 7 份 | 跳过（未生成）: 6 份
> 本文档由 /pm-summary 从已落盘原产物拼装，原产物不动，每段标来源锚点可回原文。

## 目录
- [§1 PMContext](#§1) ← 来源: pm-context.md
- [§2 收集材料](#§2) ← 来源: collect/collected-materials.md
- [§3 假设清单](#§3) ← 来源: assumptions.md
- [§4 商业模式画布](#§4) ← 来源: business-model.md
- [§5 战略分析](#§5) ← 来源: strategy.md
- [§6 产品愿景](#§6) ← 来源: vision.md
- [§7 北极星指标](#§7) ← 来源: north-star.md
- [§8 质询压力测试](#§8) ← 来源: grill.md

---

## §1 PMContext

> 来源: `docs/pm-context/pm-context.md`

（原产物 pm-context.md 完整正文嵌入此处，不改写）

---

## §2 收集材料

> 来源: `docs/pm-context/collect/collected-materials.md`

（原产物正文）

---

...（§3~§8 按映射表顺序）

## 跳过清单（未生成的原产物）

| 原产物 | 来源 skill | 提示 |
|--------|-----------|------|
| `pestle.md` | /pm-pestle | ⚠️ 未生成，先跑 `/pm-pestle` |
| `market.md` | /pm-market | ⚠️ 未生成，先跑 `/pm-market` |
| `personas.md` | /pm-persona | ⚠️ 未生成，先跑 `/pm-persona` |
| `positioning.md` | /pm-positioning | ⚠️ 未生成，先跑 `/pm-positioning` |
| `metrics.md` | /pm-metrics | ⚠️ 未生成，先跑 `/pm-metrics` |
| `assumptions.md` | /pm-assumption | ⚠️ 未生成，先跑 `/pm-assumption` |
```

## 示例 B：SUMMARY-交付.md

```markdown
# 交付 汇总 — Geek AI 运营平台

> 生成时间: 2026-07-06T19:53+08:00 | 来源产物: 5 份 | 跳过（未生成）: 7 份
> 本文档由 /pm-summary 从已落盘原产物拼装，原产物不动，每段标来源锚点可回原文。

## 目录
- [§1 AI PRD](#§1) ← 来源: prd/ai-prd.md
- [§2 Human PRD](#§2) ← 来源: prd/human-prd.md
- [§3 用户故事](#§3) ← 来源: stories.md
- [§4 优先级排序](#§4) ← 来源: prioritize.md
- [§5 发布包](#§5) ← 来源: release.md

---

## §1 AI PRD

> 来源: `docs/pm-context/prd/ai-prd.md`

（原产物 ai-prd.md 完整正文嵌入）

---

## §2 Human PRD

> 来源: `docs/pm-context/prd/human-prd.md`

（原产物正文）

---

## §3 用户故事

> 来源: `docs/pm-context/stories.md`

（原产物 stories.md 完整正文嵌入，含 3C 框架 + INVEST 校验表 + 与草图差分段）

---

...（§4~§5）

## 跳过清单（未生成的原产物）

| 原产物 | 来源 skill | 提示 |
|--------|-----------|------|
| `roadmap.md` | /pm-roadmap | ⚠️ 未生成，先跑 `/pm-roadmap` |
| `okr.md` | /pm-okr | ⚠️ 未生成 |
| `sprint.md` | /pm-sprint | ⚠️ 未生成 |
| `stakeholder-map.md` | /pm-stakeholder | ⚠️ 未生成 |
| `gtm.md` | /pm-gtm | ⚠️ 未生成 |
| `pricing.md` | /pm-pricing | ⚠️ 未生成 |
| `interview-script.md` | /pm-interview | ⚠️ 未生成 |
```

## 示例 C：INDEX.md

```markdown
# PMSkill 产物总索引

> 生成时间: 2026-07-06T19:53+08:00 | 原产物文件数: 5 | 汇总文档: 5 份
> 由 /pm-summary 生成。原产物按 skill 拍平落盘，本索引帮你一眼定位"哪份在哪个主题汇总里"。

## 按主题汇总
| 汇总文档 | 涵盖原产物数 | 一句话 |
|----------|------------|--------|
| [SUMMARY-需求.md](SUMMARY-需求.md) | 7 | 需求全貌：上下文+市场+用户+战略+指标+风险 |
| [SUMMARY-交付.md](SUMMARY-交付.md) | 5 | 交付包：PRD+故事+发布+roadmap+OKR+sprint+干系人 |
| [SUMMARY-可视化.md](SUMMARY-可视化.md) | 0 | 可视化合集：线框+IA+状态机+流程+旅程+实体字典 |
| [SUMMARY-验证.md](SUMMARY-验证.md) | 0 | 验证与复盘：实验+A/B+队列+审计+回顾+合规 |
| [INDEX.md](INDEX.md) | — | 本文件 |

## 原产物清单（按 skill 主题分组）

### 需求（discovery + 核心）
| 路径 | 标题 | 来源 skill | 摘要 | 已汇总到 |
|------|------|-----------|------|---------|
| `pm-context.md` | PMContext: Geek AI 运营平台 | /pm-need | 面向个人和企业的 AI API 网关管理与运营系统 | SUMMARY-需求.md §1 |
| `collect/collected-materials.md` | 收集材料汇总 | /pm-collect | sub2api 功能分析 + geek-ai-web UI 风格指南 | SUMMARY-需求.md §2 |
| `assumptions.md` | 风险假设 | /pm-assumption | 8 类风险 × 置信度 + Top5 最便宜测试 | SUMMARY-需求.md §3 |
| `business-model.md` | 商业模式画布 | /pm-businessmodel | BMC 9 模块 + 业务游戏分类 + 收入流 | SUMMARY-需求.md §4 |
| `strategy.md` | 战略分析套件 | /pm-strategy | SWOT/Porter 五力/Ansoff 矩阵/Lean Canvas | SUMMARY-需求.md §5 |
| `vision.md` | 产品愿景 | /pm-vision | 三要素愿景 + 10/3/1 年阶梯 + 干系人地图 | SUMMARY-需求.md §6 |
| `north-star.md` | 北极星指标 | /pm-northstar | 单一 NSM + Input 星座 + guardrail | SUMMARY-需求.md §7 |
| `grill.md` | 质询压力测试 | /pm-grill | 红队攻击承重假设 + 八维置信度盘问 | SUMMARY-需求.md §8 |

### 交付（delivery）
| 路径 | 标题 | 来源 skill | 摘要 | 已汇总到 |
|------|------|-----------|------|---------|
| `prd/ai-prd.md` | AI PRD: Geek AI 运营平台 | /pm-aiprd | 技术栈契约 + 页面路由 + 数据模型 Mock | SUMMARY-交付.md §1 |
| `prd/human-prd.md` | Human PRD: Geek AI 运营平台 | /pm-humanprd | 产品概述 + 核心功能 + UI 风格 + 交付物 | SUMMARY-交付.md §2 |
| `stories.md` | 用户故事 | /pm-stories | 3C 框架 + INVEST 准则 + 验收标准 | SUMMARY-交付.md §3 |
| `prioritize.md` | 优先级排序 | /pm-prioritize | 6 框架场景推荐 + 四象限 + 排序 | SUMMARY-交付.md §4 |
| `release.md` | 发布包 | /pm-release | 发布说明 + 测试场景 + WWA backlog | SUMMARY-交付.md §5 |

### 可视化（visualization）
| 路径 | 标题 | 来源 skill | 摘要 | 已汇总到 |
|------|------|-----------|------|---------|
| — | — | — | 本主题无产物落盘 | — |

### 验证 / 其他
| 路径 | 标题 | 来源 skill | 摘要 | 已汇总到 |
|------|------|-----------|------|---------|
| — | — | — | 本主题无产物落盘 | — |

## 未生成清单
| 原产物 | 来源 skill | 提示 |
|--------|-----------|------|
| `pestle.md` | /pm-pestle | ⚠️ 未生成，先跑 `/pm-pestle` |
| `market.md` | /pm-market | ⚠️ 未生成 |
| `personas.md` | /pm-persona | ⚠️ 未生成 |
| `positioning.md` | /pm-positioning | ⚠️ 未生成 |
| `metrics.md` | /pm-metrics | ⚠️ 未生成 |
| `sketch/wireframe.md` | /pm-sketch | ⚠️ 未生成，先跑 `/pm-sketch` |
| `experiment.md` | /pm-experiment | ⚠️ 未生成 |
| ... | ... | ... |
```

## 避坑提示

| 坑 | 怎么避 |
|----|--------|
| 改写原产物措辞 | 汇总段必须原样嵌入，不改写不 paraphrase，保原标记 `[假设]`/`[待确认]`/`[冲突]` |
| 来源锚点只标文件级 | 必须标到 heading 级 `> 来源: path#<heading>`，让读者一键回原文具体位置 |
| 缺失补内容 | 缺失放跳过清单，不补"我猜这里应该是 XXX" |
| 汇总落子目录 | 汇总必须在最外层，与 `pm-context.md` 同级，命名 `SUMMARY-*.md` / `INDEX.md` |
| 写原产物路径 | 本 skill 全程只读原产物，写 `prd/`、`sketch/`、`collect/`、`process/` 会破坏下游协议 |
| 重刷堆积旧版本 | 幂等覆盖，不保留旧版本不追加 |
```
