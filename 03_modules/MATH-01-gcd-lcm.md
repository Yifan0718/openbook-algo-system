# MATH-01 gcd / lcm

模块编号：MATH-01

模块名称：最大公约数与最小公倍数

标签：[数学][数论][gcd][lcm]

一句话用途：快速处理整除、约分、周期同步、比例化简和两个数的公共因子问题。

题面触发词：

- 最大公约数、最小公倍数。
- 互质、约分、最简分数。
- 周期同时发生、两个循环何时重合。
- 能否整除、公共因子、最大公共长度。
- 把若干数按比例化简。

什么时候用：

- 题目明显问 `gcd(a,b)`、`lcm(a,b)`。
- 需要判断 `gcd(a,b)==1`。
- 需要把分数 `x/y` 约成最简。
- 周期题中要求两个周期第一次同时出现，常用 `lcm`。

不要什么时候用：

- 需要所有因子列表时，只求 gcd 不够，要枚举因子或质因数分解。
- `lcm` 可能超过 `long long` 时不能直接乘。
- 浮点数比例不要直接 gcd，先转成整数或避免浮点。

复杂度：

- `gcd(a,b)`：`O(log min(a,b))`。
- 多个数的 gcd/lcm：每加入一个数做一次 gcd。

数据范围参考：

- `a,b <= 1e18`：`long long` 可存，`lcm` 乘法要防溢出。
- `n <= 2e5`：顺序合并 gcd/lcm 可用。

依赖的标准容器：

- 不依赖特殊容器。
- 多个数时使用 1-index 数组 `vector<ll> a(n + 1)`。

输入如何整理：

```cpp
int n;
cin >> n;
vector<ll> a(n + 1);
for (int i = 1; i <= n; i++) cin >> a[i];
```

接口：

```text
gcd_ll(a,b) -> 最大公约数
lcm_ll(a,b) -> 最小公倍数，普通版
lcm_limit(a,b,limit) -> 超过 limit 时返回 limit + 1；若 limit 已经是 LLONG_MAX，则返回 limit
```

输出能力：

- 两数或多数组合的最大公约数。
- 两数或多数组合的最小公倍数。
- 互质判断。
- 分数约分。

下游可接：

- 逆元和模运算里的互质判断。
- 中国剩余类问题的前置检查。
- 周期 DP、模拟题、字符串周期题。

可拼接模块：

- MATH-02 模运算。
- MATH-03 逆元。
- MATH-04 质因数分解。
- STR-02 KMP/Z 函数求字符串周期后接 `gcd/lcm`。

模数是否为质数的分支：

```text
本模块本身不依赖模数。
如果后续要在 mod 下做除法：
  mod 是质数 -> 可接费马逆元。
  mod 不是质数 -> 必须检查 gcd(x, mod) == 1，再用扩展 gcd 求逆元。
```

模板代码：

```cpp
using ll = long long;

ll gcd_ll(ll a, ll b) {
    if (a == LLONG_MIN || b == LLONG_MIN) {
        // 极端数据兜底；普通竞赛题很少卡 LLONG_MIN。
        unsigned long long x = a < 0 ? 0ULL - (unsigned long long)a : (unsigned long long)a;
        unsigned long long y = b < 0 ? 0ULL - (unsigned long long)b : (unsigned long long)b;
        while (y) {
            unsigned long long t = x % y;
            x = y;
            y = t;
        }
        return (ll)x;
    }
    if (a < 0) a = -a;
    if (b < 0) b = -b;
    while (b) {
        ll t = a % b;
        a = b;
        b = t;
    }
    return a;
}

ll lcm_ll(ll a, ll b) {
    if (a == 0 || b == 0) return 0;
    ll g = gcd_ll(a, b);
    __int128 x = (__int128)a / g * b;
    if (x < 0) x = -x;
    assert(x <= LLONG_MAX); // 若可能超过 long long，改用 lcm_limit。
    return (ll)x;
}

ll lcm_limit(ll a, ll b, ll limit) {
    if (a == 0 || b == 0) return 0;
    __int128 aa = a, bb = b;
    if (aa < 0) aa = -aa;
    if (bb < 0) bb = -bb;
    ll g = gcd_ll(a, b);
    aa /= g;
    __int128 lim = limit;
    ll over = (limit == LLONG_MAX ? limit : limit + 1);
    if (bb != 0 && aa > lim / bb) return over;
    __int128 res = aa * bb;
    if (res > lim) return over;
    return (ll)res;
}
```

调用示例：

```cpp
ll g = 0;
for (int i = 1; i <= n; i++) g = gcd_ll(g, a[i]);

ll l = 1;
for (int i = 1; i <= n; i++) {
    l = lcm_limit(l, a[i], 4'000'000'000'000'000'000LL);
}

if (gcd_ll(x, y) == 1) {
    // x 和 y 互质
}
```

常见坑：

- `lcm = a * b / gcd(a,b)` 容易先乘溢出，写成 `a / gcd * b`。
- `gcd(0,x)=abs(x)`，多数组合时初始值可设为 `0`。
- 负数取 gcd 时先转正；如果题目可能出现 `LLONG_MIN`，用本页安全版，不要直接 `a=-a`。
- C++17 有 `std::gcd`，但纸质模板自己写更可控。
- `lcm_ll` 只在结果保证不超过 `long long` 时使用；可能爆时用 `lcm_limit`。

暴力/部分分替代：

- 小数据可以从 `min(a,b)` 往下枚举第一个同时整除的数求 gcd。
- 小数据可以从 `max(a,b)` 往上枚举第一个同时被整除的数求 lcm。
- 周期题不会推公式时，可先模拟到 `lcm_limit` 的上限拿部分分。

升级方向：

- 多次区间 gcd 查询 -> Sparse Table 或 Segment Tree。
- 需要因子个数/因子和 -> 质因数分解。
- 模意义下除法 -> 逆元。

最小测试样例：

```text
gcd_ll(12, 18) = 6
lcm_ll(12, 18) = 36
gcd_ll(0, 5) = 5
lcm_limit(1000000000000, 1000000000000, 1000000000000) = 1000000000000
```
