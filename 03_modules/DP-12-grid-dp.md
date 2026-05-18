# DP-12：网格 DP

模型编号：DP-12

模型名称：网格 DP

标签：DP、网格、路径数、最小路径和

一句话用途：在二维网格中按固定方向移动，求路径数、最大收益或最小代价。

题面触发词：

- “从左上角到右下角”
- “只能向右/向下”
- “网格路径数量”
- “障碍物”
- “最小路径和/最大金币”

什么时候用：

- 移动方向保证无环，例如只向右、向下、右下。
- 到达一个格子的答案只依赖前面方向的格子。

不要什么时候用：

- 可以上下左右任意走且求最短步数，优先 BFS。
- 网格有权最短路且可回头，可能是 Dijkstra。
- 状态还包含钥匙/访问集合，可能要 BFS 或状压。

复杂度：

- 常见 `O(nm)`。
- 空间 `O(nm)`，可滚动成 `O(m)`。

数据范围信号：

- `n*m <= 1e7` 左右可尝试。
- 网格特别大但障碍少，可能要组合数学或压缩。

依赖的标准容器：

- 上限明确时用 `static ll a[MAXN][MAXM] / dp[MAXN][MAXM]`
- 字符网格可用 `vector<string> grid(n+1)` 且每行前面补一个空格，保持 `grid[i][j]`

输入如何整理：

- 网格坐标统一 `1..n, 1..m`。
- 障碍格用 `blocked[i][j]` 或字符 `'#'`。

接口：

```cpp
ll grid_dp(int n, int m);
```

输出能力：

- 路径数。
- 最小路径和。
- 最大收益。

下游可接：

- BFS 状态搜索。
- 状压钥匙/访问状态。
- DP-03B/DP-26 状态升维：上一步方向、是否用过机会等会影响未来时使用。

可拼接模块：

- PrefixSum：快速计算矩形/路径段贡献。
- BFS：方向不受限时替代。

状态句式：

```text
dp[i][j] 表示：走到格子 (i,j) 时的方案数/最小代价/最大收益。
```

初始化：

```text
dp[1][1] = 起点贡献或 1。
障碍格不转移。
最小值题其他状态为 LINF；最大值题其他状态为 -LINF；计数题为 0。
```

转移模板：

```cpp
dp[i][j] = merge(dp[i - 1][j], dp[i][j - 1]) + cost[i][j];
```

计数：

```cpp
dp[i][j] = dp[i - 1][j] + dp[i][j - 1];
```

答案位置：

- 通常 `dp[n][m]`。
- 终点不固定时取边界或全表最优。

循环顺序：

- `i` 从 1 到 `n`。
- `j` 从 1 到 `m`。
- 因为只依赖上方和左方。

暴力 DFS 版本：

```cpp
ll dfs(int i, int j) {
    if (i > n || j > m || blocked[i][j]) return 0;
    if (i == n && j == m) return 1;
    return dfs(i + 1, j) + dfs(i, j + 1);
}
```

记忆化版本：

```cpp
const int MAXN = 1000 + 5;
const int MAXM = 1000 + 5;
static ll memo[MAXN][MAXM];
static char vis[MAXN][MAXM];
static bool blocked[MAXN][MAXM];

ll dfs(int i, int j) {
    if (i > n || j > m || blocked[i][j]) return 0;
    if (i == n && j == m) return 1;
    if (vis[i][j]) return memo[i][j];
    vis[i][j] = 1;
    return memo[i][j] = dfs(i + 1, j) + dfs(i, j + 1);
}
```

表推版本：

```cpp
static ll dp[MAXN][MAXM];
for (int i = 0; i <= n; i++) {
    for (int j = 0; j <= m; j++) dp[i][j] = 0;
}
if (!blocked[1][1]) dp[1][1] = 1;
for (int i = 1; i <= n; i++) {
    for (int j = 1; j <= m; j++) {
        if (blocked[i][j] || (i == 1 && j == 1)) continue;
        dp[i][j] = dp[i - 1][j] + dp[i][j - 1];
    }
}
cout << dp[n][m] << '\n';
```

最小路径和版本：

下面是无障碍版；若有障碍格，在循环里先 `if (blocked[i][j]) continue;`，并且起点/终点障碍要特判无解。

```cpp
static ll dp[MAXN][MAXM];
for (int i = 0; i <= n; i++) {
    for (int j = 0; j <= m; j++) dp[i][j] = LINF;
}
dp[1][1] = a[1][1];
for (int i = 1; i <= n; i++) {
    for (int j = 1; j <= m; j++) {
        if (i == 1 && j == 1) continue;
        ll best = min(dp[i - 1][j], dp[i][j - 1]);
        if (best != LINF) dp[i][j] = best + a[i][j];
    }
}
```

常见变体：

- 允许三方向：多加一个前驱。
- 有障碍：障碍格跳过。
- 路径取模计数：每次加法取模。
- 上一步方向影响下一步：状态升成 `dp[i][j][lastMove]`。
- 最多使用一次技能/翻倍：状态升成 `dp[i][j][used]`。

常见坑：

- 第一行第一列初始化错误。
- 起点或终点是障碍没有特判。
- 允许回头时仍套普通网格 DP。
- 最小值题 `LINF + cost` 溢出，转移前判断可达。

暴力/部分分替代：

- 小网格 DFS。
- 中等网格记忆化。
- 无环方向明确后改表推。

升级方向：

- 二维 -> 滚动数组。
- 加状态：`dp[i][j][k]` 表示还剩/已用资源。
- 可自由移动 -> BFS/Dijkstra。
- 发现 `dp[i][j]` 有后效性 -> DP-26 例题卡。

最小测试样例：

```text
2 3
...
...
输出：3
```
