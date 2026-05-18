# STR-04 AC 自动机（低优先级）

模块编号：STR-04

模块名称：多模式串匹配 AC 自动机

标签：[字符串][AC自动机][多模式匹配][Trie][BFS][低优先级]

一句话用途：很多模式串同时在一个文本里匹配时，用 AC 自动机把 Trie 和 KMP 的失败指针思想合在一起，避免对每个模式串分别 KMP。

索引约定：

```text
Trie 节点编号从 0 开始，0 是根节点。
读入的第 i 个模式串仍然按题面 1-index 编号。
扫描 text 时，text 字符位置自然是 0-index；如果题目要输出题面位置，通常输出 pos + 1。
字符集默认小写 a-z。不是小写字母时，要先改映射。

回文相关不要在这里找，直接翻 STR-05 Manacher。
```

题面触发词：

- 给很多模式串，问它们在文本中出现次数。
- 敏感词过滤、关键词匹配、多关键词检索。
- 字典中任意单词是否出现在文章里。
- 多模式串总长度很大，逐个 KMP 会超时。

什么时候用：

- 模式串很多，总长度 `sumLen` 大，文本也长。
- 要统计所有模式总出现次数。
- 要判断文本是否包含任意模式串。
- 要做“禁止出现某些模式串”的 DP，AC 自动机可以作为状态转移图。

不要什么时候用：

- 只有一个模式串：KMP 更短。
- 只是前缀统计：Trie 更短。
- 字符集很大且题目很简单：先考虑 `map/unordered_map` 或逐个 KMP 拿部分分。
- 要求每个模式串分别出现次数：基础 AC 还不够，需要额外记录终点并做 fail 树/拓扑累加。

复杂度：

- 建 Trie：`O(模式串总长度)`。
- 建 fail：小写 26 字符集下 `O(节点数 * 26)`。
- 扫描文本：`O(|text|)`，如果要输出所有匹配位置，还要加输出量。

数据范围参考：

| 数据范围 | 建议 |
|---|---|
| 模式串数量少、文本短 | 暴力或 KMP 拿分 |
| 总模式长度 `<= 2e5` | AC 自动机稳 |
| 总模式长度 `<= 1e6` | 静态数组 AC 更稳；本模板用 vector，写法更短 |

输入如何整理：

```cpp
int m;
cin >> m;
AC ac;
ac.init();
for (int i = 1; i <= m; i++) {
    string p;
    cin >> p;
    ac.insert(p);
}
ac.build();
string text;
cin >> text;
cout << ac.count_matches(text) << "\n";
```

接口：

```text
AC.init()
AC.insert(pattern)
AC.build()
AC.count_matches(text) -> 所有模式串总出现次数
AC.contains_any(text) -> 是否出现任意模式串
```

模板代码：

```cpp
struct AC {
    struct Node {
        int nxt[26];
        int fail;
        int out;

        Node() {
            memset(nxt, 0, sizeof(nxt));
            fail = 0;
            out = 0;
        }
    };

    vector<Node> tr;
    bool built;

    void init() {
        tr.clear();
        tr.push_back(Node());
        built = false;
    }

    bool valid_lowercase(const string &s) const {
        for (char c : s) {
            int x = c - 'a';
            if (x < 0 || x >= 26) return false;
        }
        return true;
    }

    void insert(const string &s) {
        if (!valid_lowercase(s)) return;
        int u = 0;
        for (char c : s) {
            int x = c - 'a';
            if (!tr[u].nxt[x]) {
                tr[u].nxt[x] = (int)tr.size();
                tr.push_back(Node());
            }
            u = tr[u].nxt[x];
        }
        tr[u].out++;
    }

    void build() {
        if (built) return;
        built = true;
        queue<int> q;
        for (int c = 0; c < 26; c++) {
            int v = tr[0].nxt[c];
            if (v) q.push(v);
        }
        while (!q.empty()) {
            int u = q.front();
            q.pop();
            tr[u].out += tr[tr[u].fail].out;
            for (int c = 0; c < 26; c++) {
                int v = tr[u].nxt[c];
                if (v) {
                    tr[v].fail = tr[tr[u].fail].nxt[c];
                    q.push(v);
                } else {
                    tr[u].nxt[c] = tr[tr[u].fail].nxt[c];
                }
            }
        }
    }

    long long count_matches(const string &text) const {
        long long ans = 0;
        int u = 0;
        for (char ch : text) {
            int c = ch - 'a';
            if (c < 0 || c >= 26) {
                u = 0;
                continue;
            }
            u = tr[u].nxt[c];
            ans += tr[u].out;
        }
        return ans;
    }

    bool contains_any(const string &text) const {
        int u = 0;
        for (char ch : text) {
            int c = ch - 'a';
            if (c < 0 || c >= 26) {
                u = 0;
                continue;
            }
            u = tr[u].nxt[c];
            if (tr[u].out > 0) return true;
        }
        return false;
    }
};
```

