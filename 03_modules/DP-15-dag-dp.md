# DP-15：DAG DP

模型编号：DP-15

模型名称：DAG DP

标签：DP、拓扑排序、有向无环图、路径计数、依赖关系

一句话用途：在有向无环图上按拓扑序转移，求路径最优值、方案数或依赖完成方式。

题面触发词：

- “有向无环图”
- “依赖关系”
- “先修课程”
- “任务 A 必须在 B 前”
- “从起点到终点的路径数/最长路”

什么时候用：

- 状态之间是有向依赖且无环。
- 可以拓扑排序。
- `dp[u]` 能由前驱或后继转移。

不要什么时候用：

- 图有环，普通 DAG DP 不适用。
- 边权非负最短路在一般图上，转 Dijkstra。
- 无权最少步数，转 BFS。

复杂度：

- 拓扑排序 `O(n+m)`。
- DP 转移 `O(n+m)`。

数据范围信号：

- `n,m <= 2e5`：DAG DP 很适合。
- 若 `n <= 20` 且集合访问，可能是状压。

依赖的标准容器：

- 标准 `Graph G`。
- 本页后续 `vector<vector<pair<int,ll>>> g` 是速抄变体；与图论卷拼接时优先使用 `G.g[u]` 中的 `e.to/e.w`。
- `vector<int> indeg, topo`
- `queue<int>`
- `vector<ll> dp`

输入如何整理：

- 建有向边 `u -> v`。
- 统计入度。
- 如果题意是“u 依赖 v”，先确认边方向。

接口：

```cpp
vector<int> topo_sort(const Graph& G);
```

输出能力：

- 到达每点的最长/最短路径。
- 路径方案数。
- 依赖完成最早时间。

下游可接：

- Graph 标准建图。
- Topo 模块。

可拼接模块：

- Graph。
- 拓扑排序。
- 取模计数。

状态句式：

```text
dp[u] 表示：到达 u 的最优值/方案数。
```

为什么这个状态够用：DAG 的拓扑序保证所有影响 `u` 的前驱都已经处理完；未来只需要知道“到达 u 的当前最优/方案数”，不需要知道具体路径历史。

也可反向：

```text
dp[u] 表示：从 u 出发到终点的最优值/方案数。
```

初始化：

```text
起点 s：dp[s] = 0/1。
最大值题其他点为 -LINF；最小值题为 LINF；方案数为 0。
```

转移模板：

```cpp
for (auto e : G.g[u]) {
    int v = e.to;
    ll w = e.w;
    dp[v] = max(dp[v], dp[u] + w);
}
```

速抄局部 `g` 变体：

```cpp
for (auto [v, w] : g[u]) {
    dp[v] = max(dp[v], dp[u] + w);
}
```

方案数：

```cpp
ways[v] = (ways[v] + ways[u]) % MOD;
```

答案位置：

- 指定终点：`dp[t]`。
- 任意终点：`max/min dp[u]`。
- 路径总数：通常 `ways[t]`。

循环顺序：

- 先拓扑排序。
- 按拓扑序从前往后转移。
- 反向定义时按逆拓扑序。

暴力 DFS 版本：

```cpp
ll dfs(int u) {
    if (u == t) return 0;
    ll ans = -LINF;
    for (auto [v, w] : g[u]) {
        ll sub = dfs(v);
        if (sub != -LINF) ans = max(ans, w + sub);
    }
    return ans;
}
```

记忆化版本：

```cpp
vector<ll> memo;
vector<int> vis;

ll dfs(int u) {
    if (u == t) return 0;
    if (vis[u]) return memo[u];
    vis[u] = 1;
    ll ans = -LINF;
    for (auto [v, w] : g[u]) {
        ll sub = dfs(v);
        if (sub != -LINF) ans = max(ans, w + sub);
    }
    return memo[u] = ans;
}
```

表推版本：

```cpp
queue<int> q;
for (int i = 1; i <= n; i++) if (indeg[i] == 0) q.push(i);
vector<int> topo;
while (!q.empty()) {
    int u = q.front(); q.pop();
    topo.push_back(u);
    for (auto [v, w] : g[u]) {
        if (--indeg[v] == 0) q.push(v);
    }
}
if ((int)topo.size() != n) {
    // 有环时普通 DAG DP 不适用；按题意输出无解，或重新路由到图算法。
    return;
}

vector<ll> dp(n + 1, -LINF);
dp[s] = 0;
for (int u : topo) {
    if (dp[u] == -LINF) continue;
    for (auto [v, w] : g[u]) dp[v] = max(dp[v], dp[u] + w);
}
cout << dp[t] << '\n';
```

常见变体：

- 最短路 DAG：`min` 转移，初值 `LINF`。
- 路径计数：`ways[s]=1`。
- 任务最早完成时间：边/点权表示耗时。

常见坑：

- 图有环但仍递归，导致死循环。
- 边方向建反。
- 多个入度 0 起点没有初始化。
- 修改 `indeg` 后还要复用原入度，需备份。

暴力/部分分替代：

- 小图 DFS 枚举路径。
- 无环但顺序不清：记忆化 DFS。
- 大图：拓扑表推。

升级方向：

- DFS memo -> 拓扑 DP。
- 与 Graph 标准容器统一。
- 若有环且问最长路，通常不是普通 DP，要重新路由。

最小测试样例：

```text
4 4
1 2 3
1 3 2
2 4 4
3 4 5
s=1 t=4
输出：7
```
