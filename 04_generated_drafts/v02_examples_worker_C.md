# 0.2 版本例题扩展 Worker C

负责范围：

- 第 2 卷：暴力、枚举、记忆化与部分分。
- 第 3A 卷：贪心判别、证明与反例系统。

抽取约定：每道例题使用固定标题 `### Vxx-EXyy 标题`，并提供题面、输入输出、样例、完整 C++17 代码和至少 2 组测试设计。

## 第 2 卷例题

### V02-EX01 全排列最短访问序列

- 归属卷：第 2 卷
- 覆盖模块：全排列、`next_permutation`、小数据精确解
- 考场用途：`n <= 9` 且顺序可任意排列时，先用全排列写出正确答案。

**题目描述：** 有 `n` 个点，访问顺序可以任意决定。已知从点 `i` 到点 `j` 的代价 `w[i][j]`，要求访问每个点恰好一次，使相邻两点之间总代价最小。若有多种最优顺序，输出字典序最小的顺序。

**输入格式：** 第一行一个整数 `n`。接下来 `n` 行，每行 `n` 个整数，表示代价矩阵。

**输出格式：** 第一行输出最小总代价。第二行输出最优访问顺序。

**样例输入：**
```text
3
0 5 1
5 0 2
1 2 0
```

**样例输出：**
```text
3
1 3 2
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<vector<long long>> w(n + 1, vector<long long>(n + 1));
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++) {
            cin >> w[i][j];
        }
    }

    vector<int> p(n + 1);
    for (int i = 1; i <= n; i++) p[i] = i;

    long long best = (1LL << 62);
    vector<int> bestPath;
    do {
        long long cost = 0;
        for (int i = 1; i < n; i++) {
            cost += w[p[i]][p[i + 1]];
        }
        vector<int> cur(p.begin() + 1, p.end());
        if (cost < best || (cost == best && cur < bestPath)) {
            best = cost;
            bestPath = cur;
        }
    } while (next_permutation(p.begin() + 1, p.end()));

    cout << best << '\n';
    for (int i = 0; i < n; i++) {
        if (i) cout << ' ';
        cout << bestPath[i];
    }
    cout << '\n';
    return 0;
}
```

**测试设计：**

测试 1 输入：
```text
3
0 5 1
5 0 2
1 2 0
```
期望输出：
```text
3
1 3 2
```

测试 2 输入：
```text
4
0 1 10 10
1 0 1 10
10 1 0 1
10 10 1 0
```
期望输出：
```text
3
1 2 3 4
```

### V02-EX02 子集目标和计数

- 归属卷：第 2 卷
- 覆盖模块：子集枚举、位运算、`2^n` 暴力
- 考场用途：`n <= 20` 时直接枚举所有选或不选，给目标和类问题拿稳小数据分。

**题目描述：** 给定 `n` 个正整数和目标值 `S`，统计有多少个子集的元素和恰好等于 `S`。

**输入格式：** 第一行两个整数 `n S`。第二行 `n` 个整数。

**输出格式：** 输出一个整数，表示满足条件的子集数量。

**样例输入：**
```text
4 5
1 2 3 4
```

**样例输出：**
```text
2
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    long long target;
    cin >> n >> target;
    vector<long long> a(n + 1);
    for (int i = 1; i <= n; i++) cin >> a[i];

    long long ans = 0;
    int totalMask = 1 << n;
    for (int mask = 0; mask < totalMask; mask++) {
        long long sum = 0;
        for (int i = 1; i <= n; i++) {
            if (mask & (1 << (i - 1))) {
                sum += a[i];
            }
        }
        if (sum == target) ans++;
    }

    cout << ans << '\n';
    return 0;
}
```

**测试设计：**

测试 1 输入：
```text
4 5
1 2 3 4
```
期望输出：
```text
2
```

测试 2 输入：
```text
3 3
1 1 2
```
期望输出：
```text
2
```

### V02-EX03 组合 DFS 选 k 个数

- 归属卷：第 2 卷
- 覆盖模块：组合 DFS、递归枚举、剩余数量剪枝
- 考场用途：题目要求“从 n 个里面选 k 个”时，用 DFS 避免枚举所有排列。

**题目描述：** 给定 `n` 个整数，从中选出恰好 `k` 个数，使它们的和等于 `S`。统计方案数。不同下标视为不同元素。

