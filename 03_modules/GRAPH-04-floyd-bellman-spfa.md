# GRAPH-04 Floyd、Bellman-Ford 与 SPFA

模块编号：GRAPH-04

模块名称：Floyd、Bellman-Ford、SPFA

标签：[图论][全源最短路][负权边][负环][Floyd][Bellman-Ford][SPFA]

一句话用途：小图用 Floyd 求任意两点最短路；有负权边时用 Bellman-Ford 或 SPFA，并能判断负环风险。

题面触发词：

- 任意两点最短路、多次问 `u` 到 `v`。
- `n <= 300/500`。
- 边权可能为负。
- 判断是否存在负环。

什么时候用：

- Floyd：点数小，需要全源最短路。
- Bellman-Ford：有负权边，单源最短路，且想稳妥判断负环。
- SPFA：有负权边且图比较稀疏时可尝试，但不能保证最坏复杂度。

不要什么时候用：

- `n` 很大时不要 Floyd。
- 非负权大图优先 Dijkstra。
- 边权全为 1 优先 BFS。
- 有负环且题目要求最短距离时，要先判断“最短路是否不存在”。

复杂度：

- Floyd：`O(n^3)` 时间，`O(n^2)` 空间。
- Bellman-Ford：`O(nm)` 时间，`O(n)` 空间。
- SPFA：平均可能较快，最坏 `O(nm)`。

数据范围参考：

- Floyd：`n <= 300/500`。
- Bellman-Ford：`n*m` 能过时使用。
- SPFA：竞赛中要谨慎，能 Dijkstra 就别 SPFA。

依赖的标准容器：

- `Graph`。
- Floyd 和 Bellman-Ford 主要遍历 `G.edges`。
- SPFA 遍历 `G.g[u]`。
- 依赖主骨架：`using ll = long long; const ll LINF = 4'000'000'000'000'000'000LL;`。

输入如何整理：

```cpp
Graph G(n);
for (int i = 1; i <= m; i++) {
    int u, v;
    ll w;
    cin >> u >> v >> w;
    G.add_directed(u, v, w); // 无向边改用 G.add_undirected(u, v, w)
}
```

接口：

```text
void floyd(const Graph& G)
全局 floyd_dist[u][v]
BellmanResult bellman_ford(const Graph& G, int s)
BellmanResult spfa(const Graph& G, int s)
```

输出能力：

- Floyd：`dist[u][v]` 任意两点最短路。
- Bellman-Ford/SPFA：`dist[v]`，以及是否检测到从源点可达的负环。

下游可接：

- 全源距离矩阵可接状压 DP。
- 负环判断可接可行性输出。
- 单源负权最短路可接路径类题。

可拼接模块：

- `Graph.edges + Floyd`。
- `Graph.edges + Bellman-Ford`。
- `Graph.g + SPFA`。
- `Floyd + BitmaskDP`。

模板代码：

```cpp
struct BellmanResult {
    vector<ll> dist;
    bool has_negative_cycle = false;
};

const int MAXF = 505; // Floyd 一般只给小图用，按题目 n 上限改
static ll floyd_dist[MAXF][MAXF];

void floyd(const Graph &G) {
    assert(G.n > 0 && G.n < MAXF);
    for (int i = 1; i <= G.n; i++) {
        for (int j = 1; j <= G.n; j++) {
            floyd_dist[i][j] = (i == j ? 0 : LINF);
        }
    }
    for (auto e : G.edges) {
        floyd_dist[e.from][e.to] = min(floyd_dist[e.from][e.to], e.w);
        if (!e.directed) floyd_dist[e.to][e.from] = min(floyd_dist[e.to][e.from], e.w);
    }
    for (int k = 1; k <= G.n; k++) {
        for (int i = 1; i <= G.n; i++) {
            if (floyd_dist[i][k] == LINF) continue;
            for (int j = 1; j <= G.n; j++) {
                if (floyd_dist[k][j] == LINF) continue;
                floyd_dist[i][j] = min(floyd_dist[i][j], floyd_dist[i][k] + floyd_dist[k][j]);
            }
        }
    }
}

BellmanResult bellman_ford(const Graph &G, int s) {
    BellmanResult res;
    res.dist.assign(G.n + 1, LINF);
    res.dist[s] = 0;
    for (int i = 1; i <= G.n - 1; i++) {
        bool changed = false;
        for (auto e : G.edges) {
            if (res.dist[e.from] != LINF && res.dist[e.from] + e.w < res.dist[e.to]) {
                res.dist[e.to] = res.dist[e.from] + e.w;
                changed = true;
            }
            if (!e.directed && res.dist[e.to] != LINF && res.dist[e.to] + e.w < res.dist[e.from]) {
                res.dist[e.from] = res.dist[e.to] + e.w;
                changed = true;
            }
        }
        if (!changed) break;
    }
    for (auto e : G.edges) {
        if (res.dist[e.from] != LINF && res.dist[e.from] + e.w < res.dist[e.to]) {
            res.has_negative_cycle = true;
        }
        if (!e.directed && res.dist[e.to] != LINF && res.dist[e.to] + e.w < res.dist[e.from]) {
            res.has_negative_cycle = true;
        }
    }
    return res;
}

BellmanResult spfa(const Graph &G, int s) {
    BellmanResult res;
    res.dist.assign(G.n + 1, LINF);
    vector<int> inq(G.n + 1, 0), cnt(G.n + 1, 0);
    queue<int> q;
    res.dist[s] = 0;
    q.push(s);
    inq[s] = 1;
    cnt[s] = 1;
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        inq[u] = 0;
        for (auto e : G.g[u]) {
            int v = e.to;
            ll w = e.w;
            if (res.dist[u] + w >= res.dist[v]) continue;
            res.dist[v] = res.dist[u] + w;
            if (!inq[v]) {
                q.push(v);
                inq[v] = 1;
                cnt[v]++;
                if (cnt[v] > G.n) {
                    res.has_negative_cycle = true;
                    return res;
                }
            }
        }
    }
    return res;
}
```

调用示例：

```cpp
floyd(G);
cout << (floyd_dist[u][v] == LINF ? -1 : floyd_dist[u][v]) << "\n";

auto res = bellman_ford(G, s);
if (res.has_negative_cycle) cout << "NEGATIVE CYCLE\n";
```

常见坑：

- Floyd 初始化要处理重边取最小。
- Floyd 中 `LINF` 不能直接相加，先判断可达。
- Bellman-Ford 无向负边等价于负环风险，题目一般不会这样给最短路正解。
- Bellman-Ford 对无向边要松弛两个方向。
- SPFA 可能被卡，不是万能加速版。
- 负环判断通常只判断“从源点可达”的负环。

暴力/部分分替代：

- 小图任意两点可 Floyd。
- 没负边时用 Dijkstra。
- `n <= 50` 可直接矩阵松弛。

升级方向：

- 大图非负权：换 Dijkstra。
- 任意两点 + 必经若干点：Floyd 后接状压 DP。
- 需要路径恢复：Floyd 维护 `nxt` 或 Bellman-Ford 维护 `pre`。

最小测试样例：

```text
3 3
1 2 4
1 3 10
2 3 -2
Bellman-Ford from 1: dist[3]=2
Floyd: dist[1][3]=2
```
