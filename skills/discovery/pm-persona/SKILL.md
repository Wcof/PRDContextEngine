---
name: pm-persona
description: 从 PMContext 生成基于 JTBD 的用户画像——≥3 个 persona，每 persona 含 demographics+behaviors+JTBD（功能性/情感性/社会性）+未满足需求+代表性引言+反对意见，禁仅按 demographics 切片，每画像附 PMContext 追溯。Use when the user asks for persona or user profile, mentions 用户画像、persona、user profile、用户角色、JTBD persona、人物画像、目标用户、典型用户、user persona、customer persona.
---

# /pm-persona

> 你是一位用户研究员。摆在你面前的是 PMContext 的用户场景与反馈。你的任务是把分散的行为聚成 ≥3 个立体的 persona——他们是谁、做什么、为什么、想要什么、反对什么，而不是堆一张"25-34 岁男性白领"的 demographics 卡片。

从 PMContext 生成基于 JTBD 的用户画像。≥3 个 persona，每画像含五维 + 引言 + 反对意见。

## Purpose

把 PMContext 用户场景与反馈聚成立体 persona。pm-skills 的 user-personas/user-segmentation 收敛进 PMSkill 体系：从 PMContext 用户场景推导，每画像追溯 PMContext，与 pm-market 用户分层互补（分层看群体差异，persona 看个体立体）。

## Context

PMContext"用户场景"定义谁在什么场景下用什么达到什么目的；"现状平替与摩擦力"定义未满足需求；反馈数据（若有）提供代表性引言素材。本 skill 提取这些信息构建 persona。Persona 是 PMContext 的下游 View，与 pm-market 用户分层平级。

## Instructions

- [ ] PMContext 已读取且非空（不存在则 STOP 提示运行 /pm-need）
- [ ] "用户场景"已提取（persona 行为/JTBD 来源）
- [ ] "现状平替与摩擦力"已提取（未满足需求来源）
- [ ] "边界条件"已提取（反对意见/约束来源）
- [ ] ≥3 个 persona 已生成
- [ ] 每 persona 含五维：demographics/behaviors/JTBD（功能+情感+社会）/未满足需求/代表性引言
- [ ] 每 persona 含 ≥2 反对意见（为何不用我们的产品）
- [ ] persona 间互斥（不重叠）
- [ ] 每画像标注追溯到的 PMContext 项
- [ ] 产物落盘到 `docs/pm-context/personas.md`

## Thinking Protocol

本 Skill 承载 PM Thinking Loop 的步骤 2（建模）的 persona 构建部分：

| 步骤 | 本 Skill 的职责 | 产出（是否回灌 PMContext） |
|------|---------------|--------------------------|
| 2. 建模 | 从用户场景聚类成立体 persona | 不回灌（产出 View） |

执行时必须依次完成上述步骤，不可跳步。步骤产出写入 `.loop/persona-step2.md`。

**产出约束**：
- persona 必须 ≥3 个（少于 3 说明聚类粗糙），≤7 个（多于 7 无法聚焦）
- JTBD 必须含三性：功能性（做什么）+ 情感性（感受什么）+ 社会性（被如何看待）
- 代表性引言必须来自反馈数据或标 `[假设]`，禁编造
- persona 间必须互斥（同一用户不应属 2 个 persona）

**依赖检查**：persona 数是否 3-7？JTBD 是否三性齐全？引言是否有依据？persona 间是否互斥？

**Pre-flight Verification**（确定性审计，替代循环重试——AI 单次生成无法真循环）：依赖检查失败时，**不重试**，直接在产物顶部输出 Pre-flight 验证清单（标记每项 ✓/✗），✗ 项标 `[待确认]` + 信息缺口记录断链点 + 终止当前 Skill 并告知用户

### Step 1: 读取 PMContext 提取 persona 素材

读取 `docs/pm-context/pm-context.md`，提取：
- "用户场景" → persona 的 behaviors + JTBD
- "现状平替与摩擦力" → 未满足需求
- "边界条件" → 反对意见/约束
- 反馈数据（若有）→ 代表性引言素材

若 PMContext 不存在 → **🔴 STOP**：提示先运行 `/pm-need`。

### Step 2: 聚类成 ≥3 persona

按 behaviors + JTBD + 未满足需求 聚类（禁仅按 demographics），每 persona 命名（具体名字，非"用户A"）。

### Step 3: 每 persona 五维 + 引言 + 反对意见

```
## Persona: <具体名字>（如"独立创作者小林"）

### Demographics
- 身份/年龄/地域/职业 ← PMContext 用户场景

### Behaviors
- 如何使用产品/频率/深度/工具链 ← PMContext 用户场景

### JTBD
- 功能性：要完成什么任务
- 情感性：要感受什么（如"创作焦虑降低"）
- 社会性：要被如何看待（如"被同行认可专业"）

### 未满足需求
- 当前平替与最痛苦的摩擦力 ← PMContext 现状平替与摩擦力

### 代表性引言
- "<引言>" ← 来源: 反馈数据/`[假设]`

### 反对意见（为何不用我们）
- 反对1: <理由> ← PMContext 边界条件
- 反对2: <理由>
```