**输入格式：** 第一行三个整数 `n k S`。第二行 `n` 个整数。

**输出格式：** 输出方案数。

**样例输入：**
```text
5 2 5
1 2 3 4 5
```

**样例输出：**
```text
2
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

int n, k;
long long target;
vector<long long> a;
long long ans = 0;

void dfs(int start, int chosen, long long sum) {
    if (chosen == k) {
        if (sum == target) ans++;
        return;
    }
    if (start > n) return;
    int need = k - chosen;
    if (n - start + 1 < need) return;

    for (int i = start; i <= n; i++) {
        dfs(i + 1, chosen + 1, sum + a[i]);
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n >> k >> target;
    a.assign(n + 1, 0);
    for (int i = 1; i <= n; i++) cin >> a[i];

    dfs(1, 0, 0);
    cout << ans << '\n';
    return 0;
}
```

**测试设计：**

测试 1 输入：
```text
5 2 5
1 2 3 4 5
```
期望输出：
```text
2
```

测试 2 输入：
```text
6 3 10
1 2 3 4 5 6
```
期望输出：
```text
3
```

### V02-EX04 N 皇后方案数

- 归属卷：第 2 卷
- 覆盖模块：回溯、冲突检查、搜索树剪枝
- 考场用途：棋盘摆放、每行每列限制、不能互相攻击类问题的经典回溯模板。

**题目描述：** 在 `n * n` 棋盘上放置 `n` 个皇后，要求任意两个皇后不在同一行、同一列或同一条对角线上。输出方案数。

**输入格式：** 一个整数 `n`。

**输出格式：** 输出方案数。

**样例输入：**
```text
4
```

**样例输出：**
```text
2
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

int n;
long long ans = 0;
vector<int> colUsed, diag1Used, diag2Used;

void dfs(int row) {
    if (row == n + 1) {
        ans++;
        return;
    }
    for (int col = 1; col <= n; col++) {
        int d1 = row + col;
        int d2 = row - col + n;
        if (colUsed[col] || diag1Used[d1] || diag2Used[d2]) continue;
        colUsed[col] = diag1Used[d1] = diag2Used[d2] = 1;
        dfs(row + 1);
        colUsed[col] = diag1Used[d1] = diag2Used[d2] = 0;
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n;
    colUsed.assign(n + 1, 0);
    diag1Used.assign(2 * n + 2, 0);
    diag2Used.assign(2 * n + 2, 0);

    dfs(1);
    cout << ans << '\n';
    return 0;
}
```

**测试设计：**

测试 1 输入：
```text
4
```
期望输出：
```text
2
```

测试 2 输入：
```text
5
```
期望输出：
```text
10
```

### V02-EX05 三位密码锁 BFS 状态搜索

- 归属卷：第 2 卷
- 覆盖模块：BFS 状态、最短步数、访问判重
- 考场用途：状态数量有限、每步代价相同、问最少操作次数时，直接建图 BFS。

**题目描述：** 一个三位密码锁初始为 `000`。每次可以选择一位数字加一或减一，数字在 `0` 到 `9` 间循环。给定目标状态和若干禁用状态，求从 `000` 到目标状态的最少步数；若无法到达，输出 `-1`。

**输入格式：** 第一行一个三位字符串 `target`。第二行一个整数 `m`。接下来 `m` 行，每行一个禁用状态。

**输出格式：** 输出最少步数，无法到达输出 `-1`。

**样例输入：**
```text
002
0
```

**样例输出：**
```text
2
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

int parseState(const string &s) {
    return (s[0] - '0') * 100 + (s[1] - '0') * 10 + (s[2] - '0');
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string targetStr;
    int m;
    cin >> targetStr >> m;

    vector<int> forbidden(1000, 0);
    for (int i = 1; i <= m; i++) {
        string s;
        cin >> s;
        forbidden[parseState(s)] = 1;
    }

    int start = 0;
    int target = parseState(targetStr);
    if (forbidden[start] || forbidden[target]) {
        cout << -1 << '\n';
        return 0;
    }

    vector<int> dist(1000, -1);
    queue<int> q;
    dist[start] = 0;
    q.push(start);

    int base[3] = {100, 10, 1};
    while (!q.empty()) {
        int cur = q.front();
        q.pop();
        if (cur == target) break;

        for (int pos = 0; pos < 3; pos++) {
            int digit = (cur / base[pos]) % 10;
            for (int delta : {-1, 1}) {
                int nd = (digit + delta + 10) % 10;
                int nxt = cur + (nd - digit) * base[pos];
                if (!forbidden[nxt] && dist[nxt] == -1) {
                    dist[nxt] = dist[cur] + 1;
                    q.push(nxt);
                }
            }
        }
    }

    cout << dist[target] << '\n';
    return 0;
}
```

