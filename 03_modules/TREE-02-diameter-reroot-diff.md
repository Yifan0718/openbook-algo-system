# TREE-02 树直径、换根 DP 与树上差分

模块编号：TREE-02

模块名称：树直径、换根 DP、树上差分

标签：[树][直径][换根DP][树上差分][LCA][1-index]

一句话用途：补齐树题最常见的三个进阶拼接：求树上最远距离、每个点作为根/中心的答案、对多条路径做批量统计。

题面触发词：

- 树上最长路径、直径、最远点。
- “以每个点为根/中心”的答案。
- 多次给树上路径加一，最后统计每条边/每个点被经过次数。
- 树上所有点距离和。

什么时候用：

- 输入确认是一棵无向树。
- 多个子树答案需要从父亲“换根”传给儿子。
- 多次路径修改后统一统计。
- 想把树题从暴力 DFS 升级到 `O(n)` 或 `O((n+q)logn)`。

不要什么时候用：

- 一般图有环不能直接用树直径/树差分。
- 动态树加删边不是本模块。
- 路径上需要在线查询最值/修改，可能转树链剖分，低优先级。
- 换根 DP 的转移因题而异，本模块给最典型的“距离和”模型。

复杂度：

- 树直径：`O(n)`。
- 换根求每点到所有点距离和：`O(n)`。
- 树上差分：`O((n+q)logn + n)`，瓶颈是 LCA。

数据范围参考：

- `n,q <= 2e5` 常规可用。
- 边权距离和可能超过 `int`，使用 `ll`。

依赖的标准容器：

- 标准 `Graph`。
- `TreeInfo` 可辅助父亲、深度、DFS 序。
- `LCA` 用于树上差分。

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

```cpp
pair<int, ll> farthest_from(const Graph& T, int s);
ll tree_diameter_length(const Graph& T);
vector<ll> sum_distance_all_roots(const Graph& T, int root);
vector<ll> vertex_path_counts(const Graph& T, const vector<pair<int,int>>& queries, const LCA& lca);
vector<ll> edge_path_counts_by_child(const Graph& T, const vector<pair<int,int>>& queries, const LCA& lca);
```

输出能力：

- 树直径长度。
- 每个点到所有点的距离和。
- 多次路径后每个点/每条父子边被经过的次数。

下游可接：

- LCA。
- TreeInfo。
- 树状数组/SegmentTree 子树查询。
- 树形 DP。

可拼接模块：

- `Graph(Tree) + farthest twice`。
- `TreeInfo + reroot DP`。
- `LCA + tree difference + postorder accumulation`。

模板代码：

```cpp
pair<int, ll> farthest_from(const Graph &T, int s) {
    vector<ll> dist(T.n + 1, -1);
    queue<int> q;
    q.push(s);
    dist[s] = 0;
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        for (auto e : T.g[u]) {
            int v = e.to;
            if (dist[v] != -1) continue;
            dist[v] = dist[u] + e.w;
            q.push(v);
        }
    }

    int best = s;
    for (int i = 1; i <= T.n; i++) {
        if (dist[i] > dist[best]) best = i;
    }
    return {best, dist[best]};
}

ll tree_diameter_length(const Graph &T) {
    auto a = farthest_from(T, 1);
    auto b = farthest_from(T, a.first);
    return b.second;
}

vector<ll> sum_distance_all_roots(const Graph &T, int root = 1) {
    int n = T.n;
    vector<int> parent(n + 1, 0), sz(n + 1, 1), order;
    vector<ll> down(n + 1, 0), ans(n + 1, 0);

    queue<int> q;
    q.push(root);
    parent[root] = -1;
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        order.push_back(u);
        for (auto e : T.g[u]) {
            int v = e.to;
            if (v == parent[u]) continue;
            parent[v] = u;
            q.push(v);
        }
    }

    for (int i = (int)order.size() - 1; i >= 0; i--) {
        int u = order[i];
        sz[u] = 1;
        down[u] = 0;
        for (auto e : T.g[u]) {
            int v = e.to;
            if (parent[v] != u) continue;
            sz[u] += sz[v];
            down[u] += down[v] + (ll)sz[v] * e.w;
        }
    }

    ans[root] = down[root];
    for (int u : order) {
        for (auto e : T.g[u]) {
            int v = e.to;
            if (parent[v] != u) continue;
            ans[v] = ans[u] - (ll)sz[v] * e.w + (ll)(n - sz[v]) * e.w;
        }
    }
    return ans;
}
```

