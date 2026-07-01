# 并行 Agent 分派完整示例

## 场景

PM 需同时调研 3 个竞品 + 生成 4 类草图，共 7 个独立任务。

## 任务识别 + 独立性校验

| 任务 | 输入 | 输出 | 共享可变状态? |
|------|------|------|-------------|
| 调研竞品 X | PMContext 竞品层 | battlecard-x.md | 无（只读 PMContext） |
| 调研竞品 Y | PMContext 竞品层 | battlecard-y.md | 无 |
| 调研竞品 Z | PMContext 竞品层 | battlecard-z.md | 无 |
| 生成线框图 | PMContext 用户场景 | wireframe.md | 无 |
| 生成流程图 | PMContext 用户场景 | flowchart.md | 无 |
| 生成状态图 | PMContext 用户场景 | state.md | 无 |
| 生成 ER 图 | PMContext 数据模型 | er.md | 无 |

独立性 ✅（所有任务只读 PMContext，无共享可变状态）→ 可并行。

## 分派子 agent

| 子 agent | 任务 | skill 调用 | 输出 |
|---------|------|-----------|------|
| agent-1 | 调研竞品 X | `/pm-battlecard --competitor X` | battlecard-x.md |
| agent-2 | 调研竞品 Y | `/pm-battlecard --competitor Y` | battlecard-y.md |
| agent-3 | 调研竞品 Z | `/pm-battlecard --competitor Z` | battlecard-z.md |
| agent-4 | 生成线框图 | `/pm-sketch --type wireframe` | wireframe.md |
| agent-5 | 生成流程图 | `/pm-sketch --type flowchart` | flowchart.md |
| agent-6 | 生成状态图 | `/pm-sketch --type state` | state.md |
| agent-7 | 生成 ER 图 | `/pm-sketch --type er` | er.md |

## 结果合并 + 冲突标注

| 子 agent | 状态 | 输出 |
|---------|------|------|
| agent-1 | ✅ | battlecard-x.md |
| agent-2 | ✅ | battlecard-y.md |
| agent-3 | 🟡 超时 | 标 [待确认] |
| agent-4 | ✅ | wireframe.md |
| agent-5 | ✅ | flowchart.md |
| agent-6 | ✅ | state.md |
| agent-7 | ✅ | er.md |

- 成功：6/7
- 失败/超时：1/7（agent-3 隔离，不阻塞其他）
- 冲突：0（各输出独立文件无重叠）

## 审计三元组

`<依据集: [7 个独立任务，PMContext 竞品层+用户场景只读]> → [工具: /pm-parallel, 规则: 独立性校验+子 agent 调度] → [转换: 从任务列表校验独立性后分派子 agent，多对多实体映射：任务→子 agent→输出文件] → <产出: 6 成功+1 超时标 [待确认]+0 冲突>`
