---
name: pm-triage
description: Use when the user asks to triage issues or break plan into issues, mentions 分流、triage、issue 分流、问题分流、状态机、needs-triage、ready-for-agent、tracer bullet、垂直切片、vertical slice、拆 issue、break into issues、agent brief、 wontfix.
metadata:
  internal: true
---

# /pm-triage

> 你是一位分流调度员，正把需求/缺陷/PR 分流过状态机并拆成可抓取的 issue。**水平切片（只切一层）是 issue 拆分最大坑——必须垂直切片，每个 issue 端到端穿所有集成层。**

从 PMContext + 产物输出分流 + 垂直切片 issue + agent brief。

## Purpose

从 PMContext 与产物输出分流与 issue 拆分。提炼 skills 项目 triage + to-issues 的状态机与 tracer-bullet 方法，绑定 PMSkill 的 PMContext。目标：每个 issue 独立可抓取、端到端可验证、agent-ready。

## Context

PMContext + 产物（pm-prd/pm-stories/pm-release）是分流素材。本 skill 把这些产物拆成 issue tracker 上的独立 issue。分流是 PM Thinking Loop 的交付调度步骤。

## Instructions

- [ ] PMContext 已读取（不存在则 STOP 提示运行 /pm-need）
- [ ] 分流素材已收集（pm-stories 用户故事 / pm-release WWA / PM 提供的缺陷清单）
- [ ] 每项已分类（bug/enhancement）
- [ ] 每项已分状态（needs-triage/needs-info/ready-for-agent/ready-for-human/wontfix）
- [ ] 状态冲突已标并问 PM（一 issue 仅一 category + 一 state）
- [ ] 需拆分项已用垂直切片拆 tracer-bullet issue
- [ ] 每 issue 端到端穿所有集成层（非水平单层）
- [ ] ready-for-agent issue 已附 agent brief
- [ ] 每 issue 追溯到 PMContext/故事
- [ ] 产物落盘到 `docs/pm-context/triage.md`

## Thinking Protocol

本 Skill 承载 PM Thinking Loop 的交付调度步骤：

| 步骤 | 本 Skill 的职责 | 产出（是否回灌 PMContext） |
|------|---------------|--------------------------|
| 调度 | 分类+状态分流+垂直切片+agent brief | 不回灌（产出交付调度件） |

执行时必须依次完成上述步骤，不可跳步。步骤产出写入 `process/triage-dispatch.md`。

**产出约束**：
- 每 issue 仅一 category + 一 state，冲突标 `[状态冲突]` 问 PM
- 垂直切片必须端到端穿所有集成层（DB/API/UI/测试），水平切片（只切 UI 或只切 DB）作废重拆
- agent brief 必须自包含（agent 无需再问即可开工），含上下文/验收/边界
- wontfix 必须给理由，禁无理由关闭

**依赖检查**：每 issue 一 category 一 state？垂直切片端到端？brief 自包含？wontfix 有理由？

**Pre-flight Verification**（确定性审计，替代循环重试——AI 单次生成无法真循环）：依赖检查失败时，**不重试**，直接在产物顶部输出 Pre-flight 验证清单（标记每项 ✓/✗），✗ 项标 `[待确认]` + 信息缺口记录断链点 + 终止当前 Skill 并告知用户

### Step 1: 读取分流素材

读取：
- `docs/pm-context/pm-context.md`（需求背景）
- `docs/pm-context/stories.md`（用户故事，enhancement 来源）
- `docs/pm-context/release.md`（WWA backlog，issue 来源）
- PM 提供的缺陷清单/PR（bug 来源）

若 PMContext 不存在 → **🔴 STOP**：提示先运行 `/pm-need`。

### Step 2: 分类与状态分流

对每项分流：

