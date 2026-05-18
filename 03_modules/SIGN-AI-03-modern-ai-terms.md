# SIGN-AI-03 现代 AI 术语、向量检索与 Transformer 常识

模块编号：SIGN-AI-03

模块名称：现代 AI 术语速查：Token、Embedding、Attention、Transformer、RAG、向量相似度和训练评估

标签：签到题、AI原理、现代AI、Token、Embedding、Attention、Transformer、RAG、向量检索、C++17

一句话用途：题面出现大模型、向量检索、注意力机制、RAG、嵌入向量、训练/推理等现代 AI 词汇时，用本模块把概念翻译成可计算的字符串、向量、矩阵、排序和统计问题。

题面触发词：

- token、词元、分词、词表、embedding、词向量、向量相似度。
- attention、self-attention、query/key/value、Transformer。
- RAG、检索增强生成、向量数据库、Top-K 相似文档。
- 训练集、验证集、测试集、数据泄漏、泛化、过拟合。
- 参数、超参数、batch、epoch、learning rate、optimizer。
- 大语言模型、prompt、上下文窗口、幻觉、temperature。

什么时候用：

- 题目要求判断 AI 术语关系，或者给小向量/小矩阵要求算一次结果。
- 题目给多个文本或向量，要求按相似度排序或选 Top-K。
- 题目描述 RAG/推荐系统/检索系统，但实质是字符串处理、词频统计、余弦相似度和排序。
- 题目要求模拟 attention 的一小步计算。

不要什么时候用：

- 如果题面只是普通分类指标，优先翻 `SIGN-ML-01`。
- 如果题面给完整神经网络和梯度，优先翻第 10 卷的前向传播、反向传播和自动求导。
- 不要现场实现真实深度学习训练框架；上机题通常只会考小规模公式模拟。
- 不要使用第三方库、联网模型或在线 API。

复杂度：

- 文本分词和计数：`O(总字符数)` 或 `O(总词数)`。
- 向量余弦相似度：每对 `O(d)`。
- Top-K 检索：排序 `O(n log n)`，堆 `O(n log k)`。
- 简化 attention：`O(n^2*d)`，其中 `n` 是 token 数，`d` 是向量维度。

依赖的标准容器：

- `string`：文本和 token。
- `map<string,int>` 或 `unordered_map<string,int>`：词频、词表编号。
- `vector<double>`：向量。
- `priority_queue`：Top-K。
- 静态数组：小矩阵计算时更容易 1-index。

输入如何整理：

```text
1. 文本题：先决定分隔方式，是按空格、字符、还是题面给定规则分词。
2. 向量题：把每个样本编号为 1..n，每个维度编号为 1..d。
3. 检索题：对每个候选算 score，再排序或用堆取 Top-K。
4. Transformer/attention 题：按题面公式逐步算 Q、K、V、score、softmax、加权和。
```

接口：

```text
cosine(a,b,d) -> 两个向量余弦相似度。
softmax(x,n) -> 把分数转成概率。
top_k_by_score(items,k) -> 取分数最大的 k 项。
attention_one_query(q,K,V,n,d) -> 单个 query 对 n 个 key/value 做注意力。
```

常见坑：

- embedding 不是一个词本身，而是词/文本对应的数值向量。
- 余弦相似度要除以两个向量长度；零向量要特判。
- softmax 要减去最大值防止 `exp` 溢出。
- 训练集用于学习参数，验证集用于调超参数，测试集用于最终评估。
- 数据泄漏是把测试信息提前用于训练或调参，会导致虚高分。
- temperature 越大输出越随机，越小越确定；但竞赛题一般只要求按题面公式模拟。
- RAG 本身不神秘：先检索相关资料，再把资料放入生成模型上下文。

暴力/部分分替代：

- 不会复杂 embedding 时，用词频向量、0/1 出现向量或 Jaccard 相似度。
- Top-K 不会堆时，直接排序。
- attention 不会矩阵化时，按三层循环逐项算。
- 题面数据很小，直接用 `map<string,int>` 和 `vector<double>`，常数足够。

