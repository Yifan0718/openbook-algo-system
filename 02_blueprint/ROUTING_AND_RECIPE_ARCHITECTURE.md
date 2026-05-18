# 题面路由与拼接食谱架构 v0.1

## 1. 为什么还需要这一层

统一 `Graph`、`树状数组`、`State` 等接口，只解决了“模块能不能接上”的问题。

对算法基础薄弱、临近考试的使用者，还必须解决三个更上层的问题：

```text
该用哪个模块？
几个模块按什么顺序接？
写完后怎么快速验错？
```

因此整套资料必须从“模板库”升级为：

```text
题面信号 -> 数据范围 -> 模型候选 -> 模块组合 -> 接口契约 -> 拼接顺序 -> 最小验错
```

这才是纸质版算法作战系统。

## 2. 新增四个顶层层级

### 2.1 题面路由层

从题面关键词直接导向模型和模块。

| 题面信号 | 优先模型 | 主模块 | 辅助模块 |
|---|---|---|---|
| 区间多次查询、无修改 | 静态区间查询 | PrefixSum / SparseTable | Compressor |
| 区间修改、点查询 | 差分 | Difference / 差分树状数组 | 扫描线 |
| 点修改、区间查询 | 动态区间和/最值 | 树状数组 / SegmentTree | Compressor |
| 区间修改、区间查询 | 动态区间结构 | LazySegmentTree / 双树状数组 | Compressor |
| 连通性、合并集合 | 并查集 | DSU | Kruskal |
| 无权最短路 | BFS | Graph + BFS | queue |
| 边权非负最短路 | Dijkstra | Graph + Dijkstra | priority_queue |
| 有负边最短路 | Bellman-Ford / SPFA | Graph.edges / Graph.g | 负环判断 |
| DAG、依赖顺序 | 拓扑排序 / DAG DP | Graph + Topo | DP |
| 树上路径、祖先 | LCA | Graph + LCA | DFS depth |
| 选/不选、容量 | 背包 DP | DP State | 滚动数组 |
| n<=20 且集合相关 | 状压 | Bitmask DP / DFS | Floyd/Dijkstra |
| 区间合并/删除 | 区间 DP | DP[l][r] | PrefixSum |
| 两个字符串/序列 | 双序列 DP | LCS / EditDistance | string |

### 2.2 约束路由层

数据范围决定能不能用某模块。

| 规模 | 可接受复杂度 | 常见选择 |
|---|---|---|
| `n <= 10` | `O(n!)` | 全排列、回溯 |
| `n <= 20` | `O(2^n n)` | 状压 DP、子集 DFS |
| `n <= 40` | `O(2^(n/2))` | 折半枚举 |
| `n <= 300/500` | `O(n^3)` | Floyd、区间 DP |
| `n <= 3000/5000` | `O(n^2)` | 普通 DP、双重循环 |
| `n <= 2e5` | `O(n log n)` | 排序、堆、树状数组、线段树、Dijkstra |
| `n <= 1e6` | `O(n)` | 前缀、差分、双指针、单调队列 |

### 2.3 模块接口契约层

每个模块必须声明：

```text
模块名：
输入依赖：
输出能力：
下游可接：
不能处理：
初始化顺序：
查询/更新接口：
复杂度：
常见坑：
最小测试：
```

示例：

```text
Dijkstra：
输入依赖：Graph，边权非负，起点 s
输出能力：dist[i]
下游可接：路径恢复、最短路 DAG、计数 DP
不能处理：负权边
初始化顺序：建图 -> dist=LINF -> pq
接口：vector<ll> dijkstra(const Graph& G, int s)
复杂度：O((n+m)logn)
常见坑：负边、INF 溢出、旧状态未跳过
最小测试：3 点链式图
```

### 2.4 拼接食谱层

不要只给模板，要给“题型配方”。

固定格式：

```text
场景：
判断信号：
模块组合：
拼接顺序：
核心变量：
伪代码骨架：
替换点：
最小验错：
部分分版本：
升级版本：
```

示例：

```text
场景：多次询问区间和
判断信号：数组不变，q 次问 [l,r]
模块组合：Array + PrefixSum + Query
拼接顺序：
1. 读 n, q
2. 读 a[1..n]
3. PrefixSum ps; ps.build(a)
4. 每次输出 ps.query(l, r)
最小验错：l=r、l=1、r=n、全负数
部分分版本：每次循环求和 O(nq)
升级版本：PrefixSum O(n+q)
```

## 3. 顶层目录微调

建议最终资料前置目录调整为：

```text
00_考场总路由
01_统一接口与输入整理
02_数据范围判算法
03_题面关键词判模型
04_常用拼接食谱
05_C++17/STL 快查
06_暴力与部分分
07_DP 模型复用系统
08_数据结构
09_图论与树
10_数学与字符串
11_调试与反例清单
```

也就是说，真正的算法卷不要太早出现。前面必须先解决：

```text
怎么判断？
怎么接？
怎么验？
```

## 4. 食谱优先清单

第一批必须生成这些食谱：

### 数据结构食谱

```text
静态区间和：Array + PrefixSum
静态区间最值：Array + SparseTable
单点修改区间和：Array + 树状数组
区间加最后输出：Array + Difference
区间加区间和：双树状数组 / LazySegTree
大坐标动态统计：Compressor + 树状数组
逆序对：Compressor + 树状数组
滑动窗口最值：Deque + MonotonicQueue
最近更大/更小：MonotonicStack
```

### 图论食谱

```text
无权最短路：Graph + BFS
非负权最短路：Graph + Dijkstra
小图全源最短路：Graph.edges + Floyd
合并连通块：Graph.edges + DSU
最小生成树：Graph.edges + DSU + Kruskal
DAG 依赖顺序：Graph + Topo
DAG 路径计数/最优：Graph + Topo + DP
树上路径：Graph + DFS depth + LCA
二分图判断：Graph + BFS color
```

### DP 食谱

```text
选/不选最优：DFS -> Memo -> 0/1 背包
容量无限选：完全背包
每组最多一个：分组背包
两个序列匹配：LCS / EditDistance
区间合并：PrefixSum + IntervalDP
树上选点：Graph + TreeDP
访问所有点：Floyd/Dijkstra + BitmaskDP
DAG 上方案数：Graph + Topo + DP
复杂状态：DFS + map<tuple,...> memo
```

## 5. 对每个食谱的验错要求

每个食谱必须给最小测试点：

```text
单元素
空/无解
边界区间
全相等
有重边/自环
不连通
负数
容量为 0
```

不是每个食谱都需要全部覆盖，但必须有 3-5 个高风险点。

## 6. 一句话标准

后续生成资料时，每个模块不能只回答“我是什么算法”，还必须回答：

```text
我从哪个题面信号来？
我依赖哪个标准容器？
我输出什么给下一个模块？
我不能处理什么？
我至少怎么拿部分分？
```

