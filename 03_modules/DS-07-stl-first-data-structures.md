# DS-07 STL 优先的数据结构策略

模块编号：DS-07

模块名称：STL 优先的数据结构策略

标签：[数据结构][STL][priority_queue][unordered_map][set][静态数组][考试速写]

一句话用途：明确哪些数据结构考场上直接用 STL，哪些才需要手写模板，并整理速度写法、比较器、哈希表和 `noexcept` 的常见坑。

题面触发词：

- 堆、优先队列、每次取最小/最大。
- 队列、栈、双端队列。
- 集合、映射、计数、前驱后继。
- 哈希表、状态缓存、字符串计数。
- 需要快速编码，不想手写复杂容器。

什么时候用：

- 需要的容器行为 STL 已经直接支持。
- 算法核心不在容器实现，而在建模、转移、遍历。
- 想减少手写代码量和 bug 面。

不要什么时候用：

- 需要区间和/区间最值/区间修改，STL 容器不直接支持，转 树状数组/SegmentTree。
- 需要第 k 小/动态排名，普通 `set` 不够，转坐标压缩 + 树状数组。
- 需要堆中任意删除或修改 key，普通 `priority_queue` 不支持，常用“懒删除”或改用 `set`。
- 哈希表被卡或需要稳定最坏复杂度时，优先 `map/set`。

复杂度：

- 全局静态数组随机访问 `O(1)`，常数小，适合题目给定上限的数组/DP 表。
- `vector` 随机访问 `O(1)`，尾插均摊 `O(1)`，适合规模运行时才知道或需要动态增长的序列。
- `queue/stack/deque` 常用端点操作 `O(1)`。
- `priority_queue` `push/pop O(log n)`，`top O(1)`。
- `set/map/multiset` 插入删除查找 `O(log n)`。
- `unordered_map/unordered_set` 平均 `O(1)`，最坏可能退化。

数据范围参考：

- 上限明确：数组、DP 表、距离表优先全局静态数组。
- `n <= 2e5`：`priority_queue/set/map/unordered_map` 这类 STL 行为容器通常稳。
- `n >= 1e6`：少用 `map`；哈希表要 `reserve`；线性表优先静态数组。
- 状态数明确且范围小：优先数组 memo，不要用 map。

依赖的标准容器：

- 全局静态数组。
- `vector`、`array`、`string`。
- `queue`、`stack`、`deque`、`priority_queue`。
- `set`、`multiset`、`map`、`unordered_map`、`unordered_set`。

输入如何整理：

```cpp
const int MAXN = 200000 + 5;
ll a[MAXN];               // 1-index 数组，题目给上限时优先这样写
queue<int> q;             // BFS
deque<int> dq;            // 单调队列 / 0-1 BFS
priority_queue<pair<ll,int>, vector<pair<ll,int>>, greater<pair<ll,int>>> pq; // Dijkstra
unordered_map<long long, int> mp; // 编码状态计数
```

接口：

```text
static array: a[1..n], dp[1..n][...]
vector: reserve, resize, assign, push_back, pop_back, back
priority_queue: push, top, pop, empty
set/map: insert, erase, find, count, lower_bound, upper_bound
unordered_map: reserve, max_load_factor, find, count, operator[]
```

输出能力：

- 堆顶最大/最小。
- 当前有序集合前驱后继。
- key 到计数/答案的映射。
- BFS/DFS/DP 状态容器。

下游可接：

- Dijkstra、Kruskal、Topo、BFS。
- 记忆化搜索。
- 贪心、扫描线、离线处理。
- 坐标压缩 + 树状数组。

可拼接模块：

| 需求 | 优先 STL | 什么时候换手写/专门结构 |
|---|---|---|
| 数组、DP 表、距离矩阵 | 全局静态数组 | 上限不清楚或必须动态增长才用 `vector` |
| 邻接表 | 优先标准 `Graph`；短题可写 `vector<pair<int,ll>> g[MAXN]` | 不需要 `edges/input_id` 时才用临时静态邻接表 |
| BFS | `queue` | 双端权值 0/1 转 `deque` |
| 0-1 BFS / 单调队列 | `deque` | 无 |
| 每次取最小/最大 | `priority_queue` | 要任意删除改 `set` 或懒删除 |
| 前驱后继、有序去重 | `set/multiset` | 要排名转 树状数组 |
| key-value 映射 | `map/unordered_map` | key 范围小转 vector |
| 字符串 | `string` | 多模式匹配转 Trie/AC |

模板代码：

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

struct Node {
    ll dist;
    int id;
};

struct NodeCmp {
    bool operator()(const Node &a, const Node &b) const noexcept {
        if (a.dist != b.dist) return a.dist > b.dist; // 小 dist 优先
        return a.id > b.id;
    }
};

struct PairHash {
    size_t operator()(const pair<int, int> &p) const noexcept {
        return ((uint64_t)(unsigned)p.first << 32) ^ (unsigned)p.second;
    }
};

const int MAXN = 200000 + 5;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;

    static int a[MAXN];
    for (int i = 1; i <= n; i++) cin >> a[i];

    priority_queue<Node, vector<Node>, NodeCmp> pq;
    pq.push({0, 1});

    unordered_map<pair<int, int>, int, PairHash> memo;
    memo.max_load_factor(0.7);
    memo.reserve(n * 2 + 1);

    return 0;
}
```

调用示例：

```cpp
// 堆不能删除旧状态：用懒删除
while (!pq.empty()) {
    auto cur = pq.top();
    pq.pop();
    if (cur.dist != dist[cur.id]) continue;
}

// unordered_map 判断存在，不要用 mp[key] 误创建
auto it = memo.find({x, y});
if (it != memo.end()) {
    cout << it->second << '\n';
}
```

常见坑：

- `reserve(n)` 只预留容量，不改变 `size()`，不能直接 `a[i]`。
- 访问 `front/back/top` 前必须 `empty()` 检查。
- `priority_queue` 默认最大堆；小根堆用 `greater<pair<...>>` 或自定义比较器。
- `priority_queue` 的比较器含义是“谁优先级更低返回 true”，写反很常见。
- `sort` 比较函数必须是严格弱序，不能写 `<=`。
- `unordered_map` 没有顺序，也没有 `lower_bound`。
- `mp[key]` 会创建默认值；只查存在用 `find/count`。
- `multiset.erase(x)` 会删掉所有 `x`；只删一个要先 `find`，存在再 `erase(it)`。
- `noexcept` 不是必须，但简单的自定义 hash / comparator 可以加；不要为了加 `noexcept` 写复杂代码。真正重要的是比较器不抛异常、不修改外部状态、逻辑稳定。

暴力/部分分替代：

- 小数据每次线性扫描找最小/最大，先替代堆。
- 小数据用 `vector<pair<K,V>>` 扫描查 key，先替代 map。
- 需要排名但不会树状数组时，先 `vector` 排序重算拿部分分。

升级方向：

- `vector` 扫描 -> `priority_queue/set/map`。
- `map` 状态缓存 -> 数组 memo 或编码后 `unordered_map`。
- `set` 排名需求 -> Compressor + 树状数组。
- `priority_queue` 任意删除需求 -> 懒删除 / `multiset`。

最小测试样例：

```text
堆：push 3,1,2，小根堆 top=1
哈希：memo[{1,2}]=5 后 find({1,2}) 存在
multiset：插入 5,5，find 后 erase 一个迭代器，还剩一个 5
```
