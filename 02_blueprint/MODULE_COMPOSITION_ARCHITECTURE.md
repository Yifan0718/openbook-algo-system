# 模块化拼接顶层架构 v0.1

## 1. 核心判断

用户提出的“所有图论算法尽量使用统一建图方式”是正确方向，而且应该扩展到整套资料：

不是每个算法各写一套输入和容器，而是建立一层“统一接口层”。

最终资料应按下面四层组织：

```text
题面原始输入
  -> 输入整理层：把题目转成标准容器
  -> 统一接口层：Graph / Array / Queries / State / Math
  -> 算法模块层：BFS, Dijkstra, 树状数组, DP, DFS, ...
  -> 输出与提交层：部分分版本 / 正解版本 / 合法兜底
```

这样考场动作变成：

1. 判断题型。
2. 选标准容器。
3. 把输入整理成标准容器。
4. 从资料中抄算法模块。
5. 按统一接口调用。
6. 先交部分分，再替换或叠加升级模块。

## 2. 全资料统一约定

### 2.1 索引

默认：

- 图：1-index，点编号 `1..n`。
- 数组：1-index，`vector<ll> a(n + 1)`，`a[0]` 不用。
- 区间：闭区间 `[l, r]`。
- 查询：离线查询统一保存 `l, r, id`。
- 字符串：使用 C++ `string` 的自然 0-index，但模块开头必须醒目标注。
- 网格：默认 1-index，`1..n, 1..m`，需要转图时使用 `id(i, j)`。

为什么这样：

- 图题和区间题在国内 OJ 中更常见 1-index。
- 纸质资料要降低切换成本，宁可在字符串模块单独提醒 0-index。

### 2.2 类型

统一放在主骨架：

```cpp
using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

const int INF = 1e9;
const ll LINF = 4'000'000'000'000'000'000LL;
```

模块中的 `LINF` 默认依赖这份主骨架；不要在子模块里再改成 `(1LL << 60)` 等其他语义。

默认策略：

- 点编号、下标、数量用 `int`。
- 权值、距离、答案、方案数优先用 `long long`。
- 不使用 `#define int long long`。

### 2.3 模块接口命名

所有类尽量使用同一组动词：

- `init(...)`：重新初始化。
- `build(...)`：从数组/图构建。
- `add(...)`：单点增量。
- `add_undirected(...) / add_directed(...)`：图中加边，考场不使用布尔参数接口。
- `setv(...)`：单点赋值，避免和 `std::set` 混淆。
- `range_add(l, r, val)`：闭区间加。
- `query(l, r)`：闭区间查询。
- `sum(l, r)`：区间和。
- `prefix(pos)`：前缀查询 `[1, pos]`。
- `at(pos)`：单点查询。
- `solve_xxx(...)`：算法主函数。

所有算法函数尽量返回结果，而不是直接输出。

这样便于：

- 暴力版本和优化版本共用同一个 `solve()` 外壳。
- 一道题可以先调用 `solve_bruteforce()`，再替换为 `solve_dp()`。

## 3. 统一 Graph 设计

### 3.1 目标

同一个建图方式尽量服务：

- DFS/BFS。
- Dijkstra。
- Bellman-Ford。
- Floyd 初始化。
- 拓扑排序。
- SCC。
- Kruskal。
- LCA/树上 DFS。
- 二分图染色。

不强行服务：

- Dinic/最小费用流：需要残量网络，单独 `FlowGraph`。
- 特殊高性能图：例如极限内存的链式前向星，作为补充版。

### 3.2 推荐标准 Graph

```cpp
struct AdjEdge {
    int to;
    ll w;
    int edge_index; // 内部边下标，只给模板内部用
    bool directed;
    int input_id;   // 对外边号，1-index
};

struct FullEdge {
    int from, to;
    ll w;
    bool directed;
    int input_id;
};

struct Graph {
    int n;
    vector<vector<AdjEdge>> g; // 从点出发：BFS/Dijkstra/DFS/Topo/SCC/LCA
    vector<FullEdge> edges;    // 逻辑边表：Kruskal/Floyd/Bellman-Ford/全边排序

    Graph(int n = 0) {
        init(n);
    }

    void init(int n_) {
        n = n_;
        g.assign(n + 1, {});
        edges.clear();
    }

    void add_edge_raw(int u, int v, ll w, bool directed) {
        int edge_index = (int)edges.size();
        int input_id = edge_index + 1;
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

这份 `Graph` 是默认纸质版。它不追求最短，但可读、可抄、可拼：

- 邻接遍历统一写法：`for (auto e : G.g[u]) { int v = e.to; ll w = e.w; }`
- Kruskal 不会因为无向图双向边而重复：遍历 `G.edges`。
- Dijkstra/BFS/SCC/LCA 直接遍历 `G.g[u]`。
- Bellman-Ford 可遍历 `G.edges`，遇到无向边时手动松弛两个方向。
- Floyd 可用 `G.edges` 初始化矩阵，并根据 `e.directed` 决定是否对称赋值。

读入标准写法：

```cpp
int n, m;
cin >> n >> m;

