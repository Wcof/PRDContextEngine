---
name: pm-stories
description: Use when the user asks for user stories or backlog items, mentions 用户故事、user story、backlog、3C、INVEST、验收标准、acceptance criteria、story point、sprint backlog.
metadata:
  internal: true
---

# /pm-stories

> 你是一位敏捷教练，正在从 PMContext 中拆解可交付的用户故事。**每条故事的"追光灯"必须照回 PMContext——没有溯源的故事=凭空创造。** 没有验收标准的用户故事，等于没有完成的定义。

从 PMContext 输出用户故事。3C 框架（Card/Conversation/Confirmation）+ INVEST 准则 + 4-6 条可测试验收标准。

## Purpose

从 PMContext 输出用户故事。故事遵循 3C 框架和 INVEST 准则，每个故事追溯到 PMContext 中的用户场景/规则/验收。验收标准可测试、可观察。

## Context

PMContext 中有用户场景定义、业务规则、验收项。本 skill 提取这些信息，拆解为可独立开发的用户故事。用户故事是 PMContext 的下游 View，是 AI PRD 用户故事段的细化形态。

## Instructions

- [ ] PMContext 已读取且非空（先读 `## PMSkill` 块取 `产物目录`，块不存在回退默认 `docs/pm-context/`，从 `<产物目录>/pm-context.md` 读；不存在则 STOP 提示运行 /pm-need）
- [ ] **stamp 互校**：若 `<产物目录>/.pmskill-setup.stamp` 存在且 `pmcontext_exists: false`，提示"stamp 显示 PMContext 未生成但文件已存在——以文件为准"
- [ ] "用户场景"维度已提取（用户角色 + 场景）
- [ ] 各页面/功能"规则"已提取（作为故事业务逻辑）
- [ ] 各页面/功能"验收"已提取（作为验收标准来源）
- [ ] 用户角色已识别（distinct user roles）
- [ ] 每个故事含 3C 三要素（Card 标题/Conversation 描述/Confirmation 验收）
- [ ] 每个故事满足 INVEST 准则
- [ ] 每个故事含 4-6 条可测试验收标准
- [ ] 故事独立可任意顺序开发
- [ ] 故事大小适合一个 sprint
- [ ] 每个故事在"来源"列标注追溯到的 PMContext 项
- [ ] 产物落盘到 `docs/pm-context/stories.md`

## Thinking Protocol

本 Skill 承载 PM Thinking Loop 的步骤 6（交付）的用户故事部分：

| 步骤 | 本 Skill 的职责 | 产出（是否回灌 PMContext） |
|------|---------------|--------------------------|
| 6. 交付（用户故事） | 从 PMContext 用户场景/规则/验收拆解为 3C+INVEST 故事 | 不回灌（产出 View） |

执行时必须依次完成上述步骤，不可跳步。步骤产出写入 `process/06-stories-delivery.md`。

**产出约束**：
- 每个故事必须对应 PMContext 中的具体项，在"来源"列标注
- 无来源的故事标 `[假设]`
- 验收标准必须可测试（有可观察行为或可验证条件）
- 故事必须满足 INVEST 六准则

**依赖检查**：是否有未追溯到 PMContext 的故事？验收标准是否可测试？故事是否满足 INVEST？

**Pre-flight Verification**（确定性审计，替代循环重试——AI 单次生成无法真循环）：依赖检查失败时，**不重试**，直接在产物顶部输出 Pre-flight 验证清单（标记每项 ✓/✗），✗ 项标 `[待确认]` + 信息缺口记录断链点 + 终止当前 Skill 并告知用户

### Step 1: 读取 PMContext 提取故事素材

读取 `<产物目录>/pm-context.md`（先读 `## PMSkill` 块取 `产物目录`，块不存在回退默认 `docs/pm-context/`），提取：
- "用户场景"维度 → 用户角色 + 场景
- 各页面/功能"规则" → 故事业务逻辑
- 各页面/功能"验收" → 验收标准来源
- "边界条件" → 异常路径验收标准

