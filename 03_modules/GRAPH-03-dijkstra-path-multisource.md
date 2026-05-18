# GRAPH-03 Dijkstra、路径恢复、多源最短路

模块编号：GRAPH-03

模块名称：Dijkstra、路径恢复、多源最短路

标签：[图论][Dijkstra][非负权][路径恢复][多源最短路]

一句话用途：边权非负时求最短路，并可记录前驱恢复一条最短路径；多个起点时把所有源点一起入堆。

题面触发词：

- 边权非负、道路长度、花费、时间。
- 从一个点到其他点的最短距离。
- 从多个仓库/医院/起点出发到最近目标。
- 输出最短路径经过的点。

什么时候用：

- 边权 `w >= 0`。
- `n,m` 大，不能 Floyd。
- 单源或多源最短路。
- 需要恢复一条最短路径。

不要什么时候用：

- 有负权边，不能用 Dijkstra。
- `n <= 500` 且要求任意两点最短路，可用 Floyd。
- 边权全为 1 时 BFS 更简单。
- 要第 k 短路、动态最短路时，本模板不够。

复杂度：

- `O((n + m) log n)` 时间。
- `O(n + m)` 空间。

数据范围参考：

- `n,m <= 2e5` 常规可用。
- 距离可能很大，用 `ll`。

依赖的标准容器：

- `Graph`。
- 从 `G.g[u]` 遍历出边。
- `priority_queue`。
- 依赖主骨架：`using ll = long long; const ll LINF = 4'000'000'000'000'000'000LL;`。

输入如何整理：

```cpp
Graph G(n);
for (int i = 1; i <= m; i++) {
    int u, v;
    ll w;
    cin >> u >> v >> w;
    G.add_undirected(u, v, w); // 有向边改用 G.add_directed(u, v, w)
}
```

接口：

```text
vector<ll> dijkstra(const Graph& G, int s)
ShortestPathResult dijkstra_with_parent(const Graph& G, int s)
ShortestPathResult dijkstra_multi_source(const Graph& G, vector<int> sources)
vector<int> restore_path(pre, s, t)
```

输出能力：

- `dist[v]`：最短距离，不可达为 `LINF`。
- `pre[v]`：恢复路径用的前驱点。
- 多源版本中 `pre[source]=0`。

下游可接：

- 路径恢复。
- 最短路 DAG。
- 二分答案检查。
- 树上路径特判。

可拼接模块：

- `Graph + Dijkstra + restore_path`。
- `Graph + MultiSourceDijkstra`。
- `Dijkstra + DP`。

模板代码：

```cpp
struct ShortestPathResult {
    vector<ll> dist;
    vector<int> pre;
};

ShortestPathResult dijkstra_with_parent(const Graph &G, int s) {
    ShortestPathResult res;
    res.dist.assign(G.n + 1, LINF);
    res.pre.assign(G.n + 1, 0);
    priority_queue<pair<ll, int>, vector<pair<ll, int>>, greater<pair<ll, int>>> pq;
    res.dist[s] = 0;
    pq.push({0, s});
    while (!pq.empty()) {
        auto [du, u] = pq.top();
        pq.pop();
        if (du != res.dist[u]) continue;
        for (auto e : G.g[u]) {
            int v = e.to;
            ll w = e.w;
            if (res.dist[u] + w < res.dist[v]) {
                res.dist[v] = res.dist[u] + w;
                res.pre[v] = u;
                pq.push({res.dist[v], v});
            }
        }
    }
    return res;
}

vector<ll> dijkstra(const Graph &G, int s) {
    return dijkstra_with_parent(G, s).dist;
}

ShortestPathResult dijkstra_multi_source(const Graph &G, const vector<int> &sources) {
    ShortestPathResult res;
    res.dist.assign(G.n + 1, LINF);
    res.pre.assign(G.n + 1, 0);
    priority_queue<pair<ll, int>, vector<pair<ll, int>>, greater<pair<ll, int>>> pq;
    for (int s : sources) {
        if (s < 1 || s > G.n) continue;
        if (res.dist[s] == 0) continue;
        res.dist[s] = 0;
        pq.push({0, s});
    }
    while (!pq.empty()) {
        auto [du, u] = pq.top();
        pq.pop();
        if (du != res.dist[u]) continue;
        for (auto e : G.g[u]) {
            int v = e.to;
            ll w = e.w;
            if (res.dist[u] + w < res.dist[v]) {
                res.dist[v] = res.dist[u] + w;
                res.pre[v] = u;
                pq.push({res.dist[v], v});
            }
        }
    }
    return res;
}

vector<int> restore_path(const vector<int> &pre, int s, int t) {
    vector<int> path;
    for (int cur = t; cur != 0; cur = pre[cur]) {
        path.push_back(cur);
        if (cur == s) break;
    }
    if (path.empty() || path.back() != s) return {};
    reverse(path.begin(), path.end());
    return path;
}
```

调用示例：

```cpp
auto res = dijkstra_with_parent(G, s);
if (res.dist[t] == LINF) {
    cout << "-1\n";
} else {
    cout << res.dist[t] << "\n";
    auto path = restore_path(res.pre, s, t);
}

vector<int> sources = {1, 5, 9};
auto multi = dijkstra_multi_source(G, sources);
```

常见坑：

- 有负权边时会错。
- `LINF + w` 可能溢出，只有从堆中弹出的可达点才松弛。
- 堆里旧状态要用 `du != dist[u]` 跳过。
- 无向图用 `G.add_undirected(...)`；有向图用 `G.add_directed(...)`。
- 多源最短路不是跑多次 Dijkstra，而是所有源点距离设 0 后一起入堆。
- `restore_path` 只能恢复到起点可达的目标。

暴力/部分分替代：

- `n <= 500` 可用 Floyd。
- `m` 很小、点很少可用 Bellman-Ford。
- 边权全为 1 时用 BFS。

升级方向：

- 需要多次任意两点查询：小图 Floyd；大图通常要换模型。
- 需要方案数：在 Dijkstra 松弛时维护 `cnt[v]`。
- 需要路径限制：可能变成状态最短路，把状态拆成点。

最小测试样例：

```text
4 4
1 2 5
1 3 1
3 2 1
2 4 2
s=1
dist[4]=4
path: 1 3 2 4
```