**测试设计：**

测试 1 输入：
```text
002
0
```
期望输出：
```text
2
```

测试 2 输入：
```text
010
1
010
```
期望输出：
```text
-1
```

### V02-EX06 装载问题的 DFS 剪枝

- 归属卷：第 2 卷
- 覆盖模块：DFS、上界剪枝、排序剪枝
- 考场用途：背包容量较小或物品数不大时，先用搜索；加上剩余和剪枝后能多拿一档数据。

**题目描述：** 有 `n` 个物品，第 `i` 个重量为 `w[i]`。选择若干物品放入容量为 `C` 的箱子，使总重量不超过 `C` 且尽量大。输出最大可装重量。

**输入格式：** 第一行两个整数 `n C`。第二行 `n` 个整数表示重量。

**输出格式：** 输出最大可装重量。

**样例输入：**
```text
5 10
2 3 4 5 9
```

**样例输出：**
```text
10
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

int n;
long long C;
vector<long long> w, suffixSum;
long long best = 0;

void dfs(int idx, long long cur) {
    if (cur > C) return;
    if (idx == n + 1) {
        best = max(best, cur);
        return;
    }
    if (cur + suffixSum[idx] <= best) return;

    dfs(idx + 1, cur + w[idx]);
    dfs(idx + 1, cur);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n >> C;
    w.assign(n + 1, 0);
    for (int i = 1; i <= n; i++) cin >> w[i];
    sort(w.begin() + 1, w.end(), greater<long long>());

    suffixSum.assign(n + 2, 0);
    for (int i = n; i >= 1; i--) {
        suffixSum[i] = suffixSum[i + 1] + w[i];
    }

    dfs(1, 0);
    cout << best << '\n';
    return 0;
}
```

**测试设计：**

测试 1 输入：
```text
5 10
2 3 4 5 9
```
期望输出：
```text
10
```

测试 2 输入：
```text
6 15
6 7 8 2 3 4
```
期望输出：
```text
15
```

### V02-EX07 数字串加号的记忆化搜索

- 归属卷：第 2 卷
- 覆盖模块：暴力切分、记忆化搜索、状态压缩
- 考场用途：先写从左到右切字符串的 DFS，再把 `(位置, 当前和)` 存起来，避免重复搜索。

**题目描述：** 给定只含数字的字符串 `s` 和目标值 `T`。可以在相邻数字之间插入若干个加号，把字符串切成若干非负整数，要求这些整数之和等于 `T`。求最少需要插入多少个加号；若无法做到，输出 `-1`。

**输入格式：** 第一行字符串 `s`。第二行整数 `T`。

**输出格式：** 输出最少加号数，无法做到输出 `-1`。

**样例输入：**
```text
99999
45
```

**样例输出：**
```text
4
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

const int INF = 1000000000;

string s;
long long target;
int n;
vector<unordered_map<long long, int>> memo;

int dfs(int pos, long long sum) {
    if (sum > target) return INF;
    if (pos == n) {
        return sum == target ? 0 : INF;
    }
    if (memo[pos].count(sum)) return memo[pos][sum];

    long long val = 0;
    int best = INF;
    for (int nxt = pos; nxt < n; nxt++) {
        val = val * 10 + (s[nxt] - '0');
        if (sum + val > target) break;
        int add = (pos == 0 ? 0 : 1);
        best = min(best, add + dfs(nxt + 1, sum + val));
    }
    memo[pos][sum] = best;
    return best;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> s >> target;
    n = (int)s.size();
    memo.assign(n + 1, unordered_map<long long, int>());

    int ans = dfs(0, 0);
    cout << (ans >= INF ? -1 : ans) << '\n';
    return 0;
}
```

**测试设计：**

测试 1 输入：
```text
99999
45
```
期望输出：
```text
4
```

测试 2 输入：
```text
1234
10
```
期望输出：
```text
3
```

### V02-EX08 网格最大礼物的记忆化搜索

