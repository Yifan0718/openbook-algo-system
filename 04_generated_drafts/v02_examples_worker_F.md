# 0.2 版本例题扩展 Worker F

范围：第 6 卷数学与字符串、第 6A 卷竞赛数学参考、第 10 卷 AI 专题。

抽取约定：每道例题使用固定结构；代码均为 C++17 单文件程序，不使用文件读写。

***

### V06-EX01 多数 gcd 与有界 lcm

- 归属卷：第 6 卷
- 覆盖模块：MATH-01 gcd/lcm
- 考场用途：处理整除、约分和周期同步，顺手练习 lcm 防溢出。

**题目描述：** 给定 `n` 个整数，求它们的最大公约数 `g`。同时求最小公倍数 `l`，若 `l` 超过给定上限 `limit`，输出 `OVER`。

**输入格式：** 第一行两个整数 `n limit`。第二行 `n` 个整数。

**输出格式：** 第一行输出 `g`。第二行若最小公倍数不超过 `limit` 输出 `l`，否则输出 `OVER`。

**样例输入：**
```text
4 1000
6 10 15 30
```

**样例输出：**
```text
1
30
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

ll gcd_ll(ll a, ll b) {
    if (a < 0) a = -a;
    if (b < 0) b = -b;
    while (b) {
        ll t = a % b;
        a = b;
        b = t;
    }
    return a;
}

ll lcm_limit(ll a, ll b, ll limit) {
    if (a == 0 || b == 0) return 0;
    __int128 aa = a, bb = b;
    if (aa < 0) aa = -aa;
    if (bb < 0) bb = -bb;
    ll g = gcd_ll(a, b);
    aa /= g;
    if (aa > (__int128)limit / bb) return limit + 1;
    __int128 res = aa * bb;
    return res > limit ? limit + 1 : (ll)res;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    ll limit;
    cin >> n >> limit;
    vector<ll> a(n + 1);
    ll g = 0, l = 1;
    bool over = false;
    for (int i = 1; i <= n; i++) {
        cin >> a[i];
        g = gcd_ll(g, a[i]);
        if (!over) {
            l = lcm_limit(l, a[i], limit);
            if (l > limit) over = true;
        }
    }
    cout << g << '\n';
    if (over) cout << "OVER\n";
    else cout << l << '\n';
    return 0;
}
```

**测试设计：**

1. 输入：
```text
3 100
12 12 12
```
期望输出：
```text
12
12
```

2. 输入：
```text
3 100
20 30 70
```
期望输出：
```text
10
OVER
```

***

### V06-EX02 快速幂取模

- 归属卷：第 6 卷
- 覆盖模块：MATH-02 快速幂、取模规范
- 考场用途：避免 `pow` 浮点误差，处理负底数和 `mod=1`。

**题目描述：** 给定 `q` 次询问，每次给出 `a b mod`，输出 `a^b mod mod`。保证 `b>=0` 且 `mod>0`。

**输入格式：** 第一行一个整数 `q`。接下来 `q` 行，每行三个整数 `a b mod`。

**输出格式：** 每个询问输出一行答案。

**样例输入：**
```text
3
2 10 1000
-2 3 5
5 0 7
```

**样例输出：**
```text
24
2
1
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

ll norm(ll x, ll mod) {
    x %= mod;
    if (x < 0) x += mod;
    return x;
}

ll mul_mod(ll a, ll b, ll mod) {
    return (ll)((__int128)norm(a, mod) * norm(b, mod) % mod);
}

ll pow_mod(ll a, ll b, ll mod) {
    if (mod == 1) return 0;
    ll res = 1 % mod;
    a = norm(a, mod);
    while (b > 0) {
        if (b & 1) res = mul_mod(res, a, mod);
        a = mul_mod(a, a, mod);
        b >>= 1;
    }
    return res;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int q;
    cin >> q;
    while (q--) {
        ll a, b, mod;
        cin >> a >> b >> mod;
        cout << pow_mod(a, b, mod) << '\n';
    }
    return 0;
}
```

**测试设计：**

1. 输入：
```text
1
123 456 1
```
期望输出：
```text
0
```

2. 输入：
```text
2
10 2 6
3 4 100
```
期望输出：
```text
4
81
```

***

### V06-EX03 组合数多次查询

- 归属卷：第 6 卷
- 覆盖模块：MATH-03 组合数、逆元
- 考场用途：质数模数下快速回答 `C(n,k)`。

**题目描述：** 给定质数 `MOD` 和最大值 `N`，回答 `q` 次组合数查询 `C(n,k) mod MOD`。若 `k<0` 或 `k>n`，输出 `0`。

**输入格式：** 第一行 `N MOD q`。接下来 `q` 行，每行 `n k`。

**输出格式：** 每个询问输出一行答案。

**样例输入：**
```text
10 1000000007 4
5 2
6 0
6 7
10 5
```

**样例输出：**
```text
10
1
0
252
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

ll mod_pow(ll a, ll e, ll mod) {
    ll r = 1 % mod;
    a %= mod;
    if (a < 0) a += mod;
    while (e > 0) {
        if (e & 1) r = (ll)((__int128)r * a % mod);
        a = (ll)((__int128)a * a % mod);
        e >>= 1;
    }
    return r;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N, q;
    ll MOD;
    cin >> N >> MOD >> q;
    vector<ll> fac(N + 1), ifac(N + 1);
    fac[0] = 1;
    for (int i = 1; i <= N; i++) fac[i] = fac[i - 1] * i % MOD;
    ifac[N] = mod_pow(fac[N], MOD - 2, MOD);
    for (int i = N; i >= 1; i--) ifac[i - 1] = ifac[i] * i % MOD;

    while (q--) {
        int n, k;
        cin >> n >> k;
        if (n < 0 || n > N || k < 0 || k > n) {
            cout << 0 << '\n';
        } else {
            cout << fac[n] * ifac[k] % MOD * ifac[n - k] % MOD << '\n';
        }
    }
    return 0;
}
```

**测试设计：**

1. 输入：
```text
6 7 3
6 3
4 2
5 -1
```
期望输出：
```text
6
6
0
```

2. 输入：
```text
5 1000000007 2
5 5
5 1
```
期望输出：
```text
1
5
```

***

### V06-EX04 素数筛与质数计数

- 归属卷：第 6 卷
- 覆盖模块：MATH-04 筛法
- 考场用途：预处理质数表并回答前缀计数。

**题目描述：** 给定 `N` 和 `q` 次询问，每次给出 `x`，输出 `1..x` 中质数个数。

**输入格式：** 第一行 `N q`。接下来 `q` 行，每行一个 `x`。

**输出格式：** 每个询问输出一行答案。

**样例输入：**
```text
20 4
1
2
10
20
```

**样例输出：**
```text
0
1
4
8
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N, q;
    cin >> N >> q;
    vector<int> spf(N + 1), primes, pref(N + 1);
    for (int i = 2; i <= N; i++) {
        if (spf[i] == 0) {
            spf[i] = i;
            primes.push_back(i);
        }
        for (int p : primes) {
            if (p > spf[i] || 1LL * i * p > N) break;
            spf[i * p] = p;
        }
    }
    for (int i = 1; i <= N; i++) pref[i] = pref[i - 1] + (spf[i] == i);

    while (q--) {
        int x;
        cin >> x;
        x = max(0, min(x, N));
        cout << pref[x] << '\n';
    }
    return 0;
}
```

**测试设计：**

1. 输入：
```text
30 3
0
29
30
```
期望输出：
```text
0
10
10
```

2. 输入：
```text
5 2
4
5
```
期望输出：
```text
2
3
```