Graph G(n);
for (int i = 1; i <= m; i++) {
    int u, v;
    ll w;
    cin >> u >> v >> w;
    G.add_undirected(u, v, w); // 无向图
    // G.add_directed(u, v, w); // 有向图
}
```

无权图：

```cpp
int u, v;
cin >> u >> v;
G.add_undirected(u, v);    // 无向无权
// G.add_directed(u, v);    // 有向无权
```

### 3.3 图算法统一调用形态

#### BFS 无权最短路

```cpp
vector<int> dist = bfs_unweighted(G, 1);
```

模块内部统一遍历：

```cpp
for (auto e : G.g[u]) {
    int v = e.to;
}
```

#### Dijkstra 非负权最短路

```cpp
vector<ll> dist = dijkstra(G, 1);
```

模块内部统一遍历：

```cpp
for (auto e : G.g[u]) {
    int v = e.to;
    ll w = e.w;
}
```

#### Kruskal

```cpp
auto mst = kruskal(G);
if (mst.connected) cout << mst.total << "\n";
```

模块内部只用：

```cpp
vector<FullEdge> es = G.edges;
sort(es.begin(), es.end(), [](const FullEdge &a, const FullEdge &b) {
    return a.w < b.w;
});
```

#### Floyd

```cpp
floyd(G); // 结果在全局 floyd_dist[u][v]
```

初始化时：

```cpp
for (const FullEdge &e : G.edges) {
    dist[e.from][e.to] = min(dist[e.from][e.to], e.w);
    if (!e.directed) dist[e.to][e.from] = min(dist[e.to][e.from], e.w);
}
```

#### 拓扑排序

```cpp
vector<int> order = topo_sort(G);
```

只适用于有向图。入度可以从 `G.g` 或 `G.edges` 统计，推荐从 `G.edges` 统计并检查边的方向：

```cpp
for (const FullEdge &e : G.edges) {
    if (!e.directed) continue;
    indeg[e.to]++;
}
```

`topo_sort(G)` 只吃 `G.add_directed(u, v)` 建出的有向边；如果题目是无向图，不能直接套拓扑排序。

#### LCA/树上 DP

```cpp
LCA lca;
lca.build(G, 1);
int x = lca.query(u, v);
```

要求：

- 建边时使用 `G.add_undirected(u, v)`。
- 输入是一棵树或森林中指定根的树。

### 3.4 图模块的“不要统一”边界

以下内容保留独立模板，不强塞进标准 `Graph`：

1. 最大流/费用流：
   - 需要反向边和残量边。
   - 使用 `FlowGraph`，主接口使用 `add_edge(u, v, cap)`，并可保留 `addEdge(u, v, cap)` 包装别名兼容旧模板。

2. 极限内存链式前向星：
   - 作为低优先级补充。
   - 只在 `n,m` 特别大或 `vector<vector<int>>` 内存风险明显时使用。

3. 网格 BFS：
   - 默认直接用二维数组和方向数组。
   - 只有需要套图算法时才转成 `Graph`。

4. Floyd：
   - 算法核心是矩阵，标准 `Graph` 只负责初始化。

## 4. 统一数组/区间数据结构设计

### 4.1 标准数组形态

```cpp
int n;
vector<ll> a(n + 1);
for (int i = 1; i <= n; i++) cin >> a[i];
```

所有区间 `[l, r]` 都是闭区间。

### 4.2 PrefixSum

```cpp
struct PrefixSum {
    int n;
    vector<ll> pre;

    void build(const vector<ll> &a) {
        n = (int)a.size() - 1;
        pre.assign(n + 1, 0);
        for (int i = 1; i <= n; i++) pre[i] = pre[i - 1] + a[i];
    }

    ll prefix(int pos) {
        if (pos <= 0) return 0;
        if (pos > n) pos = n;
        return pre[pos];
    }

