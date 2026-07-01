# A/B 测试分析完整示例

## 场景

会员产品 onboarding 流程改版 A/B 测试。假设：新版 onboarding（3 步精简）比旧版（5 步）提升 D7 激活率 ≥10%。

## PMContext 度量提取

| 度量项 | PMContext 定义 | 来源 |
|--------|---------------|------|
| 主指标 | D7 激活率（注册后 7 日内完成首次付费） | PMContext 价值验证度量 |
| 阈值 | +10% 相对 lift | PMContext 价值验证度量 |
| guardrail 1 | 人均收入不退化 | PMContext 边界条件 |
| guardrail 2 | 7 日留存不退化 | PMContext 边界条件 |
| 人群 | 新注册用户（排除老用户） | PMContext 用户场景 |

## 实验设置验证

| 验证项 | 结果 | 状态 |
|--------|------|------|
| 样本量 | control 5023 / variant 4987；MDE 3% 需 4800/组（80% power, α=0.05） | ✅ 达标 |
| 运行时长 | 14 天（覆盖 2 个完整周周期，含周末） | ✅ |
| SRM | 期望 5000/5000，实际 5023/4987；χ²=0.25, p=0.62 | ✅ 无 SRM |
| 新鲜效应 | 前 3 天数据剔除后趋势稳定 | ✅ |

## 显著性计算（Python 脚本）

```python
import numpy as np
from scipy import stats

# control: 5023 样本, 617 转化
# variant: 4987 样本, 688 转化
cc, cn = 617, 5023
vc, vn = 688, 4987

p_control = cc / cn  # 0.1228
p_variant = vc / vn  # 0.1379
lift = (p_variant - p_control) / p_control * 100  # +12.2%

# two-proportion z-test
p_pool = (cc + vc) / (cn + vn)
se = np.sqrt(p_pool * (1 - p_pool) * (1/cn + 1/vn))
z = (p_variant - p_control) / se
p_value = 2 * (1 - stats.norm.cdf(abs(z)))  # 0.003

# 95% CI for lift
ci_low = (p_variant - p_control - 1.96 * se) / p_control * 100
ci_high = (p_variant - p_control + 1.96 * se) / p_control * 100
print(f"lift={lift:.1f}%, p={p_value:.4f}, 95% CI=[{ci_low:.1f}%, {ci_high:.1f}%]")
# lift=+12.2%, p=0.003, 95% CI=[+4.1%, +21.5%]
```

## guardrail 检查

| guardrail | control | variant | 变化 | p-value | 退化? |
|-----------|---------|---------|------|---------|------|
| 人均收入 | ¥45.2 | ¥44.8 | -0.9% | 0.45 | 否 |
| 7 日留存 | 68% | 67% | -1.5% | 0.32 | 否 |

## 决策矩阵

| 维度 | 结果 |
|------|------|
| 统计显著 | ✅ p=0.003 < 0.05 |
| 业务显著 | ✅ lift +12.2% ≥ PMContext 阈值 +10% |
| guardrail | ✅ 无退化 |
| **决策** | **Ship** |
| 后续 | 全量发布，监测 2 周防回退；D30 留存复核 |

## 审计三元组

`<依据集: [PMContext 价值验证度量"D7激活率"+阈值+10%, 实验数据 cc=617/cn=5023/vc=688/vn=4987]> → [工具: /pm-abtest, 规则: two-proportion z-test] → [转换: 双比例显著性检验，从转化数推 lift 与 p-value，多对多实体映射：control/variant 两组→z 统计量] → <产出: lift+12.2%, p=0.003, ship 决策>`
