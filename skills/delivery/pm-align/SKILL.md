---
name: pm-align
description: 审计已实现代码与 PMContext/AI PRD 的意图差距——定义"文档化意图"与"实现证据"，逐项比对找出 generic scanner 漏掉的意图-实现 gap，按影响分级，每 gap 给修复建议与验证方式。Use when the user asks to audit code against intent or find implementation gaps, mentions 意图实现差距、intended vs implemented、代码审计、intent audit、实现差距、gap analysis、对齐审计、文档与代码不一致、AI 生成代码审计、access control audit.
---

# /pm-align

> 你是一位意图-实现对齐审计师，正在审查已实现代码与 PMContext/AI PRD 的差距。**generic scanner 只看代码本身，看不到"本该做什么"——意图差距必须有意图模型才能发现。**

从 PMContext + AI PRD + 代码输出意图-实现差距审计。意图定义 + 实现证据 + gap 清单 + 分级 + 修复建议。

## Purpose

从 PMContext/AI PRD 与代码输出对齐审计。提炼 pm-skills/pm-ai-shipping 的 intended-vs-implemented 方法，绑定 PMSkill 的 PMContext + pm-aiprd 作为意图来源。目标：找 generic scanner 漏掉的 gap（因它无意图模型），非泛泛代码审查。

## Context

PMContext + `docs/pm-context/prd/ai-prd.md`（AI PRD 含可执行规则+验收标准）是意图来源。项目源码是实现证据。本 skill 比对两者找差距。对齐审计是 PM Thinking Loop 的交付质量门。

## Instructions

- [ ] PMContext 已读取（不存在则 STOP 提示运行 /pm-need）
- [ ] `docs/pm-context/prd/ai-prd.md` 已读取（AI PRD 规则+验收标准，不存在则提示先 /pm-aiprd）
- [ ] 项目源码已扫描（用 grep/glob 定位实现）
- [ ] "文档化意图"已提取（PRD 每条规则+验收标准+边界条件）
- [ ] "实现证据"已逐项采集（代码位置+行为）
- [ ] 每意图-实现对已比对
- [ ] gap 按影响分级（Critical/High/Medium/Low）
- [ ] 每 gap 给修复建议 + 验证方式
- [ ] 不 hand-wavy（每发现可指代码位置+意图条款）
- [ ] 产物落盘到 `docs/pm-context/align-audit.md`

## Thinking Protocol

本 Skill 承载 PM Thinking Loop 的交付质量门步骤：

| 步骤 | 本 Skill 的职责 | 产出（是否回灌 PMContext） |
|------|---------------|--------------------------|
| 质量门 | 提取意图+采集证据+比对+分级+修复 | 回灌：Critical gap 标入 PMContext 风险段 |

执行时必须依次完成上述步骤，不可跳步。步骤产出写入 `.loop/align-quality.md`。

**产出约束**：
- 意图必须有文档来源（PRD 规则/验收标准/边界条件），无文档的标 `[非文档化意图]` 不臆造
- 证据必须可指代码位置（file:line 或符号），hand-wavy 发现作废
- 分级必须基于影响（Critical=违反边界/安全；High=验收标准失败；Medium=规则未完全实现；Low=次要偏差）
- 修复建议必须具体（改哪个文件/加什么逻辑），禁"加强校验"空话

**依赖检查**：每意图有文档来源？每证据可指代码位置？分级基于影响？修复具体？

**Pre-flight Verification**（确定性审计，替代循环重试——AI 单次生成无法真循环）：依赖检查失败时，**不重试**，直接在产物顶部输出 Pre-flight 验证清单（标记每项 ✓/✗），✗ 项标 `[待确认]` + 信息缺口记录断链点 + 终止当前 Skill 并告知用户

### Step 1: 提取文档化意图

读取 `<产物目录>/pm-context.md`（先读 `## PMSkill` 块取 `产物目录`，块不存在回退默认 `docs/pm-context/`） + `<产物目录>/prd/ai-prd.md`，列出"文档化意图"清单：

| 意图ID | 类型 | 内容 | 来源 |
|---|---|---|---|
| INT-01 | 规则 | 续费前必须校验会员等级 | ai-prd.md §R3 |
| INT-02 | 验收 | 一键续费 3 秒内完成 | ai-prd.md §AC1 |
| INT-03 | 边界 | 支付失败必须回滚权益 | ai-prd.md §B2 |

类型：规则（必须做）/验收（必须达到）/边界（必须不违反）。

**意图来源层级**（每意图标注，决定 Step 3 审计深度）：

