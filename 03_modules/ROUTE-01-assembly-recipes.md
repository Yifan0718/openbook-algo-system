# ROUTE-01 第 0A 卷：拼接食谱

模块编号：ROUTE-01

模块名称：第 0A 卷 拼接食谱

标签：食谱、模块组合、部分分、升级、最小验错

一句话用途：遇到常见题面时，按固定顺序把标准容器和算法模块接起来。

题面触发词：多次查询、区间修改、最短路、连通块、DAG、树上路径、容量、区间合并、访问所有点。

什么时候用：查完 ROUTE-00 后，用本卷抄“拼接顺序”和“最小验错”。

不要什么时候用：不要跳过判断信号直接背食谱；题目只要多一个修改或负边，食谱就可能换。

复杂度：每个食谱单独列。

数据范围参考：按 ROUTE-00 预算表选择。

依赖的标准容器：Graph、Array、Query、State、Compressor。

输入如何整理：先转成标准容器，再接主模块。

接口：`build/add/range_add/query/dijkstra/topo/dfs/dp`。

输出能力：给出可直接装配的代码骨架。

下游可接：C++17/STL、暴力、DP、数据结构、图论卷。

可拼接模块：见每个食谱。

模板代码：食谱给伪代码，具体模板从对应算法卷抄。

调用示例：见每个食谱。

常见坑：判断信号不完整、忘记部分分、升级时改坏输入层、最小验错没做。

暴力/部分分替代：每个食谱都给。

升级方向：每个食谱都给。

最小测试样例：每个食谱至少列 3 个风险点。

## 食谱格式

```text
场景：
判断信号：
模块组合：
拼接顺序：
伪代码骨架：
部分分版本：
升级版本：
最小验错：
```

## R01 静态区间和

场景：多次询问数组 `[l,r]` 的和。

判断信号：数组读完后不再修改；`q` 次询问；关键词“区间和”“子段和查询”。

模块组合：`DS-01 PrefixSum`。

拼接顺序：

```text
1. 读 n, q。
2. 读 a[1..n]。
3. PrefixSum ps; ps.build(a)。
4. 每个查询输出 ps.query(l, r)。
```

伪代码骨架：

```text
read n, q
read a[1..n]
PrefixSum ps; ps.build(a)
repeat q:
    read l, r
    print ps.query(l, r)
```

部分分版本：每次 `for i=l..r` 累加，`O(nq)`。

升级版本：PrefixSum，`O(n+q)`。

最小验错：`l=r`；`l=1`；`r=n`；全负数；答案超过 `int`。

## R02 单点修改 + 区间和

场景：两类操作：修改一个位置，查询一段和。

判断信号：`op=1 pos x`、`op=2 l r`；“单点修改”“区间查询”。

模块组合：`DS-02 树状数组`。

拼接顺序：

```text
1. 读 a[1..n]。
2. 树状数组 fw; fw.build(a)。
3. 若单点加：fw.add(pos, delta)。
4. 若单点赋值：delta = newValue - a[pos]，更新 a[pos]，再 fw.add(pos, delta)。
5. 查询：fw.query(l, r)。
```

伪代码骨架：

```cpp
BIT fw; fw.build(a)
if (op == 1) {
    cin >> pos >> x;
    ll delta = x - a[pos];
    a[pos] = x;
    fw.add(pos, delta);
} else {
    cin >> l >> r;
    cout << fw.query(l, r) << "\n";
}
```

部分分版本：直接改数组，查询时循环求和。

升级版本：树状数组，`O((n+q)logn)`。

最小验错：连续修改同一位置；查询单点；负数修改；`n=1`。

## R03 区间加 + 最后输出

场景：很多次给 `[l,r]` 加值，最后输出整个数组或最终状态。

判断信号：所有修改先给完，中间没有查询；关键词“最后输出”。

模块组合：`DS-01 Difference`。

拼接顺序：

```text
1. 读原数组 a。
2. 建 diff：diff[i] = a[i] - a[i-1]。
3. 每次区间加 x：diff[l] += x，diff[r+1] -= x。
4. 最后前缀还原 a。
```

伪代码骨架：

