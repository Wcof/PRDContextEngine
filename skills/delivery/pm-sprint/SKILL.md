---
name: pm-sprint
description: Use when the user asks for sprint planning or iteration planning, mentions 迭代规划、sprint、sprint plan、迭代计划、容量估算、capacity、story selection、依赖、dependencies、sprint goal、velocity、DoR.
metadata:
  internal: true
---

# /pm-sprint

> 你是一位 Scrum Master。摆在你面前的是 backlog、团队容量与历史速率。你的任务是把"能做的事"塞进一个迭代——容量算准、故事选对、依赖排清、风险标明，最后用一句话说清楚这个迭代要交付什么。

从 PMContext 与 backlog 规划迭代。容量估算 → 故事选取 → 依赖映射 → 风险识别 → Sprint Goal。

## Purpose

把 backlog 拆成可执行的迭代计划。pm-skills 的 sprint-plan 收敛进 PMSkill 体系：从 PMContext 用户故事（pm-stories 产物）与优先级（pm-prioritize 产物）选取故事，每故事追溯 PMContext。

## Context

PMContext 衍生的 pm-stories 产物是 backlog 来源；pm-prioritize 产物定义优先级；PMContext"全局约束"定义团队资源与时间窗。本 skill 提取这些信息构建迭代计划。迭代计划是 PMContext 的下游 View。

## Instructions

- [ ] PMContext 已读取且非空（不存在则 STOP 提示运行 /pm-need）
- [ ] pm-stories 产物已读取（backlog 来源）
- [ ] pm-prioritize 产物已读取（优先级来源）
- [ ] 团队容量已估算（人数×可用×历史速率-20%buffer）
- [ ] 故事已按优先级选取且通过 DoR 校验
- [ ] 依赖已映射（内部+外部）
- [ ] 风险已识别且给缓解措施
- [ ] 单句 Sprint Goal 已定义
- [ ] 每故事标注追溯到的 PMContext 项
- [ ] 产物落盘到 `docs/pm-context/sprint.md`

## Thinking Protocol

本 Skill 承载 PM Thinking Loop 的步骤 4（权衡）+ 步骤 6（交付）的迭代规划部分：

| 步骤 | 本 Skill 的职责 | 产出（是否回灌 PMContext） |
|------|---------------|--------------------------|
| 4. 权衡 | 容量 vs 故事范围权衡 + 风险权衡 | 不回灌（产出 View） |
| 6. 交付 | 迭代计划文档 | 不回灌（产出 View） |

执行时必须依次完成上述步骤，不可跳步。步骤产出写入 `process/04-sprint-tradeoff.md`、`process/06-sprint-delivery.md`。

**产出约束**：
- 容量必须用公式估算：`人数 × 可用% × 历史速率 - 20% buffer`，禁拍脑袋
- 每故事必须通过 DoR（清晰验收标准 + 已估点 + 无 blocker），不达标标 🟡 需 refinement
- 依赖必须区分内部（可排序）与外部（需标注 owner + 风险）
- Sprint Goal 必须是单句价值描述，禁写"完成 N 个故事"

**依赖检查**：容量是否算准？故事是否过 DoR？依赖是否映射？Sprint Goal 是否单句价值？

**Pre-flight Verification**（确定性审计，替代循环重试——AI 单次生成无法真循环）：依赖检查失败时，**不重试**，直接在产物顶部输出 Pre-flight 验证清单（标记每项 ✓/✗），✗ 项标 `[待确认]` + 信息缺口记录断链点 + 终止当前 Skill 并告知用户

### Step 1: 读取 PMContext 与产物

读取 `<产物目录>/pm-context.md`（先读 `## PMSkill` 块取 `产物目录`，块不存在回退默认 `docs/pm-context/`） + `pm-stories` 产物（backlog）+ `pm-prioritize` 产物（优先级）。

若 PMContext 不存在 → **🔴 STOP**：提示先运行 `/pm-need`。
若 pm-stories 产物不存在 → 提示先运行 `/pm-stories`。

### Step 2: 容量估算

```
团队容量 = 人数 × 可用% × 历史速率 - 20% buffer

示例：5 人 × 80% 可用 × 40 点/迭代历史速率 × (1-20%buffer) = 128 点
```

| 项 | 值 | 来源 |
|----|----|----|
| 人数 | 5 | PMContext 全局约束/用户提供 |
| 可用% | 80%（扣 PTO/会议/on-call） | 用户提供 |
| 历史速率 | 40 点/迭代（近 3 迭代均值） | 用户提供/历史数据 |
| buffer | 20%（意外工作/bug/技术债） | 固定规则 |
| **可用容量** | **128 点** | 计算 |

