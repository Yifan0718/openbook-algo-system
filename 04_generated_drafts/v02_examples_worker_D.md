# v0.2 例题扩展 Worker D：第 3 卷 DP 建模与模型复用

本文件只负责第 3 卷 DP 例题扩展。每题都包含题面、输入输出、样例、完整 C++17 代码、测试设计和 DP motivation，便于自动抽取与运行验证。

### V03-EX01 最小体力跳石子

- 归属卷：第 3 卷
- 覆盖模块：DP-03 从暴力到记忆化，DP-25 DFS 记忆化案例
- 考场用途：先写暴力递归，再把重复子问题缓存成记忆化 DFS

**题目描述：** 有 `n` 块石子排成一行，编号 `1..n`，踩到第 `i` 块石子需要消耗 `cost[i]`。你从编号 `0` 的起点出发，每次可以跳到后面第 `1` 块或第 `2` 块石子，必须最后落到第 `n` 块石子。求最小总消耗。

**输入格式：** 第一行一个整数 `n`。第二行 `n` 个整数，表示 `cost[1..n]`。

**输出格式：** 输出一个整数，表示最小总消耗。

**样例输入：**
```text
6
10 15 20 1 5 1
```

**样例输出：**
```text
17
```

**Motivation：** 状态定义为 `dfs(i)`：从起点跳到第 `i` 块石子的最小消耗。这样定义是因为到达第 `i` 块以后，前面具体怎么跳不再影响答案，只需要知道当前位置。最后一步只能从 `i-1` 或 `i-2` 跳来，所以 `dfs(i)=cost[i]+min(dfs(i-1),dfs(i-2))`。朴素递归会重复计算同一个 `i`，加 `memo[i]` 后每个状态只算一次。复杂度 `O(n)`，空间 `O(n)`。

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

const long long INF = 4'000'000'000'000'000'000LL;
int n;
vector<long long> cost_value;
vector<long long> memo;

long long dfs(int i) {
    if (i == 0) return 0;
    if (i < 0) return INF;
    if (memo[i] != -1) return memo[i];
    long long best = min(dfs(i - 1), dfs(i - 2));
    memo[i] = best + cost_value[i];
    return memo[i];
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n;
    cost_value.assign(n + 1, 0);
    memo.assign(n + 1, -1);
    for (int i = 1; i <= n; i++) {
        cin >> cost_value[i];
    }
    cout << dfs(n) << '\n';
    return 0;
}
```

**测试设计：**

测试 1 输入：
```text
1
7
```
期望输出：
```text
7
```

测试 2 输入：
```text
5
5 100 5 100 5
```
期望输出：
```text
15
```

### V03-EX02 快速求和最少加号

- 归属卷：第 3 卷
- 覆盖模块：DP-21 P1874 快速求和建模例题，DP-20 计数与可行性 DP
- 考场用途：字符串切分题从指数枚举升级为位置加累计和 DP

**题目描述：** 给定一个只包含数字的字符串 `s` 和目标值 `target`。你可以在相邻数字之间插入若干个加号，把字符串切成若干段。每段按十进制整数解释，前导零允许。求表达式和等于 `target` 时最少需要插入多少个加号；如果无法做到，输出 `-1`。

**输入格式：** 第一行一个数字字符串 `s`。第二行一个整数 `target`。

**输出格式：** 输出最少加号数；无解输出 `-1`。

**样例输入：**
```text
99999
45
```

**样例输出：**
```text
4
```

**Motivation：** 状态定义为 `dp[i][sum]`：使用前 `i` 个字符，已经切出的段和为 `sum` 时，最少切出多少段。这样定义是因为后续只关心已经处理到的位置和当前累计和，不关心前面每段具体怎么切。最后一步是选择最后一段 `s[i+1..j]`，把 `dp[i][sum]` 转移到 `dp[j][sum+value]`。答案是段数减一，即加号数。复杂度约为 `O(n^2 * target)`，空间 `O(n * target)`。

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string s;
    int target;
    cin >> s >> target;
    int n = (int)s.size();
    const int INF = 1'000'000'000;
    vector<vector<int>> dp(n + 1, vector<int>(target + 1, INF));
    dp[0][0] = 0;

    for (int i = 0; i < n; i++) {
        for (int sum = 0; sum <= target; sum++) {
            if (dp[i][sum] == INF) continue;
            long long value = 0;
            for (int j = i + 1; j <= n; j++) {
                value = value * 10 + (s[j - 1] - '0');
                if (value > target) break;
                if (sum + value <= target) {
                    dp[j][sum + (int)value] = min(dp[j][sum + (int)value], dp[i][sum] + 1);
                }
            }
        }
    }

    if (dp[n][target] == INF) {
        cout << -1 << '\n';
    } else {
        cout << dp[n][target] - 1 << '\n';
    }
    return 0;
}
```

