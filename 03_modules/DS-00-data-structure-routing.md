# DS-00 数据结构路由与接口总表

模块编号：DS-00

模块名称：数据结构路由与接口总表

标签：[数据结构][路由][拼接]

一句话用途：根据操作类型快速选择 PrefixSum、Difference、树状数组、SegmentTree、SparseTable、MonotonicStack、MonotonicQueue、DSU 或 Compressor。

题面触发词：

- 区间查询。
- 区间修改。
- 单点修改。
- 动态维护。
- 排名、逆序对。
- 合并集合、连通块。
- 滑动窗口最大/最小。
- 连续区间满足和/计数条件。
- 排序数组配对、两数之和、三数之和。
- 最近更大/更小。

什么时候用：

- 题目核心不是复杂推导，而是需要维护某种数据。
- 暴力每次扫描会超时。
- 操作可以归类为查询、修改、合并、统计。

不要什么时候用：

- 数据范围很小，直接暴力更快更稳。
- 题目关键在 DP/图论建模，数据结构只是辅助，此时先完成主模型。
- 动态需求不清楚时，不要一上来写最长的线段树。

复杂度：

- 按模块不同，从 `O(1)`、`O(log n)` 到 `O(n log n)` 预处理不等。

数据范围参考：

| 操作规模 | 暴力风险 | 优先模块 |
|---|---|---|
| `n,q <= 2000` | 暴力可能可过 | 先暴力或前缀和 |
| `n,q <= 2e5` | 每次扫描会 TLE | 树状数组 / SegmentTree |
| 值域大但点数少 | 数组开不下 | Compressor + 树状数组/SegmentTree |

依赖的标准容器：

- 1-index 数组：上限明确时优先全局静态数组 `a[MAXN]`；上限不清楚时才用 `vector<ll> a(n + 1)`。
- 闭区间：`[l, r]`。
- 坐标压缩后编号也从 1 开始。

输入如何整理：

```cpp
int n, q;
cin >> n >> q;
vector<ll> a(n + 1);
for (int i = 1; i <= n; i++) cin >> a[i];
```

接口：

```text
build(a)  // 本卷主模板默认接 1-index vector<ll>
init(n)
add(pos, val)
setv(pos, val)
range_add(l, r, val)
prefix(pos)
query(l, r)
at(pos)
```

考场常数优先口径：

```text
本卷为了拼接统一，很多接口写成 build(vector<ll>& a)。
如果题目上限明确、你想直接用全局静态数组，可以把 build(a) 改成 build(n, a)，内部仍按 1..n 循环。
核心不变：数组和查询全部保持 1-index、闭区间 [l,r]。
```

输出能力：

- 静态区间和、动态区间和、区间最值、滑动窗口最值、连通性、排名统计等。

下游可接：

- DP 优化。
- 扫描线。
- 逆序对。
- 动态排名。
- Kruskal。
- 二分答案。

可拼接模块：

| 题面操作 | 模块组合 |
|---|---|
| 静态区间和 | `Array + PrefixSum` |
| 静态区间最值 | `Array + SparseTable` |
| 单点加 + 区间和 | `树状数组` |
| 区间加 + 最终还原 | `Difference` |
| 区间加 + 单点查 | `差分树状数组` |
| 区间加 + 区间和 | `双树状数组` 或 `LazySegmentTree` |
| 动态区间 min/max | `SegmentTree` |
| 值域很大 | `Compressor + 树状数组/SegmentTree` |
| 逆序对 | `Compressor + 树状数组` |
| 连通性/合并 | `DSU` |
| 最小生成树 | `Graph.edges + DSU + Kruskal` |
| 滑动窗口最值 | `MonotonicQueue` |
| 连续区间和/计数满足条件 | `TwoPointers / SlidingWindow` |
| 排序数组配对 | `TwoPointers` |
| 最近更大/更小 | `MonotonicStack` |

模板代码：

```cpp
// 数据结构选择口诀：
// 不修改区间和 -> PrefixSum
// 单点改区间和 -> 树状数组（代码类名 BIT）
// 区间改最终一次输出 -> Difference
// 区间改区间查 -> LazySegmentTree / 双树状数组（代码类名 RangeBIT）
// 静态最值 -> SparseTable
// 动态最值 -> SegmentTree
// 值域大 -> Compressor first
// 合并集合 -> DSU
```

调用示例：

```cpp
// 静态区间和
PrefixSum ps;
ps.build(a);
cout << ps.query(l, r) << "\n";

// 单点加，区间和
BIT fw;
fw.build(a);
fw.add(pos, delta);
cout << fw.query(l, r) << "\n";
```

常见坑：

- 树状数组下标不能为 0。
- 坐标范围查询不要直接用 `id(L)` 和 `id(R)`，应使用 `lower_id`/`upper_id`。
- 前缀和不支持修改。
- SparseTable 不支持修改，且只适合 min/max/gcd 这类可重叠查询。
- 区间 `[l, r]` 必须统一为闭区间。

暴力/部分分替代：

- 静态查询可每次循环求和，`O(nq)`，小数据可过。
- 动态修改可直接维护数组并每次扫描，先拿小数据。
- 合并集合可 BFS/DFS 查连通，小数据可过。

升级方向：

- 暴力扫描 -> PrefixSum/树状数组。
- 离散大值域 -> Compressor。
- 树状数组不够表达复杂区间最值 -> SegmentTree。
- 普通 SegmentTree -> LazySegmentTree。

最小测试样例：

```text
n=1
单点区间 l=r
整段区间 l=1,r=n
负数数组
多次修改同一点
```
