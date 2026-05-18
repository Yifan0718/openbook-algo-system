# STR-03 Trie 与 Rolling Hash

模块编号：STR-03

模块名称：Trie 字典树与字符串 Rolling Hash

标签：[字符串][Trie][Hash][0-index][前缀]

一句话用途：Trie 维护大量字符串前缀，Rolling Hash 用 `O(1)` 判断子串相等。

索引约定：

```text
Trie 逐字符扫描 string，字符位置使用 0-index。
Rolling Hash 的字符串 s 是 0-index，但哈希前缀数组 h/pw 使用 1-index：
  h[i+1] 表示 s[0..i] 的哈希。
  get(l,r) 接收 0-index 闭区间 [l,r]。
若题面给 1-index 闭区间 [l,r]，调用 get(l-1, r-1)。
```

题面触发词：

- 前缀、字典、单词集合。
- 插入字符串、查询某前缀出现次数。
- 大量判断两个子串是否相同。
- 最长公共前缀、字符串去重。
- 子串哈希、滚动哈希。

什么时候用：

- Trie：很多字符串共享前缀，或要统计前缀数量。
- Hash：多次询问 `s[l1..r1] == s[l2..r2]`。
- 需要二分 LCP 时，Hash 可快速比较子串。

不要什么时候用：

- Trie 字符集很大且节点数爆炸时，要改用 `map/unordered_map` 子边或排序。
- Hash 有碰撞风险，严谨题要双哈希。
- 单次子串比较，小数据直接 `substr` 更稳。
- 多模式串在文本中匹配，Trie 只能做前缀，完整多模式匹配看 AC 自动机。

复杂度：

- Trie 插入/查询：`O(字符串长度)`。
- Hash 预处理：`O(n)`。
- Hash 子串查询：`O(1)`。

数据范围参考：

- 总字符数 `<= 1e6`：Trie 数组节点可用。
- `|s|, q <= 2e5`：Rolling Hash 常用。

依赖的标准容器：

- `vector<array<int,26>>` 或节点结构。
- `vector<ll> h, pw`。
- 字符串内部 0-index，Hash 前缀数组 1-index。

输入如何整理：

```cpp
int n;
cin >> n;
Trie trie;
trie.init();
for (int i = 1; i <= n; i++) {
    string s;
    cin >> s;
    trie.insert(s);
}
```

接口：

```text
Trie.init()
Trie.insert(s)
Trie.count_word(s)
Trie.count_prefix(s)
RollingHash.build(s)
RollingHash.get(l,r) -> 0-index 闭区间哈希
RollingHash.same(l1,r1,l2,r2)
```

输出能力：

- 单词出现次数。
- 前缀出现次数。
- 子串相等判断。
- 可辅助 LCP、回文判断、去重。

下游可接：

- 字典序 DFS。
- 二分答案 + Hash。
- AC 自动机。
- 字符串 DP。

可拼接模块：

- STR-01 基础操作。
- STR-02 KMP/Z。
- STR-04 AC 自动机。
- STR-05 Manacher。
- 二分答案。

模板代码：

```cpp
struct Trie {
    struct Node {
        array<int, 26> nxt{};
        int pass = 0;
        int end = 0;
    };

    vector<Node> tr;

    void init() {
        tr.clear();
        tr.push_back(Node());
    }

    bool valid_lowercase(const string &s) const {
        for (char c : s) {
            int x = c - 'a';
            if (x < 0 || x >= 26) return false;
        }
        return true;
    }

    void insert(const string &s) {
        if (!valid_lowercase(s)) return; // 默认小写；其他字符集先改映射。
        int u = 0;
        tr[u].pass++;
        for (char c : s) {
            int x = c - 'a';
            if (tr[u].nxt[x] == 0) {
                tr[u].nxt[x] = (int)tr.size();
                tr.push_back(Node());
            }
            u = tr[u].nxt[x];
            tr[u].pass++;
        }
        tr[u].end++;
    }

    int count_word(const string &s) const {
        int u = 0;
        for (char c : s) {
            int x = c - 'a';
            if (x < 0 || x >= 26) return 0;
            if (tr[u].nxt[x] == 0) return 0;
            u = tr[u].nxt[x];
        }
        return tr[u].end;
    }

    int count_prefix(const string &s) const {
        int u = 0;
        for (char c : s) {
            int x = c - 'a';
            if (x < 0 || x >= 26) return 0;
            if (tr[u].nxt[x] == 0) return 0;
            u = tr[u].nxt[x];
        }
        return tr[u].pass;
    }
};

struct RollingHash {
    static const long long MOD = 1000000007LL;
    static const long long BASE = 911382323LL;
    vector<long long> h, pw;

    void build(const string &s) {
        int n = (int)s.size();
        h.assign(n + 1, 0);
        pw.assign(n + 1, 1);
        for (int i = 0; i < n; i++) {
            h[i + 1] = (h[i] * BASE + (unsigned char)s[i] + 1) % MOD;
            pw[i + 1] = pw[i] * BASE % MOD;
        }
    }

    long long get(int l, int r) const {
        if (l > r) return 0;
        if (l < 0 || r + 1 >= (int)h.size()) return -1;
        long long res = (h[r + 1] - h[l] * pw[r - l + 1]) % MOD;
        if (res < 0) res += MOD;
        return res;
    }

    bool same(int l1, int r1, int l2, int r2) const {
        if (r1 - l1 != r2 - l2) return false;
        long long a = get(l1, r1);
        long long b = get(l2, r2);
        if (a < 0 || b < 0) return false;
        return a == b;
    }
};
```

调用示例：

```cpp
Trie trie;
trie.init();
trie.insert("apple");
trie.insert("app");
cout << trie.count_prefix("app") << "\n"; // 2

string s = "abacaba";
RollingHash rh;
rh.build(s);
cout << rh.same(0, 2, 4, 6) << "\n"; // aba == aba

// 题面 1-index [l,r]
int l = 1, r = 3;
cout << rh.get(l - 1, r - 1) << "\n";
```

常见坑：

- Trie 模板默认只支持 `'a'..'z'`，其他字符要改字符映射；模板里加了越界防御，避免数组炸掉。
- Trie 的 `0` 是根节点，所以子边用 `0` 表示不存在，新节点编号从 1 开始。
- Hash 存在碰撞，严谨时用双模数或 `unsigned long long` 双保险。
- Hash 的 `get(l,r)` 是 0-index 闭区间。
- `BASE` 要小于 `MOD`，并尽量选大一点的随机奇数。

暴力/部分分替代：

- 前缀查询小数据：把所有单词存 `vector<string>`，逐个比较前缀。
- 子串相等小数据：直接 `s.substr(l,len)==s.substr(l2,len)`。
- 去重小数据：直接 `set<string>` 存真实子串。

升级方向：

- 多模式串在长文本中出现 -> AC 自动机。
- Hash 碰撞风险 -> 双哈希。
- 字符集大 -> Trie 子边改 `map<char,int>`。

最小测试样例：

```text
insert apple, app
count_word(app)=1
count_prefix(app)=2

s=abacaba
same(0,2,4,6)=true
题面 [1,3] 要调用 get(0,2)
```
