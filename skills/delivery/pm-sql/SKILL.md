---
name: pm-sql
description: 从 PMContext 与自然语言问题生成多方言 SQL 查询——schema 读取 + 业务问题转查询逻辑 + 方言适配（BigQuery/PostgreSQL/MySQL/Snowflake）+ 性能优化建议 + 结果验证脚本，每查询附 PMContext 度量定义追溯。Use when the user asks for SQL query or data report, mentions SQL、查询、query、数据库、database、BigQuery、PostgreSQL、MySQL、Snowflake、数据报表、data report、业务问题转查询、natural language to SQL.
---

# /pm-sql

> 你是一位数据工程师。摆在你面前的是 PM 的业务问题——"上个月高价值用户的留存怎么样"。你的任务是把这句话翻译成一条能跑、跑得快、结果对的 SQL，而不是写一条语法对但逻辑错的查询糊弄。

从 PMContext 与自然语言问题生成多方言 SQL 查询。读 schema → 转查询逻辑 → 适配方言 → 优化 → 给验证脚本。

## Purpose

把 PM 的自然语言业务问题翻译成生产可用的 SQL。pm-skills 的 sql-queries 收敛进 PMSkill 体系：从 PMContext 度量定义对齐查询指标口径，结论追溯 PMContext，避免"SQL 跑通了但口径错"。

## Context

PMContext 中"价值验证度量"定义了核心指标的计算口径（如"活跃用户=7 日内 ≥3 次会话"）；"用户场景"定义了人群筛选条件；"全局约束"可能定义了数据时间范围。本 skill 提取这些信息确保 SQL 口径对齐 PMContext。SQL 查询是 PMContext 的下游 View。

## Instructions

- [ ] PMContext 已读取且非空（不存在则 STOP 提示运行 /pm-need）
- [ ] "价值验证度量"已提取（指标计算口径来源）
- [ ] "用户场景"已提取（人群筛选条件来源）
- [ ] schema 已读取（用户提供 SQL/文档/图描述）
- [ ] SQL 方言已确认（BigQuery/PostgreSQL/MySQL/Snowflake/SQL Server）
- [ ] 查询逻辑已用自然语言解释（先讲逻辑再写 SQL）
- [ ] SQL 已生成且含注释
- [ ] 性能优化建议已给出（索引/分区/物化视图）
- [ ] 验证脚本已给出（测试查询/样本数据）
- [ ] 每查询在"来源"列标注追溯到的 PMContext 度量定义
- [ ] 产物落盘到 `docs/pm-context/sql/<query-name>.sql`

## Thinking Protocol

本 Skill 承载 PM Thinking Loop 的步骤 2（建模）+ 步骤 6（交付）的查询生成部分：

| 步骤 | 本 Skill 的职责 | 产出（是否回灌 PMContext） |
|------|---------------|--------------------------|
| 2. 建模 | 业务问题→查询逻辑映射 + schema 实体关系建模 | 不回灌（产出 View） |
| 6. 交付 | 生产可用 SQL + 验证脚本 | 不回灌（产出 View） |

执行时必须依次完成上述步骤，不可跳步。步骤产出写入 `.loop/sql-step2.md`、`.loop/sql-step6.md`。

**产出约束**：
- 查询逻辑必须先用自然语言解释（"先算 X，再 join Y，最后按 Z 聚合"），禁直接甩 SQL
- 指标口径必须对齐 PMContext 价值验证度量定义，不一致则标 `[冲突]`
- SQL 必须含注释说明复杂逻辑（窗口函数/CTE/子查询）
- 性能建议必须针对大表给索引/分区/物化视图方案

**依赖检查**：指标口径是否对齐 PMContext？方言是否确认？逻辑是否用自然语言解释？

**Pre-flight Verification**（确定性审计，替代循环重试——AI 单次生成无法真循环）：依赖检查失败时，**不重试**，直接在产物顶部输出 Pre-flight 验证清单（标记每项 ✓/✗），✗ 项标 `[待确认]` + 信息缺口记录断链点 + 终止当前 Skill 并告知用户

### Step 1: 读取 PMContext 提取查询素材

