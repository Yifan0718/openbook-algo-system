# DP-24：背包常见变体总表

模型编号：DP-24

模型名称：背包常见变体总表

标签：DP、背包、多重背包、二维背包、价值维度、计数、可行性

一句话用途：把 0/1、完全、分组之外的背包变体集中成一张考场路由卡，先判循环顺序和初始化，再抄短模板。

题面触发词：

- “每种物品最多选 k 个”
- “重量和体积两个限制”
- “价值总和较小，容量很大”
- “问方案数/能否凑出/最少硬币数”
- “每组必须选一个”
- “依赖关系、选父才能选子”

什么时候用：

- 题目本质是“从若干物品/方案中选择”，并受容量、预算、数量、体积等资源限制。
- 资源维度较小，或可以把较小的维度作为 DP 下标。
- 正解不明显时，可先写 `dfs(i, rest)` 记忆化，再改表推。

不要什么时候用：

- 容量上限巨大且没有可替代小维度，普通背包会爆内存。
- 选择之间有复杂图关系，不能只靠容量表达。
- 明显是区间合并、最短路、排序贪心，不要硬套背包。
- 物品价值可能为负时，初始化和答案位置要重新检查。

复杂度：

- 0/1、完全、分组：常见 `O(nW)`。
- 多重背包二进制拆分：`O(W * sum(log cnt[i]))`。
- 二维背包：`O(n W V)`。
- 价值维度背包：`O(n * sum_value)`。
- bitset 可行性：约 `O(nW/word)`，代码很短。

数据范围信号：

- `n * W <= 1e7`：容量维度背包较稳。
- `W` 很大但 `sum(v) <= 1e5`：价值维度背包。
- `W1 * W2 * n <= 1e7`：二维背包可考虑。
- `cnt[i]` 很大但有上限：二进制拆分或单调队列优化，多数考场先用二进制拆分。

依赖的标准容器：

- `vector<int> w, cnt`
- `vector<ll> v, dp`
- `bitset<MAXW + 1>` 或 `vector<char> reachable`

输入如何整理：

- 统一 `w[i]` 表示容量消耗，`v[i]` 表示价值或收益。
- 多重背包额外读 `cnt[i]`。
- 二维背包读 `w1[i], w2[i], val[i]`。
- 分组/依赖题先整理成组或树，再做背包合并。

接口：

```cpp
ll multiple_knapsack_binary(int n, int W, vector<int>& w, vector<ll>& v, vector<int>& cnt);
ll value_dimension_knapsack(int n, long long W, vector<int>& w, vector<int>& v);
```

输出能力：

- 最大价值。
- 最小花费。
- 是否可达。
- 方案数。
- 每组最多/必须选一个。

下游可接：

- DP-06 0/1 背包
- DP-07 完全背包
- DP-08 分组背包
- DP-14 树形 DP
- DP-20 计数/可行性 DP

可拼接模块：

- BRUTE 选/不选 DFS：小数据或先写记忆化。
- PrefixSum/MonotonicQueue：高级多重背包优化。
- TreeDP：依赖背包、树上背包。

## 1. 背包变体路由表

| 题面 | 模型 | 核心写法 |
|---|---|---|
| 每个物品最多一次 | 0/1 背包 | 容量倒序 |
| 每种物品无限个 | 完全背包 | 容量正序 |
| 每种物品最多 `cnt[i]` 个 | 多重背包 | 二进制拆成若干 0/1 物品 |
| 每组最多选一个 | 分组背包 | 每组用 `ndp` |
| 每组必须选一个 | 必选分组背包 | `ndp` 初始化为 `-LINF` |
| 两个容量限制 | 二维背包 | 两层容量都倒序 |
| 容量巨大，价值和小 | 价值维度背包 | `dp[value]=最小重量` |
| 问能否凑出 | 可行性背包 | `bool dp[j]` 或 `bitset` |
| 问方案数 | 计数背包 | 注意组合数/排列数循环顺序 |
| 问最少硬币数 | 最短背包 | `dp[j]=min(dp[j],dp[j-w]+1)` |
| 树上选 K 个点、子树容量合并 | 树上背包 | DP-14 + DP-19，容量合并 |
| 选父才能选子 | 依赖背包 | 先建依赖树；和“树上任选 K 个”不是同一题 |

## 1A. 背包变体建模口令

