# OPS-00 第 -1 卷：统一接口与标准容器

模块编号：OPS-00

模块名称：第 -1 卷 统一接口与标准容器

标签：前置卷、接口协议、标准容器、C++17、考场装配

一句话用途：把题面输入整理成统一形状，让后面的图论、数据结构、DP、暴力模块可以直接拼上去。

题面触发词：任意题目开写前都先看本卷。

什么时候用：每道题开始前，用本卷确定索引、类型、容器、函数名和模块调用外壳。

不要什么时候用：不要把本卷当算法教材；它只规定“零件接口”，不解释算法原理。

复杂度：本卷本身没有算法复杂度；复杂度由下游模块决定。

数据范围参考：所有规模都适用，尤其适合需要快速拼接多个模块的题。

依赖的标准容器：无。

输入如何整理：先读题面原始输入，再转为 1-index 全局数组、`Graph`、`Query`、`State`、`Compressor`。

接口：`init/build/add/add_edge/setv/range_add/query/prefix/at/solve_xxx`。

输出能力：提供统一外壳和下游模块调用约定。

下游可接：PrefixSum、树状数组、SegmentTree、DSU、BFS、Dijkstra、Topo、DP、DFS memo。

可拼接模块：所有模块。

模板代码：见本文件各协议代码块。

调用示例：见各协议的“考场抄法”。

常见坑：混用 0-index/1-index、区间半开半闭、图边重复、把 `int` 当距离、函数直接输出导致无法升级。

暴力/部分分替代：统一保留 `solve_bruteforce()`，先拿小数据分，再替换 `solve_optimized()`。

升级方向：把暴力外壳升级为 memo、DP、图论或数据结构正解，但输入整理层不改。

最小测试样例：每个模块接入后都测单点、边界、空结果、重复元素、极值。

## 0. 考场使用顺序

```text
1. 读题，圈出 n/m/q、是否有修改、是否是图/树/区间/状态。
2. 按本卷确定标准容器：Graph / Array / Query / State。
3. 把输入只整理一次，不在算法里边读边算。
4. 先写 solve_bruteforce() 或最简单合法版本。
5. 再把核心函数替换成正解模块。
6. 提交前只检查接口契约：索引、区间、类型、方向、初始化。
```

## 1. 全局 C++17 骨架

每份代码开头统一抄这一段。不要加考试环境不一定支持的优化开关。

如果现场 GNU g++ 支持 `bits/stdc++.h`，直接用短版。若不支持，把第一行替换成 `CPP-001` 的“标准头文件安全包”，不要现场逐个猜缺哪个头。

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

const int INF = 1000000000;
const ll LINF = 4'000'000'000'000'000'000LL;
const ll MOD = 1000000007LL; // 题目给别的模数就改这里

void solve() {
    // write here
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    solve();
    return 0;
}
```

硬规则：

| 项目 | 统一约定 |
|---|---|
| C++ 标准 | C++17 |
| 禁止 | `#pragma GCC optimize`、`freopen`、文件 IO、`#define int long long` |
| 点编号 | 默认 `1..n` |
| 数组/DP 表 | 默认 1-index；上限明确时优先全局静态数组 `a[MAXN]` / `dp[MAXN][MAXM]` |
| 区间 | 默认闭区间 `[l, r]` |
| 字符串 | 默认 C++ 自然 0-index，进入字符串模块时单独提醒 |
| 网格 | 默认 `1..n, 1..m`，转图时用 `id(i, j)` |
| 权值/距离/答案 | 优先 `long long` |
| 数量/下标 | 一般 `int` |

数组选择口令：

```text
题目给明确上限：优先全局静态数组，编号 1..n，防御性多开 5~10。
输入规模不固定或需要可变长度：再用 vector，并主动开 n+1 保持 1-index。
字符串、queue、deque、priority_queue、set/map、unordered_map 这类容器行为：直接用 STL。
集合状压的 mask 数值必须从 0 枚举，但业务对象编号仍写 1..k，取位统一写 i-1。
```

## 2. 函数命名规范

统一动词让模块能替换。

| 函数名 | 用途 | 例子 |
|---|---|---|
| `init(...)` | 清空并重新初始化 | `fw.init(n)`、`G.init(n)` |
| `build(...)` | 从已有数组/图建立结构 | `ps.build(a)`、`st.build(a)` |
| `add(pos, val)` | 单点增加 | 树状数组单点加 |
| `add_undirected/add_directed` | 图加边 | `G.add_undirected(u, v, w)` |
| `setv(pos, value)` | 单点赋值 | 线段树点赋值，避免撞 `std::set` |
| `range_add(l, r, val)` | 闭区间加 | Lazy Segment Tree |
| `query(l, r)` | 闭区间查询 | 和/最值/gcd |
| `prefix(pos)` | 查询 `[1, pos]` | 前缀和、树状数组 |
| `at(pos)` | 单点查询 | 差分树状数组 |
| `solve_bruteforce()` | 小数据精确版 | 部分分 |
| `solve_memo()` | 记忆化版 | 从 DFS 升级 |
| `solve_optimized()` | 正解版 | DP/图论/数据结构 |

