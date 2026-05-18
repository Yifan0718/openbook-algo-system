# DP-08：分组背包

模型编号：DP-08

模型名称：分组背包

标签：DP、背包、分组、每组最多选一个

一句话用途：物品按组划分，每组最多选择一个，在容量限制下求最优值、方案数或可行性。

题面触发词：

- “每组最多选一个”
- “每类商品选一个/不选”
- “课程分组、套餐选择”
- “从每个集合中选择一个方案”

什么时候用：

- 物品天然分成若干组。
- 同一组内物品互斥。
- 组与组之间独立，只有容量共享。

不要什么时候用：

- 所有物品互不互斥，转 0/1 背包。
- 每组必须选一个时，初始化和答案要按“必须”改。
- 组内可以选多个，不能套“最多一个”。

复杂度：

- `O(总物品数 * W)`。
- 空间 `O(W)`。

数据范围信号：

- `组数 * W * 平均组大小` 可承受。
- 总物品数和容量都不大时直接套。

依赖的标准容器：

- `vector<vector<pair<int,ll>>> groups(G + 1)`
- `vector<ll> dp(W + 1), ndp(W + 1)`

输入如何整理：

- 把每件物品放入对应组：`groups[g].push_back({w, v})`。
- 组编号统一 `1..G`。

接口：

```cpp
ll group_knapsack(int G, int W, vector<vector<pair<int,ll>>>& groups);
```

输出能力：

- 最大价值。
- 每组选择方案的可行性或方案数。

下游可接：

- 树形依赖背包。
- 课程/套餐类选择。
- DP-24 背包常见变体总表：每组必须选、分组计数、路径恢复。

可拼接模块：

- Compressor：组编号散乱时压缩。
- PrefixSum：组内候选由区间预处理生成时使用。

状态句式：

```text
dp[j] 表示：已经处理完若干组，容量为 j 时的最大价值。
```

初始化：

```text
最多选一个且可以不选任何组：dp[j] = 0。
必须精确容量：dp[0] = 0，其他为 -LINF。
每组必须选一个：每处理一组时 ndp 初始为 -LINF，不能直接继承“不选”。
```

转移模板：

```cpp
ndp = dp; // 每组最多选一个：允许本组不选
for (auto [w, v] : group) {
    for (int j = w; j <= W; j++) {
        ndp[j] = max(ndp[j], dp[j - w] + v);
    }
}
dp.swap(ndp);
```

答案位置：

- 不超过容量：`dp[W]`。
- 恰好容量：`dp[W]`，但必须用不可达初始化。
- 任意容量：`max(dp[0..W])`。

循环顺序：

```text
外层枚举组。
组内枚举物品。
容量用 ndp 从旧 dp 转移，防止同组多个物品被同时选。
```

暴力 DFS 版本：

```cpp
ll dfs(int g, int rest) {
    if (rest < 0) return -LINF;
    if (g == G + 1) return 0;
    ll ans = dfs(g + 1, rest); // 本组不选
    for (auto [w, v] : groups[g]) {
        ans = max(ans, v + dfs(g + 1, rest - w));
    }
    return ans;
}
```

记忆化版本：

```cpp
vector<vector<ll>> memo;
vector<vector<int>> vis;

ll dfs(int g, int rest) {
    if (rest < 0) return -LINF;
    if (g == G + 1) return 0;
    if (vis[g][rest]) return memo[g][rest];
    vis[g][rest] = 1;
    ll ans = dfs(g + 1, rest);
    for (auto [w, v] : groups[g]) {
        ans = max(ans, v + dfs(g + 1, rest - w));
    }
    return memo[g][rest] = ans;
}
```

表推版本：

下面这段是“每组最多选一个，容量不超过 W”的最大价值版本；若要求恰好容量或每组必须选，要按初始化说明改 `-LINF`。

```cpp
vector<ll> dp(W + 1, 0);
for (int g = 1; g <= G; g++) {
    vector<ll> ndp = dp;
    for (auto [w, v] : groups[g]) {
        for (int j = w; j <= W; j++) {
            ndp[j] = max(ndp[j], dp[j - w] + v);
        }
    }
    dp.swap(ndp);
}
cout << dp[W] << '\n';
```

常见变体：

- 每组必须选一个：`ndp` 初始化为 `-LINF`，不复制 `dp`。
- 每组恰好选一个且容量不超过：答案 `max(dp[0..W])`。
- 组内候选是“方案”而非单物品，也可放进 `groups`。

常见坑：

- 直接在同一个 `dp` 上更新，导致同组多个物品被选。
- 忘记区分“最多选一个”和“必须选一个”。
- 组为空时，必须选一个会无解。
- 初始化全 0 导致恰好容量题错。

暴力/部分分替代：

- 组数小：DFS 枚举每组选择。
- 容量小：记忆化 `dfs(g, rest)`。
- 组内物品多但有效容量少：过滤 `w > W` 的物品。

升级方向：

- 分组背包 -> 树上分组/依赖背包。
- 组内候选通过其他 DP 先生成。
- 空间从二维压成一维 `dp + ndp`。
- 要恢复每组选了哪个方案时，优先写二维 `choice[g][j]`，见 DP-24。

最小测试样例：

```text
2 5
组1: (2,3) (3,4)
组2: (2,4) (4,7)
输出：8
说明：选组1的(3,4)和组2的(2,4)。
```
