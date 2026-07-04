# Darwin-Skill 第二轮进化 PMSkill — 最终交付报告

> **生成时间**: 2026-07-04 08:54
> **进化轮次**: 第二轮（第一轮 dim7 系统性规整已完成）
> **执行模式**: 借鉴 4 个参考项目 + 奥卡姆剃刀（非必要勿增实体）
> **状态**: ✅ 已完成，可验证

---

## 1. 进化目标

借鉴 4 个参考项目的核心 skill 能力，扩展或深化 PMSkill：
- `/Users/ldh/Downloads/project/pm-skills` — PM 类参考主力
- `/Users/ldh/Downloads/project/superpowers` — 工程纪律类
- `/Users/ldh/Downloads/project/skills` — Matt Pocock 风格（已部分借鉴）
- `/Users/ldh/Downloads/project/Axhub-Make-main` — 前端原型工具

---

## 2. 能力缺口对照（奥卡姆剃刀过程）

| 参考项目能力 | PMSkill 现状 | 判定 | 理由 |
|---|---|---|---|
| strategy-red-team（攻击承重假设） | pm-premortem（想象失败倒推） | **深化** | 互补不重复：premortem 偏"坏结果"，red-team 偏"哪个假设错了现在该测" |
| stakeholder-map（Power×Interest） | **无** | **新增** | 干系人管理真空白，pm-meeting/pm-align 隐含需要 |
| ideal-customer-profile | pm-persona + pm-market | 不增 | persona+market 已覆盖，ICP 是市场变体 |
| porters-five-forces | pm-pestle + pm-positioning | 不增 | PESTLE+定位已覆盖五力核心 |
| customer-journey-map | pm-journey（已有） | 不增 | 已有 |
| systematic-debugging | diagnosing-bugs（已有） | 不增 | 已有 |
| intended-vs-implemented | pm-align（已实现） | 不增 | 已实现 |
| axhub prototype-annotation | pm-sketch | 不增 | 绑定 @axhub 库，违反 runtime 中立 |
| superpowers verification-before-completion | Pre-flight + 🔴CHECKPOINT | 不增 | 已有等效机制 |
| superpowers writing-skills TDD | pm-skillauthor（12 处匹配） | 不增 | 已充分实现 |

**最终进化集**：1 新增 + 1 深化 = 2 项（非必要勿增实体）

---

## 3. 完成标准（可验证）

| # | 验证项 | 标准 | 实测 | 状态 |
|---|---|---|---|---|
| 1 | pm-stakeholder 9 段模板完整性 | 9 段全有 | 9/9 | ✅ |
| 2 | pm-stakeholder frontmatter 规范 | name + description + Use when 触发词 | 合规 | ✅ |
| 3 | pm-stakeholder 代码块闭合 | ``` 成对 | 2（偶数） | ✅ |
| 4 | pm-premortem 步骤 7 Red-Team 段落地 | 含承重假设+钢人化+Fails if+最便宜测试 | 1 段完整 | ✅ |
| 5 | pm-premortem 体积控制 | < 150% 原始 | 303 行 = 122% | ✅ |
| 6 | pm-premortem 代码块闭合 | ``` 成对 | 4（偶数） | ✅ |
| 7 | git 提交完整 | 改动已 commit | 1 commit (6e41d27) | ✅ |
| 8 | 工作树隔离恢复 | pm-sketch v3 WIP 完整 | stash 已 pop 恢复 | ✅ |
| 9 | darwin 日志记录 | results.tsv 有记录 | +2 条（总 203） | ✅ |
| 10 | 0 强制回滚 | 无 git reset --hard | 全程 commit | ✅ |

---

## 4. 分数变化

| skill | Before | After | Δ | 优化维度 |
|---|---|---|---|---|
| pm-stakeholder（新建） | 0 | **84** | +84 | dim2/3/5/7/9 全维 |
| pm-premortem（深化） | 82.3 | **90** | **+7.7** | dim2/3/5/7/9（加 Red-Team 步骤 7） |

**评分依据**：pm-premortem 加步骤 7 提升 dim2（工作流更完整 9→10）、dim3（失败模式 +3 行）、dim5（Fails if/证据/Kill/测试四项具体）、dim7（Pre-Mortem vs Red-Team 分工表）、dim9（反例 +3 行）。

