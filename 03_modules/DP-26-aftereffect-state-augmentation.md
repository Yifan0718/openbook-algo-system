# DP-26：发现有后效性怎么办：升维吸收关键历史

模块编号：DP-26

模块名称：发现有后效性怎么办：升维吸收关键历史

标签：DP、无后效性、有后效性、状态升维、last、used、phase、网格 DP

一句话用途：当你发现 `dp[i]` 或 `dp[i][j]` 不够用，因为“前面怎么来的”会影响后面选择时，把那一点关键历史加进状态，让新状态重新满足无后效性。

题面触发词：

- “不能连续两次做某操作”
- “相邻不能相同”
- “上一步方向/颜色/动作影响下一步”
- “最多使用一次机会”
- “是否已经使用过某个技能/优惠/钥匙”
- “当前处于持有/冷却/空闲状态”
- “恰好选 K 个，同时还有相邻限制”

什么时候用：

- 两个局面的位置相同，但因为历史不同，后续合法选择不同。
- 转移时你忍不住想看 `path`、`lastMove`、`used`、`previousColor` 这类变量。
- 记忆化搜索中，同样的 `dfs(pos)` 得不到唯一答案，必须改成 `dfs(pos, extra_state)`。

不要什么时候用：

- 历史信息能由当前位置唯一推出，不需要重复加维。
- 历史只影响当前得分，不影响未来合法选择，可能直接在转移里处理即可。
- 升维后状态数爆炸，例如 `n * m * 2^k` 中 `k` 太大，要考虑换模型或只保留更小摘要。
- 图上可以任意回头且有环时，不一定是 DP，可能要 BFS/Dijkstra/状态搜索。

复杂度：

```text
升维后复杂度 = 原状态数 * 新维度大小 * 每个状态转移数
```

例如：

- `dp[i][j]` 加上一维上一步方向 `2`：状态数变成 `2*n*m`。
- `dp[i]` 加上是否选择当前元素 `2`：状态数变成 `2*n`。
- `dp[i][j]` 加上是否用过一次机会 `2`：状态数变成 `2*n*m`。
- `dp[i]` 加上已选数量 `K` 和当前是否选 `2`：状态数变成 `2*n*K`。

数据范围信号：

- 新维度只有 `2/3/10` 种：通常很稳。
- 新维度是容量 `W`：看 `nW` 是否可承受。
- 新维度是集合 `mask`：要求元素数通常 `n <= 20`。

依赖的标准容器：

- `vector`
- `array<ll, 2>`
- `array<ll, 3>`
- `vector<vector<array<ll, 2>>>`
- `vector<vector<vector<ll>>>`

输入如何整理：

- 先写错误状态，例如 `dp[i][j]`。
- 找反例：同一个 `(i,j)`，不同历史导致下一步能做的选择不同。
- 把这个关键历史压成小整数：`last/used/color/phase/taken`。

接口：

```text
错误状态 -> 找出影响未来的关键历史 -> 加一维 -> 新状态转移
```

输出能力：

- 最大收益。
- 最小代价。
- 方案数。
- 是否可行。

下游可接：

- DP-03B 状态增维路由。
- DP-12 网格 DP。
- DP-04/05 线性 DP、选/不选 DP。
- DP-25 暴力 DFS 到记忆化搜索。

可拼接模块：

- GridDP：位置 `(i,j)`。
- ChooseOrSkip：选择状态 `0/1`。
- MemoDFS：先写 `dfs(..., last, used)`。

## 1. 核心原则

```text
有后效性 = 同一个旧状态，未来不唯一。
破局方法 = 把影响未来的那一点历史加进状态。
```

升维不是乱加维度，而是只加“未来还需要知道”的最小历史摘要。

检查句式：

```text
只知道我在 X，下一步能做什么是否唯一？
如果不唯一，还差哪一点历史？
把那一点历史变成状态下标。
```

## 2. 例题一：网格最大收益，不能连续向下走两步

题意：

