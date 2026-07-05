---
name: pm-roadmap
description: 从 PMContext 把 output-focused roadmap（功能清单）转成 outcome-focused roadmap（客户+业务成果）——每 initiative 重写为"Enable [segment] to [customer outcome] so that [business impact]"格式 + 关键度量 + 依赖排序，每 outcome 附 PMContext 追溯。Use when the user asks for roadmap or outcome transformation, mentions roadmap、路线图、outcome roadmap、成果导向、outcome-focused、output to outcome、战略路线图、strategic roadmap、initiative transformation.
---

# /pm-roadmap

> 你是一位产品战略师。摆在你面前的是一份功能清单式 roadmap——"Q2 做搜索筛选、AI 推荐、仪表盘改版"。你的任务是把每个功能转成成果："让客户能 50% 更快找到产品"，而不是堆功能让团队对着 todo list 干活。

从 PMContext 把 output roadmap 转成 outcome roadmap。每 initiative 重写为成果陈述。

## Purpose

把功能清单式 roadmap 转成成果导向 roadmap。pm-skills 的 outcome-roadmap 收敛进 PMSkill 体系：从 PMContext 价值验证度量提取成果度量，每 outcome 追溯 PMContext 用户场景。

## Context

PMContext"用户场景"定义客户成果方向；"价值验证度量"定义业务影响度量；"全局约束"定义时间窗。本 skill 提取这些信息转换 roadmap。Roadmap 是 PMContext 的下游 View。

## Context（避免与上文 Context 段混淆——本段是 roadmap 转换的领域说明）

output-focused roadmap 制造虚假精确，让团队围绕功能而非成果对齐；outcome-focused roadmap 澄清要解决的客户问题与期望的业务价值，使执行灵活且具战略思维。

## Instructions

- [ ] PMContext 已读取且非空（不存在则 STOP 提示运行 /pm-need）
- [ ] "用户场景"已提取（客户成果方向来源）
- [ ] "价值验证度量"已提取（业务影响度量来源）
- [ ] "全局约束"已提取（时间窗来源）
- [ ] 原始 roadmap（功能清单）已读取（用户提供）
- [ ] 每 initiative 已重写为 outcome 陈述（Enable/so that 格式）
- [ ] 每 outcome 附关键度量 + 依赖/排序
- [ ] 战略对齐说明已输出（outcomes 如何对齐公司战略）
- [ ] 每 outcome 标注追溯到的 PMContext 项
- [ ] 产物落盘到 `docs/pm-context/roadmap.md`

## Thinking Protocol

本 Skill 承载 PM Thinking Loop 的步骤 4（权衡）+ 步骤 6（交付）的 roadmap 转换部分：

| 步骤 | 本 Skill 的职责 | 产出（是否回灌 PMContext） |
|------|---------------|--------------------------|
| 4. 权衡 | 每 initiative 的 outcome 推导 + 替代方案考量 | 不回灌（产出 View） |
| 6. 交付 | outcome roadmap 文档 | 不回灌（产出 View） |

执行时必须依次完成上述步骤，不可跳步。步骤产出写入 `.loop/roadmap-step4.md`、`.loop/roadmap-step6.md`。

**产出约束**：
- 每 initiative 必须用 `Enable [segment] to [customer outcome] so that [business impact]` 格式重写
- 每 outcome 必须附关键度量（从 PMContext 价值验证度量提取）
- 必须含"是否有更好方式达成同一 outcome"的考量（防功能固化）

**依赖检查**：outcome 格式是否完整？度量是否对齐 PMContext？替代方案是否考量？

**Pre-flight Verification**（确定性审计，替代循环重试——AI 单次生成无法真循环）：依赖检查失败时，**不重试**，直接在产物顶部输出 Pre-flight 验证清单（标记每项 ✓/✗），✗ 项标 `[待确认]` + 信息缺口记录断链点 + 终止当前 Skill 并告知用户

### Step 1: 读取 PMContext 与原始 roadmap

读取 `<产物目录>/pm-context.md`（先读 `## PMSkill` 块取 `产物目录`，块不存在回退默认 `docs/pm-context/`） + 用户提供的原始 roadmap（功能清单）。

若 PMContext 不存在 → **🔴 STOP**：提示先运行 `/pm-need`。
若用户未提供原始 roadmap → 提示提供，不臆造功能清单。

### Step 2: 每 initiative 的 outcome 转换

对每 initiative 问：
- 要达成什么成果？
- 解决客户什么问题？
- 改善什么业务指标？
- 是否有更好方式达成同一 outcome？

转换格式：
```
Enable [客户细分 from PMContext 用户场景] to [客户成果] so that [业务影响 from PMContext 价值验证度量]
```

### Step 3: 输出转换表

