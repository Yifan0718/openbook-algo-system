# GRAPH-13 无向图桥与割点

模块编号：GRAPH-13

模块名称：Lowlink、桥、割点

标签：[图论][无向图][桥][割点][lowlink][Tarjan]

一句话用途：找无向图中删掉会增加连通块数量的边或点，用于“关键道路、关键城市、网络脆弱点”等题。

题面触发词：

- 关键边、桥、割边。
- 关键点、割点。
- 删除一条边/一个点后是否不连通。
- 网络可靠性、必经道路。

什么时候用：

- 图是无向图。
- 需要一次性找出所有桥或割点。
- `n,m` 较大，不能枚举删除每条边/每个点再 DFS。

不要什么时候用：

- 有向图强连通问题，转 SCC。
- 只是判断普通连通性，用 DFS/BFS/DSU。
- 动态加删边，不是本模板。
- 递归深度可能到 `2e5` 时要注意栈风险。

复杂度：

- `O(n + m)` 时间。
- `O(n + m)` 空间。

数据范围参考：

- `n,m <= 2e5` 常见可用。
- 链状图会有深递归风险；若评测栈很小，考虑改迭代或只拿部分分。

依赖的标准容器：

- 标准 `Graph`。
- 图必须用无向边 `add_undirected`。
- 依赖 `AdjEdge.edge_index` 区分重边，不能只用 `v == parent` 跳过。

输入如何整理：

```cpp
Graph G(n);
for (int i = 1; i <= m; i++) {
    int u, v;
    cin >> u >> v;
    G.add_undirected(u, v);
}
```

接口：

```cpp
LowlinkResult find_bridges_cutpoints(const Graph& G);
```

输出能力：

- `bridge_input_ids`：桥对应的题面边号，1-index，可直接输出。
- `bridges`：桥的两个端点。
- `is_cut[u]`：点 `u` 是否为割点。
- `dfn/low`：调试或进阶使用。

下游可接：

- 桥边删除后分块。
- 边双连通/点双连通低优先级进阶。
- 图论部分分：小图先枚举删除，满分再 Lowlink。

可拼接模块：

- `Graph + Lowlink`。
- `Lowlink + DSU`。
- `Lowlink + DFS component`。

模板代码：

```cpp
struct LowlinkResult {
    vector<int> dfn;
    vector<int> low;
    vector<int> is_cut;
    vector<int> bridge_input_ids;
    vector<pair<int, int>> bridges;
};

struct LowlinkSolver {
    const Graph *G = nullptr;
    int timer = 0;
    LowlinkResult res;

    void dfs(int u, int parent_edge) {
        res.dfn[u] = res.low[u] = ++timer;
        int child_count = 0;

        for (auto e : G->g[u]) {
            if (e.directed) continue;
            int v = e.to;
            if (!res.dfn[v]) {
                child_count++;
                dfs(v, e.edge_index);
                res.low[u] = min(res.low[u], res.low[v]);

                if (res.low[v] > res.dfn[u]) {
                    res.bridge_input_ids.push_back(e.input_id);
                    res.bridges.push_back({u, v});
                }

                if (parent_edge != -1 && res.low[v] >= res.dfn[u]) {
                    res.is_cut[u] = 1;
                }
            } else if (e.edge_index != parent_edge) {
                res.low[u] = min(res.low[u], res.dfn[v]);
            }
        }

        if (parent_edge == -1 && child_count > 1) {
            res.is_cut[u] = 1;
        }
    }

    LowlinkResult run(const Graph &graph) {
        G = &graph;
        timer = 0;
        res.dfn.assign(G->n + 1, 0);
        res.low.assign(G->n + 1, 0);
        res.is_cut.assign(G->n + 1, 0);
        res.bridge_input_ids.clear();
        res.bridges.clear();

        for (int i = 1; i <= G->n; i++) {
            if (!res.dfn[i]) dfs(i, -1);
        }
        return res;
    }
};

LowlinkResult find_bridges_cutpoints(const Graph &G) {
    LowlinkSolver solver;
    return solver.run(G);
}
```

调用示例：

```cpp
auto res = find_bridges_cutpoints(G);
cout << res.bridges.size() << '\n';
for (auto [u, v] : res.bridges) {
    cout << u << ' ' << v << '\n';
}
for (int u = 1; u <= n; u++) {
    if (res.is_cut[u]) cout << "cut " << u << '\n';
}
```

常见坑：

- 桥/割点是无向图概念，建边要用 `G.add_undirected(u, v)`，模板只处理无向边。
- 有重边时不能只写 `if (v == parent) continue`，要按边 id 跳过父边。
- 根节点是割点的条件是 DFS 树儿子数大于 1。
- `low[v] > dfn[u]` 是桥；`low[v] >= dfn[u]` 是非根割点条件。
- `bridge_input_ids` 是 1-index 题面边号；如果只需要输出桥的两个端点，直接用 `bridges`。
- 递归深度很深可能栈溢出。

暴力/部分分替代：

- `n,m <= 2000`：枚举删除每条边，再 DFS 判断连通。
- `n <= 500`：枚举删除每个点，再 DFS 判断连通。
- 只问某一条边是不是桥：删掉它后从一端 DFS 看能否到另一端。

升级方向：

- 桥 -> 边双连通分量。
- 割点 -> 点双连通分量。
- 有向“关键可达结构”通常转 SCC 或支配树，支配树低优先级。

最小测试样例：

```text
5 5
1 2
2 3
3 1
3 4
4 5
桥：3-4, 4-5
割点：3, 4
```
