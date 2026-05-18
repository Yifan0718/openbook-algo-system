# MATH-03 逆元与组合数预处理

模块编号：MATH-03

模块名称：模逆元、阶乘逆元与组合数 `C(n,k)`

标签：[数学][逆元][组合数][阶乘][计数]

一句话用途：把模意义下的除法变成乘法，并在 `O(1)` 查询大量组合数。

题面触发词：

- 组合数、从 `n` 个选 `k` 个。
- 排列组合、方案数取模。
- 需要除以某个数后取模。
- `n,q <= 2e5/1e6` 且多次询问 `C(n,k)`。
- 模数给出为 `1e9+7`、`998244353`。

什么时候用：

- 需要计算 `a / b mod MOD`。
- 大量查询 `C(n,k) mod MOD`。
- 计数 DP 里转移含组合数。
- 排列、路径条数、二项式展开。

不要什么时候用：

- 模数不是质数时，不要直接用 `pow_mod(x, mod-2, mod)`。
- `k > n` 时组合数应为 0。
- `n` 极大但查询很少时，不一定能预处理到 `n`，要考虑 Lucas 或乘法公式。

复杂度：

- 单次费马逆元：`O(log mod)`。
- 阶乘预处理：`O(N)`。
- 查询 `C(n,k)`：`O(1)`。
- 扩展 gcd 逆元：`O(log mod)`。

数据范围参考：

- `N <= 2e6`：阶乘和逆阶乘数组常用。
- `N > 1e7`：注意内存和预处理时间。
- `mod` 不是质数：只能对与 `mod` 互质的数求逆元。

依赖的标准容器：

- 1-index 或 0-index 阶乘数组都可；本模板 `fac[0..N]` 是数学自然下标。
- 使用 `vector<ll> fac, ifac`。

输入如何整理：

```cpp
int maxN, q;
ll MOD;
cin >> maxN >> q >> MOD;
Comb comb;
comb.init(maxN, MOD, true); // true 表示确认 MOD 是质数
```

接口：

```text
inv_prime(a, mod) -> 质数模数下的逆元
inv_coprime(a, mod) -> 非质数模数下，a 与 mod 互质时的逆元
Comb.init(N, mod, mod_is_prime)
Comb.C(n,k)
Comb.P(n,k)
```

输出能力：

- 模意义下除法。
- 组合数 `C(n,k)`。
- 排列数 `P(n,k)`。
- 多次查询的快速答案。

下游可接：

- 计数 DP。
- 容斥。
- 组合计数题。
- 概率题的分数取模。

可拼接模块：

- MATH-02 快速幂。
- MATH-06 容斥基础。
- DP 方案数。

模数是否为质数的分支：

```text
mod 是质数：
  inv(a) = pow_mod(a, mod-2, mod)，要求 a % mod != 0。
  fac/ifac 预处理可 O(N)，C(n,k)=fac[n]*ifac[k]*ifac[n-k]。

mod 不是质数：
  不能用 pow_mod(a, mod-2, mod)。
  只有 gcd(a, mod) == 1 时才有逆元，用 exgcd。
  普通 fac/ifac 组合数可能失效，因为 fac 里含有与 mod 不互质的因子。
  考场弱基础策略：优先找题面是否保证 mod 是质数；没保证时用小数据 Pascal 递推或整数约分法拿部分分。
```

模板代码：