| 原 initiative（output） | 新 outcome 陈述 | 关键度量 | 依赖/排序 | PMContext 追溯 |
|------------------------|----------------|---------|----------|---------------|
| Q2: 高级搜索筛选 | Enable 高频创作者 to 50% 更快找到素材 so that 搜索退出率降 30% | 搜索退出率、首次搜索耗时 | 无 | PMContext 用户场景"找素材慢" |
| Q2: AI 推荐 | Enable 创作者 to 发现相关素材 so that 人均使用素材数 +20% | 人均素材数 | 推荐模型就绪 | PMContext 价值验证度量 |

### Step 4: 战略对齐说明

```
## 战略对齐
- outcomes 如何对齐公司战略：...
- 关键假设（客户需求）：...
- 依赖与排序：...
```

### Step 5: 写入产物

写入 `docs/pm-context/roadmap.md`，含转换表 + 战略对齐 + 追溯列。

**🔴 CHECKPOINT** — 输出产物路径 + 转换 initiative 数 + outcome 数。等待 PM 确认或自动进入下一步（`--auto` 模式）。

## 流程链落盘

步骤 4、6 产出完成后，写入中间工件：
- `docs/pm-context/.loop/roadmap-step4.md`（outcome 推导+权衡 + 审计三元组）
- `docs/pm-context/.loop/roadmap-step6.md`（roadmap 文档 + 审计三元组）

## 关联增强

在追溯列标注每 outcome 追溯到的 PMContext 项。Roadmap 与 pm-okr（季度成果对齐）、pm-prioritize（initiative 排序）交叉验证。

## 失败模式

| 触发条件 | 一线修复 | 仍失败兜底 |
|---------|---------|-----------|
| `docs/pm-context/pm-context.md` 不存在 | **🔴 STOP**：输出"未找到 PMContext，先运行 `/pm-need <需求>`" | 不阻塞，提示后退出 |
| 用户未提供原始 roadmap | **🔴 STOP**：输出"无原始 roadmap，请提供功能清单" | 不臆造功能 |
| initiative 无法转 outcome | 标 `[待确认]` 需 PM 说明该功能的客户价值 | 不硬造 outcome |
| outcome 度量无 PMContext 依据 | 标 `[假设]` 度量，提示 PM 补 | 不臆造度量 |
| 多 initiative 转同一 outcome | 合并或区分客户细分 | 标 `[冲突]` 让 PM 裁决 |

## 不要做什么（反例黑名单）

| 反模式 | 为什么不要做 |
|--------|------------|
| 保留功能清单不转 outcome | output roadmap 制造虚假精确，团队对着功能干活不知为何 |
| outcome 不附度量 | 没度量的 outcome 无法验证是否达成 |
| 不考量替代方案 | 功能固化会错过更好方式达成同一 outcome |
| 不追溯 PMContext | outcome 悬空，无法验证是否对齐需求 |
| 多 initiative 转同一 outcome 不合并 | 重复 outcome 浪费资源，应合并或区分细分 |
| 审计三元组转换操作写"基于上述依据产出" | 空话，判定为 Failure |

## 产出示例 · 实战提示

```markdown
## 原 roadmap（output）
- Q2: 高级搜索筛选、AI 推荐、仪表盘改版

## 转换后（outcome）
| 原 initiative | outcome | 度量 | PMContext 追溯 |
|--------------|---------|------|---------------|
| 高级搜索筛选 | Enable 高频创作者 to 50% 更快找到素材 so that 搜索退出率降 30% | 搜索退出率、首次搜索耗时 | 用户场景"找素材慢" |
| AI 推荐 | Enable 创作者 to 发现相关素材 so that 人均素材数 +20% | 人均素材数 | 价值验证度量 |
| 仪表盘改版 | Enable 运营 to 80% 更快监控全系统 so that 仪表盘加载降 80% | 加载耗时 | 边界条件"加载慢" |

## 替代方案考量
- "高级搜索筛选"可能有更好替代：智能分类标签（更低实现成本）→ 建议先做标签再评估筛选
```

详见 [references/roadmap-example.md](references/roadmap-example.md)（完整 roadmap 转换示例含战略对齐与替代方案）。

**实战铁律**（落盘前对照）：

- **outcome 三段式**：Enable X to Y so that Z，缺一段不完整
- **度量必附**：没度量的 outcome 无法验证，从 PMContext 价值验证度量提取
- **考量替代方案**：每个功能问"是否有更好方式"，防功能固化
- **追溯 PMContext**：outcome 悬空=没对齐需求
- **合并重复 outcome**：多 initiative 同 outcome 应合并或区分细分

### Further Reading

- [Outcome vs Output Roadmap](https://www.productcompass.pm/p/outcome-roadmap)
- [Roadmaps That Don't Suck](https://www.productcompass.pm/p/roadmaps)
- [Strategic Roadmapping](https://www.productcompass.pm/p/strategic-roadmap)
