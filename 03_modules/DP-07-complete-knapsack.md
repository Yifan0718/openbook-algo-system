# DP-07：完全背包

模型编号：DP-07

模型名称：完全背包

标签：DP、背包、容量、无限次选择

一句话用途：每种物品可以重复选任意次，在容量限制下求最优值、方案数或可行性。

题面触发词：

- “每种物品有无限个”
- “可以重复购买/使用”
- “硬币凑金额”
- “不限数量”

什么时候用：

- 每种物品重复选择不受次数限制。
- 重复选同一种物品仍消耗同样容量并获得同样收益。

不要什么时候用：

- 每个物品最多一次，转 0/1 背包。
- 每种物品有有限个，需多重背包或拆分。
- 题目要求排列数/组合数时，循环顺序要额外确认。

复杂度：

- `O(nW)` 时间。
- `O(W)` 空间。

数据范围信号：

- `n * W <= 1e7` 左右较稳。
- “硬币数量不限，金额 W 不大”是典型信号。

依赖的标准容器：

- `vector<int> w(n + 1)`
- `vector<ll> v(n + 1)`
- `vector<ll> dp(W + 1)`

输入如何整理：

- `w[i]`：每次选择的容量消耗。
- `v[i]`：每次选择的价值。

接口：

```cpp
ll complete_knapsack(int n, int W, vector<int>& w, vector<ll>& v);
```

输出能力：

- 最大价值。
- 凑金额方案数。
- 能否凑出。

下游可接：

- 计数 DP。
- 最短/最少硬币数 DP。
- DP-24 背包常见变体总表：组合数/排列数、多重背包、至少装满。

可拼接模块：

- MOD 计数模板。
- GCD：硬币问题可先判断可达性必要条件。

状态句式：

```text
dp[j] 表示：当前已处理若干种物品，容量为 j 时的最大价值/方案数/最少数量。
```

初始化：

```text
最大值不要求装满：dp[j] = 0。
恰好装满最大值：dp[0] = 0，其他为 -LINF。
最少数量：dp[0] = 0，其他为 LINF。
方案数：dp[0] = 1。
```

转移模板：

```cpp
dp[j] = max(dp[j], dp[j - w[i]] + v[i]);
```

前置条件：普通完全背包默认 `w[i] > 0`。如果 `w[i] == 0`，必须按题意单独处理；`v[i] > 0` 的最优值可能无限大，方案数也可能不是有限数。

答案位置：

- 最大价值：`dp[W]`。
- 恰好金额方案数：`dp[W]`。
- 任意不超过容量：通常 `dp[W]` 已包含“不装满”的最优。

循环顺序：

```text
物品 i 从 1 到 n。
容量 j 从 w[i] 正序到 W，允许当前物品被重复使用。
```

暴力 DFS 版本：

下面这份是“不超过容量”的最大价值版本；若要求恰好装满，终止条件要改成 `rest == 0 ? 0 : -LINF`。

```cpp
ll dfs(int i, int rest) {
    if (rest < 0) return -LINF;
    if (i == n + 1) return 0;
    ll ans = dfs(i + 1, rest); // 不再选第 i 种
    if (rest >= w[i]) ans = max(ans, v[i] + dfs(i, rest - w[i])); // 继续选 i
    return ans;
}
```

记忆化版本：

```cpp
vector<vector<ll>> memo;
vector<vector<int>> vis;

ll dfs(int i, int rest) {
    if (rest < 0) return -LINF;
    if (i == n + 1) return 0;
    if (vis[i][rest]) return memo[i][rest];
    vis[i][rest] = 1;
    ll ans = dfs(i + 1, rest);
    if (rest >= w[i]) ans = max(ans, v[i] + dfs(i, rest - w[i]));
    return memo[i][rest] = ans;
}
```

表推版本：

下面这段是“不超过容量 W 的最大价值”版本，`dp` 全 0，表示不选也合法。

```cpp
vector<ll> dp(W + 1, 0);
for (int i = 1; i <= n; i++) {
    for (int j = w[i]; j <= W; j++) {
        dp[j] = max(dp[j], dp[j - w[i]] + v[i]);
    }
}
cout << dp[W] << '\n';
```

如果题目要求“恰好装满 W”，必须换初始化：

```cpp
vector<ll> dp(W + 1, -LINF);
dp[0] = 0;
for (int i = 1; i <= n; i++) {
    for (int j = w[i]; j <= W; j++) {
        if (dp[j - w[i]] != -LINF) {
            dp[j] = max(dp[j], dp[j - w[i]] + v[i]);
        }
    }
}
cout << (dp[W] == -LINF ? -1 : dp[W]) << '\n';
```

方案数表推：

```cpp
vector<ll> dp(W + 1, 0);
dp[0] = 1;
for (int i = 1; i <= n; i++) {
    if (w[i] <= 0) throw runtime_error("complete knapsack count needs positive weight");
    for (int j = w[i]; j <= W; j++) {
        dp[j] = (dp[j] + dp[j - w[i]]) % MOD;
    }
}
```

常见变体：

- 最少硬币数：`dp[j] = min(dp[j], dp[j-w[i]] + 1)`。
- 排列数：通常容量外层、物品内层。
- 组合数：物品外层、容量内层。
- 完全背包计数默认每种物品重量为正；零重量物品要先特判，不要直接套 `dp[j] += dp[j]`。

常见坑：

- 把容量写成倒序，变成 0/1 背包。
- 计数题没区分组合数和排列数。
- 最少数量初始化成 0，导致所有状态都像可达。
- `w[i]=0` 且 `v[i]>0` 会无限收益，需特殊判断。

暴力/部分分替代：

- DFS 枚举每种物品取几个。
- 小 `W` 时记忆化很稳。
- 不会一维时先写二维 `dp[i][j]`。

升级方向：

- 二维 -> 一维正序。
- 有数量上限 -> 多重背包/二进制拆分。
- 转移带滑窗限制 -> 单调队列优化。
- 计数题先到 DP-24 区分组合数和排列数。

最小测试样例：

```text
2 5
2 3
3 4
输出：7
说明：2+3 容量，价值 7。
```
