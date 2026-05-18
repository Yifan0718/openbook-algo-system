# MATHREF-01 整除、同余与 gcd/lcm

本文件定位：竞赛数学知识查阅，不只是代码模板。看到题面后先判断“是否是整数关系/模关系/周期关系”。

调用示例：先按题面关键词定位到本文件的小节，再把对应 `C++17模板或计算方式` 抄入主程序验证。

最小测试样例：每个公式先用 2 到 3 个手算小数值自测，例如模数为 5、余数为 0/1/4 的边界。

模块编号：MATHREF-01

模块名称：整除、同余与 gcd/lcm 参考

什么时候用：题目出现整除、余数、周期、取模、最大公约数、最小公倍数、互质等整数关系。

不要什么时候用：题目核心是组合数预处理、图论或 DP 时，本文件只提供数学判断和公式，不替代对应模板。

复杂度：公式查阅本身 `O(1)`；`gcd` 为 `O(log min(a,b))`；枚举因子通常到 `sqrt(n)`。

依赖的标准容器：通常只需 `long long`；批量统计时可接 `vector<int>` 或筛法模块。

接口：`std::gcd(a,b)`、安全 `lcm`、同余判断、取模规范化。

## 1. 整除与同余

题面触发词：

- 整除、余数、取模、模 `m` 意义下相等。
- 周期、循环、每隔 `k` 次。
- 判断 `a` 和 `b` 除以 `m` 的余数是否相同。
- 输出答案对某个数取模。

使用条件：

- 所有量都是整数。
- 同余只关心余数，不关心原数大小。
- 模数 `m > 0`。

公式/结论：

```text
a ≡ b (mod m)  <=>  m | (a-b)
(a+b) mod m = ((a mod m) + (b mod m)) mod m
(a-b) mod m = ((a mod m) - (b mod m) + m) mod m
(a*b) mod m = ((a mod m) * (b mod m)) mod m

如果 a ≡ b (mod m)，c ≡ d (mod m)，则：
a+c ≡ b+d (mod m)
a*c ≡ b*d (mod m)
```

C++17模板或计算方式：

```cpp
using ll = long long;

ll norm(ll x, ll mod) {
    assert(mod > 0);
    x %= mod;
    if (x < 0) x += mod;
    return x;
}

ll floor_div(ll a, ll b) {
    // b > 0，向下取整
    assert(b > 0);
    __int128 aa = a, bb = b;
    __int128 q = aa / bb;
    __int128 r = aa % bb;
    if (r != 0 && ((r > 0) != (bb > 0))) q--;
    return (ll)q;
}

ll ceil_div(ll a, ll b) {
    // b > 0，向上取整
    assert(b > 0);
    __int128 aa = a, bb = b;
    __int128 q = aa / bb;
    __int128 r = aa % bb;
    if (r != 0 && ((r > 0) == (bb > 0))) q++;
    return (ll)q;
}
```

常见坑：

- C++ 里 `-3 % 5 == -3`，不是 2；需要 `norm`。
- `1e9+7` 不要写成浮点参与计算，写 `1000000007LL`。
- 整除要求余数为 0，不是浮点除法结果为整数。
- 地板除和 C++ `/` 对负数的截断不同。

暴力/部分分替代：

- 小数据直接模拟每一步并记录余数。
- 不会推周期时，用 `vis[余数]` 找循环。

最小验错：

```text
norm(-3, 5) = 2
7 ≡ 2 (mod 5)
floor_div(-3, 2) = -2
ceil_div(-3, 2) = -1
```

## 2. gcd/lcm 与 Bezout 直觉

题面触发词：

- 最大公约数、最小公倍数。
- 互质、约分、公共因子。
- 两个周期何时同时发生。
- 是否存在整数 `x,y` 使 `ax+by=c`。

使用条件：

- `gcd(a,b)` 用于公共因子和互质判断。
- `lcm(a,b)` 用于周期合并，要求注意溢出。
- `ax+by=c` 有整数解当且仅当 `gcd(a,b) | c`。

公式/结论：

```text
gcd(a,b) = gcd(b, a mod b)
lcm(a,b) = |a / gcd(a,b) * b|
gcd(a,b) = 1 表示 a,b 互质。

Bezout:
存在整数 x,y，使 ax + by = gcd(a,b)。
所以 ax + by = c 有解 <=> gcd(a,b) | c。
```

C++17模板或计算方式：

```cpp
using ll = long long;

ll gcd_ll(ll a, ll b) {
    if (a == LLONG_MIN || b == LLONG_MIN) {
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

常见坑：

- `lcm` 先乘再除容易溢出。
- `gcd(0,x)=|x|`。
- `lcm(0,x)=0`。
- 周期合并很多次时，一旦超过题目上限就可以停止。

暴力/部分分替代：

- 小数据从 `min(a,b)` 往下枚举 gcd。
- 小数据从 `max(a,b)` 往上枚举 lcm。
- 周期问题直接模拟到第一个同时出现的位置。

最小验错：

```text
gcd(12,18)=6
lcm(12,18)=36
gcd(0,7)=7
方程 6x+10y=8 有解，因为 gcd=2 且 2|8
方程 6x+10y=9 无解
```
