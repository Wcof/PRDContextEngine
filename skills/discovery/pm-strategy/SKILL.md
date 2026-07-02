---
name: pm-strategy
description: 从 PMContext 生成战略分析套件——按"现状→行业→增长→商业模式"四阶选择 SWOT（现状定位）/Porter 五力（行业吸引力）/Ansoff 矩阵（增长路径）/Lean Canvas（商业模式假设）组合或全套，每框架产出追溯到 PMContext 的结构化表 + 行动建议。Use when the user asks for strategy analysis or business model, mentions 战略分析、SWOT、波特五力、Porter、Ansoff 矩阵、Lean Canvas、商业模式画布、BMC、战略定位、competitive analysis、industry analysis、growth strategy、business model.
---

# /pm-strategy

> 你是一位产品战略分析师，正从 PMContext 构建战略分析。**SWOT 五力的"追光灯"必须照回 PMContext 的用户场景/竞品/边界条件——没有 PMContext 依据的战略判断是 PPT 装饰。**

从 PMContext 输出战略分析套件。按需求选择 1-4 个框架组合，每框架产出结构化表 + 行动建议 + 追溯标记。

## Purpose

从 PMContext 输出战略分析。把分散的战略框架（SWOT/Porter/Ansoff/Lean Canvas/BMC）收敛为单一 skill，按"现状定位→行业吸引力→增长路径→商业模式假设"四阶递进，避免 PM 在多个框架间手工拼接。每个判断追溯到 PMContext，杜绝凭空 SWOT。

## Context

PMContext 中有竞品/市场、用户场景、边界条件、价值验证度量。本 skill 提取这些信息构建战略分析。战略分析是 PMContext 的下游 View，和 PRD/OST 平级，用于决策评审与立项依据。

## Instructions

- [ ] PMContext 已读取且非空（不存在则 STOP 提示运行 /pm-need）
- [ ] "竞品/市场"维度已提取（SWOT 机会威胁 / Porter 五力来源）
- [ ] "用户场景"+"现状平替与摩擦力"已提取（Lean Canvas Problem / SWOT 优势来源）
- [ ] "边界条件"已提取（Ansoff 增长约束 / Porter 进入壁垒）
- [ ] "价值验证度量"已提取（Lean Canvas Metrics / 战略成功标准）
- [ ] 已确认分析范围：单框架 / 组合 / 全套（默认全套）
- [ ] 每框架产出结构化表 + Top 3 行动建议
- [ ] 每条判断在"来源"列标注追溯到的 PMContext 项，无依据标 `[假设]`
- [ ] 产物落盘到 `docs/pm-context/strategy.md`

## Thinking Protocol

本 Skill 承载 PM Thinking Loop 的步骤 1-2（理解/建模）的战略分析部分：

| 步骤 | 本 Skill 的职责 | 产出（是否回灌 PMContext） |
|------|---------------|--------------------------|
| 1. 理解 | 从 PMContext 竞品/市场/边界条件提取战略素材 | 不回灌（产出 View） |
| 2. 建模 | 套用战略框架结构化判断 + 行动建议 | 不回灌（产出 View） |

执行时必须依次完成上述步骤，不可跳步。步骤产出写入 `.loop/strategy-step1.md`、`.loop/strategy-step2.md`。

**产出约束**：
- 每条判断必须追溯到 PMContext 项，凭空判断标 `[假设]` 并提示先运行 /pm-collect 补竞品数据
- 框架之间必须交叉验证（SWOT 的机会应与 Ansoff 增长路径一致，不一致标冲突）
- 行动建议必须可执行（含"做什么/谁/何时度量"），禁"加强/提升/优化"等空话

**依赖检查**：每条判断是否有来源？框架间是否冲突？行动建议是否可执行？

**自愈机制**：依赖检查失败时，在隐式思考空间内回溯重生成当前步骤产出（最多 3 轮），超限降级为标 `[待确认]` + 信息缺口记录断链点 + 终止当前 Skill 并告知用户

### Step 1: 读取 PMContext 提取战略素材

