# MATHREF-03 筛法、质因数分解、欧拉函数与莫比乌斯

本文件定位：数论预处理和乘法函数查阅。优先掌握筛法、分解、phi；莫比乌斯作为中高阶补充。

调用示例：`n <= 1e7` 先考虑筛；单个大数分解用试除或 SPF；互质计数再接 `phi`。

最小测试样例：`12 = 2^2 * 3`，`phi(12)=4`，`mu(1)=1, mu(4)=0, mu(6)=1`。

模块编号：MATHREF-03

模块名称：筛法、质因数分解、欧拉函数与莫比乌斯参考

什么时候用：题目出现质数、分解质因数、约数、互质计数、欧拉函数、莫比乌斯或多次数论预处理。

不要什么时候用：只需要一次 `gcd/lcm` 或快速幂时，优先查 MATHREF-01 或 MATH-02。

复杂度：埃氏筛约 `O(n log log n)`；线性筛 `O(n)`；单个数试除 `O(sqrt n)`；用最小质因子分解约 `O(log n)`。

依赖的标准容器：`vector<int>`、`vector<bool>` 或 `vector<char>`；分解结果常用 `vector<pair<ll,int>>`。

接口：筛质数、最小质因子、质因数分解、`phi(n)`、莫比乌斯函数参考。

## 1. 素数筛与质因数分解

题面触发词：

- 质数、素数、合数。
- 分解质因数、约数个数、约数和。
- 多次询问某数是否是质数。
- 统计 `1..n` 中的质数。

使用条件：

- `N` 不太大时可筛，常见 `N <= 1e7`。
- 多次分解 `x <= N` 时用最小质因子 `spf`。
- 单个大数可用质数表试除到 `sqrt(x)`。

公式/结论：

```text
n = p1^a1 * p2^a2 * ... * pk^ak
约数个数 d(n) = (a1+1)(a2+1)...(ak+1)
约数和 sigma(n) = (1+p1+...+p1^a1) * ...
```

C++17模板或计算方式：

```cpp
using ll = long long;

struct Sieve {
    int N = 0;
    vector<int> primes, spf;

    void init(int n) {
        N = n;
        primes.clear();
        spf.assign(N + 1, 0);
        for (int i = 2; i <= N; i++) {
            if (!spf[i]) {
                spf[i] = i;
                primes.push_back(i);
            }
            for (int p : primes) {
                if (p > spf[i] || (ll)i * p > N) break;
                spf[i * p] = p;
            }
        }
    }

    bool is_prime(int x) const {
        return x >= 2 && x <= N && spf[x] == x;
    }

    vector<pair<int,int>> factor_spf(int x) const {
        assert(2 <= x && x <= N);
        vector<pair<int,int>> res;
        while (x > 1) {
            int p = spf[x], c = 0;
            while (x % p == 0) {
                x /= p;
                c++;
            }
            res.push_back({p, c});
        }
        return res;
    }
};
```

常见坑：

- `1` 不是质数。
- `spf` 只能分解 `<=N` 的数。
- 试除判断 `p*p<=x` 时要转 `long long`。
- `N` 太大不要强行开数组。

暴力/部分分替代：

- 单次判断质数：枚举 `2..sqrt(n)`。
- 单次分解：从 `2` 开始试除。
- 小范围统计质数：双重循环标记合数。

最小验错：

```text
20 以内质数：2 3 5 7 11 13 17 19
360 = 2^3 * 3^2 * 5
约数个数 = 4*3*2 = 24
```

## 2. 欧拉函数 phi

题面触发词：

- `1..n` 中与 `n` 互质的数有多少个。
- 欧拉函数、互质计数。
- 费马/欧拉降幂。
- 分数环、循环节、原根相关基础题。

使用条件：

- `phi(n)` 表示 `1..n` 中与 `n` 互质的正整数个数。
- 需要质因数分解或筛法。
- 欧拉定理要求 `gcd(a,m)=1`。

公式/结论：

```text
若 n = p1^a1 * p2^a2 * ... * pk^ak
phi(n) = n * (1-1/p1) * (1-1/p2) * ... * (1-1/pk)

若 gcd(a,m)=1：
a^phi(m) ≡ 1 (mod m)

质数 p：
phi(p) = p-1
```

