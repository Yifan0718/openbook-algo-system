# SIGN-MARKOV-01 马尔可夫性质、Markov 链与状态转移

模块编号：SIGN-MARKOV-01

模块名称：马尔可夫性质：Markov 链、转移矩阵、平稳分布、吸收状态、HMM 和 MDP

标签：签到题、概率、马尔可夫性质、Markov链、转移矩阵、平稳分布、吸收链、HMM、MDP、C++17

一句话用途：当题目说“下一步只和当前状态有关”、给状态转移概率矩阵、要求若干步后的分布或长期比例时，用本模块按 Markov 链处理。

题面触发词：

- 马尔可夫性质、Markov property、无后效性、记忆无关。
- 状态转移矩阵、一步转移概率、`P[i][j]`。
- 给初始分布，求第 `k` 步在各状态的概率。
- 长期稳定概率、平稳分布、steady state。
- 吸收状态、最终到达某状态的概率。
- HMM、Viterbi、MDP、强化学习。

什么时候用：

- 系统未来只由当前状态决定，不需要知道更早历史。
- 题目给的是概率状态机，而不是确定性自动机。
- 需要重复乘转移矩阵或迭代分布。
- AI/RL 题中状态、动作、转移、奖励明确给出。

不要什么时候用：

- 下一步依赖最近两步或更长历史时，原状态不满足 Markov 性质；要把“上一状态/上一步动作”等历史信息并入状态。
- 转移概率随时间改变时，不是齐次 Markov 链；要按每一步自己的矩阵乘。
- 状态数很大且步数很大时，不能直接 `O(k*n^2)`，考虑矩阵快速幂或稀疏图。
- 题目要求最短路/最优策略而非概率演化时，可能是图论或 DP。

复杂度：

- 分布迭代 `k` 步：`O(k*n^2)`。
- 转移矩阵快速幂：`O(n^3 log k)`。
- 稀疏转移每步：`O(k*m)`。
- 平稳分布迭代：`O(iter*n^2)`。
- 吸收概率可用方程组，或按迭代近似。

数据范围参考：

- `n <= 50` 且 `k` 很大：矩阵快速幂。
- `n <= 1000` 但边很少：稀疏转移迭代。
- 只问几十步：直接分布迭代最简单。
- 要长期比例且链收敛：迭代到稳定或解线性方程。

依赖的标准容器：

- 静态数组 `double P[MAXN][MAXN]`：转移矩阵，1-index。
- 静态数组 `double dist[MAXN]`：当前分布。
- `vector<pair<int,double>> g[MAXN]`：稀疏转移。
- `iomanip`：概率输出。

输入如何整理：

```text
1. 状态编号统一 1..n。
2. P[i][j] 表示从状态 i 到状态 j 的概率。
3. 每行概率和通常为 1；若题面允许误差，用 EPS 检查。
4. 初始分布 dist[i] 也应和为 1。
```

接口：

```text
iterate_distribution(n,k,dist,P) -> 直接做 k 步分布。
matrix_power_distribution(n,k,dist,P) -> 矩阵快速幂做 k 步分布。
stationary_iter(n,dist,P,iter) -> 迭代近似平稳分布。
is_markov_state_enough() -> 若未来还依赖历史，升维状态。
```

常见坑：

- 把 `P[i][j]` 当成 `P[j][i]`，行列方向反了。
- 初始分布不是概率分布，和不为 1。
- 每行转移概率和不为 1，却没有按题面解释成权重。
- 题目实际依赖上一步动作或上一个状态，却只把当前位置当状态。
- 矩阵快速幂中行向量/列向量约定混乱。
- 平稳分布不一定存在唯一极限，周期链可能震荡。
- 浮点输出不要用 `==` 比较概率。

暴力/部分分替代：

- `k` 小时直接一步一步模拟分布。
- 状态数小但历史依赖时，把最近历史并入状态，例如 `(当前点, 上一步方向)`。
- 不会平稳分布精确解时，迭代 1000 到 10000 轮拿近似分。
- 吸收概率不会列方程时，迭代很多步近似最终分布。
- HMM 不会 Viterbi 时，小规模枚举隐状态序列拿部分分。

## 1. Markov 性质到底是什么

核心公式：

```text
P(X_{t+1}=j | X_t=i, X_{t-1}, ..., X_0) = P(X_{t+1}=j | X_t=i)
```