| 层级 | 定义 | 来源 | 审计策略 |
|------|------|------|---------|
| L1 显式规则 | PRD 字面写出的规则/验收/边界 | ai-prd.md §R/§AC/§B | 字面比对即可 |
| L2 隐含语义 | PRD 未字面写但语义推导得出 | PMContext 用户目标+场景反推 | 重点审——AI 生成代码最易在此偏离，字面看对但意图错 |
| L3 业务约束推导 | 行业/合规/常识推导的约束 | 业务领域知识+法规 | 必须列推导链，避免臆造意图 |

L2/L3 意图在 Step 3 比对时优先检：generic scanner 无意图模型只能比 L1，本 skill 价值即在抓 L2/L3 gap。

若 PMContext/aiprd 不存在 → **🔴 STOP**：提示先运行 `/pm-need` + `/pm-aiprd`。

### Step 2: 采集实现证据

对每意图，用 grep/glob/ast-grep 在源码定位实现：

| 意图ID | 实现位置 | 实现行为 | 匹配? |
|---|---|---|---|
| INT-01 | src/renew.js:42 checkLevel() | 续费前校验等级 | ✓ |
| INT-02 | src/renew.js:58 renew() | 未见计时/超时处理 | ✗ 缺失 |
| INT-03 | src/pay.js:30 | 支付失败未回滚权益 | ✗ 偏差 |

证据必须可指 file:line 或符号名。找不到实现的标 `[未实现]`。

### Step 3: 比对找 gap

逐意图-证据对比，列 gap：

| GapID | 意图 | 问题类型 | 描述 | 影响 |
|---|---|---|---|---|
| GAP-01 | INT-02 | 缺失 | 无 3 秒计时逻辑 | High（验收失败） |
| GAP-02 | INT-03 | 偏差 | 支付失败未回滚 | Critical（边界违反，权益错发） |

问题类型：缺失（未实现）/偏差（实现但行为不符）/多余（实现但意图无要求，标 `[冗余]`）。

**偏差细化**（AI 生成代码最常见 gap 在此）：

| 偏差子类 | 定义 | 判定 | 处置 |
|---------|------|------|------|
| 字面一致-语义偏离（L2 偏差） | 代码满足 PRD 字面规则但违反隐含语义 | 字面 ✓ + L2 意图 ✗ | 列 gap，修复 |
| 字面偏离-语义一致（可接受偏差） | 代码未字面实现但达成意图 | 字面 ✗ + L2 意图 ✓ | 标 `[偏差-可接受]`，不列 gap |
| 字面+语义双偏离 | 字面规则和意图都未达成 | 字面 ✗ + L2 ✗ | 列 gap，升级分级 |

区分关键：generic scanner 只看字面，会把"L2 偏差"误判为"实现正确"。本 skill 必须穿透字面查 L2 语义。

### Step 4: 分级

| 级别 | 定义 | 处置 |
|---|---|---|
| Critical | 违反边界/安全/数据完整性 | 立即修复，阻塞发布 |
| High | 验收标准失败 | 修复后才能发布 |
| Medium | 规则未完全实现 | 排期修复 |
| Low | 次要偏差 | backlog |

### Step 5: 修复建议 + 验证方式

每 gap：

| GapID | 修复建议（具体） | 验证方式 |
|---|---|---|
| GAP-02 | src/pay.js catch 块加 rollbackEntitlement() 调用 | 构造支付失败用例，断言权益未变更 |
| GAP-01 | renew() 加 Date.now() 计时 + 超时降级 | 集成测试：模拟慢支付，断言 3 秒降级 |

修复禁"加强校验"空话，必须指文件/逻辑。验证必须可执行（测试用例/断言）。

### Step 5.5: 审计建议实施前验证门（借鉴 superpowers/receiving-code-review "verify before implement"）

> 审计报告给出修复建议后，往往被直接当 TODO 实施。**没有验证的修复建议是猜测**——必须确认"这个修复方式在本代码库的上下文中确实有效"再实施。

**验证门检查表**（每修复建议实施前必须过）：

| 检查 | 问题 | 不过处理 |
|------|------|---------|
| 代码库一致性 | 建议改的文件是否存在？建议的函数/变量名是否代码库实际命名？ | 标 `[需代码库验证]` 不直接实施 |
| 副作用评估 | 修复是否影响其他依赖该模块的代码？ | 标 `[需副作用分析]` 加影响范围注释 |
| 测试可覆盖性 | 修复是否能被现有测试覆盖？是否需要新增测试？ | 标 `[需新增测试]` 不裸改 |
| 回滚方案 | 修复上线后出问题，回滚路径是否清晰？ | 标 `[需回滚方案]` 除非无状态变更 |

**实施纪律**：
- 不允许跨文件批量改——每次改 1 个文件，验证后再改下一个（借鉴 receiving-code-review "one item at a time, test each"）
- 每个修复实施前先过验证门，验证不达标的修复标 🟡 不实施
- 验证门不过不是放弃修复——是"先补验证再实施"