历史速率缺失 → 标 `[假设]` 用行业均值或 PM 估算，提示收集 3 迭代后校准。

### Step 3: 故事选取（按优先级 + DoR）

从 pm-prioritize 排序的 backlog 按优先级拉取，每故事校验 DoR：

| 故事 | 优先级 | 点数 | DoR? | 依赖 | 选取? |
|------|--------|------|------|------|------|
| <故事1> | P0 | 8 | ✅ | 无 | ✅ |
| <故事2> | P0 | 13 | 🟡 验收不清 | <故事1> | 🟡 需 refinement |
| <故事3> | P1 | 5 | ✅ | 外部 API | ✅（标外部依赖） |

累计点数达容量即停。

### Step 3.5: 任务拆分粒度校验（借鉴 superpowers/writing-plans "task right-sizing + bite-sized"）

> 故事过 DoR 不等于可执行——大故事进迭代会卡住"做到一半无法验收"。必须校验每故事是否拆到"独立可测 + 2-5 天可完成"的粒度。

| 故事 | 点数 | 粒度校验 | 拆分建议 |
|------|------|---------|---------|
| 一键续费 | 8 | ✅ 独立可测（3 秒完成可断言） | 不拆 |
| 续费提醒 | 13 | 🟡 >10 点偏大，含通知模板+触发逻辑+频控 | 拆为"通知模板"(5)+"触发+频控"(8) |
| 会员等级展示 | 5 | ✅ 独立可测 | 不拆 |

**右值化标准**（借鉴 writing-plans task right-sizing）：
- **独立可测**：每任务结束有可独立验收的交付物（能写断言），不能测的拆到能测
- **2-5 天可完成**：>5 天的故事必须拆（大故事卡在迭代中段无法验收）
- **reviewer 可独立否决**：任务边界应让 reviewer 能"否决这个而批准邻居"，耦合任务拆开
- **setup 折入**：配置/脚手架/文档步骤折入需要它的交付任务，不单列

**反模式**（借鉴 writing-plans bite-sized）：
- ❌ "续费提醒 13 点整体进迭代"（中段无法验收，卡住才发现做错）
- ✅ 拆为"通知模板"(5，可独立验收模板渲染)+"触发+频控"(8，可独立验收触发逻辑)

粒度不达标的故事标 🟡 返回 pm-stories 拆分，不强行塞进迭代。

### Step 4: 依赖映射

| 故事 | 依赖类型 | 依赖对象 | Owner | 风险 |
|------|---------|---------|-------|------|
| <故事2> | 内部 | <故事1> | 团队内 | 低（可排序） |
| <故事3> | 外部 | 支付 API | 平台团队 | 中（需提前对齐） |

关键路径：识别依赖链最长路径，标注。

### Step 5: 风险识别

| 风险 | 影响 | 缓解措施 |
|------|------|---------|
| 高不确定性故事 | 范围蔓延 | 拆分或给 spike 探究 |
| 外部依赖滑期 | 阻塞 | 提前对齐 + 备选方案 |
| 知识集中（只 1 人能做） | 单点故障 | 结对/知识共享 |

### Step 6: Sprint Goal

单句价值描述（禁写"完成 N 个故事"）：

```
Sprint Goal: 让新用户在 20 分钟内完成首次付费（对应 PMContext 用户场景"降低首次付费摩擦"）
```

### Step 7: 写入产物

写入 `docs/pm-context/sprint.md`，含容量表 + 故事表 + 依赖图 + 风险表 + Sprint Goal + 追溯列。

**🔴 CHECKPOINT** — 输出产物路径 + 可用容量 + 选取故事数 + Sprint Goal。等待 PM 确认或自动进入下一步（`--auto` 模式）。

### Step 7.5: 迭代完成验证门（借鉴 superpowers/finishing-a-development-branch "verify tests → detect → options → execute → cleanup"）

> 迭代计划落盘后还不是"完成"——在宣布迭代就绪前必须跑验证门，确保计划是可执行的。

**验证门顺序**（借鉴 finishing-a-development-branch 的 verify-before-proceed）：

```
Step 1: Verify 容量 → 故事点数总和是否 ≤ 可用容量？
  是 → 继续
  否 → 标 🟡 超载，提示调整（减故事/拆故事/增容量）
  
Step 2: Verify DoR → 选取的故事是否全部通过 DoR？
  是 → 继续
  否 → 标 🟡 不达标故事需 refinement，不进入迭代
  
Step 3: Verify 粒度 → 每故事是否通过 Step 3.5 粒度校验？
  是 → 继续
  否 → 标 🟡 大故事需拆分，退回 pm-stories
  
Step 4: Verify 依赖 → 每外部依赖是否标注 owner + 风险？
  是 → 继续
  否 → 标 🟡 缺 owner 的依赖标 `[待确认]`，不阻塞但警示
  
Step 5: Verify 回滚 → 如果迭代中发现问题，是否有降级方案？
  是 → 继续
  否 → 标 🟢 建议补降级方案但不阻塞
```