| 项 | Category | State | 理由 | 来源 |
|---|---|---|---|---|
| 一键续费 | enhancement | ready-for-agent | 已有 WWA+验收 | release WWA-001 |
| 到期提醒不触发 | bug | needs-info | 复现条件不全 | PM 缺陷清单 |
| 多平台同步 | enhancement | needs-triage | 未在 PMContext，需评估 | PM 新提 |

**Category**：bug（坏了）/enhancement（新功能或改进）
**State**：
- needs-triage：需维护者评估
- needs-info：等上报者补信息
- ready-for-agent：完全规约化，agent 可直接做
- ready-for-human：需人实现
- wontfix：不做（必须给理由）

每项仅一 category + 一 state，冲突标 `[状态冲突]` 问 PM 后再分流。

### Step 3: 垂直切片拆 tracer-bullet issue

对 ready-for-agent/ready-for-human 的项，拆 tracer-bullet issue：

**垂直切片原则**（每 issue 端到端穿所有集成层）：
- ✓ 好：一键续费 = DB 字段 + API 端点 + UI 按钮 + 集成测试（穿 4 层）
- ✗ 坏：先做 DB 字段、再做 API、再做 UI（水平切片，3 issue 各只切一层）

每 issue：
```markdown
### ISSUE-001: 一键续费垂直切片
- **端到端路径**: DB(payment_token) → API(/renew-one-click) → UI(续费页按钮) → 集成测试
- **验收**: [ ]3秒完成 [ ]无需重填 [ ]失败有提示 [ ]权益正确更新
- **追溯**: release WWA-001 / PMContext 摩擦力
- **切片自检**: 端到端穿所有层✓ 独立可交付✓ 可验证✓
```

水平切片检测：若某 issue 只动一层（只 DB 或只 UI）→ 作废重拆为垂直。

### Step 4: 写 agent brief

对 ready-for-agent issue 附自包含 brief：

| brief 要素 | 内容 |
|---|---|
| 上下文 | PMContext 相关段 + 故事 + WWA |
| 目标 | 做什么（一句） |
| 验收 | 可观测条件清单 |
| 边界 | 必须不违反的约束 |
| 入口 | 改哪个文件/模块 |
| 验证 | 怎么测（测试用例/断言） |

brief 必须自包含——agent 读完无需再问即可开工。

### Step 5: 写入产物

写入 `docs/pm-context/triage.md`，含分流表 + 垂直切片 issue + agent brief + 追溯列。

### Step 5.5: 分流就绪验证（evidence-before-assertions，借鉴 superpowers/verification-before-completion）

落盘"分流完成"结论前必须跑 Gate Function，无新鲜证据不得声称完成：

| 声称 | 必须的验证证据 | 不充分（不算证据） |
|------|--------------|------------------|
| "issue 全分流" | 分流表每项有 category+state 核对 | "都分了" |
| "brief 全自包含" | 每 brief 五要素核对（上下文/验收/边界/入口/验证） | "写完了" |
| "垂直切片端到端" | 每切片穿所有层核对（DB/API/UI） | "切了" |
| "wontfix 全有理由" | 每 wontfix 项理由非空核对 | "关了" |

**Iron Law**: NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE。验证不过标 `[待验证]` + 列缺口，不声称完成。

**🔴 CHECKPOINT** — 输出产物路径 + 分流项数 + ready-for-agent 数 + 垂直切片数 + 水平切片作废数 + wontfix 数 + **分流就绪验证结果（4 项全过/🟡 N 项待验证）**。等待 PM 确认或自动进入下一步（`--auto` 模式）。

## 流程链落盘

调度步骤产出完成后，写入中间工件：
- `docs/pm-context/process/triage-dispatch.md`（分流+切片+brief + 审计三元组）

## 关联增强

在"来源"列标注每 issue 追溯。与 pm-stories 衔接（enhancement 来源）。与 pm-release 衔接（WWA → issue）。与 pm-align 衔接（bug issue 验证方式 ← align gap 验证）。

## 失败模式