***

### V06-EX05 质因数分解与约数个数

- 归属卷：第 6 卷
- 覆盖模块：MATH-04 质因数分解
- 考场用途：从质因子指数计算约数个数。

**题目描述：** 给定 `q` 个正整数 `x`，对每个 `x` 输出质因数分解和约数个数。分解格式为 `p^a`，按质因子升序；若 `x=1`，分解输出 `1`。

**输入格式：** 第一行一个整数 `q`。接下来 `q` 行，每行一个整数 `x`。

**输出格式：** 每个 `x` 输出两行：第一行为分解，第二行为约数个数。

**样例输入：**
```text
2
360
97
```

**样例输出：**
```text
2^3 3^2 5^1
24
97^1
2
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

vector<pair<ll, int>> factorize(ll x) {
    vector<pair<ll, int>> res;
    for (ll d = 2; d <= x / d; d += (d == 2 ? 1 : 2)) {
        if (x % d == 0) {
            int c = 0;
            while (x % d == 0) {
                x /= d;
                c++;
            }
            res.push_back({d, c});
        }
    }
    if (x > 1) res.push_back({x, 1});
    return res;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int q;
    cin >> q;
    while (q--) {
        ll x;
        cin >> x;
        auto f = factorize(x);
        if (f.empty()) {
            cout << "1\n1\n";
            continue;
        }
        ll cnt = 1;
        for (int i = 0; i < (int)f.size(); i++) {
            if (i) cout << ' ';
            cout << f[i].first << '^' << f[i].second;
            cnt *= f[i].second + 1;
        }
        cout << '\n' << cnt << '\n';
    }
    return 0;
}
```

**测试设计：**

1. 输入：
```text
3
1
12
100
```
期望输出：
```text
1
1
2^2 3^1
6
2^2 5^2
9
```

2. 输入：
```text
1
99991
```
期望输出：
```text
99991^1
2
```

***

### V06-EX06 KMP 多次匹配

- 归属卷：第 6 卷
- 覆盖模块：STR-02 KMP
- 考场用途：输出模式串全部出现位置，处理重叠匹配。

**题目描述：** 给定文本串 `text` 和模式串 `pat`，输出 `pat` 在 `text` 中所有出现位置，位置按 1-index 输出。若没有出现，输出 `NONE`。

**输入格式：** 第一行 `text`。第二行 `pat`。

**输出格式：** 一行，所有出现位置从小到大输出；没有出现则输出 `NONE`。

**样例输入：**
```text
ababa
aba
```

**样例输出：**
```text
1 3
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

vector<int> prefix_function(const string &s) {
    int n = (int)s.size();
    vector<int> pi(n, 0);
    for (int i = 1; i < n; i++) {
        int j = pi[i - 1];
        while (j > 0 && s[i] != s[j]) j = pi[j - 1];
        if (s[i] == s[j]) j++;
        pi[i] = j;
    }
    return pi;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string text, pat;
    cin >> text >> pat;
    string s = pat + char(1) + text;
    vector<int> pi = prefix_function(s);
    int m = (int)pat.size();
    vector<int> ans;
    for (int i = m + 1; i < (int)s.size(); i++) {
        if (pi[i] == m) ans.push_back(i - 2 * m + 1);
    }
    if (ans.empty()) {
        cout << "NONE\n";
    } else {
        for (int i = 0; i < (int)ans.size(); i++) {
            if (i) cout << ' ';
            cout << ans[i];
        }
        cout << '\n';
    }
    return 0;
}
```

**测试设计：**

1. 输入：
```text
aaaa
aa
```
期望输出：
```text
1 2 3
```

2. 输入：
```text
abc
d
```
期望输出：
```text
NONE
```

***

### V06-EX07 Z 函数求最短循环节

- 归属卷：第 6 卷
- 覆盖模块：STR-02 Z 函数
- 考场用途：判断字符串是否由更短模式重复构成。

**题目描述：** 给定字符串 `s`，求最短循环节长度。若不存在更短循环节，则输出 `|s|`。

**输入格式：** 一行字符串 `s`。

**输出格式：** 输出一个整数。

**样例输入：**
```text
ababab
```

**样例输出：**
```text
2
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

vector<int> z_function(const string &s) {
    int n = (int)s.size();
    vector<int> z(n, 0);
    int l = 0, r = 0;
    for (int i = 1; i < n; i++) {
        if (i <= r) z[i] = min(r - i + 1, z[i - l]);
        while (i + z[i] < n && s[z[i]] == s[i + z[i]]) z[i]++;
        if (i + z[i] - 1 > r) {
            l = i;
            r = i + z[i] - 1;
        }
    }
    return z;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string s;
    cin >> s;
    int n = (int)s.size();
    vector<int> z = z_function(s);
    for (int p = 1; p <= n; p++) {
        if (n % p == 0 && (p == n || z[p] >= n - p)) {
            cout << p << '\n';
            return 0;
        }
    }
    return 0;
}
```

**测试设计：**

1. 输入：
```text
abac
```
期望输出：
```text
4
```

2. 输入：
```text
x
```
期望输出：
```text
1
```

***

### V06-EX08 Trie 前缀统计

- 归属卷：第 6 卷
- 覆盖模块：STR-03 Trie
- 考场用途：维护词典并回答前缀数量。

**题目描述：** 维护一个小写字母词典，支持 `add word` 插入单词，`ask prefix` 查询有多少已插入单词以 `prefix` 为前缀。

**输入格式：** 第一行一个整数 `q`。接下来 `q` 行，每行为一个操作。

**输出格式：** 对每个 `ask` 操作输出一行答案。

**样例输入：**
```text
6
add apple
add app
ask app
ask apple
add apply
ask appl
```

**样例输出：**
```text
2
1
2
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

struct Trie {
    struct Node {
        int nxt[26]{};
        int pass = 0;
    };
    vector<Node> tr;

    Trie() {
        tr.push_back(Node());
    }

    void insert(const string &s) {
        int u = 0;
        tr[u].pass++;
        for (char c : s) {
            int x = c - 'a';
            if (!tr[u].nxt[x]) {
                tr[u].nxt[x] = (int)tr.size();
                tr.push_back(Node());
            }
            u = tr[u].nxt[x];
            tr[u].pass++;
        }
    }

    int query(const string &s) const {
        int u = 0;
        for (char c : s) {
            int x = c - 'a';
            if (x < 0 || x >= 26 || !tr[u].nxt[x]) return 0;
            u = tr[u].nxt[x];
        }
        return tr[u].pass;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int q;
    cin >> q;
    Trie trie;
    while (q--) {
        string op, s;
        cin >> op >> s;
        if (op == "add") trie.insert(s);
        else cout << trie.query(s) << '\n';
    }
    return 0;
}
```

**测试设计：**

1. 输入：
```text
5
ask a
add a
add ab
ask a
ask ab
```
期望输出：
```text
0
2
1
```

2. 输入：
```text
4
add cat
add car
ask ca
ask dog
```
期望输出：
```text
2
0
```

***

### V06-EX09 Rolling Hash 子串相等

- 归属卷：第 6 卷
- 覆盖模块：STR-03 Rolling Hash
- 考场用途：多次判断两个子串是否相等。

**题目描述：** 给定字符串 `s` 和 `q` 次询问，每次给出两个 1-index 闭区间 `[l1,r1]`、`[l2,r2]`，判断两个子串是否相等。

**输入格式：** 第一行字符串 `s`。第二行整数 `q`。接下来 `q` 行，每行 `l1 r1 l2 r2`。

**输出格式：** 相等输出 `YES`，否则输出 `NO`。