- 归属卷：第 2 卷
- 覆盖模块：记忆化 DFS、二维状态、不可达状态
- 考场用途：能自然写出“从当前位置走到终点”的递归时，先用 memo 快速变成 DP。

**题目描述：** 给定 `n * m` 网格，每个格子有一个整数价值，`-1` 表示障碍。你从 `(1,1)` 出发，只能向下或向右走到 `(n,m)`。求路径价值和最大值；若无法到达，输出 `-1`。

**输入格式：** 第一行两个整数 `n m`。接下来 `n` 行，每行 `m` 个整数。

**输出格式：** 输出最大路径和，无法到达输出 `-1`。

**样例输入：**
```text
3 3
1 2 3
4 -1 5
1 2 10
```

**样例输出：**
```text
21
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

const long long NEG = -(1LL << 60);

int n, m;
vector<vector<long long>> grid, memo;
vector<vector<int>> vis;

long long dfs(int i, int j) {
    if (i > n || j > m) return NEG;
    if (grid[i][j] == -1) return NEG;
    if (i == n && j == m) return grid[i][j];
    if (vis[i][j]) return memo[i][j];
    vis[i][j] = 1;

    long long bestNext = max(dfs(i + 1, j), dfs(i, j + 1));
    if (bestNext == NEG) memo[i][j] = NEG;
    else memo[i][j] = grid[i][j] + bestNext;
    return memo[i][j];
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n >> m;
    grid.assign(n + 1, vector<long long>(m + 1, 0));
    memo.assign(n + 1, vector<long long>(m + 1, NEG));
    vis.assign(n + 1, vector<int>(m + 1, 0));

    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            cin >> grid[i][j];
        }
    }

    long long ans = dfs(1, 1);
    cout << (ans == NEG ? -1 : ans) << '\n';
    return 0;
}
```

**测试设计：**

测试 1 输入：
```text
3 3
1 2 3
4 -1 5
1 2 10
```
期望输出：
```text
21
```

测试 2 输入：
```text
2 2
1 -1
-1 2
```
期望输出：
```text
-1
```

### V02-EX09 折半枚举不超过容量的最大和

- 归属卷：第 2 卷
- 覆盖模块：折半枚举、二分、`n <= 40`
- 考场用途：`2^40` 直接枚举爆炸时，把集合拆成两半，各枚举 `2^20` 后合并。

**题目描述：** 给定 `n` 个正整数和容量 `C`，选择若干数使总和不超过 `C` 且尽量大。输出最大总和。

**输入格式：** 第一行两个整数 `n C`。第二行 `n` 个正整数。

**输出格式：** 输出不超过 `C` 的最大子集和。

**样例输入：**
```text
6 20
7 8 9 10 11 12
```

**样例输出：**
```text
20
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

void genSums(const vector<long long> &a, int l, int r, long long C, vector<long long> &sums) {
    int len = r - l + 1;
    int totalMask = 1 << len;
    for (int mask = 0; mask < totalMask; mask++) {
        long long sum = 0;
        for (int i = 0; i < len; i++) {
            if (mask & (1 << i)) {
                sum += a[l + i];
            }
        }
        if (sum <= C) sums.push_back(sum);
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    long long C;
    cin >> n >> C;
    vector<long long> a(n + 1);
    for (int i = 1; i <= n; i++) cin >> a[i];

    int mid = n / 2;
    vector<long long> leftSums, rightSums;
    genSums(a, 1, mid, C, leftSums);
    genSums(a, mid + 1, n, C, rightSums);

    sort(rightSums.begin(), rightSums.end());
    long long ans = 0;
    for (long long x : leftSums) {
        long long remain = C - x;
        auto it = upper_bound(rightSums.begin(), rightSums.end(), remain);
        if (it == rightSums.begin()) {
            ans = max(ans, x);
        } else {
            --it;
            ans = max(ans, x + *it);
        }
    }

    cout << ans << '\n';
    return 0;
}
```

**测试设计：**

测试 1 输入：
```text
6 20
7 8 9 10 11 12
```
期望输出：
```text
20
```

测试 2 输入：
```text
4 10
1 3 4 8
```
期望输出：
```text
9
```

### V02-EX10 部分分兜底提交策略模拟

- 归属卷：第 2 卷
- 覆盖模块：部分分兜底、小数据精确解、大数据合法输出
- 考场用途：正解来不及写时，保留一个能过小数据、且大数据也不会 RE/格式错的版本。

