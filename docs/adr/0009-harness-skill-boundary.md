# ADR 0009: Harness / Skill 边界——控制层职责不由 SKILL.md 承载

> 注：原 0009 编号曾用于 refine 双执行模式（已重命名为 0009-refine-dual-execution-modes）。本 ADR 重新启用 0009 编号记录 Harness/Skill 边界决议，二者并存于 `docs/adr/` 下，文件名互不冲突。

## Status

Accepted (2026-07-04).

## Context

PMSkill 此前在 SKILL.md / 约定文件里反复堆叠"运行时控制层"语义——分片冻结、差分持久化、CoT flush、双通道置顶（Pinned-Sliding）、会话 fork 隔离等。这些本质是 **Harness 控制层**职责，但被写进 Markdown 后既无法被运行时强制执行，又使 SKILL.md 日益臃肿、维护成本上升、且与"PMContext 是唯一 Entity / SKILL.md 只描述领域动作"的既有契约（ADR 0004 / ADR 0008）相冲突。

需要一个明确边界：哪些是 Harness 控制层职责（运行时保证），哪些是 PMSkill 配合契约（写进 Markdown 即可）。

## Decision

划定边界如下：

| 职责 | 归属 | 落地形式 |
|------|------|---------|
| **冻结 / 差分持久化**（分片一经落盘即 Frozen，仅 conflict-resolver 可差分） | Harness 控制层 | 运行时强制；PMSkill 只在 `.atomcode.md` 声明 Frozen 契约供运行时读取 |
| **CoT flush**（推理过程不写入 PMContext，仅结构化分片落盘） | Harness 控制层 | 运行时在 flush 边界剥离 CoT；PMSkill 只在 `.atomcode.md` 声明"CoT 不写入 PMContext" |
| **双通道 Pinned-Sliding**（PINNED.md 置顶常驻 + SKILL.md 滑动加载） | Harness 控制层 | 运行时负责双通道调度；PMSkill 只提供 PINNED.md 文件 + SKILL.md 顶部指针 |
| **会话 fork 隔离**（局部退火时 fork 子上下文，不污染主上下文） | Harness 控制层 | 运行时实现；PMSkill 只在 pm-conflict-resolver 声明"仅读局部上下文"契约 |

**PMSkill 只提供配合契约**：
- 结构化分片（每节点产出可独立序列化的 JSON/Markdown）
- 自包含输入（pm-conflict-resolver 只接收 error 上下文 + 上游节点 JSON，不读全局 PMContext）
- PINNED.md（≤10 行核心约束，供运行时置顶加载）

**禁止后续把上述控制层逻辑硬塞进 Markdown**——凡涉及"如何冻结、如何 flush、如何双通道调度、如何 fork 会话"的实现细节，一律不得写入 SKILL.md / 约定 / ADR，以防再次臃肿。控制层能否严格执行交给运行时，PMSkill 不为"强制执行"去写运行时代码。

## Consequences

**正向**：
- SKILL.md 回归"领域动作描述"本职，体积可控
- 控制层语义集中归属运行时，单一职责，可独立演进
- PMSkill 与 Harness 解耦，可在不同运行时上复用同一套 Skill 协议

**负向**：
- 若运行时未实现上述控制层，PMSkill 的 Frozen / CoT 剥离 / 双通道置顶仅停留在"约定"层面，依赖运行时自觉遵守
- PINNED.md 与 SKILL.md 双源，需保证二者不漂移（PINNED.md 是 SKILL.md 核心约束的子集）

## References

- ADR 0004: PMContext Sole Entity
- ADR 0008: PM Thinking Loop Internalization（心智链不落盘、流程链落盘 `.loop/`）
- `.atomcode.md` — 结构化分片 + Frozen 契约
- `skills/*/PINNED.md` — 双通道置顶契约
- `skills/utility/pm-conflict-resolver/SKILL.md` — 自包含输入 + 局部退火契约