**样例输入：**
```text
abacaba
3
1 3 5 7
1 2 2 3
3 3 7 7
```

**样例输出：**
```text
YES
NO
YES
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;
using ull = unsigned long long;

struct RollingHash {
    static const ull BASE = 1315423911ULL;
    vector<ull> h, pw;

    void build(const string &s) {
        int n = (int)s.size();
        h.assign(n + 1, 0);
        pw.assign(n + 1, 1);
        for (int i = 0; i < n; i++) {
            h[i + 1] = h[i] * BASE + (unsigned char)s[i] + 1;
            pw[i + 1] = pw[i] * BASE;
        }
    }

    ull get(int l, int r) const {
        return h[r + 1] - h[l] * pw[r - l + 1];
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string s;
    cin >> s;
    RollingHash rh;
    rh.build(s);
    int q;
    cin >> q;
    while (q--) {
        int l1, r1, l2, r2;
        cin >> l1 >> r1 >> l2 >> r2;
        --l1; --r1; --l2; --r2;
        if (r1 - l1 != r2 - l2) cout << "NO\n";
        else cout << (rh.get(l1, r1) == rh.get(l2, r2) ? "YES\n" : "NO\n");
    }
    return 0;
}
```

**测试设计：**

1. 输入：
```text
aaaa
2
1 2 2 3
1 3 2 4
```
期望输出：
```text
YES
YES
```

2. 输入：
```text
abcd
2
1 1 4 4
1 2 3 4
```
期望输出：
```text
NO
NO
```

***

### V06-EX10 Manacher 回文询问

- 归属卷：第 6 卷
- 覆盖模块：STR-04 Manacher
- 考场用途：预处理后快速判断任意区间是否回文。

**题目描述：** 给定字符串 `s`，回答 `q` 次询问。每次给出 1-index 闭区间 `[l,r]`，判断 `s[l..r]` 是否为回文串。

**输入格式：** 第一行字符串 `s`。第二行整数 `q`。接下来 `q` 行，每行 `l r`。

**输出格式：** 回文输出 `YES`，否则输出 `NO`。

**样例输入：**
```text
abacaba
4
1 7
1 3
2 4
3 5
```

**样例输出：**
```text
YES
YES
NO
YES
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

pair<vector<int>, vector<int>> manacher(const string &s) {
    int n = (int)s.size();
    vector<int> d1(n), d2(n);
    for (int i = 0, l = 0, r = -1; i < n; i++) {
        int k = (i > r) ? 1 : min(d1[l + r - i], r - i + 1);
        while (i - k >= 0 && i + k < n && s[i - k] == s[i + k]) k++;
        d1[i] = k;
        if (i + k - 1 > r) {
            l = i - k + 1;
            r = i + k - 1;
        }
    }
    for (int i = 0, l = 0, r = -1; i < n; i++) {
        int k = (i > r) ? 0 : min(d2[l + r - i + 1], r - i + 1);
        while (i - k - 1 >= 0 && i + k < n && s[i - k - 1] == s[i + k]) k++;
        d2[i] = k;
        if (i + k - 1 > r) {
            l = i - k;
            r = i + k - 1;
        }
    }
    return {d1, d2};
}

bool is_pal(int l, int r, const vector<int> &d1, const vector<int> &d2) {
    int len = r - l + 1;
    if (len & 1) {
        int mid = (l + r) / 2;
        return d1[mid] >= len / 2 + 1;
    }
    int mid = (l + r + 1) / 2;
    return d2[mid] >= len / 2;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string s;
    cin >> s;
    auto data = manacher(s);
    int q;
    cin >> q;
    while (q--) {
        int l, r;
        cin >> l >> r;
        --l; --r;
        cout << (is_pal(l, r, data.first, data.second) ? "YES\n" : "NO\n");
    }
    return 0;
}
```

**测试设计：**

1. 输入：
```text
abba
3
1 4
2 3
1 3
```
期望输出：
```text
YES
YES
NO
```

2. 输入：
```text
abc
2
1 1
1 2
```
期望输出：
```text
YES
NO
```

***

### V06A-EX01 扩展 gcd 解线性方程

- 归属卷：第 6A 卷
- 覆盖模块：MATHREF-02 exgcd
- 考场用途：判断并构造 `ax+by=c` 的整数解。

**题目描述：** 给定 `a b c`，求整数 `x y` 使 `a*x+b*y=c`。若无解输出 `NO`，否则输出 `YES` 和一组解。

**输入格式：** 一行三个整数 `a b c`。

**输出格式：** 无解输出 `NO`。有解输出两行：第一行 `YES`，第二行 `x y`。

**样例输入：**
```text
30 18 12
```

**样例输出：**
```text
YES
-2 4
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

ll exgcd(ll a, ll b, ll &x, ll &y) {
    if (b == 0) {
        x = (a >= 0 ? 1 : -1);
        y = 0;
        return a >= 0 ? a : -a;
    }
    ll x1, y1;
    ll g = exgcd(b, a % b, x1, y1);
    x = y1;
    y = x1 - a / b * y1;
    return g;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    ll a, b, c, x, y;
    cin >> a >> b >> c;
    ll g = exgcd(a, b, x, y);
    if (c % g != 0) {
        cout << "NO\n";
    } else {
        x *= c / g;
        y *= c / g;
        cout << "YES\n" << x << ' ' << y << '\n';
    }
    return 0;
}
```

**测试设计：**

1. 输入：
```text
30 18 7
```
期望输出：
```text
NO
```

2. 输入：
```text
-3 6 9
```
期望输出：
```text
YES
-3 0
```

***

### V06A-EX02 扩展 CRT 合并同余

- 归属卷：第 6A 卷
- 覆盖模块：MATHREF-02 CRT/exCRT
- 考场用途：处理模数不互质的同余方程组。

**题目描述：** 给定 `k` 个同余方程 `x ≡ r_i (mod m_i)`，模数不保证互质。求最小非负解；若无解输出 `NO`。

**输入格式：** 第一行整数 `k`。接下来 `k` 行，每行 `r_i m_i`。

**输出格式：** 有解输出最小非负解，否则输出 `NO`。

**样例输入：**
```text
2
2 3
3 5
```

**样例输出：**
```text
8
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

ll exgcd(ll a, ll b, ll &x, ll &y) {
    if (b == 0) {
        x = (a >= 0 ? 1 : -1);
        y = 0;
        return a >= 0 ? a : -a;
    }
    ll x1, y1;
    ll g = exgcd(b, a % b, x1, y1);
    x = y1;
    y = x1 - a / b * y1;
    return g;
}

ll norm(ll x, ll mod) {
    x %= mod;
    if (x < 0) x += mod;
    return x;
}

bool merge_crt(ll &r, ll &m, ll r2, ll m2) {
    ll x, y;
    ll g = exgcd(m, m2, x, y);
    __int128 diff = (__int128)r2 - r;
    if (diff % g != 0) return false;
    ll mod2 = m2 / g;
    ll k = (ll)((diff / g * x) % mod2);
    k = norm(k, mod2);
    __int128 nr = (__int128)r + (__int128)m * k;
    __int128 nm = (__int128)m / g * m2;
    if (nm > LLONG_MAX) return false;
    m = (ll)nm;
    r = (ll)(nr % nm);
    if (r < 0) r += m;
    return true;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int k;
    cin >> k;
    ll r, m;
    cin >> r >> m;
    r = norm(r, m);
    for (int i = 2; i <= k; i++) {
        ll r2, m2;
        cin >> r2 >> m2;
        if (!merge_crt(r, m, norm(r2, m2), m2)) {
            cout << "NO\n";
            return 0;
        }
    }
    cout << r << '\n';
    return 0;
}
```

