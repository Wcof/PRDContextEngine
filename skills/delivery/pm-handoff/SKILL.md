---
name: pm-handoff
description: 把当前 PMSkill 会话压缩成交接文档——PMContext 状态 + 已完成产物 + 未完成项 + 条件触发式下一步建议（触发条件+动作+前置检查，借鉴 condition-based-waiting）+ 关键决策 + 知识转移（决策非显性理由+可推翻条件+ZPD 能力差距，借鉴 teach）+ 9 项质量自检，供下一个 Agent 接续。Use when the user asks to handoff or continue in another session, mentions 交接、handoff、切换会话、continue later、session handoff、换 agent、接续工作、上下文压缩、compact session、知识转移、knowledge transfer、条件触发、condition-based trigger.
---

# /pm-handoff

> 你是一位项目经理，正在把当前 PMSkill 工作压缩成可接续的交接文档。**交接文档不是聊天记录摘要，是让接手者 30 秒内进入状态的最短路径。**

把当前会话压缩成交接文档。PMContext 状态 + 已完成产物 + 未完成项 + 下一步 + 关键决策。

## Purpose

把当前 PMSkill 会话压缩成交接文档。文档让下一个 Agent 无需回看对话历史即可接续。交接文档是 PMContext 的元数据 View，记录"做到哪了、还差什么、下一步"。

## Context

长会话或跨 Agent 协作时，完整对话历史无法传递。交接文档提取工作状态关键信息，让接手者快速进入。文档落盘后，新会话开头读交接文档即可恢复上下文。

## Instructions

- [ ] PMContext 已读取（若存在）并提取当前状态
- [ ] 当前会话已完成的 skill 调用和产物已盘点
- [ ] 未完成项已识别（停在哪个 skill 的哪一步）
- [ ] 关键决策已记录（做了什么决定、为什么）
- [ ] 信息缺口和 `[待确认]` 项已盘点
- [ ] 下一步建议已给出（具体到该调哪个 skill）
- [ ] 交接文档落盘到 `docs/pm-context/handoff.md`
- [ ] 文档自包含——接手者无需回看对话历史

## Thinking Protocol

本 Skill 承载 PM Thinking Loop 的步骤 6（交付）的交接部分：

| 步骤 | 本 Skill 的职责 | 产出（是否回灌 PMContext） |
|------|---------------|--------------------------|
| 6. 交付（交接） | 盘点会话状态，压缩成交接文档 | 不回灌（产出元数据 View） |

执行时必须依次完成上述步骤，不可跳步。步骤产出写入 `.loop/handoff-step6.md`。

**产出约束**：
- 交接文档必须自包含——接手者不读对话历史也能进入
- 下一步建议必须具体到 skill 调用（如"运行 `/pm-prd --auto`"）
- 未完成项必须精确到"停在哪一步"

**依赖检查**：文档是否自包含？下一步是否具体？未完成项是否精确？

**Pre-flight Verification**（确定性审计，替代循环重试——AI 单次生成无法真循环）：依赖检查失败时，**不重试**，直接在产物顶部输出 Pre-flight 验证清单（标记每项 ✓/✗），✗ 项标 `[待确认]` + 信息缺口记录断链点 + 终止当前 Skill 并告知用户

### Step 1: 盘点 PMContext 状态

读取 `docs/pm-context/pm-context.md`（若存在），提取：
- 需求名和概述
- 置信度分布（事实/[假设]/[待确认]/[冲突] 占比）
- 信息缺口清单
- PMContext 最后修改时间

若 PMContext 不存在 → 标注"PMContext 未创建，工作处于 collect 之前阶段"。

### Step 2: 盘点已完成产物

扫描 `docs/pm-context/` 目录，列出已生成的产物：
```
已完成:
- pm-context.md ✓ (置信度: 事实 60% / [假设] 25% / [待确认] 15%)
- prd/ai-prd.md ✓
- prd/humanprd.md ✓
- sketch/wireframe.md ✓
- sketch/flow.md ✓
- sketch/ia.md ✗ (未生成)
- sketch/state.md ✗ (未生成)
- premortem.md ✓
```

