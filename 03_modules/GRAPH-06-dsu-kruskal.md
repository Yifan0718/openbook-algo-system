# GRAPH-06 DSU 与 Kruskal 最小生成树

模块编号：GRAPH-06

模块名称：DSU、Kruskal、最小生成树

拼接提醒：本模块和 `DS-04` 都给了 DSU。写 MST 时优先保留本模块的 `struct DSU`，如果前面已经复制过 DSU，就不要再复制第二份。

标签：[图论][并查集][Kruskal][最小生成树]

一句话用途：无向带权图中选出连接所有点且总权值最小的 `n-1` 条边。

题面触发词：

- 最小生成树、修路最小成本。
- 连接所有点、总代价最小。
- 无向带权图。
- 判断能不能把所有点连通。

什么时候用：

- 图是无向图。
- 要连通所有点，边权总和最小。
- 只需要一棵生成树，不需要起点到终点最短路。
- 边可以排序。

不要什么时候用：

- 有向图最小树形图不是 Kruskal。
- 问两点最短路径不要用 MST 代替。
- 图不连通时没有生成树，只能得到森林。
- 动态加删边 MST 不是本模板。

复杂度：

- 排序 `O(m log m)`。
- DSU 合并近似 `O(1)` 均摊。

数据范围参考：

- `n,m <= 2e5` 常规可用。
- 权值和用 `ll`。

依赖的标准容器：

- `Graph`。
- 只遍历 `G.edges`。
- `DSU`。

输入如何整理：

```cpp
Graph G(n);
for (int i = 1; i <= m; i++) {
    int u, v;
    ll w;
    cin >> u >> v >> w;
    G.add_undirected(u, v, w); // Kruskal 必须按无向边理解
}
```

接口：

```text
DSU.init(n), find(x), unite(a,b), same(a,b)
KruskalResult kruskal(const Graph& G)
```

输出能力：

- MST 总权值。
- 是否成功连接所有点。
- 被选中的边编号。

下游可接：

- 树上 DFS/LCA。
- 最大边最小化瓶颈树。
- 连通性检查。

可拼接模块：

- `Graph.edges + DSU + Kruskal`。
- `Kruskal + TreeDFS`。
- `Kruskal + LCA`。

模板代码：

```cpp
struct DSU {
    vector<int> fa, sz;

    DSU(int n = 0) {
        if (n > 0) init(n);
    }

    void init(int n) {
        fa.resize(n + 1);
        sz.assign(n + 1, 1);
        iota(fa.begin(), fa.end(), 0);
    }

    int find(int x) {
        while (x != fa[x]) {
            fa[x] = fa[fa[x]];
            x = fa[x];
        }
        return x;
    }

    bool unite(int a, int b) {
        a = find(a);
        b = find(b);
        if (a == b) return false;
        if (sz[a] < sz[b]) swap(a, b);
        fa[b] = a;
        sz[a] += sz[b];
        return true;
    }

    bool same(int a, int b) {
        return find(a) == find(b);
    }
};

struct KruskalResult {
    ll total = 0;
    bool connected = false;
    vector<int> chosen_input_ids; // 1-index 题面边号
};

KruskalResult kruskal(const Graph &G) {
    vector<int> ord((int)G.edges.size());
    iota(ord.begin(), ord.end(), 0);
    sort(ord.begin(), ord.end(), [&](int a, int b) {
        return G.edges[a].w < G.edges[b].w;
    });

    DSU dsu;
    dsu.init(G.n);
    KruskalResult res;
    for (int id : ord) {
        auto e = G.edges[id];
        if (e.directed) continue; // MST 只处理无向边
        if (dsu.unite(e.from, e.to)) {
            res.total += e.w;
            res.chosen_input_ids.push_back(e.input_id);
        }
    }
    res.connected = ((int)res.chosen_input_ids.size() == G.n - 1);
    return res;
}
```

调用示例：

```cpp
auto mst = kruskal(G);
if (!mst.connected) {
    cout << "orz\n";
} else {
    cout << mst.total << "\n";
}
```

常见坑：

- Kruskal 遍历 `G.edges`，不要遍历 `G.g`。
- MST 是无向图问题，建边要用 `G.add_undirected(u, v, w)`；输入有向边不能直接套。
- 图不连通时选不到 `n-1` 条边。
- 边权可能为负，Kruskal 仍然可用。
- 如果题目要求最大生成树，把排序改成从大到小。
- `total` 用 `ll`。

暴力/部分分替代：

- `n <= 10` 可枚举边子集，选 `n-1` 条判断连通。
- `m` 小时可用暴力加边排序仍然是 Kruskal 的雏形。
- 只判断连通时直接 DSU，不用排序。

升级方向：

- MST 建出树后可接 LCA 做树上最大边查询。
- 最小瓶颈生成树直接用 Kruskal 的最大入选边。
- 稠密图也可用 Prim，但本卷统一优先 Kruskal。

最小测试样例：

```text
4 5
1 2 1
2 3 2
3 4 3
1 4 10
1 3 5
MST total = 6
```