**测试设计：**

1. 输入：
```text
2
2 6
8 10
```
期望输出：
```text
8
```

2. 输入：
```text
2
1 4
2 6
```
期望输出：
```text
NO
```

***

### V06A-EX03 矩阵快速幂求 Fibonacci

- 归属卷：第 6A 卷
- 覆盖模块：MATH-05 矩阵快速幂
- 考场用途：把线性递推转为矩阵幂。

**题目描述：** 定义 `F(0)=0,F(1)=1,F(n)=F(n-1)+F(n-2)`。给定 `n` 和 `mod`，输出 `F(n) mod mod`。

**输入格式：** 一行 `n mod`。

**输出格式：** 输出答案。

**样例输入：**
```text
10 1000000007
```

**样例输出：**
```text
55
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Mat {
    ll a[2][2]{};
};

Mat mul(const Mat &A, const Mat &B, ll mod) {
    Mat C;
    for (int i = 0; i < 2; i++) {
        for (int k = 0; k < 2; k++) {
            for (int j = 0; j < 2; j++) {
                C.a[i][j] = (C.a[i][j] + (__int128)A.a[i][k] * B.a[k][j]) % mod;
            }
        }
    }
    return C;
}

Mat mpow(Mat A, long long e, ll mod) {
    Mat R;
    R.a[0][0] = R.a[1][1] = 1 % mod;
    while (e > 0) {
        if (e & 1) R = mul(R, A, mod);
        A = mul(A, A, mod);
        e >>= 1;
    }
    return R;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    long long n;
    ll mod;
    cin >> n >> mod;
    if (n == 0) {
        cout << 0 << '\n';
        return 0;
    }
    Mat T;
    T.a[0][0] = 1 % mod;
    T.a[0][1] = 1 % mod;
    T.a[1][0] = 1 % mod;
    Mat P = mpow(T, n - 1, mod);
    cout << P.a[0][0] % mod << '\n';
    return 0;
}
```

**测试设计：**

1. 输入：
```text
0 100
```
期望输出：
```text
0
```

2. 输入：
```text
50 1000
```
期望输出：
```text
25
```

***

### V06A-EX04 倍数容斥计数

- 归属卷：第 6A 卷
- 覆盖模块：MATH-06 容斥
- 考场用途：统计至少满足一个整除条件的数量。

**题目描述：** 给定 `n` 和 `m` 个正整数 `d_i`，求 `1..n` 中至少能被一个 `d_i` 整除的数有多少个。

**输入格式：** 第一行 `n m`。第二行 `m` 个整数 `d_i`。

**输出格式：** 输出答案。

**样例输入：**
```text
10 2
2 3
```

**样例输出：**
```text
7
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

ll gcd_ll(ll a, ll b) {
    while (b) {
        ll t = a % b;
        a = b;
        b = t;
    }
    return a >= 0 ? a : -a;
}

ll lcm_limit(ll a, ll b, ll limit) {
    ll g = gcd_ll(a, b);
    __int128 aa = a / g;
    __int128 bb = b;
    if (aa > (__int128)limit / bb) return limit + 1;
    return (ll)(aa * bb);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    ll n;
    int m;
    cin >> n >> m;
    vector<ll> d(m + 1);
    for (int i = 1; i <= m; i++) cin >> d[i];
    __int128 ans = 0;
    for (int mask = 1; mask < (1 << m); mask++) {
        ll l = 1;
        int bits = 0;
        bool over = false;
        for (int i = 1; i <= m; i++) {
            if (mask >> (i - 1) & 1) {
                bits++;
                l = lcm_limit(l, d[i], n);
                if (l > n) {
                    over = true;
                    break;
                }
            }
        }
        if (over) continue;
        if (bits & 1) ans += n / l;
        else ans -= n / l;
    }
    cout << (long long)ans << '\n';
    return 0;
}
```

**测试设计：**

1. 输入：
```text
20 2
2 4
```
期望输出：
```text
10
```

2. 输入：
```text
30 2
5 7
```
期望输出：
```text
10
```

***

### V06A-EX05 骰子到终点的期望步数

- 归属卷：第 6A 卷
- 覆盖模块：MATHREF-05 概率期望
- 考场用途：倒推期望 DP。

**题目描述：** 棋子从位置 `0` 出发，每步掷一个六面骰子并前进 `1..6` 格。位置大于等于 `n` 时停止，求从 `0` 到停止的期望步数。

**输入格式：** 一个整数 `n`。

**输出格式：** 输出期望步数，保留 6 位小数。

**样例输入：**
```text
1
```

**样例输出：**
```text
1.000000
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<double> dp(n + 7, 0.0);
    for (int i = n - 1; i >= 0; i--) {
        dp[i] = 1.0;
        for (int d = 1; d <= 6; d++) dp[i] += dp[i + d] / 6.0;
    }
    cout << fixed << setprecision(6) << dp[0] << '\n';
    return 0;
}
```

**测试设计：**

1. 输入：
```text
2
```
期望输出：
```text
1.166667
```

2. 输入：
```text
3
```
期望输出：
```text
1.361111
```

***

### V06A-EX06 取石子 SG 判胜

- 归属卷：第 6A 卷
- 覆盖模块：MATHREF-05 SG 函数
- 考场用途：公平组合游戏胜负判断。

**题目描述：** 有一堆 `N` 个石子。每次可以取走 `moves` 中任意一种正数个石子，不能操作者输。判断先手必胜还是必败。

**输入格式：** 第一行 `N m`。第二行 `m` 个可取数量。

**输出格式：** 先手必胜输出 `WIN`，否则输出 `LOSE`。

**样例输入：**
```text
7 2
1 3
```

**样例输出：**
```text
WIN
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

int mex_value(const vector<int> &v) {
    vector<int> seen(v.size() + 5, 0);
    for (int x : v) if (0 <= x && x < (int)seen.size()) seen[x] = 1;
    for (int i = 0; ; i++) if (!seen[i]) return i;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N, m;
    cin >> N >> m;
    vector<int> moves(m + 1);
    for (int i = 1; i <= m; i++) cin >> moves[i];
    vector<int> sg(N + 1, 0);
    for (int x = 1; x <= N; x++) {
        vector<int> next_values;
        for (int i = 1; i <= m; i++) {
            if (moves[i] > 0 && x >= moves[i]) next_values.push_back(sg[x - moves[i]]);
        }
        sg[x] = mex_value(next_values);
    }
    cout << (sg[N] ? "WIN\n" : "LOSE\n");
    return 0;
}
```

**测试设计：**

1. 输入：
```text
1 1
2
```
期望输出：
```text
LOSE
```

2. 输入：
```text
0 2
1 3
```
期望输出：
```text
LOSE
```

***

### V06A-EX07 点在线段上与多边形面积

- 归属卷：第 6A 卷
- 覆盖模块：MATHREF-06 几何叉积
- 考场用途：判断共线和计算多边形面积。

**题目描述：** 给定一个多边形，输出其面积的两倍。再给定线段 `AB` 和点 `P`，判断 `P` 是否在线段 `AB` 上。

**输入格式：** 第一行整数 `n`。接下来 `n` 行为多边形顶点。最后三行分别为点 `A`、`B`、`P`。

**输出格式：** 第一行输出多边形面积的两倍。第二行若 `P` 在线段上输出 `YES`，否则输出 `NO`。

**样例输入：**
```text
4
0 0
2 0
2 1
0 1
0 0
2 0
1 0
```

