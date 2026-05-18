# AI-06 聚类、归一化与线性回归

模块编号：AI-06

模块名称：k-means 聚类、特征归一化与线性回归路由

标签：AI、聚类、k-means、回归、归一化、梯度下降、C++17

一句话用途：当题目给无标签点集、聚类中心、迭代次数，或给线性回归训练规则时，用本模块按公式模拟。

题面触发词：

- 聚类、中心、最近中心、k-means。
- 归一化、标准化、min-max。
- 线性回归、均方误差、梯度下降。
- 学习率、迭代次数、权重更新。

什么时候用：

- 题目明确给 `k`、迭代次数和初始中心。
- 特征维度不高，点数中等。
- 线性回归给出更新公式或只要求预测。

不要什么时候用：

- 不要自行脑补随机初始化，题目通常会给初始中心或规则。
- 聚类结果 tie-break 必须看题面；本模板距离相同选编号小中心。
- 大规模矩阵运算不要写复杂库，按题面范围估算。

复杂度：

- k-means：`O(iter * n * k * d)`。
- 线性预测：`O(q*d)`。
- 梯度下降：`O(epoch * n * d)`。

依赖的标准容器：

- `vector<double>`：点、中心、权重。
- `vector<int>`：每个点所属中心。

输入如何整理：

```cpp
int n, d, k, iter;
cin >> n >> d >> k >> iter;
vector<vector<double>> x(n + 1, vector<double>(d + 1));
```

接口：

```text
kmeans(points, n, d, k, iter) -> labels + centers。
```

模板代码：

```cpp
#include <bits/stdc++.h>
using namespace std;

double squared_distance(const vector<double> &a, const vector<double> &b, int d) {
    double res = 0;
    for (int i = 1; i <= d; i++) {
        double diff = a[i] - b[i];
        res += diff * diff;
    }
    return res;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, d, k, iter;
    cin >> n >> d >> k >> iter;
    vector<vector<double>> x(n + 1, vector<double>(d + 1));
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= d; j++) cin >> x[i][j];
    }

    vector<vector<double>> center(k + 1, vector<double>(d + 1));
    for (int c = 1; c <= k; c++) center[c] = x[c];

    vector<int> label(n + 1, 1);
    for (int it = 1; it <= iter; it++) {
        for (int i = 1; i <= n; i++) {
            int best = 1;
            double best_dist = squared_distance(x[i], center[1], d);
            for (int c = 2; c <= k; c++) {
                double cur = squared_distance(x[i], center[c], d);
                if (cur < best_dist - 1e-12) {
                    best_dist = cur;
                    best = c;
                }
            }
            label[i] = best;
        }

        vector<vector<double>> sum(k + 1, vector<double>(d + 1, 0));
        vector<int> cnt(k + 1, 0);
        for (int i = 1; i <= n; i++) {
            int c = label[i];
            cnt[c]++;
            for (int j = 1; j <= d; j++) sum[c][j] += x[i][j];
        }
        for (int c = 1; c <= k; c++) {
            if (cnt[c] == 0) continue;
            for (int j = 1; j <= d; j++) center[c][j] = sum[c][j] / cnt[c];
        }
    }

    cout << fixed << setprecision(6);
    for (int i = 1; i <= n; i++) {
        if (i > 1) cout << ' ';
        cout << label[i];
    }
    cout << '\n';
    for (int c = 1; c <= k; c++) {
        for (int j = 1; j <= d; j++) {
            if (j > 1) cout << ' ';
            cout << center[c][j];
        }
        cout << '\n';
    }

    return 0;
}
```

## 线性回归路由

预测公式：

```text
pred = w[1]*x[1] + ... + w[d]*x[d] + b
```

梯度下降常见更新：

```text
err = pred - y
w[j] -= lr * err * x[j]
b -= lr * err
```

## 归一化路由

```text
min-max: x' = (x - min) / (max - min)
standard: x' = (x - mean) / std
```

常见坑：

- k-means 空簇怎么处理看题面；本模板保持原中心。
- 距离相同 tie-break 选编号小中心。
- 初始中心很关键，通常取前 k 个点或题面给定。
- 回归训练要区分批量更新和在线更新。
- 标准差为 0 时要防御。

暴力/部分分替代：

- k-means 不会迭代：只做一次最近中心分配。
- 回归不会训练：只做给定权重预测。
- 归一化不会：先用原特征跑距离。

最小测试样例：

```text
输入
4 1 2 2
0
1
10
11

输出
1 1 2 2
0.500000
10.500000
```

