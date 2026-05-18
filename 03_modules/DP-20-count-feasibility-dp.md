# DP-20：计数 / 可行性 DP

模型编号：DP-20

模型名称：计数 / 可行性 DP

标签：DP、方案数、可行性、取模、初始化、判定

一句话用途：把“有多少种方案”和“是否存在方案”从最优值 DP 中单独拆出来，避免初值、转移和取模混用。

题面触发词：

- “方案数”“有多少种”
- “对 1e9+7 取模”
- “是否存在”“能否凑出”
- “可不可以”“是否可达”
- “恰好”“至少”“至多”

什么时候用：

- `dp` 不是最大/最小值，而是数量或真假。
- 背包、网格、DAG、数位、区间里问方案数。
- 题目同时要求“是否存在”和“方案数”。

不要什么时候用：

- 明确要求最大收益/最小代价时，先按最优值 DP 写。
- 方案数可能巨大但题目没有要求取模时，要确认是否需要高精度或 long long。
- 只问最短路条数时，先路由到最短路，再在最短路上计数。

复杂度：

```text
状态数 * 转移数
```

计数/可行性不会改变状态数量，只改变 `dp` 的含义和 merge 方式。

数据范围信号：

- 容量 `W <= 1e5`：一维背包计数/可行性常见。
- 网格 `n*m <= 1e6`：路径计数/可达性常见。
- DAG `n,m <= 2e5`：拓扑计数/可达性常见。
- 数位上界很大：数位 DP 计数。

依赖的标准容器：

- `vector<ll>`：方案数。
- `vector<char>` 或 `vector<int>`：可行性。
- `vector<vector<ll>>`、`vector<vector<char>>`。

输入如何整理：

- 先确认目标是“计数”还是“可行性”。
- 再确认要求是“恰好达到”还是“不超过/任意合法”。
- 如果有取模，统一写 `MOD` 和加法函数。

接口：

```cpp
const ll MOD = 1000000007LL;
```

输出能力：

- 方案数。
- 是否存在合法方案。
- 同时维护可行性和方案数，避免取模后误判。

下游可接：

- DP-05 选/不选 DP
- DP-06/07/08 背包
- DP-12 网格 DP
- DP-15 DAG DP
- DP-17 数位 DP
- DP-19 拼接食谱

可拼接模块：

- Math 取模。
- Topo。
- PrefixSum。

## 计数和可行性的本质区别

| 类型 | `dp` 含义 | 初始值 | 合并方式 | 答案判断 |
|---|---|---|---|---|
| 计数 DP | 有多少种方案到达状态 | `0` | 加法 | 输出数量 |
| 可行性 DP | 状态是否能到达 | `false` | 或运算 | `true/false` |
| 最大值 DP | 到达状态的最大收益 | `-LINF` | `max` | 最大值 |
| 最小值 DP | 到达状态的最小代价 | `LINF` | `min` | 最小值 |

最重要的初始化：

```text
计数：起点 dp[start] = 1，表示“空方案”有 1 种。
可行性：起点 ok[start] = true，表示起点可达。
其他状态：计数为 0，可行性为 false。
```

## 从暴力到计数/可行性

计数和可行性 DP 的动机不是“换一套模板”，而是把暴力搜索的返回值换掉：

```text
暴力问最优值：所有选择里取 max/min。
计数问方案数：所有能到达的前驱方案数相加。
可行性问存在：所有能到达的前驱做 OR。
```

最后一步视角：

```text
背包计数：最后一个动作是“选第 i 个物品”，于是从 j-w[i] 来，ways[j] += ways[j-w[i]]。
网格计数：最后一步从上或左走入 (i,j)，于是 ways[i][j] = ways[i-1][j] + ways[i][j-1]。
DAG 计数：最后一条边是 u -> v，于是 ways[v] += ways[u]。
可行性：同样的前驱关系，把加法换成 ok[v] |= ok[u]。
```

## 取模套路

```cpp
using ll = long long;
const ll MOD = 1000000007LL;

void add_mod(ll& a, ll b) {
    b %= MOD;
    a += b;
    if (a >= MOD) a -= MOD;
}
```

如果一次可能加很多或有乘法：

```cpp
a = (a + b) % MOD;
c = a * b % MOD; // a,b 已经在 MOD 内时 long long 足够装 1e18 以内
```

减法取模：

```cpp
ans = (solve(R) - solve(L - 1) + MOD) % MOD;
```

常见坑：

- 计数题忘记每次加法后取模。
- 可行性题不需要取模。
- `dp[target] == 0` 只表示“方案数模 MOD 为 0”，不一定表示没有方案。若题目还问是否存在，要另开 `ok`。

## 判定套路

计数题：

```text
输出 dp[target]。
```

可行性题：

```cpp
if (ok[target]) cout << "Yes\n";
else cout << "No\n";
```

同时要数量和是否存在：

