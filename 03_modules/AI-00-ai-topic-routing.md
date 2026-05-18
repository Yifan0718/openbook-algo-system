# AI-00 AI 专项可能题型路由

模块编号：AI-00

模块名称：人工智能专项招生可能包装成机考题的算法主题

标签：AI、人工智能、搜索、机器学习、分类、相似度、模拟、C++17

一句话用途：如果题面带“智能体、训练数据、分类、相似度、推荐、路径规划、博弈、规则引擎”等 AI 味道，先用这张表判断它本质上是哪类算法题。

题面触发词：

- 智能体、机器人、路径规划、启发式、代价函数。
- 游戏 AI、对手、最优策略、轮流行动。
- 训练集、测试集、标签、分类、预测。
- 特征向量、距离、相似度、推荐。
- 准确率、召回率、混淆矩阵。
- 文本分词、词频、关键词、相似文档。
- 简单神经元、权重、训练轮数、梯度下降。
- Special Judge、得分、误差、模型选择。
- SVM、margin、hinge loss。
- DNN、多层网络、前向传播、反向传播。
- 计算图、自动求导、gradient、chain rule。

什么时候用：

- 题目是 AI 背景，但实际可化为搜索、图、数学、模拟、排序或 DP。
- 需要快速判断“是不是要写机器学习”，避免被题面吓住。
- 需要无第三方库手写 kNN、朴素贝叶斯、感知机、相似度等轻量模型。

不要什么时候用：

- 不要准备深度学习框架；但要准备小规模反向传播/计算图求导模板，用来应对规则模拟题。
- 不要把 AI 题理解成要懂很多理论；大概率仍是基础算法/数据结构包装。
- 如果数据规模很大，轻量 ML 模拟也可能变成排序、矩阵、前缀统计或图题。

复杂度：

- AI 包装题仍按算法复杂度判断。
- kNN：`O(测试数 * 训练数 * 维度)`。
- 朴素贝叶斯：训练 `O(样本数 * 特征数)`，预测 `O(类别数 * 特征数)`。
- A*：最坏仍可能接近 Dijkstra/BFS 访问状态数。
- Minimax：约 `O(分支数^深度)`，alpha-beta 只剪枝不改变最坏指数级。

依赖的标准容器：

- `vector`：特征、样本、距离、矩阵。
- `string`：标签、文本、token。
- `map/unordered_map`：标签计数、词频、词典。
- `priority_queue`：A*、Top-K 推荐。
- `queue/deque`：BFS 状态搜索。

输入如何整理：

```cpp
struct Sample {
    vector<double> x;
    int label;
};

int n, d;
cin >> n >> d;
vector<Sample> train(n + 1);
for (int i = 1; i <= n; i++) {
    train[i].x.assign(d + 1, 0);
    for (int j = 1; j <= d; j++) cin >> train[i].x[j];
    cin >> train[i].label;
}
```

接口：

```text
AI 题面 -> 算法本质：
路径规划 -> BFS / Dijkstra / A*
对弈决策 -> minimax / alpha-beta / 博弈 DP
分类预测 -> kNN / Naive Bayes / Perceptron / SVM
相似推荐 -> cosine / Jaccard / Top-K
评估指标 -> confusion matrix / accuracy / precision / recall
文本处理 -> 分词、词频、哈希、字符串
规则执行 -> SIM-03/04/05 解析器和解释器
SPJ 得分 -> baseline / metric / validation
计算图求导 -> forward / reverse backward
```

## AI 题型路由表

| AI 题面 | 本质模块 | 优先翻 |
|---|---|---|
| 机器人从起点到终点，格子有障碍/代价 | 图搜索 | `GRAPH-02/03`，`AI-01` |
| 启发式函数、估价函数、曼哈顿距离 | A* | `AI-01` |
| 双方轮流，最优行动 | 博弈搜索 / DP | `AI-01`，`DP-20` |
| 给训练集和测试集，按距离分类 | kNN | `AI-02` |
| 特征独立、条件概率、文本分类 | 朴素贝叶斯 | `AI-02` |
| 权重、学习率、训练轮数 | 感知机/线性模型 | `AI-02` |
| SVM、margin、hinge loss | 线性 SVM | `AI-11` |
| 文档相似、用户相似、向量夹角 | cosine/Jaccard | `AI-03` |
| Top-K 推荐 | 排序/堆 | `AI-03`，`CPP-004` |
| 分词、词频、关键词 | 字符串 + map | `AI-03`，`STR-01` |
| 混淆矩阵、准确率、召回率 | 模拟统计 | `AI-02/03` |
| Special Judge、误差、得分函数 | 指标 + baseline + 调参 | `AI-10` |
| 解析规则/脚本/配置 | 解析器/解释器 | `SIM-03/04/05` |
| TF-IDF、关键词检索 | 文本向量 | `AI-05` |
| 聚类中心、k-means | 无监督聚类 | `AI-06` |
| 连续值预测、MSE、gradient descent | 线性回归 | `AI-13` |
| Markov、HMM、观测序列 | 概率 DP | `AI-07` |
| 神经网络前向传播 | 矩阵向量公式 | `AI-08/12` |
| 反向传播、链式法则、参数更新 | 小网络训练模拟 | `AI-14` |
| 计算图、自动求导、偏导 | 反向模式自动微分 | `AI-15` |
| 状态、动作、奖励、策略 | MDP / RL | `AI-09` |

模板代码：

```cpp
#include <bits/stdc++.h>
using namespace std;

string route_ai_topic(const string &word) {
    if (word == "path" || word == "robot" || word == "astar") return "AI-01 / GRAPH";
    if (word == "game" || word == "minimax") return "AI-01 / DP";
    if (word == "knn" || word == "classify") return "AI-02";
    if (word == "similarity" || word == "recommend") return "AI-03";
    if (word == "spj" || word == "score" || word == "metric") return "AI-10";
    if (word == "svm" || word == "margin") return "AI-11";
    if (word == "dnn" || word == "forward") return "AI-12";
    if (word == "regression" || word == "mse") return "AI-13";
    if (word == "backprop" || word == "backward") return "AI-14";
    if (word == "autograd" || word == "gradient") return "AI-15";
    if (word == "json" || word == "script") return "SIM-04/05";
    return "ROUTE";
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string word;
    while (cin >> word) {
        cout << route_ai_topic(word) << '\n';
    }
    return 0;
}
```

调用示例：

```cpp
cout << route_ai_topic("knn") << '\n';
cout << route_ai_topic("robot") << '\n';
```

常见坑：

- AI 背景不等于要写复杂 AI；先翻译成算法关键词。
- 数据规模决定语言和算法，不由题目背景决定。
- 没有第三方库时，不要幻想 `numpy`、模型库、矩阵库。
- 小机器学习题常常就是“按公式模拟 + 排序/统计”。
- A* 的启发式必须不能高估真实代价，才能保证最短路正确。

暴力/部分分替代：

- 路径规划不会 A*：先 BFS/Dijkstra。
- 博弈不会剪枝：先 DFS 暴力小深度，再加记忆化。
- 分类不会模型：先多数类、最近 1 个样本、简单距离。
- 推荐不会复杂算法：先按共同物品数、Jaccard 或 cosine 排序。
- 文本题不会高级 NLP：先 split、词频、停用词特判。

最小测试样例：

```text
输入
knn
robot
script

输出
AI-02
AI-01 / GRAPH
SIM-04/05
```
