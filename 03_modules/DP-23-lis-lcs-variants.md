# DP-23：LIS/LCS 常见变体速查

模型编号：DP-23

模型名称：LIS/LCS 常见变体速查

标签：DP、LIS、LCS、子序列、路径恢复、变体路由

一句话用途：把“最长递增子序列”和“最长公共子序列”的常见变体集中到一张卡，考场上先判别变体，再抄对应短模板。

题面触发词：

- “最长递增/上升/不下降子序列”
- “最长公共子序列/公共子串”
- “删除最少字符使序列递增/两个串相同”
- “输出一个方案”
- “有多少个最长方案”
- “二维偏序、信封嵌套、最多能选多少个”

什么时候用：

- 题目要求保持原相对顺序，但不要求连续。
- 一个序列内部比较大小，优先看 LIS。
- 两个序列之间做公共匹配，优先看 LCS。
- 需要输出路径、统计方案数或处理重复值时，先查本卡的变体表。

不要什么时候用：

- 要求连续子段/子串，不能直接套 LIS/LCS。
- 允许插入、删除、替换三种操作并问最少次数，优先看编辑距离。
- 有容量、预算、次数限制时，可能要和背包/线性 DP 拼接。
- 需要在线修改序列，普通 LIS/LCS 表不适合直接维护。

复杂度：

- 朴素 LIS：`O(n^2)`。
- 二分 LIS：`O(n log n)`。
- 普通 LCS：`O(nm)`。
- LCS 滚动数组：`O(nm)` 时间，`O(m)` 空间。
- 计数/带权 LIS：常用树状数组/SegmentTree，`O(n log n)`。

数据范围信号：

- `n <= 5000`：朴素 LIS 或 LCS 常可交。
- `n <= 2e5` 且只求 LIS 长度：二分优化。
- `n,m <= 3000/5000`：普通 LCS。
- `n,m >= 1e5`：普通 LCS 大概率不行，先看是否有特殊字符集、短串或别的结构。

依赖的标准容器：

- `vector<int> dp, pre, tail_idx`
- `vector<ll> a`
- `string s, t`
- `vector<vector<int>> lcs_dp`

输入如何整理：

- LIS：数组推荐读成 `vector<ll> a(n + 1)`，1-index。
- LCS：字符串保持 0-index，但 DP 表用前缀长度 `i/j`，访问 `s[i-1]`。
- 二维偏序：把点整理成 `(x,y)`，先排序，再对 `y` 做 LIS。

接口：

```cpp
int lis_strict_length(const vector<ll>& a);
int lnds_length(const vector<ll>& a);
string restore_lcs(const string& s, const string& t);
```

输出能力：

- LIS/LNDS 长度。
- 输出一条 LIS 或 LCS。
- 最长公共子串长度。
- 二维偏序最大链长度。
- 最少删除次数类答案。

下游可接：

- DP-11 LIS
- DP-09 LCS
- DP-10/22 编辑距离
- DP-18 DP + 树状数组/SegmentTree 优化

可拼接模块：

- Compressor：带权/计数 LIS 的值域压缩。
- 树状数组/SegmentTree：求前缀最大值或方案数。
- Sorting：二维偏序先排序。

## 1. 变体路由表

| 题面 | 模型 | 关键区别 |
|---|---|---|
| 最长严格递增子序列 | LIS | 二分用 `lower_bound` |
| 最长不下降子序列 | LNDS | 二分用 `upper_bound` |
| 求一条具体 LIS | LIS + 前驱 | `d` 只给长度，要另存前驱 |
| 求 LIS 方案数 | DP/树状数组 | 状态存 `{长度, 方案数}` |
| 每个元素有收益，递增且收益最大 | 带权 LIS | `dp[i]=w[i]+max(dp[j])` |
| 二维点 `(x,y)` 最长链 | 排序 + 一维 LIS | 第一维升序，第二维按规则处理重复 |
| 最少删除使序列递增 | `n - LIS` | 看严格还是不下降 |
| 两个序列最长公共子序列 | LCS | 不要求连续 |
| 两个字符串最长公共子串 | 公共子串 DP | 不相等时清零 |
| 只允许删除使两串相同 | LCS | 删除次数 `n + m - 2*lcs` |
| 最短公共超序列长度 | LCS | `n + m - lcs` |
| 两个序列最长公共上升子序列 | LCIS | 扫描第二个序列维护可接到当前 `a[i]` 的 best |

