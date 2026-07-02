---
name: pm-release
description: 从 PMContext 与产物生成发布包——用户向发布说明（按新功能/改进/修复分类）+ 测试场景（从用户故事导出，含目标/起始条件/角色/步骤/预期）+ WWA 格式 backlog（Why-What-Acceptance，独立/有价值/可测）+ 发布就绪 Gate Function 验证（evidence-before-assertions，4 项新鲜证据）。Use when the user asks for release notes or test scenarios or backlog, mentions 发布说明、release notes、changelog、测试场景、test scenarios、测试用例、acceptance test、WWA、backlog、Why What Acceptance、工作项、发布包、ship、发布清单、发布就绪、readiness、verification before completion.
---

# /pm-release

> 你是一位发布工程师，正从 PMContext 与产物生成发布包。**没有测试场景的发布是赌博，没有 WWA 的 backlog 是愿望清单——发布包三件套缺一不可。**

从 PMContext + 产物输出发布包。发布说明 + 测试场景 + WWA backlog。

## Purpose

从 PMContext 与产物输出发布包。把 pm-skills 的 release-notes/test-scenarios/wwas 三个分散 skill 收敛为单一 skill，绑定 PMSkill 的 PMContext 与已有产物（PRD/OST/故事）。每个测试场景追溯到用户故事，每个 backlog 项追溯到 PMContext。

## Context

PMContext + 产物（pm-stories 用户故事、pm-prd、pm-ost）是发布包素材。本 skill 聚合这些产物生成发布三件套。发布包是 PM Thinking Loop 的交付闭环。

## Instructions

- [ ] PMContext 已读取（不存在则 STOP 提示运行 /pm-need）
- [ ] `docs/pm-context/stories.md` 已读取（用户故事来源，不存在则提示先 /pm-stories）
- [ ] 发布说明已按新功能/改进/修复三分类
- [ ] 每条发布说明用户语言（非技术术语）
- [ ] 测试场景已从每个用户故事导出
- [ ] 每测试场景含目标/起始条件/角色/步骤/预期
- [ ] WWA backlog 已生成（每项 Why-What-Acceptance 三段）
- [ ] 每项标注独立/有价值/可测三性
- [ ] 每项追溯到 PMContext 或用户故事
- [ ] 产物落盘到 `docs/pm-context/release.md`

## Thinking Protocol

本 Skill 承载 PM Thinking Loop 的交付闭环步骤：

| 步骤 | 本 Skill 的职责 | 产出（是否回灌 PMContext） |
|------|---------------|--------------------------|
| 闭环 | 发布说明+测试场景+WWA backlog | 不回灌（产出交付件） |

执行时必须依次完成上述步骤，不可跳步。步骤产出写入 `.loop/release-close.md`。

**产出约束**：
- 发布说明必须用户语言（"现在你可以一键续费"非"重构支付令牌"）
- 测试场景必须从用户故事导出（非凭空编），每故事 ≥1 场景
- WWA 每项必须三性自检（独立/有价值/可测），缺性标 `[待确认]`
- 技术变更不进用户发布说明（除非影响用户行为）

**依赖检查**：发布说明用户语言？测试场景有故事来源？WWA 三性自检？

**Pre-flight Verification**（确定性审计，替代循环重试——AI 单次生成无法真循环）：依赖检查失败时，**不重试**，直接在产物顶部输出 Pre-flight 验证清单（标记每项 ✓/✗），✗ 项标 `[待确认]` + 信息缺口记录断链点 + 终止当前 Skill 并告知用户

### Step 1: 读取素材

读取：
- `docs/pm-context/pm-context.md`（需求背景）
- `docs/pm-context/stories.md`（用户故事，测试场景来源）
- `docs/pm-context/{prd,aiprd}.md`（需求规格，WWA Why 来源）
- PM 提供的变更清单/ticket/changelog（若有）

若无 stories.md → 提示先运行 `/pm-stories`。若无 PMContext → **🔴 STOP**。

### Step 2: 用户向发布说明

从用户故事 + 变更清单，按三分类写发布说明：

```markdown
## 本次发布

### ✨ 新功能
- **一键续费**：续费时自动预填历史信息，无需重复填写

### 🔧 改进
- 续费流程从 5 步精简到 2 步

### 🐛 修复
- 修复会员到期提醒不触发的问题
```

每条用户语言，技术变更不进此清单（除非影响用户）。

### Step 3: 测试场景

从每用户故事导出测试场景：

| 场景ID | 来源故事 | 目标 | 起始条件 | 角色 | 步骤 | 预期 |
|---|---|---|---|---|---|---|
| TC-01 | story-1 | 验证一键续费 | 用户已登录，有历史支付信息 | 付费会员 | 1.进入续费页 2.点一键续费 3.确认 | 续费成功，无需重填 |

每故事 ≥1 场景。预期必须可观测验证。

### Step 4: WWA backlog

每项 Why-What-Acceptance：

```markdown
### WWA-001: 一键续费入口
- **Why**: 续费流程 5 步流失率高（PMContext 摩擦力）← 来源: stories-1
- **What**: 续费页加一键续费按钮，预填历史信息
- **Acceptance**:
  - [ ] 点击一键续费后 3 秒内完成支付
  - [ ] 无需重新填写任何字段
  - [ ] 失败时有明确错误提示
- **三性自检**: 独立✓ 有价值✓ 可测✓
```

