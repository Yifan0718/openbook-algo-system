# MATH-06 容斥基础

模块编号：MATH-06

模块名称：容斥原理基础模板

标签：[数学][容斥][计数][集合]

一句话用途：把“至少满足一个条件”的计数转成若干交集计数的加减。

题面触发词：

- 至少一个、不能被任何一个、被若干数整除。
- 多个限制条件，问合法数量。
- 不含某些元素、没有某些性质。
- 求并集大小。
- 条件数量较少，通常 `m <= 20`。

什么时候用：

- 每个条件单独或交集都容易计数。
- 条件数不大，可以枚举子集。
- 问“满足至少一个条件”或“避开所有条件”。
- 倍数计数：`1..n` 中能被给定数集合中至少一个整除。

不要什么时候用：

- 条件数很大，`2^m` 爆炸。
- 交集计数本身很难。
- 条件之间不是简单集合关系，容易重复或漏算。
- `lcm` 超过上界且未防溢出。

复杂度：

- 枚举条件子集：`O(2^m * m)`。
- 若每个交集 `O(1)` 可算，则总复杂度约 `O(2^m * m)`。

数据范围参考：

- `m <= 20`：标准子集容斥。
- `m <= 25`：可能勉强，注意常数。
- `n <= 1e18`：倍数计数可用 `n / lcm`，必须防溢出。

依赖的标准容器：

- `vector<ll> a(m)`，容斥条件内部通常用 0-index 枚举子集。
- 若条件来自题面 1-index，读入后可放到 `a[0..m-1]`。

输入如何整理：

```cpp
ll n;
int m;
cin >> n >> m;
vector<ll> d(m);
for (int i = 0; i < m; i++) cin >> d[i];
```

接口：

```text
count_divisible_by_any(n, d) -> 1..n 中能被 d 中至少一个数整除的个数
count_divisible_by_none(n, d) -> 1..n 中不能被任何 d 整除的个数
```

输出能力：

- 并集大小。
- 不满足任何条件的补集大小。
- 倍数类容斥计数。

下游可接：

- 组合数。
- gcd/lcm。
- DP 中排除非法条件。

可拼接模块：

- MATH-01 gcd/lcm。
- MATH-03 组合数。
- MATH-04 质因数分解。

模数是否为质数的分支：

```text
容斥加减取模时，mod 是否为质数都可以。
只要做加法、减法、乘法，不需要质数。
若交集计数里用组合数除法：
  mod 是质数 -> fac/ifac。
  mod 不是质数 -> Pascal 小范围或其他非质数组合方案。
```

模板代码：

```cpp
using ll = long long;

ll gcd_ll(ll a, ll b) {
    while (b) {
        ll t = a % b;
        a = b;
        b = t;
    }
    return a >= 0 ? a : -a;
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

ll count_divisible_by_any(ll n, const vector<ll> &d) {
    int m = (int)d.size();
    __int128 ans = 0;
    for (int mask = 1; mask < (1 << m); mask++) {
        ll l = 1;
        int bits = 0;
        bool over = false;
        for (int i = 0; i < m; i++) {
            if (mask >> i & 1) {
                if (d[i] == 0) {
                    over = true;
                    break;
                }
                bits++;
                l = lcm_limit(l, d[i], n);
                if (l > n) {
                    over = true;
                    break;
                }
            }
        }
        if (over) continue;
        if (l == 0) continue;
        if (bits & 1) ans += n / l;
        else ans -= n / l;
    }
    return (ll)ans;
}

ll count_divisible_by_none(ll n, const vector<ll> &d) {
    return n - count_divisible_by_any(n, d);
}
```

调用示例：

```cpp
ll n = 10;
vector<ll> d = {2, 3};
cout << count_divisible_by_any(n, d) << "\n";  // 7: 2,3,4,6,8,9,10
cout << count_divisible_by_none(n, d) << "\n"; // 3: 1,5,7
```

常见坑：

- 奇数个条件加，偶数个条件减。
- 枚举子集时 `m` 不能太大。
- `1 << m` 当 `m >= 31` 会溢出 int；本基础模板默认 `m <= 20`。
- `lcm` 必须防溢出，超过 `n` 后这个子集贡献为 0。
- `d[i] == 0` 没有“被 0 整除”的意义，题目若可能出现要先过滤。

暴力/部分分替代：

- `n <= 1e6`：枚举每个数 `x`，检查是否满足条件。
- `m` 小但不会写容斥：用集合/布尔数组标记倍数。
- 组合容斥不会推：先枚举所有方案并检查合法性。

升级方向：

- 条件来自质因子集合 -> 先质因数分解再枚举质因子子集。
- 容斥项中需要组合数 -> 接 MATH-03。
- 条件很多但结构特殊 -> Mobius 反演，低优先级。

最小测试样例：

```text
n=10, d=[2,3]
能被至少一个整除 = 7
不能被任何一个整除 = 3

n=12, d=[2,4]
能被至少一个整除 = 6
```
