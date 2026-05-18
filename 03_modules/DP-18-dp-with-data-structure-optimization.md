# DP-18：DP + 数据结构优化

模型编号：DP-18

模型名称：DP + 数据结构优化

标签：DP、树状数组、SegmentTree、单调队列、前缀和、优化转移

一句话用途：当普通 DP 需要枚举大量前驱 `j` 时，用数据结构快速查询前驱最优值。

题面触发词：

- `n <= 2e5` 但朴素 DP 是 `O(n^2)`
- “从前面某个范围转移”
- “满足 a[j] <= a[i] 的最大 dp[j]”
- “滑动窗口内最优”
- “区间最大/最小前缀”

什么时候用：

- 已经写出朴素转移 `dp[i] = merge(dp[j] + gain)`。
- 前驱 `j` 的合法条件能变成区间查询、前缀查询或滑窗最值。
- 数据范围要求优化到 `O(n log n)` 或 `O(n)`。

不要什么时候用：

- 朴素 DP 已能过，不必强行优化。
- 前驱条件无法用单调性、区间或值域表达。
- 转移有复杂二维条件，数据结构维护不了。

复杂度：

- PrefixSum 优化：通常 `O(n^2)` 降一层或减少求代价常数。
- 树状数组/SegmentTree：`O(n log n)`。
- 单调队列：`O(n)`。

数据范围信号：

- `n <= 5000`：朴素 `O(n^2)` 可先交。
- `n <= 2e5`：优先找 树状数组/SegmentTree/单调队列。

依赖的标准容器：

- `vector<ll> dp`
- `Compressor`
- `树状数组最大值版` 或 `SegmentTree`
- `deque<int>`：单调队列

输入如何整理：

- 把前驱限制写成查询条件：`key[j] <= key[i]`、`L <= j <= R`、`value in [l,r]`。
- 值域大时先坐标压缩。

接口：

```cpp
// 查询前面 key <= x 的最大 dp
best = bit.prefix(pos(x));
bit.add(pos(key[i]), dp[i]);
```

输出能力：

- 优化后的最大值/最小值 DP。
- 带权 LIS、分段 DP、滑窗 DP。

下游可接：

- 树状数组。
- SegmentTree。
- PrefixSum。
- MonotonicQueue。
- Compressor。

可拼接模块：

- DS-树状数组：前缀最大/最小。
- DS-SegmentTree：区间最大/最小。
- DS-MonotonicQueue：滑动窗口最值。
- PrefixSum：`cost(l,r)`。

状态句式：

```text
dp[i] 表示：以第 i 个元素作为最后一步时的最优值。
```

优化查询句式：

```text
需要从所有满足条件的 j 中取 max/min dp[j]，把这个集合交给数据结构查询。
```

## 先问：这个 DP 真的能用数据结构优化吗？

考场上不要一看到 `O(n^2)` 就硬套树状数组或线段树。先把朴素式子写完整：

```text
dp[i] = max/min over j < i and ok(j,i) of dp[j] + gain(j,i)
```

然后按下面四问判断：

| 问题 | 如果答案是“是” | 常用模块 |
|---|---|---|
| 合法前驱是不是一段下标区间？ | `L(i) <= j <= R(i)` | 单调队列 / SegmentTree |
| 合法前驱是不是一段值域区间？ | `a[j] <= a[i]` 或 `L <= a[j] <= R` | 树状数组 / SegmentTree + 离散化 |
| `gain(j,i)` 能不能拆成“只和 j 有关 + 只和 i 有关”？ | `dp[j] + A[j] + B[i]` | 维护 `dp[j]+A[j]` 的最值 |
| 区间代价是不是反复求和？ | `cost(l,r)` | PrefixSum / 二维前缀和 |

如果四个问题都答不上来，就先交朴素 `O(n^2)` 或记忆化版本。强行上数据结构通常会把状态含义写乱。

初始化：

```text
dp[i] 至少可以单独选择 i，初值为 base(i)。
树状数组/SegmentTree 初始为不可达值；如果允许空前驱，先加入空状态。
```

转移模板：

朴素：

```cpp
dp[i] = base(i);
for (int j = 1; j < i; j++) {
    if (ok(j, i)) dp[i] = max(dp[i], dp[j] + gain(j, i));
}
```

树状数组优化：

```cpp
dp[i] = base(i) + bit.prefix(pos(key[i]));
bit.add(pos(key[i]), dp[i]);
```

这段只适用于 `gain(j,i)` 能拆成“前驱可维护的值 + 当前 i 的值”的情况。若真实转移是 `dp[j] + cost(j,i)` 且 `cost` 同时复杂依赖 `j` 和 `i`，树状数组不能直接替代枚举。

