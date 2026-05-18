# SIGN-ML-01 机器学习算法常识与小模拟

模块编号：SIGN-ML-01

模块名称：机器学习签到题：评估指标、常见模型和按公式模拟

标签：签到题、机器学习、监督学习、无监督学习、分类、回归、聚类、SVM、DNN、C++17

一句话用途：AI 背景题如果只是给小数据和规则，按本模块公式模拟，不需要任何第三方库。

题面触发词：训练集、测试集、标签、特征、分类、回归、聚类、SVM、DNN、softmax、precision、recall、F1。

什么时候用：

- 题目要求按给定公式算预测、指标或若干轮训练。
- 数据规模小，可以直接二维数组或 `vector` 模拟。
- 题目是 Special Judge，要求最大化某个评估指标。

不要什么时候用：

- 不要把真实机器学习库思路带进考场，不能用第三方库。
- 大规模稀疏文本检索优先倒排索引、排序和哈希。
- 神经网络复杂反传优先第 10 卷 `AI-14/15`。

复杂度：

- 混淆矩阵：`O(n)`。
- kNN：`O(q*n*d)`。
- k-means 一轮：`O(n*k*d)`。
- 全连接层前向：`O(in*out)`。

依赖的标准容器：`vector<double>`、`vector<int>`、`map`、`sort`、`cmath`。

输入如何整理：

```text
样本表常见格式：n d，然后每行 d 个特征和 1 个标签。
特征一般用 double，标签一般用 int/string。
分类指标先数 TP/FP/FN/TN。
```

接口：

```text
confusion -> 混淆矩阵。
metrics_binary -> accuracy/precision/recall/F1。
knn_predict -> kNN 投票。
stable_softmax -> 稳定 softmax。
```

常见坑：

- precision 分母是预测为正，recall 分母是真实为正。
- `exp(x)` 可能溢出，softmax 要先减最大值。
- kNN 平票规则按题面，没说时可取标签编号小者。
- 归一化时最大值等于最小值要特判。

暴力/部分分替代：

- 不会训练模型时，先写最近邻、多数类、线性打分 baseline。
- 不会复杂指标时，先输出混淆矩阵和 accuracy。
- 聚类不会收敛判断时，按题面固定迭代次数。

## 1. 监督学习和评估指标

| 概念 | 说明 |
|---|---|
| feature | 样本输入变量 |
| label | 真实类别或目标值 |
| train/test | 训练集/测试集 |
| overfit | 训练好、测试差 |
| underfit | 训练和测试都差 |
| accuracy | `(TP+TN)/(TP+TN+FP+FN)` |
| precision | `TP/(TP+FP)` |
| recall | `TP/(TP+FN)` |
| F1 | `2PR/(P+R)` |
| MSE | 平方误差均值 |
| MAE | 绝对误差均值 |

```cpp
struct BinaryMetric {
    int tp = 0, fp = 0, fn = 0, tn = 0;
    double accuracy, precision, recall, f1;
};

BinaryMetric binary_metrics(const vector<int> &truth, const vector<int> &pred) {
    BinaryMetric r;
    int n = (int)truth.size();
    for (int i = 0; i < n; i++) {
        if (truth[i] == 1 && pred[i] == 1) r.tp++;
        else if (truth[i] == 0 && pred[i] == 1) r.fp++;
        else if (truth[i] == 1 && pred[i] == 0) r.fn++;
        else r.tn++;
    }
    r.accuracy = (double)(r.tp + r.tn) / max(1, n);
    r.precision = (r.tp + r.fp == 0 ? 0 : (double)r.tp / (r.tp + r.fp));
    r.recall = (r.tp + r.fn == 0 ? 0 : (double)r.tp / (r.tp + r.fn));
    r.f1 = (r.precision + r.recall == 0 ? 0 : 2 * r.precision * r.recall / (r.precision + r.recall));
    return r;
}
```

## 2. 常见模型速查

| 模型 | 考场实现 |
|---|---|
| kNN | 算距离，排序，前 k 个投票 |
| 朴素贝叶斯 | 用 log 概率相加，避免下溢 |
| 线性回归 | `y=w dot x + b` |
| Logistic | `p=sigmoid(w dot x+b)` |
| SVM | margin 与 hinge loss |
| 决策树 | Gini 或 entropy 选划分 |
| k-means | 分配最近中心，再重算中心 |
| DNN 前向 | 矩阵乘 + 激活函数 |
| Q-learning | `Q=Q+alpha*(r+gamma*maxQ-next - Q)` |

## 3. softmax 和 kNN 短代码

```cpp
vector<double> stable_softmax(vector<double> z) {
    double mx = *max_element(z.begin(), z.end());
    double sum = 0;
    for (double &x : z) {
        x = exp(x - mx);
        sum += x;
    }
    for (double &x : z) x /= sum;
    return z;
}

int knn_predict(const vector<vector<double>> &x, const vector<int> &label,
                const vector<double> &q, int k) {
    vector<pair<double, int>> v;
    for (int i = 0; i < (int)x.size(); i++) {
        double d2 = 0;
        for (int j = 0; j < (int)q.size(); j++) {
            double t = x[i][j] - q[j];
            d2 += t * t;
        }
        v.push_back({d2, label[i]});
    }
    sort(v.begin(), v.end());
    map<int, int> cnt;
    int best_label = v[0].second, best_count = 0;
    for (int i = 0; i < k && i < (int)v.size(); i++) {
        int c = ++cnt[v[i].second];
        if (c > best_count || (c == best_count && v[i].second < best_label)) {
            best_count = c;
            best_label = v[i].second;
        }
    }
    return best_label;
}
```

