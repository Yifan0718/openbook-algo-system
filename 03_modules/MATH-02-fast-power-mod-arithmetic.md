# MATH-02 快速幂与模运算

模块编号：MATH-02

模块名称：快速幂、取模规范与乘法防溢出

标签：[数学][快速幂][模运算][二进制拆分]

一句话用途：在 `O(log b)` 内计算 `a^b`，并把所有加减乘幂统一到安全的取模写法。

题面触发词：

- 答案对 `1e9+7` / `998244353` 取模。
- 求 `a^b mod p`。
- 指数很大、幂次、翻倍、二进制拆分。
- 方案数很大，请输出取模结果。
- 乘法可能溢出。

什么时候用：

- 指数 `b` 可达 `1e9/1e18`，不能循环乘。
- 计数题要求取模。
- 矩阵快速幂、组合数、逆元都要调用快速幂。
- 中间乘法可能超过 `long long`，需要 `__int128` 辅助。

不要什么时候用：

- 指数很小且只算一次时，普通循环也可拿部分分。
- 需要浮点幂时用 `pow`，但竞赛整数取模不要用浮点 `pow`。
- 模数为 1 时所有结果都是 0，要提前处理。

复杂度：

- 快速幂：`O(log b)`。
- 单次加减乘取模：`O(1)`。

数据范围参考：

- `b <= 1e18`：`long long` 指数可用。
- `a, mod <= 1e18` 且乘法会溢出：使用 `mul_mod` 的 `__int128` 版本。

依赖的标准容器：

- 不依赖特殊容器。
- 常量 `MOD` 推荐用 `long long`。

输入如何整理：

```cpp
ll a, b, mod;
cin >> a >> b >> mod;
```

接口：

```text
norm(x, mod) -> 把 x 规范到 [0, mod-1]
add_mod(a,b,mod) -> (a+b)%mod
sub_mod(a,b,mod) -> (a-b)%mod
mul_mod(a,b,mod) -> (a*b)%mod，防溢出版
pow_mod(a,b,mod) -> a^b % mod
```

输出能力：

- 整数幂取模。
- 安全加减乘取模。
- 作为逆元、组合数、矩阵快速幂的底层函数。

下游可接：

- MATH-03 逆元与组合数。
- MATH-05 矩阵快速幂。
- DP 方案数取模。

可拼接模块：

- 计数 DP + `add_mod`。
- 组合数预处理 + `pow_mod`。
- Rolling Hash 预处理幂数组。

模数是否为质数的分支：

```text
只算 a^b % mod：mod 是否为质数都可以。
用 pow_mod(a, mod-2, mod) 求逆元：只有 mod 是质数且 a % mod != 0 才能这样做。
mod 不是质数：不要套费马逆元；除法要改用扩展 gcd 逆元并检查互质。
```

模板代码：

```cpp
using ll = long long;

ll norm(ll x, ll mod) {
    assert(mod > 0);
    x %= mod;
    if (x < 0) x += mod;
    return x;
}

ll add_mod(ll a, ll b, ll mod) {
    assert(mod > 0);
    return (ll)(((__int128)norm(a, mod) + norm(b, mod)) % mod);
}

ll sub_mod(ll a, ll b, ll mod) {
    assert(mod > 0);
    return (ll)(((__int128)norm(a, mod) - norm(b, mod) + mod) % mod);
}

ll mul_mod(ll a, ll b, ll mod) {
    assert(mod > 0);
    return (ll)((__int128)norm(a, mod) * norm(b, mod) % mod);
}

ll pow_mod(ll a, ll b, ll mod) {
    assert(mod > 0);
    assert(b >= 0);
    if (mod == 1) return 0;
    a = norm(a, mod);
    ll res = 1 % mod;
    while (b > 0) {
        if (b & 1) res = mul_mod(res, a, mod);
        a = mul_mod(a, a, mod);
        b >>= 1;
    }
    return res;
}
```

调用示例：

```cpp
const ll MOD = 1000000007LL;
cout << pow_mod(2, 10, MOD) << "\n"; // 1024

ll ans = 0;
ans = add_mod(ans, ways, MOD);
ans = sub_mod(ans, bad, MOD);
```

常见坑：

- `(a - b) % mod` 在 C++ 里可能是负数，要加 `mod`。
- `1e9+7` 是 double 字面量风险，写 `1000000007LL`。
- `pow(a,b)` 返回浮点，不能拿来做整数取模。
- `mod == 1` 时 `1 % mod` 是 0，快速幂也应返回 0。
- `long long` 乘 `long long` 可能先溢出，再取模已经晚了。

暴力/部分分替代：

- `b <= 1e6` 可循环乘 `b` 次。
- 方案数小数据可先不取模，用 `long long` 暂存并观察是否溢出。
- 乘法不大时可先用 `(a % mod) * (b % mod) % mod`。

升级方向：

- 多次幂同底或同模 -> 预处理幂数组。
- 线性递推第 `n` 项 -> 矩阵快速幂。
- 需要除法 -> 逆元模块。

最小测试样例：

```text
pow_mod(2, 10, 1000000007) = 1024
sub_mod(3, 5, 7) = 5
mul_mod(1000000000000000000, 2, 1000000007) = 98
pow_mod(5, 3, 1) = 0
```