## 1. 现代 AI 术语翻译表

| 术语 | 考场理解 |
|---|---|
| token | 模型处理的最小单位，可能是字、词、子词或符号 |
| tokenizer | 把文本切成 token 的规则或算法 |
| vocabulary | token 到编号的映射表 |
| embedding | token/文本/图片映射成向量 |
| context window | 一次能放进模型的 token 上限 |
| prompt | 输入给模型的指令和上下文 |
| inference | 用训练好的模型预测 |
| pretraining | 大规模预训练 |
| fine-tuning | 在特定数据上继续训练 |
| alignment | 让模型行为更符合人类偏好 |
| hallucination | 生成看似合理但不真实的内容 |
| RAG | 检索资料 + 生成回答 |
| vector database | 存向量并做相似度搜索 |
| multimodal | 文本、图像、音频等多模态 |

## 2. 训练、验证、测试

| 集合 | 用途 | 能否调参 |
|---|---|---|
| 训练集 | 更新模型参数 | 可以 |
| 验证集 | 选模型、调超参数、早停 | 可以间接用 |
| 测试集 | 最终报告性能 | 不应参与调参 |

常见问法：

```text
模型在训练集 99%，测试集 60% -> 过拟合。
训练集和测试集都很低 -> 欠拟合或特征不足。
用测试集挑模型 -> 数据泄漏。
```

参数和超参数：

| 名称 | 例子 | 谁决定 |
|---|---|---|
| 参数 | 权重 `w`、偏置 `b` | 训练学出来 |
| 超参数 | 学习率、层数、kNN 的 k、正则强度 | 人或搜索过程指定 |

## 3. 向量相似度

常用公式：

```text
dot(a,b) = sum a[i]*b[i]
cos(a,b) = dot(a,b) / (sqrt(sum a[i]^2) * sqrt(sum b[i]^2))
euclidean(a,b) = sqrt(sum (a[i]-b[i])^2)
manhattan(a,b) = sum abs(a[i]-b[i])
```

什么时候用：

| 题面 | 常见距离 |
|---|---|
| 文本向量相似 | cosine |
| 几何坐标最近 | Euclidean |
| 网格/街区距离 | Manhattan |
| 集合相似 | Jaccard |

余弦相似度模板：

```cpp
double cosine(double a[], double b[], int d) {
    double dot = 0, na = 0, nb = 0;
    for (int i = 1; i <= d; i++) {
        dot += a[i] * b[i];
        na += a[i] * a[i];
        nb += b[i] * b[i];
    }
    if (na == 0 || nb == 0) return 0;
    return dot / sqrt(na) / sqrt(nb);
}
```

## 4. Top-K 检索完整代码

输入 `n d k`，再输入查询向量和 `n` 个候选向量，输出余弦相似度最高的 `k` 个编号。

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MAXN = 1005;
const int MAXD = 105;

int n, d, k;
double qv[MAXD], vec[MAXN][MAXD];

double cosine_one(int id) {
    double dot = 0, nq = 0, nv = 0;
    for (int j = 1; j <= d; j++) {
        dot += qv[j] * vec[id][j];
        nq += qv[j] * qv[j];
        nv += vec[id][j] * vec[id][j];
    }
    if (nq == 0 || nv == 0) return 0;
    return dot / sqrt(nq) / sqrt(nv);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n >> d >> k;
    for (int j = 1; j <= d; j++) cin >> qv[j];
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= d; j++) cin >> vec[i][j];
    }

    vector<pair<double,int>> score;
    for (int i = 1; i <= n; i++) score.push_back({cosine_one(i), i});
    sort(score.begin(), score.end(), [](const pair<double,int> &a, const pair<double,int> &b) {
        if (fabs(a.first - b.first) > 1e-12) return a.first > b.first;
        return a.second < b.second;
    });

    for (int i = 0; i < k && i < (int)score.size(); i++) {
        cout << score[i].second << (i + 1 == k || i + 1 == (int)score.size() ? '\n' : ' ');
    }
    return 0;
}
```

最小测试：

```text
输入：
3 2 2
1 0
1 0
0 1
1 1

