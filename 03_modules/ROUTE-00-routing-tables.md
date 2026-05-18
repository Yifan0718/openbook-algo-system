# ROUTE-00 第 0A 卷：题面路由表

模块编号：ROUTE-00

模块名称：第 0A 卷 题面路由表

标签：路由、关键词、数据范围、操作类型、模块选择

一句话用途：把题面信号、数据范围和操作类型快速映射到可抄模块。

题面触发词：区间、修改、查询、最短、连通、树、DAG、容量、方案数、字符串、坐标很大。

什么时候用：读完题后 3 分钟内，用本表决定第一版代码写什么。

不要什么时候用：不要在还没看数据范围时直接套高级模板。

复杂度：本表只做选择；复杂度见数据范围预算表。

数据范围参考：所有题目。

依赖的标准容器：Graph、Array、Query、State、Compressor。

输入如何整理：先圈 `n/m/q/值域/是否修改/是否有边权/是否有环`，再查表。

接口：路由到 `build/add/range_add/query/dijkstra/topo/dp/dfs` 等模块。

输出能力：给出优先模型、主模块、辅助模块和不要使用的场景。

下游可接：所有算法卷。

可拼接模块：见各表。

模板代码：无。

调用示例：按“信号 -> 模型 -> 容器 -> 模块 -> 验错”的顺序执行。

常见坑：只看关键词不看修改；只看 `n` 不看 `q`；图有负边还用 Dijkstra；树题没确认是否真是树。

暴力/部分分替代：查不到就先按数据范围写暴力或 memo。

升级方向：从预算表升级到 `O(n log n)`、`O(n)` 或图/DP 专门模块。

最小测试样例：每条路由至少测边界、小数据、极端值。

## 1. 3 分钟路由动作

```text
第 1 分钟：圈数据范围 n, m, q, 值域，写下目标复杂度。
第 2 分钟：圈题面动作：查询、修改、路径、连通、选择、计数、匹配。
第 3 分钟：查本表，决定标准容器和第一版模块。
```

优先级：

```text
先看数据范围能不能承受。
再看有没有修改。
再看图边权和方向。
最后看目标：最小/最大/方案数/可行性/构造。
```

## 2. 题面信号路由表