读取 `docs/pm-context/pm-context.md`，提取：
- "竞品/市场" → SWOT O/T、Porter 五力、Ansoff 新市场判断
- "用户场景"+"现状平替与摩擦力" → SWOT S/W、Lean Canvas Problem、Porter 替代品
- "边界条件" → Porter 进入壁垒、Ansoff 约束、Lean Canvas Unfair Advantage
- "价值验证度量" → Lean Canvas Metrics、战略成功标准

若 PMContext 不存在 → **🔴 STOP**：提示先运行 `/pm-need`。

### Step 2: 确认分析范围

询问 PM（或按参数）：
- `--swot` 仅现状定位
- `--porter` 仅行业吸引力
- `--ansoff` 仅增长路径
- `--lean` 仅商业模式假设
- 无参数 → 默认全套四阶递进

`--auto` 模式跳过询问，直接全套。

### Step 3: SWOT 现状定位

| 维度 | 判断 | 来源 |
|---|---|---|
| Strengths | <内部优势> | PMContext <项> |
| Weaknesses | <内部劣势> | PMContext <项> |
| Opportunities | <外部机会> | PMContext 竞品/市场 |
| Threats | <外部威胁> | PMContext 竞品/市场 |

**Top 3 行动**：SO（用优势抓机会）/ WT（补劣势防威胁）/ ST（用优势防威胁）各 ≥1 条。

### Step 4: Porter 五力行业吸引力

| 力量 | 强度（高/中/低） | 判断依据 | 来源 |
|---|---|---|---|
| 现有竞争者竞争 | <强度> | <依据> | PMContext <项> |
| 供应商议价力 | <强度> | <依据> | PMContext 边界条件 |
| 买方议价力 | <强度> | <依据> | PMContext 用户场景 |
| 新进入者威胁 | <强度> | <依据> | PMContext 边界条件 |
| 替代品威胁 | <强度> | <依据> | PMContext 现状平替 |

**行业吸引力结论**：高（≤2 力高强度）/中（3 力）/低（≥4 力高强度）。

### Step 5: Ansoff 矩阵增长路径

|  | 当前市场 | 新市场 |
|---|---|---|
| **当前产品** | 市场渗透：<策略> | 市场开发：<策略> |
| **新产品** | 产品开发：<策略> | 多元化：<策略> |

标注每象限风险等级（低/中/高）+ 推荐路径（基于 PMContext 价值验证度量与资源约束）。

### Step 6: Lean Canvas 商业模式假设

九宫格，每格追溯到 PMContext：
- Problem（Top 3 问题）← PMContext 摩擦力
- Solution（Top 3 方案）← PMContext 用户场景
- UVP ← PMContext 价值验证度量
- Unfair Advantage ← PMContext 边界条件
- Customer Segments ← PMContext 用户场景
- Channels ← PMContext [假设]（无则标待确认）
- Revenue Streams ← PMContext [假设]
- Cost Structure ← PMContext 边界条件
- Key Metrics ← PMContext 价值验证度量

### Step 7: 框架交叉验证 + 写入产物

检查：
- SWOT 机会 ⊆ Ansoff 推荐路径？冲突则标 `[冲突]` 并提示 PM 裁决
- Porter 威胁高 → Ansoff 该象限风险升级
- Lean Canvas Problem ⊇ SWOT Weaknesses 面向客户的部分

写入 `docs/pm-context/strategy.md`，含四框架表 + Top 3 行动 + 交叉验证结论 + 追溯列。

**🔴 CHECKPOINT** — 输出产物路径 + 四框架完成度 + 交叉验证冲突数 + `[假设]` 项数。等待 PM 确认或自动进入下一步（`--auto` 模式）。

## 流程链落盘

步骤 1-2 产出完成后，写入中间工件：
- `docs/pm-context/.loop/strategy-step1.md`（战略素材提取 + 审计三元组）
- `docs/pm-context/.loop/strategy-step2.md`（四框架结构化 + 行动建议 + 审计三元组）

## 关联增强

在"来源"列标注每条判断追溯到的 PMContext 项。无来源的标 `[假设]`。框架间冲突显式标注。

## 失败模式