### Step 3: 识别未完成项

从已完成产物盘点，识别：
- 哪些 skill 已跑完
- 哪些 skill 部分完成（停在 Step 几）
- 哪些 skill 未调用
- PMContext 中 `[待确认]` 项需 PM 补充什么

### Step 4: 记录关键决策

从会话上下文提取关键决策：
```
关键决策:
1. 选择追问模式而非自主推断（PM 想逐维确认）→ 来源: 对话
2. 续费方案选"一键续费"而非"自动续费"（PM 暂不做自动续费）→ 来源: 对话: PM 确认
3. 技术栈定为 Vue3 + Vite + TS（项目已有 package.json）→ 来源: 项目扫描
```

### Step 5: 给出下一步建议（条件触发器，借鉴 superpowers/condition-based-waiting）

**核心原则**：下一步不是"按时间顺序执行"，而是"当条件满足时触发"——避免接手者在前置条件未达时盲目执行导致空转。

基于未完成项，给出**条件触发式**下一步：

```
下一步建议（条件触发）:
1. 触发条件: PMContext [待确认] 3 项已补全
   触发动作: /pm-need <补充材料> --incremental
   前置检查: 待确认项数 == 0 后才触发下一步
2. 触发条件: PMContext 置信度 事实 >= 80%
   触发动作: /pm-ia 和 /pm-state
   前置检查: 置信度不达标则先跑 /pm-grill 补证据
3. 触发条件: 草图全生成（ia + state ✓）
   触发动作: /pm-sketch --prototype --auto
   前置检查: 草图未全则不触发，避免原型基于不完整草图
```

**条件触发器规范**（每条下一步必须含）：
- **触发条件**：可观测的状态断言（文件存在/置信度达标/待确认清零），非时间猜测
- **触发动作**：具体 skill 调用
- **前置检查**：条件未达时该做什么（补证据/跑前置 skill/等待 PM 输入），不可空转

**反模式**（借鉴 condition-based-waiting "勿猜时间"）：禁止写"然后""接下来"等时序词——时序是条件满足的自然结果，不是指令。

### Step 6: 写入交接文档

写入 `docs/pm-context/handoff.md`，格式：

