# DP-16：状压 DP

模型编号：DP-16

模型名称：状压 DP

标签：DP、集合、二进制、mask、TSP

一句话用途：当 `n` 很小且状态是“已选择/已访问集合”时，用二进制 `mask` 表示集合。

题面触发词：

- `n <= 20`
- “访问所有点”
- “每个点选或不选且集合状态重要”
- “钥匙/开关集合”
- “哈密顿路径/TSP”

什么时候用：

- 元素数量小。
- 需要知道哪些元素已经被选过/访问过。
- 状态由集合和最后位置等少量信息决定。

不要什么时候用：

- `n > 25` 通常不能直接 `2^n`。
- 不需要记集合，只需容量/数量时，用背包。
- 状态图边权非负且集合不是关键，可能是最短路。

复杂度：

- 常见 `O(2^n * n^2)`。
- 空间 `O(2^n * n)`。

数据范围信号：

- `n <= 20`：标准状压。
- `n <= 21/22`：不是默认模板可直接套的范围；必须重新估算内存、改 `KMAX/SMAX`，必要时压缩或折半。
- `n >= 25`：通常要剪枝、折半或其他模型。

依赖的标准容器：

- 逻辑点编号统一 `1..k`。
- 位运算用 `1 << (i - 1)` 表示第 `i` 个关键点。
- 上限明确时优先全局静态数组：`dist[KMAX+1][KMAX+1]`、`dp[SMAX][KMAX+1]`。

输入如何整理：

- 关键点编号保持 `1..k`，不要改成 0-index。
- `mask` 只是集合编码；第 `i` 个关键点对应第 `i-1` 位。
- 若原图有边，先算关键点之间距离。

1-index `Graph/Floyd` 到 1-index 关键点矩阵适配食谱：

```cpp
const int KMAX = 20;
const int SMAX = 1 << KMAX;
const int MAXN = 305;
ll all_dist[MAXN][MAXN]; // 按 Floyd/Dijkstra 预处理好的原图距离，原图点号 1..n
ll dist[KMAX + 1][KMAX + 1];
int key[KMAX + 1];

// G 是标准 1-index Graph，key[1..k] 是关键点在原图中的 1-index 点号。
for (int i = 1; i <= k; i++) {
    for (int j = 1; j <= k; j++) {
        dist[i][j] = all_dist[key[i]][key[j]];
    }
}
```

状压 DP 里的 `last/nxt` 全部用 `1..k` 的关键点编号；原图点号只留在 `key[i]` 里。若 `dist[i][j] == LINF`，表示两个关键点不可达，转移时跳过。

接口：

```cpp
ll tsp(int k, int start);
```

输出能力：

- 访问全部点的最小代价。
- 集合方案数。
- 最后停在某点的最优值。

下游可接：

- Floyd/Dijkstra：预处理关键点距离。
- BFS：网格钥匙状态。
- DP-03B 状态增维：只记 `mask` 不够时，加 `last` 表示当前位置。

可拼接模块：

- Floyd：全源最短路。
- Dijkstra：关键点间最短路。
- Bitset/位运算。

状态句式：

```text
dp[mask][last] 表示：已经访问的点集为 mask，并且当前最后停在 last 时的最小代价/最大收益。
last 是 1..k 的关键点编号；mask 的第 last-1 位表示 last 是否已访问。
```

为什么这个状态够用：访问过哪些点决定“以后还能去哪些点”，当前停在哪个点决定“下一步代价从哪里出发”。历史访问顺序本身不再影响未来，所以 `mask + last` 可以吸收全部关键历史。

初始化：

```text
dp[1 << (start - 1)][start] = 0：一开始只访问起点，代价为 0。
其他状态为 LINF/-LINF。
```

转移模板：

```cpp
nmask = mask | (1 << (nxt - 1));
dp[nmask][nxt] = min(dp[nmask][nxt], dp[mask][last] + dist[last][nxt]);
```