树上差分代码：

```cpp
vector<ll> vertex_path_counts(const Graph &T, const vector<pair<int, int>> &queries, const LCA &lca) {
    vector<ll> diff(T.n + 1, 0), cnt(T.n + 1, 0);
    vector<int> parent = lca.up[0];
    vector<int> order;
    queue<int> q;
    int root = lca.root;
    q.push(root);
    vector<int> vis(T.n + 1, 0);
    vis[root] = 1;
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        order.push_back(u);
        for (auto e : T.g[u]) {
            int v = e.to;
            if (vis[v]) continue;
            vis[v] = 1;
            q.push(v);
        }
    }

    for (auto [u, v] : queries) {
        int c = lca.query(u, v);
        diff[u]++;
        diff[v]++;
        diff[c]--;
        if (c != root) diff[parent[c]]--;
    }

    for (int i = (int)order.size() - 1; i >= 0; i--) {
        int u = order[i];
        cnt[u] += diff[u];
        if (u != root) cnt[parent[u]] += cnt[u];
    }
    return cnt;
}

vector<ll> edge_path_counts_by_child(const Graph &T, const vector<pair<int, int>> &queries, const LCA &lca) {
    vector<ll> diff(T.n + 1, 0), cnt(T.n + 1, 0);
    vector<int> parent = lca.up[0];
    vector<int> order;
    queue<int> q;
    int root = lca.root;
    q.push(root);
    vector<int> vis(T.n + 1, 0);
    vis[root] = 1;
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        order.push_back(u);
        for (auto e : T.g[u]) {
            int v = e.to;
            if (vis[v]) continue;
            vis[v] = 1;
            q.push(v);
        }
    }

    for (auto [u, v] : queries) {
        int c = lca.query(u, v);
        diff[u]++;
        diff[v]++;
        diff[c] -= 2;
    }

    for (int i = (int)order.size() - 1; i >= 0; i--) {
        int u = order[i];
        cnt[u] += diff[u];
        if (u != root) cnt[parent[u]] += cnt[u];
    }
    return cnt; // 边 parent[u]-u 被经过次数是 cnt[u]
}
```

调用示例：

```cpp
cout << tree_diameter_length(T) << '\n';

auto sumDist = sum_distance_all_roots(T, 1);
for (int u = 1; u <= n; u++) cout << sumDist[u] << '\n';

LCA lca;
lca.build(T, 1);
vector<pair<int, int>> qs = {{2, 5}, {3, 4}};
auto edgeCnt = edge_path_counts_by_child(T, qs, lca);
```

常见坑：

- 树直径在带权树上也可以两次最远点，但边权应非负；若有负权树，题意通常不是普通直径。
- `sum_distance_all_roots` 的换根公式中，边权 `w` 不能漏。
- 树上差分分“点被经过次数”和“边被经过次数”，扣 LCA 的方式不同。
- `edge_path_counts_by_child` 返回的是以子节点 `u` 标记父子边 `parent[u]-u`。
- LCA 必须和差分用同一个根。
- 根节点没有父边，不要输出 `cnt[root]` 当边答案。

暴力/部分分替代：

- 直径：从每个点 DFS 求最远，`O(n^2)` 小数据可过。
- 距离和：每个点跑一次 DFS/BFS，`O(n^2)`。
- 路径计数：每个询问 DFS 找路径逐点加，`O(nq)`。
- `q` 很小或 `n <= 2000`，暴力路径常能拿分。

升级方向：

- 单次路径 -> DFS。
- 多次路径距离 -> LCA。
- 多次路径批量统计 -> 树上差分。
- 每点作为根的答案 -> 换根 DP。
- 子树修改查询 -> DFS 序 + 树状数组/SegmentTree。

最小测试样例：

```text
5
1 2 1
1 3 1
2 4 1
2 5 1
直径长度 3，例如 4-2-1-3
路径 4-3 的边计数：4-2,2-1,1-3 各加 1
```