### Step 4: 互斥校验

| persona | 核心行为 | JTBD | 与其他 persona 重叠? |
|---------|---------|------|-------------------|
| 小林 | 独立创作 | 稳定输出 | 无 |
| 老王 | 团队协作 | 团队对齐 | 无 |
| ... | | | |

重叠 >20% → 重新聚类或合并。

### Step 5: 写入产物

写入 `docs/pm-context/personas.md`，含 ≥3 persona + 互斥校验表 + 追溯列。

**🔴 CHECKPOINT** — 输出产物路径 + persona 数 + 互斥校验结果。等待 PM 确认或自动进入下一步（`--auto` 模式）。

## 流程链落盘

步骤 2 产出完成后，写入中间工件：
- `docs/pm-context/.loop/persona-step2.md`（persona 聚类+五维 + 审计三元组）

## 关联增强

在追溯列标注每画像追溯到的 PMContext 项。persona 与 pm-market 用户分层互补（分层看群体差异，persona 看个体立体），与 pm-interview 联动（每 persona 可设计定向访谈）。

## 失败模式

| 触发条件 | 一线修复 | 仍失败兜底 |
|---------|---------|-----------|
| `docs/pm-context/pm-context.md` 不存在 | **🔴 STOP**：输出"未找到 PMContext，先运行 `/pm-need <需求>`" | 不阻塞，提示后退出 |
| PMContext "用户场景"为空 | **🔴 STOP**：输出"无用户场景，先运行 `/pm-collect` 补用户研究" | 不臆造 persona |
| 反馈数据不足以提取引言 | 标 `[假设]` 引言，提示补访谈 | 不编造引言 |
| persona 数 < 3 | 放宽聚类粒度重新分 | 仍不足则标 `[待确认]` 需补用户研究 |
| persona 间重叠 >20% | 重新选聚类维度或合并 | 标 `[冲突]` 让 PM 裁决 |
| JTBD 缺情感性/社会性 | 补充（问"用户感受什么/被怎么看"） | 标 `[待确认]` 该性缺失 |

## 不要做什么（反例黑名单）

| 反模式 | 为什么不要做 |
|--------|------------|
| 仅按 demographics 切片（25-34 岁男性） | demographics 不驱动产品策略，行为/JTBD 才驱动 |
| persona < 3 个 | 少于 3 说明聚类粗糙，漏关键用户群 |
| JTBD 只写功能性 | 情感与社会性是购买决策的关键，缺一不立体 |
| 代表性引言编造 | 没依据的引言是虚构，必须标 `[假设]` 或来自反馈 |
| persona 间不互斥 | 重叠 persona 说明聚类维度混淆，无法聚焦 |
| persona 命名"用户A/B" | 抽象命名无代入感，用具体名字"小林/老王" |
| 不追溯 PMContext | persona 悬空，无法验证是否对齐用户研究 |
| 审计三元组转换操作写"基于上述依据产出" | 空话，判定为 Failure |

## 产出示例 · 实战提示

会员产品 persona 片段：

```markdown
## Persona: 独立创作者小林

### Demographics
- 28 岁/一二线/自由职业内容创作者 ← PMContext 用户场景

### Behaviors
- 日更内容/工具切换频繁/社群决策/单人工作 ← PMContext 用户场景

### JTBD
- 功能性：让创作产能稳定输出
- 情感性：降低断更焦虑
- 社会性：被同行认可专业

### 未满足需求
- 当前用 Excel+日历手动排期，最痛苦的是断更无预警 ← PMContext 现状平替与摩擦力

### 代表性引言
- "我每天醒来第一件事是担心今天发什么" ← 来源: 反馈数据 review_001

### 反对意见
- 反对1: "我已经用 Excel 排期习惯了" ← PMContext 边界条件"迁移成本"
- 反对2: "月费 ¥30 对自由职业有压力" ← PMContext 边界条件"价格敏感"
```

详见 [references/persona-example.md](references/persona-example.md)（完整 3 persona 示例含互斥校验与访谈联动）。

**实战铁律**（落盘前对照）：

- **行为/JTBD 聚类非 demographics**：demographics 不驱动产品策略
- **≥3 persona**：少于 3 漏关键群，多于 7 无法聚焦
- **JTBD 三性齐全**：功能+情感+社会，缺一不立体
- **引言要有依据**：来自反馈或标 `[假设]`，禁编造
- **互斥是底线**：重叠 persona 说明维度混淆，重聚类
- **具体命名**：小林/老王 比 用户A/B 有代入感

### Further Reading

- [User Persona Best Practices](https://www.productcompass.pm/p/user-persona)
- [JTBD Framework](https://www.productcompass.pm/p/jtbd)
- [Persona vs Segment](https://www.productcompass.pm/p/persona-vs-segment)
