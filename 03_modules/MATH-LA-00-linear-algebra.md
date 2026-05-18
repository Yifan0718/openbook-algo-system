# MATH-LA-00 基础线性代数

模块编号：MATH-LA-00

模块名称：Matrix、Gaussian Elimination 与 XOR Basis

标签：[数学][线性代数][矩阵][高斯消元][线性基][异或]

一句话用途：处理矩阵乘法、线性方程组、模意义方程组和异或最大值等基础线性代数题。

题面触发词：

- 矩阵、矩阵乘法、单位矩阵。
- 解线性方程组。
- 高斯消元、唯一解、无解、无穷多解。
- 答案对质数取模。
- 异或最大值、选若干数异或、线性基。

什么时候用：

- 方程是一次线性的：`a1*x1 + ... + am*xm = b`。
- 小维度矩阵需要乘法或快速幂前置。
- 异或题允许从一堆数中任选若干个。
- 模意义高斯消元的模数通常是质数。

不要什么时候用：

- 方程有乘积、平方、`max/min` 等非线性项。
- 浮点方程精度要求极高，普通 `double` 不够。
- 模数不是质数且需要除法，不能直接用费马逆元。
- 异或线性基只处理 xor，不处理普通加法最大子集和。

复杂度：

- 矩阵乘法：`O(n*m*p)`。
- 高斯消元：`O(n*m^2)`，方阵常写作 `O(n^3)`。
- 异或线性基插入/查询：`O(LOG)`。

数据范围参考：

- 高斯消元 `n <= 200` 比较常见。
- 矩阵快速幂维度通常 `<= 50`。
- `long long` 异或线性基用 `LOG = 63`，覆盖非负 signed `long long` 的 bit 0..62。

依赖的标准容器：

- 1-index 矩阵：`vector<vector<ll>> a(n + 1, vector<ll>(m + 1))`。
- 增广矩阵：`a[i][1..m]` 是系数，`a[i][m+1]` 是常数。

输入如何整理：

```cpp
int n, m; // n 个方程，m 个未知数
cin >> n >> m;
vector<vector<double>> a(n + 1, vector<double>(m + 2));
for (int i = 1; i <= n; i++) {
    for (int j = 1; j <= m + 1; j++) cin >> a[i][j];
}
```

接口：

```text
Matrix mul(A,B,mod)
gauss_double(a,x) -> 0 无解，1 唯一解，2 无穷多解
gauss_mod(a,x,MOD) -> 0 无解，1 唯一解，2 无穷多解
XorBasis.insert(x), max_xor(seed), can(x)
```

输出能力：

- 矩阵乘积。
- 实数线性方程组解。
- 质数模意义下线性方程组解。
- 可选子集异或出的最大值、某个值是否能表示。

下游可接：

- 矩阵快速幂。
- 概率期望方程。
- 图论 Kirchhoff 矩阵树，低优先级。
- 异或贪心、异或路径。

可拼接模块：

- `MATH-LA-00 + MATH-02 FastPower`。
- `MATH-LA-00 + MATH-05 MatrixFastPower`。
- `MATH-LA-00 + GRAPH` 异或环线性基。

矩阵基础模板：

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Matrix {
    int n, m;
    vector<vector<ll>> a;

    Matrix(int n_ = 0, int m_ = 0) {
        n = n_;
        m = m_;
        a.assign(n + 1, vector<ll>(m + 1, 0));
    }

    static Matrix identity(int n) {
        Matrix I(n, n);
        for (int i = 1; i <= n; i++) I.a[i][i] = 1;
        return I;
    }
};

Matrix mul(const Matrix &A, const Matrix &B, ll mod) {
    assert(A.m == B.n && mod > 0);
    Matrix C(A.n, B.m);
    for (int i = 1; i <= A.n; i++) {
        for (int k = 1; k <= A.m; k++) {
            if (A.a[i][k] == 0) continue;
            for (int j = 1; j <= B.m; j++) {
                C.a[i][j] = (C.a[i][j] + (__int128)A.a[i][k] * B.a[k][j]) % mod;
                if (C.a[i][j] < 0) C.a[i][j] += mod;
            }
        }
    }
    return C;
}
```

高斯消元模板：`double`

```cpp
#include <bits/stdc++.h>
using namespace std;

const double EPS = 1e-9;

