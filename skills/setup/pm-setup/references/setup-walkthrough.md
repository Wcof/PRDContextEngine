# 配置流程示例与避坑提示

## 典型配置流程

### 场景 A：Claude Code 项目，首次配置

```
Step 1: Explore
  → git remote: github.com/org/project
  → CLAUDE.md: 存在（已有其他配置）
  → AGENTS.md: 不存在
  → docs/pm-context/: 不存在
  → Agent 类型: Claude Code（从会话环境推断）

Step 2: Ask（逐一确认）
  Section A — 产物目录
    默认 docs/pm-context/，用户确认

  Section B — 语言偏好
    选项：中文 / 英文 / 双语
    用户选：中文

  Section C — 知识库路径
    用户输入：~/docs/pm-kb
    验证路径存在 ✅

  Section D — Agent 规则落点
    CLAUDE.md 已存在 → 写入 CLAUDE.md

Step 3: Confirm
  展示待写入的 ## PMSkill 块，用户确认

Step 4: Write
  编辑 CLAUDE.md，追加 ## PMSkill 块（含 setup 状态行）
  创建 docs/pm-context/ 目录
  落 docs/pm-context/.pmskill-setup.stamp 凭据（YAML）
```

### 场景 B：CLAUDE.md 和 AGENTS.md 同时存在

```
Step 1: Explore
  → CLAUDE.md: 存在
  → AGENTS.md: 存在
  → 当前 Agent: Codex（从环境推断）

Step 2: 冲突处理
  → 检测到双文件
  → 推断 Agent 类型为 Codex → 选择 AGENTS.md
  → 只编辑 AGENTS.md，不同时编辑 CLAUDE.md
```

### 场景 C：知识库路径无效

```
Step 2: Ask
  Section C — 知识库路径
    用户输入：~/nonexistent/path
    验证路径不存在 ❌
    → 提示"路径不存在，请重新输入或跳过"
    用户选：跳过
```

## 写入的 PMSkill 块模板

```markdown
## PMSkill

- 领域术语：见 CONTEXT.md（若不存在，由 /pm-need 在首次澄清时沉淀）
- 产物目录：docs/pm-context/
- PMContext（唯一 Entity）：docs/pm-context/pm-context.md
- 下游 View：PRD（`prd/ai-prd.md` / `prd/human-prd.md`）、用户故事（`stories.md`）、草图（`sketch/*.md`）均从 PMContext 派生
- 汇总文档（可选）：`SUMMARY-需求.md` / `SUMMARY-交付.md` / `SUMMARY-可视化.md` / `SUMMARY-验证.md` / `INDEX.md` 由 `/pm-summary` 把散件拼装成几份大文档，原产物不动
- 风险标记：[待确认] / [假设] / [冲突] 写在正文里，无需独立检查报告
- 知识库：无
- 无 hook：/pm-collect 从对话上下文 + 项目扫描 + 知识库搜索收集，不拦截 Agent 会话
- 语言：中文
- setup 状态：未运行 PMContext（请先 `/pm-need <需求>`；本块由 /pm-setup 写入，pm-need 首次运行后会更新此行）
```

## 避坑提示

| 坑 | 怎么避 |
|----|--------|
| 两个 Agent 文件同时写入 | 只编辑被选中的那个，绝不同时编辑两个 |
| 重复追加 PMSkill 块 | 已存在则原位更新，不追加重复块 |
| 知识库路径不存在 | 当场提示，不写入错误路径 |
| 产物目录在 gitignore 中 | 明示"PMSkill 产物不会进版本库"，问用户三选一 |
| 运行多次 /pm-setup | 安全重运行：块覆盖更新，**用户手改内容会丢失**——二次 setup 前建议先备份块；stamp 覆盖时保留 pmcontext_exists 真值 |

## 延伸参考

- [Anthropic Agent Skills 规范](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
