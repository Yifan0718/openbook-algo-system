# SIM-07 方程求解：高斯消元、模方程、一元方程与多项式

模块编号：SIM-07

模块名称：方程求解模板：线性方程组、高斯消元、模意义方程、一元方程迭代、多项式求值与低次公式

标签：模拟、数学、方程求解、高斯消元、模方程、二分、牛顿法、多项式、C++17、考场模板

一句话用途：题目把条件写成若干方程、要求求未知数或判无解/多解时，先判断是线性方程组、模方程、一元连续方程还是低次多项式，再套对应模板。

题面触发词：

- 给出 `n` 个未知数和 `m` 条线性约束，求每个未知数。
- 解方程组、判断唯一解/无解/无穷多解。
- 所有运算在 `mod p` 意义下进行。
- 求 `f(x)=0` 的一个根，答案允许误差 `1e-6`。
- 给多项式系数，求某点函数值或求区间内根。
- 一元一次/二次方程，输出实根。

什么时候用：

- 方程是一次的：用高斯消元，实数版或模质数版。
- 单条同余方程 `a*x ≡ b (mod m)`：用 `gcd + exgcd`。
- 一元连续函数有单调性或已知区间两端异号：用二分。
- 已有较好初值、函数和导数好算：可用牛顿法做加速或备用。
- 多项式求值：用 Horner，少写幂函数。
- 一元一次/二次：直接公式，比迭代更稳。

不要什么时候用：

- 模数不是质数且是多元方程组：普通模高斯只对可逆主元安全，复合模需要拆 CRT 或更高阶线性代数。
- 方程里有乘积项如 `x*y`、`x^2+y^2`：不是线性方程组，不能直接高斯。
- 二分区间两端不异号且没有单调性证明：可能漏根。
- 牛顿法没有好初值或导数会接近 0：容易飞出有效区间。
- 只要求整数解且变量范围很小：直接枚举/搜索可能更短。

复杂度：

- 实数高斯消元：`O(m*n*min(m,n))`，方阵常记 `O(n^3)`。
- 模质数高斯消元：同上，每个主元多一次快速幂求逆，方阵约 `O(n^3 + n log mod)`。
- 单条线性同余：`O(log mod)`。
- 二分求根：`O(iter * eval)`，常用 80 到 100 次。
- 牛顿法：`O(iter * eval)`，常用 30 到 60 次。
- Horner 多项式求值：`O(deg)`。
- 一次/二次公式：`O(1)`。

数据范围参考：

- `n <= 100`：静态二维数组高斯最舒服。
- `n <= 500`：`O(n^3)` 可能还能过，注意常数和时限。
- 模数为 `998244353`、`1e9+7` 等质数时，模高斯最稳。
- 浮点答案误差 `1e-6`：二分 80 次通常足够。
- 多项式次数高且 `x` 很大时，`double` 可能溢出，按题意改 `long double` 或取模 Horner。

依赖的标准容器：

- 静态数组 `a[MAXN][MAXN]`：方程矩阵，行列按 1-index。
- `double`：实数高斯、二分、牛顿、公式根。
- `long long`：模方程系数和答案。
- `vector<double>`：只在输出低次公式根时临时装答案；核心矩阵仍是静态数组。

输入如何整理：

```cpp
int m, n;
cin >> m >> n;
for (int i = 1; i <= m; i++) {
    for (int j = 1; j <= n; j++) cin >> a[i][j];
    cin >> a[i][n + 1]; // 右端常数
}
```

接口：

```text
gauss_real(m,n) -> 0 无解，1 唯一解，2 多解；答案在 ans_real[1..n]。
gauss_mod_prime(m,n,mod) -> 模质数方程组，返回值同上；答案在 ans_mod[1..n]。
solve_linear_congruence(a,b,mod,x0,step) -> 解 a*x ≡ b (mod mod)，通解 x=x0+k*step。
poly_eval(deg,c,x) -> Horner 求 c[0]+c[1]x+...+c[deg]x^deg。
poly_derivative_eval(deg,c,x) -> 多项式导数在 x 的值。
bisect_poly_root(deg,c,l,r,root) -> 区间两端异号时二分一个根。
newton_poly_root(deg,c,start,root) -> 从 start 出发尝试牛顿求根。
solve_quadratic_formula(a,b,c,roots) -> 解 a*x^2+b*x+c=0，返回根数，-1 表示任意实数。
```

## 先判断题目属于哪一类

