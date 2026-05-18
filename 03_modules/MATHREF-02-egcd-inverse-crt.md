# MATHREF-02 扩展欧几里得、逆元与 CRT

本文件定位：解决“模意义下除法”和“多个同余条件合并”。竞赛里看到除法先问模数是否为质数。

调用示例：先判断模数是否质数；质数模可用快速幂逆元，非质数模优先用 `exgcd`/CRT 小节。

最小测试样例：`exgcd(30,18)`、`inv_mod(3,11)`、`x=2 mod 3, x=3 mod 5` 都应能手算核对。

模块编号：MATHREF-02

模块名称：扩展欧几里得、逆元与 CRT 参考

什么时候用：题目要求模意义下除法、线性同余方程、`ax+by=c`、多个余数条件合并。

不要什么时候用：模数明确是质数且只是普通组合数，可优先用 MATH-03 的费马逆元和阶乘逆元；没有取模除法时不要硬套。

复杂度：扩展欧几里得 `O(log min(a,b))`；CRT 合并每个方程一次 `O(k log M)`。

依赖的标准容器：`long long`；多方程 CRT 可用 `vector<pair<ll,ll>>` 存 `(remainder, mod)`。

接口：`exgcd(a,b,x,y)`、`mod_inverse(a,mod)`、线性同余求解、CRT 合并。

## 1. 扩展欧几里得与线性同余方程

题面触发词：

- 求整数解 `ax + by = c`。
- 求 `a*x ≡ b (mod m)`。
- 模数不一定是质数。
- 同余方程、最小非负解。

使用条件：

- `a,b,c,m` 是整数。
- 解线性方程前先算 `g = gcd(a,b)` 或 `gcd(a,m)`。
- `a*x ≡ b (mod m)` 有解当且仅当 `gcd(a,m) | b`。

公式/结论：

```text
exgcd(a,b) 求 x,y，使 ax + by = gcd(a,b)。

ax + by = c:
  设 g=gcd(a,b)，若 c % g != 0，无整数解。
  否则 exgcd 得到 x0,y0 后，乘 c/g 得一组解。

a*x ≡ b (mod m):
  等价于 a*x + m*y = b。
  g=gcd(a,m)，若 b%g!=0，无解。
  化成 (a/g)*x ≡ (b/g) (mod m/g)。
```

C++17模板或计算方式：

```cpp
using ll = long long;

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

ll norm(ll x, ll mod) {
    assert(mod > 0);
    x %= mod;
    if (x < 0) x += mod;
    return x;
}

// 返回 a*x ≡ b (mod m) 的一个最小非负解；无解返回 -1
ll solve_linear_congruence(ll a, ll b, ll m) {
    assert(m > 0);
    ll x, y;
    ll g = exgcd(a, m, x, y);
    if (b % g != 0) return -1;
    ll mod2 = m / g;
    return norm((__int128)x * (b / g) % mod2, mod2);
}
```

常见坑：

- `exgcd` 返回的一组解不是唯一解。
- `a*x ≡ b (mod m)` 的解模数是 `m/g`。
- `a` 或 `b` 为负时，`exgcd` 模板仍返回正 gcd，最后用 `norm` 规范答案。
- 乘 `x*(b/g)` 可能溢出，使用 `__int128`。

暴力/部分分替代：

- `m <= 1e6` 时枚举 `x=0..m-1`。
- 只判断是否有解时，只需检查 `b % gcd(a,m) == 0`。

最小验错：

```text
14*x ≡ 30 (mod 100)
gcd(14,100)=2，30%2=0，有解
化简为 7*x ≡ 15 (mod 50)
一个解 x=45，因为 14*45=630，630%100=30
```

## 2. 模逆元

题面触发词：

- 模意义下除法。
- 求 `a^{-1} mod m`。
- 组合数预处理里的逆元。
- 概率分数取模。

使用条件：

- `a` 在模 `m` 下有逆元当且仅当 `gcd(a,m)=1`。
- 若 `m` 是质数且 `a % m != 0`，可用费马小定理。
- 若 `m` 不是质数，用扩展欧几里得。

公式/结论：

```text
a * inv(a) ≡ 1 (mod m)

m 是质数：
  inv(a) = a^(m-2) mod m

m 不一定是质数：
  用 exgcd 解 ax + my = 1，x 即逆元。
```

C++17模板或计算方式：