---

## 5. 提交链

```
6e41d27 feat(evolve): darwin 进化 — 新增 pm-stakeholder + 深化 pm-premortem Red-Team 段
```

**改动统计**: 2 files changed, 242 insertions(+)

---

## 6. 新增/深化内容详述

### 6.1 新增 pm-stakeholder

**借鉴源**: `pm-skills/pm-execution/stakeholder-map` 的 Power×Interest 框架

**核心能力**:
- 从 PMContext 提取干系人（非通用 CEO/CTO 角色，必须追溯 PMContext 规则/边界条件/用户场景）
- Power×Interest 二分四象限（Manage Closely/Keep Satisfied/Keep Informed/Monitor）
- 每象限给 4 项：频率/渠道/关键信息/忽视风险
- 冲突干系人对识别 + 对标策略（升级/分阶段/数据驱动三选一）
- 沟通计划表 + 追溯列

**生态联动**: 与 pm-align（代码意图差距）互补管人对齐差距，与 pm-handoff 联动（交接含干系人状态），与 pm-meeting 联动（Manage Closely 干系人定向 1:1）

### 6.2 深化 pm-premortem（加步骤 7 Red-Team 段）

**借鉴源**: `pm-skills/pm-execution/strategy-red-team` 的承重假设攻击

**核心能力**（非新建 skill，作为 premortem 收尾深化）:
- 从第 6 步 Tiger 筛承重假设（≤5 个，"假了就全盘崩"的）
- 钢人化再攻击（先给最强版本再攻击，禁稻草人）
- 写"Fails if ___"（具体可证伪）
- 按 (影响×可能错×测试便宜度) 排序
- 每个存活承重假设给 4 项：Fails if / 本周该取证据 / Kill criterion / 最便宜测试
- 站得住的假设明说"成立无需测试"（禁制造怀疑）

**Pre-Mortem vs Red-Team 分工表**:

| 维度 | Pre-Mortem（步骤 1-6） | Red-Team（步骤 7） |
|------|----------------------|---------------------|
| 时态 | 想象已失败，倒推为什么 | 现在攻击承重假设 |
| 产出 | Tiger/Paper Tiger/Elephant 三分 | 承重假设 + 最便宜测试 |
| 行动 | 缓解措施（防御） | 本周测试（主动验证） |
| 价值 | 防盲点 | 防自信错 |

---

## 7. ⚠️ 评估可信度声明

| 项 | 说明 |
|---|---|
| dim8 全为 dry_run | 本环境无法 spawn 独立子 agent，按 darwin 黑名单第 6 条 dry_run=100% > 30%，**分数标 ⚠️ 不可全信** |
| 结构维度可信 | dim1-7,9 为静态分析，本次优化主要在 dim2/3/5/7/9，可信 |
| 后续验证建议 | 需 spawn 子 agent 环境跑 full_test 重评 dim8 |

---

## 8. 工作树最终状态

```
当前分支: darwin-evolve-20260704
本次进化提交: 6e41d27
pm-sketch v3 WIP: 已从 stash 恢复，工作树脏状态原样保留
darwin 日志: .agents/skills/darwin-skill/results.tsv（203 条，gitignore 内）
```

---

## 9. 后续建议

| # | 触发条件 | 触发动作 | 前置检查 |
|---|---|---|---|
| 1 | 认可本轮进化 | 合并 darwin-evolve-20260704 到 main | 确认 pm-sketch v3 WIP 已 stash 不丢 |
| 2 | 要继续进化 | 重新跑 darwin 基线评分找新短板 | 当前 49 skill 平均 ~85.85，dim8 不可信 |
| 3 | 要 dim8 full_test | 需 spawn 子 agent 环境 | 当前全 dry_run |
| 4 | 要清理分支 | auto-optimize/20260704-0451 已合并可删 | darwin-evolve-20260704 未合并先留 |

---

**Darwin-Skill 第二轮进化 PMSkill 任务已完成。奥卡姆剃刀后 1 新增 + 1 深化，非必要勿增实体，所有改动可追溯。**