| 题面形式 | 优先模板 | 关键检查 |
|---|---|---|
| `a11*x1+...+a1n*xn=b1` | 实数高斯 | `EPS`、主元、无解/多解 |
| 同上但 `mod p` | 模质数高斯 | `p` 是质数、负数取模 |
| `a*x ≡ b (mod m)` | `gcd + exgcd` | `gcd(a,m)` 是否整除 `b` |
| `f(x)=0`，连续且有区间 | 二分 | 两端异号或单调性 |
| `f(x)=0`，有导数和初值 | 牛顿 | 导数别接近 0 |
| 多项式代入 | Horner | 系数顺序和溢出 |
| 一次/二次 | 公式 | 退化和判别式 `EPS` |

## 高斯消元的行列约定

增广矩阵按 1-index 存：

```text
a[i][1..n]     是第 i 条方程的系数
a[i][n + 1]    是右端常数
ans[1..n]      是未知数 x1..xn
where[col]     记录第 col 个未知数在哪一行成为主元
```

判定顺序：

1. 每一列找绝对值最大的主元。
2. 主元行归一化。
3. 消掉其他所有行的这一列。
4. 最后检查 `0 = 非零`，这是无解。
5. 有变量没主元，是多解；所有变量有主元，是唯一解。

模板代码：

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

const int MAXN = 105;
const double EPS = 1e-10;

double mat_real[MAXN][MAXN];
double ans_real[MAXN];
int where_real[MAXN];

ll mat_mod[MAXN][MAXN];
ll ans_mod[MAXN];
int where_mod[MAXN];

double coef_poly[MAXN];

int sign_double(double x) {
    if (x > EPS) return 1;
    if (x < -EPS) return -1;
    return 0;
}

ll norm_mod(ll x, ll mod) {
    x %= mod;
    if (x < 0) x += mod;
    return x;
}

ll mul_mod(ll a, ll b, ll mod) {
    return (ll)((__int128)norm_mod(a, mod) * norm_mod(b, mod) % mod);
}

ll pow_mod(ll a, ll e, ll mod) {
    ll res = 1 % mod;
    a = norm_mod(a, mod);
    while (e > 0) {
        if (e & 1) res = mul_mod(res, a, mod);
        a = mul_mod(a, a, mod);
        e >>= 1;
    }
    return res;
}

ll exgcd(ll a, ll b, ll &x, ll &y) {
    if (b == 0) {
        x = 1;
        y = 0;
        return a;
    }
    ll x1, y1;
    ll g = exgcd(b, a % b, x1, y1);
    x = y1;
    y = x1 - (a / b) * y1;
    return g;
}

ll inv_mod_coprime(ll a, ll mod) {
    ll x, y;
    ll g = exgcd(norm_mod(a, mod), mod, x, y);
    if (g != 1) return -1;
    return norm_mod(x, mod);
}

int gauss_real(int m, int n) {
    for (int i = 1; i <= n; i++) where_real[i] = 0;

    int row = 1;
    for (int col = 1; col <= n && row <= m; col++) {
        int sel = row;
        for (int i = row + 1; i <= m; i++) {
            if (fabs(mat_real[i][col]) > fabs(mat_real[sel][col])) {
                sel = i;
            }
        }
        if (fabs(mat_real[sel][col]) < EPS) continue;

        for (int j = col; j <= n + 1; j++) {
            swap(mat_real[sel][j], mat_real[row][j]);
        }

        where_real[col] = row;
        double div = mat_real[row][col];
        for (int j = col; j <= n + 1; j++) mat_real[row][j] /= div;

        for (int i = 1; i <= m; i++) {
            if (i == row) continue;
            double factor = mat_real[i][col];
            if (fabs(factor) < EPS) continue;
            for (int j = col; j <= n + 1; j++) {
                mat_real[i][j] -= factor * mat_real[row][j];
            }
        }
        row++;
    }

    for (int i = 1; i <= m; i++) {
        bool all_zero = true;
        for (int j = 1; j <= n; j++) {
            if (fabs(mat_real[i][j]) > EPS) {
                all_zero = false;
                break;
            }
        }
        if (all_zero && fabs(mat_real[i][n + 1]) > EPS) return 0;
    }

    for (int i = 1; i <= n; i++) {
        ans_real[i] = where_real[i] ? mat_real[where_real[i]][n + 1] : 0.0;
    }
    for (int i = 1; i <= n; i++) {
        if (!where_real[i]) return 2;
    }
    return 1;
}

