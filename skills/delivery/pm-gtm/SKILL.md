---
name: pm-gtm
description: 从 PMContext 生成 GTM（走向市场）策略——Beachhead 首攻细分选择（四准则评分）+ ICP 画像 + 渠道矩阵 + 信息阶梯 messaging + 发布时间线 + 增长循环五型设计（Viral/Usage/Collaboration/UGC/Referral）+ 成功度量。Use when the user asks for go-to-market or launch strategy, mentions GTM、走向市场、beachhead、go-to-market.
---

# /pm-gtm

> 你是一位 GTM 策略师，正从 PMContext 构建 Go-to-Market 计划。**没有 Beachhead 的 GTM 是撒胡椒面——先选一个能赢的首攻细分，再谈扩张。**

从 PMContext 输出 GTM 策略。Beachhead 选择 + ICP 画像 + 渠道矩阵 + messaging + 发布时间线。

## Purpose

从 PMContext 输出 GTM 策略。把 pm-skills 的 gtm-strategy/beachhead-segment/ideal-customer-profile 三个分散 skill 收敛为单一 skill，按"选细分→画像→渠道→信息→时间线"五步递进。每个选择追溯到 PMContext，杜绝凭空 GTM。

## Context

PMContext 中有用户场景、竞品/市场、价值验证度量、边界条件。本 skill 提取这些信息构建 GTM。GTM 是 PMContext 的下游 View，和 PRD/OST 平级，用于发布评审与渠道决策。

## Instructions

- [ ] PMContext 已读取且非空（不存在则 STOP 提示运行 /pm-need）
- [ ] "用户场景"已提取（ICP 行为/JTBD 来源）
- [ ] "竞品/市场"已提取（Beachhead 可赢性来源）
- [ ] "价值验证度量"已提取（GTM 成功度量来源）
- [ ] "边界条件"已提取（渠道约束/预算来源）
- [ ] Beachhead 已用四准则评分选定 1 个首攻细分
- [ ] ICP 画像含 demographics/behaviors/JTBD/needs 四维
- [ ] 渠道矩阵含 ≥5 渠道 + 触达/成本/转化评估
- [ ] messaging 用信息阶梯（Feature→Benefit→Value→Identity）
- [ ] 发布时间线含 3 阶段（预热/发布/发布后）+ 每阶段度量
- [ ] 每项在"来源"列标注追溯到的 PMContext 项
- [ ] 产物落盘到 `docs/pm-context/gtm.md`

## Thinking Protocol

本 Skill 承载 PM Thinking Loop 的步骤 2-3（建模/方案）的 GTM 部分：

| 步骤 | 本 Skill 的职责 | 产出（是否回灌 PMContext） |
|------|---------------|--------------------------|
| 2. 建模 | Beachhead 选择 + ICP 画像 | 不回灌（产出 View） |
| 3. 方案 | 渠道矩阵 + messaging + 时间线 | 不回灌（产出 View） |

执行时必须依次完成上述步骤，不可跳步。步骤产出写入 `.loop/gtm-step2.md`、`.loop/gtm-step3.md`。

**产出约束**：
- Beachhead 必须是单一细分（非"中小企业"等宽泛表述），用四准则评分选定
- 渠道必须按"触达/成本/转化"三维评估，禁只列渠道名
- messaging 必须用信息阶梯四层，禁只写一句 slogan
- 时间线每阶段必须有度量阈值，禁只写日期

**依赖检查**：Beachhead 是否单一具体？渠道是否有三维评估？messaging 是否四层？时间线是否有度量？

**Pre-flight Verification**（确定性审计，替代循环重试——AI 单次生成无法真循环）：依赖检查失败时，**不重试**，直接在产物顶部输出 Pre-flight 验证清单（标记每项 ✓/✗），✗ 项标 `[待确认]` + 信息缺口记录断链点 + 终止当前 Skill 并告知用户

### Step 1: 读取 PMContext 提取 GTM 素材

读取 `docs/pm-context/pm-context.md`，提取：
- "用户场景" → ICP demographics/behaviors/JTBD
- "竞品/市场" → Beachhead 可赢性、渠道空白
- "价值验证度量" → GTM 成功度量
- "边界条件" → 渠道约束、预算、合规

若 PMContext 不存在 → **🔴 STOP**：提示先运行 `/pm-need`。

