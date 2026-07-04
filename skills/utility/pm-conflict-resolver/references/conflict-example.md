# Conflict Resolver 示例——最小差分修复

## 场景：node3-prd.json 引用了 node2-domain.json 中不存在的状态

### 报错上下文

```
node3-prd.json: 字段 'payment_flow' 引用状态 'pending_review'
错误: 状态 'pending_review' 未在 node2-domain.json 的状态机中定义
```

### 输入（仅两项）

1. 报错节点 JSON 片段（node3-prd.json 相关字段）：

```json
{
  "payment_flow": {
    "steps": [
      {"action": "submit", "next_state": "pending_review"},
      {"action": "approve", "next_state": "paid"}
    ]
  }
}
```

2. 上游节点 JSON（node2-domain.json 状态机片段）：

```json
{
  "states": ["draft", "submitted", "paid", "rejected"],
  "transitions": [
    {"from": "draft", "event": "submit", "to": "submitted"},
    {"from": "submitted", "event": "approve", "to": "paid"},
    {"from": "submitted", "event": "reject", "to": "rejected"}
  ]
}
```

### 输出：最小 diff

只改报错字段，不动其他分片：

```json
{
  "diff": {
    "file": "node3-prd.json",
    "field": "payment_flow.steps[0].next_state",
    "before": "pending_review",
    "after": "submitted",
    "reason": "node2-domain 状态机中 submit 事件的目标状态为 'submitted'，'pending_review' 不存在；对齐为 'submitted'"
  },
  "affected_downstream": ["node5-tech.json"],
  "rerun": ["node5-tech"]
}
```

### conflict-log.json 追加条目

```json
{
  "timestamp": "2026-07-04T12:00:00Z",
  "error_node": "node3-prd",
  "upstream_consumed": "node2-domain",
  "affected_field": "payment_flow.steps[0].next_state",
  "before": "pending_review",
  "after": "submitted",
  "affected_downstream": ["node5-tech"],
  "global_pmcontext_touched": false
}
```

### 不做的事

- ❌ 不读取全局 `docs/pm-context/pm-context.md`
- ❌ 不重写 node3-prd.json 的其他字段
- ❌ 不修改 node2-domain.json（上游 Frozen，除非波及检测判定需改上游→转 STOP/冲突）
