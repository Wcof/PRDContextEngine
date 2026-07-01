# 交接文档完整示例

会员续费 PMSkill 会话交接文档完整示例。

```markdown
# 会话交接: 会员续费 PMSkill

> 生成时间: 2026-07-01T23:50 | 上一个 Agent 的会话
> PMContext 置信度: 高 6 / 中 2 / 低 1

## PMContext 状态
- 路径: docs/pm-context/pm-context.md
- 置信度: 高 6 / 中 2 / 低 1
- [待确认] 项: 3

## 已完成产物
| 产物 | 完成 | 路径 | 备注 |
|---|---|---|---|
| PMContext | ✓ | docs/pm-context/pm-context.md | 8 维全 |
| AI PRD | ✓ | docs/pm-context/aiprd.md | - |
| Human PRD | ✓ | docs/pm-context/humanprd.md | - |
| OST | ✓ | docs/pm-context/ost.md | 4 机会 6 方案 |
| 用户故事 | ✓ | docs/pm-context/stories.md | 3 故事 |
| 线框图 | ✓ | docs/pm-context/sketch/wireframe.md | - |
| 流程图 | ✓ | docs/pm-context/sketch/flow.md | - |
| 信息架构图 | ✗ | - | 未生成 |
| 状态机图 | ✗ | - | 未生成 |
| Pre-Mortem | ✓ | docs/pm-context/premortem.md | - |

## 未完成项
1. 信息架构图（/pm-ia）未调用
2. 状态机图（/pm-state）未调用
3. PMContext 中 3 项 [待确认]:
   - 续费转化率基线数据（PM 需提供）
   - 支付通道限制（PM 需确认）
   - 会员等级体系（PM 需补充）

## 关键决策
| 决策 | 选择 | 理由 | 来源 |
|---|---|---|---|
| refine 模式 | 追问模式 | PM 想逐维确认 | 对话 |
| 续费方案 | 一键续费 | PM 暂不做自动续费 | 对话: PM 确认 |
| 技术栈 | Vue3+Vite+TS | 项目已有 package.json | 项目扫描 |

## 下一步建议
1. **优先:** 补全 PMContext [待确认] 项 → `/pm-need <补充材料> --incremental`
2. **然后:** 生成剩余草图 → `/pm-ia` 和 `/pm-state`
3. **可选:** HTML 原型 → `/pm-sketch --prototype --auto`

## 接手者快速进入指南
1. 读本文件了解工作状态
2. 读 `docs/pm-context/pm-context.md` 了解需求全貌
3. 读未完成产物对应 skill 的 SKILL.md 了解下一步怎么跑
4. 按上方"下一步建议"顺序执行
```