### Step 2: Beachhead 首攻细分选择

从 PMContext 用户场景枚举 2-4 个候选细分，用四准则评分（每项 0-1，归一化）：

| 准则 | 权重 | 候选A | 候选B | 候选C |
|---|---|---|---|---|
| 痛点烈度（Burning Pain） | 0.3 | | | |
| 付费意愿（Willingness to Pay） | 0.25 | | | |
| 可赢市场份额（Winnable，3-18 月 60-70%） | 0.25 | | | |
| 推荐潜力（Referral，可触达相邻市场） | 0.2 | | | |
| **加权总分** | | | | |

选定 Top 1 作为 Beachhead，标注放弃候选的理由。

### Step 3: ICP 理想客户画像

对 Beachhead 细分画 ICP 四维：
- **Demographics**：公司规模/行业/地域/职位 ← PMContext 用户场景
- **Behaviors**：发现/评估/决策方式、采纳速度、协作模式 ← PMContext 用户场景
- **JTBD**：待办任务（功能性+情感性+社会性）← PMContext 用户场景
- **Needs**：必须满足的需求 + 不能接受的 ← PMContext 摩擦力

### Step 4: 渠道矩阵

枚举 ≥5 渠道（数字/内容/销售/社区/产品内驱），三维评估：

| 渠道 | 触达 ICP 覆盖度 | 单获客成本（量级） | 预期转化率 | 优先级 |
|---|---|---|---|---|
| 付费搜索 | <高/中/低> | <量级> | <量级> | P0/P1/P2 |
| ... | | | | |

优先级 = 触达 × 转化 ÷ 成本。选 P0 渠道 2-3 个集中投入。

### Step 4.5: 创意营销 Idea 生成（借鉴 pm-marketing-growth/marketing-ideas）

传统渠道矩阵解决"在哪投"，创意营销 idea 解决"怎么投出彩"——为 Beachhead ICP 生成 3-5 个低成本高创意的营销 ideas，每 idea 含渠道 + 核心信息 + 为什么有效 + 性价比评估。

| # | 创意 Idea | 渠道 | 核心信息 | 为什么对 ICP 有效 | 性价比 |
|---|----------|------|---------|------------------|--------|
| 1 | <Idea 名称> | <发布渠道> | <一句话口号> | <基于 ICP 行为/JTBD 的推理> | ⭐⭐⭐ |
| 2 | ... | | | | |

**生成规则**：
- 从 PMContext 用户场景提取 ICP 的行为模式与触媒偏好（非臆造）
- 优先非常规/低成本渠道（社区/口碑/内容/合作/UGD），禁无脑投付费搜索
- 每 idea 必须标注"为什么对 ICP 有效"，基于 PMContext 的用户场景/JTBD
- ≥3 个（少于 3 个发散不足），≤5 个（多于 5 个不可聚焦）
- 不替代 Step 4 渠道矩阵——idea 是渠道矩阵的补充，增强 P0 渠道的具体打法

### Step 5: 信息阶梯 messaging

四层信息阶梯（自下而上）：
- **Identity**：成为什么样的人（"我们是 X 时代的 Y")
- **Value**：核心价值主张 ← PMContext 价值验证度量
- **Benefit**：具体收益（用户语言）
- **Feature**：支撑功能（最底层，不单独宣传）

### Step 6: 发布时间线

三阶段，每阶段含动作 + 度量阈值：

| 阶段 | 时间窗 | 关键动作 | 度量阈值 |
|---|---|---|---|
| 预热（Pre-launch） | T-4~T-1 周 | 候选名单/waitlist/种子用户 | waitlist ≥ N |
| 发布（Launch） | T~T+2 周 | P0 渠道全开、ICP 定向 | 首周激活率 ≥ X% |
| 发布后（Post-launch） | T+3~T+12 周 | 留存优化、相邻细分扩张 | 4 周留存 ≥ Y% |

### Step 6.5: 增长循环设计（Growth Loops）

发布时间线解决"冷启动"，增长循环解决"可持续"。从 PMContext 用户场景与 Beachhead ICP 推导最适配的 1-2 个增长循环，减少对付费获客的依赖。

**五型增长循环**（借鉴 pm-skills/growth-loops）：