```cpp
vector<ll> diff(n + 2, 0);
for (int i = 1; i <= n; i++) diff[i] = a[i] - a[i - 1];
for (int qi = 0; qi < q; qi++) {
    int l, r;
    ll x;
    cin >> l >> r >> x;
    diff[l] += x;
    diff[r + 1] -= x;
}
ll cur = 0;
for (int i = 1; i <= n; i++) {
    cur += diff[i];
    cout << cur << (i == n ? '\n' : ' ');
}
```

部分分版本：每次循环 `i=l..r` 加。

升级版本：差分，`O(n+q)`。

最小验错：`r=n` 时 `diff[n+1]` 存在；负数加；区间长度 1；所有区间覆盖。

## R04 区间加 + 单点查

场景：在线操作，区间加，询问某个点当前值。

判断信号：`range add l r x` 和 `query pos` 混在一起；只查单点。

模块组合：`DS-02 差分树状数组`。

拼接顺序：

```text
1. 树状数组维护差分。
2. 初始数组用 range_add(i, i, a[i]) 或先建 diff。
3. 区间加：add(l, x), add(r+1, -x)。
4. 单点值：prefix(pos)。
```

伪代码骨架：

```cpp
void range_add(int l, int r, ll x) {
    fw.add(l, x);
    if (r + 1 <= n) fw.add(r + 1, -x);
}
ll at(int pos) {
    return fw.prefix(pos);
}
```

部分分版本：直接循环加，单点输出。

升级版本：差分树状数组，`O((n+q)logn)`。

最小验错：`r=n`；多次覆盖同一点；初值不是 0；负数加。

## R05 区间加 + 区间和

场景：在线区间加，还要在线查询区间和。

判断信号：操作中同时出现“区间修改”和“区间求和”。

模块组合：`DS-03 LazySegmentTree` 或 `DS-02 双树状数组`。

拼接顺序：

```text
1. 若只求和，优先 双树状数组；若还要求 min/max，优先 LazySegmentTree。
2. build(a)。
3. 修改：range_add(l, r, x)。
4. 查询：query(l, r)。
```

伪代码骨架：

```cpp
seg.build(a)
if (op == 1) seg.range_add(l, r, x);
else cout << seg.query(l, r) << "\n";
```

部分分版本：数组循环修改，查询循环求和。

升级版本：LazySegmentTree，`O((n+q)logn)`。

最小验错：连续区间修改后查询；查询整个数组；负数加；`l=r`。

## R06 静态区间最值

场景：数组不变，多次询问区间最大值、最小值或 gcd。

判断信号：无修改；`q` 很大；操作可重叠合并。

模块组合：`DS-03 SparseTable`。

拼接顺序：

```text
1. 读 a。
2. SparseTable st; st.build(a)。
3. 每次 st.query(l, r)。
```

伪代码骨架：

```cpp
SparseTable st;
st.build(a);
while (q--) {
    cin >> l >> r;
    cout << st.query(l, r) << "\n";
}
```

部分分版本：每次循环找 min/max/gcd。

升级版本：SparseTable，`O(nlogn+q)`。

最小验错：全相等；区间长度 1；长度不是 2 的幂；不要拿 ST 做区间和。

## R07 大坐标动态统计

场景：值域到 `1e9/1e18`，但操作次数只有 `2e5` 左右，需要统计排名、个数、前缀数量。

判断信号：坐标/权值很大；只关心相对大小；所有操作可以先读入。

模块组合：`CPP-007 Compressor + DS-02 树状数组`。

拼接顺序：

```text
1. 先读所有操作到 queries。
2. 把会出现的 x 放进 all。
3. Compressor cp.build(all)。
4. 树状数组 fw.init(cp.size())。
5. 按原顺序处理操作。
```

伪代码骨架：

```text
for each query:
    all.push_back(x)
cp.build(all)
fw.init(cp.size())
for each query:
    int p = cp.id(x)
    fw.add(p, delta)
```

部分分版本：用 `vector` 存所有当前值，每次排序或循环。

升级版本：Compressor + 树状数组，`O(qlogq)`。

最小验错：重复值；查询范围内无值；负坐标；`lower_id > upper_id`。

## R08 逆序对

场景：求数组中 `i<j` 且 `a[i]>a[j]` 的对数。

判断信号：关键词“逆序对”“交换排序次数”“前面比它大的数”。

模块组合：`CPP-007 Compressor + DS-02 树状数组`。

拼接顺序：