```cpp
using ll = long long;

ll norm(ll x, ll mod) {
    x %= mod;
    if (x < 0) x += mod;
    return x;
}

ll mul_mod(ll a, ll b, ll mod) {
    return (ll)((__int128)norm(a, mod) * norm(b, mod) % mod);
}

ll pow_mod(ll a, ll b, ll mod) {
    assert(b >= 0);
    ll res = 1 % mod;
    a = norm(a, mod);
    while (b > 0) {
        if (b & 1) res = mul_mod(res, a, mod);
        a = mul_mod(a, a, mod);
        b >>= 1;
    }
    return res;
}

ll exgcd(ll a, ll b, ll &x, ll &y) {
    if (b == 0) {
        x = (a >= 0 ? 1 : -1);
        y = 0;
        return a >= 0 ? a : -a;
    }
    ll x1, y1;
    ll g = exgcd(b, a % b, x1, y1);
    x = y1;
    __int128 yy = (__int128)x1 - (__int128)(a / b) * y1;
    assert((__int128)LLONG_MIN <= yy && yy <= (__int128)LLONG_MAX);
    y = (ll)yy;
    return g;
}

ll inv_prime(ll a, ll mod) {
    assert(mod > 1);
    a = norm(a, mod);
    if (a == 0) return -1; // 不存在逆元
    return pow_mod(a, mod - 2, mod);
}

ll inv_coprime(ll a, ll mod) {
    ll x, y;
    ll g = exgcd(a, mod, x, y);
    if (g != 1) return -1; // 不存在逆元
    return norm(x, mod);
}

struct Comb {
    int N;
    ll mod;
    vector<ll> fac, ifac;

    void init(int n, ll mod_, bool mod_is_prime) {
        N = n;
        mod = mod_;
        if (!mod_is_prime || N >= mod) {
            // 阶乘逆元法只适用于质数模且 N < mod；非质数模请用 Pascal/扩展组合数。
            N = 0;
            fac.assign(1, 1);
            ifac.assign(1, 1);
            return;
        }
        fac.assign(N + 1, 1);
        ifac.assign(N + 1, 1);
        for (int i = 1; i <= N; i++) fac[i] = mul_mod(fac[i - 1], i, mod);

        ifac[N] = inv_prime(fac[N], mod);

        for (int i = N; i >= 1; i--) ifac[i - 1] = mul_mod(ifac[i], i, mod);
    }

    ll C(int n, int k) {
        if (k < 0 || k > n || n > N) return 0;
        return mul_mod(fac[n], mul_mod(ifac[k], ifac[n - k], mod), mod);
    }

    ll P(int n, int k) {
        if (k < 0 || k > n || n > N) return 0;
        return mul_mod(fac[n], ifac[n - k], mod);
    }
};
```

调用示例：

```cpp
const ll MOD = 1000000007LL;
Comb comb;
comb.init(1000000, MOD, true);
cout << comb.C(5, 2) << "\n"; // 10

ll inv2 = inv_prime(2, MOD);
ll half = mul_mod(x, inv2, MOD);
```

常见坑：

- `mod` 不是质数却套费马逆元，是最常见错误。
- `a % mod == 0` 没有逆元；本模板的 `inv_prime` 会返回 `-1`。
- `C(n,k)` 中 `k<0` 或 `k>n` 要返回 0。
- 多测时 `init` 要按最大 `N` 重新建或一次建到全局最大。
- `fac[N]` 在非质数模数下可能不可逆，`ifac` 会失效。
- 阶乘逆元法要求 `mod` 是质数且 `N < mod`；不满足时改 Pascal、Lucas 或扩展组合数。

暴力/部分分替代：

- `n <= 2000`：Pascal 递推 `C[i][j]=C[i-1][j-1]+C[i-1][j]`，不需要逆元，非质数模数也能用。
- 查询很少且 `k` 小：用乘法公式逐项约分，或逐项乘后除的整数版。
- 不确定模数是否质数：先写 Pascal 小范围版本拿部分分。

升级方向：

- `n` 很大、`mod` 是小质数 -> Lucas。
- `mod` 不是质数且 `n` 大 -> 分解模数/CRT，难度高，低优先级。
- 组合数参与容斥 -> 接 MATH-06。

最小测试样例：

```text
MOD = 1000000007
inv_prime(2, MOD) = 500000004
C(5,2) = 10
P(5,2) = 20

MOD = 8
inv_coprime(3, 8) = 3
inv_coprime(2, 8) = -1
```