**验证通过则迭代就绪**，可进入开发阶段。验证不通过的项目不阻塞发布，但标 🟡 在迭代计划顶部标注风险区域。

## 流程链落盘

步骤 4、6 产出完成后，写入中间工件：
- `docs/pm-context/process/04-sprint-tradeoff.md`（容量权衡+风险 + 审计三元组）
- `docs/pm-context/process/06-sprint-delivery.md`（迭代计划 + 审计三元组）

## 关联增强

在追溯列标注每故事追溯到的 PMContext 项。迭代计划与 pm-stories（backlog 来源）、pm-prioritize（优先级来源）、pm-retro（历史速率校准来源）交叉验证。

## 失败模式

| 触发条件 | 一线修复 | 仍失败兜底 |
|---------|---------|-----------|
| `docs/pm-context/pm-context.md` 不存在 | **🔴 STOP**：输出"未找到 PMContext，先运行 `/pm-need <需求>`" | 不阻塞，提示后退出 |
| pm-stories 产物不存在 | 提示先运行 `/pm-stories` 生成 backlog | 不臆造故事 |
| 历史速率数据缺失 | 标 `[假设]` 用 PM 估算，提示收集 3 迭代后校准 | 不阻塞 |
| 团队人数/可用%未提供 | **🔴 STOP**：输出"无团队容量信息，需 PM 提供人数与可用率" | 不臆造容量 |
| 故事未通过 DoR | 标 🟡 需 refinement，不选取 | 提示先 refine |
| 容量 < 最高优先级故事点数 | 缩小范围或拆分故事 | 标 `[待确认]` 需 PM 调整优先级 |
| 外部依赖无 owner | 标 `[待确认]` 需 PM 指定对接人 | 不臆造 owner |

## 不要做什么（反例黑名单）

| 反模式 | 为什么不要做 |
|--------|------------|
| 容量拍脑袋不按公式 | 没有依据的容量要么超载要么闲置 |
| 选取未过 DoR 的故事 | 验收不清的故事做到一半才发现做错 |
| 选取粒度不达标的故事（>5天/不可独立测，违反 Step 3.5） | 大故事卡迭代中段无法验收，必须拆到 2-5 天独立可测 |
| Sprint Goal 写"完成 N 个故事" | 这是 todo list 不是 goal，goal 要描述价值交付 |
| 不区分内部/外部依赖 | 内部可排序，外部需对齐，混为一谈会漏外部风险 |
| 不留 buffer | 20% buffer 是应对意外的底线，满载必爆 |
| 历史速率缺失不标假设 | 用拍脑袋的速率当事实，迭代必超载 |
| 不追溯 PMContext | 故事悬空，无法验证是否对齐需求 |
| 审计三元组转换操作写"基于上述依据产出" | 空话，未阐明具体推导逻辑，判定为 Failure |

## 产出示例 · 实战提示

会员产品迭代计划片段：

```markdown
## 容量：128 点
5 人 × 80% × 40 点 × 80% = 128 点

## 选取故事（共 122 点）
| 故事 | 优先级 | 点数 | DoR | 依赖 |
|------|--------|------|-----|------|
| 一键续费 | P0 | 8 | ✅ | 无 |
| 续费提醒 | P0 | 13 | ✅ | 内部:通知模块 |
| 会员等级展示 | P1 | 5 | ✅ | 无 |
| ...

## Sprint Goal
让到期会员在 3 次点击内完成续费（对应 PMContext 用户场景"续费流程太麻烦"）
```

详见 [references/sprint-example.md](references/sprint-example.md)（完整迭代计划示例含依赖图与风险矩阵）。

**实战铁律**（落盘前对照）：

- **容量按公式**：人数×可用×速率×80%，不要拍脑袋
- **DoR 是闸门**：没过 DoR 的故事不进迭代，先 refine
- **Sprint Goal 说价值**：禁写"完成 N 个故事"，写交付的价值
- **外部依赖早对齐**：外部依赖是滑期主因，迭代开始前就对齐
- **20% buffer 是底线**：满载必爆，留 buffer 应对意外

### Further Reading

- [Sprint Planning Guide](https://www.productcompass.pm/p/sprint-planning)
- [Scrum Guide - Sprint Planning](https://scrumguides.org/)
- [Velocity and Capacity Estimation](https://www.productcompass.pm/p/velocity-estimation)