C++17模板或计算方式：

```cpp
using ll = long long;

ll phi_one(ll n) {
    ll ans = n;
    for (ll p = 2; p <= n / p; p++) {
        if (n % p == 0) {
            while (n % p == 0) n /= p;
            ans = ans / p * (p - 1);
        }
    }
    if (n > 1) ans = ans / n * (n - 1);
    return ans;
}

vector<int> phi_sieve(int n) {
    vector<int> phi(n + 1), primes, is_comp(n + 1, 0);
    if (n >= 1) phi[1] = 1;
    for (int i = 2; i <= n; i++) {
        if (!is_comp[i]) {
            primes.push_back(i);
            phi[i] = i - 1;
        }
        for (int p : primes) {
            if ((ll)i * p > n) break;
            is_comp[i * p] = 1;
            if (i % p == 0) {
                phi[i * p] = phi[i] * p;
                break;
            } else {
                phi[i * p] = phi[i] * (p - 1);
            }
        }
    }
    return phi;
}
```

常见坑：

- 欧拉定理必须有 `gcd(a,m)=1`。
- `phi[1]=1` 是常用约定。
- `ans = ans / p * (p-1)` 顺序不要写反，避免中间非整数和溢出。
- 大数 `p*p<=n` 要注意溢出。

暴力/部分分替代：

- 小数据直接枚举 `i=1..n`，统计 `gcd(i,n)==1`。
- 多次小范围询问可预处理 gcd 表或直接筛。

最小验错：

```text
phi(1)=1
phi(5)=4
phi(12)=4，对应 1,5,7,11
```

## 3. 莫比乌斯函数与容斥基础

题面触发词：

- 互质对数、`gcd(i,j)=1` 的计数。
- 莫比乌斯、Mobius、反演。
- 容斥、没有被任何质因子整除。
- 平方因子、无平方因子数。

使用条件：

- 入门只需记住 `mu(n)` 与质因数关系。
- 真正的莫比乌斯反演属于中高阶；考试时间紧时优先容斥/暴力拿分。
- 常见用于把 `gcd=1` 转成按公因子求和。

公式/结论：

```text
mu(1)=1
若 n 含有平方质因子，则 mu(n)=0
若 n 是 k 个不同质数的乘积，则 mu(n)=(-1)^k

基础结论：
sum_{d|n} mu(d) = 1, n=1
sum_{d|n} mu(d) = 0, n>1

互质对数：
count(gcd(i,j)=1, 1<=i<=n,1<=j<=m)
= sum_{d=1..min(n,m)} mu(d) * floor(n/d) * floor(m/d)
```

C++17模板或计算方式：

```cpp
vector<int> mobius_sieve(int n) {
    vector<int> mu(n + 1), primes, is_comp(n + 1, 0);
    if (n >= 1) mu[1] = 1;
    for (int i = 2; i <= n; i++) {
        if (!is_comp[i]) {
            primes.push_back(i);
            mu[i] = -1;
        }
        for (int p : primes) {
            if ((long long)i * p > n) break;
            is_comp[i * p] = 1;
            if (i % p == 0) {
                mu[i * p] = 0;
                break;
            } else {
                mu[i * p] = -mu[i];
            }
        }
    }
    return mu;
}

long long count_coprime_pairs(int n, int m) {
    if (n <= 0 || m <= 0) return 0;
    int lim = min(n, m);
    vector<int> mu = mobius_sieve(lim);
    __int128 ans = 0;
    for (int d = 1; d <= lim; d++) {
        ans += (__int128)mu[d] * (n / d) * (m / d);
    }
    return (long long)ans;
}
```

常见坑：

- `mu` 不是欧拉函数。
- 含平方因子时 `mu=0`。
- 互质对公式里的 `floor(n/d)` 是整数除法。
- 反演公式容易套错，基础卷只建议用于熟悉模型。

暴力/部分分替代：

- `n,m <= 3000`：双重循环统计 `gcd(i,j)==1`。
- 条件少时直接用容斥枚举质因子集合。

最小验错：

```text
mu(1)=1
mu(2)=-1
mu(6)=1
mu(12)=0，因为含 2^2
1..2 与 1..2 的互质有 (1,1)(1,2)(2,1)，共 3
```