**测试设计：**

测试 1 输入：
```text
1234
10
```
期望输出：
```text
3
```

测试 2 输入：
```text
105
6
```
期望输出：
```text
1
```

### V03-EX03 编辑距离

- 归属卷：第 3 卷
- 覆盖模块：DP-10 编辑距离，DP-22 编辑距离建模例题
- 考场用途：两个字符串最少增删改操作的标准二维 DP

**题目描述：** 给定两个字符串 `a` 和 `b`。一次操作可以插入一个字符、删除一个字符或替换一个字符。求把 `a` 变成 `b` 的最少操作次数。

**输入格式：** 第一行字符串 `a`。第二行字符串 `b`。

**输出格式：** 输出一个整数，表示最少操作次数。

**样例输入：**
```text
kitten
sitting
```

**样例输出：**
```text
3
```

**Motivation：** 状态定义为 `dp[i][j]`：把 `a` 的前 `i` 个字符变成 `b` 的前 `j` 个字符的最少操作数。这样定义是因为任意最优方案最后只会落在两个前缀之间。最后一步有四类：字符相等时不操作，从 `dp[i-1][j-1]` 来；否则可以替换、删除或插入。复杂度 `O(nm)`，空间 `O(nm)`。

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string a, b;
    cin >> a >> b;
    int n = (int)a.size();
    int m = (int)b.size();
    a = " " + a;
    b = " " + b;

    vector<vector<int>> dp(n + 1, vector<int>(m + 1, 0));
    for (int i = 1; i <= n; i++) dp[i][0] = i;
    for (int j = 1; j <= m; j++) dp[0][j] = j;

    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            if (a[i] == b[j]) {
                dp[i][j] = dp[i - 1][j - 1];
            } else {
                int replace_cost = dp[i - 1][j - 1] + 1;
                int delete_cost = dp[i - 1][j] + 1;
                int insert_cost = dp[i][j - 1] + 1;
                dp[i][j] = min(replace_cost, min(delete_cost, insert_cost));
            }
        }
    }

    cout << dp[n][m] << '\n';
    return 0;
}
```

**测试设计：**

测试 1 输入：
```text
abc
abc
```
期望输出：
```text
0
```

测试 2 输入：
```text
abc
yabd
```
期望输出：
```text
2
```

### V03-EX04 0/1 背包最大价值

- 归属卷：第 3 卷
- 覆盖模块：DP-06 0/1 背包，DP-05 选或不选
- 考场用途：每件物品最多选一次，容量限制下求最大价值

**题目描述：** 有 `n` 件物品和容量为 `W` 的背包。第 `i` 件物品重量为 `w[i]`，价值为 `v[i]`，每件物品最多选一次。求不超过容量时的最大总价值。

**输入格式：** 第一行两个整数 `n W`。接下来 `n` 行，每行两个整数 `w[i] v[i]`。

**输出格式：** 输出一个整数，表示最大总价值。

**样例输入：**
```text
4 7
3 4
4 5
2 3
3 7
```

**样例输出：**
```text
12
```

**Motivation：** 状态定义为 `dp[j]`：已经处理若干件物品后，容量不超过 `j` 的最大价值。处理第 `i` 件物品时，最后选择只有两种：不选它，或者从 `j-w[i]` 转移并选它。因为每件物品只能选一次，容量循环必须从大到小，防止同一件物品被重复使用。复杂度 `O(nW)`，空间 `O(W)`。

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, W;
    cin >> n >> W;
    vector<int> w(n + 1), v(n + 1);
    for (int i = 1; i <= n; i++) {
        cin >> w[i] >> v[i];
    }

    vector<long long> dp(W + 1, 0);
    for (int i = 1; i <= n; i++) {
        for (int j = W; j >= w[i]; j--) {
            dp[j] = max(dp[j], dp[j - w[i]] + v[i]);
        }
    }

    cout << dp[W] << '\n';
    return 0;
}
```

