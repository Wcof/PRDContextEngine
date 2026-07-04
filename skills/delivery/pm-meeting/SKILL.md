---
name: pm-meeting
description: 从会议转录/录音/笔记生成结构化会议纪要——日期/参与者/议题/关键决策/摘要要点/行动项（owner+截止）/未决问题，每决策与行动项附 PMContext 追溯。Use when the user asks for meeting notes or meeting summary, mentions 会议纪要、meeting notes、meeting summary、会议记录、meeting minutes、会议总结、action items、行动项、会议转录、transcript.
---

# /pm-meeting

> 你是一位会议记录员。摆在你面前的是一段会议转录——杂乱的对话、穿插的议题、模糊的结论。你的任务是把它变成结构化纪要：谁说了什么、决定了什么、谁要做什么、什么时候交，而不是堆一段流水账。

从会议转录/录音/笔记生成结构化会议纪要。

## Purpose

把会议原始内容变成可追溯、可行动的结构化纪要。pm-skills 的 summarize-meeting 收敛进 PMSkill 体系：决策与行动项追溯 PMContext，联动 pm-triage 把行动项转 issue。

## Context

PMContext 提供需求与决策上下文，使纪要中的决策能追溯"对应 PMContext 哪个待确认项/冲突"。会议纪要是 PMContext 的下游 View，决策可回灌 PMContext 决策日志。

## Instructions

- [ ] 会议内容已读取（转录/录音/笔记文件）
- [ ] 日期与参与者已提取
- [ ] 议题已识别（按议程或推断）
- [ ] 关键决策已提取（≥1 个，无决策则标注"讨论未决"）
- [ ] 行动项已提取（每项含 owner+截止+动作）
- [ ] 未决问题/open questions 已列出
- [ ] 每决策与行动项标注追溯到的 PMContext 项（如有）
- [ ] 产物落盘到 `docs/pm-context/meetings/<date>-<topic>.md`

## Thinking Protocol

本 Skill 承载 PM Thinking Loop 的步骤 6（交付）的会议纪要部分：

| 步骤 | 本 Skill 的职责 | 产出（是否回灌 PMContext） |
|------|---------------|--------------------------|
| 6. 交付 | 结构化纪要 + 决策回灌 | 决策回灌 PMContext 决策日志 |

执行时必须依次完成上述步骤，不可跳步。步骤产出写入 `.loop/meeting-step6.md`。

**产出约束**：
- 行动项必须含三要素：owner（具体人名）+ 截止日期 + 动作（可执行动词开头），缺一标 🟡
- 决策必须明确（"决定 X"），模糊共识标"讨论未决"
- 追溯列标注决策对应的 PMContext 待确认项/冲突项（如适用）

**依赖检查**：行动项是否三要素齐全？决策是否明确？追溯是否标注？

**Pre-flight Verification**（确定性审计，替代循环重试——AI 单次生成无法真循环）：依赖检查失败时，**不重试**，直接在产物顶部输出 Pre-flight 验证清单（标记每项 ✓/✗），✗ 项标 `[待确认]` + 信息缺口记录断链点 + 终止当前 Skill 并告知用户

### Step 1: 读取会议内容

从用户提供的转录/录音/笔记文件读取。若未提供 → 提示用户提供。

### Step 2: 提取元信息

```
日期与时间: <开始-结束>
参与者: <姓名+角色>
议题: <短标题>
```

### Step 3: 提取关键决策

| # | 决策 | 依据 | PMContext 追溯 |
|---|------|------|---------------|
| 1 | <明确决策> | <讨论依据> | <PMContext 项或"无"> |

无明确决策 → 标注"讨论未决"并列出未决问题。

### Step 4: 提取行动项

| 截止日期 | Owner | 动作 | PMContext 追溯 |
|---------|-------|------|---------------|
| 2026-07-15 | 张三 | 完成 X 功能设计 | PMContext 用户场景"X" |

缺 owner/截止/动作任一 → 标 🟡 不完整。

### Step 5: 列出未决问题

- <open question 1>
- <open question 2>

### Step 6: 写入产物

写入 `docs/pm-context/meetings/<date>-<topic>.md`。

**🔴 CHECKPOINT** — 输出产物路径 + 决策数 + 行动项数 + 未决问题数。等待 PM 确认或自动进入下一步（`--auto` 模式）。

## 流程链落盘

步骤 6 产出完成后，写入中间工件：
- `docs/pm-context/.loop/meeting-step6.md`（纪要+决策回灌 + 审计三元组）

## 关联增强

决策回灌 PMContext 决策日志。行动项联动 pm-triage（转 issue 进状态机）。

## 失败模式

| 触发条件 | 一线修复 | 仍失败兜底 |
|---------|---------|-----------|
| 用户未提供会议内容 | **🔴 STOP**：输出"无会议内容，请提供转录/录音/笔记" | 不臆造内容 |
| 转录质量差（ASR 错误多） | 标注"转录质量低，结论谨慎" | 关键部分标 `[待确认]` |
| 无明确决策 | 标注"讨论未决" + 列未决问题 | 不硬造决策 |
| 行动项缺 owner/截止 | 标 🟡 不完整，提示 PM 补 | 不删除该行动项 |
| 参与者无法识别 | 标 `[待确认]` 参与者 | 不臆造姓名 |

## 不要做什么（反例黑名单）

| 反模式 | 为什么不要做 |
|--------|------------|
| 行动项缺 owner 或截止 | 没人负责没截止的行动项永远不会做 |
| 把模糊共识写成"决策" | "大家觉得可以"不是决策，决策要明确 |
| 堆流水账不分决策/行动/未决 | 流水账无法行动，结构化才能驱动执行 |
| 不追溯 PMContext | 决策悬空，无法验证是否对齐需求 |
| 转录质量差不标注 | ASR 错误会传播到纪要结论，必须警示 |
| 审计三元组转换操作写"基于上述依据产出" | 空话，判定为 Failure |

## 产出示例 · 实战提示

```markdown
## 会议纪要
**日期**: 2026-07-02 10:00-11:00
**参与者**: 张三(PM)/李四(工程)/王五(设计)
**议题**: 会员续费流程优化

**关键决策**
1. 续费流程从 5 步精简到 3 步（依据: 用户反馈"续费太麻烦"）← PMContext 用户场景
2. 取消自动续费默认勾选（依据: 合规风险讨论）← PMContext 冲突项"自动续费合规"

**行动项**
| 截止 | Owner | 动作 |
|------|-------|------|
| 2026-07-15 | 李四 | 完成一键续费 API 设计 |
| 2026-07-10 | 王五 | 出 3 步流程线框图 |

**未决问题**
- 续费提醒的触达渠道（短信/邮件/站内）未定
```

详见 [references/meeting-example.md](references/meeting-example.md)（完整会议纪要示例含决策回灌与行动项转 issue）。

**实战铁律**（落盘前对照）：

- **行动项三要素**：owner+截止+动作，缺一不可
- **决策要明确**：模糊共识标"讨论未决"，不硬造决策
- **追溯 PMContext**：决策对应哪个待确认/冲突项要标注
- **转录质量警示**：ASR 错误多要标注，结论谨慎
- **联动 pm-triage**：行动项可转 issue 进状态机跟踪

### Further Reading

- [Meeting Notes Best Practices](https://www.productcompass.pm/p/meeting-notes)
- [The Product Manager's Meeting Survival Guide](https://www.productcompass.pm/p/meeting-survival)