// a 是 1-index 增广矩阵：n 行，m 个未知数，常数列在 m+1。
// 返回 0 无解，1 唯一解，2 无穷多解。
int gauss_double(vector<vector<double>> a, vector<double> &x) {
    int n = (int)a.size() - 1;
    int m = (int)a[1].size() - 2;
    vector<int> where(m + 1, -1);

    int row = 1;
    for (int col = 1; col <= m && row <= n; col++) {
        int sel = row;
        for (int i = row; i <= n; i++) {
            if (fabs(a[i][col]) > fabs(a[sel][col])) sel = i;
        }
        if (fabs(a[sel][col]) < EPS) continue;

        swap(a[sel], a[row]);
        where[col] = row;

        double div = a[row][col];
        for (int j = col; j <= m + 1; j++) a[row][j] /= div;

        for (int i = 1; i <= n; i++) {
            if (i == row) continue;
            if (fabs(a[i][col]) < EPS) continue;
            double factor = a[i][col];
            for (int j = col; j <= m + 1; j++) {
                a[i][j] -= factor * a[row][j];
            }
        }
        row++;
    }

    for (int i = 1; i <= n; i++) {
        bool all_zero = true;
        for (int j = 1; j <= m; j++) {
            if (fabs(a[i][j]) > EPS) all_zero = false;
        }
        if (all_zero && fabs(a[i][m + 1]) > EPS) return 0;
    }

    x.assign(m + 1, 0);
    for (int col = 1; col <= m; col++) {
        if (where[col] != -1) x[col] = a[where[col]][m + 1];
    }

    for (int col = 1; col <= m; col++) {
        if (where[col] == -1) return 2;
    }
    return 1;
}
```

模意义高斯消元骨架：质数模

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

ll norm(ll x, ll mod) {
    x %= mod;
    if (x < 0) x += mod;
    return x;
}

ll mod_pow(ll a, ll e, ll mod) {
    ll res = 1 % mod;
    a = norm(a, mod);
    while (e > 0) {
        if (e & 1) res = (ll)((__int128)res * a % mod);
        a = (ll)((__int128)a * a % mod);
        e >>= 1;
    }
    return res;
}

// MOD 必须是质数；a 是 1-index 增广矩阵。
// 返回 0 无解，1 唯一解，2 无穷多解。
int gauss_mod(vector<vector<ll>> a, vector<ll> &x, ll MOD) {
    int n = (int)a.size() - 1;
    int m = (int)a[1].size() - 2;
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m + 1; j++) a[i][j] = norm(a[i][j], MOD);
    }

    vector<int> where(m + 1, -1);
    int row = 1;

    for (int col = 1; col <= m && row <= n; col++) {
        int sel = 0;
        for (int i = row; i <= n; i++) {
            if (a[i][col] != 0) {
                sel = i;
                break;
            }
        }
        if (sel == 0) continue;

        swap(a[sel], a[row]);
        where[col] = row;

        ll inv = mod_pow(a[row][col], MOD - 2, MOD);
        for (int j = col; j <= m + 1; j++) {
            a[row][j] = (ll)((__int128)a[row][j] * inv % MOD);
        }

        for (int i = 1; i <= n; i++) {
            if (i == row || a[i][col] == 0) continue;
            ll factor = a[i][col];
            for (int j = col; j <= m + 1; j++) {
                ll sub = (ll)((__int128)factor * a[row][j] % MOD);
                a[i][j] = norm(a[i][j] - sub, MOD);
            }
        }
        row++;
    }

    for (int i = 1; i <= n; i++) {
        bool all_zero = true;
        for (int j = 1; j <= m; j++) {
            if (a[i][j] != 0) all_zero = false;
        }
        if (all_zero && a[i][m + 1] != 0) return 0;
    }

    x.assign(m + 1, 0);
    for (int col = 1; col <= m; col++) {
        if (where[col] != -1) x[col] = a[where[col]][m + 1];
    }

    for (int col = 1; col <= m; col++) {
        if (where[col] == -1) return 2;
    }
    return 1;
}
```

异或线性基模板：

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct XorBasis {
    static const int LOG = 63;
    ll b[LOG];

    XorBasis() {
        memset(b, 0, sizeof(b));
    }

    bool insert(ll x) {
        for (int i = LOG - 1; i >= 0; i--) {
            if (((x >> i) & 1LL) == 0) continue;
            if (b[i] == 0) {
                b[i] = x;
                return true;
            }
            x ^= b[i];
        }
        return false;
    }

    ll max_xor(ll seed = 0) const {
        ll res = seed;
        for (int i = LOG - 1; i >= 0; i--) {
            res = max(res, res ^ b[i]);
        }
        return res;
    }

    bool can(ll x) const {
        for (int i = LOG - 1; i >= 0; i--) {
            if (((x >> i) & 1LL) == 0) continue;
            if (b[i] == 0) return false;
            x ^= b[i];
        }
        return true;
    }

    int rank() const {
        int res = 0;
        for (int i = 0; i < LOG; i++) {
            if (b[i]) res++;
        }
        return res;
    }
};
```

调用示例：

```cpp
vector<double> x;
int type = gauss_double(a, x);
if (type == 1) {
    for (int i = 1; i < (int)x.size(); i++) cout << x[i] << '\n';
}

XorBasis xb;
for (int i = 1; i <= n; i++) xb.insert(a[i]);
cout << xb.max_xor() << '\n';
```

常见坑：

- 高斯消元读的是增广矩阵，列数要开到 `m+2`。
- `double` 比较必须用 `EPS`，不要直接 `== 0`。
- 模意义高斯消元只有在 pivot 可逆时才能除；质数模下非零元素都可逆。
- 模数不是质数时，`pow(a, MOD-2)` 求逆元是错的。
- 异或线性基默认处理非负 `long long`；如果题目有符号数，先确认位数和比较规则。
- 线性基插入失败表示这个数可由已有数异或出来，不代表它没用错了。

暴力/部分分替代：

- 方程数量很小：枚举未知数或手推。
- 模方程未知数很少且取值范围小：DFS 枚举。
- 异或最大值 `n <= 24`：枚举所有子集。
- 只需要矩阵乘法，不需要快速幂：直接三重循环。

升级方向：

- 矩阵基础 -> 矩阵快速幂。
- 高斯消元 -> 期望 DP 方程组。
- 异或线性基 -> 图上异或环、路径最大异或。
- 模高斯 -> 矩阵求逆、行列式，低优先级。

最小测试样例：

```text
double 方程：
x + y = 3
x - y = 1
解：x=2, y=1

线性基：
1 2 3
最大异或：3
```