**样例输出：**
```text
4
YES
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Point {
    ll x, y;
};

Point operator-(Point a, Point b) {
    return {a.x - b.x, a.y - b.y};
}

__int128 cross(Point a, Point b) {
    return (__int128)a.x * b.y - (__int128)a.y * b.x;
}

__int128 cross(Point a, Point b, Point c) {
    return cross(b - a, c - a);
}

bool on_segment(Point a, Point b, Point p) {
    return cross(a, b, p) == 0 &&
           min(a.x, b.x) <= p.x && p.x <= max(a.x, b.x) &&
           min(a.y, b.y) <= p.y && p.y <= max(a.y, b.y);
}

void print_i128(__int128 x) {
    if (x == 0) {
        cout << 0;
        return;
    }
    if (x < 0) {
        cout << '-';
        x = -x;
    }
    string s;
    while (x > 0) {
        s.push_back(char('0' + x % 10));
        x /= 10;
    }
    reverse(s.begin(), s.end());
    cout << s;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<Point> p(n + 1);
    for (int i = 1; i <= n; i++) cin >> p[i].x >> p[i].y;
    Point A, B, P;
    cin >> A.x >> A.y >> B.x >> B.y >> P.x >> P.y;
    __int128 area2 = 0;
    for (int i = 1; i <= n; i++) area2 += cross(p[i], p[i == n ? 1 : i + 1]);
    if (area2 < 0) area2 = -area2;
    print_i128(area2);
    cout << '\n' << (on_segment(A, B, P) ? "YES\n" : "NO\n");
    return 0;
}
```

**测试设计：**

1. 输入：
```text
3
0 0
1 0
0 1
0 0
1 1
1 0
```
期望输出：
```text
1
NO
```

2. 输入：
```text
3
0 0
2 0
0 2
0 0
2 2
1 1
```
期望输出：
```text
4
YES
```

***

### V06A-EX08 日期相差天数

- 归属卷：第 6A 卷
- 覆盖模块：SIM-06 日期/日历
- 考场用途：处理公历闰年和日期差。

**题目描述：** 给定两个合法公历日期，输出第二个日期距离第一个日期的天数。使用公历，不考虑历史切历。

**输入格式：** 一行 `y1 m1 d1 y2 m2 d2`。

**输出格式：** 输出天数差，可为负数。

**样例输入：**
```text
2024 2 28 2024 3 1
```

**样例输出：**
```text
2
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

ll floor_div(ll a, ll b) {
    ll q = a / b, r = a % b;
    if (r != 0 && ((r > 0) != (b > 0))) q--;
    return q;
}

ll days_from_civil(ll y, int m, int d) {
    y -= m <= 2;
    ll era = floor_div(y, 400);
    unsigned yoe = (unsigned)(y - era * 400);
    unsigned mp = (unsigned)(m + (m > 2 ? -3 : 9));
    unsigned doy = (153 * mp + 2) / 5 + (unsigned)d - 1;
    unsigned doe = yoe * 365 + yoe / 4 - yoe / 100 + doy;
    return era * 146097 + (ll)doe - 719468;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    ll y1, y2;
    int m1, d1, m2, d2;
    cin >> y1 >> m1 >> d1 >> y2 >> m2 >> d2;
    cout << days_from_civil(y2, m2, d2) - days_from_civil(y1, m1, d1) << '\n';
    return 0;
}
```

**测试设计：**

1. 输入：
```text
2023 2 28 2023 3 1
```
期望输出：
```text
1
```

2. 输入：
```text
2024 3 1 2024 2 28
```
期望输出：
```text
-2
```

***

### V06A-EX09 地板除与天花板除

- 归属卷：第 6A 卷
- 覆盖模块：MATHREF-06 整数取整
- 考场用途：避免负数除法边界错误。

**题目描述：** 给定 `q` 次询问，每次给出整数 `a b`，输出 `floor(a/b)` 与 `ceil(a/b)`。保证 `b!=0`。

**输入格式：** 第一行整数 `q`。接下来 `q` 行，每行 `a b`。

**输出格式：** 每行输出两个整数。

**样例输入：**
```text
3
7 3
-7 3
7 -3
```

**样例输出：**
```text
2 3
-3 -2
-3 -2
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

ll floor_div(ll a, ll b) {
    __int128 aa = a, bb = b;
    __int128 q = aa / bb, r = aa % bb;
    if (r != 0 && ((r > 0) != (bb > 0))) q--;
    return (ll)q;
}

ll ceil_div(ll a, ll b) {
    __int128 aa = a, bb = b;
    __int128 q = aa / bb, r = aa % bb;
    if (r != 0 && ((r > 0) == (bb > 0))) q++;
    return (ll)q;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int q;
    cin >> q;
    while (q--) {
        ll a, b;
        cin >> a >> b;
        cout << floor_div(a, b) << ' ' << ceil_div(a, b) << '\n';
    }
    return 0;
}
```

**测试设计：**

1. 输入：
```text
2
-6 3
6 -3
```
期望输出：
```text
-2 -2
-2 -2
```

2. 输入：
```text
2
1 2
-1 2
```
期望输出：
```text
0 1
-1 0
```

***

### V06A-EX10 互质对数量

- 归属卷：第 6A 卷
- 覆盖模块：MATHREF-03 Mobius
- 考场用途：用莫比乌斯函数统计有序互质对。

**题目描述：** 给定 `A B`，求有序数对 `(x,y)` 的数量，使 `1<=x<=A,1<=y<=B` 且 `gcd(x,y)=1`。

**输入格式：** 一行两个整数 `A B`。

**输出格式：** 输出答案。

**样例输入：**
```text
3 3
```

**样例输出：**
```text
7
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

vector<int> mobius(int n) {
    vector<int> mu(n + 1), primes, is_comp(n + 1);
    if (n >= 1) mu[1] = 1;
    for (int i = 2; i <= n; i++) {
        if (!is_comp[i]) {
            primes.push_back(i);
            mu[i] = -1;
        }
        for (int p : primes) {
            if (1LL * i * p > n) break;
            is_comp[i * p] = 1;
            if (i % p == 0) {
                mu[i * p] = 0;
                break;
            }
            mu[i * p] = -mu[i];
        }
    }
    return mu;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int A, B;
    cin >> A >> B;
    int n = min(A, B);
    vector<int> mu = mobius(n);
    long long ans = 0;
    for (int d = 1; d <= n; d++) ans += 1LL * mu[d] * (A / d) * (B / d);
    cout << ans << '\n';
    return 0;
}
```

**测试设计：**

1. 输入：
```text
1 5
```
期望输出：
```text
5
```

2. 输入：
```text
2 2
```
期望输出：
```text
3
```

***

### V10-EX01 kNN 分类器

- 归属卷：第 10 卷
- 覆盖模块：AI-02 kNN
- 考场用途：把训练集、特征、标签转成距离排序和投票。

**题目描述：** 给定训练样本和查询样本，使用 `k` 近邻分类。距离使用欧氏距离平方，投票数多的标签胜出；票数相同标签小者胜出。

**输入格式：** 第一行 `n q d k`。接下来 `n` 行，每行 `d` 个特征和一个标签。接下来 `q` 行，每行 `d` 个特征。

**输出格式：** 每个查询输出预测标签。

**样例输入：**
```text
3 2 2 1
0 0 1
10 10 2
1 0 1
0 1
9 9
```