**测试设计：**

测试 1 输入：
```text
3 5
2 6
2 10
3 12
```
期望输出：
```text
22
```

测试 2 输入：
```text
2 0
1 10
2 20
```
期望输出：
```text
0
```

### V03-EX05 完全背包最大价值

- 归属卷：第 3 卷
- 覆盖模块：DP-07 完全背包，DP-24 背包变体
- 考场用途：每种物品可无限次选择，容量限制下求最大价值

**题目描述：** 有 `n` 种物品和容量为 `W` 的背包。第 `i` 种物品重量为 `w[i]`，价值为 `v[i]`，每种物品可以选择任意多次。求不超过容量时的最大总价值。

**输入格式：** 第一行两个整数 `n W`。接下来 `n` 行，每行两个整数 `w[i] v[i]`。

**输出格式：** 输出一个整数，表示最大总价值。

**样例输入：**
```text
3 10
2 3
3 4
5 8
```

**样例输出：**
```text
16
```

**Motivation：** 状态定义为 `dp[j]`：容量不超过 `j` 时的最大价值。最后一步是再放入一个第 `i` 种物品，于是从 `dp[j-w[i]]` 转移。因为同一种物品可以重复用，容量循环从小到大，让本轮刚更新出的 `dp[j-w[i]]` 继续参与转移。复杂度 `O(nW)`，空间 `O(W)`。

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, W;
    cin >> n >> W;
    vector<int> w(n + 1), v(n + 1);
    for (int i = 1; i <= n; i++) {
        cin >> w[i] >> v[i];
    }

    vector<long long> dp(W + 1, 0);
    for (int i = 1; i <= n; i++) {
        for (int j = w[i]; j <= W; j++) {
            dp[j] = max(dp[j], dp[j - w[i]] + v[i]);
        }
    }

    cout << dp[W] << '\n';
    return 0;
}
```

**测试设计：**

测试 1 输入：
```text
1 7
3 5
```
期望输出：
```text
10
```

测试 2 输入：
```text
2 2
3 10
4 20
```
期望输出：
```text
0
```

### V03-EX06 分组背包最大价值

- 归属卷：第 3 卷
- 覆盖模块：DP-08 分组背包，DP-24 背包变体
- 考场用途：每组最多选一件物品，训练从组到容量的转移顺序

**题目描述：** 有 `G` 组物品和容量为 `W` 的背包。每组里有若干件物品，同一组最多选一件，也可以不选。求不超过容量时的最大总价值。

**输入格式：** 第一行两个整数 `G W`。接下来对每一组，先输入整数 `k`，表示该组物品数；再输入 `k` 行，每行两个整数 `weight value`。

**输出格式：** 输出一个整数，表示最大总价值。

**样例输入：**
```text
3 7
2
2 6
3 8
2
4 7
2 4
2
3 5
1 2
```

**样例输出：**
```text
15
```

**Motivation：** 状态定义为 `dp[j]`：处理完前若干组后，容量不超过 `j` 的最大价值。最后一步是在当前组中选择一件物品，或者当前组不选。为了保证一组内最多选一件，处理新组时必须从上一组的 `old` 数组转移，不能让本组更新结果再次选本组物品。复杂度 `O(总物品数 * W)`，空间 `O(W)`。

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int G, W;
    cin >> G >> W;
    vector<long long> dp(W + 1, 0);

    for (int group_id = 1; group_id <= G; group_id++) {
        int k;
        cin >> k;
        vector<int> weight(k + 1), value(k + 1);
        for (int i = 1; i <= k; i++) {
            cin >> weight[i] >> value[i];
        }

        vector<long long> old = dp;
        for (int j = 0; j <= W; j++) {
            dp[j] = old[j];
        }
        for (int i = 1; i <= k; i++) {
            for (int j = weight[i]; j <= W; j++) {
                dp[j] = max(dp[j], old[j - weight[i]] + value[i]);
            }
        }
    }

    cout << dp[W] << '\n';
    return 0;
}
```

