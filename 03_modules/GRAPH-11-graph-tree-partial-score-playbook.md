# GRAPH-11：图/树部分分作战表

模块编号：GRAPH-11

模块名称：图/树部分分作战表

标签：图论、树、部分分、暴力、BFS、Floyd、LCA、状态搜索

一句话用途：图/树题不会正解时，按 V0 到 V5 逐步写，至少拿小数据、特殊性质和合法输出分。

题面触发词：

- 图、树、连通、最短路、生成树、LCA、子树、路径。
- 数据有多个子任务或特殊性质。
- 每题多次提交取最高分。

什么时候用：

- 图/树正解一时想不出。
- 想先写一个稳定小数据版本。
- 题面存在 `n <= 20/200/2000`、链、星、边权全 1、树等特殊条件。

不要什么时候用：

- 已经能明确套 BFS/Dijkstra/Kruskal/LCA/树 DP 时，直接写正解。
- 输出必须严格最优且无部分分时，不要停在兜底版本。

复杂度：

- V0/V1：`O(n+m)` 或只读入输出。
- V2：Floyd `O(n^3)`，每问 DFS/BFS `O(n+m)`。
- V3：枚举点/边集常见 `O(2^n)` 或 `O(2^m)`，只适合小数据。
- V4：树上每问 DFS `O(nq)`，暴力 LCA `O(nq)` 最坏。
- V5：正解模块复杂度见各模块。

数据范围信号：

- `n <= 20`：枚举点集/边集。
- `n <= 200`：Floyd、小图邻接矩阵。
- `n,q <= 2000`：每问 DFS/BFS、暴力 LCA。
- `m = n - 1`：优先判断是否是树。
- 边权全 1：BFS 替代 Dijkstra。

依赖的标准容器：

- `Graph`
- `DSU`
- `queue`
- `vector<vector<int>>`

输入如何整理：

- 统一先读成 `Graph G`。
- 记录特殊性质：`is_tree`、`all_weight_one`、`all_directed`、`n_small`。
- 树题优先构造 `TreeInfo`。

接口：

```text
V0 合法兜底 -> V1 特判 -> V2 小图精确 -> V3 枚举 -> V4 树暴力 -> V5 正解
```

输出能力：

- 合法输出。
- 小数据精确解。
- 特殊性质精确解。
- 正解升级路线。

下游可接：

- GRAPH-01/02/03/04/05/06/09/10。
- TREE-01。
- DP-14/15。
- BRUTE-11 状态 BFS。

可拼接模块：

- Floyd：小图最短路。
- DSU：连通性/MST/生成树检查。
- BFS/DFS：连通、最短步数、树上路径。
- TreeInfo：树上父亲/深度/DFS 序。

## V0：读入完整 + 合法兜底

先保证：

```text
1. 输入全部读完。
2. 输出格式合法。
3. n=1、m=0、q=0 不 RE。
4. 不输出越界点号或不存在边号。
```

常见兜底：

| 题型 | 兜底 |
|---|---|
| 判断连通 | 无边且 `n>1` 输出 No，`n=1` 输出 Yes |
| 最短路 | 不会时至少不可达输出 `-1`，不要乱输出路径 |
| 构造路径 | 若 `s==t`，输出长度 0 或单点路径 |
| 输出边集 | 空边集是否允许先看题面，不允许就输出合法失败标志 |
| 树题 | `n==1` 单独处理 |

## V1：特殊性质特判

```cpp
bool all_weight_one = true;
bool maybe_tree = ((int)G.edges.size() == G.n - 1);
for (auto e : G.edges) {
    if (e.w != 1) all_weight_one = false;
}
```

| 特殊性质 | 写法 |
|---|---|
| 边权全 1 | BFS |
| 小图 | Floyd |
| 已是树 | TreeInfo/LCA/树 DP |
| 链 | 转数组前缀和/相邻处理 |
| 星 | 中心点特判 |
| DAG | Topo + DP |

## V2：小图精确

小图多源最短路：

```cpp
const int MAXF = 505;
static ll dist_small[MAXF][MAXF];

void floyd_small(const Graph& G) {
    int n = G.n;
    assert(n > 0 && n < MAXF);
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++) {
            dist_small[i][j] = (i == j ? 0 : LINF);
        }
    }
    for (auto e : G.edges) {
        dist_small[e.from][e.to] = min(dist_small[e.from][e.to], e.w);
        if (!e.directed) dist_small[e.to][e.from] = min(dist_small[e.to][e.from], e.w);
    }
    for (int k = 1; k <= n; k++) {
        for (int i = 1; i <= n; i++) {
            if (dist_small[i][k] == LINF) continue;
            for (int j = 1; j <= n; j++) {
                if (dist_small[k][j] == LINF) continue;
                dist_small[i][j] = min(dist_small[i][j], dist_small[i][k] + dist_small[k][j]);
            }
        }
    }
}
```

