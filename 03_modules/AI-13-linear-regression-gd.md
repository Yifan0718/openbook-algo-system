# AI-13 线性回归与梯度下降训练

模块编号：AI-13

模块名称：线性回归在线梯度下降与预测

标签：AI、监督学习、回归、线性回归、梯度下降、MSE、C++17

一句话用途：当题目给连续标签、学习率和训练轮数，要求按线性回归公式训练并预测时，用本模块写一个可调的回归 baseline。

题面触发词：

- regression、linear model、MSE、loss。
- 连续值预测、房价、评分、概率分数。
- 学习率、epoch、gradient descent。
- 权重、偏置、预测误差。

什么时候用：

- 输出是连续值，Special Judge 按误差给分。
- 特征维度不高，可以手写线性模型。
- 题面直接给更新公式或允许自选简单模型。

不要什么时候用：

- 不要把所有回归题都强行套线性模型；先看是否有明显公式。
- 特征量级差异很大时，最好先归一化。
- 学习率过大会发散，SPJ 题要小步调参。

复杂度：

- 训练：`O(epoch * n * d)`。
- 单次预测：`O(d)`。

依赖的标准容器：

- `vector<vector<double>>`：训练特征。
- `vector<double>`：标签、权重、查询。

输入如何整理：

```cpp
int n, d, epoch;
double lr;
cin >> n >> d >> epoch >> lr;
```

接口：

```text
pred = w[1]*x[1] + ... + w[d]*x[d] + b
err = pred - y
w[j] -= lr * err * x[j]
b -= lr * err
```

模板代码：

```cpp
#include <bits/stdc++.h>
using namespace std;

double predict_linear(const vector<double> &w, double b, const vector<double> &x, int d) {
    double res = b;
    for (int j = 1; j <= d; j++) res += w[j] * x[j];
    return res;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, d, epoch;
    double lr;
    cin >> n >> d >> epoch >> lr;

    vector<vector<double>> x(n + 1, vector<double>(d + 1));
    vector<double> y(n + 1);
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= d; j++) cin >> x[i][j];
        cin >> y[i];
    }

    vector<double> w(d + 1, 0);
    double b = 0;

    for (int ep = 1; ep <= epoch; ep++) {
        for (int i = 1; i <= n; i++) {
            double pred = predict_linear(w, b, x[i], d);
            double err = pred - y[i];
            for (int j = 1; j <= d; j++) {
                w[j] -= lr * err * x[i][j];
            }
            b -= lr * err;
        }
    }

    int q;
    cin >> q;
    cout << fixed << setprecision(6);
    for (int qi = 1; qi <= q; qi++) {
        vector<double> query(d + 1);
        for (int j = 1; j <= d; j++) cin >> query[j];
        cout << predict_linear(w, b, query, d) << '\n';
    }

    return 0;
}
```

## SPJ 调参建议

| 现象 | 调整 |
|---|---|
| 预测值爆炸 | 降低 `lr`，先做归一化 |
| 训练太慢 | 减少 epoch 或只用部分特征 |
| valid 分数差 | 尝试 `lr = 0.001/0.01/0.05/0.1` |
| 输出范围有限 | 最后 `pred = min(max(pred, L), R)` |

常见坑：

- 在线更新和批量更新结果不同，题面若规定必须照题面。
- 若用 MSE 的完整梯度，有些写法会多一个 `2`，这可合并到学习率里。
- 回归输出通常多打几位小数。
- 标签和特征很大时，`double` 比 `float` 稳。

暴力/部分分替代：

- 不会训练：输出训练标签平均值。
- 特征只有一维：先尝试按比例或最小二乘公式。
- SPJ 有多次提交：先均值 baseline，再上线性回归，再调学习率。

最小测试样例：

```text
输入
1 1 1 1
1 2
1
3

输出
8.000000
```
