# STR-05 Manacher 回文算法

模块编号：STR-05

模块名称：Manacher 回文半径、最长回文子串、区间回文判断

标签：[字符串][回文][Manacher][最长回文子串][1-index]

一句话用途：在线性时间 `O(n)` 求每个中心能扩展出的最长回文半径，适合长字符串的最长回文子串、统计回文子串数量、大量区间回文判断。

索引约定：

```text
本模板把原字符串 raw 转成 1-index 字符串 s = " " + raw。
s[1..n] 是真实字符。

d1[i]：以 i 为中心的奇数回文半径。
覆盖区间：[i - d1[i] + 1, i + d1[i] - 1]。
对应最长奇数回文长度：2 * d1[i] - 1。

d2[i]：以 i-1 和 i 中间为中心的偶数回文半径。
覆盖区间：[i - d2[i], i + d2[i] - 1]。
对应最长偶数回文长度：2 * d2[i]。

题面如果给 1-index 区间 [l,r]，直接调用 is_pal(l,r)。
```

题面触发词：

- 最长回文子串。
- 回文半径。
- 回文子串数量。
- 很多次询问 `s[l..r]` 是否为回文。
- 字符串长度很大，中心扩展 `O(n^2)` 可能超时。

什么时候用：

- `n` 到 `1e5`、`1e6` 级别，需要处理所有回文中心。
- 回文查询次数很多，不能每次双指针检查。
- 需要把“某段是不是回文”作为 DP 或枚举的快速判断条件。

不要什么时候用：

- 只判断一个字符串整体是否回文：直接双指针或 `reverse`。
- 只做几次短区间回文判断：直接检查更快写。
- 需要动态修改字符串后再查回文：Manacher 是静态预处理，修改后要重建。
- 题目是“最长回文子序列”：那是 DP，不是 Manacher。

复杂度：

- 预处理：`O(n)`。
- 最长回文子串：预处理后 `O(n)` 扫一遍。
- 单次区间回文判断：`O(1)`。
- 统计回文子串数量：`O(n)`，答案可能需要 `long long`。

数据范围参考：

| 数据范围 | 建议 |
|---|---|
| `n <= 2000` | 中心扩展或区间 DP 都能尝试 |
| `n <= 1e5` | Manacher 稳 |
| `n <= 1e6` | Manacher + 静态全局数组，避免反复分配 |

依赖的标准容器：

- `string`：存原串和 1-index 处理串。
- 静态全局数组 `d1[]/d2[]`：存奇偶回文半径。

输入如何整理：

```cpp
string raw;
cin >> raw;
build_manacher(raw);
```

接口：

```text
build_manacher(raw)：预处理 d1/d2。
is_pal(l,r)：判断 1-index 闭区间 [l,r] 是否为回文。
longest_pal_len()：返回最长回文子串长度。
count_pal_substrings()：返回回文子串总数。
```

模板代码：

```cpp
const int MAXN = 1000000 + 5;

int n;
string s;          // s[1..n]
int d1[MAXN];      // odd radius
int d2[MAXN];      // even radius, center between i-1 and i

void build_manacher(const string &raw) {
    n = (int)raw.size();
    s = " " + raw;

    int l = 1, r = 0;
    for (int i = 1; i <= n; i++) {
        int k = (i > r) ? 1 : min(d1[l + r - i], r - i + 1);
        while (i - k >= 1 && i + k <= n && s[i - k] == s[i + k]) {
            k++;
        }
        d1[i] = k;
        if (i + k - 1 > r) {
            l = i - k + 1;
            r = i + k - 1;
        }
    }

    l = 1;
    r = 0;
    for (int i = 1; i <= n; i++) {
        int k = (i > r) ? 0 : min(d2[l + r - i + 1], r - i + 1);
        while (i - k - 1 >= 1 && i + k <= n && s[i - k - 1] == s[i + k]) {
            k++;
        }
        d2[i] = k;
        if (i + k - 1 > r) {
            l = i - k;
            r = i + k - 1;
        }
    }
}

bool is_pal(int l, int r) {
    if (l > r) return true;
    if (l < 1 || r > n) return false;
    int len = r - l + 1;
    if (len & 1) {
        int mid = (l + r) / 2;
        return d1[mid] >= len / 2 + 1;
    } else {
        int mid = (l + r + 1) / 2;
        return d2[mid] >= len / 2;
    }
}

int longest_pal_len() {
    int ans = 0;
    for (int i = 1; i <= n; i++) {
        ans = max(ans, 2 * d1[i] - 1);
        ans = max(ans, 2 * d2[i]);
    }
    return ans;
}

long long count_pal_substrings() {
    long long ans = 0;
    for (int i = 1; i <= n; i++) {
        ans += d1[i];
        ans += d2[i];
    }
    return ans;
}
```

