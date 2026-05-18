# MATHREF-04 组合数学、容斥、抽屉与常见计数

本文件定位：纸质查阅常用计数结论。先判断“有序/无序、可重复/不可重复、是否有禁区、是否取模”。

调用示例：先判断是否“选 k 个”“排列”“不相邻”“括号/合法序列”，再接组合数、容斥或 Catalan 小节。

最小测试样例：`C(5,2)=10`，`P(5,2)=20`，`Catalan(3)=5`。

模块编号：MATHREF-04

模块名称：组合数学、容斥、抽屉与常见计数参考

什么时候用：题目问排列组合、路径条数、二项式系数、容斥、抽屉原理、Catalan 或常见计数模型。

不要什么时候用：题目有明显顺序状态依赖时，优先看 DP-20 计数 DP；只求普通 `C(n,k)` 代码时看 MATH-03。

复杂度：公式型 `O(1)`；Pascal 预处理 `O(n^2)`；阶乘逆元预处理 `O(n)`；容斥通常 `O(2^m)`。

依赖的标准容器：`vector<ll>`、`vector<vector<ll>>`；小集合容斥可用 bitmask。

接口：排列组合公式、Pascal、Lucas 入口、容斥、抽屉、Catalan 常见结论。

## 1. 排列组合与二项式

题面触发词：

- 从 `n` 个中选 `k` 个。
- 排列、组合、有序、无序。
- 二项式系数、`C(n,k)`。
- 路径条数，只能向右/向下走。

使用条件：

- 组合：选出集合，不关心顺序。
- 排列：选出并排列，关心顺序。
- 阶乘逆元要求模数是质数；非质数先考虑 Pascal。

公式/结论：

```text
P(n,k) = n! / (n-k)!
C(n,k) = n! / (k!(n-k)!)
C(n,k) = C(n,n-k)
C(n,k) = C(n-1,k-1) + C(n-1,k)

二项式：
(x+y)^n = sum C(n,k) x^k y^(n-k)

网格从 (1,1) 到 (n,m)，只向下/右：
路径数 = C(n+m-2, n-1)
```

C++17模板或计算方式：

```cpp
using ll = long long;

vector<vector<ll>> comb_pascal(int N, ll mod) {
    vector<vector<ll>> C(N + 1, vector<ll>(N + 1, 0));
    for (int i = 0; i <= N; i++) {
        C[i][0] = C[i][i] = 1 % mod;
        for (int j = 1; j < i; j++) {
            C[i][j] = (C[i - 1][j - 1] + C[i - 1][j]) % mod;
        }
    }
    return C;
}
```

常见坑：

- `C(n,k)` 中 `k<0` 或 `k>n` 是 0。
- 排列和组合不要混。
- 取模除法不能直接用 `/`。
- `n` 大时 Pascal 是 `O(n^2)`，只能小范围。

暴力/部分分替代：

- `n <= 20`：DFS 枚举选/不选。
- `N <= 2000`：Pascal 递推。
- 查询少且 `k` 小：用整数约分乘法计算。

最小验错：

```text
C(5,2)=10
P(5,2)=20
C(5,0)=1
3x3 网格路径数 = C(4,2)=6
```

## 2. Lucas 定理

题面触发词：

- `n,k` 极大，模数是小质数。
- 求 `C(n,k) mod p`，`p` 是质数。
- 多次大组合数查询。

使用条件：

- 模数 `p` 必须是质数。
- 通常 `p` 较小，可以预处理 `0..p-1` 的组合数。
- `n,k` 可很大，用 `p` 进制拆位。

公式/结论：

```text
把 n,k 写成 p 进制：
n = n0 + n1*p + n2*p^2 + ...
k = k0 + k1*p + k2*p^2 + ...

Lucas:
C(n,k) mod p = product C(ni,ki) mod p
若某位 ki > ni，则答案为 0。
```

C++17模板或计算方式：

```cpp
using ll = long long;

ll mod_pow(ll a, ll e, ll mod) {
    ll r = 1 % mod;
    while (e) {
        if (e & 1) r = r * a % mod;
        a = a * a % mod;
        e >>= 1;
    }
    return r;
}

struct Lucas {
    ll p;
    vector<ll> fac, ifac;

    void init(ll prime_mod) {
        p = prime_mod;
        assert(p <= INT_MAX);
        fac.assign(p, 1);
        ifac.assign(p, 1);
        for (int i = 1; i < p; i++) fac[i] = fac[i - 1] * i % p;
        ifac[p - 1] = mod_pow(fac[p - 1], p - 2, p);
        for (int i = (int)p - 1; i >= 1; i--) ifac[i - 1] = ifac[i] * i % p;
    }

    ll smallC(ll n, ll k) const {
        if (k < 0 || k > n) return 0;
        return fac[n] * ifac[k] % p * ifac[n - k] % p;
    }

    ll C(ll n, ll k) const {
        if (k < 0 || k > n) return 0;
        ll ans = 1;
        while (n > 0 || k > 0) {
            ll ni = n % p, ki = k % p;
            if (ki > ni) return 0;
            ans = ans * smallC(ni, ki) % p;
            n /= p;
            k /= p;
        }
        return ans;
    }
};
```

常见坑：

- Lucas 只适用于质数模数。
- `p` 太大时不能开 `fac[p]`。
- 每一位如果 `ki>ni`，直接 0。
- `fac` 下标是 `0..p-1`，p 很大要转 int 风险。

暴力/部分分替代：

- `n <= 2000`：Pascal。
- 查询少：用乘法公式加约分。
- 模数不是质数：Lucas 不适用，先拿小数据部分分。

