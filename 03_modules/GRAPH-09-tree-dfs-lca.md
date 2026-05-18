# GRAPH-09 树上 DFS、距离与 LCA

模块编号：GRAPH-09

模块名称：树上 DFS、树上距离、LCA

标签：[图论][树][DFS][LCA][倍增][距离]

一句话用途：在无向树上预处理深度、根距离和倍增父亲，快速回答祖先、最近公共祖先、两点距离。

题面触发词：

- 树、`n` 个点 `n-1` 条边。
- 祖先、公共祖先、最近公共祖先。
- 树上两点距离、路径长度。
- 多次询问树上路径。

什么时候用：

- 输入是一棵树或森林中的一棵根树。
- 多次询问 LCA 或两点距离。
- 边权可能存在，距离用 `ll`。
- 需要父节点、深度、到根距离。

不要什么时候用：

- 一般图有环时不能直接当树。
- 单次两点路径可 BFS/DFS 一次，不一定要 LCA。
- 动态加边删边的树路径不是本模板。
- 根会频繁变化时，需要额外处理。

复杂度：

- 预处理：`O(n log n)`。
- 每次 LCA：`O(log n)`。
- 空间：`O(n log n)`。

数据范围参考：

- `n,q <= 2e5` 常规可用。
- `LOG` 自动按 `n` 计算。

依赖的标准容器：

- `Graph`。
- 树边用 `G.add_undirected(u, v, w)`。
- 遍历 `G.g[u]`。
- 调用 `build` 前最好先用 `TREE-01 is_connected_tree(T)` 检查：无向、连通、边数为 `n-1`。

输入如何整理：

```cpp
Graph T(n);
for (int i = 1; i <= n - 1; i++) {
    int u, v;
    ll w;
    cin >> u >> v >> w;
    T.add_undirected(u, v, w);
}
```

接口：

```text
LCA.build(Graph, root)
LCA.query(u, v)
LCA.distance(u, v)
depth[u], distRoot[u], up[k][u]
```

输出能力：

- 每个点深度。
- 每个点到根的距离。
- `u,v` 的 LCA。
- `u,v` 的树上距离。

下游可接：

- 树上路径查询。
- Kruskal 后建 MST 树再查路径。
- 树形 DP。

可拼接模块：

- `Graph(Tree) + DFS + LCA`。
- `Kruskal + Tree + LCA`。
- `TreeDFS + DP`。

模板代码：

```cpp
struct LCA {
    int n = 0, LOG = 0;
    int root = 1;
    vector<int> depth;
    vector<ll> distRoot;
    vector<vector<int>> up;

    void build(const Graph &G, int root_ = 1) {
        // 前置条件：G 是无向连通树，root_ 是 1..n 的点号。
        n = G.n;
        root = root_;
        LOG = 1;
        while ((1 << LOG) <= n) LOG++;
        depth.assign(n + 1, 0);
        distRoot.assign(n + 1, 0);
        up.assign(LOG, vector<int>(n + 1, 0));

        queue<int> q;
        vector<int> vis(n + 1, 0);
        vis[root] = 1;
        up[0][root] = root;
        depth[root] = 1;
        q.push(root);
        while (!q.empty()) {
            int u = q.front();
            q.pop();
            for (auto e : G.g[u]) {
                int v = e.to;
                if (vis[v]) continue;
                vis[v] = 1;
                up[0][v] = u;
                depth[v] = depth[u] + 1;
                distRoot[v] = distRoot[u] + e.w;
                q.push(v);
            }
        }
        for (int k = 1; k < LOG; k++) {
            for (int v = 1; v <= n; v++) {
                up[k][v] = up[k - 1][up[k - 1][v]];
            }
        }
    }

    int lift(int u, int steps) const {
        for (int k = 0; k < LOG; k++) {
            if (steps & (1 << k)) u = up[k][u];
        }
        return u;
    }

    int query(int a, int b) const {
        if (depth[a] < depth[b]) swap(a, b);
        a = lift(a, depth[a] - depth[b]);
        if (a == b) return a;
        for (int k = LOG - 1; k >= 0; k--) {
            if (up[k][a] != up[k][b]) {
                a = up[k][a];
                b = up[k][b];
            }
        }
        return up[0][a];
    }

    ll distance(int a, int b) const {
        int c = query(a, b);
        return distRoot[a] + distRoot[b] - 2LL * distRoot[c];
    }
};
```

调用示例：

```cpp
LCA lca;
lca.build(T, 1);
int c = lca.query(u, v);
cout << c << "\n";
cout << lca.distance(u, v) << "\n";
```

常见坑：

- 树要用无向边。
- `n` 个点必须有 `n-1` 条边且连通，森林要对每棵树单独处理或加超级根。
- 边权距离用 `ll`。
- 根的父亲设成根自己，避免查询时跳到虚拟 0 点。
- 根不同，父子关系不同，但无权/带权两点距离不受根影响。
- 如果只读无权树，`w` 默认 1。

暴力/部分分替代：

- 单次距离查询可从 `u` BFS/DFS 到 `v`。
- `q` 很小可每次爬父亲或 DFS。
- `n <= 2000` 可预处理任意两点距离。

升级方向：

- 路径上最大边：倍增表同时存 `mx[k][v]`。
- 子树查询：DFS 序 + 树状数组/SegmentTree。
- 树上修改查询：重链剖分，低优先级。

最小测试样例：

```text
5
1 2 3
1 3 2
2 4 4
2 5 1
LCA(4,5)=2
distance(4,3)=9
```
