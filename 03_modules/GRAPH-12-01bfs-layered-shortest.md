# GRAPH-12 0-1 BFS 与分层图最短路

模块编号：GRAPH-12

模块名称：0-1 BFS、分层图、带次数限制的状态最短路

标签：[图论][最短路][0-1 BFS][分层图][状态图][deque]

一句话用途：边权只有 `0/1` 时用 deque 代替 Dijkstra；题目有“最多用 k 次免费/折扣/跳过/特殊能力”时，把 `次数 used` 加进状态做分层最短路。

题面触发词：

- 边权只有 `0` 或 `1`。
- “免费通过最多 k 次”“最多改 k 条边”“最多跳过 k 次费用”。
- “状态里除了点编号，还要记住用了几次机会”。
- 网格或图上求最小代价，但代价不是普通单一顶点。

什么时候用：

- 0-1 BFS：所有边权都在 `{0,1}`。
- 分层图：到达同一个点时，“已经使用几次机会”会影响未来。
- 普通 `dist[u]` 不够，必须用 `dist[used][u]`。

不要什么时候用：

- 边权不是 `0/1`，且有一般非负权，优先 Dijkstra。
- 有负权边，转 Bellman-Ford/SPFA。
- 状态维度很多且 `n * 状态数` 爆内存时，不要硬开二维数组。
- 只是无权最少步数，普通 BFS 更简单。

复杂度：

- 0-1 BFS：`O(n + m)`。
- 分层图若每层边仍是 `0/1` 且用 deque：`O((k+1) * (n+m))`。
- 分层图若有一般非负权且用 priority_queue：`O((k+1) * (n+m) * log((k+1)*n))`。

数据范围参考：

- `n,m <= 2e5` 且 `k <= 20/50` 常见可做。
- 如果 `k` 接近 `n`，先估算 `(k+1)*(n+1)` 是否会爆内存。

依赖的标准容器：

- 标准 `Graph`。
- `deque<int>`。
- `static ll layer_dist[LAYER_MAXK][LAYER_MAXN]`，点号仍是 `1..n`，名字加前缀避免和其他模块的 `MAXN/MAXK` 冲突。
- 依赖主骨架：`using ll = long long; const ll LINF = 4'000'000'000'000'000'000LL;`。

输入如何整理：

```cpp
Graph G(n);
for (int i = 1; i <= m; i++) {
    int u, v;
    ll w;
    cin >> u >> v >> w; // w 必须是 0 或 1 才能 0-1 BFS
    G.add_undirected(u, v, w);
}
```

接口：

```cpp
vector<ll> zero_one_bfs(const Graph& G, int s);
bool shortest_with_free_passes(const Graph& G, int s, int k);
```

输出能力：

- `dist[v]`：0-1 权图从 `s` 到 `v` 的最短路。
- `dist[used][v]`：从 `s` 到 `v`，已经使用 `used` 次特殊机会时的最小代价。
- 最终答案通常是 `min(dist[0..k][t])`。

下游可接：

- 状态 BFS。
- Dijkstra。
- DP-03B 状态增维：`used` 是典型“后效性吸收到状态里”的维度。

可拼接模块：

- `Graph + 0-1 BFS`。
- `Graph + dist[used][u] + Dijkstra/0-1 BFS`。
- `GridState + used`。

模板代码：

```cpp
vector<ll> zero_one_bfs(const Graph &G, int s) {
    vector<ll> dist(G.n + 1, LINF);
    deque<int> dq;
    dist[s] = 0;
    dq.push_front(s);

    while (!dq.empty()) {
        int u = dq.front();
        dq.pop_front();
        for (auto e : G.g[u]) {
            int v = e.to;
            ll w = e.w;
            assert(w == 0 || w == 1);
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                if (w == 0) dq.push_front(v);
                else dq.push_back(v);
            }
        }
    }
    return dist;
}

const int LAYER_MAXN = 200000 + 5;
const int LAYER_MAXK = 55;
static ll layer_dist[LAYER_MAXK][LAYER_MAXN];

bool shortest_with_free_passes(const Graph &G, int s, int k) {
    if (k < 0 || k >= LAYER_MAXK || G.n <= 0 || G.n >= LAYER_MAXN) return false;
    for (int used = 0; used <= k; used++) {
        for (int v = 1; v <= G.n; v++) {
            layer_dist[used][v] = LINF;
        }
    }
    priority_queue<tuple<ll, int, int>, vector<tuple<ll, int, int>>, greater<tuple<ll, int, int>>> pq;

    layer_dist[0][s] = 0;
    pq.push({0, 0, s}); // cost, used, node

    while (!pq.empty()) {
        auto [d, used, u] = pq.top();
        pq.pop();
        if (d != layer_dist[used][u]) continue;

        for (auto e : G.g[u]) {
            int v = e.to;
            ll w = e.w;

            if (d + w < layer_dist[used][v]) {
                layer_dist[used][v] = d + w;
                pq.push({layer_dist[used][v], used, v});
            }

            if (used < k && d < layer_dist[used + 1][v]) {
                layer_dist[used + 1][v] = d; // 免费走这条边
                pq.push({layer_dist[used + 1][v], used + 1, v});
            }
        }
    }
    return true;
}
```

调用示例：

```cpp
auto dist01 = zero_one_bfs(G, 1);
cout << (dist01[n] == LINF ? -1 : dist01[n]) << '\n';

int k = 2;
if (!shortest_with_free_passes(G, 1, k)) {
    cout << "-1\n";
    return;
}
ll ans = LINF;
for (int used = 0; used <= k; used++) ans = min(ans, layer_dist[used][n]);
cout << (ans == LINF ? -1 : ans) << '\n';
```

常见坑：

- 0-1 BFS 只能处理边权 `0/1`，不是“小整数 BFS”。
- 0 权边要 `push_front`，1 权边要 `push_back`。
- 分层图答案常常是 `min(dist[used][t])`，不是只看 `dist[k][t]`。
- `dist[used][u]` 中 `used` 必须表示已经用了多少次机会，含义不要混。
- 有向图要用 `add_directed`，无向图要用 `add_undirected`。
- `k*n` 太大时，改用 `unordered_map` 稀疏记忆化可能拿部分分。

暴力/部分分替代：

- `n <= 20`：DFS 枚举是否使用免费机会，记录最小值。
- `k = 0`：直接普通 Dijkstra。
- 边权全 1：普通 BFS。
- 小图任意两点：Floyd 后再做简单枚举。

升级方向：

- 普通 BFS -> 0-1 BFS -> Dijkstra。
- `dist[u]` 不够 -> `dist[used][u]`。
- 网格带钥匙/体力/次数 -> `dist[x][y][state]`。

最小测试样例：

```text
分层 Dijkstra / 免费一次样例：
3 3
1 2 1
2 3 1
1 3 5
k=1
免费一次后可直接免费走 1->3，最小代价是 0
```