**样例输出：**
```text
1
2
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

struct Sample {
    vector<double> x;
    int label;
};

double dist2(const vector<double> &a, const vector<double> &b, int d) {
    double s = 0;
    for (int i = 1; i <= d; i++) {
        double t = a[i] - b[i];
        s += t * t;
    }
    return s;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, q, d, k;
    cin >> n >> q >> d >> k;
    vector<Sample> train(n + 1);
    for (int i = 1; i <= n; i++) {
        train[i].x.assign(d + 1, 0);
        for (int j = 1; j <= d; j++) cin >> train[i].x[j];
        cin >> train[i].label;
    }
    while (q--) {
        vector<double> x(d + 1);
        for (int j = 1; j <= d; j++) cin >> x[j];
        vector<pair<double, int>> near;
        for (int i = 1; i <= n; i++) near.push_back({dist2(train[i].x, x, d), train[i].label});
        sort(near.begin(), near.end());
        map<int, int> vote;
        for (int i = 0; i < min(k, (int)near.size()); i++) vote[near[i].second]++;
        int best_label = -1, best_cnt = -1;
        for (auto [lab, cnt] : vote) {
            if (cnt > best_cnt || (cnt == best_cnt && lab < best_label)) {
                best_cnt = cnt;
                best_label = lab;
            }
        }
        cout << best_label << '\n';
    }
    return 0;
}
```

**测试设计：**

1. 输入：
```text
4 1 1 3
0 1
2 2
4 2
6 1
3
```
期望输出：
```text
2
```

2. 输入：
```text
2 1 1 2
0 1
2 2
1
```
期望输出：
```text
1
```

***

### V10-EX02 TF-IDF 文档检索

- 归属卷：第 10 卷
- 覆盖模块：AI-05 TF-IDF
- 考场用途：文本切词、词频、余弦相似度综合模拟。

**题目描述：** 给定 `n` 篇英文文档和一个查询，按小写字母数字连续段切词。使用 `idf(w)=log((n+1)/(df(w)+1))+1`，权重为 `tf*idf`。输出与查询余弦相似度最高的文档编号和分数，平分取编号小。

**输入格式：** 第一行整数 `n`。接下来 `n` 行为文档。最后一行为查询。

**输出格式：** 输出文档编号和相似度，保留 6 位。

**样例输入：**
```text
3
Apple banana apple
Orange banana
car bus train
apple banana
```

**样例输出：**
```text
1 0.959146
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

vector<string> tokenize(const string &s) {
    vector<string> words;
    string cur;
    for (unsigned char c : s) {
        if (isalnum(c)) cur.push_back((char)tolower(c));
        else if (!cur.empty()) {
            words.push_back(cur);
            cur.clear();
        }
    }
    if (!cur.empty()) words.push_back(cur);
    return words;
}

map<string, int> count_words(const vector<string> &v) {
    map<string, int> c;
    for (auto &w : v) c[w]++;
    return c;
}

double cosine(const map<string, int> &a, const map<string, int> &b, const map<string, int> &df, int n) {
    map<string, double> va, vb;
    for (auto [w, c] : a) {
        int dfi = df.count(w) ? df.at(w) : 0;
        va[w] = c * (log((double)(n + 1) / (dfi + 1)) + 1.0);
    }
    for (auto [w, c] : b) {
        int dfi = df.count(w) ? df.at(w) : 0;
        vb[w] = c * (log((double)(n + 1) / (dfi + 1)) + 1.0);
    }
    double dot = 0, na = 0, nb = 0;
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
    getline(cin, line);
    auto query = count_words(tokenize(line));
    int best = 1;
    double score = -1;
    for (int i = 1; i <= n; i++) {
        double cur = cosine(docs[i], query, df, n);
        if (cur > score + 1e-12) {
            score = cur;
            best = i;
        }
    }
    cout << fixed << setprecision(6) << best << ' ' << score << '\n';
    return 0;
}
```

**测试设计：**

1. 输入：
```text
2
hello
world
xyz
```
期望输出：
```text
1 0.000000
```

2. 输入：
```text
2
cat dog
cat cat
cat dog
```
期望输出：
```text
1 1.000000
```

***

### V10-EX03 k-means 一维聚类

- 归属卷：第 10 卷
- 覆盖模块：AI-06 k-means
- 考场用途：按题意模拟聚类迭代和空簇处理。

**题目描述：** 给定 `n` 个一维点、簇数 `k` 和迭代次数 `iter`。初始中心为前 `k` 个点。每轮先分配到最近中心，距离相同选编号小；再用簇内均值更新中心，空簇保持原中心。输出最终标签和中心。

**输入格式：** 第一行 `n k iter`。第二行 `n` 个实数点。

**输出格式：** 第一行输出 `n` 个簇编号。第二行输出 `k` 个中心，保留 6 位。

**样例输入：**
```text
5 2 2
0 1 2 10 11
```

**样例输出：**
```text
1 1 1 2 2
1.000000 10.500000
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, k, iter;
    cin >> n >> k >> iter;
    vector<double> x(n + 1), center(k + 1);
    for (int i = 1; i <= n; i++) cin >> x[i];
    for (int i = 1; i <= k; i++) center[i] = x[i];
    vector<int> label(n + 1, 1);
    for (int it = 1; it <= iter; it++) {
        for (int i = 1; i <= n; i++) {
            int best = 1;
            double best_dist = fabs(x[i] - center[1]);
            for (int c = 2; c <= k; c++) {
                double cur = fabs(x[i] - center[c]);
                if (cur < best_dist - 1e-12) {
                    best_dist = cur;
                    best = c;
                }
            }
            label[i] = best;
        }
        vector<double> sum(k + 1, 0);
        vector<int> cnt(k + 1, 0);
        for (int i = 1; i <= n; i++) {
            sum[label[i]] += x[i];
            cnt[label[i]]++;
        }
        for (int c = 1; c <= k; c++) if (cnt[c]) center[c] = sum[c] / cnt[c];
    }
    for (int i = 1; i <= n; i++) {
        if (i > 1) cout << ' ';
        cout << label[i];
    }
    cout << '\n' << fixed << setprecision(6);
    for (int c = 1; c <= k; c++) {
        if (c > 1) cout << ' ';
        cout << center[c];
    }
    cout << '\n';
    return 0;
}
```

**测试设计：**

1. 输入：
```text
3 2 1
0 10 20
```
期望输出：
```text
1 2 2
0.000000 15.000000
```

2. 输入：
```text
3 2 0
1 2 3
```
期望输出：
```text
1 1 1
1.000000 2.000000
```

***

### V10-EX04 线性回归在线训练

- 归属卷：第 10 卷
- 覆盖模块：AI-13 线性回归梯度下降
- 考场用途：按题面公式模拟参数更新。

**题目描述：** 一维线性模型 `pred=w*x+b`，初始 `w=b=0`。给定训练集、轮数和学习率，按输入顺序做在线梯度下降：`err=pred-y`，`w-=lr*err*x`，`b-=lr*err`。训练后回答查询预测。

**输入格式：** 第一行 `n epoch lr`。接下来 `n` 行 `x y`。然后一行 `q`。接下来 `q` 行每行一个 `x`。

**输出格式：** 每个查询输出预测值，保留 6 位。

**样例输入：**
```text
2 1 0.1
1 2
2 4
2
1
3
```

**样例输出：**
```text
1.420000
3.180000
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, epoch;
    double lr;
    cin >> n >> epoch >> lr;
    vector<double> x(n + 1), y(n + 1);
    for (int i = 1; i <= n; i++) cin >> x[i] >> y[i];
    double w = 0, b = 0;
    for (int ep = 1; ep <= epoch; ep++) {
        for (int i = 1; i <= n; i++) {
            double pred = w * x[i] + b;
            double err = pred - y[i];
            w -= lr * err * x[i];
            b -= lr * err;
        }
    }
    int q;
    cin >> q;
    cout << fixed << setprecision(6);
    while (q--) {
        double t;
        cin >> t;
        cout << w * t + b << '\n';
    }
    return 0;
}
```

