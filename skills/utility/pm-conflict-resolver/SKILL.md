---
name: pm-conflict-resolver
description: 局部退火——某节点报错时只对「报错上下文 + 其依赖的上游节点 JSON」做最小差分修复，不重写全局 PMContext。Use when a downstream node fails and needs局部回退, or the user mentions 局部退火、冲突解决、partial backtracking、节点报错、局部修复.
metadata:
  internal: true
---

# /pm-conflict-resolver

> 核心约束见 PINNED.md（供运行时置顶加载）

## Purpose

下游节点失败时，用最低代价做局部修复，避免全链路重跑。

## Context

auto 模式下各节点产出独立落盘为 `.cache/nodeN-*.json` 分片（Frozen）。当某节点报错，传统做法是回到 `/pm-need` 起点重跑全链路——代价高且会覆盖已 Frozen 的健康分片。本 skill 只对报错节点 + 其依赖的上游节点 JSON 做最小差分修复，其余分片保持 Frozen。

## Instructions

1. 🔴 输入契约（严格限定，禁止越界）：仅接收两项——
   - 报错节点的 error 上下文
   - 该节点依赖的上游节点 JSON（如 node2-domain.json）
   - 禁止读取全局 `docs/pm-context/pm-context.md`
2. 只在这两个局部上下文内做微调，输出「最小差分（diff）」而非重写。
3. 差分写入 `docs/pm-context/process/conflict-log.json`，记录：受影响字段 / 修改前后值 / 受影响下游节点清单。
4. 修完只提示重跑「受影响下游集合」，其余分片保持 Frozen。

### `.cache/` 分片结构（技术缓存，不进版本库；conflict-log.json 落 `process/` 进版本库）

| 分片 | 产出节点 | 内容 |
|------|---------|------|
| `node2-domain.json` | pm-refine 步骤 2（建模） | 领域模型片段（实体/关系/不变量） |
| `node3-prd.json` | pm-prd | PRD 规则与验收（可执行片段） |
| `node5-tech.json` | pm-sketch / 技术约束节点 | 技术约束与资源约束 |
| `conflict-log.json`（落 `process/`） | 本 skill | 差分修复日志（受影响字段/前后值/受影响下游） |

> 分片一经落盘即 Frozen（见 `.atomcode.md` 约定），仅本 skill 可对其做差分修改。

## Thinking Protocol

| 步骤 | 本 Skill 的职责 | 产出 |
|------|---------------|------|
| 1. 定位 | 从 error 上下文定位报错字段 + 依赖的上游分片 | 受影响字段清单 |
| 2. 差分 | 在局部上下文内产出最小 diff（before→after） | diff 对象 |
| 3. 波及检测 | 判定 diff 是否波及 >1 个上游节点 | 波及判定 |
| 4. 落盘 | 写入 conflict-log.json + 提示重跑受影响下游 | 日志条目 + 重跑清单 |

## 关联增强

diff 必须显式声明受影响下游节点清单，确保重跑集合可被编排器直接消费，不漏跑。

## 失败模式

| 触发条件 | 动作 |
|---|---|
| 上游 JSON 缺失 | 🔴 STOP：提示先跑对应上游节点，不臆造 |
| 修改会波及 >1 个上游节点 | 🔴 标 `[冲突]` 交 PM 裁决，不自作主张扩大改动面 |
| error 上下文不足以定位字段 | 🔴 STOP：提示补充报错节点的具体字段与错误信息 |
| diff 写入 conflict-log.json 失败 | 🟡 提示日志落盘失败，diff 仍以对话形式输出供 PM 手动记录 |

## 禁止做什么

- 禁止把全局 PMContext 拉进上下文
- 禁止重写未报错的节点分片
- 禁止为"一次性修干净"而扩大改动面到多个上游
- 禁止臆造上游 JSON 中不存在的字段或状态

## 产出示例

详见 [references/conflict-example.md](references/conflict-example.md)。

### Further Reading

- ADR 0009: Harness/Skill 边界（会话 fork 隔离属控制层职责）
- `.atomcode.md` — 节点分片 Frozen 契约
