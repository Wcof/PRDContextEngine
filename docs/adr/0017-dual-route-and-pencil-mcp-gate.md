# ADR 0017: 双线路入口与 Pencil MCP 原型门

日期：2026-07-08

## 背景

PMSkill 同时存在两条运行线路：

1. **自动化链路**：`/pm-need --auto` 编排 collect → refine → premortem → PRD → stories → sketch。
2. **单 skill 调用**：PM 直接运行 `/pm-prd`、`/pm-premortem`、`/pm-sketch`、`/pm-summary` 读取既有 PMContext/产物做增量交付。

原文档将「斜杠菜单可见」与「仅人类触发」混用，导致 `pm-prd` / `pm-sketch` 这类既可见又可被编排的入口在约束上漂移。另一个新增诉求是：`pm-sketch --prototype` 在 runtime 提供 Pencil MCP 时，应优先通过 Pencil MCP 实现原型系统；未提供或不可用时，才走原有 Simple/Scaffold 本地技术栈。

## 决定

1. 将可见入口拆为两类：
   - **Human-only Entry**：可见且 `disable-model-invocation: true`，当前为 `pm-setup` / `pm-need`。
   - **Hybrid Entry**：可见但可被模型编排调用，当前为 `pm-prd` / `pm-premortem` / `pm-sketch` / `pm-summary`。
2. 插件清单必须包含 6 个可见入口，并与 `CONTEXT.md`、README、frontmatter 一致。
3. `/pm-need --auto` 调 `/pm-sketch` 时必须传 `--no-fallback`，防止 sketch 缺 PMContext 时回链 need 形成递归。
4. `pm-sketch --prototype` 新增 **Step -0.75 Pencil MCP 实现门**：
   - 检测到可用 Pencil MCP 且具备 create/update/export/persist 能力 → 使用 Pencil MCP 生成/更新原型系统，并写 `sketch/pencil/pencil-prototype-manifest.json`。
   - 未检测到、用户显式 `--no-mcp`、MCP 不具备持久化能力或调用失败 → 继续原有 Step -0.5 技术栈硬门与 Step -1 Simple/Scaffold 判断。
5. 新增 `scripts/validate_pmskill.py` 作为确定性漂移检查，覆盖 skill 数量、可见入口清单、插件清单、frontmatter 重复 key、自动化链路和 Pencil MCP 门。

## 结果

- 「可见」和「可被编排」从一个二值概念改为三类入口，减少 Agent 对调用边界的误读。
- Pencil MCP 成为原型实现优先通道，但不会破坏原有技术栈 fallback。
- 约束不只写在自然语言里，还通过 CI 可运行的验证脚本防回归。