| 题面信号 | 优先模型 | 标准容器 | 主模块 | 辅助模块 | 不要用在 |
|---|---|---|---|---|---|
| 数组不变，多次问 `[l,r]` 和 | 静态区间和 | `vector<ll> a` | PrefixSum | Query | 有修改 |
| 数组不变，多次问 min/max/gcd | 静态 RMQ | `vector<ll> a` | SparseTable | Log 表 | 有修改、区间和 |
| 单点修改，区间和 | 动态前缀 | Array | 树状数组 | SegmentTree | 区间修改 |
| 单点修改，区间最值 | 动态区间最值 | Array | SegmentTree | Compressor | 只问区间和时优先 树状数组 |
| 区间加，单点查 | 差分 | Array | Difference / 差分树状数组 | Query | 还要区间和 |
| 区间加，区间和 | 动态区间结构 | Array | LazySegTree / 双树状数组 | Compressor | 只做最后输出 |
| 值域很大，但只比较大小/排名 | 离散化 | Compressor | 树状数组 / SegmentTree | Sort | 需要真实连续距离 |
| 求逆序对、前面有多少数大/小 | 动态统计 | Compressor | 树状数组 | Sort | `n` 很小可暴力 |
| 滑动窗口最大/最小 | 单调队列 | Array | MonotonicQueue | Deque | 窗口长度不固定且有复杂删除 |
| 最近更大/更小、贡献边界 | 单调栈 | Array | MonotonicStack | 前后边界数组 | 需要任意区间动态查询 |
| 连通性、合并集合 | 并查集 | 边表 | DSU | Kruskal | 需要删除边 |
| 最小生成树、修路最小费用 | MST | `Graph.edges` | Kruskal | DSU | 有向图最小树形图 |
| 无权最短路、最少步数 | BFS | Graph / Grid | BFS | queue | 有权边 |
| 边权非负最短路 | 单源最短路 | Graph | Dijkstra | priority_queue | 有负边 |
| 有负边最短路 | 松弛最短路 | `Graph.edges` | Bellman-Ford / SPFA | 负环判断 | `n,m` 很大且无负边 |
| 小图任意两点最短路 | 全源最短路 | `Graph.edges` + 矩阵 | Floyd | 路径恢复 | `n > 500` 通常危险 |
| DAG、依赖、先后顺序 | 拓扑 | Graph directed | Topo | DP | 有环 |
| DAG 上最长/最短/方案数 | DAG DP | Graph directed | Topo + DP | 入度 | 有环未处理 |
| 树上祖先、两点路径 | 树上查询 | Graph undirected | LCA | DFS depth/dist | 不是树或森林 |
| 树上选点、父子依赖 | 树形 DP | Graph undirected | DFS DP | State | 一般图有环 |
| 树上选 K 个、子树合并容量 | 树上背包 | Graph tree + State | DP-14 / DP-19 | Knapsack | 一般图有环 |
| 每个点作为根/中心、贡献重算 | 换根 DP | Graph tree | TREE-02 | TreeDP | 非树 |
| 选/不选、容量限制 | 背包 | State | 0/1 Knapsack | 滚动数组 | 物品可无限选 |
| 可以无限选某物品 | 完全背包 | State | Complete Knapsack | 循环顺序 | 每物只能选一次 |
| 每组最多选一个 | 分组背包 | State | Group Knapsack | 分组循环 | 物品无组限制 |
| 两个字符串/序列匹配 | 双序列 DP | string / Array | LCS / EditDistance | DP 表 | 只需子串可考虑哈希/KMP |
| LIS/LCS 变体、LCIS、公共且上升 | 序列 DP 变体 | Array / string | DP-23 | 树状数组/SegmentTree | 连续子串要换模型 |
| 训练集、测试集、标签、模型、SPJ 得分 | AI 包装题 | 样本表 / 特征矩阵 | AI-00 / AI-10 | AI-02..15 | 不要上第三方库或随机大模型 |
| SVM、DNN、反向传播、自动求导 | AI 公式模拟 | 计算图 / 矩阵向量 | AI-11..15 | SIM-03 | 数据大时先 baseline |
| JSON/CSV/INI、表达式、脚本规则 | 解析模拟 | Token / AST | SIM-03/04/05 | string / map | 不要临场乱写半解析 |
| 日期、时区、经过天数、历法 | 日期模拟 | Date / day number | SIM-06 | 数学取模 | 夏令时规则不明时按题面 |
| 区间合并、区间删除、括号匹配 | 区间 DP | Array | IntervalDP | PrefixSum | `n` 很大 |
| `n <= 20` 且访问集合 | 状压 | State mask | BitmaskDP / DFS | Floyd/Dijkstra | `n > 22` 基本爆 |
| 1..N、数位限制、上界很大 | 数位 DP | digits + state | DP-17 | DFS memo | 小范围普通枚举 |
| `dp[i]=min/max dp[j]+cost` 且查询范围 | DP 优化 | State + query | DP-18 | 树状数组/SegmentTree | 先写朴素 |
| 方案数、可行性、能否凑出 | 计数/可行性 DP | State | DP-20 | MOD / bitset | 不要用取模值判可达 |
| 多重/二维/价值维度/至少装满背包 | 背包变体 | Knapsack State | DP-24 | DP-06/07/08 | 先判至多/恰好/至少 |
| 斜率、分治、Knuth、SOS、轮廓线等高阶 DP 信号 | 高阶 DP 索引 | State | DP-27 | 先交朴素/记忆化 | 不满足条件别硬套 |
| 重复状态明显但不好表推 | 记忆化搜索 | State | DFS + memo | map tuple | 状态有环且无处理 |
| 求第 k、小于等于 x 个数 | 排名/二分 | Compressor | 树状数组 / SegmentTree | 二分答案 | 静态可排序二分 |
| 最大最小值、最小化最大值 | 二分答案 | 判断函数 | BinarySearch + Check | Greedy/Graph/DP | check 不单调 |

## 3. 数据范围预算表

先用最大量级估算，不要被样例骗。

