# TREE-01：普通树 RootedTree 信息层

模块编号：TREE-01

模块名称：普通树 RootedTree 信息层

标签：树、DFS序、父亲、深度、子树大小、1-index、模块拼接

一句话用途：把一棵无向树整理成有根树信息：`parent/depth/distRoot/order/tin/tout/subtree_size/children`，后续接 LCA、树形 DP、DFS 序子树查询。

题面触发词：

- “给一棵树”
- “以 1 为根”
- “子树”
- “父亲、深度、祖先”
- “树上路径/树上 DP/子树查询”

什么时候用：

- 题目给的是普通无向树，需要先确定根。
- 后续要用树形 DP、LCA、DFS 序、子树大小。
- 想把树题的第一步统一成一个可复用结构。

不要什么时候用：

- 输入不是树，而是一般图有环。
- 动态加边删边，普通 DFS 序会失效。
- 只是单次连通性或最短路，不一定需要完整 TreeInfo。

复杂度：

- 建树信息：`O(n)`。
- 空间：`O(n)`。

数据范围信号：

- `n <= 2e5` 可用 BFS/迭代 DFS，避免递归爆栈。
- `n` 很小也可直接递归 DFS，但本模块给迭代版。

依赖的标准容器：

- 标准 `Graph`。
- `vector<int>`
- `vector<ll>`

输入如何整理：

```cpp
Graph T(n);
for (int i = 1; i <= n - 1; i++) {
    int u, v;
    cin >> u >> v;
    T.add_undirected(u, v);
}
```

接口：

```cpp
TreeInfo build_tree_info(const Graph& T, int root);
bool is_connected_tree(const Graph& G);
```

输出能力：

- `parent[u]`：父亲。
- `depth[u]`：深度。
- `distRoot[u]`：到根距离。
- `children[u]`：有根树儿子。
- `order`：从根 BFS/DFS 的顺序。
- `tin/tout`：DFS 序，子树区间是 `[tin[u], tout[u]]`。
- `subtree_size[u]`：子树大小。

下游可接：

- GRAPH-09 LCA。
- DP-14 树形 DP。
- 树状数组/SegmentTree 子树查询。
- 树直径、换根 DP。

可拼接模块：

- Graph 标准建图。
- 树状数组：对子树区间加/查。
- SegmentTree：对子树区间最值/和。

模板代码：

```cpp
struct TreeInfo {
    int n = 0;
    int root = 1;
    vector<int> parent;
    vector<int> depth;
    vector<ll> distRoot;
    vector<vector<int>> children;
    vector<int> order;
    vector<int> tin;
    vector<int> tout;
    vector<int> subtree_size;
};

bool is_connected_tree(const Graph& G) {
    if ((int)G.edges.size() != G.n - 1) return false;
    for (auto e : G.edges) {
        if (e.directed) return false;
    }
    vector<int> vis(G.n + 1, 0);
    queue<int> q;
    q.push(1);
    vis[1] = 1;
    int cnt = 0;
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        cnt++;
        for (auto e : G.g[u]) {
            int v = e.to;
            if (vis[v]) continue;
            vis[v] = 1;
            q.push(v);
        }
    }
    return cnt == G.n;
}

TreeInfo build_tree_info(const Graph& T, int root = 1) {
    TreeInfo info;
    info.n = T.n;
    info.root = root;
    info.parent.assign(T.n + 1, 0);
    info.depth.assign(T.n + 1, 0);
    info.distRoot.assign(T.n + 1, 0);
    info.children.assign(T.n + 1, {});
    info.tin.assign(T.n + 1, 0);
    info.tout.assign(T.n + 1, 0);
    info.subtree_size.assign(T.n + 1, 1);

    queue<int> q;
    vector<int> vis(T.n + 1, 0);
    q.push(root);
    vis[root] = 1;
    info.parent[root] = 0;
    info.depth[root] = 0;

    while (!q.empty()) {
        int u = q.front();
        q.pop();
        info.order.push_back(u);
        for (auto e : T.g[u]) {
            int v = e.to;
            if (vis[v]) continue;
            vis[v] = 1;
            info.parent[v] = u;
            info.depth[v] = info.depth[u] + 1;
            info.distRoot[v] = info.distRoot[u] + e.w;
            info.children[u].push_back(v);
            q.push(v);
        }
    }

    int timer = 0;
    vector<int> it(T.n + 1, 0);
    vector<int> st;
    st.push_back(root);
    while (!st.empty()) {
        int u = st.back();
        if (it[u] == 0) {
            info.tin[u] = ++timer;
        }
        if (it[u] < (int)info.children[u].size()) {
            int v = info.children[u][it[u]++];
            st.push_back(v);
        } else {
            info.tout[u] = timer;
            st.pop_back();
        }
    }

    for (int idx = (int)info.order.size() - 1; idx >= 0; idx--) {
        int u = info.order[idx];
        info.subtree_size[u] = 1;
        for (int v : info.children[u]) {
            info.subtree_size[u] += info.subtree_size[v];
        }
    }

    return info;
}
```

调用示例：

```cpp
if (!is_connected_tree(T)) {
    cout << "Not a tree\n";
    return;
}

TreeInfo tr = build_tree_info(T, 1);
cout << tr.parent[u] << ' ' << tr.depth[u] << ' ' << tr.subtree_size[u] << '\n';
```

DFS 序子树查询接法：

```cpp
// u 的子树对应 DFS 序闭区间 [tin[u], tout[u]]
BIT fw;
fw.init(n);
for (int u = 1; u <= n; u++) {
    fw.add(tr.tin[u], value[u]);
}
ll subtree_sum = fw.query(tr.tin[u], tr.tout[u]);
```

二叉树转普通 Graph：

```cpp
Graph binary_tree_to_graph(int n, const vector<int>& lc, const vector<int>& rc) {
    Graph T(n);
    for (int u = 1; u <= n; u++) {
        if (lc[u] > 0) T.add_undirected(u, lc[u]);
        if (rc[u] > 0) T.add_undirected(u, rc[u]);
    }
    return T;
}
```

常见坑：

- 普通树边必须无向建图。
- 调用 `build_tree_info` 前先确认 `is_connected_tree(T)`，否则有向边、森林、一般图都会让父子关系失真。
- `tin/tout` 是 DFS 序，不是 BFS 序。
- 子树区间 `[tin[u], tout[u]]` 只在固定根后成立。
- 换根后子树概念会改变。
- 链状树递归 DFS 可能爆栈，本模块用迭代版。

暴力/部分分替代：

- `n <= 2000`：每次询问直接 DFS 子树/路径。
- 只问一次子树大小：临时 DFS 即可。
- 不会 DFS 序时，先用 `children` 每次遍历子树拿部分分。

升级方向：

- `TreeInfo` -> LCA。
- `tin/tout` -> 树状数组/SegmentTree 子树查询。
- `children` -> DP-14 树形 DP。
- `parent/depth` -> 暴力爬父亲 LCA。

最小测试样例：

```text
5
1 2
1 3
2 4
2 5
root=1
parent[4]=2
depth[4]=2
subtree_size[2]=3
```