```markdown
# 交接文档

> 生成时间: <timestamp>
> 需求: <需求名>
> 会话起点: <本会话从哪开始>

## PMContext 状态
- **路径:** `docs/pm-context/pm-context.md`
- **置信度分布:** 事实 N% / [假设] N% / [待确认] N% / [冲突] N%
- **最后修改:** <时间>
- **状态:** <精炼中/已审计/已生成 PRD/已生成草图>

## 已完成产物
| 产物 | 状态 | 路径 | 备注 |
|---|---|---|---|
| PMContext | ✓ | docs/pm-context/pm-context.md | 置信度 75% |
| AI PRD | ✓ | docs/pm-context/prd/ai-prd.md | - |
| Human PRD | ✓ | docs/pm-context/prd/human-prd.md | - |
| 线框图 | ✓ | docs/pm-context/sketch/wireframe.md | - |
| 流程图 | ✓ | docs/pm-context/sketch/flow.md | - |
| 信息架构图 | ✗ | - | 未生成 |
| 状态机图 | ✗ | - | 未生成 |
| Pre-Mortem | ✓ | docs/pm-context/premortem.md | - |

## 未完成项
1. 信息架构图（/pm-ia）未调用
2. 状态机图（/pm-state）未调用
3. PMContext 中 3 项 [待确认]:
   - 续费转化率基线数据（PM 需提供）
   - 支付通道限制（PM 需确认）
   - 会员等级体系（PM 需补充）

## 关键决策
| 决策 | 选择 | 理由 | 来源 |
|---|---|---|---|
| refine 模式 | 追问模式 | PM 想逐维确认 | 对话 |
| 续费方案 | 一键续费 | PM 暂不做自动续费 | 对话: PM 确认 |
| 技术栈 | Vue3+Vite+TS | 项目已有 package.json | 项目扫描 |

## 下一步建议（条件触发）
| # | 触发条件 | 触发动作 | 前置检查 |
|---|---------|---------|---------|
| 1 | PMContext [待确认] 项 = 0 | `/pm-need <补充材料> --incremental` | 未清零不触发 |
| 2 | 置信度 事实 >= 80% | `/pm-ia` + `/pm-state` | 不达标先 `/pm-grill` |
| 3 | 草图全生成（ia+state ✓） | `/pm-sketch --prototype --auto` | 草图未全不触发 |

## 知识转移（借鉴 skills/teach：mission grounding + learning records + ZPD）

> 状态交接让接手者知道"做到哪"，知识转移让接手者知道"为什么这样定"——非显性决策理由是避免重复讨论的关键。

### 决策理由（learning-records 式，非显性知识）
| 决策 | 选择 | 为什么这样定（非显性理由） | 可被推翻的条件 |
|------|------|--------------------------|--------------|
| refine 模式选追问 | 逐维确认 | PM 首次做该需求，对领域不熟，自主推断风险高 | PM 表达熟悉度提升后可切自主模式 |
| 续费选一键续费 | 非自动续费 | 自动续费涉及合规+扣费争议，本期合规审查未启动 | 合规审查通过后可重启自动续费评估 |

### 接手者能力-任务差距（ZPD，zone of proximal development）
- **接手者需具备**：读 PMContext 的能力 + 跑 skill 的能力 + 判断条件触发的能力
- **可能差距**：若接手者不熟悉条件触发器模式 → 建议先读本文件"下一步建议（条件触发）"段说明
- **弥合建议**：复杂决策旁标"为什么"，接手者遇疑问先查"决策理由"表再问 PM

## 接手者快速进入指南
1. 读本文件了解工作状态
2. 读 `docs/pm-context/pm-context.md` 了解需求全貌
3. 读未完成产物对应 skill 的 SKILL.md 了解下一步怎么跑
4. 按上方"下一步建议"顺序执行
```

### Step 6.5: 交接文档质量自检（写入前必过）

借鉴 superpowers/verification-before-completion 纪律——交接文档落盘前必须过以下自检，任一不过标 🟡 需修补：

| # | 自检项 | 通过标准 | 不过处理 |
|---|--------|---------|---------|
| 1 | **自包含性** | 接手者不读对话历史能否进入工作？ | 补足缺失上下文 |
| 2 | **下一步具体性** | 每条下一步是否具体到 skill 调用（如`/pm-prd --auto`）？ | 改为具体 skill 调用 |
| 3 | **未完成项精确性** | 每未完成项是否精确到"停在哪一步"？ | 补 Step 编号或标"进度不明" |
| 4 | **关键决策可追溯** | 每决策是否标注来源（对话/PMContext/项目扫描）？ | 补来源标注 |
| 5 | **置信度分布完整** | 事实/[假设]/[待确认]/[冲突] 四态占比是否齐全？ | 从 PMContext 手动统计 |
| 6 | **产物状态盘点** | 每产物是否标 ✓/✗ + 路径？ | 补状态标注 |
| 7 | **`[待确认]` 项盘点** | PMContext 待确认项是否全列出？ | 补全待确认项清单 |
| 8 | **条件触发器完整** | 每下一步是否含触发条件+触发动作+前置检查三要素？ | 改为条件触发式（禁"然后/接下来"时序词） |
| 9 | **知识转移完整** | 关键决策是否含"非显性理由"+"可被推翻条件"？ | 补决策理由，标注推翻条件 |