| 循环类型 | 机制 | 适用条件 | 关键挑战 | PMContext 推导依据 |
|---------|------|---------|---------|------------------|
| **Viral（病毒式）** | 用户在产品内创建内容 → 分享到外部平台 → 新用户发现并注册 | 产品输出天然可分享（设计/视频/文档） | 需高度可分享内容 + 分享激励 | 用户场景是否含"创作并分享"行为 |
| **Usage（使用式）** | 用户创建内容/价值 → 分享 → 他人消费 → 成为活跃用户 | 产品输出是消费型内容（文章/模板/thread） | 内容创作摩擦须极低 | 用户场景是否含"生产-消费"闭环 |
| **Collaboration（协作式）** | 用户邀请同事共创 → 同事发现产品价值 | 协作型产品（文档/设计/项目管理） | 需团队协作场景 | 用户场景是否含"多人协作" |
| **UGC（用户生成）** | 用户发现他人内容 → 创建类似内容 → 分享 → 他人发现 | 内容平台型（TikTok/Pinterest/YouTube） | 需高质量内容临界规模 | 用户场景是否含"内容发现-模仿-创作" |
| **Referral（推荐式）** | 用户推荐 → 被推荐者加入 → 推荐者获奖励 → 更多推荐 | 适合大多数产品（Dropbox/Uber/PayPal） | 奖励设计需平衡成本与激励 | 边界条件中的获客成本预算 |

**选择规则**：
- 从 PMContext 用户场景提取核心行为模式，匹配上表"适用条件"
- 首选 1 个主循环（最适配）+ 1 个辅循环（补充），禁撒胡椒面选 3+ 个
- 每循环必须画出闭环图：`新用户 → 价值体验 → 创建/分享/邀请 → 新用户`，标注每环节的度量阈值

**循环闭环图模板**：
```
新用户激活 → [核心行为: <PMContext 用户场景>]
    → [产出: <可分享内容/邀请链接/协作项目>]
    → [分发: <外部平台/私信/团队渠道>]
    → [新用户发现 → 激活] （闭环）
度量：K 因子 = 每用户平均带来新用户数（K>1 自增长）
```

**失败模式（增长循环特有）**：

| 触发条件 | 一线修复 | 仍失败兜底 |
|---------|---------|-----------|
| PMContext 用户场景无法匹配任何循环类型 | 标 `[待确认]` 需补用户行为数据 | 默认选 Referral（最通用）并标 `[假设]` |
| 选了 3+ 个循环 | 收敛到 1 主 + 1 辅，标注放弃理由 | 不撒胡椒面 |
| 循环闭环图某环节无度量阈值 | 从 PMContext 价值验证度量提取 | 无依据则标 `[待确认]` |
| K 因子 < 1（无法自增长） | 标 🟡 需配合付费获客，不抛弃循环 | 标注"循环+付费"混合策略 |

**反例**：把"做增长"等同于"投广告"——没有增长循环的 GTM 永远依赖付费获客，CAC 随竞争上涨不可持续。

### Step 7: 写入产物

写入 `docs/pm-context/gtm.md`，含 Beachhead 评分表 + ICP 画像 + 渠道矩阵 + 信息阶梯 + 时间线 + 追溯列。

**🔴 CHECKPOINT** — 输出产物路径 + Beachhead 选定细分 + P0 渠道数 + 时间线阶段数 + `[假设]` 项数。等待 PM 确认或自动进入下一步（`--auto` 模式）。

## 流程链落盘

步骤 2-3 产出完成后，写入中间工件：
- `docs/pm-context/.loop/gtm-step2.md`（Beachhead+ICP + 审计三元组）
- `docs/pm-context/.loop/gtm-step3.md`（渠道+messaging+时间线 + 审计三元组）

## 关联增强

在"来源"列标注每项追溯到的 PMContext 项。无来源的标 `[假设]`。Beachhead 与 pm-strategy 的 Ansoff 推荐路径交叉验证（Beachhead 应在推荐象限内）。

## 失败模式

