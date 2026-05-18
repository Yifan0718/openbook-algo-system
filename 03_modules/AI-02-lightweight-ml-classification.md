# AI-02 轻量机器学习分类与评估

模块编号：AI-02

模块名称：kNN、朴素贝叶斯、感知机与混淆矩阵路由

标签：AI、机器学习、分类、kNN、朴素贝叶斯、感知机、混淆矩阵、C++17

一句话用途：当题目给训练集、测试集、标签和特征时，把它当作“按公式模拟 + 排序/统计”的算法题，优先使用 kNN、计数概率或线性打分。

题面触发词：

- 训练集、测试集、样本、标签、特征。
- 最近邻、距离、分类。
- 条件概率、先验概率、词频、文本分类。
- 权重、学习率、训练轮数、预测正负类。
- 准确率、混淆矩阵、precision、recall。

什么时候用：

- 数据规模中小，直接按训练集扫描每个测试样本可接受。
- 题目明确给出 k、距离公式或分类规则。
- 特征是离散计数，可以做朴素贝叶斯。
- 二分类线性模型按题面给定公式训练。

不要什么时候用：

- 不要实现复杂神经网络、反向传播和矩阵库。
- 数据极大时，kNN 的 `测试数 * 训练数 * 维度` 会 TLE。
- 浮点误差敏感时，比较要按题目要求设置精度。
- 类别很多且概率极小，朴素贝叶斯要用 log，不能直接乘很多小数。

复杂度：

- kNN 预测一个样本：`O(n*d + n log n)`，可用 nth_element 降到均摊 `O(n*d + n)`。
- 混淆矩阵：`O(q)`。
- 朴素贝叶斯训练：`O(n*d)`，预测：`O(class_count*d)`。
- 感知机：`O(epoch*n*d)`。

依赖的标准容器：

- `vector<double>`：特征。
- `vector<int>`：标签。
- `map<int,int>`：投票计数。
- `vector<vector<int>>`：混淆矩阵。

输入如何整理：

```cpp
struct Sample {
    vector<double> x; // 1-index 特征
    int label;
};
```

接口：

```text
predict_knn(train, query, k, d) -> 预测标签。
tie-break：票数多优先；票数相同标签小优先。
```

模板代码：

```cpp
#include <bits/stdc++.h>
using namespace std;

struct Sample {
    vector<double> x;
    int label;
};

double squared_distance(const vector<double> &a, const vector<double> &b, int d) {
    double res = 0;
    for (int i = 1; i <= d; i++) {
        double diff = a[i] - b[i];
        res += diff * diff;
    }
    return res;
}

int predict_knn(const vector<Sample> &train, const vector<double> &query, int k, int d) {
    vector<pair<double, int>> dist;
    for (int i = 1; i < (int)train.size(); i++) {
        dist.push_back({squared_distance(train[i].x, query, d), train[i].label});
    }
    sort(dist.begin(), dist.end());

    map<int, int> vote;
    for (int i = 0; i < k && i < (int)dist.size(); i++) {
        vote[dist[i].second]++;
    }

    int best_label = -1;
    int best_count = -1;
    for (auto [label, count] : vote) {
        if (count > best_count || (count == best_count && label < best_label)) {
            best_count = count;
            best_label = label;
        }
    }
    return best_label;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, q, d, k;
    cin >> n >> q >> d >> k;

    vector<Sample> train(n + 1);
    for (int i = 1; i <= n; i++) {
        train[i].x.assign(d + 1, 0);
        for (int j = 1; j <= d; j++) cin >> train[i].x[j];
        cin >> train[i].label;
    }

    for (int i = 1; i <= q; i++) {
        vector<double> query(d + 1);
        for (int j = 1; j <= d; j++) cin >> query[j];
        cout << predict_knn(train, query, k, d) << '\n';
    }

    return 0;
}
```

## 朴素贝叶斯路由

适合离散特征或词频文本分类。核心公式：

```text
score[c] = log(P(c)) + sum log(P(feature_j | c))
```

为什么用 log：

- 很多小概率直接相乘会下溢。
- log 后乘法变加法，比较大小不变。

## 感知机路由

适合二分类、题面直接给训练轮数和学习率：

```text
pred = sign(w · x + b)
如果 pred != y:
    w = w + lr * y * x
    b = b + lr * y
```

标签通常要转成 `-1/+1`。

## 混淆矩阵

```text
matrix[真实标签][预测标签]++
accuracy = 正确数 / 总数
```

调用示例：

```cpp
// int label = predict_knn(train, query, k, d);
```

常见坑：

- kNN 距离可以不开根号，平方距离排序结果相同。
- 浮点排序相等时，要按标签或样本编号做稳定 tie-break。
- 标签不一定从 1 连续到 c，可先离散化。
- k 大于训练样本数时，只取所有训练样本。
- 朴素贝叶斯要做平滑，例如 `+1`，避免概率为 0。
- 精度输出用 `fixed << setprecision(...)`。

暴力/部分分替代：

- kNN 太慢：先支持 `k=1` 或测试数小的子任务。
- 朴素贝叶斯不会：先按每类样本数预测多数类。
- 感知机不会：按题面给的权重直接预测，不训练。
- 混淆矩阵不会指标：先输出 accuracy 或正确数。

最小测试样例：

```text
输入
4 3 2 3
0 0 1
0 1 1
10 10 2
10 11 2
0 0.2
9 10
5 5

输出
1
2
1
```