**自检纪律**（借鉴 verification-before-completion）：
- 不得声称"交接文档已完成"而不跑自检——evidence before assertions
- 自检不过的文档标 🟡 不落盘，先修补再落盘
- 落盘后再次跑自检确认通过

**🔴 CHECKPOINT** — 输出交接文档路径 + 已完成产物数 + 未完成项数 + 下一步建议数 + 自检结果（9 项全过/🟡 N 项需修补）。

## 流程链落盘

步骤 6（交付）产出完成后，写入中间工件：
- `docs/pm-context/.loop/handoff-step6.md`（状态盘点映射 + 审计三元组）

## 失败模式

| 触发条件 | 一线修复 | 仍失败兜底 |
|---------|---------|-----------|
| **🔴 STOP**：`docs/pm-context/pm-context.md` 不存在 | 标注"工作处于 collect 之前阶段"，交接文档仅记录会话上下文 | 不阻塞，生成精简版交接文档 |
| **🔴 STOP**：会话上下文不足以提取关键决策 | 标注"关键决策记录不全，建议接手者与 PM 确认" | 不阻塞，但交接文档顶部加 ⚠️ |
| PMContext 存在但置信度字段缺失 | 从 PMContext 内容手动统计置信度分布 | 无法统计则标注"置信度待评估" |
| 产物目录有文件但内容为空 | 标注"产物文件存在但为空，疑似生成中断" | 提示接手者重跑对应 skill |
| 无法确定"停在哪一步" | 从最后修改的 `.loop/` 文件推断进度 | 无法推断则标注"进度不明，建议从 skill 起点重跑" |

## 不要做什么（反例黑名单）

| 反模式 | 为什么不要做 |
|--------|------------|
| 把对话历史原样复制当交接文档 | 接手者需要的是状态摘要，不是聊天记录 |
| 下一步建议写"继续工作"等模糊措辞 | 必须具体到 skill 调用（如"运行 `/pm-prd --auto`"） |
| 不盘点未完成项 | 未完成项是交接的核心，遗漏导致接手者重复劳动 |
| 不记录关键决策 | 决策丢失导致接手者重复讨论已定事项 |
| 交接文档依赖对话历史才能理解 | 文档必须自包含，否则失去交接意义 |
| 忽略 `[待确认]` 项盘点 | 待确认项是 PM 需补充的，接手者必须知道还缺什么 |
| 审计三元组转换操作写"将 A 转换为 A'" | 同义反复，无推理密度，判定为 Failure |
| 审计三元组转换操作写"基于上述依据产出" | 空话，未阐明具体推导逻辑，判定为 Failure |

## 产出示例

交接文档片段：

```markdown
## 未完成项
1. 信息架构图（/pm-ia）未调用
2. PMContext 中 3 项 [待确认]: 续费转化率基线/支付通道/会员等级

## 下一步建议
1. **优先:** 补全 [待确认] → `/pm-need <补充材料> --incremental`
2. `/pm-ia` 生成信息架构图
3. **可选:** `/pm-sketch --prototype --auto` 生成 HTML 原型
```

### Further Reading

- [Anthropic Agent Skills 规范](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Session Handoff Best Practices](https://www.productcompass.pm/p/cpdm)

## 产出示例 · 延伸参考 · 实战提示

详见 [references/handoff-example.md](references/handoff-example.md)（完整交接文档示例 + 状态盘点检查清单）。

### 实战提示

- **30 秒进入是标准**：接手者读交接文档 30 秒内应知道"做到哪、还差什么、下一步"
- **下一步必须具体到 skill 调用**：写"运行 `/pm-prd --auto`"而非"继续工作"
- **未完成项是核心**：遗漏未完成项 = 让接手者重复劳动
- **关键决策防止重复讨论**：记录"为什么这样定"，接手者不会重新争论已定事项
- **新会话开头读交接文档**：接手 Agent 第一件事是读本文件恢复上下文