### Step 6: 写入产物

写入 `docs/pm-context/align-audit.md`，含意图清单 + 证据表 + gap 表 + 分级 + 修复建议 + 追溯列。Critical gap 回灌 PMContext 风险段。

**🔴 CHECKPOINT** — 输出产物路径 + 意图数 + gap 数（按级）+ Critical 数 + hand-wavy 作废数。等待 PM 确认或自动进入下一步（`--auto` 模式）。

## 流程链落盘

质量门步骤产出完成后，写入中间工件：
- `docs/pm-context/.loop/align-quality.md`（意图+证据+gap+修复 + 审计三元组）

## 关联增强

Critical gap 回灌 PMContext 风险段。与 pm-premortem 交叉（gap 即上线风险）。与 pm-experiment 衔接（gap 验证方式 → 测试用例）。

## 失败模式

| 触发条件 | 一线修复 | 仍失败兜底 |
|---------|---------|-----------|
| **🔴 STOP**：`docs/pm-context/pm-context.md` 不存在 | 提示先运行 `/pm-need <需求>` | 不阻塞，提示后退出 |
| **🔴 STOP**：`docs/pm-context/prd/ai-prd.md` 不存在 | 提示先运行 `/pm-aiprd` | 无意图来源无法审计 |
| 源码库空或找不到目标模块 | 提示确认代码路径 | 标 `[无法定位实现]` 该意图悬空 |
| 意图无文档来源（PM 口头要求） | 标 `[非文档化意图]` 建议补 PRD | 不臆造意图审计 |
| 证据 hand-wavy（"大概在支付模块"） | 退回定位到 file:line | 无法定位标 `[证据不足]` |
| 修复建议写"加强校验" | 改写为指文件+具体逻辑 | 仍空泛标 `[待确认]` |
| 验证方式不可执行 | 改写为测试用例/断言 | 无法执行标 `[需评估]` |

## 不要做什么（反例黑名单）

| 反模式 | 为什么不要做 |
|--------|------------|
| 审计无意图模型（纯代码扫描） | generic scanner 已做，意图差距必须有 PRD 意图 |
| hand-wavy 发现（"支付模块有问题"） | 必须指 file:line + 意图条款，否则作废 |
| 臆造无文档的意图 | 无 PRD 来源的标 `[非文档化意图]`，不编 |
| 修复建议写"加强校验" | 空话，必须指文件+具体逻辑 |
| 验证方式不可执行 | 必须测试用例/断言，"人工检查"不算 |
| gap 不分级 | 无分级无法排修复优先级，必须 Critical/High/Medium/Low |
| Critical gap 不回灌 PMContext | 不回灌等于没审计，上线风险会漏 |
| 把"多余实现"当 gap 严重对待 | 多余实现标 `[冗余]` Low 级，非 Critical |
| 审计三元组转换操作写"将 A 转换为 A'" | 同义反复，判定为 Failure |

## 产出示例 · 实战提示

会员续费对齐审计片段：

```markdown
## 文档化意图
| ID | 类型 | 内容 | 来源 |
|---|---|---|---|
| INT-03 | 边界 | 支付失败必须回滚权益 | aiprd §B2 |

## 实现证据
| 意图 | 位置 | 行为 | 匹配 |
|---|---|---|---|
| INT-03 | src/pay.js:30 catch | 仅 log 错误，未回滚 | ✗ 偏差 |

## Gap
| ID | 意图 | 类型 | 影响 |
|---|---|---|---|
| GAP-02 | INT-03 | 偏差 | Critical（权益错发） |

## 修复
- 建议：src/pay.js catch 块加 rollbackEntitlement(userId) 调用
- 验证：构造支付失败用例，断言权益未变更
```

**实战铁律**（落盘前对照）：

- **意图模型是核心**：generic scanner 无意图模型，意图差距只有 PRD 能定
- **hand-wavy 作废**：发现必须指 file:line + 意图条款，否则无效
- **分级基于影响**：边界违反=Critical，验收失败=High，规则未全=Medium
- **修复必须具体**：指文件+逻辑，"加强校验"是空话
- **验证必须可执行**：测试用例/断言，"人工检查"不算
- **Critical 回灌风险段**：不回灌上线会漏，必须入 PMContext 风险

### Further Reading

- [Intended vs Implemented (pm-ai-shipping)](https://www.productcompass.pm/p/intended-vs-implemented)
- [Auditing AI-Built Code](https://www.productcompass.pm/p/audit-ai-code)
- [Intent Models for Code Review](https://www.productcompass.pm/p/intent-models)
