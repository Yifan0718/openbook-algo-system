# BRUTE-08：数组 / vector 记忆化

模块编号：BRUTE-08

模块名称：数组 / vector 记忆化

标签：vector memo、数组 memo、状态范围明确、最快版本

一句话用途：当每一维状态范围都清楚时，用 `vector` 或数组做最快、最稳的记忆化。

题面触发词：

- `0 <= i <= n`
- `0 <= rest <= W`
- `mask < 2^n`
- 维度小、边界明确。

适用场景：

- 背包类 `dfs(i, rest)`。
- 网格类 `dfs(x, y)`。
- 状压类 `dfs(mask, last)`。
- 数位 DP 中小范围状态。

什么时候用：

- 每个参数都能映射到非负整数下标。
- 总状态数能开内存。
- 追求比 `map` 更快。

不要什么时候用：

- 参数有大负数、大值域、字符串或复杂结构。
- 状态稀疏但范围巨大。
- 维度太多导致内存不可控。

复杂度：

- 时间：`O(状态数 * 转移数)`。
- 空间：`O(状态数)`。
- 查询/写入：`O(1)`。

数据范围参考：

- `n * W <= 1e7` 比较稳。
- `2^n * n` 要求 `n <= 20` 左右。
- `vector<vector<vector<...>>>` 维度越多越要先算内存。

依赖的标准容器：

- `vector`

输入如何整理：

- 普通物品/序列下标统一用 `1..n`；如果用 vector，也开 `n + 1`。
- 若 `rest` 可为负，先在函数开头拦截，不要访问 `memo[i][rest]`。
- 若状态含负数，例如 `diff in [-S,S]`，使用 `diff + OFFSET`。

接口：

```cpp
vector<vector<long long>> memo;
vector<vector<int>> vis;
long long dfs(int i, int rest);
```

输出能力：

- 最大值 / 最小值 / 计数 / 可行性。
- 可以额外存 `choice[i][rest]` 还原路径。

下游可接：

- DP 卷表推背包、网格、状压。
- BRUTE-14 提交版本路线。

可拼接模块：

- BRUTE-07 记忆化搜索总论。
- BRUTE-04 组合 DFS。
- BRUTE-05 子集枚举。

模板代码：

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const ll LINF = (1LL << 60);

int n, W;
vector<int> cost;
vector<ll> value;
vector<vector<ll>> memo;
vector<vector<int>> vis;

ll dfs(int i, int rest) {
    if (rest < 0) return -LINF;
    if (i == n + 1) return 0;

    if (vis[i][rest]) return memo[i][rest];
    vis[i][rest] = 1;

    ll ans = dfs(i + 1, rest);
    ans = max(ans, value[i] + dfs(i + 1, rest - cost[i]));

    return memo[i][rest] = ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n >> W;
    cost.assign(n + 1, 0);
    value.assign(n + 1, 0);
    for (int i = 1; i <= n; i++) cin >> cost[i] >> value[i];

    memo.assign(n + 2, vector<ll>(W + 1, 0));
    vis.assign(n + 2, vector<int>(W + 1, 0));

    cout << dfs(1, W) << '\n';
    return 0;
}
```

调用示例：

```cpp
memo.assign(n + 2, vector<ll>(W + 1, 0));
vis.assign(n + 2, vector<int>(W + 1, 0));
cout << dfs(1, W) << '\n';
```

常见坑：

- `rest < 0` 之后才访问 `memo[i][rest]`，直接越界。
- `memo` 初值和真实答案冲突，所以建议单独用 `vis`。
- 多测时 `memo/vis` 没有重新 `assign`。
- `W` 很大时开二维数组 MLE。
- `vector<bool>` 有特殊实现，不建议做通用 memo 标记。

暴力/部分分替代：

- 状态范围太大：改 `map<tuple,...>`。
- 只需小数据：保留 DFS。
- `rest` 维很大但实际状态少：用 `unordered_map` 或 `map`。

升级方向：

- vector memo -> 表推 DP。
- 二维 memo -> 滚动数组。
- `dfs(i, rest)` -> `dp[i][rest]` 或 `dp[rest]`。

最小测试样例：

```text
输入：
2 3
2 5
3 7

输出：
7
```
