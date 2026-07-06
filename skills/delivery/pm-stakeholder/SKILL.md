---
name: pm-stakeholder
description: 从 PMContext 构建干系人地图——Power×Interest 四象限分类（Manage Closely/Keep Satisfied/Keep Informed/Monitor）+ 每象限沟通策略（频率/渠道/关键信息/忽视风险）+ 冲突干系人对标 + 沟通计划表，每干系人追溯 PMContext。Use when preparing for launch, aligning cross-functional teams, or the user mentions 干系人、stakeholder、沟通计划、stakeholder map.
metadata:
  internal: true
---

# /pm-stakeholder

> 你是一位项目交付经理，正在为即将上线的产品构建干系人地图。**干系人地图不是把所有名字列出来，是识别谁能在上线日挡你、谁能帮你扫清障碍——然后把精力按 Power×Interest 分配，而非对所有人一视同仁。**

从 PMContext 构建干系人地图 + 沟通计划。Power×Interest 四象限 + 每象限策略 + 冲突对标。

## Purpose

把 PMContext 涉及的干系人聚成 Power×Interest 地图，产出差异化沟通计划。提炼 pm-skills/pm-execution/stakeholder-map 的 Power×Interest 框架，绑定 PMSkill 的 PMContext 作为干系人来源。与 pm-align 互补（pm-align 审代码意图差距，本 skill 管人对齐差距），与 pm-handoff 联动（交接文档含干系人状态）。

## Context

产品即将上线或跨团队协作。PMContext 的"用户场景/边界条件/规则"隐含干系人（决策者、审批方、依赖方、受影响方）。本 skill 从 PMContext 提取这些角色，按 Power×Interest 分类，产出沟通计划。干系人地图是 PMContext 的交付 View，与 PRD/草图平级。

## Instructions

读取 `<产物目录>/pm-context.md`（先读 `## PMSkill` 块取 `产物目录`，块不存在回退默认 `docs/pm-context/`）。若不存在，提示先运行 `/pm-need`。

- [ ] PMContext 已读取且非空
- [ ] 干系人已从 PMContext 提取（决策者/审批方/依赖方/受影响方/反对者）
- [ ] 每干系人已按 Power（高/低）× Interest（高/低）分类
- [ ] 四象限策略已分配（Manage Closely/Keep Satisfied/Keep Informed/Monitor）
- [ ] 每象限有沟通频率+渠道+关键信息+忽视风险
- [ ] 冲突干系人对已识别（利益相争的双方）+ 对标策略
- [ ] 沟通计划表已生成
- [ ] 每干系人追溯 PMContext 项
- [ ] 产物落盘到 `docs/pm-context/stakeholder-map.md`

## Thinking Protocol

本 Skill 承载 PM Thinking Loop 的步骤 6（交付）的干系人对齐部分：

| 步骤 | 本 Skill 的职责 | 产出（是否回灌 PMContext） |
|------|---------------|--------------------------|
| 6. 交付（对齐） | 从 PMContext 提取干系人，Power×Interest 分类，产出沟通计划 | 不回灌（产出 View） |

执行时必须依次完成上述步骤，不可跳步。步骤产出写入 `process/06-stakeholder-delivery.md`。
每项产出必须附带审计三元组（依据集 → 工具/技术 → 产出），完整版落 `process/`。

**产出约束**：
- 干系人必须从 PMContext 提取，禁凭空列"CEO/CTO"通用角色——必须对应当前产品的具体决策者/审批方
- Power×Interest 必须二分（高/低），禁"中等"骑墙
- "Manage Closely"象限干系人必须有 1:1 频率（周/双周），禁仅"定期更新"
- 冲突干系人对必须给出对标策略（非仅标注"有冲突"）

**依赖检查**：干系人是否全部追溯 PMContext？Power×Interest 是否二分？Manage Closely 是否有 1:1 频率？冲突对是否有对标策略？