中文口令：

```text
未来只看现在，不看过去。
```

这和 DP 的“无后效性”很像：

| DP 语境 | Markov 语境 |
|---|---|
| 状态包含决定未来的全部信息 | 当前状态包含下一步概率所需全部信息 |
| 历史不影响后续转移 | 更早历史不影响下一步概率 |
| 有后效性就升维 | 不满足 Markov 就把关键历史并入状态 |

例子：

```text
不能连续向下走两步：
只用位置 (i,j) 不够，因为下一步能否向下取决于上一步方向。
升维为 (i,j,last_dir) 后，就恢复 Markov/无后效性。
```

## 2. 转移矩阵

若有 `n` 个状态，`P[i][j]` 表示从 `i` 到 `j` 的概率。

```text
dist_next[j] = sum_i dist[i] * P[i][j]
```

矩阵写法：

```text
dist_after_k = dist_initial * P^k
```

注意：

- 本卷默认行向量分布，所以是 `dist * P`。
- 有些教材用列向量，会写 `P * dist`，不要混淆。
- 竞赛题通常直接给 `P[i][j]`，按题意。

## 3. 直接迭代模板

适合 `k` 不大，或者 `n` 较大但转移稀疏。

```cpp
const int MAXN = 105;
double P[MAXN][MAXN], distv[MAXN], ndist[MAXN];

void iterate_distribution(int n, long long k) {
    for (long long step = 1; step <= k; step++) {
        for (int j = 1; j <= n; j++) ndist[j] = 0;
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= n; j++) {
                ndist[j] += distv[i] * P[i][j];
            }
        }
        for (int j = 1; j <= n; j++) distv[j] = ndist[j];
    }
}
```

## 4. 矩阵快速幂模板

适合 `k` 很大、`n` 不大。

```cpp
const int MAXN = 105;
int N;
double A[MAXN][MAXN], R[MAXN][MAXN], T[MAXN][MAXN];

void mat_mul(double X[][MAXN], double Y[][MAXN], double Z[][MAXN]) {
    static double C[MAXN][MAXN];
    for (int i = 1; i <= N; i++) {
        for (int j = 1; j <= N; j++) {
            C[i][j] = 0;
            for (int k = 1; k <= N; k++) C[i][j] += X[i][k] * Y[k][j];
        }
    }
    for (int i = 1; i <= N; i++) {
        for (int j = 1; j <= N; j++) Z[i][j] = C[i][j];
    }
}

void mat_pow(long long e) {
    for (int i = 1; i <= N; i++) {
        for (int j = 1; j <= N; j++) R[i][j] = (i == j);
    }
    while (e > 0) {
        if (e & 1) mat_mul(R, A, R);
        mat_mul(A, A, A);
        e >>= 1;
    }
}
```

得到 `P^k` 后：

```cpp
for (int j = 1; j <= n; j++) {
    ans[j] = 0;
    for (int i = 1; i <= n; i++) ans[j] += dist[i] * R[i][j];
}
```

## 5. 平稳分布

平稳分布 `pi` 满足：

```text
pi = pi * P
sum pi[i] = 1
```

直觉：

- 如果链满足一定连通/非周期条件，反复转移会趋向一个稳定分布。
- 题目若只要求近似，直接迭代很多轮通常够用。

```cpp
void stationary_iter(int n, int iter) {
    for (int i = 1; i <= n; i++) distv[i] = 1.0 / n;
    for (int step = 1; step <= iter; step++) {
        for (int j = 1; j <= n; j++) ndist[j] = 0;
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= n; j++) ndist[j] += distv[i] * P[i][j];
        }
        for (int j = 1; j <= n; j++) distv[j] = ndist[j];
    }
}
```

## 6. 吸收状态

吸收状态：

```text
P[x][x] = 1，且不会离开 x。
```

常见问题：

- 最终被哪个吸收状态吸收的概率。
- 到吸收状态的期望步数。

处理方式：

| 问题 | 方法 |
|---|---|
| 小数据近似 | 迭代很多步 |
| 精确吸收概率 | 列线性方程组，用 `SIM-07` 高斯 |
| 期望步数 | `E[u] = 1 + sum P[u][v]E[v]`，吸收态 `E=0` |

## 7. HMM、MDP、强化学习的关系