**测试设计：**

测试 1 输入：
```text
2 5
2
5 10
4 9
2
1 4
2 7
```
期望输出：
```text
13
```

测试 2 输入：
```text
2 3
1
4 10
1
3 5
```
期望输出：
```text
5
```

### V03-EX07 最长不下降子序列与最少删除

- 归属卷：第 3 卷
- 覆盖模块：DP-11 LIS，DP-23 LIS/LCS 常见变体速查
- 考场用途：区分严格递增和不下降，输出长度和最少删除数

**题目描述：** 给定长度为 `n` 的整数序列。求最长不下降子序列长度，并求最少删除多少个元素可以让剩余序列不下降。

**输入格式：** 第一行一个整数 `n`。第二行 `n` 个整数 `a[1..n]`。

**输出格式：** 输出两个整数，分别表示最长不下降子序列长度和最少删除数。

**样例输入：**
```text
7
3 1 2 2 4 3 5
```

**样例输出：**
```text
5 2
```

**Motivation：** 状态定义为 `dp[i]`：以第 `i` 个元素结尾的最长不下降子序列长度。这样定义是因为最后一步一定选择了 `a[i]`，前一个被选元素只能来自某个 `j<i` 且 `a[j]<=a[i]` 的位置。答案是 `max(dp[i])`，最少删除数为 `n - max(dp[i])`。复杂度 `O(n^2)`，空间 `O(n)`。

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<long long> a(n + 1);
    for (int i = 1; i <= n; i++) {
        cin >> a[i];
    }

    vector<int> dp(n + 1, 1);
    int best = 0;
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j < i; j++) {
            if (a[j] <= a[i]) {
                dp[i] = max(dp[i], dp[j] + 1);
            }
        }
        best = max(best, dp[i]);
    }

    cout << best << ' ' << n - best << '\n';
    return 0;
}
```

**测试设计：**

测试 1 输入：
```text
4
5 5 5 5
```
期望输出：
```text
4 0
```

测试 2 输入：
```text
3
5 4 3
```
期望输出：
```text
1 2
```

### V03-EX08 最长公共子序列长度

- 归属卷：第 3 卷
- 覆盖模块：DP-09 LCS，DP-23 LIS/LCS 常见变体速查
- 考场用途：两个字符串前缀 DP，训练匹配和跳过的最后一步

**题目描述：** 给定两个字符串 `a` 和 `b`，求它们的最长公共子序列长度。子序列可以不连续，但字符相对顺序必须保持。

**输入格式：** 第一行字符串 `a`。第二行字符串 `b`。

**输出格式：** 输出一个整数，表示最长公共子序列长度。

**样例输入：**
```text
ABCBDAB
BDCABA
```

**样例输出：**
```text
4
```

**Motivation：** 状态定义为 `dp[i][j]`：`a` 的前 `i` 个字符和 `b` 的前 `j` 个字符的 LCS 长度。这样定义是因为最后一步要么匹配 `a[i]` 与 `b[j]`，要么跳过其中一个末尾字符。若字符相等，从 `dp[i-1][j-1]+1` 转移；否则从 `dp[i-1][j]` 和 `dp[i][j-1]` 取最大。复杂度 `O(nm)`，空间 `O(nm)`。

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string a, b;
    cin >> a >> b;
    int n = (int)a.size();
    int m = (int)b.size();
    a = " " + a;
    b = " " + b;

    vector<vector<int>> dp(n + 1, vector<int>(m + 1, 0));
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            if (a[i] == b[j]) {
                dp[i][j] = dp[i - 1][j - 1] + 1;
            } else {
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1]);
            }
        }
    }

    cout << dp[n][m] << '\n';
    return 0;
}
```

**测试设计：**

测试 1 输入：
```text
abc
def
```
期望输出：
```text
0
```

