# MATH-04 筛法与质因数分解

模块编号：MATH-04

模块名称：质数筛、最小质因子与质因数分解

标签：[数学][筛法][质数][质因数分解]

一句话用途：预处理质数，快速判断质数、分解整数，并支持因子个数、因子和、欧拉函数等数论计数。

题面触发词：

- 质数、素数、合数。
- 质因数、分解质因数。
- 因子个数、约数个数、约数和。
- 多次询问某数是否为质数。
- `1..n` 中有多少质数。

什么时候用：

- 需要对很多数判断质数。
- 需要快速分解许多 `x <= N` 的数。
- 需要枚举质数做试除。
- 因子相关计数题。

不要什么时候用：

- 只判断一个很大的数，筛到 `sqrt(x)` 可能够，但筛到 `x` 不行。
- `N` 达到 `1e9` 不能开数组筛。
- 只需要 gcd/lcm 时，不一定要分解。

复杂度：

- 埃氏筛：`O(N log log N)`。
- 线性筛：`O(N)`。
- 用最小质因子分解 `x`：`O(质因子个数)`。
- 用质数表试除分解 `x`：`O(pi(sqrt(x)))`。

数据范围参考：

- `N <= 1e7`：可筛，注意内存。
- 多次分解 `x <= 1e7`：预处理 `spf` 最稳。
- 单次 `x <= 1e12`：筛到 `1e6` 后试除。

依赖的标准容器：

- `vector<int> primes`。
- `vector<int> spf`，下标自然从 `0..N`。

输入如何整理：

```cpp
int N;
cin >> N;
LinearSieve sieve;
sieve.init(N);
```

接口：

```text
LinearSieve.init(N)
is_prime(x)
factorize_by_spf(x)
factorize_by_primes(x, primes)
```

输出能力：

- 质数表。
- 判断 `x` 是否质数。
- 质因数分解结果 `(p, cnt)`。
- 因子个数、因子和的基础材料。

下游可接：

- 组合数非质数模数的高级处理。
- gcd/lcm 分析。
- 容斥中枚举质因子集合。

可拼接模块：

- MATH-01 gcd/lcm。
- MATH-03 逆元中判断互质。
- MATH-06 容斥基础。

模数是否为质数的分支：

```text
本模块可用来判断 mod 是否为质数。
mod 是质数 -> 逆元/组合数可走费马和 fac/ifac。
mod 不是质数 -> 逆元只在 gcd(a, mod)==1 时存在；组合数不要直接 fac/ifac。
```

模板代码：

```cpp
using ll = long long;

struct LinearSieve {
    int N;
    vector<int> primes;
    vector<int> spf; // smallest prime factor

    void init(int n) {
        N = n;
        primes.clear();
        spf.assign(N + 1, 0);
        for (int i = 2; i <= N; i++) {
            if (spf[i] == 0) {
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
        if (x < 2 || x > N) return false;
        return spf[x] == x;
    }

    vector<pair<int, int>> factorize_by_spf(int x) const {
        assert(2 <= x && x <= N);
        vector<pair<int, int>> res;
        while (x > 1) {
            int p = spf[x], cnt = 0;
            while (x % p == 0) {
                x /= p;
                cnt++;
            }
            res.push_back({p, cnt});
        }
        return res;
    }
};

vector<pair<ll, int>> factorize_by_primes(ll x, const vector<int> &primes) {
    vector<pair<ll, int>> res;
    if (x <= 1) return res;
    for (int p : primes) {
        if ((ll)p > x / p) break;
        if (x % p == 0) {
            int cnt = 0;
            while (x % p == 0) {
                x /= p;
                cnt++;
            }
            res.push_back({p, cnt});
        }
    }

    // 如果 primes 没筛到 sqrt(原始 x)，继续朴素试除，避免把合数静默当质数。
    ll start = primes.empty() ? 2LL : (ll)primes.back() + 1;
    if (start <= 2 && x % 2 == 0) {
        int cnt = 0;
        while (x % 2 == 0) {
            x /= 2;
            cnt++;
        }
        res.push_back({2, cnt});
        start = 3;
    }
    if (start % 2 == 0) start++;
    for (ll d = start; d <= x / d; d += 2) {
        if (x % d == 0) {
            int cnt = 0;
            while (x % d == 0) {
                x /= d;
                cnt++;
            }
            res.push_back({d, cnt});
        }
    }
    if (x > 1) res.push_back({x, 1});
    return res;
}
```

调用示例：

```cpp
LinearSieve sieve;
sieve.init(1000000);

if (sieve.is_prime(97)) {
    // 97 是质数
}

auto fac = sieve.factorize_by_spf(360);
// fac = (2,3), (3,2), (5,1)

auto big_fac = factorize_by_primes(1000000000039LL, sieve.primes);
```

常见坑：

- `1` 不是质数。
- `spf[0]`、`spf[1]` 没有意义。
- `x > N` 时不能用 `factorize_by_spf(x)`。
- 试除循环条件用 `(ll)p * p <= x`，避免 `p*p` 溢出。
- `factorize_by_primes` 最好筛到 `sqrt(x)`；本模板带朴素兜底，质数表不够时仍正确但会慢。
- 多测不同 `N` 时，筛到所有测试的最大 `N` 更省时间。

暴力/部分分替代：

- 单次判断质数：枚举 `d=2..sqrt(x)`。
- 单次分解：从 `d=2` 开始试除。
- `N <= 5000`：直接双重循环标记合数也能拿分。

升级方向：

- 区间 `[L,R]` 很大但长度小 -> 区间筛。
- 大整数质性测试 -> Miller-Rabin，低优先级。
- 分解 `1e18` 大数 -> Pollard Rho，高难低优先级。

最小测试样例：

```text
init(20)
primes = 2 3 5 7 11 13 17 19
is_prime(1) = false
is_prime(17) = true
factorize_by_spf(360) = 2^3 * 3^2 * 5^1
```
