# BRUTE-10：unordered_map + 编码记忆化

模块编号：BRUTE-10

模块名称：`unordered_map` + 编码记忆化

标签：哈希、编码、稀疏状态、性能升级

一句话用途：当状态范围较大但实际访问稀疏，且能保证编码不冲突时，用 `unordered_map<long long,...>` 加速 memo。

题面触发词：

- `map` 版本能过样例但可能慢。
- 状态范围已知。
- 状态稀疏，不适合开大数组。
- 多维整数状态。

适用场景：

- `dfs(i, rest, last)` 中 `rest` 范围很大但访问少。
- BFS/DFS 状态需要哈希去重。
- `mask` 与小整数维度组合。

什么时候用：

- 每一维范围能明确写出来。
- 能设计无冲突编码。
- 需要比 `map` 更快的查询。

不要什么时候用：

- 不知道每一维范围。
- 维度有负数但没有平移。
- 编码可能冲突。
- 状态范围小且稠密，vector 更好。

复杂度：

- 平均查询/写入：`O(1)`。
- 最坏可能退化，但考试中通常可接受。
- 总时间：`O(状态数 * 转移数)` 平均。

数据范围参考：

- 状态数量 `1e5~1e6` 可尝试。
- 若 `unordered_map` 超时，可以 `reserve` 和调低装载因子。

依赖的标准容器：

- `unordered_map`
- `vector`

输入如何整理：

- 把状态维度转为非负整数。
- 为每一维确定上界，例如 `i <= n`、`rest <= W`、`last <= n`。
- 用乘法进制编码，比位移更不容易算错。

接口：

```cpp
long long encode(int i, int rest, int last);
unordered_map<long long, long long> memo;
```

输出能力：

- 最大值 / 最小值 / 计数 / 可行性。
- 稀疏状态快速缓存。

下游可接：

- BFS 状态搜索去重。
- 状压 DP 稀疏优化。

可拼接模块：

- BRUTE-07 记忆化搜索总论。
- BRUTE-09 map<tuple> memo。
- BRUTE-11 BFS 状态搜索。

模板代码：

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const ll LINF = (1LL << 60);

int n, W;
vector<int> cost;
vector<ll> value;
unordered_map<ll, ll> memo;

// 要求：0 <= i <= n+1, 0 <= rest <= W, 0 <= last <= n。
ll encode(int i, int rest, int last) {
    ll base_rest = (ll)W + 1;
    ll base_last = (ll)n + 1;
    return ((ll)i * base_rest + rest) * base_last + last;
}

ll dfs(int i, int rest, int last) {
    if (rest < 0) return -LINF;
    if (i == n + 1) return 0;

    ll key = encode(i, rest, last);
    auto it = memo.find(key);
    if (it != memo.end()) return it->second;

    ll ans = dfs(i + 1, rest, last);
    if (last == 0 || i - last >= 2) {
        ans = max(ans, value[i] + dfs(i + 1, rest - cost[i], i));
    }

    memo[key] = ans;
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n >> W;
    cost.assign(n + 1, 0);
    value.assign(n + 1, 0);
    for (int i = 1; i <= n; i++) cin >> cost[i] >> value[i];

    memo.reserve(200000);
    memo.max_load_factor(0.7);

    cout << dfs(1, W, 0) << '\n';
    return 0;
}
```

调用示例：

```cpp
memo.clear();
memo.reserve(estimated_states * 2);
cout << dfs(1, W, 0) << '\n';
```

常见坑：

- 编码冲突：两个不同状态算出同一个 key。
- 乘法编码溢出 `long long`。
- 状态有负数没有加 OFFSET。
- 多测中 `W` 或 `n` 变化，旧 key 不能复用，必须 `clear()`。
- 用 `memo[key]` 查存在性，会插入默认值。

暴力/部分分替代：

- 不确定编码：退回 `map<tuple,...>`。
- 状态范围小：用 vector。
- 状态没重复：保留 DFS + 剪枝。

升级方向：

- `map<tuple>` -> 编码 `unordered_map`。
- 编码 memo -> vector memo。
- 哈希 DFS -> 表推 DP 或 BFS 去重。

最小测试样例：

```text
输入：
3 5
2 5
2 6
3 7

输出：
12
```

