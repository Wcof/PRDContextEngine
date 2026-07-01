# 风险假设识别完整示例

## 场景

会员产品从 PMContext 识别 8 类风险假设。

## 三视角思考

- PM 视角：市场需求/付费意愿/竞争/定价
- Designer 视角：首次体验/onboarding/认知负荷/可用性
- Engineer 视角：build vs buy/可扩展/技术债/算法可行性

## 8 类风险假设（共 12 条）

| 类型 | 假设 | 置信度 | 来源 |
|------|------|--------|------|
| Value | 用户会持续用（非尝鲜） | 6 | PMContext 用户场景 |
| Value | 断更是创作者真痛点（非我们臆想） | 7 | PMContext 现状平替 |
| Usability | 用户能 5 分钟上手智能排期 | 5 | 推断 |
| Usability | 断更预警不会被当骚扰 | 6 | 推断 |
| Viability | ¥30/月能覆盖成本（LTV>CAC） | 4 | PMContext 边界条件 |
| Feasibility | 推荐算法 M1 8G 服务器可跑 | 7 | PMContext 技术约束 |
| Feasibility | 200+ 模板 3 月内可建 | 5 | 推断 |
| Ethics | 创作数据收集合规 | 8 | PMContext 边界条件 |
| GTM | 创作者社群渠道能触达 ICP | 5 | PMContext 用户场景 |
| Strategy | 竞品 6 月内不复制预警功能 | 4 | PMContext 竞品层 |
| Strategy | 平台 API 政策不变 | 6 | 推断 |
| Team | 算法团队 3 月内不流失 | 6 | 推断 |

## 优先级排序（Impact×Likelihood wrong）

| 排名 | 假设 | Impact | Likelihood wrong | 优先级 |
|------|------|--------|-----------------|--------|
| 1 | [Viability] ¥30/月覆盖成本 | 10 | 6 | 🔴 最高 |
| 2 | [Strategy] 竞品 6 月内不复制 | 8 | 6 | 🔴 高 |
| 3 | [GTM] 社群渠道触达 ICP | 8 | 5 | 🟡 中高 |
| 4 | [Usability] 5 分钟上手 | 6 | 5 | 🟡 中 |
| 5 | [Feasibility] 200+ 模板 3 月内 | 5 | 5 | 🟡 中 |

## Top 5 最便宜测试

| # | 假设 | Fails if | 本周证据 | 最便宜测试（pm-grill 成本阶梯） |
|---|------|---------|---------|-----------------------------|
| 1 | ¥30/月覆盖成本 | LTV<¥360 或 CAC>¥200 | 查现有付费用户 LTV+CAC | 已有数据查询（<1 人日） |
| 2 | 竞品 6 月内不复制 | 竞品 X 发布预警功能 | 监控竞品 changelog | web search 监控（<0.5 人日） |
| 3 | 社群触达 ICP | 社群获客转化<2% | 投放社群测试帖 | landing page+社群帖（2 人日） |
| 4 | 5 分钟上手 | 新用户 5 分钟完成率<60% | 5 用户可用性测试 | 5 用户访谈（pm-interview，3 人日） |
| 5 | 200+ 模板 3 月内 | 模板产能<70/月 | 试产 1 周模板 | 试产产能测试（5 人日） |

## 回灌 PMContext

Top 5 假设回灌 PMContext 假设清单段，置信度+最便宜测试标注，联动 pm-experiment（验证闭环）+ pm-grill（质询）。

## 审计三元组

`<依据集: [PMContext 全维度+三视角思考]> → [工具: /pm-assumption, 规则: 8 类风险×置信度×Impact×Likelihood] → [转换: 从 PMContext 各维度推导 8 类假设，多对多实体映射：PMContext 维度→风险类型→假设] → <产出: 12 假设+Top5 优先级+最便宜测试+回灌>`
