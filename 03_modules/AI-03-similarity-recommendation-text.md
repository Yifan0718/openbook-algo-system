# AI-03 相似度、推荐与文本向量

模块编号：AI-03

模块名称：Cosine、Jaccard、混淆矩阵与 Top-K 推荐

标签：AI、相似度、推荐、文本、向量、Cosine、Jaccard、Top-K、C++17

一句话用途：当题目要求计算用户相似、文档相似、向量相似、推荐 Top-K 或评估预测结果时，用本模块把 AI 背景化成排序、集合和向量运算。

题面触发词：

- 相似度、余弦相似度、夹角、向量。
- Jaccard、交集、并集、共同兴趣。
- 推荐、Top-K、最相似用户、最相关文档。
- 词频、关键词、文本向量。
- 准确率、混淆矩阵、预测标签。

什么时候用：

- 特征已经给成向量或集合。
- 文本可以按空格切词统计词频。
- 推荐规则就是按相似度排序。
- 指标按公式计算，不需要真正训练模型。

不要什么时候用：

- 不要实现复杂深度语义模型、词向量训练、神经网络。
- 文本分词如果涉及中文自然语言复杂规则，按题面给的分词规则走。
- 向量维度和样本数都很大时，注意 `O(n*d)` 是否可承受。

复杂度：

- cosine：`O(d)`。
- Jaccard：排序后 `O(n+m)`，或 set 统计。
- Top-K：全排序 `O(n log n)`，堆可 `O(n log k)`。
- 混淆矩阵：`O(q)`。

依赖的标准容器：

- `vector<double>`：向量。
- `vector<int>`：集合元素、标签。
- `map<string,int>`：词频。
- `priority_queue`：Top-K。

输入如何整理：

```cpp
int d;
cin >> d;
vector<double> a(d + 1), b(d + 1);
for (int i = 1; i <= d; i++) cin >> a[i];
for (int i = 1; i <= d; i++) cin >> b[i];
```

接口：

```text
cosine(a,b,d) -> 余弦相似度。
jaccard(A,B) -> 集合 Jaccard，相同元素先去重。
```

模板代码：

```cpp
#include <bits/stdc++.h>
using namespace std;

double cosine_similarity(const vector<double> &a, const vector<double> &b, int d) {
    double dot = 0;
    double na = 0;
    double nb = 0;
    for (int i = 1; i <= d; i++) {
        dot += a[i] * b[i];
        na += a[i] * a[i];
        nb += b[i] * b[i];
    }
    if (na == 0 || nb == 0) return 0;
    return dot / sqrt(na * nb);
}

double jaccard_similarity(vector<int> a, vector<int> b) {
    sort(a.begin() + 1, a.end());
    sort(b.begin() + 1, b.end());
    a.erase(unique(a.begin() + 1, a.end()), a.end());
    b.erase(unique(b.begin() + 1, b.end()), b.end());

    int i = 1;
    int j = 1;
    int inter = 0;
    int uni = 0;

    while (i < (int)a.size() || j < (int)b.size()) {
        if (j >= (int)b.size() || (i < (int)a.size() && a[i] < b[j])) {
            uni++;
            i++;
        } else if (i >= (int)a.size() || b[j] < a[i]) {
            uni++;
            j++;
        } else {
            inter++;
            uni++;
            i++;
            j++;
        }
    }

    if (uni == 0) return 0;
    return (double)inter / uni;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string mode;
    cin >> mode;

    cout << fixed << setprecision(6);
    if (mode == "cosine") {
        int d;
        cin >> d;
        vector<double> a(d + 1), b(d + 1);
        for (int i = 1; i <= d; i++) cin >> a[i];
        for (int i = 1; i <= d; i++) cin >> b[i];
        cout << cosine_similarity(a, b, d) << '\n';
    } else if (mode == "jaccard") {
        int n, m;
        cin >> n >> m;
        vector<int> a(n + 1), b(m + 1);
        for (int i = 1; i <= n; i++) cin >> a[i];
        for (int i = 1; i <= m; i++) cin >> b[i];
        cout << jaccard_similarity(a, b) << '\n';
    } else if (mode == "confusion") {
        int c, q;
        cin >> c >> q;
        vector<vector<int>> mat(c + 1, vector<int>(c + 1, 0));
        int correct = 0;
        for (int i = 1; i <= q; i++) {
            int real_label, pred_label;
            cin >> real_label >> pred_label;
            mat[real_label][pred_label]++;
            if (real_label == pred_label) correct++;
        }
        cout << (double)correct / q << '\n';
        for (int i = 1; i <= c; i++) {
            for (int j = 1; j <= c; j++) {
                if (j > 1) cout << ' ';
                cout << mat[i][j];
            }
            cout << '\n';
        }
    }

    return 0;
}
```

## Top-K 推荐套路

```text
对每个候选 item 计算 score
按 score 降序、id 升序排序
输出前 k 个
```

如果候选很多：

```text
priority_queue 保留前 k 个
```

## 文本向量套路

```text
1. 按题面规则切词。
2. map<string,int> 统计词频。
3. 统一词典后变成向量。
4. 用 cosine/Jaccard 比较。
```

调用示例：

```cpp
// double sim = cosine_similarity(a, b, d);
// double jac = jaccard_similarity(A, B);
```

常见坑：

- cosine 分母为 0 时要防御。
- Jaccard 要先去重；多重集合相似度是另一种题。
- 相似度排序要写清楚 tie-break，常见是分数高优先、id 小优先。
- 文本大小写、标点、停用词都按题面规则处理，不要自行脑补。
- `double` 输出按题目要求设置精度。

暴力/部分分替代：

- 推荐不会优化：先全排序。
- 文本不会建完整向量：先统计共同词数。
- cosine 不会：先用点积排序，有些数据可拿部分分。
- 混淆矩阵不会高级指标：先输出矩阵和 accuracy。

最小测试样例：

```text
输入
cosine
3
1 0 1
1 1 0

输出
0.500000
```

补充自测：

```text
输入
jaccard
4 5
1 2 2 3
2 3 4 4 5

输出
0.400000
```

补充自测 2：

```text
输入
confusion
3 5
1 1
1 2
2 2
3 1
3 3

输出
0.600000
1 1 0
0 1 0
1 0 1
```

