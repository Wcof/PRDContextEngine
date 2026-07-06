# ADR 0016: Explicit Process Artifacts — 过程文件显性化

## Status

Accepted (2026-07-06).

## Context

PMSkill 的过程文档（问题重构 / 领域模型 / 决策表 / 风险清单 / 交付物追溯 / 图元追溯）此前落盘到 `docs/pm-context/.loop/`，被三重隐藏：

1. **点前缀**：`.loop/` 目录名以点开头，在文件管理器、`ls`（不带 `-a`）默认隐藏
2. **gitignore**：`.gitignore` 显式忽略 `docs/pm-context/.loop/`，不入版本库，协作时他人看不到
3. **Wipe-on-Entry 删除**：`/pm-need` 入口（非 `--incremental`）每次 `rm -rf` 整目录清空，重跑即丢历史

用户审计诉求：PM 希望**事后能直接查看过程文档**，回溯「问题怎么重构的 / 决策为什么这么选 / 风险怎么识别的」，而非依赖 PMContext 摘要 + 对话历史。三重隐藏使过程文档事实上不可审计。

## Decision

将过程文档从 `.loop/` 迁移到显性的 `docs/pm-context/process/`：

1. **显性目录**：`process/` 无点前缀，文件管理器与 `ls` 默认可见
2. **进版本库**：`.gitignore` 放行 `docs/pm-context/process/`（技术缓存 `.cache/` 与归档 `.archive/` 仍忽略）
3. **重跑归档而非删除**：`/pm-need` 入口（非 `--incremental`）改为归档逻辑——`process/` 下文件移到 `process/.archive/<timestamp>/`，保留历史供审计；技术缓存 `.cache/` 仍清空
4. **路径重命名**：按阅读顺序重命名（`collect-step1.md` → `01-collect-understand.md`，`refine-step2.md` → `02-refine-model.md` 等），索引写在 `process/README.md`
5. **产物完整性自检闸**：`/pm-need` 末尾（`--auto` 与正常模式都执行）强制体检——PMContext 必须存在且非空（Sole Entity 绝不能缺），过程文档与结果文档按链路点名，缺任一报 🔴 不得标完成

### 路径映射

| 旧路径（删除） | 新路径（写入） |
|---|---|
| `.loop/collect-step1.md` | `process/01-collect-understand.md` |
| `.loop/refine-step2/3/4.md` | `process/02-refine-model.md` / `03-refine-options.md` / `04-refine-tradeoff.md` |
| `.loop/premortem-step5.md` | `process/05-premortem-risk.md` |
| `.loop/{aiprd,humanprd,stories,...}-step6.md` | `process/06-*-delivery.md` |
| `.loop/{wireframe,ia,state,flow}-step6.md` | `process/06-sketch-*.md` |
| `.loop/conflict-log.json` | `process/conflict-log.json`（进版本库） |
| `.loop/nodeN-*.json` | `.cache/nodeN-*.json`（技术缓存，不进版本库） |

## Trade-offs

| 取 | 舍 |
|----|----|
| **可审计性**：PM 可直接查看过程文档，协作时他人能看到 | **版本库体积**：过程文档进版本库，每次重跑新增一组文件（旧版归档不进库） |
| **历史保留**：重跑归档而非删除，可对比多轮推断 | **目录杂乱**：`process/` 下文件增多（用编号前缀保阅读顺序） |
| **完整性闸**：防 PMContext 缺失静默完成 | **执行成本**：每轮末尾多一次体检（成本可忽略） |

取舍倾向：**选可审计性**。过程文档本就是为审计而生，三重隐藏违背其设计初衷。版本库体积增量小（Markdown 文本），且归档不进库。

## Consequences

- 每个 SKILL.md 的「流程链落盘」段路径需同步更新（已完成）
- `/pm-need` 的 Wipe-on-Entry 逻辑改为归档（已完成）
- `.gitignore` 放行 `process/`、忽略 `.cache/` 与 `.archive/`（已完成）
- README / CONTEXT 产物目录树补 `process/` + `.cache/`（已完成）
- evals 补测：`process/` 下生成全部过程文档、完整性体检块、`.loop/` 不再被写入（已完成）

## Relationships

- **推翻** ADR 0008 中「`.loop/` 隐藏 + gitignore + Wipe-on-Entry 删除」部分（第 25 行双层注入模型表格的「流程层」行、第 10 节 GC 策略）。ADR 0008 的其余部分（心智链 6 步、双层注入模型、审计三元组、自愈机制）不变。
- **承接** ADR 0004（PMContext Sole Entity）：完整性自检闸强制 PMContext 存在且非空，是 Sole Entity 的硬保。
- **承接** ADR 0005（Explicit Markers）：过程文档中的 `[待确认]` `[假设]` `[冲突]` 标记沿用 ADR 0005 的显式标记体系。

## References

- ADR 0004: PMContext Sole Entity
- ADR 0005: Explicit Markers Replace Soft Gate
- ADR 0008: Loop Internalization（本决议推翻其 `.loop/` 隐藏 + Wipe 删除部分）
- 用户审计诉求（2026-07-06）：过程文档三重隐藏不可审计