    ll query(int l, int r) {
        if (l > r) return 0;
        return prefix(r) - prefix(l - 1);
    }
};
```

统一调用：

```cpp
PrefixSum ps;
ps.build(a);
cout << ps.query(l, r) << "\n";
```

### 4.3 树状数组

```cpp
struct BIT {
    int n;
    vector<ll> bit;

    void init(int n_) {
        n = n_;
        bit.assign(n + 1, 0);
    }

    void add(int pos, ll val) {
        if (pos <= 0 || pos > n) return;
        for (; pos <= n; pos += pos & -pos) bit[pos] += val;
    }

    void build(const vector<ll> &a) {
        init((int)a.size() - 1);
        for (int i = 1; i <= n; i++) add(i, a[i]);
    }

    ll prefix(int pos) {
        if (pos <= 0) return 0;
        if (pos > n) pos = n;
        ll res = 0;
        for (; pos > 0; pos -= pos & -pos) res += bit[pos];
        return res;
    }

    ll query(int l, int r) {
        if (l > r) return 0;
        return prefix(r) - prefix(l - 1);
    }

    ll at(int pos) {
        return query(pos, pos);
    }
};
```

统一调用：

```cpp
BIT fw;
fw.init(n);
fw.add(pos, delta);
ll ans = fw.query(l, r);
```

### 4.4 SegmentTree

线段树至少准备两个接口一致的版本：

1. `SegTreePoint`
   - 单点修改。
   - 区间查询。
   - 标准实现名保留 `SegTreeSum`，通用别名 `using SegmentTree = SegTreeSum;`。

2. `SegTreeLazy`
   - 区间加。
   - 区间查询。
   - 标准实现名保留 `LazySegTreeSum`，通用别名 `using LazySegmentTree = LazySegTreeSum;`。

统一命名：

```cpp
build(a);
add(pos, delta);
setv(pos, value);
range_add(l, r, delta);
query(l, r);
```

动态 max/min 的单点线段树不另开新接口，只替换 `merge` 和 `neutral`：

```cpp
// max: neutral = -LINF, merge(a, b) = max(a, b)
// min: neutral = LINF, merge(a, b) = min(a, b)
```

### 4.5 SparseTable

静态 RMQ：

```cpp
SparseTable st;
st.build(a);
ll ans = st.query(l, r);
```

注意：

- `query(l, r)` 仍然使用闭区间。
- 操作必须满足可重叠合并，例如 min/max/gcd。
- 区间和不要用 Sparse Table，优先前缀和。

### 4.6 CoordinateCompression

```cpp
struct Compressor {
    vector<ll> xs;

    void build(vector<ll> v) {
        xs = v;
        sort(xs.begin(), xs.end());
        xs.erase(unique(xs.begin(), xs.end()), xs.end());
    }

    int id(ll x) {
        return lower_bound(xs.begin(), xs.end(), x) - xs.begin() + 1;
    }

    int lower_id(ll x) {
        return lower_bound(xs.begin(), xs.end(), x) - xs.begin() + 1;
    }

    int upper_id(ll x) {
        return upper_bound(xs.begin(), xs.end(), x) - xs.begin();
    }

    ll val(int pos) {
        return xs[pos - 1];
    }

    int size() {
        return (int)xs.size();
    }
};
```

统一约定：

- 压缩后编号也从 1 开始。
- 便于直接接 树状数组/SegmentTree。
- 如果 `x` 一定出现在坐标表中，用 `id(x)`。
- 如果查询原坐标范围 `[L, R]`，用 `lower_id(L)` 和 `upper_id(R)`，不要直接假设 `L/R` 出现过。

常见拼接：

```text
值域很大 + 动态排名/逆序对
  -> Compressor
  -> 树状数组

区间离散化 + 区间覆盖
  -> Compressor
  -> Difference/树状数组/SegmentTree
```

## 5. 暴力、记忆化、DP 的统一升级结构

每道题尽量按三层写：

```cpp
void readInput() {
    // 只读入并整理标准容器，不写算法
}

ll solve_bruteforce() {
    // 小数据精确解
}

ll solve_memo() {
    // 暴力 DFS + 记忆化
}

ll solve_optimized() {
    // DP / 图论 / 数据结构正解
}

