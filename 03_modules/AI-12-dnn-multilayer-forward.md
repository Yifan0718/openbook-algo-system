# AI-12 多层 DNN 前向传播模板

模块编号：AI-12

模块名称：多层全连接神经网络前向传播

标签：AI、DNN、神经网络、全连接层、ReLU、Sigmoid、Softmax、C++17

一句话用途：当题目给多层权重、偏置、激活函数，要求算输出概率或分类结果时，用本模块按层模拟前向传播。

题面触发词：

- 多层感知机、DNN、MLP。
- layer、weight、bias、activation。
- ReLU、Sigmoid、Tanh、Softmax。
- 前向传播、推理、概率输出。

什么时候用：

- 题目只要求 forward，不要求反向传播。
- 每层规模不大，可以用 `vector` 或静态数组模拟矩阵向量乘。
- 输出要求类别、logit 或概率。

不要什么时候用：

- 不要手写复杂训练框架。
- 不要把 softmax 放在中间层，除非题面这样要求。
- 大矩阵要估算 `sum(in_dim*out_dim)`，避免超时。

复杂度：

- 总复杂度：所有层 `O(in_dim * out_dim)` 求和。
- 空间：当前层向量 + 下一层向量即可。

依赖的标准容器：

- `vector<double>`：当前向量、下一层向量。
- `vector<vector<double>>`：当前层权重。

输入如何整理：

```cpp
int layer_count;
cin >> layer_count;
int dim;
cin >> dim;
vector<double> cur(dim + 1);
```

接口：

```text
每层输入:
out_dim activation
out_dim 行，每行 in_dim 个权重，最后一个数是 bias
activation: none / relu / sigmoid / tanh / softmax
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

void apply_activation(vector<double> &a, const string &act) {
    int n = (int)a.size() - 1;
    if (act == "relu") {
        for (int i = 1; i <= n; i++) a[i] = max(0.0, a[i]);
    } else if (act == "sigmoid") {
        for (int i = 1; i <= n; i++) a[i] = sigmoid(a[i]);
    } else if (act == "tanh") {
        for (int i = 1; i <= n; i++) a[i] = tanh(a[i]);
    } else if (act == "softmax") {
        double mx = a[1];
        for (int i = 2; i <= n; i++) mx = max(mx, a[i]);
        double sum = 0;
        for (int i = 1; i <= n; i++) {
            a[i] = exp(a[i] - mx);
            sum += a[i];
        }
        for (int i = 1; i <= n; i++) a[i] /= sum;
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int layer_count;
    cin >> layer_count;

    int dim;
    cin >> dim;
    vector<double> cur(dim + 1);
    for (int j = 1; j <= dim; j++) cin >> cur[j];

    for (int layer = 1; layer <= layer_count; layer++) {
        int out_dim;
        string act;
        cin >> out_dim >> act;

        vector<double> nxt(out_dim + 1, 0);
        for (int i = 1; i <= out_dim; i++) {
            for (int j = 1; j <= dim; j++) {
                double w;
                cin >> w;
                nxt[i] += w * cur[j];
            }
            double b;
            cin >> b;
            nxt[i] += b;
        }

        apply_activation(nxt, act);
        cur = nxt;
        dim = out_dim;
    }

    int pred = 1;
    for (int i = 2; i <= dim; i++) {
        if (cur[i] > cur[pred] + 1e-12) pred = i;
    }

    cout << fixed << setprecision(6);
    cout << pred << '\n';
    for (int i = 1; i <= dim; i++) {
        if (i > 1) cout << ' ';
        cout << cur[i];
    }
    cout << '\n';

    return 0;
}
```

调用示例：

```cpp
// 每层只保留当前向量，适合手写多层前向传播题。
```

常见坑：

- softmax 要减最大值，防止 `exp` 溢出。
- 权重矩阵方向看题面：本模板是 `out_dim` 行、`in_dim` 列。
- 输出类别 tie-break 本模板选编号小。
- 题面如果输出 logit，就不要对最后一层 softmax。

暴力/部分分替代：

- 多层太长：先支持 `none/relu/softmax` 三种激活。
- 不会 sigmoid/tanh：用库函数 `exp/tanh`，注意精度。
- 训练不会：只做前向推理，也常能拿对应子任务分。

最小测试样例：

```text
输入
2
2
1 2
2 relu
1 0 0
0 1 0
2 softmax
1 0 0
0 1 0

输出
2
0.268941 0.731059
```