int gauss_mod_prime(int m, int n, ll mod) {
    for (int i = 1; i <= n; i++) where_mod[i] = 0;

    int row = 1;
    for (int col = 1; col <= n && row <= m; col++) {
        int sel = 0;
        for (int i = row; i <= m; i++) {
            if (norm_mod(mat_mod[i][col], mod) != 0) {
                sel = i;
                break;
            }
        }
        if (!sel) continue;

        for (int j = col; j <= n + 1; j++) {
            swap(mat_mod[sel][j], mat_mod[row][j]);
            mat_mod[row][j] = norm_mod(mat_mod[row][j], mod);
        }

        where_mod[col] = row;
        ll inv = pow_mod(mat_mod[row][col], mod - 2, mod);
        for (int j = col; j <= n + 1; j++) {
            mat_mod[row][j] = mul_mod(mat_mod[row][j], inv, mod);
        }

        for (int i = 1; i <= m; i++) {
            if (i == row) continue;
            ll factor = norm_mod(mat_mod[i][col], mod);
            if (factor == 0) continue;
            for (int j = col; j <= n + 1; j++) {
                mat_mod[i][j] = norm_mod(mat_mod[i][j] - mul_mod(factor, mat_mod[row][j], mod), mod);
            }
        }
        row++;
    }

    for (int i = 1; i <= m; i++) {
        bool all_zero = true;
        for (int j = 1; j <= n; j++) {
            if (norm_mod(mat_mod[i][j], mod) != 0) {
                all_zero = false;
                break;
            }
        }
        if (all_zero && norm_mod(mat_mod[i][n + 1], mod) != 0) return 0;
    }

    for (int i = 1; i <= n; i++) {
        ans_mod[i] = where_mod[i] ? norm_mod(mat_mod[where_mod[i]][n + 1], mod) : 0;
    }
    for (int i = 1; i <= n; i++) {
        if (!where_mod[i]) return 2;
    }
    return 1;
}

bool solve_linear_congruence(ll a, ll b, ll mod, ll &x0, ll &step) {
    if (mod <= 0) return false;
    if (mod == 1) {
        x0 = 0;
        step = 1;
        return true;
    }

    ll aa = norm_mod(a, mod);
    ll g = gcd(aa, mod);
    if (b % g != 0) return false;

    ll reduced_mod = mod / g;
    if (reduced_mod == 1) {
        x0 = 0;
        step = 1;
        return true;
    }

    ll inv = inv_mod_coprime(aa / g, reduced_mod);
    if (inv < 0) return false;
    ll rhs = norm_mod(b / g, reduced_mod);
    x0 = mul_mod(rhs, inv, reduced_mod);
    step = reduced_mod;
    return true;
}

double poly_eval(int deg, const double c[], double x) {
    double res = c[deg];
    for (int i = deg - 1; i >= 0; i--) {
        res = res * x + c[i];
    }
    return res;
}

double poly_derivative_eval(int deg, const double c[], double x) {
    if (deg == 0) return 0.0;
    double res = deg * c[deg];
    for (int i = deg - 1; i >= 1; i--) {
        res = res * x + i * c[i];
    }
    return res;
}

bool bisect_poly_root(int deg, const double c[], double l, double r, double &root) {
    double fl = poly_eval(deg, c, l);
    double fr = poly_eval(deg, c, r);
    if (fabs(fl) < EPS) {
        root = l;
        return true;
    }
    if (fabs(fr) < EPS) {
        root = r;
        return true;
    }
    if (fl * fr > 0) return false;

    for (int it = 1; it <= 100; it++) {
        double mid = (l + r) / 2.0;
        double fm = poly_eval(deg, c, mid);
        if (fabs(fm) < EPS) {
            root = mid;
            return true;
        }
        if (fl * fm <= 0) {
            r = mid;
            fr = fm;
        } else {
            l = mid;
            fl = fm;
        }
        (void)fr;
    }
    root = (l + r) / 2.0;
    return true;
}

bool newton_poly_root(int deg, const double c[], double start, double &root) {
    double x = start;
    for (int it = 1; it <= 60; it++) {
        double fx = poly_eval(deg, c, x);
        double dfx = poly_derivative_eval(deg, c, x);
        if (!isfinite(fx) || !isfinite(dfx) || fabs(dfx) < EPS) return false;
        double nx = x - fx / dfx;
        if (!isfinite(nx)) return false;
        if (fabs(nx - x) < 1e-12) {
            root = nx;
            return fabs(poly_eval(deg, c, root)) < 1e-7;
        }
        x = nx;
    }
    root = x;
    return fabs(poly_eval(deg, c, root)) < 1e-7;
}

