# GRAPH-01 DFS/BFS 连通与遍历

模块编号：GRAPH-01

模块名称：DFS/BFS 连通、连通块、可达性

标签：[图论][DFS][BFS][连通性][可达性]

一句话用途：从某个点出发访问所有能到达的点，或把整张图分成若干连通块。

题面触发词：

- 是否连通、能不能到达。
- 有几个连通块。
- 从 `s` 出发能访问哪些点。
- 岛屿、网络、关系传递。

什么时候用：

- 无权图只关心可达，不关心最短距离。
- 无向图统计连通块。
- 有向图从一个起点统计可达点。
- 树上从根遍历父子关系。

不要什么时候用：

- 要最短路距离时优先用 `GRAPH-02` 无权 BFS 或 `GRAPH-03` Dijkstra。
- 有很多次动态加边连通查询时，优先 DSU。
- 有向图要求强连通分量时，用 SCC。
- 递归深度可能到 `2e5` 时，DFS 递归可能爆栈，优先 BFS 或手写栈。

复杂度：

- `O(n + m)` 时间。
- `O(n)` 额外空间。

数据范围参考：

- `n,m <= 2e5` 常规可用。
- 深链树建议 BFS 或迭代 DFS。

依赖的标准容器：

- `Graph`。
- 遍历从 `G.g[u]` 出发。

输入如何整理：

```cpp
Graph G(n);
for (int i = 1; i <= m; i++) {
    int u, v;
    cin >> u >> v;
    G.add_undirected(u, v); // 无向连通性
}
```

接口：

```text
vector<int> bfs_order(const Graph& G, int s)
vector<int> dfs_order_iterative(const Graph& G, int s)
vector<int> connected_component_id_undirected(const Graph& G, int& cnt)
```

输出能力：

- 一次遍历顺序。
- 每个点所属连通块编号。
- 连通块数量。

下游可接：

- 连通块内分别做 DP。
- 检查图是否连通后再跑 Kruskal、树算法。
- BFS 最短路模块。

可拼接模块：

- `Graph + DFS/BFS + TreeDFS`。
- `Graph + BFS + BipartiteColor`。
- `Graph + DSU` 连通性互相替换。

模板代码：

```cpp
vector<int> bfs_order(const Graph &G, int s) {
    vector<int> vis(G.n + 1, 0), order;
    queue<int> q;
    vis[s] = 1;
    q.push(s);
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        order.push_back(u);
        for (auto e : G.g[u]) {
            int v = e.to;
            if (vis[v]) continue;
            vis[v] = 1;
            q.push(v);
        }
    }
    return order;
}

vector<int> dfs_order_iterative(const Graph &G, int s) {
    vector<int> vis(G.n + 1, 0), order;
    vector<int> st;
    st.push_back(s);
    while (!st.empty()) {
        int u = st.back();
        st.pop_back();
        if (vis[u]) continue;
        vis[u] = 1;
        order.push_back(u);
        for (auto e : G.g[u]) {
            int v = e.to;
            if (!vis[v]) st.push_back(v);
        }
    }
    return order;
}

// 仅限无向图连通块；有向图强连通请用 SCC。
vector<int> connected_component_id_undirected(const Graph &G, int &cnt) {
    vector<int> comp(G.n + 1, 0);
    cnt = 0;
    for (int s = 1; s <= G.n; s++) {
        if (comp[s]) continue;
        cnt++;
        queue<int> q;
        comp[s] = cnt;
        q.push(s);
        while (!q.empty()) {
            int u = q.front();
            q.pop();
            for (auto e : G.g[u]) {
                int v = e.to;
                if (comp[v]) continue;
                comp[v] = cnt;
                q.push(v);
            }
        }
    }
    return comp;
}
```

调用示例：

```cpp
auto order = bfs_order(G, 1);

int cnt = 0;
auto comp = connected_component_id_undirected(G, cnt);
cout << cnt << "\n";
cout << (comp[x] == comp[y] ? "YES" : "NO") << "\n";
```

常见坑：

- 有向图的可达性不是无向连通性，`G.add_directed(u,v)` 只能从 `u` 到 `v`。
- 递归 DFS 在长链上容易爆栈。
- 连通块编号要从所有未访问点启动，而不是只从 1。
- 多组数据 `vis/comp` 要重新开。
- 自环不会影响连通性，重边只会多遍历几次。

暴力/部分分替代：

- `n <= 500` 可用邻接矩阵 + DFS。
- 查询次数少时，每次从起点 BFS 判断可达。
- 静态多次连通查询可升级为一次连通块编号或 DSU。

升级方向：

- 可达 + 最短步数：换无权 BFS。
- 多次合并集合：换 DSU。
- 有向强连通：换 SCC。
- 树上遍历：接树上 DFS 距离。

最小测试样例：

```text
4 2
1 2
3 4
连通块数 = 2
comp[1] == comp[2]
comp[1] != comp[3]
```
