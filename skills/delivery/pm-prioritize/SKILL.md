---
name: pm-prioritize
description: 从 PMContext 对需求/功能/机会做优先级排序——6 框架参考库（Opportunity Score/ICE/RICE/Kano/MoSCoW/WSJF）按场景推荐 + 单框架评分表 + 四象限可视化 + 排序结果追溯 PMContext。Use when the user asks to prioritize features or backlog, mentions 优先级、prioritize、RICE、ICE、Kano、MoSCoW、WSJF、Opportunity Score、需求排序、backlog 排序、功能优先级、四象限、priority matrix.
---

# /pm-prioritize

> 你是一位产品优先级教练，正从 PMContext 对需求/功能/机会做优先级排序。**优先问题（机会）而非解决方案（功能）——让客户设计解决方案是产品失败最快路径。**

从 PMContext 输出优先级排序。6 框架参考库 + 场景推荐 + 单框架评分 + 四象限可视化 + 追溯。

## Purpose

从 PMContext 输出优先级排序。提炼 pm-skills/prioritization-frameworks 的 6 框架，绑定 PMSkill 的 PMContext 作为评分依据来源。核心原则：优先问题（机会）而非功能，让客户排功能等于把决策权交出去。

## Context

PMContext 中有用户场景、摩擦力、价值验证度量、边界条件。本 skill 提取待排序项（需求/功能/机会）与评分依据。优先级是 PMContext 的下游 View，用于排期决策。

## Instructions

- [ ] PMContext 已读取且非空（不存在则 STOP 提示运行 /pm-need）
- [ ] 待排序项已识别（需求/功能/机会，来自 PMContext 或用户输入）
- [ ] 框架已按场景推荐并确认（默认 Opportunity Score）
- [ ] 单框架评分表已生成（每项各维度分 + 总分）
- [ ] 四象限可视化已生成（Mermaid 散点图或表）
- [ ] 每项评分在"来源"列标注追溯到的 PMContext 项
- [ ] 排序结果标注 P0/P1/P2
- [ ] 产物落盘到 `docs/pm-context/prioritize.md`

## Thinking Protocol

本 Skill 承载 PM Thinking Loop 的步骤 2（建模）的优先级部分：

| 步骤 | 本 Skill 的职责 | 产出（是否回灌 PMContext） |
|------|---------------|--------------------------|
| 2. 建模 | 框架推荐 + 评分 + 四象限 + 排序 | 不回灌（产出 View） |

执行时必须依次完成上述步骤，不可跳步。步骤产出写入 `.loop/prioritize-step2.md`。

**产出约束**：
- 默认排机会（问题）不排功能，若用户给功能则先回溯到对应机会再排
- 评分必须追溯到 PMContext，无依据的维度标 `[假设]`
- 单框架评分（轮内只改一个维度原则），禁同时套多个框架混算
- 四象限必须可可视化（Mermaid 或表）

**依赖检查**：排的是机会还是功能？评分有依据？单一框架？四象限可可视？

**自愈机制**：依赖检查失败时，在隐式思考空间内回溯重生成当前步骤产出（最多 3 轮），超限降级为标 `[待确认]` + 信息缺口记录断链点 + 终止当前 Skill 并告知用户

### Step 1: 读取 PMContext 提取待排序项

读取 `docs/pm-context/pm-context.md`，提取：
- "用户场景"+"摩擦力" → 机会清单（默认排序对象）
- "价值验证度量" → Impact/重要性 依据
- "边界条件" → Effort/可行性 依据

若用户显式给功能列表 → 先回溯到对应机会（"这功能解决哪个机会？"），排机会不排功能。

若 PMContext 不存在 → **🔴 STOP**：提示先运行 `/pm-need`。

### Step 2: 框架推荐

按场景推荐单一框架（详见 references/priority-frameworks.md）：

| 场景 | 推荐框架 | 理由 |
|---|---|---|
| 排客户问题/机会 | **Opportunity Score** | 优先问题非方案，Importance×(1−Satisfaction) |
| 排创意/倡议（含风险与经济） | **ICE** | Impact×Confidence×Ease，兼顾风险与成本 |
| 大团队需更细粒度 | **RICE** | 把 ICE 的 Impact 拆为 Reach×Impact |
| 需求必须有/应有/想有/不会有 | **MoSCoW** | 定性分类，发布范围划定 |
| 功能满意度分类（基本/性能/兴奋） | **Kano** | 客户期待类型分析 |
| 敏捷迭代带成本-of-delay | **WSJF** | (用户价值+时间价值+风险降低)/作业量 |

`--auto` 模式默认 Opportunity Score（排机会）。用户可 `--rice` 等显式指定。

### Step 3: 单框架评分

按推荐框架评分，每维度追溯到 PMContext：

**Opportunity Score**（默认）：
| 机会 | Importance | Satisfaction | Score | 来源 |
|---|---|---|---|---|
| <机会> | 0-1 | 0-1 | I×(1−S) | PMContext <项> |

**RICE**：
| 项 | Reach | Impact | Confidence | Effort | Score=(R×I×C)/E | 来源 |

**ICE**：Impact×Confidence×Ease

**MoSCoW**：Must/Should/Could/Won't 分类 + 理由

**Kano**：基本/性能/兴奋分类 + 满意度曲线

**WSJF**：(用户价值+时间价值+风险降低)/作业量