背包的共同核心不是“背模板”，而是把题目翻译成资源坐标：

```text
dp[资源用量] = 当前能得到的最好答案 / 方案数 / 是否可行
最后一步 = 最后考虑的那个物品到底选了几次
```

然后按题面把资源轴和物品规则调整：

| 发现的问题 | 对状态/循环的影响 | 动机 |
|---|---|---|
| 每件最多一次 | 容量倒序 | 防止同一件在本轮被重复使用 |
| 每件无限次 | 容量正序 | 允许本轮刚更新的状态继续使用同一件 |
| 每件最多 `cnt` 次 | 拆成若干 0/1 物品或单调队列 | 把“有限次数”转回熟悉的 0/1 规则 |
| 有两个资源限制 | `dp[w1][w2]` 升维 | 单独知道重量不够，还要知道体积/时间 |
| 容量很大但价值小 | `dp[value]=最小重量` 换维度 | 用小的那一维做下标 |
| 要计数 | `dp[j] += dp[j-w]` | 最后一步从能到达 `j-w` 的方案接过来 |

如果一维 `dp[j]` 写不明白，先写二维 `dp[i][j]`；二维清楚后再滚动成一维。

## 2. 多重背包：二进制拆分成 0/1

二进制拆分的动机：如果一种物品最多取 `13` 个，不必枚举 `0..13` 每个数量。把它拆成 `1,2,4,6` 四包，每包只能选或不选，就能表示 `0..13` 的任意数量，同时直接套 0/1 背包倒序循环。

```cpp
ll multiple_knapsack_binary(int n, int W, vector<int>& w, vector<ll>& v, vector<int>& cnt) {
    vector<int> nw;
    vector<ll> nv;
    nw.push_back(0);
    nv.push_back(0);

    for (int i = 1; i <= n; i++) {
        long long c = cnt[i];
        for (long long k = 1; k <= c; k <<= 1) {
            long long packed_w = 1LL * w[i] * k;
            nw.push_back(packed_w > W ? W + 1 : (int)packed_w);
            nv.push_back(v[i] * k);
            c -= k;
        }
        if (c > 0) {
            long long packed_w = 1LL * w[i] * c;
            nw.push_back(packed_w > W ? W + 1 : (int)packed_w);
            nv.push_back(v[i] * c);
        }
    }

    vector<ll> dp(W + 1, 0);
    for (int i = 1; i < (int)nw.size(); i++) {
        for (int j = W; j >= nw[i]; j--) {
            dp[j] = max(dp[j], dp[j - nw[i]] + nv[i]);
        }
    }
    return dp[W];
}
```

## 3. 二维背包

例如同时限制重量 `A` 和体积 `B`。

```cpp
vector<vector<ll>> dp(A + 1, vector<ll>(B + 1, 0));
for (int i = 1; i <= n; i++) {
    for (int a = A; a >= w1[i]; a--) {
        for (int b = B; b >= w2[i]; b--) {
            dp[a][b] = max(dp[a][b], dp[a - w1[i]][b - w2[i]] + val[i]);
        }
    }
}
cout << dp[A][B] << '\n';
```

## 4. 价值维度背包

当 `W` 很大但总价值小，用 `dp[value] = 达到该价值的最小重量`。

```cpp
ll value_dimension_knapsack(int n, long long W, vector<int>& w, vector<int>& v) {
    int V = 0;
    for (int i = 1; i <= n; i++) V += v[i];

    const long long INF = numeric_limits<long long>::max() / 4;
    vector<long long> dp(V + 1, INF);
    dp[0] = 0;

    for (int i = 1; i <= n; i++) {
        for (int val = V; val >= v[i]; val--) {
            if (dp[val - v[i]] != INF) {
                dp[val] = min(dp[val], dp[val - v[i]] + w[i]);
            }
        }
    }

    int ans = 0;
    for (int val = 0; val <= V; val++) {
        if (dp[val] <= W) ans = val;
    }
    return ans;
}
```

## 5. 可行性背包 bitset

只问某个和能不能凑出时非常好抄。

```cpp
bitset<100005> can;
can[0] = 1;
for (int i = 1; i <= n; i++) {
    can |= (can << w[i]); // 0/1 可达性
}
cout << (can[target] ? "Yes" : "No") << '\n';
```

如果 `target` 不是编译期常量，改用 `vector<char>` 普通背包。