测试 2 输入：
```text
ABC
AC
```
期望输出：
```text
2
```

### V03-EX09 最长公共上升子序列

- 归属卷：第 3 卷
- 覆盖模块：DP-23 LCIS 变体，DP-09 LCS，DP-11 LIS
- 考场用途：两个序列公共匹配，同时要求值严格上升

**题目描述：** 给定两个整数序列 `a[1..n]` 和 `b[1..m]`。求它们的最长公共上升子序列长度，即子序列必须同时出现在两个序列中，并且数值严格递增。

**输入格式：** 第一行整数 `n`。第二行 `n` 个整数。第三行整数 `m`。第四行 `m` 个整数。

**输出格式：** 输出一个整数，表示 LCIS 长度。

**样例输入：**
```text
5
1 3 2 4 6
6
3 1 2 4 5 6
```

**样例输出：**
```text
4
```

**Motivation：** 状态定义为 `dp[j]`：处理完当前 `a` 的前缀后，以 `b[j]` 作为最后一个公共元素的 LCIS 长度。这样定义把 LCS 的公共位置和 LIS 的结尾值合在一起。枚举 `a[i]` 时，用 `best` 维护所有 `b[j] < a[i]` 且可接到当前值前面的最大长度；当 `a[i] == b[j]`，最后一步就是把当前相等值接在 `best` 后面。复杂度 `O(nm)`，空间 `O(m)`。

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n;
    vector<int> a(n + 1);
    for (int i = 1; i <= n; i++) cin >> a[i];
    cin >> m;
    vector<int> b(m + 1);
    for (int j = 1; j <= m; j++) cin >> b[j];

    vector<int> dp(m + 1, 0);
    for (int i = 1; i <= n; i++) {
        int best = 0;
        for (int j = 1; j <= m; j++) {
            if (a[i] == b[j]) {
                dp[j] = max(dp[j], best + 1);
            } else if (b[j] < a[i]) {
                best = max(best, dp[j]);
            }
        }
    }

    int answer = 0;
    for (int j = 1; j <= m; j++) answer = max(answer, dp[j]);
    cout << answer << '\n';
    return 0;
}
```

**测试设计：**

测试 1 输入：
```text
3
1 2 3
3
3 2 1
```
期望输出：
```text
1
```

测试 2 输入：
```text
3
1 2 3
3
4 5 6
```
期望输出：
```text
0
```

### V03-EX10 石子合并区间 DP

- 归属卷：第 3 卷
- 覆盖模块：DP-13 区间 DP
- 考场用途：训练区间长度枚举、分割点枚举和前缀和代价

**题目描述：** 有 `n` 堆石子排成一行，第 `i` 堆有 `a[i]` 个石子。每次只能合并相邻的两段石子，代价为这两段石子的总数。求把所有石子合并成一堆的最小总代价。

**输入格式：** 第一行一个整数 `n`。第二行 `n` 个整数 `a[1..n]`。

**输出格式：** 输出一个整数，表示最小总代价。

**样例输入：**
```text
4
4 5 9 4
```

**样例输出：**
```text
44
```

**Motivation：** 状态定义为 `dp[l][r]`：把连续区间 `l..r` 合并成一堆的最小代价。这样定义是因为任何一次最终合并前，区间一定被某个分割点 `k` 分成两段 `l..k` 和 `k+1..r`。最后一步代价是整个区间石子总和，所以转移为 `dp[l][k]+dp[k+1][r]+sum(l,r)`。复杂度 `O(n^3)`，空间 `O(n^2)`。

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<long long> a(n + 1), prefix(n + 1, 0);
    for (int i = 1; i <= n; i++) {
        cin >> a[i];
        prefix[i] = prefix[i - 1] + a[i];
    }

    vector<vector<long long>> dp(n + 2, vector<long long>(n + 2, 0));
    for (int len = 2; len <= n; len++) {
        for (int l = 1; l + len - 1 <= n; l++) {
            int r = l + len - 1;
            dp[l][r] = 4'000'000'000'000'000'000LL;
            long long total = prefix[r] - prefix[l - 1];
            for (int k = l; k < r; k++) {
                dp[l][r] = min(dp[l][r], dp[l][k] + dp[k + 1][r] + total);
            }
        }
    }

    cout << dp[1][n] << '\n';
    return 0;
}
```