```text
给 n*m 网格，每格有收益。
从 (1,1) 走到 (n,m)，每步只能向下或向右。
规则：不能连续向下走两步。
求最大收益。
```

错误状态：

```text
dp[i][j] = 到达 (i,j) 的最大收益
```

为什么错：

```text
同样到达 (i,j)，如果上一步是向下，下一步不能继续向下。
如果上一步是向右，下一步可以向下。
只知道 (i,j) 不够，未来不唯一。
```

正确升维：

```text
dp[i][j][0] = 到达 (i,j)，且最后一步是向下的最大收益
dp[i][j][1] = 到达 (i,j)，且最后一步是向右的最大收益
```

转移：

```text
最后一步向下：只能从上方来，且上一个状态最后一步不能也是向下。
dp[i][j][0] = dp[i-1][j][1] + a[i][j]

最后一步向右：从左方来，上一步方向不限。
dp[i][j][1] = max(dp[i][j-1][0], dp[i][j-1][1]) + a[i][j]
```

完整 C++17：

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;
const ll NEG = numeric_limits<ll>::min() / 4;
const int MAXN = 1000 + 5;
const int MAXM = 1000 + 5;
static ll a[MAXN][MAXM];
static ll dp[MAXN][MAXM][2];

ll max_grid_no_two_down(int n, int m) {
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            dp[i][j][0] = dp[i][j][1] = NEG;
        }
    }

    dp[1][1][0] = a[1][1];
    dp[1][1][1] = a[1][1];

    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            if (i == 1 && j == 1) continue;

            if (i > 1 && dp[i - 1][j][1] != NEG) {
                dp[i][j][0] = max(dp[i][j][0], dp[i - 1][j][1] + a[i][j]);
            }
            if (j > 1) {
                ll best_left = max(dp[i][j - 1][0], dp[i][j - 1][1]);
                if (best_left != NEG) {
                    dp[i][j][1] = max(dp[i][j][1], best_left + a[i][j]);
                }
            }
        }
    }

    ll ans = max(dp[n][m][0], dp[n][m][1]);
    return ans == NEG ? -1 : ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            cin >> a[i][j];
        }
    }

    cout << max_grid_no_two_down(n, m) << '\n';
    return 0;
}
```

最小测试：

```text
3 2
1 1
100 1
100 1
输出：103
说明：不能走下、下、右；可走下、右、下。
```

## 3. 例题二：爬楼梯，不能连续跳同样步数

题意：

```text
从第 0 级爬到第 n 级，每次跳 1 或 2 级。
不能连续两次跳同样步数。
问方案数。
```

错误状态：

```text
dp[i] = 到达第 i 级的方案数
```

为什么错：

```text
同样到达第 i 级，如果上一跳是 1，下一跳不能跳 1。
如果上一跳是 2，下一跳不能跳 2。
只知道 i 不够。
```

正确状态：

```text
dp[i][last] = 到达第 i 级，上一跳是 last 的方案数
last=0 表示起点还没有上一跳，last=1/2 表示上一跳步数。
```

完整 C++17：

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;
const int MOD = 1000000007;

int count_stairs_no_same_jump(int n) {
    if (n == 0) return 1;
    vector<array<int, 3>> dp(n + 1);
    dp[0][0] = 1;

    for (int i = 0; i <= n; i++) {
        for (int last = 0; last <= 2; last++) {
            if (dp[i][last] == 0) continue;
            for (int step = 1; step <= 2; step++) {
                if (step == last) continue;
                if (i + step <= n) {
                    dp[i + step][step] += dp[i][last];
                    if (dp[i + step][step] >= MOD) dp[i + step][step] -= MOD;
                }
            }
        }
    }

    return (dp[n][1] + dp[n][2]) % MOD;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;

    cout << count_stairs_no_same_jump(n) << '\n';
    return 0;
}
```

最小测试：

```text
4
输出：1
说明：只能 1,2,1。
```

## 4. 例题三：恰好选 K 个数，且不能选相邻

题意：