若 PMContext 不存在 → **🔴 STOP**：提示先运行 `/pm-need`。

### Step 2: 识别用户角色

从 PMContext 用户场景提取 distinct user roles：
```
角色1: 月付会员（主要用户，80%）
角色2: 年付会员（次要用户，20%）
角色3: 管理员（运营人员）
```

### Step 3: 拆解用户故事

对每个角色 × 每个功能，生成 3C 故事：

**Card（标题）**：`[功能名] - [角色] [动作]`
**Conversation（描述）**：`作为 [角色]，我想要 [动作]，以便 [价值]`
**Confirmation（验收）**：4-6 条可测试标准

### Step 4: 校验 INVEST 准则

每个故事校验：
- **I**ndependent — 可独立开发，不依赖其他故事
- **N**egotiable — 可协商，不是合同
- **V**aluable — 对用户有明确价值
- **E**stimable — 可估算工作量
- **S**mall — 适合一个 sprint
- **T**estable — 有可测试的验收标准

任一准则不满足 → 拆分或重写故事。

### Step 5: 写入产物

写入 `<产物目录>/stories.md`（默认 `docs/pm-context/stories.md`），格式：

```markdown
# 用户故事

> 来源: PMContext <需求名>
> 角色数: N | 故事数: M | [假设] 故事: L 个

## 用户角色
| 角色 | 描述 | 占比 | 来源 |
|---|---|---|---|
| 月付会员 | 主要用户 | 80% | PMContext 用户场景 |
| 年付会员 | 次要用户 | 20% | PMContext 用户场景 |

## 故事列表

### US-1: 一键续费 - 月付会员快速续费

**Card:** 一键续费 - 月付会员快速续费

**Conversation:** 作为月付会员，我想要一键续费（预填历史信息），以便不用重新填写资料快速完成续费。

**Confirmation（验收标准）:**
1. 会员到期前 7 天，会员中心展示"一键续费"入口 ← PMContext 规则: 到期提醒
2. 点击"一键续费"后预填上次支付信息（姓名/地址/支付方式），仅需确认 ← PMContext 验收
3. 若支付信息过期，提示更新而非阻断 ← PMContext 边界条件
4. 续费成功后立即激活会员权限，展示成功页 ← PMContext 验收
5. 续费失败保留当前会员状态，提示重试，不收任何费用 ← PMContext 边界条件
6. 整个续费流程 ≤ 3 次点击完成 ← PMContext [假设: 续费流程负相关, 7/10]

**INVEST 校验:** I ✓ | N ✓ | V ✓ | E ✓ | S ✓ | T ✓

**来源:** PMContext 用户场景 + 规则: 到期提醒 + 验收: 续费激活 + 边界: 支付失败

---

### US-2: ...
```

### Step 6: 与草图产物对照差分（若 sketch 已存在）

若 `<产物目录>/sketch/` 目录存在（即 pm-sketch 已先于本 skill 跑过），读取其产物清单（wireframe/ia/state/flow/prototype），在 stories.md 末尾追加"**与草图对照差分**"章节：
- 列出 stories 中有但草图无对应页面的故事 → 标 `[待确认]` 提示 PM 补 PMContext 页面定义后重跑 sketch
- 列出草图中有但 stories 无对应故事的页面 → 标 `[假设]` 提示 PM 补故事或确认该页面无独立故事价值
- 双方都没有的孤立项不列入，只列单向差分

**🔴 CHECKPOINT** — 输出产物路径 + 角色数 + 故事数 + 验收标准总数 + `[假设]` 项数 + 与草图差分项数。等待 PM 确认或自动进入下一步（`--auto` 模式）。

## 流程链落盘

步骤 6（交付）产出完成后，写入中间工件：
- `docs/pm-context/process/06-stories-delivery.md`（故事追溯映射 + 审计三元组 + 与草图差分结果）

## 关联增强

在"来源"列标注每个故事和验收标准追溯到的 PMContext 项。无来源的故事标 `[假设]`。

## 失败模式

