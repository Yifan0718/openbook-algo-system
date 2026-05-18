# GRAPH-00 标准 Graph 与建图场景

模块编号：GRAPH-00

模块名称：标准 Graph、建图场景、有向/无向图

标签：[图论][标准容器][建图][1-index]

一句话用途：把题面里的边统一整理成 `Graph`，后续 BFS、DFS、Dijkstra、Topo、Kruskal、Floyd、Bellman-Ford、SCC、LCA 都尽量共用它。

题面触发词：

- 有 `n` 个点、`m` 条边。
- 道路、航线、关系、依赖、连接、能到达。
- 树、森林、无向图、有向图、带权图。
- 点编号通常是 `1..n`。

什么时候用：

- 普通图论题先用本模块建图。
- 需要从点出发遍历时使用 `G.g[u]`。
- 需要处理全部边、排序边、初始化矩阵时使用 `G.edges`。
- 权值、距离、答案统一优先用 `ll`。

不要什么时候用：

- 最大流、最小费用流不要直接用本 `Graph`，它们需要残量边，见 `GRAPH-10`。
- 极限内存卡得很死时，可能要链式前向星。
- 网格 BFS 通常直接用二维数组和方向数组，除非题目明显要转图。

复杂度：

- 建图：`O(n + m)` 空间，`O(m)` 时间。
- 无向边在 `G.g` 中存两次，在 `G.edges` 中只存一次逻辑边。

数据范围参考：

- `n,m <= 2e5` 常规可用。
- `m` 特别大时注意 `vector<vector<AdjEdge>>` 的常数和内存。

依赖的标准容器：

- `Graph`。
- 1-index 点编号。
- `ll` 边权。

输入如何整理：

```cpp
int n, m;
cin >> n >> m;
Graph G(n);
for (int i = 1; i <= m; i++) {
    int u, v;
    ll w;
    cin >> u >> v >> w;
    G.add_undirected(u, v, w); // 无向带权
}
```

接口：

```text
Graph G(n)
G.init(n)
G.add_undirected(u, v, w)
G.add_directed(u, v, w)
G.g[u]      从 u 出发的邻接边
G.edges     每条输入逻辑边
```

输出能力：

- 统一邻接表。
- 统一全边表。
- 记录有向/无向信息，方便 Floyd、Bellman-Ford 等模块。

下游可接：

- DFS/BFS、无权最短路、Dijkstra、Topo、DAG DP、SCC、LCA。
- Floyd、Bellman-Ford、Kruskal。

可拼接模块：

- `GRAPH-01` 连通性。
- `GRAPH-02/03/04` 最短路。
- `GRAPH-05` Topo/DAG DP。
- `GRAPH-06` DSU/Kruskal。
- `GRAPH-08` SCC。
- `GRAPH-09` 树和 LCA。

模板代码：

```cpp
struct AdjEdge {
    int to;
    ll w;
    int edge_index; // 内部边下标，只给模板内部跳父边/查原边用
    bool directed;
    int input_id;   // 对外边号，默认 1-index
};

struct FullEdge {
    int from, to;
    ll w;
    bool directed;
    int input_id;   // 对外边号，默认 1-index
};

struct Graph {
    int n;
    vector<vector<AdjEdge>> g;
    vector<FullEdge> edges;

    Graph(int n = 0) {
        init(n);
    }

    void init(int n_) {
        n = n_;
        g.assign(n + 1, {});
        edges.clear();
    }

    void add_edge_raw(int u, int v, ll w, bool directed) {
        int edge_index = (int)edges.size(); // 内部 0-based，不输出
        int input_id = edge_index + 1;      // 题面边号统一 1-based
        edges.push_back({u, v, w, directed, input_id});
        g[u].push_back({v, w, edge_index, directed, input_id});
        if (!directed) {
            g[v].push_back({u, w, edge_index, directed, input_id});
        }
    }

    void add_undirected(int u, int v, ll w = 1) {
        add_edge_raw(u, v, w, false);
    }

    void add_directed(int u, int v, ll w = 1) {
        add_edge_raw(u, v, w, true);
    }
};
```

调用示例：

```cpp
Graph G(n);
G.add_undirected(1, 2);       // 无向无权
G.add_undirected(2, 3, 5);    // 无向带权
G.add_directed(3, 4, 7);      // 有向带权 3 -> 4
G.add_directed(4, 5);         // 有向无权 4 -> 5，更不容易写错

for (auto e : G.g[2]) {
    int v = e.to;
    ll w = e.w;
    int input_id = e.input_id; // 1-index，可直接输出题面边号
}

for (auto e : G.edges) {
    int u = e.from;
    int v = e.to;
}
```

常见坑：

- 无向图只写 `add_undirected`，有向图只写 `add_directed`；考场不要直接调用 `add_edge_raw`。
- 不要写 `G.add_edge(u, v, true)` 这种四参/布尔接口；本资料主模板故意不暴露它，避免把 `true` 当权值。
- Kruskal 只能遍历 `G.edges`，不要遍历 `G.g`，否则无向边会重复。
- Topo 和 SCC 通常要求有向边，建图时统一写 `G.add_directed(u, v, w)`；不要临时改回布尔参数接口。
- Floyd 初始化时要看 `e.directed`，无向边要对称赋值。
- 多组数据必须重新 `G.init(n)`。
- 如果题目点编号是 `0..n-1`，读入时立刻 `u++, v++` 转成内部 `1..n`，后续不要切换到 0-index。
- 点编号默认 1-index；对外边号用 `input_id`，也是 1-index。内部 `edge_index` 不输出，只给 Lowlink 跳父边等模板内部使用。

## 图类型与模块路由协议

| 图类型 | 建图方式 | 优先模块 | 误用风险 |
|---|---|---|---|
| 无向无权图 | `add_undirected(u,v)` | DFS/BFS、连通块、二分图 | Topo/SCC 不适用 |
| 无向带权图 | `add_undirected(u,v,w)` | Dijkstra、Kruskal、树 LCA | Kruskal 遍历 `edges`，不要遍历 `g` |
| 有向无权图 | `add_directed(u,v)` | BFS、Topo、SCC | 不要临时改回布尔参数接口 |
| 有向带权图 | `add_directed(u,v,w)` | Dijkstra、Bellman-Ford、DAG DP | 有负边不能 Dijkstra |
| DAG | 全部有向边且无环 | Topo、DAG DP | `topo.size()!=n` 说明有环 |
| 树 | 无向、连通、`m=n-1` | TreeDFS、LCA、树形 DP | 一般图不能当树 |
| 流网络 | `FlowGraph` | Dinic | 不用普通 `Graph` |

暴力/部分分替代：

- 点很少时可以用邻接矩阵 `dist[n+1][n+1]`。
- 只判断一两次连通时，可临时用二维 `bool adj` + DFS。

升级方向：

- 普通无权图：接 BFS。
- 非负权：接 Dijkstra。
- 小图全源：接 Floyd。
- 最小生成树：接 DSU/Kruskal。
- 树路径：接 DFS distance + LCA。

最小测试样例：

```text
n=3
add 1 2 undirected
add 2 3 directed
G.g[1] 有 2
G.g[2] 有 1 和 3
G.g[3] 没有 2
G.edges.size() = 2
```