```text
给 n 个数，恰好选 K 个，不能选相邻位置，求最大和。
```

错误状态：

```text
dp[i][cnt] = 处理完前 i 个，已经选 cnt 个的最大和
```

为什么还不够：

```text
处理第 i+1 个时，需要知道第 i 个是否已经选了。
如果第 i 个选了，第 i+1 个不能选；如果没选，就可以选。
```

正确状态：

```text
dp[i][cnt][0] = 处理完前 i 个，选了 cnt 个，且第 i 个没选的最大和
dp[i][cnt][1] = 处理完前 i 个，选了 cnt 个，且第 i 个选了的最大和
```

完整 C++17：

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;
const ll NEG = numeric_limits<ll>::min() / 4;

ll max_sum_choose_k_no_adjacent(const vector<ll>& a, int K) {
    int n = (int)a.size() - 1;
    vector<vector<array<ll, 2>>> dp(n + 1, vector<array<ll, 2>>(K + 1, {NEG, NEG}));

    dp[0][0][0] = 0;
    for (int i = 1; i <= n; i++) {
        for (int cnt = 0; cnt <= K; cnt++) {
            dp[i][cnt][0] = max(dp[i - 1][cnt][0], dp[i - 1][cnt][1]);
            if (cnt > 0 && dp[i - 1][cnt - 1][0] != NEG) {
                dp[i][cnt][1] = dp[i - 1][cnt - 1][0] + a[i];
            }
        }
    }

    ll ans = max(dp[n][K][0], dp[n][K][1]);
    return ans == NEG ? -1 : ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, K;
    cin >> n >> K;
    vector<ll> a(n + 1);
    for (int i = 1; i <= n; i++) cin >> a[i];

    cout << max_sum_choose_k_no_adjacent(a, K) << '\n';
    return 0;
}
```

最小测试：

```text
5 2
2 7 9 3 1
输出：11
说明：选 2 和 9。
```

## 5. 例题四：网格最大收益，最多一次收益翻倍

题意：

```text
从 (1,1) 到 (n,m)，只能向右或向下。
可以选择最多一个格子，把该格收益翻倍。
求最大收益。
```

有后效性的地方：

```text
同样走到 (i,j)，如果已经用过翻倍机会，后面就不能再用。
如果还没用过，后面仍然可以用。
```

正确状态：

```text
dp[i][j][0] = 到达 (i,j)，还没用过翻倍机会的最大收益
dp[i][j][1] = 到达 (i,j)，已经用过翻倍机会的最大收益
```

完整 C++17：

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;
const ll NEG = numeric_limits<ll>::min() / 4;

ll max_grid_one_double(int n, int m, vector<vector<ll>>& a) {
    vector<vector<array<ll, 2>>> dp(n + 1, vector<array<ll, 2>>(m + 1, {NEG, NEG}));

    dp[1][1][0] = a[1][1];
    dp[1][1][1] = a[1][1] * 2;

    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            if (i == 1 && j == 1) continue;

            array<ll, 2> best = {NEG, NEG};
            if (i > 1) {
                best[0] = max(best[0], dp[i - 1][j][0]);
                best[1] = max(best[1], dp[i - 1][j][1]);
            }
            if (j > 1) {
                best[0] = max(best[0], dp[i][j - 1][0]);
                best[1] = max(best[1], dp[i][j - 1][1]);
            }

            if (best[0] != NEG) {
                dp[i][j][0] = max(dp[i][j][0], best[0] + a[i][j]);
                dp[i][j][1] = max(dp[i][j][1], best[0] + 2 * a[i][j]);
            }
            if (best[1] != NEG) {
                dp[i][j][1] = max(dp[i][j][1], best[1] + a[i][j]);
            }
        }
    }

    ll ans = max(dp[n][m][0], dp[n][m][1]);
    return ans == NEG ? -1 : ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;
    vector<vector<ll>> a(n + 1, vector<ll>(m + 1));
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            cin >> a[i][j];
        }
    }

    cout << max_grid_one_double(n, m, a) << '\n';
    return 0;
}
```