**题目描述：** 给定 `n` 个物品重量和容量 `C`。本例模拟部分分提交策略：当 `n <= 20` 时输出不超过 `C` 的最大子集和；当 `n > 20` 时输出按输入顺序能放就放得到的合法子集和。这个程序不是满分背包正解，而是“先活下来”的兜底版本。

**输入格式：** 第一行两个整数 `n C`。第二行 `n` 个正整数。

**输出格式：** 输出本策略得到的子集和。

**样例输入：**
```text
5 10
2 7 4 6 3
```

**样例输出：**
```text
10
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

long long exactSmall(const vector<long long> &a, int n, long long C) {
    long long best = 0;
    int totalMask = 1 << n;
    for (int mask = 0; mask < totalMask; mask++) {
        long long sum = 0;
        for (int i = 1; i <= n; i++) {
            if (mask & (1 << (i - 1))) {
                sum += a[i];
            }
        }
        if (sum <= C) best = max(best, sum);
    }
    return best;
}

long long fallbackLarge(const vector<long long> &a, int n, long long C) {
    long long sum = 0;
    for (int i = 1; i <= n; i++) {
        if (sum + a[i] <= C) {
            sum += a[i];
        }
    }
    return sum;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    long long C;
    cin >> n >> C;
    vector<long long> a(n + 1);
    for (int i = 1; i <= n; i++) cin >> a[i];

    if (n <= 20) {
        cout << exactSmall(a, n, C) << '\n';
    } else {
        cout << fallbackLarge(a, n, C) << '\n';
    }
    return 0;
}
```

**测试设计：**

测试 1 输入：
```text
5 10
2 7 4 6 3
```
期望输出：
```text
10
```

测试 2 输入：
```text
21 10
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
```
期望输出：
```text
6
```

## 第 3A 卷例题

### V03A-EX01 最少总等待时间排序贪心

- 归属卷：第 3A 卷
- 覆盖模块：排序贪心、交换论证、最短处理时间优先
- 考场用途：任务顺序可自由调整且目标是等待时间总和时，按耗时从小到大排序。

**题目描述：** 有 `n` 个任务，第 `i` 个任务耗时 `t[i]`。一次只能处理一个任务，任务顺序可以任意调整。一个任务的等待时间是它开始前已经处理完的任务总耗时。求最小总等待时间。

**输入格式：** 第一行一个整数 `n`。第二行 `n` 个整数表示任务耗时。

**输出格式：** 输出最小总等待时间。

**样例输入：**
```text
3
3 1 2
```

**样例输出：**
```text
4
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<long long> t(n + 1);
    for (int i = 1; i <= n; i++) cin >> t[i];
    sort(t.begin() + 1, t.end());

    long long elapsed = 0;
    long long ans = 0;
    for (int i = 1; i <= n; i++) {
        ans += elapsed;
        elapsed += t[i];
    }

    cout << ans << '\n';
    return 0;
}
```

**测试设计：**

测试 1 输入：
```text
3
3 1 2
```
期望输出：
```text
4
```

测试 2 输入：
```text
4
5 5 1 2
```
期望输出：
```text
12
```

### V03A-EX02 最多不重叠活动

- 归属卷：第 3A 卷
- 覆盖模块：区间贪心、按右端点排序、活动选择
- 考场用途：区间互不重叠、要选最多个时，优先尝试按结束时间从早到晚选。

**题目描述：** 给定 `n` 个半开区间 `[l, r)`，选择尽量多的区间，使任意两个被选区间不重叠。若一个区间的结束时间等于另一个区间的开始时间，允许同时选择。

**输入格式：** 第一行一个整数 `n`。接下来 `n` 行，每行两个整数 `l r`。

**输出格式：** 输出最多能选择的区间数量。

**样例输入：**
```text
4
1 3
2 4
3 5
0 7
```

**样例输出：**
```text
2
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

struct Seg {
    long long l;
    long long r;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<Seg> seg(n + 1);
    for (int i = 1; i <= n; i++) cin >> seg[i].l >> seg[i].r;

    sort(seg.begin() + 1, seg.end(), [](const Seg &a, const Seg &b) {
        if (a.r != b.r) return a.r < b.r;
        return a.l < b.l;
    });

    long long lastEnd = -(1LL << 60);
    int ans = 0;
    for (int i = 1; i <= n; i++) {
        if (seg[i].l >= lastEnd) {
            ans++;
            lastEnd = seg[i].r;
        }
    }

    cout << ans << '\n';
    return 0;
}
```