每问 BFS：仅限无权图或边权全为 1：

```cpp
int bfs_one_query(const Graph& G, int s, int t) {
    vector<int> dist(G.n + 1, -1);
    queue<int> q;
    dist[s] = 0;
    q.push(s);
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        if (u == t) return dist[u];
        for (auto e : G.g[u]) {
            int v = e.to;
            if (dist[v] != -1) continue;
            dist[v] = dist[u] + 1;
            q.push(v);
        }
    }
    return -1;
}
```

## V3：枚举点集/边集

枚举点集常用于：

- 最大独立集小数据。
- 最小点覆盖小数据。
- 选关键点是否满足条件。

枚举边集常用于小图 MST：

```cpp
ll brute_mst_edges(int n, vector<FullEdge>& edges) {
    int m = (int)edges.size();
    if (m > 22) return LINF;
    ll ans = LINF;
    for (long long mask = 0; mask < (1LL << m); mask++) {
        if (__builtin_popcount((unsigned)mask) != n - 1) continue;
        DSU dsu(n);
        ll cost = 0;
        int used = 0;
        for (int i = 0; i < m; i++) {
            if (!(mask >> i & 1)) continue;
            if (edges[i].directed) continue;
            if (dsu.unite(edges[i].from, edges[i].to)) {
                cost += edges[i].w;
                used++;
            }
        }
        if (used == n - 1) ans = min(ans, cost);
    }
    return ans == LINF ? -1 : ans;
}
```

只适合 `m <= 22` 左右。

## V4：树题暴力

每问 DFS 找距离：

```cpp
bool dfs_path_distance(const Graph& T, int u, int p, int target, ll cur, ll& ans) {
    if (u == target) {
        ans = cur;
        return true;
    }
    for (auto e : T.g[u]) {
        int v = e.to;
        if (v == p) continue;
        if (dfs_path_distance(T, v, u, target, cur + e.w, ans)) return true;
    }
    return false;
}

ll tree_distance_one_query(const Graph& T, int u, int v) {
    ll ans = -1;
    dfs_path_distance(T, u, 0, v, 0, ans);
    return ans;
}
```

暴力爬父亲 LCA：

```cpp
int lca_climb(int u, int v, const vector<int>& parent, const vector<int>& depth) {
    while (depth[u] > depth[v]) u = parent[u];
    while (depth[v] > depth[u]) v = parent[v];
    while (u != v) {
        u = parent[u];
        v = parent[v];
    }
    return u;
}
```

`n,q <= 2000` 时可以先交。大数据再换 GRAPH-09 倍增 LCA。

## V5：升级路线表

| 小数据/特殊版 | 正解模块 |
|---|---|
| 每问 BFS 无权最短路 | GRAPH-02 BFS，必要时多源 BFS |
| 每问 Dijkstra | GRAPH-03 Dijkstra |
| Floyd 小图 | Dijkstra/Floyd 按数据范围取舍 |
| 枚举边集 MST | GRAPH-06 Kruskal |
| 暴力拓扑 DFS | GRAPH-05 Topo / DP-15 DAG DP |
| 每问树上 DFS | TREE-01 + GRAPH-09 LCA |
| 枚举点集树 DP | DP-14 树形 DP |
| 普通 BFS 状态 | BRUTE-11 状态 BFS |

常见坑：

- 小数据版本也要保证大数据不会 TLE 到完全没结果；可用条件分支保护。
- 有向/无向别建反。
- 边权全 1 才能 BFS。
- 树必须连通且 `m=n-1`。
- 枚举 `1<<m` 时 `m` 不能太大。
- 暴力 DFS 树路径递归深度可能爆栈，链很长时谨慎。

暴力/部分分替代：

- 本模块本身就是部分分路线。
- 不会正解时，至少保留小数据精确解和特殊性质精确解。

升级方向：

```text
合法兜底
-> 特判特殊性质
-> 小图精确
-> 暴力枚举/每问 DFS
-> 正式图论/树算法
```

最小测试样例：

```text
树路径：
3
1 2 5
2 3 7
query 1 3
输出：12
```
