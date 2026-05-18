# BRUTE-12：折半枚举

模块编号：BRUTE-12

模块名称：折半枚举

标签：meet-in-the-middle、折半、子集和、二分

一句话用途：当 `n <= 40` 导致 `2^n` 太大时，把元素分成两半分别枚举，再排序/二分合并。

题面触发词：

- `n <= 40`。
- 选若干个。
- 子集和。
- 不超过容量的最大值。
- 精确凑出某个和。

适用场景：

- 子集和。
- 0/1 选择但 `n` 在 30 到 44 左右。
- 需要统计两边组合满足某条件。

什么时候用：

- 直接 `2^n` 不行，但 `2^(n/2)` 可行。
- 左右两半结果可以合并。
- 合并能用排序、二分、双指针或哈希。

不要什么时候用：

- 选择之间有强顺序依赖，不能简单拆两半。
- 状态需要复杂路径信息，左右无法合并。
- `n` 很大，`2^(n/2)` 也不可行。

复杂度：

- 枚举：`O(2^(n/2))`。
- 排序：`O(2^(n/2) log 2^(n/2))`。
- 合并：通常 `O(2^(n/2) log 2^(n/2))` 或双指针。

数据范围参考：

- `n <= 40`：经典适用。
- `n <= 44`：看时限和内存。
- `n <= 50`：通常需要更强优化或其他算法。

依赖的标准容器：

- `vector`
- `algorithm`

输入如何整理：

- 把数组拆成 `[1, mid]` 和 `[mid+1, n]`。
- 分别枚举两半所有子集和。
- 对右半排序，左半每个值二分找搭配。

接口：

```cpp
vector<long long> enum_sums(int l, int r);
```

输出能力：

- 不超过 `W` 的最大子集和。
- 是否存在和为 `target`。
- 满足条件的方案数量。

下游可接：

- 二分。
- 双指针。
- 哈希计数。
- DP 卷背包优化思路。

可拼接模块：

- BRUTE-05 子集枚举。
- BRUTE-01 复杂度速查。

模板代码：

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int n;
ll W;
vector<ll> a;

vector<ll> enum_sums(int l, int r) {
    int len = r - l + 1;
    vector<ll> sums;
    long long total = 1LL << len;
    for (long long mask = 0; mask < total; mask++) {
        ll s = 0;
        for (int i = 0; i < len; i++) {
            if (mask & (1LL << i)) s += a[l + i];
        }
        sums.push_back(s);
    }
    return sums;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n >> W;
    a.assign(n + 1, 0);
    for (int i = 1; i <= n; i++) cin >> a[i];

    int mid = n / 2;
    vector<ll> L = enum_sums(1, mid);
    vector<ll> R = enum_sums(mid + 1, n);
    sort(R.begin(), R.end());

    ll best = 0;
    for (ll x : L) {
        if (x > W) continue;
        auto it = upper_bound(R.begin(), R.end(), W - x);
        if (it == R.begin()) {
            best = max(best, x);
        } else {
            --it;
            best = max(best, x + *it);
        }
    }

    cout << best << '\n';
    return 0;
}
```

调用示例：

```cpp
vector<ll> left = enum_sums(1, n / 2);
vector<ll> right = enum_sums(n / 2 + 1, n);
sort(right.begin(), right.end());
```

常见坑：

- `1 << len` 当 `len >= 31` 溢出；折半后一般 `len <= 22`。
- 右半为空时也要有和 `0`。
- `upper_bound` 返回 `begin()` 时不能直接 `--it`。
- 本页完整模板默认 `a[i] >= 0`、`W >= 0`、空集合法，因此可以跳过 `x > W` 的左半和。
- 如果有负数，不能用 `if (x > W) continue`，因为右半负数可能把总和拉回合法；此时删掉该剪枝并把 `best` 初始化成 `-LINF`。
- 统计方案数时要处理重复和。

暴力/部分分替代：

- `n <= 24`：直接枚举全部子集。
- `n <= 40`：折半枚举。
- 容量 `W` 小：背包 DP 可能更好。

升级方向：

- 折半 + 二分 -> 折半 + 双指针。
- 折半枚举 -> 哈希计数。
- 折半 -> 正式 DP 或搜索剪枝。

最小测试样例：

```text
输入：
4 10
2 4 8 9

输出：
10
```