| 触发条件 | 一线修复 | 仍失败兜底 |
|---------|---------|-----------|
| `<产物目录>/pm-context.md` 不存在 | **🔴 STOP**：输出"未找到 PMContext，先运行 `/pm-need <需求>`" | 不阻塞，提示后退出 |
| PMContext 中"用户场景"维度为空 | **🔴 STOP**：输出"用户场景未精炼，先运行 `/pm-refine`" | 不臆造用户角色 |
| 某功能在 PMContext 中无"验收"项 | 该功能故事验收标准标 `[假设]` 并提示 PM 补充 | 不阻塞，但故事顶部加 ⚠️ |
| 故事不满足 INVEST 的 Independent | 拆分为更小故事，标注依赖关系 | 仍无法独立则合并为更大故事并说明 |
| 故事不满足 INVEST 的 Small（> 1 sprint） | 拆分为多个小故事 | 仍过大则标注"epic，需进一步拆分" |
| 验收标准不可测试（如"用户体验好"） | 改写为可观察行为（如"任务完成时间 ≤ 30 秒"） | 仍不可测试则标 `[待确认]` |
| 故事无法追溯到 PMContext | 重新从 PMContext 提取素材 | 确实无依据则删除该故事，记信息缺口 |

## 不要做什么（反例黑名单）

| 反模式 | 为什么不要做 |
|--------|------------|
| 验收标准不可测试 | 不可测试等于没有完成的定义，无法判断故事是否做完 |
| 故事不满足 INVEST 任一准则 | 违反敏捷故事基本纪律，导致开发困难 |
| 故事不追溯到 PMContext | 故事与需求脱节，可能开发出不需要的功能 |
| 一个故事含多个角色 | 故事应聚焦单一角色，多角色拆分为多个故事 |
| 验收标准 < 4 条 | 验收标准不足导致"完成"边界模糊 |
| 验收标准 > 6 条 | 过多验收标准说明故事过大，应拆分 |
| 用技术语言写故事描述 | 故事用用户语言，技术细节属于 AI PRD 的实施规则 |
| 审计三元组转换操作写"将 A 转换为 A'" | 同义反复，无推理密度，判定为 Failure |
| 审计三元组转换操作写"基于上述依据产出" | 空话，未阐明具体推导逻辑，判定为 Failure |

## 产出示例 · 实战提示

会员续费用户故事示例：

```markdown
### US-1: 一键续费 - 月付会员快速续费

**Conversation:** 作为月付会员，我想要一键续费（预填历史信息），以便不用重新填写资料快速完成续费。

**Confirmation:**
1. 会员到期前 7 天展示"一键续费"入口 ← PMContext 规则
2. 点击后预填上次支付信息，仅需确认 ← PMContext 验收
3. 支付信息过期提示更新而非阻断 ← PMContext 边界条件
4. 续费成功立即激活权限 ← PMContext 验收
5. 续费失败保留当前状态，提示重试 ← PMContext 边界条件
6. 整个流程 ≤ 3 次点击 ← PMContext [假设, 7/10]
```

详见 [references/stories-example.md](references/stories-example.md)（完整用户故事集示例 + INVEST 校验对照表）。

**实战铁律**（落盘前对照）：

- **验收标准 4-6 条是甜区**：< 4 边界模糊，> 6 故事过大
- **"作为...我想要...以便..."是黄金句式**：角色 + 动作 + 价值三者缺一不可
- **验收必须可观察**：用"展示""激活""提示"等可验证动词，不用"体验好""流畅"等主观词
- **与 AI PRD 互补**：AI PRD 重实施规则，用户故事重用户价值和验收边界
- **INVEST 校验是质量门**：任一准则不满足，拆分或重写，不要硬塞

### Further Reading

- [How to Write User Stories: The Ultimate Guide](https://www.productcompass.pm/p/how-to-write-user-stories)
- [INVEST in Good User Stories](https://www.agilealliance.org/glossary/invest/)
- [3 C's of User Stories (Ron Jeffries)](https://ronjeffries.com/articles/x0023c/)