**测试设计：**

测试 1 输入：
```text
1
10
```
期望输出：
```text
0
```

测试 2 输入：
```text
3
1 2 3
```
期望输出：
```text
9
```

### V03-EX11 树上最大独立集

- 归属卷：第 3 卷
- 覆盖模块：DP-14 树形 DP，TREE-01 根树 DFS 顺序
- 考场用途：树上相邻节点不能同时选的选或不选模型

**题目描述：** 给定一棵 `n` 个点的树，每个点 `i` 有权值 `value[i]`。你可以选择若干个点，但任意一条边的两个端点不能同时被选。求可获得的最大权值和。

**输入格式：** 第一行一个整数 `n`。第二行 `n` 个整数 `value[1..n]`。接下来 `n-1` 行，每行两个整数 `u v` 表示一条无向边。

**输出格式：** 输出一个整数，表示最大权值和。

**样例输入：**
```text
5
10 1 5 4 7
1 2
1 3
2 4
2 5
```

**样例输出：**
```text
21
```

**Motivation：** 状态定义为 `dp[u][0]` 和 `dp[u][1]`：在以 `u` 为根的子树内，`u` 不选或选时的最大权值。这样定义是因为父子是否能选只由当前点是否被选决定。最后一步是合并每个子树：若选 `u`，孩子都不能选；若不选 `u`，每个孩子可选可不选取最大。复杂度 `O(n)`，空间 `O(n)`。

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

int n;
vector<long long> value_node;
vector<vector<int>> graph_edges;
vector<array<long long, 2>> dp;