读取 `docs/pm-context/pm-context.md`，提取：
- "价值验证度量" → 指标计算口径（如"活跃=7 日内 ≥3 会话"）
- "用户场景" → 人群筛选条件
- "全局约束" → 数据时间范围/分区约束

若 PMContext 不存在 → **🔴 STOP**：提示先运行 `/pm-need`。

### Step 2: 读 schema

从用户提供的 schema 文件（SQL/文档/图描述）提取：
- 表名 + 列定义 + 数据类型
- 主键 + 外键 + 关系
- 索引/分区策略（如有）

若用户未提供 schema → 提示用户提供，不臆造表结构。

### Step 3: 业务问题→查询逻辑

用自然语言解释查询逻辑（先讲逻辑再写 SQL）：

```
业务问题：上个月高价值用户的留存
查询逻辑：
1. 定义"高价值用户"：PMContext 度量口径 = 月消费 ≥ ¥200 的付费用户
2. 定义"留存"：PMContext 度量口径 = 次月仍有 ≥1 次会话
3. 筛选上月高价值用户 → left join 本月会话表 → 留存率 = 有会话的人数 / 高价值用户总数
```

### Step 4: 生成 SQL（方言适配）

按确认的方言生成 SQL，含注释：

```sql
-- 方言：PostgreSQL
-- 指标口径：PMContext 价值验证度量"高价值用户=月消费≥¥200"（来源：PMContext）
-- 留存口径：PMContext 价值验证度量"留存=次月≥1会话"（来源：PMContext）
WITH high_value_users AS (
  -- 上月（2026-06）高价值用户
  SELECT user_id
  FROM payments
  WHERE payment_date >= '2026-06-01'
    AND payment_date < '2026-07-01'
  GROUP BY user_id
  HAVING SUM(amount) >= 200
),
retained_users AS (
  -- 本月（2026-07）有会话的高价值用户
  SELECT DISTINCT h.user_id
  FROM high_value_users h
  JOIN sessions s ON s.user_id = h.user_id
  WHERE s.session_date >= '2026-07-01'
    AND s.session_date < '2026-08-01'
)
-- 留存率
SELECT
  COUNT(DISTINCT h.user_id) AS high_value_total,
  COUNT(DISTINCT r.user_id) AS retained,
  ROUND(COUNT(DISTINCT r.user_id)::numeric / COUNT(DISTINCT h.user_id) * 100, 2) AS retention_rate_pct
FROM high_value_users h
LEFT JOIN retained_users r ON r.user_id = h.user_id;
```

### Step 5: 性能优化建议

| 优化项 | 建议 | 适用条件 |
|--------|------|---------|
| 索引 | `payments(user_id, payment_date)` 复合索引 | 大表查询 |
| 分区 | `sessions` 按 `session_date` 月分区 | 时间范围查询 |
| 物化视图 | 预聚合"高价值用户"日表 | 高频查询 |

### Step 6: 验证脚本

给测试查询验证结果正确性：

```sql
-- 验证：高价值用户总数应 > 0
SELECT COUNT(*) FROM high_value_users;
-- 验证：留存率应在 0-100% 之间
-- 验证：抽样 10 个高价值用户核对消费额
SELECT user_id, SUM(amount) FROM payments
WHERE payment_date >= '2026-06-01' AND payment_date < '2026-07-01'
GROUP BY user_id ORDER BY SUM(amount) DESC LIMIT 10;
```

### Step 7: 写入产物

写入 `docs/pm-context/sql/<query-name>.sql`，含查询逻辑说明 + SQL + 性能建议 + 验证脚本 + 追溯注释。

**🔴 CHECKPOINT** — 输出产物路径 + 方言 + 查询逻辑摘要 + 指标口径对齐状态。等待 PM 确认或自动进入下一步（`--auto` 模式）。

## 流程链落盘

步骤 2、6 产出完成后，写入中间工件：
- `docs/pm-context/.loop/sql-step2.md`（schema 建模+查询逻辑 + 审计三元组）
- `docs/pm-context/.loop/sql-step6.md`（SQL+验证脚本 + 审计三元组）

## 关联增强

