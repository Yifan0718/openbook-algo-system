# 数学片段边界运行探针报告

执行环境：WSL `g++ -std=c++17 -O2 -pipe -Wall -Wextra -Werror`

本报告覆盖子代理在数学卷中指出的若干非 standalone 代码片段风险。它们没有完整 `main`，不进入 `standalone_runtime_manifest.json`，因此用临时拼接程序验证关键边界。

## 结果

- `inv_prime(0, 7)` 返回 `-1`，不再静默当作合法逆元。
- `lcm_limit(LLONG_MAX, LLONG_MAX - 1, LLONG_MAX)` 返回 `LLONG_MAX`，不产生 `limit + 1` 溢出。
- `factorize_by_primes(221, {2,3,5,7})` 返回 `13^1, 17^1`，质数表不足时不再把 `221` 当质数。
- `floor_div(LLONG_MIN, 2)` 返回 `-4611686018427387904`。
- `ceil_div(LLONG_MAX, 2)` 返回 `4611686018427387904`。
- `count_coprime_pairs(0, 5)` 返回 `0`。
- `inclusion_exclusion_basic(5, count_intersection=1)` 返回 `1`。
- `sg_take_stones(3, {0,1})` 返回 `0 1 0 1`，非正 move 被过滤。

结论：数学边界探针通过。