```text
1. 压缩所有 a[i]。
2. 从左到右扫描。
3. 已出现个数 = i - 1。
4. 小于等于当前的个数 = fw.prefix(id)。
5. 前面更大的个数 = 已出现 - fw.prefix(id)。
6. fw.add(id, 1)。
```

伪代码骨架：

```cpp
ll ans = 0;
for (int i = 1; i <= n; i++) {
    int p = cp.id(a[i]);
    ans += (i - 1) - fw.prefix(p);
    fw.add(p, 1);
}
```

部分分版本：双重循环 `O(n^2)`。

升级版本：树状数组，`O(nlogn)`。

最小验错：全相等答案 0；严格递增 0；严格递减 `n*(n-1)/2`；答案用 `ll`。

## R09 滑动窗口最值

场景：固定长度窗口，每个窗口求最大/最小。

判断信号：关键词“连续 k 个”“窗口”“每一段长度为 k”。

模块组合：`DS-04 MonotonicQueue`。

拼接顺序：

```text
1. 维护 deque 存下标。
2. 新元素进队前弹掉不可能成为答案的尾部。
3. 弹掉窗口外队首。
4. i >= k 时输出队首对应值。
```

伪代码骨架：

```cpp
for (int i = 1; i <= n; i++) {
    while (!dq.empty() && a[dq.back()] <= a[i]) dq.pop_back();
    dq.push_back(i);
    while (!dq.empty() && dq.front() <= i - k) dq.pop_front();
    if (i >= k) cout << a[dq.front()] << "\n";
}
```

部分分版本：每个窗口循环找最值。

升级版本：单调队列，`O(n)`。

最小验错：`k=1`；`k=n`；全相等；递增/递减数组。

## R10 无权最短路

场景：边没有权，求最少边数、最少步数、最少操作次数。

判断信号：无权图；网格一步代价相同；关键词“最少步数”。

模块组合：`GRAPH-02 BFS + queue`。

拼接顺序：

```text
1. 建 Graph 或保留 Grid。
2. dist 初始化 -1。
3. 起点入队 dist[s]=0。
4. 每次扩展未访问邻点。
```

伪代码骨架：

```cpp
queue<int> q;
vector<int> dist(n + 1, -1);
dist[s] = 0; q.push(s);
while (!q.empty()) {
    int u = q.front(); q.pop();
    for (auto e : G.g[u]) {
        int v = e.to;
        if (dist[v] == -1) {
            dist[v] = dist[u] + 1;
            q.push(v);
        }
    }
}
```

部分分版本：DFS 只能判可达，不能保证最短；可拿连通性相关分。

升级版本：BFS，`O(n+m)`。

最小验错：起点等于终点；不可达；重边；网格边界。

## R11 非负权最短路

场景：边有非负权，求从一个点到其他点的最短距离。

判断信号：边权 `w >= 0`；关键词“最短路径”“最小花费”。

模块组合：`GRAPH-03 Dijkstra + CPP-004 priority_queue`。

拼接顺序：

```text
1. Graph 加权建图。
2. dist 初始化 LINF。
3. 小根堆存 {dist, node}。
4. 弹出旧状态要跳过。
5. 松弛邻边。
```

伪代码骨架：

```cpp
dist[s] = 0;
pq.push({0, s});
while (!pq.empty()) {
    auto [du, u] = pq.top(); pq.pop();
    if (du != dist[u]) continue;
    for (auto e : G.g[u]) {
        if (dist[e.to] > du + e.w) {
            dist[e.to] = du + e.w;
            pq.push({dist[e.to], e.to});
        }
    }
}
```

部分分版本：Bellman-Ford 小数据 `O(nm)` 或 DFS 枚举简单路径极小数据。

升级版本：Dijkstra，`O((n+m)logn)`。

最小验错：不可达；多条重边；0 权边；有负边时不能用。

## R12 小图全源最短路

场景：任意两点最短路，`n <= 300/500`。

判断信号：多次问任意 `u,v`；图小；可能要中转。

模块组合：`GRAPH-04 Floyd`。

拼接顺序：

```text
1. dist[n+1][n+1] 初始化 LINF。
2. dist[i][i]=0。
3. 用 G.edges 初始化边。
4. 三重循环 k,i,j。
5. 回答 dist[u][v]。
```

伪代码骨架：