答案位置：

- 常见：`max(dp[1..n])`。
- 如果必须以 `n` 结尾：`dp[n]`。

循环顺序：

- 通常 `i` 从 1 到 `n`。
- 查询只看已经加入的数据结构的前驱。
- 算完 `dp[i]` 后再把 `i` 加入数据结构。

暴力 DFS 版本：

```cpp
ll dfs(int i) {
    if (vis[i]) return memo[i];
    vis[i] = 1;
    ll ans = base(i);
    for (int j = 1; j < i; j++) {
        if (ok(j, i)) ans = max(ans, dfs(j) + gain(j, i));
    }
    return memo[i] = ans;
}
```

记忆化版本：

```cpp
vector<ll> memo(n + 1);
vector<int> vis(n + 1, 0);

ll dfs(int i) {
    if (vis[i]) return memo[i];
    vis[i] = 1;
    ll ans = base(i);
    for (int j = 1; j < i; j++) {
        if (ok(j, i)) ans = max(ans, dfs(j) + gain(j, i));
    }
    return memo[i] = ans;
}
```

表推版本（朴素）：

```cpp
vector<ll> dp(n + 1, -LINF);
ll ans = -LINF;
for (int i = 1; i <= n; i++) {
    dp[i] = base(i);
    for (int j = 1; j < i; j++) {
        if (ok(j, i)) dp[i] = max(dp[i], dp[j] + gain(j, i));
    }
    ans = max(ans, dp[i]);
}
cout << ans << '\n';
```

树状数组最大值版本：

```cpp
struct BITMax {
    int n;
    vector<ll> bit;
    BITMax(int n = 0) { init(n); }
    void init(int n_) { n = n_; bit.assign(n + 1, -LINF); }
    void add(int idx, ll val) {
        for (; idx <= n; idx += idx & -idx) bit[idx] = max(bit[idx], val);
    }
    ll prefix(int idx) {
        ll ans = -LINF;
        for (; idx > 0; idx -= idx & -idx) ans = max(ans, bit[idx]);
        return ans;
    }
};

// 例：带权 LIS，要求 a[j] < a[i]，收益为 w[i]
vector<ll> vals = a;
sort(vals.begin() + 1, vals.end());
vals.erase(unique(vals.begin() + 1, vals.end()), vals.end());
auto pos = [&](ll x) {
    return int(lower_bound(vals.begin() + 1, vals.end(), x) - vals.begin());
};

BITMax bit((int)vals.size() + 2);
ll ans = 0; // 如果必须选至少一个且权值可能全负，改成 -LINF
for (int i = 1; i <= n; i++) {
    int p = pos(a[i]);
    ll best = bit.prefix(p - 1);
    ll dp_i = w[i] + max(0LL, best);
    bit.add(p, dp_i);
    ans = max(ans, dp_i);
}
cout << ans << '\n';
```

如果题目要求至少选一个且 `w[i]` 可能为负，保留 `dp_i = w[i] + max(0LL, best)` 仍然可以让每个元素单独开头，但 `ans` 必须初始化为 `-LINF`，不能用 `0` 当空方案答案。

单调队列优化句式：

```text
如果 dp[i] = min(dp[j] + cost(i)) 且 j 只在 [i-K, i-1]，维护窗口内最小 dp[j]。
```

常见变体：

- `key[j] <= key[i]`：树状数组前缀查询。
- `L <= key[j] <= R`：SegmentTree 区间查询。
- `i-K <= j <= i-1`：单调队列。
- `cost(l,r)` 多次出现：PrefixSum。

常见坑：

- 先 `add(i)` 再 `query`，把自己当成前驱。
- 坐标压缩后严格 `<` 和 `<=` 的查询位置不同。
- 树状数组默认做前缀，区间查询要用 SegmentTree 或两个前缀处理。
- 最大值树初始值不能是 0，除非空前驱合法。

暴力/部分分替代：

- `n <= 5000`：朴素 `O(n^2)`。
- 优化写不出：先交朴素表推。
- 查询条件复杂：先用记忆化/朴素确认答案。

升级方向：

- 朴素前驱枚举 -> 树状数组/SegmentTree 查询。
- 固定窗口 -> 单调队列。
- 区间代价重复计算 -> PrefixSum。
- 空间大 -> 滚动数组。

最小测试样例：

```text
5
a: 1 3 2 4 3
w: 2 5 4 6 7
带权严格递增 LIS 输出：13
说明：1(2) -> 2(4) -> 3(7)。
```