**测试设计：**

1. 输入：
```text
1 0 0.1
5 10
2
1
5
```
期望输出：
```text
0.000000
0.000000
```

2. 输入：
```text
1 1 0.5
2 4
1
2
```
期望输出：
```text
10.000000
```

***

### V10-EX05 感知机二分类

- 归属卷：第 10 卷
- 覆盖模块：AI-02 感知机
- 考场用途：二分类在线更新，标签为 `-1/+1`。

**题目描述：** 给定二维样本和标签 `-1/+1`，初始 `w1=w2=b=0`。训练 `epoch` 轮。若 `y*(w·x+b)<=0`，执行 `w+=lr*y*x,b+=lr*y`。训练后预测查询点，分数 `>=0` 输出 `1`，否则输出 `-1`。

**输入格式：** 第一行 `n epoch lr`。接下来 `n` 行 `x1 x2 y`。然后一行 `q`。接下来 `q` 行 `x1 x2`。

**输出格式：** 每个查询输出预测标签。

**样例输入：**
```text
4 2 1
1 1 1
2 1 1
-1 -1 -1
-2 -1 -1
3
3 2
-3 -2
0 0
```

**样例输出：**
```text
1
-1
1
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, epoch;
    double lr;
    cin >> n >> epoch >> lr;
    vector<double> x1(n + 1), x2(n + 1);
    vector<int> y(n + 1);
    for (int i = 1; i <= n; i++) cin >> x1[i] >> x2[i] >> y[i];
    double w1 = 0, w2 = 0, b = 0;
    for (int ep = 1; ep <= epoch; ep++) {
        for (int i = 1; i <= n; i++) {
            double score = w1 * x1[i] + w2 * x2[i] + b;
            if (y[i] * score <= 0) {
                w1 += lr * y[i] * x1[i];
                w2 += lr * y[i] * x2[i];
                b += lr * y[i];
            }
        }
    }
    int q;
    cin >> q;
    while (q--) {
        double a, c;
        cin >> a >> c;
        double score = w1 * a + w2 * c + b;
        cout << (score >= 0 ? 1 : -1) << '\n';
    }
    return 0;
}
```

**测试设计：**

1. 输入：
```text
1 1 1
1 0 1
2
-1 0
0 0
```
期望输出：
```text
1
1
```

2. 输入：
```text
1 0 1
1 1 -1
1
5 5
```
期望输出：
```text
1
```

***

### V10-EX06 简化 SVM 更新

- 归属卷：第 10 卷
- 覆盖模块：AI-11 线性 SVM
- 考场用途：模拟 hinge loss 下的权重衰减和错边界更新。

**题目描述：** 给定一维样本和标签 `-1/+1`，初始 `w=b=0`。每轮对每个样本计算 `margin=y*(w*x+b)`。先执行 `w-=lr*lambda*w`。若 `margin<1`，再执行 `w+=lr*y*x,b+=lr*y`。训练后输出查询预测。

**输入格式：** 第一行 `n epoch lr lambda`。接下来 `n` 行 `x y`。然后一行 `q`。接下来 `q` 行每行一个 `x`。

**输出格式：** 每个查询输出 `-1` 或 `1`。

**样例输入：**
```text
2 1 1 0
-1 -1
1 1
3
-2
0
2
```

**样例输出：**
```text
-1
1
1
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, epoch;
    double lr, lambda;
    cin >> n >> epoch >> lr >> lambda;
    vector<double> x(n + 1);
    vector<int> y(n + 1);
    for (int i = 1; i <= n; i++) cin >> x[i] >> y[i];
    double w = 0, b = 0;
    for (int ep = 1; ep <= epoch; ep++) {
        for (int i = 1; i <= n; i++) {
            double margin = y[i] * (w * x[i] + b);
            w -= lr * lambda * w;
            if (margin < 1.0) {
                w += lr * y[i] * x[i];
                b += lr * y[i];
            }
        }
    }
    int q;
    cin >> q;
    while (q--) {
        double t;
        cin >> t;
        cout << (w * t + b >= 0 ? 1 : -1) << '\n';
    }
    return 0;
}
```

**测试设计：**

1. 输入：
```text
1 1 0.5 0
2 1
2
2
-2
```
期望输出：
```text
1
-1
```

2. 输入：
```text
1 0 1 0
5 -1
1
0
```
期望输出：
```text
1
```

***

### V10-EX07 DNN 前向传播

- 归属卷：第 10 卷
- 覆盖模块：AI-12 多层前向传播
- 考场用途：按层模拟全连接网络、ReLU 和 softmax。

**题目描述：** 给定多层全连接网络，按层计算输出。每层输入格式为 `out_dim activation`，随后 `out_dim` 行，每行当前输入维度个权重和一个 bias。激活支持 `none/relu/softmax`。输出预测类别和最终向量。

**输入格式：** 第一行 `L`。第二行输入维度 `d` 和 `d` 个输入值。随后按层给出参数。

**输出格式：** 第一行输出预测类别，编号从 1 开始，平分选小。第二行输出最终向量，保留 6 位。

**样例输入：**
```text
1
2 1 2
2 softmax
1 0 0
0 1 0
```

**样例输出：**
```text
2
0.268941 0.731059
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

void activate(vector<double> &a, const string &act) {
    int n = (int)a.size() - 1;
    if (act == "relu") {
        for (int i = 1; i <= n; i++) a[i] = max(0.0, a[i]);
    } else if (act == "softmax") {
        double mx = a[1];
        for (int i = 2; i <= n; i++) mx = max(mx, a[i]);
        double sum = 0;
        for (int i = 1; i <= n; i++) {
            a[i] = exp(a[i] - mx);
            sum += a[i];
        }
        for (int i = 1; i <= n; i++) a[i] /= sum;
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int L, d;
    cin >> L >> d;
    vector<double> cur(d + 1);
    for (int i = 1; i <= d; i++) cin >> cur[i];
    for (int layer = 1; layer <= L; layer++) {
        int out;
        string act;
        cin >> out >> act;
        vector<double> nxt(out + 1, 0);
        for (int i = 1; i <= out; i++) {
            for (int j = 1; j <= d; j++) {
                double w;
                cin >> w;
                nxt[i] += w * cur[j];
            }
            double b;
            cin >> b;
            nxt[i] += b;
        }
        activate(nxt, act);
        cur = nxt;
        d = out;
    }
    int pred = 1;
    for (int i = 2; i <= d; i++) if (cur[i] > cur[pred] + 1e-12) pred = i;
    cout << pred << '\n' << fixed << setprecision(6);
    for (int i = 1; i <= d; i++) {
        if (i > 1) cout << ' ';
        cout << cur[i];
    }
    cout << '\n';
    return 0;
}
```

**测试设计：**

1. 输入：
```text
1
2 1 -2
2 relu
1 0 0
0 1 0
```
期望输出：
```text
1
1.000000 0.000000
```

2. 输入：
```text
1
1 3
2 none
1 0
-1 0
```
期望输出：
```text
1
3.000000 -3.000000
```

***

### V10-EX08 二层网络反向传播一轮

- 归属卷：第 10 卷
- 覆盖模块：AI-14 反向传播
- 考场用途：手算链式法则并验证参数更新方向。

**题目描述：** 二层网络只有一个隐藏神经元：`z1=w1*x+b1,a1=max(0,z1),z2=w2*a1+b2,yhat=z2`。损失为 `0.5*(yhat-y)^2`。给定一个样本和学习率，执行一轮梯度下降，输出更新后的四个参数。