```text
for k in 1..n:
    for i in 1..n:
        for j in 1..n:
            dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
```

部分分版本：每次询问跑 BFS/Dijkstra。

升级版本：Floyd，预处理 `O(n^3)`，查询 `O(1)`。

最小验错：重边取 min；不可达；有向/无向初始化；`LINF + LINF` 防溢出。

## R13 最小生成树

场景：连接所有点的最小总费用。

判断信号：无向图；关键词“修路”“连接所有城市”“总费用最小”。

模块组合：`GRAPH-06 DSU + Kruskal`。

拼接顺序：

```text
1. 用 Graph 读边。
2. 复制 G.edges 并按 w 升序排序。
3. DSU.init(n)。
4. 能 unite 的边加入答案。
5. 最后检查加入边数是否 n-1。
```

伪代码骨架：

```text
sort(es by w)
for e in es:
    if dsu.unite(e.from, e.to):
        ans += e.w
        cnt++
if cnt != n - 1: no solution
```

部分分版本：枚举边集只适合极小数据；或只判连通拿部分分。

升级版本：Kruskal，`O(mlogm)`。

最小验错：图不连通；重边；负权边也可用；不要用有向图。

## R14 DAG 依赖顺序 + DP

场景：任务依赖、课程先修、从前驱转移到后继。

判断信号：有向边表示先后；题面说“无环”或可拓扑；求最长链/方案数/最早完成时间。

模块组合：`GRAPH-05 Topo + DAG DP`。

拼接顺序：

```text
1. 用 `G.add_directed(u, v)` 建图。
2. topo_sort 得 order。
3. 若 order.size()!=n，说明有环。
4. 按 order 顺序转移 dp。
```

伪代码骨架：

```cpp
vector<int> order = topo_sort(G);
for (int u : order) {
    for (auto e : G.g[u]) {
        int v = e.to;
        dp[v] = max(dp[v], dp[u] + value);
    }
}
```

部分分版本：DFS + memo，遇到正在访问的点标记有环。

升级版本：Topo + DP，`O(n+m)`。

最小验错：多个入度 0；有环；不连通 DAG；方案数取模。

## R15 树上路径查询

场景：树上两点距离、最近公共祖先、路径信息。

判断信号：`n` 个点 `n-1` 条边；无向连通；多次问 `u,v`。

模块组合：`GRAPH-09 LCA`。

拼接顺序：

```text
1. 无向建树。
2. 从根 1 DFS，得到 depth、up、distRoot。
3. 每问 lca = query(u,v)。
4. 距离 = distRoot[u] + distRoot[v] - 2*distRoot[lca]。
```

伪代码骨架：

```cpp
lca.build(G, 1);
int z = lca.query(u, v);
ll d = distRoot[u] + distRoot[v] - 2 * distRoot[z];
```

部分分版本：每次 BFS/DFS 找父亲路径，`O(nq)`。

升级版本：LCA，预处理 `O(nlogn)`，查询 `O(logn)`。

最小验错：`u=v`；根参与查询；链状树；星状树；边权为 0。

## R16 0/1 背包

场景：每个物品最多选一次，在容量内最大价值/可行性/方案数。

判断信号：“每个只能选一次”“容量 W”“重量/价值”。

模块组合：`DP-06/07/08/24 Knapsack`。

拼接顺序：

```text
1. dp[0..W] 初始化。
2. 枚举物品 i。
3. 容量 j 从 W 倒序到 weight[i]。
4. dp[j] = max(dp[j], dp[j-w]+val)。
```

伪代码骨架：

```cpp
for (int i = 1; i <= n; i++) {
    for (int j = W; j >= w[i]; j--) {
        dp[j] = max(dp[j], dp[j - w[i]] + val[i]);
    }
}
```

部分分版本：DFS 枚举选/不选。

升级版本：滚动数组 DP，`O(nW)`。

最小验错：`W=0`；物品重量大于 W；价值为 0；倒序循环不能写反。

## R17 区间 DP

场景：区间合并、括号匹配、删除一段、石子合并。

判断信号：答案定义在 `[l,r]`；转移枚举中间点 `k`；`n <= 300/500`。

模块组合：`DP-13 Interval DP + DS-01 PrefixSum`。

拼接顺序：

