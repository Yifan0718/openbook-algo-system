# SIGN-PROB-01 概率统计速查

模块编号：SIGN-PROB-01

模块名称：概率、期望、统计指标和描述统计

标签：签到题、概率、统计、期望、方差、分位数、Bayes、C++17

一句话用途：遇到概率、统计、平均数、方差、分位数、相关系数或 A/B 测试类题时，用本模块快速查公式和小代码。

题面触发词：概率、条件概率、Bayes、期望、方差、标准差、中位数、众数、分位数、相关系数、直方图。

什么时候用：

- 题目给一组数，要求统计量。
- 题目给事件概率，要求组合概率或条件概率。
- 机器学习评估题需要先算基础统计。

不要什么时候用：

- 概率 DP 状态复杂，优先 DP 卷。
- 组合概率涉及大组合数取模，优先第 8 卷。
- 随机模拟只能做调试或部分分，不应替代精确算法。

复杂度：

- 均值/方差：`O(n)`。
- 中位数/分位数：排序 `O(n log n)`，或 `nth_element` 平均 `O(n)`。
- 相关系数：`O(n)`。

依赖的标准容器：`vector<double>`、`vector<int>`、`sort`、`map`。

输入如何整理：

```text
先确认统计的是总体还是样本。
总体方差分母 n，样本方差分母 n-1。
百分位定义题面可能不同，按题面为准。
```

接口：

```text
mean(a,n) -> 平均数。
variance_population(a,n) -> 总体方差。
median(a,n) -> 中位数。
pearson(x,y,n) -> 皮尔逊相关系数。
```

常见坑：

- 方差不要忘记平方。
- `n=1` 时样本方差分母 `n-1` 为 0，要特判。
- 概率相乘需要独立性；不独立时用条件概率。
- 精度输出用 `double`，计数用 `long long`。

暴力/部分分替代：

- 概率推不出时，小状态可枚举所有结果。
- 分位数规则不确定时，优先按题面样例反推。
- 大样本统计不会优化时，先排序写 `O(n log n)`。

## 1. 概率公式

| 名称 | 公式 |
|---|---|
| 补事件 | `P(not A)=1-P(A)` |
| 加法公式 | `P(A or B)=P(A)+P(B)-P(A and B)` |
| 条件概率 | `P(A|B)=P(A and B)/P(B)` |
| 乘法公式 | `P(A and B)=P(A|B)*P(B)` |
| 独立事件 | `P(A and B)=P(A)*P(B)` |
| Bayes | `P(A|B)=P(B|A)P(A)/P(B)` |
| 期望线性性 | `E(X+Y)=E(X)+E(Y)` |
| 方差 | `E(X^2)-E(X)^2` |

## 2. 描述统计小代码

```cpp
double mean_value(const vector<double> &a) {
    double s = 0;
    for (double x : a) s += x;
    return s / (double)a.size();
}

double variance_population(const vector<double> &a) {
    double mu = mean_value(a), s = 0;
    for (double x : a) s += (x - mu) * (x - mu);
    return s / (double)a.size();
}

double median_value(vector<double> a) {
    sort(a.begin(), a.end());
    int n = (int)a.size();
    if (n % 2 == 1) return a[n / 2];
    return (a[n / 2 - 1] + a[n / 2]) / 2.0;
}
```

## 3. 相关系数

```cpp
double pearson(const vector<double> &x, const vector<double> &y) {
    int n = (int)x.size();
    double mx = mean_value(x), my = mean_value(y);
    double num = 0, sx = 0, sy = 0;
    for (int i = 0; i < n; i++) {
        double dx = x[i] - mx, dy = y[i] - my;
        num += dx * dy;
        sx += dx * dx;
        sy += dy * dy;
    }
    if (sx == 0 || sy == 0) return 0;
    return num / sqrt(sx * sy);
}
```

## 4. 常见分布

| 分布 | 使用场景 | 关键量 |
|---|---|---|
| Bernoulli | 一次成败 | `P(1)=p` |
| Binomial | `n` 次独立成败 | `C(n,k)p^k(1-p)^(n-k)` |
| Geometric | 第一次成功在第几次 | `(1-p)^(k-1)p` |
| Poisson | 单位时间稀有事件数 | `lambda^k e^-lambda / k!` |
| Normal | 近似连续测量误差 | z-score |