int solve_quadratic_formula(double a, double b, double c, double roots[]) {
    if (fabs(a) < EPS) {
        if (fabs(b) < EPS) {
            return fabs(c) < EPS ? -1 : 0;
        }
        roots[1] = -c / b;
        return 1;
    }

    double delta = b * b - 4.0 * a * c;
    if (delta < -EPS) return 0;
    if (fabs(delta) <= EPS) {
        roots[1] = -b / (2.0 * a);
        return 1;
    }

    double sqrt_delta = sqrt(max(0.0, delta));
    double q = -0.5 * (b + (b >= 0 ? sqrt_delta : -sqrt_delta));
    if (fabs(q) < EPS) {
        roots[1] = (-b - sqrt_delta) / (2.0 * a);
        roots[2] = (-b + sqrt_delta) / (2.0 * a);
    } else {
        roots[1] = q / a;
        roots[2] = c / q;
    }
    if (roots[1] > roots[2]) swap(roots[1], roots[2]);
    return 2;
}

void print_real_solution(const string &tag, int n) {
    cout << tag << '\n';
    if (tag == "NO") return;
    for (int i = 1; i <= n; i++) {
        if (i > 1) cout << ' ';
        double x = fabs(ans_real[i]) < 5e-13 ? 0.0 : ans_real[i];
        cout << x;
    }
    cout << '\n';
}

void print_mod_solution(const string &tag, int n) {
    cout << tag << '\n';
    if (tag == "NO") return;
    for (int i = 1; i <= n; i++) {
        if (i > 1) cout << ' ';
        cout << ans_mod[i];
    }
    cout << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cout.setf(ios::fixed);
    cout << setprecision(10);

    string op;
    if (!(cin >> op)) return 0;

    if (op == "real") {
        int m, n;
        cin >> m >> n;
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n + 1; j++) cin >> mat_real[i][j];
        }
        int status = gauss_real(m, n);
        if (status == 0) print_real_solution("NO", n);
        else if (status == 1) print_real_solution("UNIQUE", n);
        else print_real_solution("MANY", n);
    } else if (op == "mod") {
        int m, n;
        ll mod;
        cin >> m >> n >> mod;
        if (mod <= 1) {
            cout << "BAD_MOD\n";
            return 0;
        }
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n + 1; j++) {
                cin >> mat_mod[i][j];
                mat_mod[i][j] = norm_mod(mat_mod[i][j], mod);
            }
        }
        int status = gauss_mod_prime(m, n, mod);
        if (status == 0) print_mod_solution("NO", n);
        else if (status == 1) print_mod_solution("UNIQUE", n);
        else print_mod_solution("MANY", n);
    } else if (op == "congruence") {
        ll a, b, mod, x0, step;
        cin >> a >> b >> mod;
        if (!solve_linear_congruence(a, b, mod, x0, step)) {
            cout << "NO\n";
        } else {
            cout << x0 << ' ' << step << '\n';
        }
    } else if (op == "eval") {
        int deg;
        double x;
        cin >> deg;
        for (int i = 0; i <= deg; i++) cin >> coef_poly[i];
        cin >> x;
        cout << poly_eval(deg, coef_poly, x) << '\n';
    } else if (op == "bisect") {
        int deg;
        double l, r, root;
        cin >> deg;
        for (int i = 0; i <= deg; i++) cin >> coef_poly[i];
        cin >> l >> r;
        if (bisect_poly_root(deg, coef_poly, l, r, root)) {
            cout << root << ' ' << poly_eval(deg, coef_poly, root) << '\n';
        } else {
            cout << "NO_BRACKET\n";
        }
    } else if (op == "newton") {
        int deg;
        double start, root;
        cin >> deg;
        for (int i = 0; i <= deg; i++) cin >> coef_poly[i];
        cin >> start;
        if (newton_poly_root(deg, coef_poly, start, root)) {
            cout << root << ' ' << poly_eval(deg, coef_poly, root) << '\n';
        } else {
            cout << "FAIL\n";
        }
    } else if (op == "quad") {
        double a, b, c;
        double roots[3] = {0, 0, 0};
        cin >> a >> b >> c;
        int cnt = solve_quadratic_formula(a, b, c, roots);
        if (cnt < 0) {
            cout << "INF\n";
        } else {
            cout << cnt << '\n';
            for (int i = 1; i <= cnt; i++) {
                double x = fabs(roots[i]) < 5e-13 ? 0.0 : roots[i];
                cout << x << '\n';
            }
        }
    }

    return 0;
}
```

调用示例：

```cpp
// 2x + y = 5
// x - y = 1
// 高斯后得到 x=2, y=1。
int m = 2, n = 2;
mat_real[1][1] = 2; mat_real[1][2] = 1;  mat_real[1][3] = 5;
mat_real[2][1] = 1; mat_real[2][2] = -1; mat_real[2][3] = 1;
int status = gauss_real(m, n);
if (status == 1) {
    cout << ans_real[1] << ' ' << ans_real[2] << '\n';
}

