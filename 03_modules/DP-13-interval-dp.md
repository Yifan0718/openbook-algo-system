# DP-13：区间 DP

模型编号：DP-13

模型名称：区间 DP

标签：DP、区间、合并、分割点、回文、两端取

一句话用途：处理“只考虑区间 [l,r]”的最优合并、删除、匹配或博弈类问题。

题面触发词：

- “区间合并”
- “合并石子”
- “括号匹配”
- “回文删除”
- “每次从两端取”
- “删除一段/合并相邻”

什么时候用：

- 子问题天然是连续区间。
- 大区间可以由小区间合并。
- 转移常枚举分割点 `k` 或两端决策。

不要什么时候用：

- 只是区间查询/修改，转数据结构。
- 子集不要求连续，可能是状压或背包。
- 数据 `n > 1000` 且需要 `O(n^3)` 时，必须找优化或别的模型。

复杂度：

- 常见 `O(n^3)`：长度 * 左端点 * 分割点。
- 两端转移可为 `O(n^2)`。

数据范围信号：

- `n <= 300/500`：`O(n^3)` 常见。
- `n <= 5000`：只能做 `O(n^2)` 或优化。

依赖的标准容器：

- `vector<vector<ll>> dp`
- `vector<ll> prefix`：区间和代价。

输入如何整理：

- 序列 1-index。
- 预处理 `sum(l,r)`。

接口：

```cpp
ll interval_dp(int n, vector<ll>& a);
```

输出能力：

- 区间最小/最大合并代价。
- 回文/括号匹配最优值。
- 两端取最优差值。

下游可接：

- PrefixSum。
- 记忆化 DFS。

可拼接模块：

- PrefixSum：`cost(l,r)`。
- 记忆化搜索：先写 `dfs(l,r)`。

状态句式：

```text
dp[l][r] 表示：只考虑闭区间 [l,r] 时的最优值/方案数。
```

初始化：

```text
len = 1 的区间通常为 0 或 a[l]，按题意。
最小值题其他状态为 LINF；最大值题为 -LINF。
```

转移模板：

枚举分割点：

```cpp
dp[l][r] = min(dp[l][r], dp[l][k] + dp[k + 1][r] + cost(l, r));
```

两端选择：

```cpp
dp[l][r] = max(a[l] - dp[l + 1][r], a[r] - dp[l][r - 1]);
```

答案位置：

- 整段答案：`dp[1][n]`。

循环顺序：

```text
for len = 1..n
  for l = 1..n-len+1
    r = l + len - 1
    枚举转移
```

暴力 DFS 版本：

```cpp
ll dfs(int l, int r) {
    if (l == r) return 0;
    ll ans = LINF;
    for (int k = l; k < r; k++) {
        ans = min(ans, dfs(l, k) + dfs(k + 1, r) + sum(l, r));
    }
    return ans;
}
```

记忆化版本：

```cpp
vector<vector<ll>> memo;
vector<vector<int>> vis;

ll dfs(int l, int r) {
    if (l == r) return 0;
    if (vis[l][r]) return memo[l][r];
    vis[l][r] = 1;
    ll ans = LINF;
    for (int k = l; k < r; k++) {
        ans = min(ans, dfs(l, k) + dfs(k + 1, r) + sum(l, r));
    }
    return memo[l][r] = ans;
}
```

表推版本：

```cpp
vector<vector<ll>> dp(n + 2, vector<ll>(n + 2, 0));
for (int len = 2; len <= n; len++) {
    for (int l = 1; l + len - 1 <= n; l++) {
        int r = l + len - 1;
        dp[l][r] = LINF;
        for (int k = l; k < r; k++) {
            dp[l][r] = min(dp[l][r], dp[l][k] + dp[k + 1][r] + sum(l, r));
        }
    }
}
cout << dp[1][n] << '\n';
```

常见变体：

- 环形区间 DP：复制一倍序列，枚举长度 `n` 的区间。
- 回文匹配：转移可能看 `a[l] == a[r]`。
- 两端取博弈：`dp[l][r]` 常表示当前玩家领先分差。

常见坑：

- 没按长度从小到大，导致依赖未算。
- 分割点范围写成 `k <= r`。
- `sum(l,r)` 没有 `O(1)` 预处理，复杂度多乘一层。
- `dp[l][r]` 初值忘记按最小/最大设置。

暴力/部分分替代：

- `n <= 20`：递归枚举。
- `n <= 300`：区间表推。
- 表推顺序想不清：先记忆化 `dfs(l,r)`。

升级方向：

- PrefixSum 优化代价。
- 四边形不等式/Knuth 优化属于高阶，低优先级。
- 环形问题复制数组。

最小测试样例：

```text
3
1 2 3
输出：9
说明：先合并 1+2 花 3，再和 3 合并花 6，总 9。
```

