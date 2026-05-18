# AI-08 神经网络前向传播、激活函数与 Softmax

模块编号：AI-08

模块名称：神经网络基础前向传播与分类输出

标签：AI、神经网络、前向传播、ReLU、Sigmoid、Softmax、分类、C++17

一句话用途：当题目给权重、偏置、输入向量和激活函数，要求你算模型输出或预测类别时，用本模块按矩阵向量公式模拟前向传播。

题面触发词：

- 神经元、权重、偏置、激活函数。
- ReLU、Sigmoid、Softmax。
- logits、概率、预测类别。
- 前向传播、推理、模型参数。

什么时候用：

- 题目只要求推理，不要求复杂训练。
- 网络层数少，权重直接给出。
- 分类输出按最大概率或最大 logit。

不要什么时候用：

- 不要实现反向传播，除非题面给非常明确的更新公式。
- 不要使用第三方矩阵库。
- 大矩阵乘法仍按 `O(层数 * 输出维度 * 输入维度)` 估算。

复杂度：

- 单层全连接：`O(c*d)`。
- 多层：各层 `输出维度 * 输入维度` 求和。
- softmax：`O(c)`。

依赖的标准容器：

- `vector<double>`：向量、权重、偏置。
- `vector<vector<double>>`：权重矩阵，1-index。

输入如何整理：

```cpp
string act;
int c, d;
cin >> act >> c >> d;
```

接口：

```text
z[i] = bias[i] + sum_j w[i][j] * x[j]
activation: none / relu / sigmoid / softmax
prediction = argmax output[i]，tie 选编号小。
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

vector<double> softmax(vector<double> z) {
    int n = (int)z.size() - 1;
    double mx = z[1];
    for (int i = 2; i <= n; i++) mx = max(mx, z[i]);
    double sum = 0;
    for (int i = 1; i <= n; i++) {
        z[i] = exp(z[i] - mx);
        sum += z[i];
    }
    for (int i = 1; i <= n; i++) z[i] /= sum;
    return z;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string act;
    int c, d;
    cin >> act >> c >> d;

    vector<double> x(d + 1);
    for (int j = 1; j <= d; j++) cin >> x[j];

    vector<vector<double>> w(c + 1, vector<double>(d + 1));
    vector<double> b(c + 1);
    for (int i = 1; i <= c; i++) {
        for (int j = 1; j <= d; j++) cin >> w[i][j];
        cin >> b[i];
    }

    vector<double> y(c + 1, 0);
    for (int i = 1; i <= c; i++) {
        y[i] = b[i];
        for (int j = 1; j <= d; j++) y[i] += w[i][j] * x[j];
    }

    if (act == "relu") {
        for (int i = 1; i <= c; i++) y[i] = max(0.0, y[i]);
    } else if (act == "sigmoid") {
        for (int i = 1; i <= c; i++) y[i] = sigmoid(y[i]);
    } else if (act == "softmax") {
        y = softmax(y);
    }

    int pred = 1;
    for (int i = 2; i <= c; i++) {
        if (y[i] > y[pred] + 1e-12) pred = i;
    }

    cout << fixed << setprecision(6);
    cout << pred << '\n';
    for (int i = 1; i <= c; i++) {
        if (i > 1) cout << ' ';
        cout << y[i];
    }
    cout << '\n';

    return 0;
}
```

调用示例：

```cpp
// softmax 输出概率，argmax 为预测类别。
```

常见坑：

- softmax 要减最大 logit，防止 `exp` 溢出。
- 类别编号通常 1-index，输出 tie-break 选编号小。
- sigmoid 大负数直接 `exp(-x)` 会溢出，本模板分情况写。
- ReLU 会把负数变成 0。
- 题面可能要求输出 logits 而不是概率，仔细看输出格式。

暴力/部分分替代：

- 多层不会写：先写单层全连接。
- softmax 不会写：先输出最大 logit 的类别。
- 训练不会写：先实现前向推理。

最小测试样例：

```text
输入
softmax 2 2
1 2
1 0 0
0 1 0

输出
2
0.268941 0.731059
```