接口原则：

```text
算法函数尽量返回结果，不直接 cout。
solve() 负责读入、选择版本、输出。
```

标准外壳：

```cpp
void read_input() {
    // 只读入并整理成标准容器
}

ll solve_bruteforce() {
    // 小数据精确版
    return 0;
}

ll solve_optimized() {
    // 正解版
    return 0;
}

void solve() {
    read_input();
    cout << solve_optimized() << "\n";
}
```

## 3. Graph 协议

目标：一份建图同时服务 BFS、DFS、Dijkstra、Topo、Kruskal、Floyd、Bellman-Ford、LCA。

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
    int input_id;   // 对外边号，1-index
};

struct Graph {
    int n;
    vector<vector<AdjEdge>> g;
    vector<FullEdge> edges;

    Graph(int n = 0) { init(n); }

    void init(int n_) {
        n = n_;
        g.assign(n + 1, {});
        edges.clear();
    }

    void add_edge_raw(int u, int v, ll w, bool directed) {
        int edge_index = (int)edges.size(); // 内部 0-based，不输出
        int input_id = edge_index + 1;      // 题面边号 1-based
        edges.push_back({u, v, w, directed, input_id});
        g[u].push_back({v, w, edge_index, directed, input_id});
        if (!directed) g[v].push_back({u, w, edge_index, directed, input_id});
    }

    void add_undirected(int u, int v, ll w = 1) {
        add_edge_raw(u, v, w, false);
    }

    void add_directed(int u, int v, ll w = 1) {
        add_edge_raw(u, v, w, true);
    }
};
```

考场抄法：

```cpp
int n, m;
cin >> n >> m;
Graph G(n);
for (int i = 1; i <= m; i++) {
    int u, v;
    ll w;
    cin >> u >> v >> w;
    G.add_undirected(u, v, w); // 无向图
}
```

无权图：

```cpp
int u, v;
cin >> u >> v;
G.add_undirected(u, v);    // 无向无权，推荐写法
G.add_directed(u, v);      // 有向无权，推荐写法
```

Graph 的双视图：

| 视图 | 用途 | 遍历方式 |
|---|---|---|
| `G.g[u]` | BFS、DFS、Dijkstra、Topo、SCC、LCA | `for (auto e : G.g[u])` |
| `G.edges` | Kruskal、Floyd 初始化、Bellman-Ford、全边排序 | `for (auto e : G.edges)` |

Graph 接口坑位：

```text
1. Kruskal 只遍历 G.edges，不遍历 G.g，否则无向边会重复。
2. Bellman-Ford 遇到无向边要松弛两个方向。
3. Topo 只适用于 `G.add_directed(u, v)` 建出的有向边。
4. LCA/树 DP 要用无向边，并从根 DFS。
5. 最大流不要用 Graph，另用 FlowGraph。
6. 考场只写 add_undirected/add_directed，不直接调用 add_edge_raw。
7. 点编号默认 1-index；对外边号用 input_id，也是 1-index。edge_index 是内部跳父边用的下标，不输出。
```

## 4. Array 协议

标准读入：

```cpp
int n;
cin >> n;
vector<ll> a(n + 1);
for (int i = 1; i <= n; i++) cin >> a[i];
```

区间约定：

```text
所有区间都是闭区间 [l, r]。
空区间 l > r 时，查询类函数返回 0 或对应单位元。
```

静态前缀和协议：

```cpp
struct PrefixSum {
    int n;
    vector<ll> pre;

    void build(const vector<ll> &a) {
        n = (int)a.size() - 1;
        pre.assign(n + 1, 0);
        for (int i = 1; i <= n; i++) pre[i] = pre[i - 1] + a[i];
    }

    ll prefix(int pos) const {
        if (pos <= 0) return 0;
        if (pos > n) pos = n;
        return pre[pos];
    }

    ll query(int l, int r) const {
        if (l > r) return 0;
        return prefix(r) - prefix(l - 1);
    }
};
```

动态区间和协议：

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

    ll prefix(int pos) const {
        pos = min(pos, n);
        ll res = 0;
        for (; pos > 0; pos -= pos & -pos) res += bit[pos];
        return res;
    }

    ll query(int l, int r) const {
        if (l > r) return 0;
        return prefix(r) - prefix(l - 1);
    }

    ll at(int pos) const {
        return query(pos, pos);
    }
};
```

线段树统一接口先记名字，代码放数据结构卷：

```cpp
build(a);
add(pos, delta);
setv(pos, value);
range_add(l, r, delta);
query(l, r);
```

## 5. Query 协议

多次询问统一先存成 `Query`，不要把各种题写成各自的临时变量。