## 1A. 变体建模口令

LIS/LCS 变体最容易“看着像模板，实际状态没想清楚”。每次套模板前先补三句话：

```text
1. 状态是什么：以哪里结尾？处理到哪个前缀？是否还要记住长度/方案数/最后值？
2. 最后一步是什么：最后选了哪个元素？最后匹配了哪两个字符？最后一个公共元素是谁？
3. 答案在哪里：max(dp[i])、dp[n][m]、还是 max(dp[j])？
```

常用模型对照：

| 模型 | 状态来源 | 最后一步 | 答案 |
|---|---|---|---|
| LIS `O(n^2)` | `dp[i]` 以第 `i` 个数结尾 | 从某个 `j<i,a[j]<a[i]` 接到 `i` | `max dp[i]` |
| LCS | `dp[i][j]` 两个前缀 | `s[i]` 与 `t[j]` 匹配或跳过一边 | `dp[n][m]` |
| 公共子串 | `dp[i][j]` 以 `s[i],t[j]` 同时结尾 | 相等就从左上延长，不等清零 | `max dp[i][j]` |
| LCIS | `dp[j]` 以 `b[j]` 结尾且已处理当前 `a` 前缀 | 当前 `a[i]` 匹配某个 `b[j]` | `max dp[j]` |

如果说不清“以哪里结尾”，优先写暴力 DFS 或二维表推，不要直接抄二分 LIS。

## 2. LIS 严格/不下降短模板

注意：本卡的序列函数默认 `a[1..n]`，调用时要保留 `a[0]` 这个 dummy 位，例如 `vector<ll> a(n + 1)`。如果你把普通 0-index `vector` 直接传进来，会漏掉第一个元素。

```cpp
int lis_strict_length(const vector<ll>& a) {
    int n = (int)a.size() - 1;
    vector<ll> d;
    for (int i = 1; i <= n; i++) {
        auto it = lower_bound(d.begin(), d.end(), a[i]);
        if (it == d.end()) d.push_back(a[i]);
        else *it = a[i];
    }
    return (int)d.size();
}

int lnds_length(const vector<ll>& a) {
    int n = (int)a.size() - 1;
    vector<ll> d;
    for (int i = 1; i <= n; i++) {
        auto it = upper_bound(d.begin(), d.end(), a[i]);
        if (it == d.end()) d.push_back(a[i]);
        else *it = a[i];
    }
    return (int)d.size();
}
```

## 3. 输出一条 LIS

```cpp
vector<ll> restore_lis(const vector<ll>& a) {
    int n = (int)a.size() - 1;
    vector<ll> tail_value;
    vector<int> tail_idx;
    vector<int> pre(n + 1, 0);

    for (int i = 1; i <= n; i++) {
        int pos = lower_bound(tail_value.begin(), tail_value.end(), a[i]) - tail_value.begin();
        if (pos == (int)tail_value.size()) {
            tail_value.push_back(a[i]);
            tail_idx.push_back(i);
        } else {
            tail_value[pos] = a[i];
            tail_idx[pos] = i;
        }
        if (pos > 0) pre[i] = tail_idx[pos - 1];
    }

    vector<ll> ans;
    int cur = tail_idx.empty() ? 0 : tail_idx.back();
    while (cur != 0) {
        ans.push_back(a[cur]);
        cur = pre[cur];
    }
    reverse(ans.begin(), ans.end());
    return ans;
}
```

## 4. 二维偏序：排序后一维 LIS

常见于信封嵌套：`w` 和 `h` 都要严格变大。

