# MATH-05 矩阵快速幂

模块编号：MATH-05

模块名称：矩阵快速幂与线性递推

标签：[数学][矩阵][快速幂][递推]

一句话用途：把固定线性递推的第 `n` 项从逐项推 `O(n)` 升级到 `O(k^3 log n)`。

题面触发词：

- 求斐波那契第 `n` 项，`n` 很大。
- 线性递推、第 `n` 天、第 `n` 次操作。
- 状态转移固定，重复执行很多次。
- `n <= 1e18`，状态维度很小。
- 每一步从前几项线性组合得到下一项。

什么时候用：

- 状态转移可以写成 `next = T * current`。
- 转移矩阵不随时间变化。
- `n` 很大但状态维度 `k` 小，一般 `k <= 50`。
- 需要在模数下输出结果。

不要什么时候用：

- 转移每一步都变，不是固定矩阵。
- 状态维度太大，`k^3` 扛不住。
- `n` 很小，直接循环 DP 更简单。
- 转移包含 `max/min`，不是普通加乘线性递推。

复杂度：

- 矩阵乘法：`O(k^3)`。
- 矩阵快速幂：`O(k^3 log n)`。
- 矩阵乘向量：`O(k^2)`。

数据范围参考：

- `k <= 30` 且 `n <= 1e18`：很常用。
- `k <= 100`：可能还能过，注意常数。
- `k > 300`：普通矩阵快速幂通常不合适。

依赖的标准容器：

- `vector<vector<ll>>`。
- 状态向量按 0-index 存放；数学模块内部下标自然从 `0..k-1`。

输入如何整理：

```cpp
ll n, mod;
cin >> n >> mod;
// 按题意构造转移矩阵 T 和初始向量 base
```

接口：

```text
Matrix(k, mod)
identity(k, mod)
multiply(A,B)
mpow(A,e)
apply(A, vec)
```

输出能力：

- 线性递推第 `n` 项。
- 固定转移重复执行 `n` 次后的状态。
- 小维度路径计数：邻接矩阵 `A^k`。

下游可接：

- 快速幂。
- 图上固定步数路径计数。
- DP 的矩阵优化。

可拼接模块：

- MATH-02 快速幂与模运算。
- DP 线性递推。
- GRAPH 邻接矩阵路径计数。

模数是否为质数的分支：

```text
矩阵快速幂只做加法和乘法，mod 是否为质数都可以。
如果矩阵推导中需要除法或逆矩阵：
  mod 是质数 -> 可考虑费马逆元。
  mod 不是质数 -> 只有互质元素才可逆，考场低优先级，尽量改推导避免除法。
```

模板代码：

```cpp
using ll = long long;

struct Matrix {
    int n;
    ll mod;
    vector<vector<ll>> a;

    Matrix(int n_ = 0, ll mod_ = 1) {
        n = n_;
        mod = mod_;
        a.assign(n, vector<ll>(n, 0));
    }
};

Matrix identity(int n, ll mod) {
    Matrix I(n, mod);
    for (int i = 0; i < n; i++) I.a[i][i] = 1 % mod;
    return I;
}

Matrix multiply(const Matrix &A, const Matrix &B) {
    int n = A.n;
    ll mod = A.mod;
    Matrix C(n, mod);
    for (int i = 0; i < n; i++) {
        for (int k = 0; k < n; k++) {
            if (A.a[i][k] == 0) continue;
            for (int j = 0; j < n; j++) {
                C.a[i][j] = (C.a[i][j] + (__int128)A.a[i][k] * B.a[k][j]) % mod;
                if (C.a[i][j] < 0) C.a[i][j] += mod;
            }
        }
    }
    return C;
}

Matrix mpow(Matrix A, long long e) {
    Matrix res = identity(A.n, A.mod);
    while (e > 0) {
        if (e & 1) res = multiply(res, A);
        A = multiply(A, A);
        e >>= 1;
    }
    return res;
}

vector<ll> apply(const Matrix &A, const vector<ll> &v) {
    int n = A.n;
    vector<ll> res(n, 0);
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            res[i] = (res[i] + (__int128)A.a[i][j] * v[j]) % A.mod;
            if (res[i] < 0) res[i] += A.mod;
        }
    }
    return res;
}
```

调用示例：

```cpp
// Fibonacci: F0=0, F1=1
// [F_n, F_{n-1}]^T = [[1,1],[1,0]]^(n-1) * [F1,F0]^T
ll fib(ll n, ll mod) {
    if (n == 0) return 0;
    Matrix T(2, mod);
    T.a = {{1, 1}, {1, 0}};
    Matrix P = mpow(T, n - 1);
    vector<ll> base = {1, 0};
    return apply(P, base)[0];
}
```

常见坑：

- 初始向量顺序必须和转移矩阵对应。
- `n=0/1` 等边界要先判。
- 矩阵下标模板是 0-index，不要和题目 1-index 混。
- 如果 `mod` 很大，乘法用 `__int128`。
- 转移不是线性的题不要硬套矩阵。

暴力/部分分替代：

- `n <= 1e7`：直接循环递推。
- 状态很小但不会建矩阵：先写普通 DP 拿部分分。
- 图上固定步数路径小数据：重复做 `k` 次 DP。

升级方向：

- 矩阵很稀疏 -> 优化乘法或用状态转移循环。
- 多个 `n` 查询同一矩阵 -> 预处理 `T^(2^i)`。
- 递推阶数很高 -> 线性递推优化，低优先级。

最小测试样例：

```text
fib(0, 1000000007) = 0
fib(1, 1000000007) = 1
fib(10, 1000000007) = 55
```