| 数据范围 | 目标复杂度 | 常见可用模块 | 考场口令 |
|---|---|---|---|
| `n <= 8..10` | `O(n!)` | 全排列、爆搜 | 可以先全排列拿分 |
| `n <= 18..22` | `O(2^n n)` | 状压 DP、子集枚举 | 看到集合访问先想 mask |
| `n <= 35..45` | `O(2^(n/2))` | 折半枚举 | 一分为二，排序合并 |
| `n <= 300` | `O(n^3)` | Floyd、区间 DP | 三重循环可接受 |
| `n <= 500` | 勉强 `O(n^3)` | Floyd、小规模 DP | 常数要小 |
| `n <= 3000` | `O(n^2)` | 双序列 DP、普通 DP | 双重循环可试 |
| `n <= 5000` | `O(n^2)` 边缘 | DP、枚举优化前版本 | C++ 勉强，注意常数 |
| `n,q <= 2e5` | `O((n+q)log n)` | 树状数组、SegmentTree、Dijkstra、排序 | 默认 log 结构 |
| `n,m <= 2e5` | `O((n+m)log n)` | BFS、Dijkstra、Kruskal、Topo | 图用邻接表 |
| `n <= 1e6` | `O(n)` 或 `O(n log n)` | 前缀、差分、双指针、筛法 | 少开二维 |
| 值域 `1e9/1e18`，数量 `2e5` | `O(n log n)` | Compressor + 树状数组 | 坐标压缩 |
| 网格 `n*m <= 2e5` | `O(nm)` | Grid BFS/DP | 二维直接做 |
| 网格 `n,m <= 1000` | `O(nm)` | BFS、前缀、DP | 内存约百万级 |
| 多测试总和给出 | 按总和 | 清空容器 | 不要按单测最大乘 T |
| 多测试无总和 | 保守 | 暴力分档/剪枝 | 防止总量爆炸 |

粗算：

```text
1e8 次简单操作已经危险。
2e8 次以上不要赌，除非常数极小且时间宽。
vector<vector<ll>>(5000,5000) 约 200MB，通常危险。
```

## 4. 操作类型路由表

| 操作组合 | 第一选择 | 接口 | 复杂度 | 部分分版本 | 升级方向 |
|---|---|---|---|---|---|
| 静态区间和 | PrefixSum | `build/query` | `O(n+q)` | 每问循环 `O(nq)` | 无需升级 |
| 静态区间 min/max/gcd | SparseTable | `build/query` | `O(nlogn+q)` | 每问循环 | SegmentTree 若有修改 |
| 单点加 + 前缀/区间和 | 树状数组 | `add/prefix/query` | `O(logn)` | 直接改数组再循环 | SegmentTree |
| 单点赋值 + 区间和 | 树状数组 | `add(pos, new-old)` | `O(logn)` | 数组暴力 | SegmentTree |
| 单点赋值 + 区间最值 | SegmentTree | `setv/query` | `O(logn)` | 数组暴力 | 无 |
| 区间加 + 最后输出 | Difference | `diff[l]+=x,diff[r+1]-=x` | `O(n+q)` | 每次循环加 | 差分树状数组 |
| 区间加 + 单点查 | 差分树状数组 | `range_add/at` | `O(logn)` | 差分离线 | LazySegTree |
| 区间加 + 区间和 | LazySegTree / 双树状数组 | `range_add/query` | `O(logn)` | 每次循环 | LazySegTree |
| 第 k 小 / 动态排名 | Compressor + 树状数组 | `add/prefix` + 二分 | `O(log^2 n)` | 排序数组重算 | 权值线段树 |
| 连通块合并 | DSU | `find/unite` | 近似 `O(1)` | DFS 每次判连通 | 无删除边 |
| 加边判是否成环 | DSU | `unite` 返回真假 | 近似 `O(1)` | DFS | Kruskal |
| 无权单源最短路 | BFS | `bfs(G,s)` | `O(n+m)` | DFS 不保证最短 | Dijkstra 若有权 |
| 非负权单源最短路 | Dijkstra | `dijkstra(G,s)` | `O((n+m)logn)` | Bellman-Ford 小数据 | 无负边 |
| 任意两点小图最短路 | Floyd | `dist[i][j]` | `O(n^3)` | 每次 BFS/Dijkstra | Johnson 不作为优先 |
| 有向无环依赖 | Topo | `topo_sort(G)` | `O(n+m)` | DFS 记忆化 | DAG DP |
| 树上路径距离 | DFS + LCA | `lca.query(u,v)` | `O(logn)` | 每问 BFS/爬父亲 | 树剖低优先 |
| 容量选择最优 | 背包 DP | `dp[j]` | `O(nW)` | DFS 枚举 | 优化循环/滚动 |
| 复杂状态最优 | Memo DFS | `dfs(state)` | 状态数 * 转移 | 暴力 DFS | 表推 DP |

## 5. 路由冲突时怎么判

```text
有修改优先看操作类型，不要直接用静态算法。
有边权优先看权值符号：无权 BFS，非负 Dijkstra，负边 Bellman-Ford/SPFA。
是树先确认 m = n - 1 且连通；否则按一般图处理。
有 DAG 字样但可能有环，先 topo 检查 order.size() == n。
值域大但只出现 2e5 个数，先 Compressor。
能先拿部分分时，先写暴力版本，保留函数名再升级。
```
