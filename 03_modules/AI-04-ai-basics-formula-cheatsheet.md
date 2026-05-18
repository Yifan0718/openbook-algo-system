# AI-04 AI 基础知识与公式速查

模块编号：AI-04

模块名称：AI 必备基础概念、常见公式与机考落地方式

标签：AI、机器学习、监督学习、无监督学习、强化学习、损失函数、评估指标、C++17

一句话用途：遇到 AI 专项背景题时，先用这一页把术语翻译成可手写算法和公式，避免看到“模型、训练、推理、损失、策略”就卡住。

题面触发词：

- 数据集、训练集、测试集、特征、标签。
- 模型、参数、权重、偏置、学习率、迭代轮数。
- 损失函数、准确率、召回率、F1。
- 反向传播、计算图、自动求导、链式法则。
- 聚类、中心、距离、相似度。
- 状态、动作、奖励、策略、价值。

什么时候用：

- 题目用了 AI/ML 术语，但没有要求第三方库。
- 需要把题面公式转成循环和数组。
- 需要确认某个指标、模型或训练过程的基本含义。

不要什么时候用：

- 不要把这页当机器学习教材；机考通常只考公式模拟和基础算法。
- 不要准备深度学习框架、复杂矩阵库；但要会按题面规则模拟小计算图、反向传播和自动求导。
- 如果题面给了具体公式，以题面公式为准。

复杂度：

- 训练/推理复杂度按样本数、特征数、迭代次数估算。
- 典型公式：`O(epoch * n * d)`、`O(test * train * d)`、`O(iter * n * k * d)`。

依赖的标准容器：

- `vector<double>`：特征、权重、中心。
- `vector<int>`：标签、类别、动作。
- `map/unordered_map`：词典、类别计数。
- `priority_queue`：Top-K。

输入如何整理：

```cpp
int n, d;
cin >> n >> d;
vector<vector<double>> x(n + 1, vector<double>(d + 1));
vector<int> y(n + 1);
for (int i = 1; i <= n; i++) {
    for (int j = 1; j <= d; j++) cin >> x[i][j];
    cin >> y[i];
}
```

接口：

```text
监督学习：有标签 y，做分类/回归。
无监督学习：无标签 y，做聚类/降维/相似度。
强化学习：有状态、动作、奖励，做策略或价值更新。
推理：给定模型参数，算输出。
训练：按题面规则迭代更新参数。
```

## 概念翻译表

| AI 术语 | 竞赛题里的含义 | 翻模块 |
|---|---|---|
| feature | 一个样本的数组 | `vector<double>` |
| label | 类别编号或目标值 | `int/double` |
| inference | 给参数算答案 | 循环公式 |
| training | 重复更新参数 | 模拟迭代 |
| loss | 误差函数 | 数学公式 |
| gradient | 更新方向 | `AI-14/15` 或按题面公式 |
| classification | 输出类别 | `AI-02/08/11/12` |
| regression | 输出连续值 | `AI-06/13` |
| clustering | 分组 | `AI-06` |
| policy | 状态到动作 | `AI-09` |
| value | 状态未来收益 | `AI-09` |
| special judge | 按分数评测 | `AI-10` |
| backpropagation | 从输出层往前传梯度 | `AI-14` |
| autograd | 计算图反向求偏导 | `AI-15` |

## 常见公式

```text
dot(w,x) = sum w[i] * x[i]
linear = dot(w,x) + b
relu(x) = max(0,x)
sigmoid(x) = 1 / (1 + exp(-x))
softmax[i] = exp(z[i]) / sum exp(z[j])
MSE = average((pred - y)^2)
hinge_loss = max(0, 1 - y * score)
accuracy = correct / total
precision = TP / (TP + FP)
recall = TP / (TP + FN)
F1 = 2 * precision * recall / (precision + recall)
chain_rule: dL/dx = dL/dy * dy/dx
```

模板代码：

```cpp
#include <bits/stdc++.h>
using namespace std;

double dot_product(const vector<double> &a, const vector<double> &b, int d) {
    double res = 0;
    for (int i = 1; i <= d; i++) res += a[i] * b[i];
    return res;
}

double relu(double x) {
    return max(0.0, x);
}

double sigmoid(double x) {
    return 1.0 / (1.0 + exp(-x));
}

double f1_score(double tp, double fp, double fn) {
    double precision = (tp + fp == 0) ? 0 : tp / (tp + fp);
    double recall = (tp + fn == 0) ? 0 : tp / (tp + fn);
    if (precision + recall == 0) return 0;
    return 2 * precision * recall / (precision + recall);
}
```

调用示例：

```cpp
double z = dot_product(w, x, d) + b;
double y = sigmoid(z);
```

常见坑：

- 题目给的标签可能是 `0/1`，也可能是 `-1/+1`，训练公式不同。
- softmax 要减最大值防止 `exp` 溢出。
- 浮点输出按题目要求 `fixed << setprecision(k)`。
- 分类 tie-break 通常要按标签小、编号小或输入顺序。
- “训练轮数”是外层循环，不要少跑或多跑一轮。

暴力/部分分替代：

- 不会训练：先实现推理。
- 不会复杂模型：先实现多数类、最近邻或线性打分。
- 不会优化：先按题面公式逐样本模拟。

最小测试样例：

```text
本模块是公式速查，无完整输入输出主程序。
```