最小验错：

```text
C(5,2) mod 3 = 10 mod 3 = 1
5=(12)_3, 2=(02)_3
C(2,2)*C(1,0)=1
```

## 3. 容斥

题面触发词：

- 至少一个、没有任何一个。
- 不包含某些元素。
- 能被多个数中至少一个整除。
- 计算并集大小。

使用条件：

- 条件数量不大，或交集大小容易算。
- 能计算每个条件子集同时满足的数量。
- `m <= 20` 是常见子集容斥范围。

公式/结论：

```text
|A1 union A2 union ... union Am|
= sum |Ai|
  - sum |Ai intersect Aj|
  + sum |Ai intersect Aj intersect Ak|
  - ...

奇数个集合交集加，偶数个集合交集减。
```

C++17模板或计算方式：

```cpp
long long inclusion_exclusion_basic(int m, function<long long(long long)> count_intersection) {
    assert(0 <= m && m <= 60);
    __int128 ans = 0;
    for (long long mask = 1; mask < (1LL << m); mask++) {
        int bits = __builtin_popcountll((unsigned long long)mask);
        long long cur = count_intersection(mask);
        if (bits & 1) ans += cur;
        else ans -= cur;
    }
    return (long long)ans;
}
```

常见坑：

- 符号反了。
- 空集不参与“至少一个”的容斥。
- 交集计数写错比容斥公式本身更常见。
- `1<<m` 要求 `m` 不大。

暴力/部分分替代：

- 枚举每个对象，逐个检查是否满足条件。
- 用布尔数组标记被覆盖对象。

最小验错：

```text
1..10 中能被 2 或 3 整除：
floor(10/2)+floor(10/3)-floor(10/6)=5+3-1=7
```

## 4. 鸽巢/抽屉原理

题面触发词：

- 至少有两个相同。
- 证明一定存在。
- `n+1` 个物品放进 `n` 个盒子。
- 余数、颜色、生日、前缀和模 `m`。

使用条件：

- 要证明存在性，而不是构造复杂对象。
- 能把对象映射到有限个“盒子”。
- 对前缀和取模是常见盒子。

公式/结论：

```text
普通抽屉：
n+1 个物品放入 n 个盒子，至少一个盒子有 >=2 个物品。

加强版：
N 个物品放入 k 个盒子，至少一个盒子有 ceil(N/k) 个物品。

前缀和结论：
若有 n 个数，考虑前缀和 mod n。
若某个前缀余数为 0，存在和能被 n 整除的前缀。
否则 n 个非零余数落入 n-1 个盒子，必有两个相同，相减得到一段和能被 n 整除。
```

C++17模板或计算方式：

```cpp
// 找一段非空子数组，其和能被 n 整除。返回 1-index 闭区间。
pair<int,int> subarray_sum_divisible_by_n(const vector<long long> &a) {
    int n = (int)a.size() - 1;
    if (n <= 0) return {-1, -1};
    vector<int> first(n, -1);
    long long sum = 0;
    first[0] = 0;
    for (int i = 1; i <= n; i++) {
        sum = (sum + a[i] % n) % n;
        if (sum < 0) sum += n;
        if (first[sum] != -1) return {first[sum] + 1, i};
        first[sum] = i;
    }
    return {-1, -1};
}
```

常见坑：

- 抽屉原理只保证存在，不一定直接给构造。
- 盒子数量要数对。
- 前缀和余数有 `0..n-1` 共 n 种。
- 题目要求输出方案时，要保存第一次出现位置。

暴力/部分分替代：

- 枚举所有区间和，检查是否满足。
- 小数据直接搜索构造。

最小验错：

```text
1-index 数组 a={0,1,2,3}, n=3
前缀和 mod 3：1,0
[1,2] 的和 3 能被 3 整除
```

## 5. Catalan 与常见计数

题面触发词：

- 合法括号序列。
- 出栈序列、二叉树形态。
- 不越过对角线的路径。
- 将凸多边形三角剖分。

使用条件：

- 典型 Catalan 结构：每个前缀都不“欠账”。
- 常见规模不大可 DP，大规模需要组合数。
- 取模组合公式要求模数处理正确。

公式/结论：

```text
Catalan(n) = 1/(n+1) * C(2n,n)
Catalan(n) = C(2n,n) - C(2n,n+1)

递推：
cat[0]=1
cat[n] = sum_{i=0..n-1} cat[i] * cat[n-1-i]

前几项：
1, 1, 2, 5, 14, 42
```

C++17模板或计算方式：

```cpp
vector<long long> catalan_dp(int N, long long mod) {
    assert(mod > 0);
    vector<long long> cat(N + 1, 0);
    cat[0] = 1 % mod;
    for (int n = 1; n <= N; n++) {
        for (int i = 0; i < n; i++) {
            cat[n] = (cat[n] + (__int128)cat[i] * cat[n - 1 - i]) % mod;
        }
    }
    return cat;
}
```

常见坑：

- `1/(n+1)` 是模意义除法，不能直接整数除再取模，除非先算整数大数。
- 合法括号要求任意前缀左括号数不少于右括号数。
- Catalan 模型很多，但别把所有路径题都套 Catalan。

暴力/部分分替代：

- `n <= 10`：枚举所有括号序列检查合法。
- `N <= 5000`：Catalan DP。
- 大规模且不会逆元：用 `C(2n,n)-C(2n,n+1)` 配合 Pascal 小范围。

最小验错：

```text
n=0 -> 1
n=1 -> 1
n=2 -> 2
n=3 -> 5
```