**测试设计：**

测试 1 输入：
```text
4
1 3
2 4
3 5
0 7
```
期望输出：
```text
2
```

测试 2 输入：
```text
5
1 2
2 3
3 4
1 4
4 5
```
期望输出：
```text
4
```

### V03A-EX03 最少点覆盖闭区间

- 归属卷：第 3A 卷
- 覆盖模块：区间选点、排序贪心、右端点策略
- 考场用途：每个闭区间至少被一个点覆盖时，每次在当前最早结束区间的右端点放点。

**题目描述：** 给定 `n` 个闭区间 `[l, r]`。请选择尽量少的整数点，使每个区间内至少包含一个被选点。输出最少点数和这些点。

**输入格式：** 第一行一个整数 `n`。接下来 `n` 行，每行两个整数 `l r`。

**输出格式：** 第一行输出最少点数。第二行按选择顺序输出所有点。

**样例输入：**
```text
3
1 3
2 5
3 6
```

**样例输出：**
```text
1
3
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

struct Seg {
    long long l;
    long long r;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<Seg> seg(n + 1);
    for (int i = 1; i <= n; i++) cin >> seg[i].l >> seg[i].r;

    sort(seg.begin() + 1, seg.end(), [](const Seg &a, const Seg &b) {
        if (a.r != b.r) return a.r < b.r;
        return a.l < b.l;
    });

    vector<long long> points;
    long long lastPoint = -(1LL << 60);
    for (int i = 1; i <= n; i++) {
        if (lastPoint < seg[i].l) {
            lastPoint = seg[i].r;
            points.push_back(lastPoint);
        }
    }

    cout << points.size() << '\n';
    for (int i = 0; i < (int)points.size(); i++) {
        if (i) cout << ' ';
        cout << points[i];
    }
    cout << '\n';
    return 0;
}
```

**测试设计：**

测试 1 输入：
```text
3
1 3
2 5
3 6
```
期望输出：
```text
1
3
```

测试 2 输入：
```text
4
1 2
3 4
2 3
5 5
```
期望输出：
```text
3
2 4 5
```

### V03A-EX04 合并果子的堆贪心

- 归属卷：第 3A 卷
- 覆盖模块：堆贪心、Huffman 思想、每次取两个最小
- 考场用途：每次合并产生代价，总代价最小，优先考虑小根堆。

**题目描述：** 有 `n` 堆果子，每次可以选择两堆合并，新堆大小为两堆之和，本次代价也是两堆之和。求把所有果子合成一堆的最小总代价。

**输入格式：** 第一行一个整数 `n`。第二行 `n` 个整数表示每堆果子数量。

**输出格式：** 输出最小总代价。

**样例输入：**
```text
4
1 2 3 4
```

**样例输出：**
```text
19
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    priority_queue<long long, vector<long long>, greater<long long>> pq;
    for (int i = 1; i <= n; i++) {
        long long x;
        cin >> x;
        pq.push(x);
    }

    long long ans = 0;
    while ((int)pq.size() > 1) {
        long long a = pq.top();
        pq.pop();
        long long b = pq.top();
        pq.pop();
        ans += a + b;
        pq.push(a + b);
    }

    cout << ans << '\n';
    return 0;
}
```

**测试设计：**

测试 1 输入：
```text
4
1 2 3 4
```
期望输出：
```text
19
```

测试 2 输入：
```text
3
10 20 30
```
期望输出：
```text
90
```

### V03A-EX05 最少会议室

- 归属卷：第 3A 卷
- 覆盖模块：堆贪心、区间扫描、资源复用
- 考场用途：求最少机器、教室、会议室数量时，按开始时间扫，用小根堆维护最早结束资源。

**题目描述：** 给定 `n` 个半开会议区间 `[l, r)`，同一间会议室中结束时间等于下一场开始时间时可以复用。求最少需要多少间会议室。

**输入格式：** 第一行一个整数 `n`。接下来 `n` 行，每行两个整数 `l r`。

**输出格式：** 输出最少会议室数量。

**样例输入：**
```text
4
1 4
2 5
6 7
3 8
```

