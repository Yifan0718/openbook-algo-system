# GRAPH-05 拓扑排序与 DAG DP

模块编号：GRAPH-05

模块名称：Topo、DAG DP

标签：[图论][拓扑排序][DAG][依赖顺序][DP]

一句话用途：有向无环图中先求合法顺序，再按拓扑序做路径计数、最长路、最短路或依赖 DP。

题面触发词：

- 依赖、先修、前置任务。
- 有向无环图、DAG。
- 必须先完成 A 才能完成 B。
- 问方案数、最长链、最早完成时间。

什么时候用：

- 图是有向图，且没有环。
- 转移依赖方向明确。
- DP 状态沿边传播，要求先算前驱再算后继。
- 需要判断是否存在环。

不要什么时候用：

- 无向图不能直接拓扑排序。
- 有向图有环时，普通 DAG DP 不成立。
- 边权有正负但要求一般最短路时，不要硬套 DAG DP，除非图确实无环。
- 树上 DP 用树 DFS 更直接。

复杂度：

- 拓扑排序：`O(n + m)`。
- DAG DP：通常 `O(n + m)`。

数据范围参考：

- `n,m <= 2e5` 常规可用。
- 方案数可能很大，按题目取模。

依赖的标准容器：

- `Graph`。
- Topo 只适用于 `G.add_directed(u, v)` 建出的有向边；无向边不能直接参与拓扑排序。
- Topo 入度建议从 `G.edges` 统计有向边。
- DP 转移从 `G.g[u]` 出发，并跳过非有向边。
- 依赖主骨架：`using ll = long long; const ll LINF = 4'000'000'000'000'000'000LL;`。

输入如何整理：

```cpp
Graph G(n);
for (int i = 1; i <= m; i++) {
    int u, v;
    cin >> u >> v;
    G.add_directed(u, v); // u 必须在 v 前
}
```

接口：

```text
vector<int> topo_sort(const Graph& G)
vector<ll> dag_count_paths(const Graph& G, int s, ll mod)
vector<ll> dag_longest_path(const Graph& G, int s)
```

输出能力：

- 一个拓扑序。
- 如果拓扑序长度小于 `n`，说明有环。
- DAG 上从源点出发的路径方案数或最长路。

下游可接：

- DAG DP。
- 任务排程。
- 最短路 DAG 计数。
- 依赖合法性判断。

可拼接模块：

- `Graph + Topo + DP`。
- `Dijkstra + ShortestPathDAG + Topo`。
- `Topo + Queue`。

模板代码：

```cpp
vector<int> topo_sort(const Graph &G) {
    for (auto e : G.edges) {
        if (!e.directed) return {};
    }
    vector<int> indeg(G.n + 1, 0);
    for (auto e : G.edges) {
        if (!e.directed) continue;
        indeg[e.to]++;
    }
    queue<int> q;
    for (int i = 1; i <= G.n; i++) {
        if (indeg[i] == 0) q.push(i);
    }
    vector<int> order;
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        order.push_back(u);
        for (auto e : G.g[u]) {
            if (!e.directed) continue;
            int v = e.to;
            indeg[v]--;
            if (indeg[v] == 0) q.push(v);
        }
    }
    return order;
}

vector<ll> dag_count_paths(const Graph &G, int s, ll mod) {
    auto order = topo_sort(G);
    if ((int)order.size() != G.n) return {};
    vector<ll> dp(G.n + 1, 0);
    dp[s] = 1;
    for (int u : order) {
        for (auto e : G.g[u]) {
            if (!e.directed) continue;
            int v = e.to;
            dp[v] = (dp[v] + dp[u]) % mod;
        }
    }
    return dp;
}

vector<ll> dag_longest_path(const Graph &G, int s) {
    auto order = topo_sort(G);
    if ((int)order.size() != G.n) return {};
    vector<ll> dp(G.n + 1, -LINF);
    dp[s] = 0;
    for (int u : order) {
        if (dp[u] == -LINF) continue;
        for (auto e : G.g[u]) {
            if (!e.directed) continue;
            int v = e.to;
            dp[v] = max(dp[v], dp[u] + e.w);
        }
    }
    return dp;
}
```

调用示例：

```cpp
auto order = topo_sort(G);
if ((int)order.size() < n) {
    cout << "cycle\n";
} else {
    auto ways = dag_count_paths(G, 1, 1000000007LL);
    cout << ways[n] << "\n";
}
```

常见坑：

- Topo 只对有向图有意义，标准 `Graph` 中必须用 `G.add_directed(u, v, w)` 建边。
- 建边方向要按“前置 -> 后继”，不要反。
- `order.size() < n` 表示有环，DAG DP 结果不可用。
- 本页两个 DAG DP 函数遇到有环会返回空数组，调用处要判断 `empty()`。
- 无向边放进 Topo 会让入度统计失真。
- 多源 DAG DP 可以把所有源点 `dp[s]=1`。
- 最长路初始化要用 `-LINF`，不可达不能参与转移。

暴力/部分分替代：

- `n <= 20` 可 DFS 枚举所有路径。
- 无权最长链小数据可记忆化 DFS。
- 只判断环，小数据可 DFS 三色标记。

升级方向：

- DFS 记忆化 DAG DP -> Topo 表推。
- 依赖顺序 + 资源限制可能升级为普通 DP/贪心。
- 最短路 DAG 计数：先 Dijkstra，再只保留满足 `dist[u]+w==dist[v]` 的边做 DP。

最小测试样例：

```text
4 4
1 2
1 3
2 4
3 4
Topo 可能为 1 2 3 4
从 1 到 4 路径数 = 2
```