## 6. 组合数 vs 排列数

完全背包计数最容易错。

组合数：不关心顺序，`1+2` 和 `2+1` 算同一种。

```cpp
vector<int> dp(W + 1, 0);
dp[0] = 1;
for (int i = 1; i <= n; i++) {
    for (int j = w[i]; j <= W; j++) {
        dp[j] = (dp[j] + dp[j - w[i]]) % MOD;
    }
}
```

排列数：关心顺序，`1+2` 和 `2+1` 算两种。

```cpp
vector<int> dp(W + 1, 0);
dp[0] = 1;
for (int j = 1; j <= W; j++) {
    for (int i = 1; i <= n; i++) {
        if (j >= w[i]) dp[j] = (dp[j] + dp[j - w[i]]) % MOD;
    }
}
```

## 7. 至少装满的最小代价

题面常见说法：“至少达到 `W` 的容量/攻击力/分数，花费最小”。推荐容量封顶：超过 `W` 的状态都合并到 `W`。

```cpp
long long at_least_knapsack_min_cost(int n, int W, vector<int>& gain, vector<int>& cost) {
    const long long INF = numeric_limits<long long>::max() / 4;
    vector<long long> dp(W + 1, INF);
    dp[0] = 0;

    for (int i = 1; i <= n; i++) {
        vector<long long> ndp = dp;
        for (int j = 0; j <= W; j++) {
            if (dp[j] == INF) continue;
            int nj = min(W, j + gain[i]);
            ndp[nj] = min(ndp[nj], dp[j] + cost[i]);
        }
        dp.swap(ndp);
    }
    return dp[W] == INF ? -1 : dp[W];
}
```

如果每个物品可以无限选，把 `ndp` 改成原地正序更新，但考场不确定时先写 0/1 版本保稳。

## 8. 0/1 背包路径恢复：二维 take

初学者要输出选了哪些物品时，优先用二维表，别急着一维恢复。

```cpp
vector<int> restore_zero_one_items(int n, int W, vector<int>& w, vector<int>& v) {
    vector<vector<int>> dp(n + 1, vector<int>(W + 1, 0));
    vector<vector<char>> take(n + 1, vector<char>(W + 1, 0));

    for (int i = 1; i <= n; i++) {
        for (int j = 0; j <= W; j++) {
            dp[i][j] = dp[i - 1][j];
            if (j >= w[i] && dp[i - 1][j - w[i]] + v[i] > dp[i][j]) {
                dp[i][j] = dp[i - 1][j - w[i]] + v[i];
                take[i][j] = 1;
            }
        }
    }

    vector<int> chosen;
    int j = W;
    for (int i = n; i >= 1; i--) {
        if (take[i][j]) {
            chosen.push_back(i);
            j -= w[i];
        }
    }
    reverse(chosen.begin(), chosen.end());
    return chosen;
}
```

若题目要求“恰好装满”，二维 `dp` 要用不可达初始化，不能默认全 0。

常见坑：

- 多重背包直接正序更新，会把数量上限冲掉。
- 二维背包如果每个物品最多一次，两个容量都要倒序。
- 价值维度里 `dp[value]` 存重量，不是价值。
- 可行性/恰好装满必须初始化不可达状态，不能全 0。
- 完全背包计数要先区分组合数和排列数。
- 分组“必须选一个”不能 `ndp = dp`。
- “至少装满”不要直接访问超过 `W` 的下标，推荐容量封顶。
- 一维背包路径恢复容易被覆盖；初学者优先二维 `take`。

暴力/部分分替代：

- `n <= 25`：DFS 枚举每件选/不选。
- 多重背包数量小：DFS 枚举每种取几个。
- 容量小：`dfs(i, rest)` 加记忆化。
- 不确定一维循环方向时，先写二维 `dp[i][j]`。

升级方向：

```text
DFS 选物品 -> 0/1 背包
数量无限 -> 完全背包
数量有限 -> 二进制拆分
两种资源 -> 二维背包
容量太大 -> 价值维度
只问能否 -> bitset/可行性背包
问方案数 -> 计数背包，先判组合/排列
```

最小测试样例：

```text
多重背包：
2 10
2 3 3
3 4 2
输出：14
说明：3 个第一种 + 1 个第二种，容量 9，价值 13；2 个第一种 + 2 个第二种，容量 10，价值 14。
```