**样例输出：**
```text
3
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

struct Seg {
    long long l;
    long long r;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<Seg> seg(n + 1);
    for (int i = 1; i <= n; i++) cin >> seg[i].l >> seg[i].r;

    sort(seg.begin() + 1, seg.end(), [](const Seg &a, const Seg &b) {
        if (a.l != b.l) return a.l < b.l;
        return a.r < b.r;
    });

    priority_queue<long long, vector<long long>, greater<long long>> ends;
    int ans = 0;
    for (int i = 1; i <= n; i++) {
        if (!ends.empty() && ends.top() <= seg[i].l) {
            ends.pop();
        }
        ends.push(seg[i].r);
        ans = max(ans, (int)ends.size());
    }

    cout << ans << '\n';
    return 0;
}
```

**测试设计：**

测试 1 输入：
```text
4
1 4
2 5
6 7
3 8
```
期望输出：
```text
3
```

测试 2 输入：
```text
5
1 2
2 3
3 4
1 4
4 5
```
期望输出：
```text
2
```

### V03A-EX06 截止时间课程的反悔贪心

- 归属卷：第 3A 卷
- 覆盖模块：反悔贪心、截止时间、最大堆删除最差选择
- 考场用途：先按截止时间尝试加入，超时就删掉耗时最长的任务。

**题目描述：** 有 `n` 门课程，第 `i` 门需要 `t[i]` 天完成，必须在第 `d[i]` 天或之前完成。一天只能学习一门课的一天内容。求最多能完成多少门课。

**输入格式：** 第一行一个整数 `n`。接下来 `n` 行，每行两个整数 `t d`。

**输出格式：** 输出最多能完成的课程数。

**样例输入：**
```text
4
100 200
200 1300
1000 1250
2000 3200
```

**样例输出：**
```text
3
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

struct Course {
    long long t;
    long long d;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<Course> c(n + 1);
    for (int i = 1; i <= n; i++) cin >> c[i].t >> c[i].d;

    sort(c.begin() + 1, c.end(), [](const Course &a, const Course &b) {
        if (a.d != b.d) return a.d < b.d;
        return a.t < b.t;
    });

    priority_queue<long long> chosen;
    long long total = 0;
    for (int i = 1; i <= n; i++) {
        total += c[i].t;
        chosen.push(c[i].t);
        if (total > c[i].d) {
            total -= chosen.top();
            chosen.pop();
        }
    }

    cout << chosen.size() << '\n';
    return 0;
}
```

**测试设计：**

测试 1 输入：
```text
4
100 200
200 1300
1000 1250
2000 3200
```
期望输出：
```text
3
```

测试 2 输入：
```text
3
5 5
4 6
2 6
```
期望输出：
```text
2
```

### V03A-EX07 0/1 背包反例转 DP

- 归属卷：第 3A 卷
- 覆盖模块：贪心反例、性价比失败、0/1 背包 DP
- 考场用途：看到容量和选或不选时，不要只按价值密度贪心；普通 0/1 背包应转 DP。

**题目描述：** 有 `n` 个物品，每个物品有重量 `w[i]` 和价值 `v[i]`，每个物品最多选一次。背包容量为 `W`，求最大总价值。

**输入格式：** 第一行两个整数 `n W`。接下来 `n` 行，每行两个整数 `w v`。

**输出格式：** 输出最大总价值。

**样例输入：**
```text
3 50
10 60
20 100
30 120
```

