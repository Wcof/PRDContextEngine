# SQL 查询完整示例

## 场景

PM 问："上个月高价值用户的留存率是多少？"——需要生成跨方言可用的 SQL。

## PMContext 度量提取

| 度量项 | PMContext 定义 | 来源 |
|--------|---------------|------|
| 高价值用户 | 月消费 ≥ ¥200 | PMContext 价值验证度量 |
| 留存 | 次月有 ≥1 次会话 | PMContext 价值验证度量 |
| 时间范围 | 上月=2026-06，本月=2026-07 | PMContext 全局约束 |

## schema（用户提供）

```
payments(payment_id, user_id, amount, payment_date)
sessions(session_id, user_id, session_date, duration)
users(user_id, signup_date, tier)
```

## 查询逻辑（自然语言先讲）

1. 定义"高价值用户"：PMContext 口径 = 2026-06 月消费合计 ≥ ¥200
2. 定义"留存"：PMContext 口径 = 2026-07 有 ≥1 次会话
3. 筛选 2026-06 高价值用户 → left join 2026-07 会话 → 留存率 = 有会话人数 / 高价值用户总数

## SQL — PostgreSQL

```sql
-- 口径：高价值用户=月消费≥¥200（来源：PMContext 价值验证度量）
-- 口径：留存=次月≥1会话（来源：PMContext 价值验证度量）
WITH high_value_users AS (
  SELECT user_id
  FROM payments
  WHERE payment_date >= '2026-06-01' AND payment_date < '2026-07-01'
  GROUP BY user_id
  HAVING SUM(amount) >= 200
),
retained_users AS (
  SELECT DISTINCT h.user_id
  FROM high_value_users h
  JOIN sessions s ON s.user_id = h.user_id
  WHERE s.session_date >= '2026-07-01' AND s.session_date < '2026-08-01'
)
SELECT
  COUNT(DISTINCT h.user_id) AS high_value_total,
  COUNT(DISTINCT r.user_id) AS retained,
  ROUND(COUNT(DISTINCT r.user_id)::numeric / COUNT(DISTINCT h.user_id) * 100, 2) AS retention_rate_pct
FROM high_value_users h
LEFT JOIN retained_users r ON r.user_id = h.user_id;
```

## SQL — BigQuery（方言差异）

```sql
-- BigQuery 用 EXACT_COUNT_DISTINCT 替代 COUNT(DISTINCT)
WITH high_value_users AS (
  SELECT user_id
  FROM `project.dataset.payments`
  WHERE payment_date >= '2026-06-01' AND payment_date < '2026-07-01'
  GROUP BY user_id
  HAVING SUM(amount) >= 200
),
retained_users AS (
  SELECT DISTINCT h.user_id
  FROM high_value_users h
  JOIN `project.dataset.sessions` s ON s.user_id = h.user_id
  WHERE s.session_date >= '2026-07-01' AND s.session_date < '2026-08-01'
)
SELECT
  EXACT_COUNT_DISTINCT(h.user_id) AS high_value_total,
  EXACT_COUNT_DISTINCT(r.user_id) AS retained,
  ROUND(EXACT_COUNT_DISTINCT(r.user_id) / EXACT_COUNT_DISTINCT(h.user_id) * 100, 2) AS retention_rate_pct
FROM high_value_users h
LEFT JOIN retained_users r ON r.user_id = h.user_id;
```

## 性能优化建议

| 优化项 | 建议 | 适用条件 |
|--------|------|---------|
| 复合索引 | `payments(user_id, payment_date)` | payments > 1M 行 |
| 分区 | `sessions` 按 `session_date` 月分区 | sessions > 10M 行 |
| 物化视图 | 预聚合"高价值用户"日表（每日刷新） | 此查询高频调用 |

## 验证脚本

```sql
-- 验证 1：高价值用户总数应 > 0
SELECT COUNT(*) FROM high_value_users;

-- 验证 2：留存率应 ∈ [0%, 100%]
-- (主查询结果核对)

-- 验证 3：抽样 10 个高价值用户核对消费额
SELECT user_id, SUM(amount) AS total
FROM payments
WHERE payment_date >= '2026-06-01' AND payment_date < '2026-07-01'
GROUP BY user_id ORDER BY total DESC LIMIT 10;
-- 核对：每个 user_id 的 total 应 ≥ 200
```

## 审计三元组

`<依据集: [PMContext 价值验证度量"高价值用户=月消费≥¥200"+"留存=次月≥1会话", schema payments/sessions]> → [工具: /pm-sql, 规则: 多方言 SQL 生成] → [转换: 自然语言业务问题→查询逻辑→SQL，同义词推导：PM 说"高价值"→映射 HAVING SUM(amount)>=200] → <产出: PostgreSQL/BigQuery SQL + 性能建议 + 验证脚本>`
