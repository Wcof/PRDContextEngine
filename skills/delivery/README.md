# Delivery

交付——从 PMContext 生成可交付的 PRD、发布包与质量审计。

## User-invoked

无。

## Model-invoked

- **[pm-prd](./pm-prd/SKILL.md)**（Hybrid）— 从 PMContext 生成 PRD 文档（给 AI 和给人两种形态）。
- **[pm-handoff](./pm-handoff/SKILL.md)** — 把当前 PMSkill 会话压缩成交接文档，供下一个 Agent 接续。
- **[pm-aiprd](./pm-aiprd/SKILL.md)** — 从 PMContext 生成给 AI 执行的 PRD。
- **[pm-humanprd](./pm-humanprd/SKILL.md)** — 从 PMContext 生成给人阅读的 PRD。
- **[pm-premortem](./pm-premortem/SKILL.md)**（Hybrid）— 从 PMContext 假设上线失败倒推风险，产出 Tiger/Paper Tiger/Elephant 三分 + 行动计划。
- **[pm-stories](./pm-stories/SKILL.md)** — 从 PMContext 生成用户故事——3C 框架 + INVEST 准则 + 验收标准。
- **[pm-gtm](./pm-gtm/SKILL.md)** — 从 PMContext 生成 GTM 策略——Beachhead 四准则 + ICP 画像 + 渠道矩阵 + 信息阶梯 + 发布时间线。
- **[pm-experiment](./pm-experiment/SKILL.md)** — 从 PMContext 生成假设验证闭环——8 类风险假设 + Impact×Risk 矩阵 + XYZ 假设 + pretotype 含 skin-in-the-game。
- **[pm-retro](./pm-retro/SKILL.md)** — 从 PMContext 与迭代产物生成回顾——三格式 + 主题聚合 + 行动项三要素 + 经验回灌。
- **[pm-prioritize](./pm-prioritize/SKILL.md)** — 从 PMContext 做优先级排序——6 框架场景推荐 + 单框架评分 + 四象限 + 排机会不排功能。
- **[pm-pricing](./pm-pricing/SKILL.md)** — 从 PMContext 生成定价与变现策略——模型按业务游戏 + 竞品矩阵 + Van Westendorp WTP + 弹性 + 3-5 变现方案。
- **[pm-release](./pm-release/SKILL.md)** — 从 PMContext 与产物生成发布包——发布说明 + 测试场景 + WWA backlog 三性自检。
- **[pm-align](./pm-align/SKILL.md)** — 审计已实现代码与 PMContext/AI PRD 的意图差距——意图模型 + 实现证据 file:line + gap 分级 + 修复建议。
- **[pm-triage](./pm-triage/SKILL.md)** — 从 PMContext 与产物把需求/缺陷/PR 分流过状态机 + 垂直切片拆 tracer-bullet issue + 写 agent-ready brief。
- **[pm-abtest](./pm-abtest/SKILL.md)** — A/B 测试统计分析——样本量/SRM 验证 + 显著性计算（p/CI/lift）+ guardrail 检查 + ship/extend/stop 决策。
- **[pm-cohort](./pm-cohort/SKILL.md)** — 队列分析——分队列 + 留存/采纳曲线 + 异常队列定位 + 跟进研究建议。
- **[pm-sql](./pm-sql/SKILL.md)** — 自然语言→多方言 SQL——schema 读取 + 查询逻辑 + 方言适配 + 性能优化 + 验证脚本。
- **[pm-okr](./pm-okr/SKILL.md)** — OKR 拆解——定性 Objective + 3 定量 KR（60-70% 信心）+ 三套候选 + KR/KPI/NSM 关系澄清。
- **[pm-sprint](./pm-sprint/SKILL.md)** — 迭代规划——容量估算（公式）+ 故事选取（DoR 校验）+ 依赖映射 + 风险 + Sprint Goal。
- **[pm-meeting](./pm-meeting/SKILL.md)** — 会议纪要结构化——日期/参与者/决策/行动项（owner+截止）/未决问题。
- **[pm-roadmap](./pm-roadmap/SKILL.md)** — output→outcome roadmap 转换——Enable/so that 格式 + 度量 + 替代方案考量。
- **[pm-battlecard](./pm-battlecard/SKILL.md)** — 竞品作战卡——对比表+优势+反制+异议话术+地雷问题+赢/输模式。
- **[pm-stakeholder](./pm-stakeholder/SKILL.md)** — 从 PMContext 生成干系人地图与分层沟通计划。
