# DS-04 单调结构与并查集

模块编号：DS-04

模块名称：MonotonicStack、MonotonicQueue 与 DSU

拼接提醒：本模块和 `GRAPH-06` 都给了 DSU。考场拼接 Kruskal 时只保留一个 `struct DSU`，不要重复复制导致重定义。

标签：[数据结构][单调栈][单调队列][并查集]

一句话用途：单调栈找最近更大/更小，单调队列维护滑动窗口最值，并查集合并集合和查询连通性。

题面触发词：

- 最近更大、最近更小。
- 每个位置左边/右边第一个大于它的数。
- 滑动窗口最大值/最小值。
- 合并集合。
- 判断连通。
- 最小生成树。

什么时候用：

- 单调栈：每个元素进出栈一次，找附近第一个满足大小关系的位置。
- 单调队列：固定长度窗口或 DP 转移中只需要窗口最大/最小。
- DSU：只需要合并和查询集合，不需要删除。

不要什么时候用：

- 单调栈不适合任意区间查询。
- 单调队列要求窗口按顺序滑动。
- DSU 不支持普通删除边/拆集合。

复杂度：

- 单调栈/队列：`O(n)`。
- DSU：近似 `O(1)` 均摊。

数据范围参考：

- `n <= 1e6` 常用，注意数组内存。
- DSU 可用于 `n,m <= 2e5` 或更大。

依赖的标准容器：

- 1-index 数组。
- DSU 点编号 `1..n`。

输入如何整理：

```cpp
vector<ll> a(n + 1);
for (int i = 1; i <= n; i++) cin >> a[i];
```

接口：

```text
DSU: init(n), find(x), unite(a,b), same(a,b)
```

输出能力：

- 最近更大/更小位置。
- 每个滑动窗口最大/最小。
- 连通性。
- Kruskal 合并结果。

下游可接：

- 单调栈可接贡献统计。
- 单调队列可接 DP 优化。
- DSU 可接 Kruskal、连通块计数。

可拼接模块：

- `Graph.edges + DSU + Kruskal`。
- `DP + MonotonicQueue`。
- `Array + MonotonicStack`。

模板代码：

```cpp
// 每个 i 左侧最近的严格更大元素位置，不存在为 0
vector<int> previous_greater(const vector<ll> &a) {
    int n = (int)a.size() - 1;
    vector<int> ans(n + 1, 0);
    vector<int> st;
    for (int i = 1; i <= n; i++) {
        while (!st.empty() && a[st.back()] <= a[i]) st.pop_back();
        ans[i] = st.empty() ? 0 : st.back();
        st.push_back(i);
    }
    return ans;
}

// 滑动窗口最大值，窗口长度 k，返回每个右端点 i 的最大值，i>=k 有意义
vector<ll> sliding_window_max(const vector<ll> &a, int k) {
    int n = (int)a.size() - 1;
    vector<ll> ans(n + 1, 0);
    deque<int> dq;
    for (int i = 1; i <= n; i++) {
        while (!dq.empty() && dq.front() <= i - k) dq.pop_front();
        while (!dq.empty() && a[dq.back()] <= a[i]) dq.pop_back();
        dq.push_back(i);
        if (i >= k) ans[i] = a[dq.front()];
    }
    return ans;
}

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
```

调用示例：

```cpp
auto leftGreater = previous_greater(a);
auto winMax = sliding_window_max(a, k);

DSU dsu;
dsu.init(n);
dsu.unite(u, v);
cout << (dsu.same(x, y) ? "YES" : "NO") << "\n";
```

常见坑：

- 单调栈中 `<=` 和 `<` 决定严格/非严格。
- 单调队列要先弹出过期下标。
- 滑动窗口答案通常从 `i>=k` 才有效。
- DSU 必须 `init(n)`。
- DSU 不能处理删除。

暴力/部分分替代：

- 最近更大/更小可向左/右扫描，`O(n^2)`。
- 滑动窗口可每个窗口扫一遍。
- 连通性可每次 BFS/DFS。

升级方向：

- 暴力窗口 -> MonotonicQueue。
- 暴力最近元素 -> MonotonicStack。
- BFS 连通查询 -> DSU。

最小测试样例：

```text
a=[2,1,3]
previous_greater=[0,1,0]
k=2 sliding max=[-,2,3]
DSU unite(1,2), same(1,2)=true
```