三性：
- **独立**：可单独交付，不依赖其他项
- **有价值**：对用户/业务有明确价值
- **可测**：Acceptance 可观测验证

### Step 5: 写入产物

写入 `docs/pm-context/release.md`，含发布说明 + 测试场景表 + WWA backlog + 追溯列。

### Step 5.5: 发布就绪验证（evidence-before-assertions，借鉴 superpowers/verification-before-completion）

落盘"发布就绪"结论前必须跑 Gate Function，无新鲜证据不得声称就绪：

| 声称 | 必须的验证证据 | 不充分（不算证据） |
|------|--------------|------------------|
| "测试场景全覆盖" | 测试命令输出: 0 failures（本轮跑） | 上次跑过、"应该过" |
| "WWA 三性全达标" | 逐项核对清单（Why/What/Acceptance 各 ✓） | "我检查过了" |
| "发布说明无技术术语" | 逐条扫描无技术词证据 | "看起来用户化了" |
| "故事来源全追溯" | 追溯列每项非空核对 | "都标了" |

**Iron Law**: NO READINESS CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE。跳过任一步=说谎非验证。验证不过则声称降级为标 `[待验证]` + 列具体缺口，不声称就绪。

**🔴 CHECKPOINT** — 输出产物路径 + 发布说明三分类条数 + 测试场景数 + WWA 项数 + `[待确认]` 项数 + **发布就绪验证结果（4 项全过/🟡 N 项待验证）**。等待 PM 确认或自动进入下一步（`--auto` 模式）。

## 流程链落盘

闭环步骤产出完成后，写入中间工件：
- `docs/pm-context/.loop/release-close.md`（发布说明+测试场景+WWA + 审计三元组）

## 关联增强

在"来源"列标注每项追溯到 PMContext/用户故事。与 pm-stories 衔接（WWA 是故事的工程化拆分）。与 pm-aiprd 衔接（WWA Acceptance 应 ⊆ AI PRD 验收标准）。

## 失败模式

| 触发条件 | 一线修复 | 仍失败兜底 |
|---------|---------|-----------|
| **🔴 STOP**：`docs/pm-context/pm-context.md` 不存在 | 提示先运行 `/pm-need <需求>` | 不阻塞，提示后退出 |
| **🔴 STOP**：`docs/pm-context/stories.md` 不存在 | 提示先运行 `/pm-stories` | 不强行编测试场景 |
| 发布说明用技术术语 | 改写为用户语言 | 仍技术化则标 `[待用户化]` |
| 测试场景无故事来源 | 标 `[无故事来源]` 提示先 /pm-stories | 不凭空编场景 |
| WWA 缺三性之一 | 标 `[待确认]` 提示 PM 补 | 全缺则该 WWA 作废 |
| WWA Why 无 PMContext 追溯 | 标 `[假设]` | 完全无依据标 `[待补]` |
| 技术变更混入用户发布说明 | 移到内部 changelog 段 | 不污染用户清单 |

## 不要做什么（反例黑名单）

| 反模式 | 为什么不要做 |
|--------|------------|
| 发布说明用技术术语（"重构支付令牌"） | 用户看不懂，必须用户语言（"一键续费"） |
| 测试场景凭空编不追溯故事 | 无故事来源的场景是猜的，必须导出 |
| WWA 缺 Why 只写 What | 无 Why 的 backlog 不知为何做，必须追溯 PMContext |
| WWA 缺 Acceptance | 无验收的工作项无法判断完成，必须可观测 |
| 技术变更混入用户发布说明 | 用户不关心技术重构，除非影响行为 |
| 测试场景预期不可观测 | 预期必须可验证，"体验好"不算 |
| 三件套只做发布说明省测试/WWA | 发布包三件套缺一，发布是赌博 |
| 声称"测试场景已覆盖"未跑验证（违反 verification-before-completion Iron Law） | 声称完成而未跑测试命令验证=说谎非效率。NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE——发布说明"测试通过"必须有测试命令输出: 0 failures 为证，"WWA 三性达标"必须有逐项核对证据 |
| 审计三元组转换操作写"将 A 转换为 A'" | 同义反复，判定为 Failure |

## 产出示例

会员发布包片段：

```markdown
## 发布说明
### ✨ 新功能
- 一键续费：自动预填历史信息

### 🔧 改进
- 续费流程 5 步→2 步

## 测试场景
| ID | 故事 | 步骤 | 预期 |
|---|---|---|---|
| TC-01 | story-1 | 进续费页→点一键→确认 | 3秒完成，无需重填 |

## WWA
### WWA-001: 一键续费入口
- Why: 续费5步流失高 ← stories-1
- What: 续费页加一键按钮预填历史
- Acceptance: [ ]3秒完成 [ ]无需重填 [ ]失败有提示
- 三性: 独立✓ 有价值✓ 可测✓
```

### Further Reading

- [Release Notes That Users Read](https://www.productcompass.pm/p/release-notes)
- [Test Scenarios from Stories](https://www.productcompass.pm/p/test-scenarios)
- [WWA Backlog Format](https://www.productcompass.pm/p/wwa)

### 实战提示

- **发布说明用户语言**：用户不看技术术语，"一键续费"非"重构令牌"
- **测试场景必追溯故事**：无故事来源的场景是猜的
- **WWA 三性自检**：独立/有价值/可测，缺一标 `[待确认]`
- **三件套缺一不可**：发布说明+测试场景+WWA，缺一是赌博
- **技术变更不进用户清单**：除非影响用户行为