**Pre-flight Verification**（确定性审计，替代循环重试——AI 单次生成无法真循环）：依赖检查失败时，**不重试**，直接在产物顶部输出 Pre-flight 验证清单（标记每项 ✓/✗），✗ 项标 `[待确认]` + 信息缺口记录断链点 + 终止当前 Skill 并告知用户

**审计三元组示例**：
`<依据集: [PMContext规则R1"合规需法务审批", PMContext边界条件"上线需财务签批"]> → [工具: /pm-stakeholder, 方法: Power×Interest分类] → [转换: 规则R1+边界条件→法务/财务为High Power+High Interest→Manage Closely象限] → <产出: 法务总监 1:1 周会 + 财务签批节点嵌入上线 checklist>`

## 流程

### 1. 读取 PMContext 提取干系人

读取 `<产物目录>/pm-context.md`（先读 `## PMSkill` 块取 `产物目录`，块不存在回退默认 `docs/pm-context/`），提取：
- "规则" → 审批方/合规方（如"需法务审批"→法务）
- "边界条件" → 决策者/签批方（如"预算上限"→财务/赞助人）
- "用户场景" → 受影响方（如"现有用户迁移"→客服/运营）
- 全局约束 → 依赖方（如"依赖支付通道"→支付团队）
- 反对意见（若有）→ 潜在反对者

若 PMContext 不存在 → **🔴 STOP**：提示先运行 `/pm-need`。

### 2. Power×Interest 分类

对每干系人二分：

| 维度 | 高 | 低 |
|------|---|---|
| **Power**（影响力） | 能否决/能批资源/能改方向 | 仅建议/仅被通知 |
| **Interest**（受影响度） | 直接受产品影响/深度参与 | 间接受影响/边缘参与 |

### 3. 四象限策略

| | High Interest | Low Interest |
|---|---|---|
| **High Power** | **Manage Closely** — 1:1 周会，早期参与决策，征求意见 | **Keep Satisfied** — 定期汇报，仅关键问题升级 |
| **Low Power** | **Keep Informed** — 定期状态更新，邀请 demo，收反馈 | **Monitor** — 轻量更新，按需提供 |

每象限必须给出 4 项：
- **沟通频率**（日/周/双周/月）
- **渠道**（1:1/邮件/Slack/会议/dashboard）
- **关键信息**（针对该象限关心的内容）
- **忽视风险**（若不沟通会怎样）

### 4. 冲突干系人对识别

识别利益相争的干系人对（如"销售要快上线"vs"法务要合规审查"），给出对标策略：
- 升级共同上级裁决
- 分阶段交付（先满足一方，后补另一方）
- 数据驱动谈判（用 PMContext 度量对齐）

### 5. 沟通计划表

| 干系人 | 角色 | Power | Interest | 象限 | 频率 | 渠道 | 关键信息 |
|---|---|---|---|---|---|---|---|

### 6. 写入产物

写入 `docs/pm-context/stakeholder-map.md`，含四象限图 + 沟通计划表 + 冲突对标 + 追溯列。

**🔴 CHECKPOINT** — 输出产物路径 + 四象限干系人数 + 冲突对数。等待 PM 确认或自动进入下一步（`--auto` 模式）。

## 流程链落盘

步骤 6 产出完成后，写入中间工件：
- `docs/pm-context/process/06-stakeholder-delivery.md`（干系人清单+四象限+沟通计划+审计三元组）

产物主文件落盘路径：`docs/pm-context/stakeholder-map.md`

## 关联增强

每干系人追溯 PMContext 项（规则/边界条件/用户场景）。与 pm-align 联动（pm-align 找代码意图差距，本 skill 找人对齐差距），与 pm-handoff 联动（交接文档含干系人状态），与 pm-meeting 联动（每 Manage Closely 干系人可设计定向 1:1 议程）。

## 失败模式