```cpp
vector<ll> ways(W + 1, 0);
vector<char> ok(W + 1, 0);
ways[0] = 1;
ok[0] = 1;

// 转移时 ways 做加法，ok 做或运算。
```

不要用取模后的 `ways[target] != 0` 代替可行性。

## 套路 1：0/1 背包方案数

题面信号：

```text
每个数最多用一次
问凑出恰好 W 的方案数
```

状态句式：

```text
dp[j] 表示：当前已处理若干物品，凑出和 j 的方案数。
```

初始化：

```text
dp[0] = 1：什么都不选，凑出 0，有 1 种方案。
其他 dp[j] = 0：暂时没有方案。
```

转移：

```cpp
vector<ll> dp(W + 1, 0);
dp[0] = 1;
for (int i = 1; i <= n; i++) {
    for (int j = W; j >= a[i]; j--) {
        dp[j] = (dp[j] + dp[j - a[i]]) % MOD;
    }
}
cout << dp[W] << '\n';
```

循环方向原因：

```text
0/1 背包倒序，防止同一个物品在本轮被重复使用。
```

## 套路 2：完全背包方案数

题面信号：

```text
每种物品可以用无限次
问凑出 W 的方案数
```

转移：

```cpp
vector<ll> dp(W + 1, 0);
dp[0] = 1;
for (int i = 1; i <= n; i++) {
    for (int j = a[i]; j <= W; j++) {
        dp[j] = (dp[j] + dp[j - a[i]]) % MOD;
    }
}
```

循环方向原因：

```text
完全背包正序，允许当前物品在本轮被继续使用。
```

注意：

```text
上面写法统计“组合数”：物品顺序不重要。
如果题目把不同排列也算不同方案，外层通常改成 j，内层枚举物品。
```

排列计数写法：

```cpp
vector<ll> dp(W + 1, 0);
dp[0] = 1;
for (int j = 1; j <= W; j++) {
    for (int i = 1; i <= n; i++) {
        if (j >= a[i]) dp[j] = (dp[j] + dp[j - a[i]]) % MOD;
    }
}
```

## 套路 3：可行性背包

题面信号：

```text
能否凑出 W
是否存在子集满足条件
```

状态句式：

```text
ok[j] 表示：当前已处理若干物品，是否能凑出 j。
```

0/1 版本：

```cpp
vector<char> ok(W + 1, 0);
ok[0] = 1;
for (int i = 1; i <= n; i++) {
    for (int j = W; j >= a[i]; j--) {
        ok[j] = ok[j] || ok[j - a[i]];
    }
}

cout << (ok[W] ? "Yes\n" : "No\n");
```

完全背包版本：

```cpp
vector<char> ok(W + 1, 0);
ok[0] = 1;
for (int i = 1; i <= n; i++) {
    for (int j = a[i]; j <= W; j++) {
        ok[j] = ok[j] || ok[j - a[i]];
    }
}
```

常见坑：

- `vector<bool>` 有特殊压缩行为，初学者更推荐 `vector<char>`。
- `ok[0]=true` 不是说选了东西，而是空方案可达。

## 套路 4：分组计数 / 可行性

题面信号：

```text
每组最多选一个
从每组中选 0 或 1 个
```

计数版本：

```cpp
vector<ll> dp(W + 1, 0);
dp[0] = 1;
for (const auto &group : groups) {
    vector<ll> ndp = dp; // 本组一个也不选
    for (auto item : group) {
        int cost = item.first; // group: vector<pair<int,ll>>，first 是费用
        for (int j = cost; j <= W; j++) {
            ndp[j] = (ndp[j] + dp[j - cost]) % MOD;
        }
    }
    dp.swap(ndp);
}
```

可行性版本：

```cpp
vector<char> ok(W + 1, 0);
ok[0] = 1;
for (const auto &group : groups) {
    vector<char> nok = ok; // 本组不选
    for (auto item : group) {
        int cost = item.first; // group: vector<pair<int,ll>>，first 是费用
        for (int j = cost; j <= W; j++) {
            if (ok[j - cost]) nok[j] = 1;
        }
    }
    ok.swap(nok);
}
```

常见坑：

- 分组题必须从上一组的 `dp` 转到新组 `ndp`。
- 直接在同一个 `dp` 上更新，可能一组里选了多个物品。

## 套路 5：网格路径计数 / 可达性

题面信号：

```text
只能向右/下走
障碍格
问路径条数或能否到达
```

计数：

```cpp
vector<vector<ll>> dp(n + 1, vector<ll>(m + 1, 0));
if (!blocked[1][1]) dp[1][1] = 1;

for (int i = 1; i <= n; i++) {
    for (int j = 1; j <= m; j++) {
        if (blocked[i][j]) {
            dp[i][j] = 0;
            continue;
        }
        if (i == 1 && j == 1) continue;
        dp[i][j] = ((i > 1 ? dp[i - 1][j] : 0) + (j > 1 ? dp[i][j - 1] : 0)) % MOD;
    }
}
```

