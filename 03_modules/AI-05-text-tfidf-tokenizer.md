# AI-05 文本处理、词频与 TF-IDF

模块编号：AI-05

模块名称：文本分词、词频统计、TF-IDF 与文档相似度

标签：AI、NLP、文本处理、TF-IDF、词频、文档相似度、C++17

一句话用途：当题目给文档、查询、关键词或相似文本时，用分词 + 词频 + TF-IDF + cosine 把自然语言题变成字符串和向量题。

题面触发词：

- 文档、查询、关键词、词频、倒排索引。
- TF、IDF、TF-IDF。
- 文本相似度、最相关文档。
- 忽略大小写、去掉标点、按非字母数字切词。

什么时候用：

- 题面给了英文文本或已经分好的 token。
- 需要统计词频、文档频率、关键词分数。
- 要按查询文本找最相似文档。

不要什么时候用：

- 中文复杂分词、语义理解、词向量训练，不适合手写。
- 题面如果给了自己的分词规则，以题面为准。
- 文档极大时，要注意 map 和字符串内存。

复杂度：

- 分词：`O(总字符数)`。
- 统计词频：`O(总 token 数 * log 词典)`，用 map。
- 查询所有文档：`O(文档数 * 查询词数)` 或按实现略高。

依赖的标准容器：

- `string`
- `vector<string>`
- `map<string,int>`
- `set<string>`
- `vector<map<string,int>>`

输入如何整理：

```cpp
int n;
cin >> n;
string line;
getline(cin, line);
for (int i = 1; i <= n; i++) getline(cin, doc[i]);
getline(cin, query);
```

接口：

```text
tokenize(line) -> 小写 token 列表。
tfidf_cosine(doc_count, query_count, df, n) -> 相似度。
```

模板代码：

```cpp
#include <bits/stdc++.h>
using namespace std;

vector<string> tokenize(const string &s) {
    vector<string> words;
    string cur;
    for (char ch : s) {
        unsigned char c = (unsigned char)ch;
        if (isalnum(c)) {
            cur.push_back((char)tolower(c));
        } else if (!cur.empty()) {
            words.push_back(cur);
            cur.clear();
        }
    }
    if (!cur.empty()) words.push_back(cur);
    return words;
}

map<string, int> count_words(const vector<string> &words) {
    map<string, int> cnt;
    for (const string &w : words) cnt[w]++;
    return cnt;
}

double tfidf_cosine(const map<string, int> &a, const map<string, int> &b, const map<string, int> &df, int n) {
    map<string, double> va, vb;
    for (auto [w, c] : a) {
        int dfi = df.count(w) ? df.at(w) : 0;
        double idf = log((double)(n + 1) / (dfi + 1)) + 1;
        va[w] = c * idf;
    }
    for (auto [w, c] : b) {
        int dfi = df.count(w) ? df.at(w) : 0;
        double idf = log((double)(n + 1) / (dfi + 1)) + 1;
        vb[w] = c * idf;
    }

    double dot = 0;
    double na = 0;
    double nb = 0;
    for (auto [w, x] : va) {
        na += x * x;
        if (vb.count(w)) dot += x * vb[w];
    }
    for (auto [w, y] : vb) nb += y * y;
    if (na == 0 || nb == 0) return 0;
    return dot / sqrt(na * nb);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    string line;
    getline(cin, line);

    vector<map<string, int>> docs(n + 1);
    map<string, int> df;
    for (int i = 1; i <= n; i++) {
        getline(cin, line);
        docs[i] = count_words(tokenize(line));
        for (auto [w, c] : docs[i]) df[w]++;
    }

    string query_line;
    getline(cin, query_line);
    map<string, int> query = count_words(tokenize(query_line));

    int best_id = 1;
    double best_score = -1;
    for (int i = 1; i <= n; i++) {
        double score = tfidf_cosine(docs[i], query, df, n);
        if (score > best_score + 1e-12) {
            best_score = score;
            best_id = i;
        }
    }

    cout << fixed << setprecision(6) << best_id << ' ' << best_score << '\n';
    return 0;
}
```

调用示例：

```cpp
vector<string> words = tokenize("Apple, banana! apple");
auto cnt = count_words(words);
```

常见坑：

- 大小写是否敏感看题面；本模板默认转小写。
- TF 是否除以文档长度看题面；本模板用原始词频。
- IDF 公式版本很多，以题面为准。
- 查询词不在任何文档中时，本模板仍给它一个平滑 IDF。
- 相似度相同默认保留编号小的文档。

暴力/部分分替代：

- 不会 TF-IDF：先按共同词数量排序。
- 不会 cosine：先按点积排序。
- 文本太大：先只处理题目要求的关键词。

最小测试样例：

```text
输入
2
apple banana
cat dog
apple

输出
1 0.707107
```