| 触发条件 | 一线修复 | 仍失败兜底 |
|---------|---------|-----------|
| `docs/pm-context/pm-context.md` 不存在 | **🔴 STOP**：输出"未找到 PMContext，先运行 `/pm-need <需求>`" | 不阻塞，提示后退出 |
| PMContext 无明确干系人线索（纯技术产品） | 从全局约束和边界条件推断依赖方 | 标 `[假设]` 推断的干系人，提示 PM 确认 |
| 干系人全部落入同一象限 | 重新审视 Power/Interest 划分，通常说明维度混淆 | 标 `[待确认]` 分类粒度 |
| 冲突对无对标策略 | 至少给"升级共同上级"兜底 | 标 `[冲突]` 让 PM 裁决 |
| Manage Closely 干系人 >5 | 聚合同部门干系人，减少 1:1 数量 | 标注"Manage Closely 过载，建议代表制" |
| 干系人无法追溯 PMContext | 标 `[假设]` 并附推断依据 | 记入信息缺口清单 |

## 不要做什么（反例黑名单）

| 反模式 | 为什么不要做 |
|--------|------------|
| 列通用角色"CEO/CTO/市场总监" | 通用角色与当前产品脱节，必须从 PMContext 提取具体决策者 |
| Power/Interest 写"中等" | 骑墙分类无策略意义，必须二分 |
| Manage Closely 仅"定期更新" | 高权力高兴趣干系人需 1:1 早期参与，定期更新是 Keep Informed 策略 |
| 冲突对仅标注"有冲突" | 不给对标策略=没解决，必须给升级/分阶段/数据驱动三选一 |
| 所有干系人同一频率 | 一视同仁=资源错配，高 Power 必须高频 |
| 不追溯 PMContext | 干系人悬空，无法验证是否对齐产品上下文 |
| 审计三元组转换操作写"将 A 转换为 A'" | 同义反复，无推理密度，判定为 Failure |
| 审计三元组转换操作写"基于上述依据产出" | 空话，未阐明具体推导逻辑，判定为 Failure |

## 产出示例 · 实战提示

`/pm-stakeholder 会员体系重构` 产出片段：

```markdown
# 干系人地图: 会员体系重构

## 四象限
| 象限 | 干系人 | 策略 |
|------|--------|------|
| Manage Closely | 法务总监(合规审批)/财务总监(定价签批)/产品VP(资源) | 1:1 周会 |
| Keep Satisfied | CTO(技术资源)/CEO(战略) | 月度汇报+关键升级 |
| Keep Informed | 客服主管(迁移影响)/运营(促销协同) | 双周状态+demo |
| Monitor | 外部支付通道PM(依赖) | 按需同步 |

## 沟通计划
| 干系人 | 角色 | Power | Interest | 象限 | 频率 | 渠道 | 关键信息 |
|---|---|---|---|---|---|---|---|
| 法务总监 | 合规审批 | 高 | 高 | Manage Closely | 周 | 1:1 | 退款政策/隐私条款/合规风险 |
| 财务总监 | 定价签批 | 高 | 高 | Manage Closely | 周 | 1:1 | LTV测算/价格敏感度/收入预测 |
| 客服主管 | 迁移影响 | 低 | 高 | Keep Informed | 双周 | 邮件+demo | 用户迁移节奏/培训需求/客诉预案 |

## 冲突对标
| 冲突对 | 争点 | 对标策略 |
|--------|------|---------|
| 销售 vs 法务 | 销售要快上线/法务要审查周期 | 分阶段：先上线非敏感功能，敏感功能等法务签批 |
```

**实战铁律**（落盘前对照）：

- **从 PMContext 提取非通用角色**：通用 CEO/CTO 与产品脱节
- **Power×Interest 二分**：骑墙分类无策略意义
- **Manage Closely 必须 1:1**：定期更新是 Keep Informed 的活
- **冲突对必须给对标策略**：标注"有冲突"不解决
- **一象限过载要聚合**：Manage Closely >5 用代表制

### Further Reading

- [The Product Management Frameworks Compendium](https://www.productcompass.pm/p/the-product-frameworks-compendium)
- [Team Topologies: Set and Scale Product Teams](https://www.productcompass.pm/p/team-topologies-a-handbook-to-set)
- [5 GTM Principles as a PM](https://www.productcompass.pm/p/5-gtm-principles-with-frameworks-templates)