```cpp
struct Query {
    int l = 0, r = 0;
    int id = 0;
    int op = 0;   // 题目有操作类型时使用
    int pos = 0;  // 单点位置
    ll x = 0;     // 修改值、阈值、权值
};
```

常见读法：

```cpp
int q;
cin >> q;
vector<Query> qs(q + 1);
for (int i = 1; i <= q; i++) {
    cin >> qs[i].op >> qs[i].l >> qs[i].r;
    qs[i].id = i;
}
```

离线查询约定：

```text
id 保留原顺序。
排序只排序 Query 数组，不改答案数组。
答案统一放 ans[id]。
```

## 6. Compressor 协议

值域很大但实际出现的数不多时，先压缩再接 树状数组/SegmentTree。

```cpp
struct Compressor {
    vector<ll> xs;

    void build(vector<ll> v) {
        xs = v;
        sort(xs.begin(), xs.end());
        xs.erase(unique(xs.begin(), xs.end()), xs.end());
    }

    int id(ll x) const {
        return lower_bound(xs.begin(), xs.end(), x) - xs.begin() + 1;
    }

    int lower_id(ll x) const {
        return lower_bound(xs.begin(), xs.end(), x) - xs.begin() + 1;
    }

    int upper_id(ll x) const {
        return upper_bound(xs.begin(), xs.end(), x) - xs.begin();
    }

    ll val(int pos) const {
        return xs[pos - 1];
    }

    int size() const {
        return (int)xs.size();
    }
};
```

接法：

```cpp
vector<ll> all;
// 把所有 a[i]、查询里的 x、区间端点等需要比较的值放进 all
Compressor cp;
cp.build(all);

BIT fw;
fw.init(cp.size());
fw.add(cp.id(x), 1);
```

压缩坑位：

```text
1. 压缩后编号仍然从 1 开始。
2. x 一定出现过，用 id(x)。
3. 查询原坐标范围 [L, R]，用 lower_id(L), upper_id(R)。
4. lower_id(L) > upper_id(R) 表示范围内没有点。
```

## 7. State 协议

状态统一拆成三类：

```text
State = {进度, 资源, 记忆}
```

| 类别 | 常用变量名 | 例子 |
|---|---|---|
| 进度 | `i, pos, u, step` | 处理到第几个物品、当前点 |
| 资源 | `cap, k, rem, cost` | 剩余容量、次数、预算 |
| 记忆 | `mask, last, color, used` | 已访问集合、上一个点、颜色 |

纸质默认稳妥写法：

```cpp
map<tuple<int, int, int>, ll> memo;

ll dfs(int i, int cap, int mask) {
    if (i == n + 1) return 0; // base case 按题意替换
    auto key = make_tuple(i, cap, mask);
    if (memo.count(key)) return memo[key];

    ll ans = -LINF;
    // 枚举选择
    return memo[key] = ans;
}
```

边界清晰时换成数组：

```cpp
const int MAXN = 200000 + 5;
const int MAXW = 5000 + 5;
static ll dp[MAXN][MAXW];

for (int i = 0; i <= n; i++) {
    for (int j = 0; j <= W; j++) dp[i][j] = -LINF;
}
```

状态存储选择：

| 情况 | 容器 | 考场优先级 |
|---|---|---|
| 范围小且明确 | `vector` / 多维 `vector` | 最高 |
| 有集合访问 | `vector` + `mask` | 高 |
| 维度复杂但状态少 | `map<tuple<...>, ll>` | 最稳 |
| 需要速度且能编码 | `unordered_map<ll, ll>` | 升级 |

## 8. 模块契约卡

每个算法模块接入前，先在纸上补全这张卡。

```text
模块名：
输入依赖：
输出能力：
下游可接：
不能处理：
初始化顺序：
查询/更新接口：
复杂度：
最小测试：
```

例：Dijkstra

```text
输入依赖：Graph，非负边权，起点 s
输出能力：dist[i]
下游可接：路径恢复、最短路 DAG、计数 DP
不能处理：负权边
初始化顺序：建图 -> dist=LINF -> pq
查询/更新接口：vector<ll> dijkstra(const Graph& G, int s)
复杂度：O((n+m)logn)
最小测试：3 点链、不可达点、重边、起点到自己
```

## 9. 最小自检

每次拼完模块，提交前用 60 秒过这张表。

| 检查项 | 问自己 |
|---|---|
| 索引 | 输入是 0-index 还是 1-index？我有没有统一？ |
| 区间 | 所有 `[l, r]` 都是闭区间吗？ |
| 类型 | 距离、答案、乘法有没有用 `ll`？ |
| 初始化 | 多组数据时数组、图、memo 有没有清空？ |
| 图方向 | `directed` 写对了吗？ |
| 不可达 | `LINF` 会不会被拿去加法溢出？ |
| 排序 | 离线排序后答案有没有按 `id` 放回？ |
| 输出 | 每个查询都有输出吗？换行够吗？ |