最小测试：

```text
2 2
1 10
2 3
输出：24
说明：路径 1->10->3，并把 10 翻倍。
```

## 6. 例题五：股票买卖，冷冻期一天

题意：

```text
给每天股价。每天可以不动、买入、卖出。
卖出后的下一天不能买入，求最大收益。
```

错误状态：

```text
dp[i] = 第 i 天结束后的最大收益
```

为什么错：

```text
同样第 i 天结束，有可能手里持股、空闲、刚卖出处于冷冻。
这三种状态下一天能做的操作不同。
```

正确状态：

```text
hold = 手里持股
free = 手里没股且不在冷冻，可买
cool = 今天刚卖出，下一天冷冻
```

完整 C++17：

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;
const ll NEG = numeric_limits<ll>::min() / 4;

ll max_profit_with_cooldown(const vector<ll>& price) {
    int n = (int)price.size() - 1;
    vector<array<ll, 3>> dp(n + 1, {NEG, NEG, NEG});

    dp[0][0] = NEG; // hold
    dp[0][1] = 0;   // free
    dp[0][2] = NEG; // cool

    for (int i = 1; i <= n; i++) {
        dp[i][0] = max(dp[i - 1][0], dp[i - 1][1] - price[i]);
        dp[i][1] = max(dp[i - 1][1], dp[i - 1][2]);
        dp[i][2] = dp[i - 1][0] + price[i];
    }

    return max(dp[n][1], dp[n][2]);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<ll> price(n + 1);
    for (int i = 1; i <= n; i++) cin >> price[i];

    cout << max_profit_with_cooldown(price) << '\n';
    return 0;
}
```

最小测试：

```text
5
1 2 3 0 2
输出：3
```

## 7. 升维清单

| 发现的问题 | 加什么维度 | 典型状态 |
|---|---|---|
| 上一步动作影响下一步 | `lastMove` | `dp[i][j][lastMove]` |
| 相邻不能相同 | `lastColor/lastValue` | `dp[i][last]` |
| 当前元素选没选影响下一个 | `take` | `dp[i][0/1]` |
| 机会是否用过 | `used` | `dp[i][j][used]` |
| 还剩几次机会 | `rest` | `dp[i][rest]` |
| 处于持有/冷却/空闲 | `phase` | `dp[i][phase]` |
| 已访问哪些点 | `mask` | `dp[mask][last]` |

## 8. 从 DFS 角度理解升维

如果你先写 DFS，升维会更自然：

```text
不能连续向下：
dfs(i, j, lastMove)

不能连续同样跳法：
dfs(pos, lastStep)

恰好选 K 且不能相邻：
dfs(i, cnt, prevTaken)

最多一次翻倍：
dfs(i, j, used)

股票冷冻期：
dfs(day, phase)
```

这时 DFS 的可变参数就是 memo 的 key，也是表推 DP 的下标。

常见坑：

- 忘记把影响未来的变量放进 memo key，导致不同历史被错误合并。
- 加了太多无关历史，状态数爆炸。
- `last` 的初始值没有设计好；可以用特殊值，或像网格例题那样给起点两个虚拟方向。
- 最大值题初始不可达状态要用 `NEG`，不要默认 0。
- 允许负收益时，默认 0 会错误地制造一条不存在的路径。

暴力/部分分替代：

- 先写 `dfs(..., last/used/phase)`。
- 小数据不加 memo 也能跑。
- 中数据加 `memo`。
- 状态小且无环后，再改成表推 DP。

升级方向：

```text
错误 dp[i][j]
-> 找到导致未来不同的历史 last/used/phase
-> dp[i][j][last]
-> memo DFS 或表推
-> 如果维度太大，压缩/换模型
```

最小测试样例：

```text
网格不能连续向下：
3 2
1 1
100 1
100 1
输出：103

爬楼梯不能连续同样跳法：
4
输出：1

恰好选 K 且不能相邻：
5 2
2 7 9 3 1
输出：11
```