### Step 4: 四象限可视化

用 Mermaid 或表可视化：

```mermaid
quadrantChart
    title Importance vs Satisfaction
    x-axis 低满足 --> 高满足
    y-axis 低重要 --> 高重要
    quadrant-1 甜点区（高重要低满足）
    quadrant-2 维持区
    quadrant-3 次要区
    quadrant-4 过度满足区
    <机会1>: [0.2, 0.9]
    <机会2>: [0.1, 0.95]
```

### Step 5: 排序与标注

按总分排序，标 P0（Top 20%）/P1（中 50%）/P2（末 30%）。

### Step 6: 写入产物

写入 `docs/pm-context/prioritize.md`，含待排序项 + 框架选择理由 + 评分表 + 四象限 + 排序结果 + 追溯列。

**🔴 CHECKPOINT** — 输出产物路径 + 框架 + 待排序项数 + P0 数 + `[假设]` 项数。等待 PM 确认或自动进入下一步（`--auto` 模式）。

## 流程链落盘

步骤 2 产出完成后，写入中间工件：
- `docs/pm-context/.loop/prioritize-step2.md`（评分+四象限+排序 + 审计三元组）

## 关联增强

在"来源"列标注每评分追溯到的 PMContext 项。与 pm-ost 交叉验证（OST 的 Opportunity Score 应与本 skill 一致，不一致标冲突）。与 pm-experiment 衔接（P0 机会 → experiment 的高影响假设）。

## 失败模式

| 触发条件 | 一线修复 | 仍失败兜底 |
|---------|---------|-----------|
| `docs/pm-context/pm-context.md` 不存在 | **🔴 STOP**：输出"未找到 PMContext，先运行 `/pm-need <需求>`" | 不阻塞，提示后退出 |
| 待排序项是功能而非机会 | 回溯"这功能解决哪个机会"，排机会 | 无法回溯则提示先 /pm-ost 生成机会 |
| 评分维度无 PMContext 依据 | 标 `[假设]` 并汇总假设数 | 假设占比 >40% 提示数据不足 |
| 同时套多个框架混算 | 退回单框架，混算结果作废 | 不混算，框架间结果可对比但分开评分 |
| 框架选错场景（排机会用 WSJF） | 提示 WSJF 适用敏捷迭代，改推 Opportunity Score | 用户坚持则按用户选但标注场景不匹配 |
| 与 pm-ost Opportunity Score 冲突 | 标 `[冲突]` 让 PM 裁决 | 不静默合并 |
| 四象限数据点过少（<3） | 提示待排序项不足 | 不强行画图，改用纯排序表 |

## 不要做什么（反例黑名单）

| 反模式 | 为什么不要做 |
|--------|------------|
| 让客户排功能（解决方案） | 让客户设计解决方案是失败最快路径，排机会不排功能 |
| 评分无 PMContext 依据拍脑袋 | 无依据的分数是数字游戏，必须追溯或标 `[假设]` |
| 同时套多个框架混算 | 多变量同时变无法归因，单框架评分框架间可对比但分开 |
| 框架选错场景（排机会用 WSJF） | 框架有适用场景，乱套等于没用，按场景推荐 |
| 跳过四象限只给排序 | 四象限揭示"甜点区"，纯排序丢失 Importance× Satisfaction 二维信息 |
| P0/P1/P2 不基于分数凭感觉 | 必须按分数 Top20/中50/末30，凭感觉等于没排 |
| Opportunity Score 不与 pm-ost 交叉验证 | 两处 Score 不一致是信号，必须标冲突让 PM 裁决 |
| 审计三元组转换操作写"基于上述依据产出" | 空话，未阐明具体推导逻辑，判定为 Failure（ADR 0008 §11） |

## 产出示例

会员机会优先级片段：

```markdown
## 框架：Opportunity Score（排客户问题/机会）

| 机会 | Importance | Satisfaction | Score | 优先级 | 来源 |
|---|---|---|---|---|---|
| 续费流程太麻烦 | 0.95 | 0.1 | 0.855 | P0 | PMContext 摩擦力 |
| 忘记会员到期日 | 0.9 | 0.2 | 0.72 | P0 | PMContext 摩擦力 |
| 权益价值不清 | 0.7 | 0.4 | 0.42 | P1 | PMContext [假设] |

## 四象限
甜点区（高重要低满足）：续费太麻烦、忘记到期日 → P0
过度满足区：权益价值不清（重要性中低，可降级）
```

### Further Reading

- [Prioritization Frameworks Reference](https://www.productcompass.pm/p/prioritization-frameworks)
- [Opportunity Score (Dan Olsen, Lean Product Playbook)](https://www.productcompass.pm/p/opportunity-score)
- [WSJF for Agile Teams](https://www.productcompass.pm/p/wsjf)

6 框架完整公式、when-to-use、模板详见 [references/priority-frameworks.md](references/priority-frameworks.md)。

### 实战提示

- **排机会不排功能**：让客户排功能等于交出决策权，先排机会再选方案
- **单框架评分**：轮内只改一个维度，框架间可对比但分开算
- **追溯优先于数字**：没依据的分数标 `[假设]`，不靠数字补数据
- **四象限揭示甜点区**：纯排序丢失二维信息，甜点区是高重要低满足
- **与 ost 交叉验证**：两处 Opportunity Score 不一致必须标冲突