```text
1. 初始化长度为 1 的区间。
2. 枚举 len 从 2 到 n。
3. 枚举 l，得到 r。
4. 枚举分割点 k。
5. 若需要区间和，用 PrefixSum.query(l,r)。
```

伪代码骨架：

```cpp
for (int len = 2; len <= n; len++) {
    for (int l = 1; l + len - 1 <= n; l++) {
        int r = l + len - 1;
        for (int k = l; k < r; k++) {
            dp[l][r] = min(dp[l][r], dp[l][k] + dp[k + 1][r] + cost(l, r));
        }
    }
}
```

部分分版本：DFS 枚举合并顺序 + memo。

升级版本：表推区间 DP，`O(n^3)`。

最小验错：长度 1；长度 2；初始化 INF；区间和下标。

## R18 访问所有点状压

场景：从若干点中访问所有点，求最短路径/最小代价。

判断信号：`n <= 20`；关键词“每个点访问一次/至少一次”“集合状态”。

模块组合：`GRAPH-03/04 shortest path + DP-16 Bitmask DP`。

拼接顺序：

```text
1. 先求关键点两两距离。
2. dp[mask][last] 表示访问集合 mask，最后在 last 的最小代价。
3. 枚举 mask、last、next。
4. 答案取完整 mask 的最小值。
```

伪代码骨架：

```cpp
dp[1 << (start - 1)][start] = 0; // start 是 1..k 的关键点编号，full = 1 << k
for (int mask = 0; mask < full; mask++) {
    for (int last = 1; last <= k; last++) {
        if (dp[mask][last] == INF) continue;
        for (int nxt = 1; nxt <= k; nxt++) {
            if (mask >> (nxt - 1) & 1) continue;
            int nmask = mask | (1 << (nxt - 1));
            dp[nmask][nxt] = min(dp[nmask][nxt], dp[mask][last] + dist[last][nxt]);
        }
    }
}
```

部分分版本：全排列枚举访问顺序。

升级版本：状压 DP，`O(2^n n^2)`。

最小验错：不可达距离；起点是否固定；回不回起点；`1<<n` 溢出，n 不要太大。

## R19 复杂状态 DFS + memo

场景：题目选择多、状态难表推，但递归会重复。

判断信号：暴力 DFS 会多次遇到同一个 `(进度,资源,记忆)`；数据不够支持纯暴力。

模块组合：`BRUTE-09 map<tuple<...>, ans>` 或 `DP-25 DFS + memo`。

拼接顺序：

```text
1. 写纯 dfs，参数只放影响未来的量。
2. 找 base case。
3. 在函数开头查 memo。
4. 枚举选择并更新 ans。
5. 返回前写 memo。
```

伪代码骨架：

```cpp
ll dfs(int i, int rem, int last) {
    if (rem < 0) return -LINF;
    auto key = make_tuple(i, rem, last);
    if (memo.count(key)) return memo[key];
    if (i == n + 1) return memo[key] = 0;
    ll ans = dfs(i + 1, rem, last);
    if (can_choose) ans = max(ans, gain + dfs(i + 1, rem - cost, i)); // can_choose 必须包含资源可行性
    return memo[key] = ans;
}
```

部分分版本：纯 DFS。

升级版本：Memo；若范围清楚，再改数组 DP。

最小验错：base 是否写入 memo；状态是否漏了影响未来的变量；有环状态要加 visiting；返回值单位元。

## R20 二分答案 + 检查函数

场景：最大化最小值、最小化最大值、求最少时间/最小容量。

判断信号：问“最小的最大”“最大的最小”；答案有单调性。

模块组合：`DS-06 BinarySearch + Check + GREEDY/GRAPH/DP`。

拼接顺序：

```text
1. 明确 check(x) 表示 x 是否可行。
2. 证明口头单调：x 变大更容易，或 x 变大更难。
3. 设定答案左右边界。
4. 二分并调用 check。
5. 输出边界。
```

伪代码骨架：

```cpp
while (l < r) {
    ll mid = l + (r - l) / 2;
    if (check(mid)) r = mid;
    else l = mid + 1;
}
cout << l << "\n";
```

部分分版本：枚举答案逐个 check。

升级版本：二分答案，复杂度 `O(check * logV)`。

最小验错：边界是否包含答案；`mid` 是否溢出；check 单调方向；输出 `l` 还是 `r`。
