# MATHREF-05 递推、概率期望与博弈论

本文件定位：把“状态随步骤变化”“随机过程”“必胜必败”三类数学建模快速分流。

调用示例：线性递推先试矩阵快速幂；概率题先定义 `dp[state]` 期望；博弈题先找必胜/必败状态。

最小测试样例：斐波那契 `F(1)=1,F(2)=1,F(5)=5`；只有一步可走的博弈先手必胜。

模块编号：MATHREF-05

模块名称：递推、概率期望与博弈论参考

什么时候用：题目出现第 `n` 项、固定递推、随机过程、期望值、概率、先手必胜/必败。

不要什么时候用：普通最短路、背包或区间 DP 不需要概率/博弈公式；递推带 `max/min` 时不是矩阵快速幂。

复杂度：普通递推 `O(n*状态数)`；矩阵快速幂 `O(k^3 log n)`；小状态博弈 DP 为状态数乘转移数。

依赖的标准容器：`vector<double>`、`vector<ll>`、矩阵可用 `vector<vector<ll>>`。

接口：线性递推、矩阵快速幂入口、期望 DP 基础方程、Nim/SG 入门判断。

## 1. 递推与矩阵快速幂

题面触发词：

- 第 `n` 项、第 `n` 天、第 `n` 次操作。
- 斐波那契、线性递推。
- `n` 很大，例如 `1e18`。
- 固定转移重复执行。

使用条件：

- 普通递推：`n` 不大，可以从小到大推。
- 矩阵快速幂：状态转移是固定线性关系。
- 转移只含加法和乘法，不含 `max/min`。

公式/结论：

```text
线性递推例：
f[n] = c1*f[n-1] + c2*f[n-2] + ... + ck*f[n-k]

写成矩阵：
state[n] = T * state[n-1]
state[n] = T^(n-base) * state[base]

Fibonacci:
[F_n, F_{n-1}]^T = [[1,1],[1,0]]^(n-1) * [F_1,F_0]^T
```

C++17模板或计算方式：

```cpp
using ll = long long;

struct Mat {
    int n;
    ll mod;
    vector<vector<ll>> a;
    Mat(int n_, ll mod_) : n(n_), mod(mod_), a(n_, vector<ll>(n_, 0)) {}
};

Mat mul(const Mat &A, const Mat &B) {
    Mat C(A.n, A.mod);
    for (int i = 0; i < A.n; i++) {
        for (int k = 0; k < A.n; k++) if (A.a[i][k]) {
            for (int j = 0; j < A.n; j++) {
                C.a[i][j] = (C.a[i][j] + (__int128)A.a[i][k] * B.a[k][j]) % A.mod;
                if (C.a[i][j] < 0) C.a[i][j] += A.mod;
            }
        }
    }
    return C;
}

Mat mat_pow(Mat A, long long e) {
    Mat R(A.n, A.mod);
    for (int i = 0; i < A.n; i++) R.a[i][i] = 1 % A.mod;
    while (e) {
        if (e & 1) R = mul(R, A);
        A = mul(A, A);
        e >>= 1;
    }
    return R;
}
```

常见坑：

- 初始状态向量顺序必须与矩阵行列一致。
- `n=0/1` 边界先单独处理。
- 矩阵模板常用 0-index。
- 非线性转移不能套矩阵乘法。

暴力/部分分替代：

- `n <= 1e7`：直接递推。
- 维度太大：保留普通 DP 或找矩阵稀疏优化。

最小验错：

```text
F0=0,F1=1
F2=1,F3=2,F10=55
```

## 2. 概率与期望基础

题面触发词：

- 概率、随机、等概率。
- 期望、平均次数、期望得分。
- 抽卡、掷骰子、随机游走。
- 成功概率、失败概率。

使用条件：

- 概率总和为 1。
- 期望可以用线性性：总期望等于各部分期望之和，不要求独立。
- 若状态会转移，常写期望 DP 或方程。

公式/结论：

```text
概率：
P(A^c)=1-P(A)
P(A union B)=P(A)+P(B)-P(A intersect B)
独立时 P(A intersect B)=P(A)P(B)

期望：
E[X] = sum x * P(X=x)
线性性：E[X+Y]=E[X]+E[Y]

几何分布：
每次成功概率 p，直到第一次成功的期望次数 = 1/p
```