void dfs(int u, int parent) {
    dp[u][0] = 0;
    dp[u][1] = value_node[u];
    for (int v : graph_edges[u]) {
        if (v == parent) continue;
        dfs(v, u);
        dp[u][0] += max(dp[v][0], dp[v][1]);
        dp[u][1] += dp[v][0];
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n;
    value_node.assign(n + 1, 0);
    graph_edges.assign(n + 1, {});
    dp.assign(n + 1, {0, 0});

    for (int i = 1; i <= n; i++) cin >> value_node[i];
    for (int i = 1; i <= n - 1; i++) {
        int u, v;
        cin >> u >> v;
        graph_edges[u].push_back(v);
        graph_edges[v].push_back(u);
    }

    dfs(1, 0);
    cout << max(dp[1][0], dp[1][1]) << '\n';
    return 0;
}
```

**测试设计：**

测试 1 输入：
```text
1
8
```
期望输出：
```text
8
```

测试 2 输入：
```text
3
5 100 5
1 2
2 3
```
期望输出：
```text
100
```

### V03-EX12 DAG 最长路径

- 归属卷：第 3 卷
- 覆盖模块：DP-15 DAG DP，GRAPH-05 拓扑 DAG DP
- 考场用途：有向无环图上按拓扑序做最长路径 DP

**题目描述：** 给定一个有向无环图，有 `n` 个点和 `m` 条有向边。每条边 `u -> v` 有非负权值 `w`。求图中任意起点到任意终点的一条路径的最大边权和。

**输入格式：** 第一行两个整数 `n m`。接下来 `m` 行，每行三个整数 `u v w`，表示一条有向边。

**输出格式：** 输出一个整数，表示最大路径权值和。

**样例输入：**
```text
5 5
1 2 3
1 3 2
2 4 4
3 4 1
4 5 5
```

**样例输出：**
```text
12
```

**Motivation：** 状态定义为 `dp[v]`：以点 `v` 作为终点的最大路径权值和。这样定义是因为 DAG 中按拓扑序处理后，所有能转移到 `v` 的前驱都已经算完。最后一步一定是某条边 `u -> v`，转移为 `dp[v]=max(dp[v],dp[u]+w)`。复杂度 `O(n+m)`，空间 `O(n+m)`。

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

struct Edge {
    int to;
    long long weight;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;
    vector<vector<Edge>> graph_edges(n + 1);
    vector<int> indegree(n + 1, 0);
    for (int i = 1; i <= m; i++) {
        int u, v;
        long long w;
        cin >> u >> v >> w;
        graph_edges[u].push_back({v, w});
        indegree[v]++;
    }

    queue<int> q;
    for (int i = 1; i <= n; i++) {
        if (indegree[i] == 0) q.push(i);
    }

    vector<long long> dp(n + 1, 0);
    long long answer = 0;
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        answer = max(answer, dp[u]);
        for (const Edge& edge : graph_edges[u]) {
            int v = edge.to;
            dp[v] = max(dp[v], dp[u] + edge.weight);
            indegree[v]--;
            if (indegree[v] == 0) q.push(v);
        }
    }

    cout << answer << '\n';
    return 0;
}
```

**测试设计：**

测试 1 输入：
```text
3 0
```
期望输出：
```text
0
```

测试 2 输入：
```text
4 4
1 2 5
1 3 2
2 4 1
3 4 10
```
期望输出：
```text
12
```

### V03-EX13 状压最短访问路径

- 归属卷：第 3 卷
- 覆盖模块：DP-16 状压 DP
- 考场用途：`n <= 16` 时用集合状态表示已经访问的点

**题目描述：** 有 `n` 个景点，编号 `1..n`，从景点 `i` 到景点 `j` 的代价为 `cost[i][j]`。你从景点 `1` 出发，每个景点必须恰好访问一次，可以在任意景点结束。求最小总代价。

**输入格式：** 第一行一个整数 `n`。接下来 `n` 行，每行 `n` 个整数，表示代价矩阵 `cost[1..n][1..n]`。

**输出格式：** 输出一个整数，表示最小总代价。

**样例输入：**
```text
4
0 10 15 20
10 0 35 25
15 35 0 30
20 25 30 0
```

**样例输出：**
```text
65
```

**Motivation：** 状态定义为 `dp[mask][last]`：已经访问的景点集合为 `mask`，当前停在 `last` 时的最小总代价。这样定义是因为后续只关心哪些点访问过以及最后停在哪里。最后一步是从某个 `last` 走到一个未访问点 `next`，新集合加入 `next`。复杂度 `O(2^n * n^2)`，空间 `O(2^n * n)`。

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<vector<long long>> cost(n + 1, vector<long long>(n + 1, 0));
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++) {
            cin >> cost[i][j];
        }
    }

    int total_mask = 1 << n;
    const long long INF = 4'000'000'000'000'000'000LL;
    vector<vector<long long>> dp(total_mask, vector<long long>(n + 1, INF));
    int start_mask = 1 << 0;
    dp[start_mask][1] = 0;

    for (int mask = 0; mask < total_mask; mask++) {
        for (int last = 1; last <= n; last++) {
            if (dp[mask][last] == INF) continue;
            for (int next = 1; next <= n; next++) {
                int bit = 1 << (next - 1);
                if ((mask & bit) != 0) continue;
                int new_mask = mask | bit;
                dp[new_mask][next] = min(dp[new_mask][next], dp[mask][last] + cost[last][next]);
            }
        }
    }

    int full_mask = total_mask - 1;
    long long answer = INF;
    for (int last = 1; last <= n; last++) {
        answer = min(answer, dp[full_mask][last]);
    }

    cout << answer << '\n';
    return 0;
}
```

**测试设计：**

测试 1 输入：
```text
1
0
```
期望输出：
```text
0
```

测试 2 输入：
```text
3
0 2 9
1 0 6
15 7 0
```
期望输出：
```text
8
```

### V03-EX14 数位 DP 统计无相邻相同数字

- 归属卷：第 3 卷
- 覆盖模块：DP-17 数位 DP
- 考场用途：统计 `1..N` 中满足数字约束的整数个数

**题目描述：** 给定正整数 `N`，统计 `1..N` 中有多少个整数满足：十进制表示中任意相邻两位数字都不相同。

**输入格式：** 一行一个正整数 `N`，长度不超过 `18`。

**输出格式：** 输出一个整数，表示满足条件的整数个数。

**样例输入：**
```text
20
```

**样例输出：**
```text
19
```

**Motivation：** 状态定义为 `dfs(pos, prev, tight, started)`：处理到第 `pos` 位，上一位数字为 `prev`，是否贴着上界，是否已经开始填非前导零数字时的方案数。这样定义是因为后续合法性只取决于上一位数字和上界限制，不需要知道完整前缀。最后一步是枚举当前位置填的数字，如果已经开始且等于上一位则跳过。复杂度 `O(位数 * 11 * 2 * 10)`，空间 `O(位数 * 11 * 2)`。

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

string digits;
long long memo[25][11][2];
bool visited[25][11][2];

long long dfs(int pos, int prev, bool tight, bool started) {
    int len = (int)digits.size() - 1;
    if (pos > len) {
        return started ? 1 : 0;
    }
    int prev_index = prev + 1;
    if (!tight && visited[pos][prev_index][started ? 1 : 0]) {
        return memo[pos][prev_index][started ? 1 : 0];
    }

    int limit = tight ? digits[pos] - '0' : 9;
    long long ways = 0;
    for (int d = 0; d <= limit; d++) {
        bool next_tight = tight && (d == limit);
        if (!started && d == 0) {
            ways += dfs(pos + 1, -1, next_tight, false);
        } else {
            if (started && d == prev) continue;
            ways += dfs(pos + 1, d, next_tight, true);
        }
    }

    if (!tight) {
        visited[pos][prev_index][started ? 1 : 0] = true;
        memo[pos][prev_index][started ? 1 : 0] = ways;
    }
    return ways;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string n;
    cin >> n;
    digits = " " + n;
    cout << dfs(1, -1, true, false) << '\n';
    return 0;
}
```

