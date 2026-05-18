# GRAPH-08 有向图强连通分量 SCC

模块编号：GRAPH-08

模块名称：SCC、Tarjan 强连通分量

标签：[图论][SCC][Tarjan][有向图][缩点]

一句话用途：把有向图中互相可达的点缩成一个强连通分量，得到 DAG 后继续做 DP 或统计。

题面触发词：

- 有向图互相可达。
- 强连通分量、缩点。
- 一组点之间都能到达。
- 有向图中最少加边、缩点后入度出度。

什么时候用：

- 图是有向图。
- 需要判断哪些点互相可达。
- 有环的有向图要先缩成 DAG 再 DP。
- 需要统计 SCC 个数、每个分量大小。

不要什么时候用：

- 无向图连通块用 BFS/DFS 或 DSU。
- 只求从单点能到哪些点，用普通 DFS/BFS。
- DAG 已经无环，不需要 SCC。
- 递归深度极大时 Tarjan 递归可能爆栈，要小心环境。

复杂度：

- `O(n + m)` 时间。
- `O(n + m)` 空间。

数据范围参考：

- `n,m <= 2e5` 常用。
- 递归栈风险与链长有关。

依赖的标准容器：

- `Graph`。
- 遍历 `G.g[u]`。
- 建图必须使用 `G.add_directed(u, v)`。
- 本模块只消费有向边，混入无向边时会跳过。

输入如何整理：

```cpp
Graph G(n);
for (int i = 1; i <= m; i++) {
    int u, v;
    cin >> u >> v;
    G.add_directed(u, v);
}
```

接口：

```text
SCCResult tarjan_scc(const Graph& G)
Graph build_scc_dag(const Graph& G, const SCCResult& scc)
```

输出能力：

- `belong[u]`：点 `u` 属于哪个 SCC。
- `size[c]`：分量大小。
- `cnt`：分量数量。
- 缩点 DAG。

下游可接：

- DAG DP。
- 缩点后拓扑排序。
- 入度/出度统计。

可拼接模块：

- `Graph + SCC + Topo + DAG DP`。
- `SCC + component indegree/outdegree`。

模板代码：

```cpp
struct SCCResult {
    int cnt = 0;
    vector<int> belong;
    vector<int> sz;
};

struct TarjanSCC {
    const Graph *G = nullptr;
    int timer = 0, scc_cnt = 0;
    vector<int> dfn, low, in_st, st, belong, sz;

    void dfs(int u) {
        dfn[u] = low[u] = ++timer;
        st.push_back(u);
        in_st[u] = 1;
        for (auto e : G->g[u]) {
            if (!e.directed) continue;
            int v = e.to;
            if (!dfn[v]) {
                dfs(v);
                low[u] = min(low[u], low[v]);
            } else if (in_st[v]) {
                low[u] = min(low[u], dfn[v]);
            }
        }
        if (low[u] == dfn[u]) {
            scc_cnt++;
            int x = 0;
            do {
                x = st.back();
                st.pop_back();
                in_st[x] = 0;
                belong[x] = scc_cnt;
                if ((int)sz.size() <= scc_cnt) sz.resize(scc_cnt + 1, 0);
                sz[scc_cnt]++;
            } while (x != u);
        }
    }

    SCCResult run(const Graph &graph) {
        G = &graph;
        int n = G->n;
        timer = scc_cnt = 0;
        dfn.assign(n + 1, 0);
        low.assign(n + 1, 0);
        in_st.assign(n + 1, 0);
        belong.assign(n + 1, 0);
        sz.assign(1, 0);
        st.clear();
        for (int i = 1; i <= n; i++) {
            if (!dfn[i]) dfs(i);
        }
        return {scc_cnt, belong, sz};
    }
};

SCCResult tarjan_scc(const Graph &G) {
    TarjanSCC solver;
    return solver.run(G);
}

Graph build_scc_dag(const Graph &G, const SCCResult &scc) {
    Graph dag(scc.cnt);
    set<pair<int, int>> seen;
    for (auto e : G.edges) {
        if (!e.directed) continue;
        int a = scc.belong[e.from];
        int b = scc.belong[e.to];
        if (a == b) continue;
        if (seen.insert({a, b}).second) {
            dag.add_directed(a, b, e.w);
        }
    }
    return dag;
}

pair<int, int> scc_zero_indeg_outdeg(const Graph &dag) {
    vector<int> indeg(dag.n + 1, 0), outdeg(dag.n + 1, 0);
    for (auto e : dag.edges) {
        if (!e.directed) continue;
        outdeg[e.from]++;
        indeg[e.to]++;
    }
    int zero_in = 0, zero_out = 0;
    for (int i = 1; i <= dag.n; i++) {
        if (indeg[i] == 0) zero_in++;
        if (outdeg[i] == 0) zero_out++;
    }
    return {zero_in, zero_out};
}
```

调用示例：

```cpp
auto scc = tarjan_scc(G);
cout << scc.cnt << "\n";
auto dag = build_scc_dag(G, scc);
auto order = topo_sort(dag);

if (scc.cnt == 1) {
    cout << 0 << "\n";
} else {
    auto [zin, zout] = scc_zero_indeg_outdeg(dag);
    cout << max(zin, zout) << "\n"; // 最少加边使缩点 DAG 强连通
}
```

常见坑：

- SCC 是有向图概念，建边要用 `G.add_directed(u, v)`。
- 标准模板会跳过无向边；如果题目本来就是有向图，不要混入无向边。
- `dfn/low/in_st` 三个数组不能混用。
- 弹栈时直到弹出 `u` 为止。
- 缩点后可能有重边，本模板按 `(from,to)` 去重且保留第一条权值；如果要最短路取最小权、最长路取最大权、路径计数保留重边，需要按题意改去重策略。
- 递归深度过大可能爆栈。
- SCC 编号不保证拓扑序。

暴力/部分分替代：

- `n <= 300` 可 Floyd 求可达矩阵，互相可达归为一组。
- `n <= 2000` 可从每个点 DFS，得到可达性后分组。
- 只判断两个点是否互达，可以分别 DFS 一次。

升级方向：

- 缩点 DAG 后接 Topo/DAG DP。
- 统计最少加边强连通：看缩点 DAG 入度为 0 和出度为 0 的分量数。
- 2-SAT 是 SCC 的专门应用。

最小测试样例：

```text
4 4
1 2
2 1
2 3
3 4
SCC: {1,2}, {3}, {4}
缩点后是 DAG
```