C++17模板或计算方式：

```cpp
// 骰子走到 >=n 的期望步数示意：dp[i] 表示从 i 到终点的期望
vector<double> dice_expectation(int n) {
    vector<double> dp(n + 6, 0.0);
    for (int i = n - 1; i >= 0; i--) {
        dp[i] = 1.0;
        for (int d = 1; d <= 6; d++) dp[i] += dp[i + d] / 6.0;
    }
    return dp;
}
```

有自环时的移项模板：

```text
E[x] = 1 + p_self * E[x] + sum(p_to * E[to])
=> E[x] = (1 + sum(p_to * E[to])) / (1 - p_self)
```

```cpp
double expectation_with_self_loop(double p_self, const vector<pair<double, double>>& next_exp) {
    const double EPS = 1e-12;
    if (p_self < -EPS || p_self > 1.0 + EPS) throw runtime_error("bad probability");
    if (1.0 - p_self < EPS) return 1e100; // 按题意可能是无穷大或不可达
    double rhs = 1.0;
    for (auto [p, e] : next_exp) {
        if (p < -EPS || p > 1.0 + EPS) throw runtime_error("bad probability");
        rhs += p * e;
    }
    return rhs / (1.0 - p_self);
}
```

考场口令：如果转移会“留在原状态”，不要直接递推；先把 `E[x]` 项移到等号左边。

常见坑：

- 期望线性性不要求独立，但概率乘法通常要求独立。
- 有自环的期望 DP 可能要移项解方程。
- 输出小数注意精度；输出模数下概率时要用逆元。
- `double` 比较不要直接 `==`。

暴力/部分分替代：

- 小状态随机过程可模拟很多次估计，但只能拿部分分/调试。
- 小数据枚举所有随机路径。
- 期望方程不会解时，先写有限步 DP 截断。

最小验错：

```text
公平硬币正面概率 1/2
直到第一次正面的期望次数 = 2

掷一次骰子的期望点数 = (1+2+3+4+5+6)/6 = 3.5
```

## 3. 博弈论 SG / 必胜必败

题面触发词：

- 两人轮流操作。
- 不能操作者输。
- 必胜、必败、先手、后手。
- 取石子、Nim、SG 函数。
- 多个独立游戏合并。

使用条件：

- 标准公平组合游戏：两人可选操作相同，无随机，无隐藏信息，不能操作者输。
- 状态图有向无环或可按大小递推。
- 多个独立子游戏用 SG 异或。

公式/结论：

```text
必败态：没有后继，或所有后继都是必胜态。
必胜态：存在一个后继是必败态。

SG(x) = mex{SG(y) | y 是 x 的后继}
多个独立游戏：
SG_total = SG1 xor SG2 xor ...
SG_total = 0 -> 先手必败
SG_total != 0 -> 先手必胜

Nim：
若所有石子堆大小 xor 为 0，先手必败；否则先手必胜。
```

C++17模板或计算方式：

```cpp
int mex_value(const vector<int> &vals) {
    vector<int> seen(vals.size() + 2, 0);
    for (int x : vals) if (0 <= x && x < (int)seen.size()) seen[x] = 1;
    for (int i = 0; ; i++) if (!seen[i]) return i;
}

vector<int> sg_take_stones(int N, const vector<int> &moves) {
    vector<int> sg(N + 1, 0);
    for (int x = 1; x <= N; x++) {
        vector<int> nxt;
        for (int mv : moves) {
            if (mv <= 0) continue;
            if (x >= mv) nxt.push_back(sg[x - mv]);
        }
        sg[x] = mex_value(nxt);
    }
    return sg;
}
```

常见坑：

- SG 只适用于公平组合游戏，不适合有随机/信息不对称/双方操作不同的题。
- “不能操作者赢”的 misere 规则不同。
- 多堆合并是异或，不是加法。
- 状态有环时不能直接递推 SG。

暴力/部分分替代：

- 小状态 DFS 判断 win/lose。
- 小堆数枚举所有操作搜索。
- Nim 题不会 SG 时先算所有堆 xor。

最小验错：

```text
取石子，每次取 1 或 2，0 为必败
sg[0]=0
sg[1]=1
sg[2]=2
sg[3]=0

Nim piles=[1,2,3]，xor=0，先手必败
```