**样例输出：**
```text
220
```

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
    for (int i = 1; i <= n; i++) cin >> w[i] >> v[i];

    vector<long long> dp(W + 1, 0);
    for (int i = 1; i <= n; i++) {
        for (int cap = W; cap >= w[i]; cap--) {
            dp[cap] = max(dp[cap], dp[cap - w[i]] + v[i]);
        }
    }

    cout << dp[W] << '\n';
    return 0;
}
```

**测试设计：**

测试 1 输入：
```text
3 50
10 60
20 100
30 120
```
期望输出：
```text
220
```

测试 2 输入：
```text
4 7
6 13
4 8
3 6
2 4
```
期望输出：
```text
14
```

### V03A-EX08 普通硬币找零反例转完全背包

- 归属卷：第 3A 卷
- 覆盖模块：贪心反例、硬币找零、完全背包 DP
- 考场用途：币值不是标准币制时，最大面值优先不可靠，应使用 DP 求最少硬币数。

**题目描述：** 给定 `n` 种硬币面值，每种硬币可以使用任意多次。求凑出金额 `S` 所需的最少硬币数；若无法凑出，输出 `-1`。

**输入格式：** 第一行两个整数 `n S`。第二行 `n` 个整数表示硬币面值。

**输出格式：** 输出最少硬币数，无法凑出输出 `-1`。

**样例输入：**
```text
3 6
1 3 4
```

**样例输出：**
```text
2
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, S;
    cin >> n >> S;
    vector<int> coin(n + 1);
    for (int i = 1; i <= n; i++) cin >> coin[i];

    const int INF = 1000000000;
    vector<int> dp(S + 1, INF);
    dp[0] = 0;
    for (int i = 1; i <= n; i++) {
        for (int sum = coin[i]; sum <= S; sum++) {
            dp[sum] = min(dp[sum], dp[sum - coin[i]] + 1);
        }
    }

    cout << (dp[S] == INF ? -1 : dp[S]) << '\n';
    return 0;
}
```

**测试设计：**

测试 1 输入：
```text
3 6
1 3 4
```
期望输出：
```text
2
```

测试 2 输入：
```text
2 7
2 4
```
期望输出：
```text
-1
```

### V03A-EX09 加权区间选择转 DP

- 归属卷：第 3A 卷
- 覆盖模块：区间贪心反例、加权区间调度、排序后二分 DP
- 考场用途：最多活动可以贪心，但最大收益区间选择通常要 DP。

**题目描述：** 给定 `n` 个半开区间 `[l, r)`，每个区间有收益 `w`。选择若干互不重叠区间，使总收益最大。端点相接不算重叠。

**输入格式：** 第一行一个整数 `n`。接下来 `n` 行，每行三个整数 `l r w`。

**输出格式：** 输出最大总收益。

**样例输入：**
```text
3
1 3 5
3 5 5
1 5 20
```

**样例输出：**
```text
20
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

struct Job {
    long long l;
    long long r;
    long long w;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<Job> job(n + 1);
    for (int i = 1; i <= n; i++) cin >> job[i].l >> job[i].r >> job[i].w;

    sort(job.begin() + 1, job.end(), [](const Job &a, const Job &b) {
        if (a.r != b.r) return a.r < b.r;
        return a.l < b.l;
    });

    vector<long long> ends(n + 1, 0);
    for (int i = 1; i <= n; i++) ends[i] = job[i].r;

    vector<long long> dp(n + 1, 0);
    for (int i = 1; i <= n; i++) {
        int p = int(upper_bound(ends.begin() + 1, ends.begin() + i, job[i].l) - ends.begin()) - 1;
        dp[i] = max(dp[i - 1], dp[p] + job[i].w);
    }

    cout << dp[n] << '\n';
    return 0;
}
```

**测试设计：**

测试 1 输入：
```text
3
1 3 5
3 5 5
1 5 20
```
期望输出：
```text
20
```

测试 2 输入：
```text
4
1 2 50
2 3 50
1 3 120
3 4 1
```
期望输出：
```text
121
```

### V03A-EX10 相邻限制选择转线性 DP

- 归属卷：第 3A 卷
- 覆盖模块：局部最优失败、线性 DP、选或不选
- 考场用途：相邻不能同时选时，不要只看当前最大值；需要记录前缀最优。

**题目描述：** 给定 `n` 个位置的收益 `a[i]`，选择若干位置，使任意两个被选位置不相邻，最大化收益和。

**输入格式：** 第一行一个整数 `n`。第二行 `n` 个整数。

**输出格式：** 输出最大收益和。

**样例输入：**
```text
5
2 7 9 3 1
```

**样例输出：**
```text
12
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<long long> a(n + 1, 0);
    for (int i = 1; i <= n; i++) cin >> a[i];

    vector<long long> dp(n + 1, 0);
    if (n >= 1) dp[1] = max(0LL, a[1]);
    for (int i = 2; i <= n; i++) {
        dp[i] = max(dp[i - 1], dp[i - 2] + a[i]);
    }

    cout << dp[n] << '\n';
    return 0;
}
```

**测试设计：**

测试 1 输入：
```text
5
2 7 9 3 1
```
期望输出：
```text
12
```

测试 2 输入：
```text
4
5 1 1 5
```
期望输出：
```text
10
```