| 名称 | 核心 |
|---|---|
| Markov 链 | 只有状态转移 |
| HMM | 隐状态 Markov，另有观测概率 |
| MDP | 状态 + 动作 + 转移概率 + 奖励 |
| Q-learning | 学 `Q[state][action]` |
| Viterbi | HMM 中求最可能隐状态路径 |

HMM 的两个概率：

```text
transition: P(hidden_t -> hidden_{t+1})
emission: P(observation_t | hidden_t)
```

MDP 的 Markov 性质：

```text
下一状态和奖励只依赖当前状态与当前动作，不依赖更早历史。
```

## 8. 完整可运行模板

支持三种模式：

- `step`：直接迭代 `k` 步。
- `power`：矩阵快速幂求 `k` 步。
- `stationary`：迭代近似平稳分布。

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MAXN = 105;
int N;
double P[MAXN][MAXN], A[MAXN][MAXN], R[MAXN][MAXN];
double distv[MAXN], ansv[MAXN], ndist[MAXN];

void mat_mul(double X[][MAXN], double Y[][MAXN], double Z[][MAXN]) {
    static double C[MAXN][MAXN];
    for (int i = 1; i <= N; i++) {
        for (int j = 1; j <= N; j++) {
            C[i][j] = 0;
            for (int k = 1; k <= N; k++) C[i][j] += X[i][k] * Y[k][j];
        }
    }
    for (int i = 1; i <= N; i++) {
        for (int j = 1; j <= N; j++) Z[i][j] = C[i][j];
    }
}

void mat_pow(long long e) {
    for (int i = 1; i <= N; i++) {
        for (int j = 1; j <= N; j++) R[i][j] = (i == j ? 1.0 : 0.0);
    }
    while (e > 0) {
        if (e & 1) mat_mul(R, A, R);
        mat_mul(A, A, A);
        e >>= 1;
    }
}

void print_dist(double d[]) {
    cout << fixed << setprecision(6);
    for (int i = 1; i <= N; i++) {
        if (i > 1) cout << ' ';
        cout << d[i];
    }
    cout << "\n";
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string mode;
    long long k;
    cin >> mode >> N >> k;
    for (int i = 1; i <= N; i++) cin >> distv[i];
    for (int i = 1; i <= N; i++) {
        for (int j = 1; j <= N; j++) {
            cin >> P[i][j];
            A[i][j] = P[i][j];
        }
    }

    if (mode == "step") {
        for (long long step = 1; step <= k; step++) {
            for (int j = 1; j <= N; j++) ndist[j] = 0;
            for (int i = 1; i <= N; i++) {
                for (int j = 1; j <= N; j++) ndist[j] += distv[i] * P[i][j];
            }
            for (int j = 1; j <= N; j++) distv[j] = ndist[j];
        }
        print_dist(distv);
    } else if (mode == "power") {
        mat_pow(k);
        for (int j = 1; j <= N; j++) {
            ansv[j] = 0;
            for (int i = 1; i <= N; i++) ansv[j] += distv[i] * R[i][j];
        }
        print_dist(ansv);
    } else if (mode == "stationary") {
        for (int i = 1; i <= N; i++) distv[i] = 1.0 / N;
        for (long long step = 1; step <= k; step++) {
            for (int j = 1; j <= N; j++) ndist[j] = 0;
            for (int i = 1; i <= N; i++) {
                for (int j = 1; j <= N; j++) ndist[j] += distv[i] * P[i][j];
            }
            for (int j = 1; j <= N; j++) distv[j] = ndist[j];
        }
        print_dist(distv);
    }
    return 0;
}
```

## 9. 最小测试样例

```text
step 2 2
1 0
0.5 0.5
0.2 0.8
=> 0.350000 0.650000

power 2 10
1 0
0.5 0.5
0.2 0.8
=> 0.285735 0.714265

stationary 2 100
0 0
0.5 0.5
0.2 0.8
=> 0.285714 0.714286
```

## 10. 考场判断清单

- 当前状态是否包含影响未来的全部信息？
- 转移概率每行是否和为 1？
- 分布是行向量还是列向量？
- `k` 大不大？大则考虑矩阵快速幂。
- 是否有吸收态？
- 是否要求最优策略？若是 MDP/强化学习，不只是普通 Markov 链。