完整可运行代码：

```cpp
#include <bits/stdc++.h>
using namespace std;

struct AC {
    struct Node {
        int nxt[26];
        int fail;
        int out;

        Node() {
            memset(nxt, 0, sizeof(nxt));
            fail = 0;
            out = 0;
        }
    };

    vector<Node> tr;
    bool built;

    void init() {
        tr.clear();
        tr.push_back(Node());
        built = false;
    }

    bool valid_lowercase(const string &s) const {
        for (char c : s) {
            int x = c - 'a';
            if (x < 0 || x >= 26) return false;
        }
        return true;
    }

    void insert(const string &s) {
        if (!valid_lowercase(s)) return;
        int u = 0;
        for (char c : s) {
            int x = c - 'a';
            if (!tr[u].nxt[x]) {
                tr[u].nxt[x] = (int)tr.size();
                tr.push_back(Node());
            }
            u = tr[u].nxt[x];
        }
        tr[u].out++;
    }

    void build() {
        if (built) return;
        built = true;
        queue<int> q;
        for (int c = 0; c < 26; c++) {
            int v = tr[0].nxt[c];
            if (v) q.push(v);
        }
        while (!q.empty()) {
            int u = q.front();
            q.pop();
            tr[u].out += tr[tr[u].fail].out;
            for (int c = 0; c < 26; c++) {
                int v = tr[u].nxt[c];
                if (v) {
                    tr[v].fail = tr[tr[u].fail].nxt[c];
                    q.push(v);
                } else {
                    tr[u].nxt[c] = tr[tr[u].fail].nxt[c];
                }
            }
        }
    }

    long long count_matches(const string &text) const {
        long long ans = 0;
        int u = 0;
        for (char ch : text) {
            int c = ch - 'a';
            if (c < 0 || c >= 26) {
                u = 0;
                continue;
            }
            u = tr[u].nxt[c];
            ans += tr[u].out;
        }
        return ans;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int m;
    cin >> m;
    AC ac;
    ac.init();
    for (int i = 1; i <= m; i++) {
        string p;
        cin >> p;
        ac.insert(p);
    }
    ac.build();

    string text;
    cin >> text;
    cout << ac.count_matches(text) << "\n";
    return 0;
}
```

调用示例：

```cpp
AC ac;
ac.init();
ac.insert("he");
ac.insert("she");
ac.insert("hers");
ac.build();
cout << ac.count_matches("shers") << "\n"; // 3
```

常见坑：

- 本模板默认只支持小写字母；字符集不同要改 `nxt[26]` 和 `c - 'a'`。
- `out` 通过 fail 累加后，`count_matches` 统计的是所有模式总出现次数。
- 如果题目问“每个模式串分别出现几次”，要保存每个模式的终点节点，扫描后对节点访问次数沿 fail 树累加。
- 如果模式串里有重复，`out++` 会把重复模式也计入总匹配次数。
- 文本中遇到非小写字符时，本模板回到根节点。

暴力/部分分替代：

- 模式串少：每个模式暴力匹配或 KMP。
- 只问是否出现任意一个：逐个 `text.find(pattern)` 先拿小数据。
- 字符集复杂：先用 `unordered_map<char,int>` 写 Trie 或直接暴力拿分。

升级方向：

- AC + DP：统计不含敏感词的字符串数量。
- AC + fail 树：统计每个模式串出现次数。
- AC + 拓扑累加：把扫描命中的节点次数传给 fail 祖先。

最小测试样例：

```text
输入：
3
he
she
hers
shers

输出：
3
```
