# PINNED — /pm-conflict-resolver

> 绝不可被稀释的核心约束（供运行时置顶加载）。冗长示例见 references/。

1. 输入仅两项：报错节点 error 上下文 + 依赖的上游节点 JSON，禁止读全局 PMContext
2. 只输出最小差分（diff），不重写未报错的节点分片
3. 差分写入 `docs/pm-context/.loop/conflict-log.json`
4. 上游 JSON 缺失 → STOP，不臆造
5. 修改波及 >1 个上游节点 → 标 `[冲突]` 交 PM 裁决，不扩大改动面