```cpp
struct Point {
    int x;
    int y;
};

int two_dim_lis(vector<Point> p) {
    sort(p.begin(), p.end(), [](const Point& a, const Point& b) {
        if (a.x != b.x) return a.x < b.x;
        return a.y > b.y; // x 相同不能互选，所以 y 降序
    });

    vector<int> d;
    for (auto e : p) {
        auto it = lower_bound(d.begin(), d.end(), e.y);
        if (it == d.end()) d.push_back(e.y);
        else *it = e.y;
    }
    return (int)d.size();
}
```

## 5. 输出一条 LCS

```cpp
string restore_lcs(const string& s, const string& t) {
    int n = s.size(), m = t.size();
    vector<vector<int>> dp(n + 1, vector<int>(m + 1, 0));

    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            if (s[i - 1] == t[j - 1]) dp[i][j] = dp[i - 1][j - 1] + 1;
            else dp[i][j] = max(dp[i - 1][j], dp[i][j - 1]);
        }
    }

    string ans;
    int i = n, j = m;
    while (i > 0 && j > 0) {
        if (s[i - 1] == t[j - 1]) {
            ans.push_back(s[i - 1]);
            i--;
            j--;
        } else if (dp[i - 1][j] >= dp[i][j - 1]) {
            i--;
        } else {
            j--;
        }
    }
    reverse(ans.begin(), ans.end());
    return ans;
}
```

## 6. 统计 LIS 个数

朴素 `O(n^2)` 版本最适合考场先写。`len[i]` 表示以 `i` 结尾的 LIS 长度，`cnt[i]` 表示这种长度的方案数。

```cpp
pair<int, long long> count_lis(const vector<ll>& a) {
    int n = (int)a.size() - 1;
    vector<int> len(n + 1, 1);
    vector<long long> cnt(n + 1, 1);

    int best = 0;
    long long ways = 0;
    for (int i = 1; i <= n; i++) {
        len[i] = 1;
        cnt[i] = 1;
        for (int j = 1; j < i; j++) {
            if (a[j] < a[i]) {
                if (len[j] + 1 > len[i]) {
                    len[i] = len[j] + 1;
                    cnt[i] = cnt[j];
                } else if (len[j] + 1 == len[i]) {
                    cnt[i] += cnt[j];
                }
            }
        }

        if (len[i] > best) {
            best = len[i];
            ways = cnt[i];
        } else if (len[i] == best) {
            ways += cnt[i];
        }
    }
    return {best, ways};
}
```

若题目需要“值相同的序列只算一次”，计数规则会复杂很多；这份模板统计的是按下标选择的方案数。

## 7. 带权 LIS

每个元素有收益 `w[i]`，要求选出的值递增，最大化收益。

```cpp
long long weighted_lis_n2(const vector<ll>& a, const vector<ll>& weight) {
    int n = (int)a.size() - 1;
    vector<long long> dp(n + 1, 0);
    long long ans = -LINF; // 若允许空子序列，可改成 0
    for (int i = 1; i <= n; i++) {
        dp[i] = weight[i];
        for (int j = 1; j < i; j++) {
            if (a[j] < a[i]) {
                dp[i] = max(dp[i], dp[j] + weight[i]);
            }
        }
        ans = max(ans, dp[i]);
    }
    return ans;
}
```

`n <= 5000` 时可先交这个。`n` 大时升级为坐标压缩 + 树状数组/SegmentTree 查询前缀最大值，见 DP-18。

## 8. 山形/合唱队形

求先严格上升再严格下降的最长长度。做两次 LIS：`up[i]` 表示以 `i` 结尾的上升长度，`down[i]` 表示以 `i` 开始的下降长度。

```cpp
int bitonic_length_n2(const vector<ll>& a) {
    int n = (int)a.size() - 1;
    vector<int> up(n + 1, 1), down(n + 1, 1);

    for (int i = 1; i <= n; i++) {
        for (int j = 1; j < i; j++) {
            if (a[j] < a[i]) up[i] = max(up[i], up[j] + 1);
        }
    }

    for (int i = n; i >= 1; i--) {
        for (int j = n; j > i; j--) {
            if (a[j] < a[i]) down[i] = max(down[i], down[j] + 1);
        }
    }

    int ans = 0;
    for (int i = 1; i <= n; i++) {
        ans = max(ans, up[i] + down[i] - 1);
    }
    return ans;
}
```

