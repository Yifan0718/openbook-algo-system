# AI-11 线性 SVM、间隔分类与 Hinge Loss

模块编号：AI-11

模块名称：线性 SVM 训练与预测模板

标签：AI、监督学习、SVM、线性分类、Hinge Loss、SGD、C++17

一句话用途：当题目给二分类样本、学习率、正则系数和训练轮数，要求按线性 SVM 或最大间隔思想预测时，用本模块直接模拟更新。

题面触发词：

- SVM、support vector、margin、hinge loss。
- 二分类、标签 `-1/+1`。
- 学习率、lambda、正则化、迭代轮数。
- `max(0, 1 - y*(w*x+b))`。

什么时候用：

- 题目明确要求线性 SVM 或给出 hinge loss 更新规则。
- 特征维度不高，训练轮数有限。
- 输出类别只需要正负类预测。

不要什么时候用：

- 不要实现核函数 SVM，除非题面给非常具体的公式。
- 标签不是 `-1/+1` 时要先转换，不要直接拿 `0/1` 进更新。
- 如果题面只是普通线性分类，感知机可能更短；SVM 是更稳的备用模板。

复杂度：

- 训练：`O(epoch * n * d)`。
- 单个预测：`O(d)`。

依赖的标准容器：

- `vector<vector<double>>`：1-index 特征矩阵。
- `vector<int>`：标签。
- `vector<double>`：权重。

输入如何整理：

```cpp
int n, d, epoch;
double lr, lambda;
cin >> n >> d >> epoch >> lr >> lambda;
```

接口：

```text
score = w[1]*x[1] + ... + w[d]*x[d] + b
pred = score >= 0 ? +1 : -1
if y * score < 1:
    w[j] = w[j] - lr * lambda * w[j] + lr * y * x[j]
    b = b + lr * y
else:
    w[j] = w[j] - lr * lambda * w[j]
```

模板代码：

```cpp
#include <bits/stdc++.h>
using namespace std;

double dot_product(const vector<double> &w, const vector<double> &x, int d) {
    double res = 0;
    for (int j = 1; j <= d; j++) res += w[j] * x[j];
    return res;
}

int predict_svm(const vector<double> &w, double b, const vector<double> &x, int d) {
    double score = dot_product(w, x, d) + b;
    return score >= 0 ? 1 : -1;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, d, epoch;
    double lr, lambda;
    cin >> n >> d >> epoch >> lr >> lambda;

    vector<vector<double>> x(n + 1, vector<double>(d + 1));
    vector<int> y(n + 1);
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= d; j++) cin >> x[i][j];
        cin >> y[i];
        if (y[i] == 0) y[i] = -1;
    }

    vector<double> w(d + 1, 0);
    double b = 0;

    for (int ep = 1; ep <= epoch; ep++) {
        for (int i = 1; i <= n; i++) {
            double score = dot_product(w, x[i], d) + b;
            double margin = y[i] * score;
            for (int j = 1; j <= d; j++) {
                w[j] -= lr * lambda * w[j];
            }
            if (margin < 1.0) {
                for (int j = 1; j <= d; j++) {
                    w[j] += lr * y[i] * x[i][j];
                }
                b += lr * y[i];
            }
        }
    }

    int q;
    cin >> q;
    for (int qi = 1; qi <= q; qi++) {
        vector<double> query(d + 1);
        for (int j = 1; j <= d; j++) cin >> query[j];
        cout << predict_svm(w, b, query, d) << '\n';
    }

    return 0;
}
```

调用示例：

```cpp
// 标签输入若是 0/1，模板会把 0 转成 -1。
```

常见坑：

- `score == 0` 的 tie-break 本模板预测 `+1`，题面不同就改。
- 有正则项时，即使分类正确也要衰减 `w`。
- SVM 的 `lambda`、`lr`、`epoch` 常数很影响 SPJ 分数，优先按验证集调。
- 特征尺度差很多时，先做归一化，否则训练容易被某一维支配。

暴力/部分分替代：

- 不会 SVM：先写感知机；只在错误时更新。
- 不会训练：输出多数类或按给定权重预测。
- 数据很小：用 kNN 通常更稳。

最小测试样例：

```text
输入
2 1 1 1 0
1 1
-1 -1
3
2
-2
0

输出
1
-1
1
```
