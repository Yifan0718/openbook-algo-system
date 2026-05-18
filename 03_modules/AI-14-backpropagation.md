# AI-14 反向传播、链式法则与小网络训练

模块编号：AI-14

模块名称：二层神经网络反向传播模板

标签：AI、反向传播、链式法则、神经网络训练、梯度下降、C++17

一句话用途：当题目给一个小神经网络、损失函数和学习率，要求你手算或模拟一轮/多轮参数更新时，用本模块按链式法则从输出层往前传梯度。

题面触发词：

- backward、backpropagation、gradient、chain rule。
- loss、MSE、cross entropy。
- 学习率、参数更新、一轮训练。
- 隐藏层、输出层、ReLU、sigmoid。

什么时候用：

- 网络很小，题目要求按公式模拟训练。
- 题面给初始权重、偏置、学习率和训练轮数。
- Special Judge 按预测误差打分，你想在线性模型之外再尝试小网络。

不要什么时候用：

- 不要现场写通用深度学习框架。
- 不要在数据很大时盲目训练多层网络，容易 TLE 且调参困难。
- 如果题目只要前向传播，翻 `AI-08/12`，不要写反向传播。

复杂度：

- 本模板二层网络每个样本：`O(d*h)`。
- 总训练：`O(epoch * n * d * h)`。

依赖的标准容器：

- `vector<vector<double>>`：输入层到隐藏层权重。
- `vector<double>`：隐藏层、输出层权重和偏置。

输入如何整理：

```cpp
int n, d, h, epoch;
double lr;
cin >> n >> d >> h >> epoch >> lr;
```

接口：

```text
隐藏层:
z1[j] = b1[j] + sum_k W1[j][k] * x[k]
a1[j] = relu(z1[j])

输出层:
z2 = b2 + sum_j W2[j] * a1[j]
yhat = sigmoid(z2)
loss = 0.5 * (yhat - y)^2

反向传播:
dz2 = (yhat - y) * yhat * (1 - yhat)
dW2[j] = dz2 * a1[j]
da1[j] = dz2 * W2[j]
dz1[j] = da1[j] * (z1[j] > 0)
dW1[j][k] = dz1[j] * x[k]
```

## 多分类 softmax + 交叉熵规则

很多模拟题会把输出层写成多分类 softmax，此时最常见、也最好背的是下面这一句：

```text
p = softmax(z)
loss = -log(p[label])
输出层梯度: dz[k] = p[k] - (k == label)
```

如果隐藏层是 sigmoid：

```text
delta1[i] = a1[i] * (1 - a1[i]) * sum_k W2[k][i] * dz[k]
```

如果隐藏层是 ReLU：

```text
delta1[i] = (z1[i] > 0 ? 1 : 0) * sum_k W2[k][i] * dz[k]
```

考场判断：

```text
二分类 + 单输出概率 -> 可以用本模块完整代码。
多分类 + softmax -> 用本节公式，把输出层从一个数改成 c 个数。
题面只问梯度，不问训练 -> 也可以翻 AI-15 计算图自动求导。
```

模板代码：

```cpp
#include <bits/stdc++.h>
using namespace std;

double sigmoid(double x) {
    if (x >= 0) {
        double e = exp(-x);
        return 1.0 / (1.0 + e);
    }
    double e = exp(x);
    return e / (1.0 + e);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, d, h, epoch;
    double lr;
    cin >> n >> d >> h >> epoch >> lr;

    vector<vector<double>> x(n + 1, vector<double>(d + 1));
    vector<double> target(n + 1);
    for (int i = 1; i <= n; i++) {
        for (int k = 1; k <= d; k++) cin >> x[i][k];
        cin >> target[i];
    }

    vector<vector<double>> w1(h + 1, vector<double>(d + 1));
    vector<double> b1(h + 1);
    for (int j = 1; j <= h; j++) {
        for (int k = 1; k <= d; k++) cin >> w1[j][k];
        cin >> b1[j];
    }

    vector<double> w2(h + 1);
    double b2;
    for (int j = 1; j <= h; j++) cin >> w2[j];
    cin >> b2;

    for (int ep = 1; ep <= epoch; ep++) {
        for (int i = 1; i <= n; i++) {
            vector<double> z1(h + 1), a1(h + 1);
            for (int j = 1; j <= h; j++) {
                z1[j] = b1[j];
                for (int k = 1; k <= d; k++) z1[j] += w1[j][k] * x[i][k];
                a1[j] = max(0.0, z1[j]);
            }

            double z2 = b2;
            for (int j = 1; j <= h; j++) z2 += w2[j] * a1[j];
            double yhat = sigmoid(z2);

            double dz2 = (yhat - target[i]) * yhat * (1.0 - yhat);
            vector<double> old_w2 = w2;

            for (int j = 1; j <= h; j++) {
                double grad_w2 = dz2 * a1[j];
                w2[j] -= lr * grad_w2;
            }
            b2 -= lr * dz2;

            for (int j = 1; j <= h; j++) {
                double da1 = dz2 * old_w2[j];
                double dz1 = (z1[j] > 0.0) ? da1 : 0.0;
                for (int k = 1; k <= d; k++) {
                    double grad_w1 = dz1 * x[i][k];
                    w1[j][k] -= lr * grad_w1;
                }
                b1[j] -= lr * dz1;
            }
        }
    }

    int q;
    cin >> q;
    cout << fixed << setprecision(6);
    for (int qi = 1; qi <= q; qi++) {
        vector<double> query(d + 1);
        for (int k = 1; k <= d; k++) cin >> query[k];

        vector<double> a1(h + 1);
        for (int j = 1; j <= h; j++) {
            double z = b1[j];
            for (int k = 1; k <= d; k++) z += w1[j][k] * query[k];
            a1[j] = max(0.0, z);
        }

        double z2 = b2;
        for (int j = 1; j <= h; j++) z2 += w2[j] * a1[j];
        cout << sigmoid(z2) << '\n';
    }

    return 0;
}
```

调用示例：

```cpp
// 先用 epoch=1 对样例复现；确认方向正确后再调 lr 和 epoch。
```

常见坑：

- 更新隐藏层时必须用更新前的 `w2` 计算 `da1`，本模板用 `old_w2` 保存。
- ReLU 在 `z <= 0` 时梯度为 0；`z == 0` 题面若有规定按题面。
- MSE + sigmoid 的 `dz2` 比交叉熵多乘 `yhat*(1-yhat)`。
- 学习率太大会发散，SPJ 题先用小学习率。
- 反向传播本质是链式法则，不要试图背一堆公式；从输出层往前乘局部导数。

暴力/部分分替代：

- 不会训练：只做前向传播，翻 `AI-08/12`。
- 不会隐藏层：先写线性回归或 SVM，翻 `AI-11/13`。
- SPJ 有多次提交：先均值/多数类 baseline，再小网络调参。

最小测试样例：

```text
输入
1 1 1 1 1
1 1
0 0
0 0
1
1

输出
0.531209
```
