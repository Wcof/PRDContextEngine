# PMContext: Skill 质量看板

## 概述

### 问题与目标
PMSkill 项目中散落着 13 个 SKILL.md（加 darwin-skill 共 14 个），PM 无法直观了解每个 skill 的质量水平、短板分布和优化优先级。需要提供一个**质量看板 Dashboard**，自动扫描所有 SKILL.md，按 darwin-skill 的 9 维 rubric 打分，展示评分卡和短板分析，帮助 PM 一眼看出哪些 skill 需要优化。

### 现状平替与摩擦力
目前 PM 想了解 skill 质量需要手动阅读每个 SKILL.md，或者每次调用 darwin-skill 运行评估流程。没有历史趋势、没有横向对比、没有可视化仪表盘。摩擦力在于：无法持续追踪质量变化，优化效果只能靠记忆。

### 价值验证度量
- 核心度量：看板首次加载后 PM **定位最弱 skill 的时间**从 >5 分钟降到 <30 秒
- 辅助度量：每周看板访问次数（预期 ≥3 次/周）、优化决策采纳率

## 用户场景
### 事实
- PM 是每天使用 PMSkill 的产品经理
- 场景：PM 在日常工作中需要知道"我的 skill 质量怎么样"
- 场景：PM 在做 darwin-skill 优化前需要快速定位最有改进空间的 skill
- 场景：优化后 PM 需要确认分数是否真正提升

### 规则
- 看板必须从所有 `skills/*/SKILL.md` 读取数据，不需要 PM 手动配置
- 评分必须使用 darwin-skill 的 9 维 rubric（d1-d9）
- 每个 skill 展示：总评分、维度雷达图、短板 Top-3、趋势（如果 history 存在）
- [假设] 看板数据每天更新一次（通过 scheduled scan 或手动触发）

### 验收
- 打开看板看到所有 skill 的评分卡
- 每张评分卡展示评分、短板、上次评估时间
- 按分数升序/降序排列
- 点击 skill 查看维度的详细评分

## 数据模型
### 事实
- `Skill`: name, description, type (user-invoked/model-invoked), 路径
- `Score`: skill_id, total_score, 维度分(d1-d9), eval_mode, timestamp, commit_hash
- `History`: 与 Score 1对多关系，支持趋势展示
- `Bucket`: setup/discovery/delivery/visualization, 包含多个 Skill

### 规则
- 每个 Skill 可以有多次 Score 记录（趋势追踪）
- Score 的维度分必须对应精确的 d1-d9 权重 ← PMContext: darwin-skill rubric
- 数据来源：每次 darwin-skill 评估后写入 results.tsv，看板从此文件读取

### 验收
- 数据模型覆盖 Skill / Score / History / Bucket
- Score 关联到 Skill，且包含完整维度分
- History 记录支持 delta 趋势追踪

## 全局约束
| 约束 | 说明 |
|------|------|
| 数据源 | results.tsv（由 darwin-skill 维护），避免双重写入 |
| 展示格式 | HTML 页面，嵌入 git 仓库直接访问（无服务端） |
| 无需后端 | 纯前端方案，JSON 或 TSV to HTML |
| 兼容性 | 在 Claude Code / Codex / Cursor 等 agent 中可直接打开 |

## 决策日志
| 决策点 | 选项A | 选项B | 最终选择 | 理由 | 来源 |
|--------|------|------|---------|------|------|
| 数据源 | results.tsv 直接解析 | 独立 DB | results.tsv | 避免两种数据源不一致 | 对话上下文 |
| 看板形态 | 静态 HTML | 动态 web app | 静态 HTML | 无需服务端，git 仓库可直接打开 | 项目扫描: README.md |
| 排序方式 | 分数升序（最弱在前） | 字母序 | 分数升序 | PM 最关心最弱的 skill | 对话上下文 |

## 假设清单与验证计划
| 假设 | 置信度(1-10) | 风险类型 | 验证方式 | 成功指标/阈值 | 验证时机 |
|------|------------|---------|---------|--------------|---------|
| PM 每天都需要看板 | 6 | 采纳风险 | 首次部署后观察使用频率 | ≥3次/周 | 上线后2周 |
| results.tsv 作为数据源足够 | 8 | 技术风险 | 检查 results.tsv 格式稳定性 | 数据完整性和格式一致性 | 看板开发时验证 |

## 风险项
- [待确认] 看板是否需要支持 manual refresh 按钮
- [假设] 用户需要趋势图（置信度 7）

## 信息缺口
- 数据源：results.tsv 的格式是否稳定？需要确认 darwin-skill results.tsv 的列结构
- 展示粒度：PM 需要看到维度级别的详情吗？还是总分就够了？