答案位置：

- 不要求回起点：`min dp[(1<<k)-1][last]`。
- 要求回起点：`min dp[full][last] + dist[last][start]`。

循环顺序：

- `mask` 从 0 到 `full`。
- 枚举 `last`。
- 枚举未访问 `nxt`。

暴力 DFS 版本：

```cpp
ll dfs(int mask, int last) {
    if (mask == full) return 0;
    ll ans = LINF;
    for (int nxt = 1; nxt <= k; nxt++) {
        if (mask >> (nxt - 1) & 1) continue;
        if (dist[last][nxt] == LINF) continue;
        ll sub = dfs(mask | (1 << (nxt - 1)), nxt);
        if (sub != LINF) ans = min(ans, dist[last][nxt] + sub);
    }
    return ans;
}
```

记忆化版本：

```cpp
ll memo[SMAX][KMAX + 1];
bool vis[SMAX][KMAX + 1];

ll dfs(int mask, int last) {
    if (mask == full) return 0;
    if (vis[mask][last]) return memo[mask][last];
    vis[mask][last] = 1;
    ll ans = LINF;
    for (int nxt = 1; nxt <= k; nxt++) {
        if (mask >> (nxt - 1) & 1) continue;
        if (dist[last][nxt] == LINF) continue;
        ll sub = dfs(mask | (1 << (nxt - 1)), nxt);
        if (sub != LINF) ans = min(ans, dist[last][nxt] + sub);
    }
    return memo[mask][last] = ans;
}
```

表推版本：

```cpp
ll dp[SMAX][KMAX + 1];

int total = 1 << k;
int full = total - 1;
for (int mask = 0; mask < total; mask++) {
    for (int i = 1; i <= k; i++) dp[mask][i] = LINF;
}
dp[1 << (start - 1)][start] = 0;

for (int mask = 0; mask < total; mask++) {
    for (int last = 1; last <= k; last++) {
        if (dp[mask][last] == LINF) continue;
        for (int nxt = 1; nxt <= k; nxt++) {
            if (mask >> (nxt - 1) & 1) continue;
            if (dist[last][nxt] == LINF) continue;
            int nmask = mask | (1 << (nxt - 1));
            dp[nmask][nxt] = min(dp[nmask][nxt], dp[mask][last] + dist[last][nxt]);
        }
    }
}

ll ans = LINF;
for (int last = 1; last <= k; last++) {
    if (dp[full][last] == LINF) continue;
    ans = min(ans, dp[full][last]); // 如果要求回到 start，再检查 dist[last][start] 后加上它
}
cout << ans << '\n';
```

常见变体：

- `dp[mask]`：不关心最后位置。
- 子集枚举：`for (sub = mask; sub; sub = (sub-1)&mask)`。
- 网格钥匙：BFS 状态 `(x,y,mask)`，不一定是表推 DP。

常见坑：

- `1 << n` 用 `int` 时 `n` 太大溢出；必要时用 `1LL << n`。
- 逻辑点编号保持 1-index；取位时统一写 `(i - 1)`，不要把关键点数组改成 0-index。
- `full` 变量在 DFS 前未初始化。
- 内存 `2^n * n` 爆掉。
- 只记 `mask` 但转移还需要知道当前停在哪个点时，必须写成 `dp[mask][last]`。

暴力/部分分替代：

- `n <= 10`：排列枚举。
- `n <= 20`：状压 DP。
- 图上访问关键点：先算关键点最短路，再状压。

升级方向：

- 暴力排列 -> DFS mask -> memo -> 表推。
- 与 Floyd/Dijkstra 拼接。
- 子集 DP 用子集枚举优化。
- 状态漏当前位置/钥匙/阶段时，回 DP-03B/DP-26 检查需要加哪一维。

最小测试样例：

```text
k=3 start=1
dist:
0 1 5
1 0 2
5 2 0
输出：3
说明：1 -> 2 -> 3。
```