| 触发条件 | 一线修复 | 仍失败兜底 |
|---------|---------|-----------|
| `docs/pm-context/pm-context.md` 不存在 | **🔴 STOP**：输出"未找到 PMContext，先运行 `/pm-need <需求>`" | 不阻塞，提示后退出 |
| PMContext "用户场景"为空，无法枚举细分 | **🔴 STOP**：输出"无用户场景，先运行 `/pm-collect` 补用户研究" | 不臆造细分 |
| Beachhead 候选 < 2 个 | 放宽细分粒度重新枚举 | 仍不足则提示 PM 手动指定细分 |
| 渠道数据缺失无法三维评估 | 从 PMContext 边界条件推断成本量级 | 完全无依据则标 `[假设]` 只给优先级不给数字 |
| messaging 写成单句 slogan | 拆为信息阶梯四层 | 仍拆不出则标 `[待确认]` |
| 时间线无度量阈值 | 从 PMContext 价值验证度量提取 | 无依据则标 `[待确认]` 让 PM 定 |
| Beachhead 与 pm-strategy Ansoff 路径冲突 | 标 `[冲突]` 让 PM 裁决 | 不静默合并 |
| 增长循环无法从 PMContext 用户场景推导 | 默认选 Referral（最通用）并标 `[假设]` | 标 `[待确认]` 需补用户行为数据 |

## 不要做什么（反例黑名单）

| 反模式 | 为什么不要做 |
|--------|------------|
| Beachhead 选"中小企业"等宽泛表述 | 不宽泛不叫 Beachhead，必须是能 3-18 月赢 60-70% 的单一细分 |
| 渠道只列名不三维评估 | 没触达/成本/转化评估等于没选，撒胡椒面 |
| messaging 只写一句 slogan | 信息阶梯四层缺一不可，slogan 是 Identity 层不是全部 |
| 时间线只写日期无度量 | 没度量的时间线是日历不是 GTM 计划 |
| 跳过 Beachhead 直接铺渠道 | 没有 Beachhead 的 GTM 是撒胡椒面，先选能赢的细分 |
| ICP 只写 demographics | Behaviors/JTBD/Needs 缺一不可，demographics 只是画像一角 |
| 发布后阶段省略 | 发布后留存与扩张才是 GTM 真正考验，不能只到发布 |
| 选 3+ 个增长循环撒胡椒面 | 资源分散哪个都做不深，1 主 + 1 辅足够 |
| 把增长等同于投广告 | 没有增长循环的 GTM 永远依赖付费获客，CAC 随竞争上涨不可持续 |
| 审计三元组转换操作写"基于上述依据产出" | 空话，未阐明具体推导逻辑，判定为 Failure |

## 产出示例 · 实战提示

会员产品 GTM 片段：

```markdown
## Beachhead 选择
| 准则 | 权重 | 高频创作者 | 企业团队 | 一次性活动用户 |
|---|---|---|---|---|
| 痛点烈度 | 0.3 | 0.9 | 0.7 | 0.4 |
| 付费意愿 | 0.25 | 0.8 | 0.9 | 0.3 |
| 可赢份额 | 0.25 | 0.75 | 0.5 | 0.6 |
| 推荐潜力 | 0.2 | 0.85 | 0.6 | 0.5 |
| **总分** | | **0.83** | 0.69 | 0.44 |

选定：高频创作者。放弃企业团队（可赢份额低，竞争激烈）。

## ICP
- Demographics：个体/小工作室、内容创作行业、一二线、主理人
- Behaviors：工具切换频繁、社群决策、采纳快、单人决策
- JTBD：让创作产能稳定输出（功能）/ 创作焦虑降低（情感）/ 被同行认可专业（社会）
- Needs：必须稳定输出节奏；不能接受断更风险

## 渠道 P0
1. 创作者社群 KOC 合作（触达高/成本低/转化中）
2. 工具内嵌引导（触达高/成本极低/转化高）
```

**实战铁律**（落盘前对照）：

- **Beachhead 先于渠道**：没选首攻细分就铺渠道是 GTM 最大反模式
- **四准则必须评分**：拍脑袋选 Beachhead 等于没选，加权评分才有依据
- **渠道集中 P0**：P0 渠道 2-3 个集中投入，撒胡椒面哪个都做不深
- **信息阶梯自下而上构建自上而下宣传**：构建从 Feature 起，宣传从 Identity 起
- **发布后才是真考验**：留存与扩张度量不能省

### Further Reading

- [Beachhead Market Strategy (Play Bigger)](https://www.productcompass.pm/p/beachhead)
- [ICP Framework](https://www.productcompass.pm/p/icp)
- [Messaging Hierarchy: Information Stairs](https://www.productcompass.pm/p/messaging)