```cpp
using ll = long long;

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

ll norm(ll x, ll mod) {
    assert(mod > 0);
    x %= mod;
    if (x < 0) x += mod;
    return x;
}

ll mul_mod(ll a, ll b, ll mod) {
    assert(mod > 0);
    a %= mod;
    b %= mod;
    if (a < 0) a += mod;
    if (b < 0) b += mod;
    return (ll)((__int128)a * b % mod);
}

ll pow_mod(ll a, ll e, ll mod) {
    assert(mod > 0);
    assert(e >= 0);
    ll res = 1 % mod;
    a %= mod;
    if (a < 0) a += mod;
    while (e > 0) {
        if (e & 1) res = mul_mod(res, a, mod);
        a = mul_mod(a, a, mod);
        e >>= 1;
    }
    return res;
}

ll inv_prime(ll a, ll mod) {
    assert(mod > 1);
    a = norm(a, mod);
    if (a == 0) return -1; // 不存在逆元
    return pow_mod(a, mod - 2, mod);
}

ll inv_exgcd(ll a, ll mod) {
    assert(mod > 0);
    ll x, y;
    ll g = exgcd(a, mod, x, y);
    if (g != 1) return -1;
    return norm(x, mod);
}
```

常见坑：

- `mod` 不保证质数时不能用 `a^(mod-2)`。
- `a % mod == 0` 没有逆元；本模板的 `inv_prime` 会返回 `-1`。
- 分数取模不是普通整数除法。
- 组合数阶乘逆元在非质数模数下可能整体失效。

暴力/部分分替代：

- `mod <= 1e6` 时枚举 `x` 找 `a*x % mod == 1`。
- 小范围组合数用 Pascal 递推，不用逆元。

最小验错：

```text
mod=7，inv(3)=5，因为 3*5%7=1
mod=8，inv(3)=3，因为 3*3%8=1
mod=8，inv(2) 不存在，因为 gcd(2,8)=2
```

## 3. CRT 与扩展 CRT

题面触发词：

- 同时满足多个余数条件。
- `x ≡ a_i (mod m_i)`。
- 多个周期同时对齐。
- 模数两两互质/不一定互质。

使用条件：

- CRT 标准版要求模数两两互质。
- 扩展 CRT 不要求互质，但每次合并要检查是否兼容。
- 结果通常输出最小非负解。

公式/结论：

```text
两个方程：
x ≡ r1 (mod m1)
x ≡ r2 (mod m2)

令 x = r1 + m1*k
代入第二个：
m1*k ≡ r2-r1 (mod m2)

有解条件：
gcd(m1,m2) | (r2-r1)

新模数：
lcm(m1,m2) = m1/g*m2
```

C++17模板或计算方式：

```cpp
using ll = long long;

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

ll norm(ll x, ll mod) {
    assert(mod > 0);
    x %= mod;
    if (x < 0) x += mod;
    return x;
}

bool merge_crt(ll &r1, ll &m1, ll r2, ll m2) {
    // 当前 x ≡ r1 (mod m1)，合并 x ≡ r2 (mod m2)
    assert(m1 > 0 && m2 > 0);
    ll x, y;
    ll g = exgcd(m1, m2, x, y);
    __int128 diff = (__int128)r2 - r1;
    if (diff % g != 0) return false;

    ll mod2 = m2 / g;
    __int128 left = (diff / g) % mod2;
    if (left < 0) left += mod2;
    ll k = (ll)(left * norm(x, mod2) % mod2);

    __int128 nr = (__int128)r1 + (__int128)m1 * k;
    __int128 nm = (__int128)m1 / g * m2;
    if (nm <= 0 || nm > LLONG_MAX) return false; // 本模板只返回 long long 范围内的合并模数
    r1 = (ll)(nr % nm);
    if (r1 < 0) r1 += (ll)nm;
    m1 = (ll)nm;
    return true;
}

// 方程编号 1..k：x ≡ r[i] (mod m[i])
// 返回 {是否有解, 最小非负解}
pair<bool, ll> excrt(ll r[], ll m[], int k) {
    if (k <= 0) return {false, -1};
    for (int i = 1; i <= k; i++) {
        if (m[i] <= 0) return {false, -1};
    }
    ll ans = r[1], mod = m[1];
    ans = norm(ans, mod);
    for (int i = 2; i <= k; i++) {
        if (!merge_crt(ans, mod, norm(r[i], m[i]), m[i])) {
            return {false, -1};
        }
    }
    return {true, ans};
}
```

常见坑：

- 模数不互质时，普通 CRT 公式可能错，必须用扩展 CRT。
- 兼容条件是 `(r2-r1) % gcd(m1,m2) == 0`。
- 新模数是 lcm，可能溢出。
- 余数先规范到 `[0,m-1]`。

暴力/部分分替代：

- 模数乘积小：从 `x=r1` 开始每次加 `m1` 枚举。
- 条件少且上界小：直接枚举 `x=0..limit` 检查所有同余。

最小验错：

```text
x ≡ 2 (mod 3)
x ≡ 3 (mod 5)
最小非负解 x=8

x ≡ 1 (mod 2)
x ≡ 0 (mod 4)
无解，因为 gcd(2,4)=2 不能整除 -1
```
