# AI-10 Special Judge、评分指标与模型选择策略

模块编号：AI-10

模块名称：AI 题 Special Judge 评分、指标计算与 baseline 选择

标签：AI、Special Judge、准确率、误差、F1、模型选择、C++17

一句话用途：当题目不是唯一答案，而是按准确率、误差、相似度、得分函数评测时，用本模块先写一个确定性 baseline，再按数据范围逐步升级。

题面触发词：

- Special Judge、得分、score、accuracy、loss、error。
- 预测值、真实值、训练集、验证集、测试集。
- 平均误差、均方误差、RMSE、F1、precision、recall。
- 输出任意满足条件的模型结果、越接近越高分。

什么时候用：

- 输出可以不是唯一标准答案。
- 题目给训练数据和隐藏测试，要求你输出预测、分类或参数。
- 可以多次提交，且最终取最高分，适合 baseline -> 调参 -> 升级模型。

不要什么时候用：

- 如果题目是普通 OJ 精确答案，不要把它当机器学习题。
- 不要随机输出不可复现结果；考场调参必须保证同一代码每次一样。
- 不要为了复杂模型牺牲合法输出和部分分 baseline。

复杂度：

- 指标计算：`O(n)`。
- 选择多数类/平均值 baseline：`O(n)`。
- 网格调参：`O(参数组合数 * 验证集规模 * 单次预测复杂度)`。

依赖的标准容器：

- `vector<double>`：真实值、预测值。
- `vector<int>`：真实类别、预测类别。
- `map<int,int>`：多数类统计。

输入如何整理：

```cpp
int n;
cin >> n;
vector<double> y(n + 1), pred(n + 1);
for (int i = 1; i <= n; i++) cin >> y[i] >> pred[i];
```

接口：

```text
metric mode:
accuracy: 输入 n 行真实类别 预测类别，输出准确率。
mae:      输入 n 行真实值 预测值，输出平均绝对误差。
rmse:     输入 n 行真实值 预测值，输出均方根误差。
f1:       输入 n 行真实二分类标签 预测二分类标签，正类固定为 1。
```

模板代码：

```cpp
#include <bits/stdc++.h>
using namespace std;

double metric_accuracy(const vector<int> &real_label, const vector<int> &pred_label, int n) {
    int correct = 0;
    for (int i = 1; i <= n; i++) {
        if (real_label[i] == pred_label[i]) correct++;
    }
    return n == 0 ? 0.0 : (double)correct / n;
}

double metric_mae(const vector<double> &y, const vector<double> &pred, int n) {
    double sum = 0;
    for (int i = 1; i <= n; i++) sum += fabs(y[i] - pred[i]);
    return n == 0 ? 0.0 : sum / n;
}

double metric_rmse(const vector<double> &y, const vector<double> &pred, int n) {
    double sum = 0;
    for (int i = 1; i <= n; i++) {
        double e = y[i] - pred[i];
        sum += e * e;
    }
    return n == 0 ? 0.0 : sqrt(sum / n);
}

double metric_binary_f1(const vector<int> &real_label, const vector<int> &pred_label, int n) {
    int tp = 0, fp = 0, fn = 0;
    for (int i = 1; i <= n; i++) {
        if (real_label[i] == 1 && pred_label[i] == 1) tp++;
        if (real_label[i] != 1 && pred_label[i] == 1) fp++;
        if (real_label[i] == 1 && pred_label[i] != 1) fn++;
    }
    double precision = (tp + fp == 0) ? 0.0 : (double)tp / (tp + fp);
    double recall = (tp + fn == 0) ? 0.0 : (double)tp / (tp + fn);
    if (precision + recall == 0) return 0.0;
    return 2.0 * precision * recall / (precision + recall);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string mode;
    int n;
    cin >> mode >> n;

    cout << fixed << setprecision(6);
    if (mode == "accuracy" || mode == "f1") {
        vector<int> real_label(n + 1), pred_label(n + 1);
        for (int i = 1; i <= n; i++) cin >> real_label[i] >> pred_label[i];
        if (mode == "accuracy") cout << metric_accuracy(real_label, pred_label, n) << '\n';
        else cout << metric_binary_f1(real_label, pred_label, n) << '\n';
    } else {
        vector<double> y(n + 1), pred(n + 1);
        for (int i = 1; i <= n; i++) cin >> y[i] >> pred[i];
        if (mode == "mae") cout << metric_mae(y, pred, n) << '\n';
        else if (mode == "rmse") cout << metric_rmse(y, pred, n) << '\n';
    }

    return 0;
}
```

## SPJ 考场 baseline 路由

| 输出类型 | 第一个可提交 baseline | 升级方向 |
|---|---|---|
| 分类标签 | 训练集多数类 | `AI-02` kNN/朴素贝叶斯，`AI-11` SVM |
| 连续数值 | 训练集平均值/中位数 | `AI-13` 线性回归，`AI-06` 归一化 |
| 排名/推荐 | 全局热门度 | `AI-03/05` 相似度、Top-K、TF-IDF |
| 聚类编号 | 按输入顺序分组 | `AI-06` k-means、距离阈值 |
| 路径/动作 | 合法最短/贪心动作 | `GRAPH-02/03`，`AI-01` A* |
| 小网络预测 | 线性模型/前向传播 | `AI-12` 多层前向，`AI-14` 小网络反传 |
| 计算图梯度 | 数值差分 | `AI-15` 反向模式自动求导 |

## 验证集与调参策略

```text
1. 先把训练集前 80% 当 train，后 20% 当 valid。
2. 写最简单 baseline，算 valid 分数。
3. 只调 1-2 个参数：k、学习率、迭代轮数、距离权重。
4. 固定随机性：不要 rand；如果必须打散，用固定种子。
5. 最后用全部训练集重训一次，再输出测试集预测。
```

常见坑：

- Special Judge 仍然会检查输出格式，格式错就是 0 分。
- 评分指标越大越好还是越小越好必须确认。
- 浮点输出一般多打几位，`fixed << setprecision(10)` 很稳。
- hidden test 分布可能和样例不同，不要只为样例调参。
- 如果类标不是 `1..c`，先离散化或用 `map` 统计。

暴力/部分分替代：

- 完全不会模型：分类输出多数类，回归输出均值，推荐输出热门项。
- 数据小：直接 kNN 或枚举参数。
- 不会训练：按题面给定权重做推理，或输出合法默认值。

最小测试样例：

```text
输入
f1 5
1 1
1 0
0 1
0 0
1 1

输出
0.666667
```
