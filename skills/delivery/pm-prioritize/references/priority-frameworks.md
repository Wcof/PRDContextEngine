# 优先级框架参考库

6 框架完整公式、when-to-use、模板。按场景选用单一框架，禁混算。

## 核心原则

优先**问题（机会）**而非解决方案（功能）。让客户设计解决方案是产品失败最快路径。

## 1. Opportunity Score（Dan Olsen, *Lean Product Playbook*）

排客户问题/机会的首选框架。调研客户对每需求的 Importance 与 Satisfaction（归一化 0–1）。

三公式：
- 当前价值 = Importance × Satisfaction
- **Opportunity Score** = Importance × (1 − Satisfaction)
- 创造价值 = Importance × (S2 − S1)，S1=改前满足，S2=改后

高重要 + 低满足 = 最高 Opportunity Score = 最佳机会。画 Importance vs Satisfaction 图，左上象限是甜点区。优先客户问题非方案。

**When to use**：排客户问题/机会；有 Importance+Satisfaction 调研数据。

## 2. ICE

排创意/倡议，兼顾价值、风险、经济。

- I（Impact）= Opportunity Score × 影响客户数
- C（Confidence）= 多确信？1-10，含风险
- E（Ease）= 多易实现？1-10，含经济

Score = I × C × E，越高越优先。

**When to use**：排倡议/创意；需兼顾风险与成本但粒度不需太细。

## 3. RICE

把 ICE 的 Impact 拆为 Reach×Impact，适合大团队需更细粒度。

Score = (Reach × Impact × Confidence) / Effort

- Reach：触达人数（每周期）
- Impact：1-5，对单人影响
- Confidence：0-100%
- Effort：人月/人周

**When to use**：大团队；需区分触达与单点影响；有量化数据。

## 4. MoSCoW

定性分类，划定发布范围。

- **Must**：必须有，否则发布无意义
- **Should**：应有，重要但非阻塞
- **Could**：能有，锦上添花
- **Won't**：这次不会有，明确排除

**When to use**：发布范围划定；需求必须分类而非排序；定性足够。

## 5. Kano

按客户期待类型分类功能。

- **基本型**：没有就愤怒，有了无感
- **性能型**：越多越好，线性满意度
- **兴奋型**：没有无感，有了惊喜

画满意度曲线，识别哪些是基本门槛、哪些是差异化投入。

**When to use**：功能满意度分类；判断哪些是门槛哪些是差异化；有客户期待调研。

## 6. WSJF（Weighted Shortest Job First）

敏捷迭代带 cost-of-delay。

Score = (用户价值 + 时间价值 + 风险降低/机会启用) / 作业量

分子越大越紧急，分母越小越便宜，比值越大越优先。

**When to use**：敏捷迭代；需考虑 cost-of-delay；有作业量估算。

## 框架选择速查

| 你要排… | 用… |
|---|---|
| 客户问题/机会 | Opportunity Score |
| 倡议/创意（含风险经济） | ICE |
| 大团队细粒度 | RICE |
| 发布范围定性分类 | MoSCoW |
| 功能期待类型 | Kano |
| 敏捷迭代带延迟成本 | WSJF |
