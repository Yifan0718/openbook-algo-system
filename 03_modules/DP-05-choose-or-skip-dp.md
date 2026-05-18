# DP-05：选/不选 DP

模型编号：DP-05

模型名称：选/不选 DP

标签：DP、子集、决策树、部分分、记忆化

一句话用途：每个元素只有“选/不选”两条路时，先写 DFS，再按状态维度升级成 DP。

题面触发词：

- “每个元素可以选或不选”
- “从若干物品中选择一些”
- “最多/恰好选 k 个”
- “满足限制的子集数量”
- “选择若干项目使收益最大/代价最小”

什么时候用：

- 决策是按元素逐个推进。
- 除了位置 `i`，还要记住数量、容量、余数、上一状态等。
- 还没确定是不是背包、状压或线性 DP 时，它是通用入口。

不要什么时候用：

- `n <= 20` 且需要枚举集合关系，状压可能更直接。
- 物品有容量维度且每个最多一次，优先 0/1 背包。
- 选择顺序本身重要，不只是选集合。

复杂度：

- 暴力：`O(2^n)`。
- 记忆化/DP：`O(状态数 * 2)`。

数据范围信号：

- `n <= 25`：暴力 DFS 可能拿分。
- `n <= 1000` 且有 `k/W/mod` 小维度：二维 DP。
- `n <= 2e5`：通常要压缩状态或转其他模型。

依赖的标准容器：

- `vector<ll> a(n + 1)`
- `vector<vector<ll>> memo/dp`
- `map<tuple<...>, ll>`：状态复杂时使用。

输入如何整理：

- 统一每个元素的属性：`cost[i]`、`val[i]`、`type[i]`。
- 把限制整理成状态参数：`cnt`、`rest`、`mod`、`last`。

接口：

```cpp
ll dfs(int i, int state);
```

输出能力：

- 最大值、最小值、方案数、可行性。

下游可接：

- DP-06 0/1 背包。
- DP-16 状压 DP。
- BRUTE 记忆化搜索。

可拼接模块：

- `map<tuple>` memo。
- Compressor：状态值域大时先压缩。
- PrefixSum：计算已选前缀贡献。

状态句式：

```text
dfs(i, rest) 表示：从第 i 个元素开始，当前剩余资源为 rest 时，后续能得到的最优值。
```

表推句式：

```text
dp[i][j] 表示：处理完前 i 个元素，附加状态为 j 时的答案。
```

初始化：

```text
dp[0][初始状态] = 0/1/true：还没处理元素时，只有初始状态合法。
其他状态为不可达。
```

转移模板：

```cpp
// 不选
dp[i][j] = merge(dp[i][j], dp[i - 1][j]);
// 选
dp[i][next(j, i)] = merge(dp[i][next(j, i)], dp[i - 1][j] + gain(i));
```

答案位置：

- 恰好达到状态：`dp[n][target]`。
- 任意合法状态：`max/min/sum dp[n][j]`。
- DFS 版本：`dfs(1, initial_state)`。

循环顺序：

- 二维表：`i` 从 1 到 `n`，`j` 枚举所有合法状态。
- 一维滚动：看是否与背包一致；0/1 场景通常倒序。

暴力 DFS 版本：

下面这份是“容量至多为 W”的最大值版本；如果题目要求恰好用完容量，终止条件要改成 `rest == 0 ? 0 : -LINF`。

```cpp
ll dfs(int i, int rest) {
    if (rest < 0) return -LINF;
    if (i == n + 1) return 0;
    ll ans = dfs(i + 1, rest); // 不选
    ans = max(ans, val[i] + dfs(i + 1, rest - cost[i])); // 选
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
    ans = max(ans, val[i] + dfs(i + 1, rest - cost[i]));
    return memo[i][rest] = ans;
}
```

表推版本：

```cpp
vector<vector<ll>> dp(n + 1, vector<ll>(W + 1, -LINF));
dp[0][W] = 0;
for (int i = 1; i <= n; i++) {
    for (int rest = 0; rest <= W; rest++) {
        dp[i][rest] = max(dp[i][rest], dp[i - 1][rest]);
        if (rest + cost[i] <= W && dp[i - 1][rest + cost[i]] != -LINF) {
            dp[i][rest] = max(dp[i][rest], dp[i - 1][rest + cost[i]] + val[i]);
        }
    }
}
cout << *max_element(dp[n].begin(), dp[n].end()) << '\n';
```

常见变体：

- 恰好选 `k` 个：状态加 `cnt`。
- 余数限制：状态加 `mod`。
- 上一个选择影响当前：状态加 `last`。

常见坑：

- DFS 里用了全局 `sum/path` 却没有放进状态，memo 会错。
- 终止条件没有检查“恰好”还是“至多”。
- 一维压缩时把同一元素重复选了。
- `rest` 为负后还访问数组。

暴力/部分分替代：

- `n <= 25`：DFS。
- `n <= 40`：折半枚举可拿更多分。
- 状态范围不清：`map<tuple<int,int,int>, ll>`。

升级方向：

- 选/不选 + 容量 -> 0/1 背包。
- 选/不选 + 集合关系 -> 状压 DP。
- 选/不选 + 前驱范围最优 -> DP + 数据结构。

最小测试样例：

```text
3 5
2 3
3 4
4 5
输出：7
```
