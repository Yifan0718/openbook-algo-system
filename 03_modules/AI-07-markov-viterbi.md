# AI-07 Markov 链、HMM 与 Viterbi

模块编号：AI-07

模块名称：Markov 状态转移、隐马尔可夫模型与 Viterbi 最可能路径

标签：AI、概率模型、Markov、HMM、Viterbi、动态规划、C++17

一句话用途：当题目出现状态转移概率、观测序列、最可能隐藏状态路径时，用 Viterbi 把概率模型变成 DP。

题面触发词：

- Markov、状态转移、转移矩阵。
- hidden state、observation、emission probability。
- 给观测序列，求最可能状态序列。
- 概率连乘、路径最大概率。

什么时候用：

- 下一步状态只依赖当前状态。
- 观测概率只依赖当前隐藏状态。
- 要最大概率路径，而不是总概率。

不要什么时候用：

- 只求所有路径概率总和时，用 forward DP，不是 Viterbi max。
- 概率极小，不能直接乘很多次；本模板用 log。
- 状态数和序列长很大时，`O(T*n^2)` 可能 TLE。

复杂度：

- Viterbi：`O(T * n^2)`。
- 空间：`O(T*n)` 用于回溯路径；只求概率可滚动。

依赖的标准容器：

- `vector<vector<double>>`：log 概率 DP。
- `vector<vector<int>>`：前驱路径。
- `vector<int>`：观测序列。

输入如何整理：

```cpp
int n, m, T;
cin >> n >> m >> T;
```

接口：

```text
pi[i] 初始概率。
trans[i][j] 状态 i 到 j 的概率。
emit[i][o] 状态 i 产生观测 o 的概率。
obs[t] 第 t 个观测。
```

模板代码：

```cpp
#include <bits/stdc++.h>
using namespace std;

const double NEG = -1e100;

double safe_log(double x) {
    if (x <= 0) return NEG;
    return log(x);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m, T;
    cin >> n >> m >> T;
    if (n <= 0 || m <= 0 || T <= 0) throw runtime_error("bad size");

    vector<double> pi(n + 1);
    for (int i = 1; i <= n; i++) cin >> pi[i];

    vector<vector<double>> trans(n + 1, vector<double>(n + 1));
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++) cin >> trans[i][j];
    }

    vector<vector<double>> emit(n + 1, vector<double>(m + 1));
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) cin >> emit[i][j];
    }

    vector<int> obs(T + 1);
    for (int t = 1; t <= T; t++) {
        cin >> obs[t];
        if (obs[t] < 1 || obs[t] > m) throw runtime_error("bad observation");
    }

    vector<vector<double>> dp(T + 1, vector<double>(n + 1, NEG));
    vector<vector<int>> pre(T + 1, vector<int>(n + 1, 0));

    for (int s = 1; s <= n; s++) {
        dp[1][s] = safe_log(pi[s]) + safe_log(emit[s][obs[1]]);
    }

    for (int t = 2; t <= T; t++) {
        for (int s = 1; s <= n; s++) {
            for (int p = 1; p <= n; p++) {
                double cur = dp[t - 1][p] + safe_log(trans[p][s]) + safe_log(emit[s][obs[t]]);
                if (cur > dp[t][s]) {
                    dp[t][s] = cur;
                    pre[t][s] = p;
                }
            }
        }
    }

    int last = 1;
    for (int s = 2; s <= n; s++) {
        if (dp[T][s] > dp[T][last]) last = s;
    }
    if (dp[T][last] <= NEG / 2) {
        cout << fixed << setprecision(6) << 0.0 << '\n';
        cout << -1 << '\n';
        return 0;
    }

    vector<int> path(T + 1);
    path[T] = last;
    for (int t = T; t >= 2; t--) {
        if (pre[t][path[t]] == 0) throw runtime_error("broken path");
        path[t - 1] = pre[t][path[t]];
    }

    cout << fixed << setprecision(6) << exp(dp[T][last]) << '\n';
    for (int t = 1; t <= T; t++) {
        if (t > 1) cout << ' ';
        cout << path[t];
    }
    cout << '\n';

    return 0;
}
```

调用示例：

```cpp
// 按 HMM 输入后输出最大概率和隐藏状态路径。
```

常见坑：

- 概率为 0 时 log 是负无穷，要特殊处理。
- Viterbi 是取最大路径，不是概率求和。
- 输出概率可能很小，题面可能要求输出 log 概率。
- 如果路径 tie-break 有要求，要在 `cur > dp` 改成带编号比较。

暴力/部分分替代：

- 状态数小、T 小：暴力枚举所有路径。
- 不会 log：小数据直接乘概率。
- 只要最终状态：不保存 pre，滚动数组。

最小测试样例：

```text
输入
2 2 3
0.5 0.5
0.9 0.1
0.2 0.8
0.8 0.2
0.1 0.9
1 2 2

输出
0.025920
1 2 2
```
