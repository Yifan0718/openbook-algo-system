# BRUTE-05：子集枚举与子集的子集

模块编号：BRUTE-05

模块名称：子集枚举与子集的子集

标签：bitmask、子集、状压、枚举子掩码

一句话用途：当 `n <= 20` 且状态是集合时，用二进制掩码枚举集合、子集或子集的子集。

题面触发词：

- 集合。
- 已选择/未选择。
- 访问过哪些点。
- `n <= 20`。
- 状态压缩、二进制。

适用场景：

- 枚举所有子集。
- 求每个集合的代价。
- 枚举 `mask` 的所有子集 `sub`。
- 状压 DP 的预处理或转移。

什么时候用：

- 元素数量不超过 20 到 22。
- 集合能用一个整数表示。
- 需要快速判断某元素是否已选。

不要什么时候用：

- `n >= 25` 且需要枚举全部 `2^n`。
- 集合元素不是小整数编号，需先压缩。
- 子集的子集总复杂度是 `O(3^n)`，不能误以为是 `O(2^n)`。

复杂度：

- 所有子集：`O(2^n * check_cost)`。
- 所有 `mask` 的所有 `sub`：总计 `O(3^n)`。
- 空间：常见 `O(2^n)`。

数据范围参考：

- `n <= 20`：`2^n` 通常可用。
- `n <= 16`：`3^n` 可能可用。
- `n > 22`：优先考虑折半或其他模型。

依赖的标准容器：

- 全局静态数组。

输入如何整理：

- 元素编号保持 `1..n`。
- 第 `i` 个元素对应 mask 的第 `i-1` 位。
- 字符串仍按 C++ 自然下标；普通数组不改 0-index。

接口：

```cpp
for (int mask = 0; mask < (1 << n); mask++) {}
for (int sub = mask; sub; sub = (sub - 1) & mask) {}
```

输出能力：

- 子集最大/最小值。
- 方案计数。
- 状压 DP 预处理。
- 集合划分转移。

下游可接：

- 状压 DP。
- BRUTE-12 折半枚举。
- BRUTE-07 记忆化搜索。

可拼接模块：

- BRUTE-01 复杂度速查。
- BRUTE-10 unordered_map 编码 memo。

模板代码：

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    if (n < 0) {
        cout << 0 << '\n';
        return 0;
    }
    if (n > 22) {
        // 本完整示例只覆盖 n<=22；大数据走合法兜底，至少保证有输出。
        ll x;
        for (int i = 1; i <= n; i++) cin >> x;
        cout << 0 << '\n';
        return 0;
    }
    static ll a[25];
    for (int i = 1; i <= n; i++) cin >> a[i];

    int total = 1 << n;
    static ll sum[1 << 22];
    for (int mask = 1; mask < total; mask++) {
        int b = __builtin_ctz(mask);
        int prev = mask ^ (1 << b);
        sum[mask] = sum[prev] + a[b + 1];
    }

    ll best = 0;
    for (int mask = 0; mask < total; mask++) {
        best = max(best, sum[mask]);
    }

    cout << best << '\n';
    return 0;
}
```

调用示例：

```cpp
// 枚举 mask 的所有子集，包括 0。
for (int sub = mask; ; sub = (sub - 1) & mask) {
    // use sub
    if (sub == 0) break;
}

// 枚举非空子集。
for (int sub = mask; sub; sub = (sub - 1) & mask) {
    // use sub
}
```

常见坑：

- `1 << n` 当 `n >= 31` 会溢出，应使用 `1LL << n`，但通常 `n` 不应这么大。
- 子集枚举包含空集时，循环要手动在 `sub == 0` 后 `break`。
- `__builtin_ctz(0)` 未定义，必须保证 `mask != 0`。
- 业务元素编号保持 1-index；只有取位时用 `i-1` 或 `b+1` 转回元素编号。

暴力/部分分替代：

- `n <= 20`：直接子集枚举。
- `n <= 40`：折半枚举左右两半。
- 集合 + 最优值：尝试 `dp[mask]` 或 `dfs(mask)` + memo。

升级方向：

- 子集枚举 -> 状压 DP。
- 子集的子集 -> 集合划分 DP。
- `2^n` -> 折半枚举。

最小测试样例：

```text
输入：
3
1 -2 4

输出：
5
```