完整可运行代码 1：最长回文子串长度

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MAXN = 1000000 + 5;

int n;
string s;
int d1[MAXN], d2[MAXN];

void build_manacher(const string &raw) {
    n = (int)raw.size();
    s = " " + raw;

    int l = 1, r = 0;
    for (int i = 1; i <= n; i++) {
        int k = (i > r) ? 1 : min(d1[l + r - i], r - i + 1);
        while (i - k >= 1 && i + k <= n && s[i - k] == s[i + k]) k++;
        d1[i] = k;
        if (i + k - 1 > r) {
            l = i - k + 1;
            r = i + k - 1;
        }
    }

    l = 1;
    r = 0;
    for (int i = 1; i <= n; i++) {
        int k = (i > r) ? 0 : min(d2[l + r - i + 1], r - i + 1);
        while (i - k - 1 >= 1 && i + k <= n && s[i - k - 1] == s[i + k]) k++;
        d2[i] = k;
        if (i + k - 1 > r) {
            l = i - k;
            r = i + k - 1;
        }
    }
}

int longest_pal_len() {
    int ans = 0;
    for (int i = 1; i <= n; i++) {
        ans = max(ans, 2 * d1[i] - 1);
        ans = max(ans, 2 * d2[i]);
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string raw;
    cin >> raw;
    build_manacher(raw);
    cout << longest_pal_len() << "\n";
    return 0;
}
```

完整可运行代码 2：多次判断区间是否回文

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MAXN = 1000000 + 5;

int n;
string s;
int d1[MAXN], d2[MAXN];

void build_manacher(const string &raw) {
    n = (int)raw.size();
    s = " " + raw;

    int l = 1, r = 0;
    for (int i = 1; i <= n; i++) {
        int k = (i > r) ? 1 : min(d1[l + r - i], r - i + 1);
        while (i - k >= 1 && i + k <= n && s[i - k] == s[i + k]) k++;
        d1[i] = k;
        if (i + k - 1 > r) {
            l = i - k + 1;
            r = i + k - 1;
        }
    }

    l = 1;
    r = 0;
    for (int i = 1; i <= n; i++) {
        int k = (i > r) ? 0 : min(d2[l + r - i + 1], r - i + 1);
        while (i - k - 1 >= 1 && i + k <= n && s[i - k - 1] == s[i + k]) k++;
        d2[i] = k;
        if (i + k - 1 > r) {
            l = i - k;
            r = i + k - 1;
        }
    }
}

bool is_pal(int l, int r) {
    if (l > r) return true;
    if (l < 1 || r > n) return false;
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

    string raw;
    cin >> raw;
    build_manacher(raw);

    int q;
    cin >> q;
    while (q--) {
        int l, r;
        cin >> l >> r;
        cout << (is_pal(l, r) ? "YES" : "NO") << "\n";
    }
    return 0;
}
```

调用示例：

```cpp
string raw = "abacaba";
build_manacher(raw);
cout << longest_pal_len() << "\n";       // 7
cout << is_pal(1, 7) << "\n";            // true
cout << count_pal_substrings() << "\n";  // 所有回文子串个数
```

常见坑：

- `d1[i]` 和 `d2[i]` 是半径，不是长度。
- 奇数回文中心是一个字符 `i`；偶数回文中心是缝隙，在 `i-1` 和 `i` 之间。
- 题面如果给的是 1-index 区间，本模板可以直接用；不要再 `l--, r--`。
- 空格、中文等复杂字符按字节处理；算法竞赛通常是小写字母或 ASCII 字符。
- `count_pal_substrings()` 可能到 `n*(n+1)/2`，必须用 `long long`。
- Manacher 只能处理静态字符串，字符串修改后必须重建。

暴力/部分分替代：

```cpp
bool slow_pal(const string &raw, int l, int r) {
    // raw 是普通 0-index string，题面 [l,r] 是 1-index。
    l--;
    r--;
    while (l < r) {
        if (raw[l] != raw[r]) return false;
        l++;
        r--;
    }
    return true;
}
```

- `n <= 2000`：可以枚举中心向两边扩展，求最长回文。
- `q` 很小：每次双指针判断区间，先拿部分分。
- 题目是“最少切成若干回文串”：先用 Manacher 或 `slow_pal` 得到 `is_pal(l,r)`，再接 DP。

最小测试样例 1：

```text
输入：
babad

输出：
3
```

最小测试样例 2：

```text
输入：
abacaba
4
1 7
2 4
2 6
3 5

输出：
YES
NO
YES
YES
```
