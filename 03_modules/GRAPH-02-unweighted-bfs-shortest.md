# GRAPH-02 无权最短路 BFS

模块编号：GRAPH-02

模块名称：无权图最短路 BFS

标签：[图论][BFS][无权最短路][最少步数]

一句话用途：在每条边代价都一样时，用 BFS 求从起点到所有点的最少边数。

题面触发词：

- 最少经过几条边。
- 最少操作次数。
- 每次移动代价相同。
- 无权图、边权全为 1。

什么时候用：

- 所有边权都是 1。
- 网格每步上下左右代价相同。
- 状态图每次操作代价相同。
- 需要最短步数和父节点恢复路径。

不要什么时候用：

- 边权不是全相等时不要用普通 BFS。
- 边权非负但有不同值，用 Dijkstra。
- 有负权边，用 Bellman-Ford/SPFA。
- 只判断连通性，不要多维护距离也可以。

复杂度：

- `O(n + m)` 时间。
- `O(n)` 空间。

数据范围参考：

- `n,m <= 2e5` 或更大都可。
- 网格 BFS 复杂度约 `O(n*m)`。

依赖的标准容器：

- `Graph`。
- 从 `G.g[u]` 遍历邻接点。

输入如何整理：

```cpp
Graph G(n);
for (int i = 1; i <= m; i++) {
    int u, v;
    cin >> u >> v;
    G.add_undirected(u, v); // 无向无权
}
```

接口：

```text
vector<int> bfs_unweighted(const Graph& G, int s)
vector<int> multi_source_bfs(const Graph& G, const vector<int>& sources)
BfsResult bfs_with_parent(const Graph& G, int s)
```

输出能力：

- `dist[v]`：从 `s` 到 `v` 的最少边数，不可达为 `-1`。
- `pre[v]`：最短路树中的前驱，可接路径恢复。

下游可接：

- 路径恢复。
- 分层图 DP。
- 二分图染色。
- 多源 BFS。

可拼接模块：

- `Graph + BFS + restore_path`。
- `Graph + BFS + MultiSource`。
- `Grid + BFS`。

模板代码：

```cpp
struct BfsResult {
    vector<int> dist;
    vector<int> pre;
};

vector<int> bfs_unweighted(const Graph &G, int s) {
    vector<int> dist(G.n + 1, -1);
    queue<int> q;
    dist[s] = 0;
    q.push(s);
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        for (auto e : G.g[u]) {
            int v = e.to;
            if (dist[v] != -1) continue;
            dist[v] = dist[u] + 1;
            q.push(v);
        }
    }
    return dist;
}

BfsResult bfs_with_parent(const Graph &G, int s) {
    BfsResult res;
    res.dist.assign(G.n + 1, -1);
    res.pre.assign(G.n + 1, 0);
    queue<int> q;
    res.dist[s] = 0;
    q.push(s);
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        for (auto e : G.g[u]) {
            int v = e.to;
            if (res.dist[v] != -1) continue;
            res.dist[v] = res.dist[u] + 1;
            res.pre[v] = u;
            q.push(v);
        }
    }
    return res;
}

vector<int> multi_source_bfs(const Graph &G, const vector<int> &sources) {
    vector<int> dist(G.n + 1, -1);
    queue<int> q;
    for (int s : sources) {
        if (s < 1 || s > G.n) continue;
        if (dist[s] != -1) continue;
        dist[s] = 0;
        q.push(s);
    }
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        for (auto e : G.g[u]) {
            int v = e.to;
            if (dist[v] != -1) continue;
            dist[v] = dist[u] + 1;
            q.push(v);
        }
    }
    return dist;
}
```

调用示例：

```cpp
auto res = bfs_with_parent(G, s);
cout << res.dist[t] << "\n";

vector<int> sources = {1, 5, 9};
auto dist_nearest_source = multi_source_bfs(G, sources);
```

常见坑：

- BFS 只适合边权相同的最短路。
- 不可达点 `dist=-1`，输出前按题意处理。
- 有向无权图用 `G.add_directed(...)` 建边；无向无权图用 `G.add_undirected(...)`。
- 如果要路径，第一次到达时记录 `pre[v]=u`。
- 网格 BFS 不一定要转 Graph，直接二维数组更短。

暴力/部分分替代：

- `n <= 20` 可以 DFS 枚举简单路径取最短，但容易指数爆炸。
- `n <= 500` 可用 Floyd 求全源，但无权单源 BFS 更优。

升级方向：

- 边权变成非负数：Dijkstra。
- 多个起点：多源 BFS。
- 需要输出路径：接 `restore_path`。

最小测试样例：

```text
4 3
1 2
2 3
1 4
s=1
dist[1]=0 dist[2]=1 dist[3]=2 dist[4]=1
```