| 触发条件 | 一线修复 | 仍失败兜底 |
|---------|---------|-----------|
| `docs/pm-context/pm-context.md` 不存在 | **🔴 STOP**：输出"未找到 PMContext，先运行 `/pm-need <需求>`" | 不阻塞，提示后退出 |
| PMContext "竞品/市场"维度为空 | **🔴 STOP**：输出"无竞品数据，先运行 `/pm-collect` 补竞品扫描" | SWOT/Porter 标 `[假设]` 降级输出，不臆造竞品 |
| 某框架判断无 PMContext 依据 | 标 `[假设]` 并在产物头部汇总假设数 | 假设占比 > 40% → 提示数据不足，建议先 /pm-collect |
| 框架间冲突（SWOT 机会 ∉ Ansoff 路径） | 标 `[冲突]` 列出两边依据让 PM 裁决 | 不静默合并，保留冲突显式化 |
| 行动建议写成"加强/提升/优化" | 改写为"做什么/谁/何时度量"三要素 | 仍不可执行则标 `[待确认]` 让 PM 细化 |
| Porter 某力量数据缺失 | 从 PMContext 现状平替/边界条件推断 | 完全无依据则标强度"未知"不强行打分 |

## 不要做什么（反例黑名单）

| 反模式 | 为什么不要做 |
|--------|------------|
| 凭空 SWOT 不追溯 PMContext | 没依据的 SWOT 是 PPT 装饰，决策时无人信 |
| 四框架各自为政不做交叉验证 | 框架间冲突是战略矛盾信号，掩盖它等于埋雷 |
| Porter 五力全打"中等"和稀泥 | 五力价值在区分强度，全中等等于没分析 |
| Ansoff 推荐多元化（最高风险象限）却不标风险 | 多元化是 Ansoff 最危险路径，必须标高风险 + 退出条件 |
| Lean Canvas Unfair Advantage 写"团队经验" | 不是 unfair advantage（竞争对手也能招人），必须是难复制的壁垒 |
| 行动建议写"加强/提升/优化" | 不可执行，无度量无责任人不叫行动 |
| 跳过 Step 1 直接套框架 | 没素材的框架是填空游戏，必须先提取再套用 |
| 审计三元组转换操作写"将 A 转换为 A'" | 同义反复，无推理密度，判定为 Failure（ADR 0008 §11） |

## 产出示例

会员产品战略分析片段：

```markdown
## SWOT
| 维度 | 判断 | 来源 |
|---|---|---|
| S | 30 万存量付费会员基础 | PMContext 用户场景 |
| W | 续费流程 5 步流失率高 | PMContext 摩擦力 |
| O | 会员权益整合第三方服务 | PMContext 竞品空白 |
| T | 平台型竞品捆绑免费会员 | PMContext 竞品/市场 |

**Top 3 行动**：
1. SO：用存量会员基础推权益整合，Q3 接入 ≥2 第三方服务，度量权益使用率
2. WT：续费流程改 2 步，2 周内上线 A/B，度量完成率 40%→65%
3. ST：存量会员忠诚度计划防平台竞品挖角，度量 6 月留存

## 交叉验证
- SWOT 机会"权益整合" ⊆ Ansoff 产品开发（当前市场+新产品）✓ 一致
- Porter 替代品威胁"高" → Ansoff 市场开发风险升级为高
- Lean Canvas Problem Top1"续费太麻烦" ⊇ SWOT W"续费流失" ✓ 一致
```

### Further Reading

- [SWOT to Strategy: Closing the Gap](https://www.productcompass.pm/p/swot-to-strategy)
- [Porter's Five Forces in Practice](https://www.productcompass.pm/p/porters-five-forces)
- [Lean Canvas vs Business Model Canvas](https://www.productcompass.pm/p/lean-canvas-vs-bmc)

### 实战提示

- **追溯优先于框架**：没 PMContext 依据的判断标 `[假设]`，不靠框架补数据
- **交叉验证是核心价值**：四框架收敛到单一 skill 的意义就在交叉验证冲突
- **Unfair Advantage 必须难复制**：团队/经验/努力都不是，专利/网络效应/数据壁垒才是
- **行动三要素**：做什么 + 谁 + 何时度量，缺一不可