在追溯注释标注每指标口径追溯到的 PMContext 度量定义。SQL 查询结果与 pm-cohort/pm-abtest 联动（为队列分析/实验分析提供数据查询）。

## 失败模式

| 触发条件 | 一线修复 | 仍失败兜底 |
|---------|---------|-----------|
| `docs/pm-context/pm-context.md` 不存在 | **🔴 STOP**：输出"未找到 PMContext，先运行 `/pm-need <需求>`" | 不阻塞，提示后退出 |
| PMContext "价值验证度量"为空 | 标 `[待确认]` 指标口径，提示 PM 补度量定义 | 不臆造口径 |
| 用户未提供 schema | **🔴 STOP**：输出"无 schema 无法生成 SQL，请提供表结构" | 不臆造表结构 |
| 方言未指定 | 默认 PostgreSQL，提示 PM 确认 | 标 `[假设]` 方言 |
| 指标口径与 PMContext 冲突 | 标 `[冲突]` 在注释中标注两版口径 | 不静默采用任一版 |
| 查询逻辑无法用 schema 实现 | 标 `[待确认]` 缺失字段/表，建议补 schema | 不强行写错 SQL |
| 性能优化无依据（表小） | 标注"小表无需优化" | 不堆无效优化建议 |

## 不要做什么（反例黑名单）

| 反模式 | 为什么不要做 |
|--------|------------|
| 直接甩 SQL 不先讲逻辑 | PM 无法验证查询逻辑对错，跑出错结果才发现就晚了 |
| 指标口径不对齐 PMContext | SQL 跑通了但口径错，结论全错 |
| 臆造表结构/字段 | 没有 schema 的 SQL 是猜的，跑不了 |
| 不区分方言 | BigQuery 的 `EXACT_COUNT_DISTINCT` 与 PostgreSQL 的 `COUNT(DISTINCT)` 不同，混用出错 |
| 不给验证脚本 | 没有验证的 SQL 结果不可信，PM 无法核对 |
| 复杂逻辑不加注释 | 窗口函数/CTE 不加注释，后续维护困难 |
| 性能建议堆砌不考虑表大小 | 小表堆索引是过度优化，浪费存储 |
| 审计三元组转换操作写"基于上述依据产出" | 空话，未阐明具体推导逻辑，判定为 Failure |

## 产出示例 · 实战提示

会员产品 SQL 查询片段：

```markdown
## 业务问题
上个月高价值用户的留存率

## 查询逻辑
1. 高价值用户 = PMContext 度量口径"月消费 ≥ ¥200"（来源：PMContext 价值验证度量）
2. 留存 = PMContext 度量口径"次月 ≥1 会话"（来源：PMContext 价值验证度量）
3. 筛选 2026-06 高价值用户 → left join 2026-07 会话 → 算留存率

## SQL（PostgreSQL）
[见 Step 4 示例]

## 性能建议
- payments(user_id, payment_date) 复合索引
- sessions 按月分区

## 验证
- 高价值用户总数 > 0
- 留存率 ∈ [0%, 100%]
- 抽样核对消费额
```

详见 [references/sql-example.md](references/sql-example.md)（完整 SQL 查询示例含多方言对照与性能优化案例）。

**实战铁律**（落盘前对照）：

- **先讲逻辑再写 SQL**：PM 能验证逻辑，不能验证语法，逻辑错了 SQL 再漂亮也没用
- **口径对齐 PMContext**：指标定义不查 PMContext 就是猜，跑对了也是巧合
- **方言必须确认**：不同方言函数/语法差异大，默认 PostgreSQL 要提示确认
- **验证脚本必备**：没有验证的 SQL 结果不可信，给抽样核对脚本
- **性能看表大小**：小表别堆索引，大表必给分区/物化视图方案

### Further Reading

- [The Product Analytics Playbook: AARRR, HEART, Cohorts & Funnels](https://www.productcompass.pm/p/the-product-analytics-playbook-aarrr)
- [How to Become a Technology-Literate PM](https://www.productcompass.pm/p/how-to-become-a-technology-literate)
- [SQL Performance Explained](https://use-the-index-luke.com/)