void solve() {
    readInput();

    if (can_bruteforce()) {
        cout << solve_bruteforce() << "\n";
        return;
    }

    if (can_memo()) {
        cout << solve_memo() << "\n";
        return;
    }

    cout << solve_optimized() << "\n";
}
```

考场上不一定三个都写全，但纸质资料统一这样呈现，有两个收益：

- 先交部分分版本不会浪费，后续只替换 `solve_optimized()`。
- DP 资料能明确展示“暴力递归如何变成记忆化/表推”。

## 6. 统一状态编码

### 6.1 优先级

状态存储优先级：

1. 边界明确、小整数：
   - 用 `vector` / 多维 `vector`，最快。

2. 状态含 `mask`：
   - 用 `vector<ll> dp(1 << n)` 或 `vector<vector<ll>>`。

3. 状态维度复杂但数量不大：
   - 用 `map<tuple<...>, ll>`，最稳，纸质上最不容易错。

4. 状态需要性能：
   - 用 `unordered_map<long long, ll>` 加 `encode(...)`。

### 6.2 纸质模板默认

弱基础优先稳：

```cpp
map<tuple<int, int, int>, ll> memo;

ll dfs(int i, int j, int s) {
    auto key = make_tuple(i, j, s);
    if (memo.count(key)) return memo[key];

    if (i == n + 1) return memo[key] = 0; // base case 按题意替换

    ll ans = LINF;
    // try choices
    return memo[key] = ans;
}
```

性能升级版另给：

```cpp
unordered_map<long long, ll> memo;

long long encode(int a, int b, int c) {
    return ((long long)a << 42) ^ ((long long)b << 21) ^ c;
}
```

必须提醒：

- 位移编码要求每一维范围已知且不会超过位数。
- 不确定时用 `map<tuple<...>>`，慢一点但稳。

## 7. 模块拼接食谱

资料中应新增“拼接食谱”页，而不是只列模板。

### 7.1 图论拼接

```text
最短路 + 路径恢复
  -> Graph
  -> Dijkstra 返回 dist + pre
  -> restore_path(pre, s, t)

最小生成树 + 连通性
  -> Graph.edges
  -> DSU
  -> Kruskal

DAG 依赖 + DP
  -> Graph G(n)
  -> G.add_directed(u, v, w)
  -> topo_sort
  -> 按拓扑序转移 dp[v]

树上路径查询
  -> Graph T(n)
  -> T.add_undirected(u, v, w)
  -> LCA.build(T, root)
  -> depth/distRoot
```

### 7.2 数据结构拼接

```text
区间和静态查询
  -> PrefixSum

单点修改 + 区间和
  -> 树状数组

区间加 + 单点查询
  -> Difference 或 树状数组差分

区间加 + 区间和
  -> Lazy Segment Tree

值域大 + 需要排名
  -> Compressor
  -> 树状数组/SegmentTree

静态区间 min/max/gcd
  -> SparseTable
```

### 7.3 暴力到正解拼接

```text
n <= 20
  -> DFS/子集枚举/状压 DP

n <= 40
  -> 折半枚举

重复状态明显
  -> 暴力 DFS
  -> 加 memo
  -> 如果状态边界清晰，再改表推 DP

有区间查询瓶颈
  -> 先 O(n^2) 暴力
  -> 加 PrefixSum/树状数组/SegmentTree 优化查询
```

## 8. 对原执行计划的微调

应在原计划中新增一项核心交付：

```text
第 -1 卷 / 或第 0 卷前置页：统一接口与拼接规范
```

内容包括：

- 全局 C++ 类型和索引约定。
- 标准 `Graph`。
- 标准数组/区间容器。
- 标准查询结构。
- 标准状态编码。
- 模块拼接食谱。

每个算法模块也需要新增字段：

```text
依赖的标准容器：
可拼接模块：
```

例如 Dijkstra：

```text
依赖的标准容器：Graph
可拼接模块：路径恢复、二分答案、树上最短路特判、状态最短路
```

例如 树状数组：

```text
依赖的标准容器：1-index vector / Compressor
可拼接模块：逆序对、动态排名、离线查询、扫描线
```

## 9. 总结

这套资料要从“模板大全”升级为“标准容器 + 模块算法 + 拼接食谱”。

关键不是每个算法代码最短，而是：

- 输入整理方式统一。
- 模块接口统一。
- 索引和区间统一。
- 暴力、记忆化、正解版本能共用外壳。
- 低频高级算法不要污染高频接口层。

这样才能让弱基础考生在考场上真正执行：

```text
看题 -> 转标准形 -> 找模块 -> 拼接 -> 先交 -> 升级
```