最少删除变成山形：`n - bitonic_length`。

## 9. 最长公共子串

公共子串要求连续，不是 LCS。

```cpp
int longest_common_substring(const string& s, const string& t) {
    int n = s.size(), m = t.size();
    vector<vector<int>> dp(n + 1, vector<int>(m + 1, 0));
    int ans = 0;
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            if (s[i - 1] == t[j - 1]) {
                dp[i][j] = dp[i - 1][j - 1] + 1;
                ans = max(ans, dp[i][j]);
            } else {
                dp[i][j] = 0;
            }
        }
    }
    return ans;
}
```

## 10. LCIS 最长公共上升子序列

两个序列既要“公共”，又要“严格上升”。`dp[j]` 表示当前处理到 `a[i]` 时，以 `b[j]` 结尾的 LCIS 长度。

为什么不是“先求 LCS 再求 LIS”：LCS 的某一条公共子序列不一定保留所有可能的上升选择，先求出来的一条 LCS 可能把更优 LCIS 需要的元素丢掉。必须在匹配两个序列的同时维护“上升”限制。

最后一步视角：

```text
如果 a[i] == b[j]，并且 LCIS 最后一个公共元素选 b[j]，
那么前一个公共元素必须来自某个 k<j 且 b[k]<a[i]。
扫描 b[j] 时维护 best = max(dp[k])，就能 O(nm) 转移。
```

```cpp
int lcis_length(const vector<int>& a, const vector<int>& b) {
    int n = (int)a.size() - 1;
    int m = (int)b.size() - 1;
    vector<int> dp(m + 1, 0);

    for (int i = 1; i <= n; i++) {
        int best = 0;
        for (int j = 1; j <= m; j++) {
            if (a[i] == b[j]) {
                dp[j] = max(dp[j], best + 1);
            }
            if (b[j] < a[i]) {
                best = max(best, dp[j]);
            }
        }
    }

    int ans = 0;
    for (int j = 1; j <= m; j++) ans = max(ans, dp[j]);
    return ans;
}
```

触发词是“两个序列”“公共”“上升/递增”。如果只说公共，不说递增，用 LCS；如果只说递增，不说两个序列，用 LIS。

常见坑：

- `lower_bound` 是严格 LIS，`upper_bound` 是不下降 LIS。
- 二分 LIS 的 `d` 不是真实答案序列，恢复路径要另存前驱。
- 二维偏序有重复第一维时，第二维通常要降序，防止同一第一维被选两次。
- LCS 是子序列，公共子串是连续子串，两者转移不同。
- LCS 路径恢复中，相等走左上，不等走更大的方向。
- LIS 计数模板默认按下标计数；如果题目按值去重，要另做去重逻辑；如果题目要求取模，每次累加 `cnt` 都要取模，精确大数要转高精度。
- LCIS 的 `best` 必须在扫描 `b[j]` 时维护，不能简单套 LCS 后再 LIS。

暴力/部分分替代：

- LIS：`n <= 25` 先 DFS 选/不选，`n <= 5000` 用 `O(n^2)`。
- LCS：短串先 DFS/记忆化，`n*m` 可承受再二维表推。
- 二维偏序不确定排序规则时，用小数据暴力枚举子集验证。

升级方向：

```text
LIS 长度 -> 输出路径 -> 计数/带权 -> 树状数组/SegmentTree
LCS 长度 -> 输出一条 LCS -> 滚动数组节省空间
公共子序列 -> 公共子串：相等延长，不等清零
二维选择 -> 排序 -> 一维 LIS
```

最小测试样例：

```text
LIS:
6
10 9 2 5 3 7
输出：3

LCS:
abcde
ace
输出：ace
```
