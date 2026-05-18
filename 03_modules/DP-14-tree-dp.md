# DP-14：树形 DP

模型编号：DP-14

模型名称：树形 DP

标签：DP、树、子树、选点、覆盖、染色

一句话用途：在树上按子树合并状态，处理选点、覆盖、染色、最大独立集等问题。

题面触发词：

- “树上选择若干点”
- “父子不能同时选”
- “覆盖所有点”
- “树上染色”
- “以子树为单位”

什么时候用：

- 输入是一棵树或森林。
- 一个节点的答案可以由儿子子树合并。
- 状态通常描述 `u` 自己选不选、颜色或覆盖情况。

不要什么时候用：

- 图有环且不是树，普通树形 DP 不适用。
- 问树上路径多次查询，可能是 LCA/树链/数据结构。
- 子树之间有额外横向边，状态不独立。

复杂度：

- 常见 `O(n * 状态数^2)` 或 `O(n * 状态数)`。

数据范围信号：

- `n <= 2e5` 且状态少：树形 DP 可做。
- 状态含背包容量：复杂度可能变成 `O(nW^2)` 或 `O(nW)`。

依赖的标准容器：

- 标准 `Graph G`。
- 本页后续 `vector<vector<int>> g(n + 1)` 是速抄变体；与图论卷拼接时优先从 `G.g` 取 `e.to/e.w`。
- `vector<array<ll, 2>> dp`
- `vector<int> parent, order`

输入如何整理：

- 建无向树。
- DFS 时传 `parent` 防止走回父亲。
- 权值统一 `w[u]`。

接口：

```cpp
void dfs(int u, int p);
```

输出能力：

- 树上最大/最小选择值。
- 覆盖、染色、方案数。

下游可接：

- Graph 标准建图。
- 树上背包。
- DP-03B 状态增维：不同方向进入同一节点、`parent/prev` 影响未来时检查 memo key。

可拼接模块：

- Graph：统一邻接表。
- 0/1 背包：子树容量合并。
- 记忆化 DFS：状态复杂时先写。

状态句式：

```text
dp[u][state] 表示：只考虑 u 的子树，并且 u 自己处于 state 状态时的最优值/方案数。
```

为什么这个状态够用：固定根以后，不同儿子子树之间没有横向边；父亲对子树的影响只通过 `u` 的状态传下来。只要 `u` 的状态确定，每个儿子子树就可以独立求解，再合并。

最大独立集常用：

```text
dp[u][0] 表示：u 不选时，u 子树最大权值。
dp[u][1] 表示：u 选时，u 子树最大权值。
```

初始化：

```text
dp[u][0] = 0：不选 u，初始没有贡献。
dp[u][1] = w[u]：选 u，先拿 u 的权值。
```

转移模板：

```cpp
dp[u][0] += max(dp[v][0], dp[v][1]);
dp[u][1] += dp[v][0];
```

标准 `Graph G` 循环写法：

```cpp
for (auto e : G.g[u]) {
    int v = e.to;
    ll w = e.w;
    if (v == p) continue;
    // 树边权不用时忽略 w
}
```

速抄局部 `g` 变体：

```cpp
for (int v : g[u]) {
    if (v == p) continue;
}
```

答案位置：

- 根为 `1`：`max(dp[1][0], dp[1][1])`。
- 森林：对每棵树答案相加。

循环顺序：

- 后序 DFS：先算儿子，再合并到父亲。
- 或先拿 DFS 序，再按逆序表推。

暴力 DFS 版本：

```cpp
ll brute(int u, int p, int parentChosen) {
    ll ans0 = 0; // 不选 u
    for (int v : g[u]) if (v != p) ans0 += brute(v, u, 0);

    ll ans1 = -LINF;
    if (!parentChosen) {
        ans1 = w[u];
        for (int v : g[u]) if (v != p) ans1 += brute(v, u, 1);
    }
    return max(ans0, ans1);
}
```

记忆化版本：

注意：下面 memo 版本只适用于固定根以后，`u` 的父亲唯一的树形 DP。若换根，或同一个 `u` 可能带不同 `p`，必须把 `p/parent` 纳入状态，或者不要缓存。

```cpp
vector<array<ll, 2>> memo;
vector<array<int, 2>> vis;

ll dfs_memo(int u, int p, int parentChosen) {
    if (vis[u][parentChosen]) return memo[u][parentChosen];
    vis[u][parentChosen] = 1;

    ll ans0 = 0;
    for (int v : g[u]) if (v != p) ans0 += dfs_memo(v, u, 0);

    ll ans1 = -LINF;
    if (!parentChosen) {
        ans1 = w[u];
        for (int v : g[u]) if (v != p) ans1 += dfs_memo(v, u, 1);
    }
    return memo[u][parentChosen] = max(ans0, ans1);
}
```

表推版本：

```cpp
vector<array<ll, 2>> dp(n + 1);

void dfs(int u, int p) {
    dp[u][0] = 0;
    dp[u][1] = w[u];
    for (int v : g[u]) {
        if (v == p) continue;
        dfs(v, u);
        dp[u][0] += max(dp[v][0], dp[v][1]);
        dp[u][1] += dp[v][0];
    }
}

dfs(1, 0);
cout << max(dp[1][0], dp[1][1]) << '\n';
```

常见变体：

- 最小点覆盖：`dp[u][0] += dp[v][1]`，`dp[u][1] += min(dp[v][0], dp[v][1])`。
- 树上染色：`dp[u][color]` 合并儿子颜色。
- 树上背包：`dp[u][k]` 表示子树选 `k` 个。

常见坑：

- 忘记传父亲，递归走回去。
- 根的父亲状态处理错。
- 递归深度过大可能爆栈。
- 子树合并时更新顺序覆盖旧值。
- 固定根树形 DP 中 `parent` 通常是 DFS 参数；如果同一个 `u` 可能从不同方向进入并被缓存，`parent/prev` 必须进入状态。
- `n` 接近 `2e5` 时递归可能爆栈；如果现场栈限制严格，改用父数组 + DFS 序逆序表推更稳。

暴力/部分分替代：

- `n <= 20`：枚举点集检查边约束。
- 树结构明确但转移复杂：先写递归 + memo。
- 多个连通块：逐个根 DFS。

升级方向：

- 简单选点 -> `dp[u][0/1]`。
- 覆盖问题 -> `dp[u][0/1/2]`。
- 容量限制 -> 树上背包。
- 换根或无固定父亲的记忆化 -> 先检查 DP-03B 的 `parent/prev` 维度。

最小测试样例：

```text
3
w: 1 2 3
edges: 1-2, 1-3
输出：5
说明：选 2 和 3。
```