| 触发条件 | 一线修复 | 仍失败兜底 |
|---------|---------|-----------|
| **🔴 STOP**：`docs/pm-context/pm-context.md` 不存在 | 提示先运行 `/pm-need <需求>` | 不阻塞，提示后退出 |
| **🔴 STOP**：无 stories 也无 release 也无缺陷清单 | 提示先运行 `/pm-stories` 或 `/pm-release` | 无素材无法分流 |
| 一项多 category 或多 state | 标 `[状态冲突]` 问 PM | 不静默选一个 |
| issue 水平切片（只动一层） | 作废重拆为垂直端到端 | 无法端到端则标 `[需评估切片]` |
| brief 不自包含（agent 还需问） | 补上下文/验收/边界/入口/验证 | 仍不自包含标 `[brief待补]` |
| wontfix 无理由 | 补理由（超范围/低价值/重复） | 无理由不关，标 `[待确认]` |
| needs-info 复现条件不全 | 列出缺哪些信息问上报者 | 不臆造条件强行分流 |
| 声称"分流完成"未跑 Gate Function（违反 verification Iron Law） | NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE——必须跑 Step 5.5 四项核对 | 标 `[待验证]` 不声称完成 |

## 不要做什么（反例黑名单）

| 反模式 | 为什么不要做 |
|--------|------------|
| 水平切片（只切 DB/API/UI 一层） | 端到端不可验证，必须垂直穿所有层 |
| 一项多 category 多 state | 状态机冲突，仅一 category 一 state |
| brief 不自包含 | agent 还需问等于没写，必须自包含 |
| wontfix 无理由 | 无理由关闭是黑箱，必须给理由 |
| needs-info 不列缺哪些信息 | 不列等于让上报者猜，必须明确缺什么 |
| ready-for-agent 无验收 | agent 不知何时完成，必须有可观测验收 |
| issue 不追溯 PMContext/故事 | 无追溯的 issue 脱离需求，变凭空任务 |
| 把 bug 当 enhancement 凑数 | bug 是坏了必须修，enhancement 是改进，不可混 |
| 审计三元组转换操作写"将 A 转换为 A'" | 同义反复，判定为 Failure |

## 产出示例 · 实战提示

会员分流片段：

```markdown
## 分流
| 项 | Category | State | 来源 |
|---|---|---|---|
| 一键续费 | enhancement | ready-for-agent | release WWA-001 |
| 到期提醒不触发 | bug | needs-info | PM 缺陷清单 |
| 多平台同步 | enhancement | wontfix（超范围，PMContext 无） | PM 新提 |

## ISSUE-001: 一键续费垂直切片
- 端到端: DB(payment_token) → API(/renew-one-click) → UI(按钮) → 集成测试
- 验收: [ ]3秒 [ ]无需重填 [ ]失败有提示 [ ]权益更新
- 切片自检: 端到端✓ 独立✓ 可验证✓

## agent brief
- 上下文: PMContext 摩擦力"续费太麻烦" + WWA-001
- 入口: src/renew.js, src/pay.js
- 验证: 构造一键续费用例，断言3秒完成+权益更新
```

**实战铁律**（落盘前对照）：

- **垂直切片是底线**：水平切片端到端不可验证，必须穿所有集成层
- **一 issue 一 category 一 state**：状态机冲突必须问 PM，不静默选
- **brief 必须自包含**：agent 读完无需再问才算 ready
- **wontfix 必须给理由**：无理由关闭是黑箱
- **needs-info 列缺什么**：让上报者猜等于不沟通
- **bug 与 enhancement 不可混**：bug 是坏了必修，enhancement 是改进

### Further Reading

- [Tracer Bullet Vertical Slices](https://www.productcompass.pm/p/tracer-bullet)
- [Triage State Machine](https://www.productcompass.pm/p/triage-state-machine)
- [Writing Agent-Ready Briefs](https://www.productcompass.pm/p/agent-brief)