**测试设计：**

测试 1 输入：
```text
9
```
期望输出：
```text
9
```

测试 2 输入：
```text
100
```
期望输出：
```text
90
```

### V03-EX15 股票冷冻期状态升维

- 归属卷：第 3 卷
- 覆盖模块：DP-26 状态升维与有后效性，DP-03B 状态维度路由
- 考场用途：发现只用 `dp[i]` 不够时，把持有和冷冻状态加进 DP

**题目描述：** 给定 `n` 天股票价格 `price[1..n]`。每天你可以选择买入、卖出或什么都不做。任意时刻最多持有一股。卖出股票后的第二天不能买入，也就是有一天冷冻期。求最大利润。

**输入格式：** 第一行一个整数 `n`。第二行 `n` 个整数 `price[1..n]`。

**输出格式：** 输出一个整数，表示最大利润。

**样例输入：**
```text
5
1 2 3 0 2
```

**样例输出：**
```text
3
```

**Motivation：** 如果只定义 `dp[i]` 为前 `i` 天最大利润，会丢失“今天是否持股”和“今天是否刚卖出”这些会影响明天操作的历史信息。升维后定义 `dp[i][0]` 表示第 `i` 天结束后空仓且不在刚卖出状态，`dp[i][1]` 表示持股，`dp[i][2]` 表示今天刚卖出。最后一步分别是休息、买入、卖出。复杂度 `O(n)`，空间 `O(n)`，也可滚动优化到 `O(1)`。

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<long long> price(n + 1);
    for (int i = 1; i <= n; i++) {
        cin >> price[i];
    }

    const long long NEG = -4'000'000'000'000'000'000LL;
    vector<array<long long, 3>> dp(n + 1);
    for (int i = 0; i <= n; i++) {
        dp[i] = {NEG, NEG, NEG};
    }

    dp[0][0] = 0;
    for (int i = 1; i <= n; i++) {
        dp[i][0] = max(dp[i - 1][0], dp[i - 1][2]);
        dp[i][1] = max(dp[i - 1][1], dp[i - 1][0] - price[i]);
        dp[i][2] = dp[i - 1][1] + price[i];
    }

    cout << max(dp[n][0], dp[n][2]) << '\n';
    return 0;
}
```

**测试设计：**

测试 1 输入：
```text
1
5
```
期望输出：
```text
0
```

测试 2 输入：
```text
6
6 1 3 2 4 7
```
期望输出：
```text
6
```