**输入格式：** 一行 `x y w1 b1 w2 b2 lr`。

**输出格式：** 输出更新后的 `w1 b1 w2 b2`，保留 6 位。

**样例输入：**
```text
2 5 1 0 1 0 0.1
```

**样例输出：**
```text
1.600000 0.300000 1.600000 0.300000
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    double x, y, w1, b1, w2, b2, lr;
    cin >> x >> y >> w1 >> b1 >> w2 >> b2 >> lr;
    double z1 = w1 * x + b1;
    double a1 = max(0.0, z1);
    double yhat = w2 * a1 + b2;
    double dz2 = yhat - y;
    double dw2 = dz2 * a1;
    double db2 = dz2;
    double da1 = dz2 * w2;
    double dz1 = z1 > 0 ? da1 : 0.0;
    double dw1 = dz1 * x;
    double db1 = dz1;
    w1 -= lr * dw1;
    b1 -= lr * db1;
    w2 -= lr * dw2;
    b2 -= lr * db2;
    cout << fixed << setprecision(6) << w1 << ' ' << b1 << ' ' << w2 << ' ' << b2 << '\n';
    return 0;
}
```

**测试设计：**

1. 输入：
```text
1 1 1 0 1 0 0.1
```
期望输出：
```text
1.000000 0.000000 1.000000 0.000000
```

2. 输入：
```text
1 2 -1 0 1 0 0.1
```
期望输出：
```text
-1.000000 0.000000 1.000000 0.200000
```

***

### V10-EX09 反向模式自动求导

- 归属卷：第 10 卷
- 覆盖模块：AI-15 自动求导
- 考场用途：计算图按拓扑序前向、逆序累加梯度。

**题目描述：** 给定拓扑序计算图，节点支持 `var value`、`const value`、`add a b`、`mul a b`、`sin a`。输出最后一个节点的值，以及所有变量节点按出现顺序的梯度。

**输入格式：** 第一行整数 `n`。接下来 `n` 行描述节点。

**输出格式：** 第一行输出节点 `n` 的值。第二行输出变量梯度，保留 6 位。

**样例输入：**
```text
5
var 2
var 3
mul 1 2
sin 1
add 3 4
```

**样例输出：**
```text
6.909297
2.583853 2.000000
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

struct Node {
    string op;
    int l = 0, r = 0;
    double val = 0, grad = 0;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<Node> a(n + 1);
    vector<int> vars;
    for (int i = 1; i <= n; i++) {
        cin >> a[i].op;
        if (a[i].op == "var" || a[i].op == "const") {
            cin >> a[i].val;
            if (a[i].op == "var") vars.push_back(i);
        } else if (a[i].op == "add" || a[i].op == "mul") {
            cin >> a[i].l >> a[i].r;
            if (a[i].op == "add") a[i].val = a[a[i].l].val + a[a[i].r].val;
            else a[i].val = a[a[i].l].val * a[a[i].r].val;
        } else if (a[i].op == "sin") {
            cin >> a[i].l;
            a[i].val = sin(a[a[i].l].val);
        }
    }
    a[n].grad = 1;
    for (int i = n; i >= 1; i--) {
        double g = a[i].grad;
        if (a[i].op == "add") {
            a[a[i].l].grad += g;
            a[a[i].r].grad += g;
        } else if (a[i].op == "mul") {
            int l = a[i].l, r = a[i].r;
            a[l].grad += g * a[r].val;
            a[r].grad += g * a[l].val;
        } else if (a[i].op == "sin") {
            int l = a[i].l;
            a[l].grad += g * cos(a[l].val);
        }
    }
    cout << fixed << setprecision(6) << a[n].val << '\n';
    for (int i = 0; i < (int)vars.size(); i++) {
        if (i) cout << ' ';
        cout << a[vars[i]].grad;
    }
    cout << '\n';
    return 0;
}
```

**测试设计：**

1. 输入：
```text
3
var 2
var 3
mul 1 2
```
期望输出：
```text
6.000000
3.000000 2.000000
```

2. 输入：
```text
2
var 0
sin 1
```
期望输出：
```text
0.000000
1.000000
```

***

### V10-EX10 Viterbi 与 accuracy 评分

- 归属卷：第 10 卷
- 覆盖模块：AI-07 Viterbi、AI-10 SPJ 评分
- 考场用途：用 log 概率做 HMM 最优路径，并计算预测准确率。

**题目描述：** 给定一个 HMM，输出观测序列的最可能隐藏状态路径。随后给出真实隐藏状态路径，输出路径预测准确率。概率为 0 时认为该路径不可走。

**输入格式：** 第一行 `n m T`。第二行 `n` 个初始概率。接下来 `n` 行转移矩阵。接下来 `n` 行发射矩阵。一行 `T` 个观测编号。一行 `T` 个真实状态编号。

**输出格式：** 第一行输出预测路径。第二行输出准确率，保留 6 位。

**样例输入：**
```text
2 2 3
0.6 0.4
0.7 0.3
0.4 0.6
0.5 0.5
0.1 0.9
1 2 2
1 2 2
```

**样例输出：**
```text
1 2 2
1.000000
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

const double NEG = -1e100;

double safe_log(double x) {
    return x <= 0 ? NEG : log(x);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m, T;
    cin >> n >> m >> T;
    vector<double> pi(n + 1);
    for (int i = 1; i <= n; i++) cin >> pi[i];
    vector<vector<double>> trans(n + 1, vector<double>(n + 1));
    for (int i = 1; i <= n; i++) for (int j = 1; j <= n; j++) cin >> trans[i][j];
    vector<vector<double>> emit(n + 1, vector<double>(m + 1));
    for (int i = 1; i <= n; i++) for (int j = 1; j <= m; j++) cin >> emit[i][j];
    vector<int> obs(T + 1), real(T + 1);
    for (int t = 1; t <= T; t++) cin >> obs[t];
    for (int t = 1; t <= T; t++) cin >> real[t];

    vector<vector<double>> dp(T + 1, vector<double>(n + 1, NEG));
    vector<vector<int>> pre(T + 1, vector<int>(n + 1, 1));
    for (int s = 1; s <= n; s++) dp[1][s] = safe_log(pi[s]) + safe_log(emit[s][obs[1]]);
    for (int t = 2; t <= T; t++) {
        for (int s = 1; s <= n; s++) {
            for (int p = 1; p <= n; p++) {
                double cur = dp[t - 1][p] + safe_log(trans[p][s]) + safe_log(emit[s][obs[t]]);
                if (cur > dp[t][s]) {
                    dp[t][s] = cur;
                    pre[t][s] = p;
                }
            }
        }
    }
    int last = 1;
    for (int s = 2; s <= n; s++) if (dp[T][s] > dp[T][last]) last = s;
    vector<int> path(T + 1);
    path[T] = last;
    for (int t = T; t >= 2; t--) path[t - 1] = pre[t][path[t]];

    int correct = 0;
    for (int t = 1; t <= T; t++) {
        if (t > 1) cout << ' ';
        cout << path[t];
        if (path[t] == real[t]) correct++;
    }
    cout << '\n' << fixed << setprecision(6) << (double)correct / T << '\n';
    return 0;
}
```

**测试设计：**

1. 输入：
```text
1 1 2
1
1
1
1 1
1 1
```
期望输出：
```text
1 1
1.000000
```

2. 输入：
```text
2 1 1
0.9 0.1
1 0
0 1
1
1
2
```
期望输出：
```text
1
0.000000
```