// 多项式 1 - 3x + 2x^2 在 x=3 的值。
double c[3];
c[0] = 1;
c[1] = -3;
c[2] = 2;
cout << poly_eval(2, c, 3) << '\n'; // 10
```

## 二分和牛顿怎么选

二分是“慢但稳”：

- 必须能保证根在区间里。
- 最常见保证是 `f(l)` 与 `f(r)` 异号。
- 如果函数单调，也可以二分找 `f(x) >= 0` 的边界。

牛顿是“快但挑初值”：

```text
x_{k+1} = x_k - f(x_k) / f'(x_k)
```

- 初值离根太远可能发散。
- 导数接近 0 时要停。
- 考场建议：能二分先二分；牛顿只在题目明确或需要加速时用。

## 多项式求根的低心智路线

```text
一次：a*x+b=0，直接 -b/a。
二次：a*x^2+b*x+c=0，判别式 delta=b^2-4ac。
三次及以上：如果只求某个区间一个根，用二分/牛顿；不要临场硬抄三次公式。
```

如果题目要求“所有实根”：

- 二次公式可以全部输出。
- 高次多项式需要导数分段、Sturm、或题面给出特殊性质；普通 SIM 模板不强行覆盖。
- 只给误差要求且区间小，可以按题意扫描小区间，再对异号段二分，但偶重根可能不会异号。

常见坑：

- 高斯消元一定要先判无解，再判多解。
- 实数高斯主元要选绝对值最大行，别直接拿当前行。
- `EPS` 不是越小越好；普通 `double` 用 `1e-9` 到 `1e-12`。
- 多解时自由变量可以先置 0，但题目如果要求参数形式，要单独输出自由变量。
- 模高斯这里默认 `mod` 是质数；复合模下非零数不一定有逆元。
- 读入负数系数后要 `((x % mod) + mod) % mod`。
- `a*x ≡ b (mod m)` 有解条件是 `gcd(a,m) | b`。
- 二分根要求连续函数；离散答案二分和连续二分不是同一件事。
- 区间两端同号不代表没有根，例如 `(x-1)^2=0`。
- 牛顿法要防导数为 0、结果变成 `nan/inf`。
- Horner 系数顺序必须统一，本模板用低次到高次：`c[0], c[1], ..., c[deg]`。
- 二次公式里 `delta` 接近 0 时按一个根处理，避免输出两个几乎相同的根。
- 输出浮点答案记得 `fixed << setprecision(...)`。

暴力/部分分替代：

- 未知数 `n <= 3` 且整数范围小：枚举所有变量检查方程。
- 实数方程组只要求小数据：可以用 Cramer's rule 解 `2x2/3x3`，但高斯更通用。
- 模方程变量很少且模数小：直接枚举 `0..mod-1`。
- 一元方程区间很短且答案是整数：枚举整数点。
- 多项式次数低：优先一次/二次公式。
- Newton 不稳时，退回二分。

升级方向：

```text
整数小范围枚举 -> 实数/模高斯
单条同余 -> exgcd
模质数方程组 -> 模高斯
连续一元方程 -> 二分
二分太慢且导数好算 -> 牛顿
二次以内 -> 公式
高次所有根 -> 导数分段 / Sturm / 专题数学
```

最小测试样例：

```text
输入
real
2 2
2 1 5
1 -1 1

输出
UNIQUE
2.0000000000 1.0000000000
```

补充自测 1：

```text
输入
mod
2 2 1000000007
2 1 5
1 -1 1

输出
UNIQUE
2 1
```

补充自测 2：

```text
输入
congruence
14 30 100

输出
45 50
```

补充自测 3：

```text
输入
eval
2
1 -3 2
3

输出
10.0000000000
```

补充自测 4：

```text
输入
bisect
2
-2 0 1
0 2

输出示例
1.4142135624 0.0000000000
```

补充自测 5：

```text
输入
quad
1 -3 2

输出
2
1.0000000000
2.0000000000
```