输出：
1 3
```

## 5. Softmax

用途：

- 把一组分数转成概率。
- 多分类最后一层常用。
- attention 中把相似度分数转成权重。

稳定写法：

```cpp
void softmax(double x[], double p[], int n) {
    double mx = x[1];
    for (int i = 2; i <= n; i++) mx = max(mx, x[i]);
    double sum = 0;
    for (int i = 1; i <= n; i++) {
        p[i] = exp(x[i] - mx);
        sum += p[i];
    }
    for (int i = 1; i <= n; i++) p[i] /= sum;
}
```

为什么减最大值：

```text
exp(1000) 会溢出。
softmax(x) 与 softmax(x - max(x)) 结果相同。
```

## 6. Attention 最小模型

给一个 query `q`，多个 key `K[i]` 和 value `V[i]`：

```text
score[i] = dot(q, K[i]) / sqrt(d)
weight = softmax(score)
out = sum_i weight[i] * V[i]
```

口令：

```text
Q 问“我要找什么”，K 表示“我有什么标签”，V 表示“真正取走的信息”。
```

简化模板：

```cpp
const int MAXN = 105;
const int MAXD = 105;
double q[MAXD], key[MAXN][MAXD], val[MAXN][MAXD];
double score[MAXN], w[MAXN], out[MAXD];

void attention_one_query(int n, int d) {
    for (int i = 1; i <= n; i++) {
        score[i] = 0;
        for (int j = 1; j <= d; j++) score[i] += q[j] * key[i][j];
        score[i] /= sqrt((double)d);
    }
    softmax(score, w, n);
    for (int j = 1; j <= d; j++) out[j] = 0;
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= d; j++) out[j] += w[i] * val[i][j];
    }
}
```

## 7. Transformer 常识

| 部件 | 作用 |
|---|---|
| token embedding | 把 token 编号变成向量 |
| positional encoding | 给序列位置信息 |
| self-attention | 每个 token 看其他 token |
| multi-head | 多组 attention 并行关注不同关系 |
| feed-forward | 每个位置独立的小网络 |
| residual | 残差连接，缓解训练困难 |
| layer norm | 层归一化，稳定训练 |

考场判断：

```text
Transformer 的核心不是 RNN，而是 self-attention。
自注意力可以并行处理序列，但标准注意力有 O(n^2) 序列长度开销。
```

## 8. RAG 题型拆解

RAG 流程：

```text
query -> 编码成向量 -> 检索 Top-K 文档 -> 拼接上下文 -> 生成答案
```

可能考法：

| 考法 | 实际操作 |
|---|---|
| 给查询和文档向量，选最相关文档 | 余弦相似度排序 |
| 给词频，算相似度 | TF/TF-IDF + cosine |
| 给多个候选答案和证据分 | 按加权得分排序 |
| 判断 RAG 优点 | 可引入外部资料、缓解知识过期 |
| 判断 RAG 风险 | 检索错、上下文太长、仍可能幻觉 |

## 9. 生成模型参数常识

| 参数 | 含义 |
|---|---|
| temperature | 随机性，越高越发散 |
| top-k | 只在概率最高的 k 个 token 中采样 |
| top-p | 只在累计概率达到 p 的候选中采样 |
| max tokens | 最大生成长度 |

竞赛题如果给出这些参数，通常会把概率表也给出，让你按规则采样或选最大概率。若题目要求确定输出，一般会规定取概率最大或给随机数序列。

## 10. 与 Markov 性质的关系

现代 AI 中经常出现“只看当前状态”的简化：

| 场景 | Markov 化方式 |
|---|---|
| 强化学习 | 状态必须包含决策所需信息 |
| 文本生成 | 下一个 token 由当前上下文决定 |
| HMM | 隐状态按 Markov 链转移 |
| 递归/DP | 状态包含未来所需的全部历史摘要 |

如果题目说“下一步还依赖上一步动作/前两个字符/上一轮输出”，就把这些历史并入状态，和 `SIGN-MARKOV-01` 的升维思想一致。