可达性：

```cpp
vector<vector<char>> ok(n + 1, vector<char>(m + 1, 0));
if (!blocked[1][1]) ok[1][1] = 1;

for (int i = 1; i <= n; i++) {
    for (int j = 1; j <= m; j++) {
        if (blocked[i][j]) continue;
        if (i > 1) ok[i][j] = ok[i][j] || ok[i - 1][j];
        if (j > 1) ok[i][j] = ok[i][j] || ok[i][j - 1];
    }
}
```

常见坑：

- 起点或终点是障碍时答案直接为 0/No。
- 初始化第一行第一列时，障碍后面不能继续继承。

## 套路 6：DAG 路径计数

题面信号：

```text
有向无环图
从 s 到 t 有多少条路径
依赖关系方案数
```

状态句式：

```text
ways[u] 表示：从 s 到 u 的路径数量。
```

转移：

```cpp
vector<ll> ways(n + 1, 0);
ways[s] = 1;
for (int u : topo) {
    for (auto [v, w] : g[u]) {
        ways[v] = (ways[v] + ways[u]) % MOD;
    }
}
cout << ways[t] << '\n';
```

可达性：

```cpp
vector<char> ok(n + 1, 0);
ok[s] = 1;
for (int u : topo) {
    if (!ok[u]) continue;
    for (auto [v, w] : g[u]) ok[v] = 1;
}
```

常见坑：

- 没有拓扑序，普通图上直接这么计数会因为环出错。
- 多个起点时要把所有起点 `ways[x]=1` 或 `ok[x]=1`。

## 套路 7：数位 DP 计数

题面信号：

```text
统计 1..N 中满足数位条件的数
答案取模
```

状态句式：

```text
dfs(pos,tight,leading,state) 返回当前状态后面能组成的合法数量。
```

返回边界：

```cpp
if (pos == len) {
    return legal(state, leading) ? 1 : 0;
}
```

计数转移：

```cpp
ll ans = 0;
for (int d = 0; d <= up; d++) {
    ans = (ans + dfs(pos + 1, ntight, nleading, nstate)) % MOD;
}
```

常见坑：

- 终点返回的是 `1` 或 `0`，不是最优值。
- `[L,R]` 答案做减法时要补 `MOD`。
- 前导零是否算合法数字，要按题面决定。

## 初始化总表

| 场景 | 初始化 |
|---|---|
| 计数，空方案合法 | `dp[0] = 1` |
| 计数，起点为 `s` | `ways[s] = 1` |
| 可行性，空状态可达 | `ok[0] = true` |
| 可行性，起点为 `s` | `ok[s] = true` |
| 恰好选 0 个 | `dp[0][0] = 1` 或 `ok[0][0] = true` |
| 其他状态 | 计数为 `0`，可行性为 `false` |

## 转移总表

| 类型 | merge 写法 |
|---|---|
| 计数 | `dp[to] = (dp[to] + dp[from]) % MOD` |
| 可行性 | `ok[to] = ok[to] || ok[from]` |
| 计数带权选择 | `dp[next] += dp[cur]`，权值只影响 `next` |
| 最优值 | `max/min`，不要和计数加法混用 |

## 答案位置总表

| 题面 | 答案 |
|---|---|
| 恰好凑出 W | `dp[W]` / `ok[W]` |
| 不超过 W 任意合法 | `sum(dp[0..W])` 或 `any(ok[0..W])` |
| 恰好选 K 个 | `dp[K]` / `ok[K]` |
| 网格到终点 | `dp[n][m]` / `ok[n][m]` |
| DAG 从 s 到 t | `ways[t]` / `ok[t]` |
| 数位范围 | `solve(R) - solve(L - 1)` |

常见坑：

- “至多 W”却只输出 `dp[W]`。
- “恰好 W”却把 `dp[0..W]` 全加了。
- 方案数题把初值设成 `-LINF`。
- 可行性题把 `ok` 默认成 `true`。
- 组合数和排列数循环顺序写反。

暴力/部分分替代：

- 小数据先 DFS 枚举所有选择，遇到合法方案 `ans++` 或设置 `found=true`。
- DFS 能重复到同一状态时，把返回值从最优值改成“方案数/是否可行”。
- 背包循环方向拿不准时，先写二维 `dp[i][j]`，确认后再压成一维。

升级方向：

- 计数 DFS -> 记忆化计数 -> 表推计数。
- 可行性 DFS -> `ok` 表。
- 二维背包 -> 一维滚动。
- DAG DFS 计数 -> Topo 计数。
- 数位暴力枚举 -> 数位 DP 计数。

最小测试样例：

```text
物品：1 2 3，目标 W=3

0/1 方案数：2
方案：{3}, {1,2}

0/1 可行性：Yes

完全背包组合方案数：3
方案：{1+1+1}, {1+2}, {3}
```
