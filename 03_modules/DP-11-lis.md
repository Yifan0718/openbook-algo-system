# DP-11：LIS 最长递增子序列

模型编号：DP-11

模型名称：LIS

标签：DP、序列、递增、二分优化

一句话用途：求一个序列中保持原相对顺序的最长递增/不下降子序列长度。

题面触发词：

- “最长递增子序列”
- “最长上升子序列”
- “不下降子序列”
- “保持原顺序”
- “最多能选多少个”

什么时候用：

- 只处理一个序列。
- 要求选出的元素下标递增，值也满足递增/不下降。

不要什么时候用：

- 要求连续，改成最长递增连续段。
- 有两个序列公共匹配，转 LCS。
- 有额外容量/代价限制，需要扩展状态。

复杂度：

- 朴素 DP：`O(n^2)`。
- 二分优化：`O(n log n)`。

数据范围信号：

- `n <= 5000`：朴素 `O(n^2)` 可写。
- `n <= 2e5`：用二分优化。

依赖的标准容器：

- `vector<ll> a(n + 1)`
- `vector<int> dp(n + 1)`
- `vector<ll> d`

输入如何整理：

- 序列读成 `a[1..n]`；二分辅助数组 `d` 是 STL 工作容器，可按 `push_back` 自然使用。

接口：

```cpp
int lis_length(const vector<ll>& a);
```

输出能力：

- LIS 长度。
- 可扩展恢复一个序列。

下游可接：

- DP + 树状数组优化。
- 坐标压缩。
- DP-23 LIS/LCS 常见变体速查：路径恢复、二维偏序、公共子串/LCS 区分。

可拼接模块：

- Compressor：值域大但要用树状数组。
- 树状数组/SegmentTree：求以值为结尾的最大长度。

状态句式：

朴素 DP：

```text
dp[i] 表示：必须以第 i 个元素结尾的最长递增子序列长度。
```

二分优化：

```text
d[len] 表示：长度为 len 的递增子序列中，最小可能结尾值。
```

初始化：

```text
朴素：dp[i] = 1，每个元素自己就是长度 1 的子序列。
二分：d 为空，逐个插入/替换。
```

转移模板：

朴素：

```cpp
if (a[j] < a[i]) dp[i] = max(dp[i], dp[j] + 1);
```

二分：

```cpp
auto it = lower_bound(d.begin(), d.end(), a[i]); // 严格递增
```

答案位置：

- 朴素：`max(dp[1..n])`。
- 二分：`d.size()`。

循环顺序：

- 朴素：`i` 从 1 到 `n`，`j` 从 1 到 `i-1`。
- 二分：按原序列顺序扫描。

暴力 DFS 版本：

```cpp
int dfs(int i, int last) {
    if (i == n + 1) return 0;
    int ans = dfs(i + 1, last);
    if (last == 0 || a[last] < a[i]) {
        ans = max(ans, 1 + dfs(i + 1, i));
    }
    return ans;
}
```

记忆化版本：

```cpp
vector<vector<int>> memo, vis;

int dfs(int i, int last) {
    if (i == n + 1) return 0;
    if (vis[i][last]) return memo[i][last];
    vis[i][last] = 1;
    int ans = dfs(i + 1, last);
    if (last == 0 || a[last] < a[i]) ans = max(ans, 1 + dfs(i + 1, i));
    return memo[i][last] = ans;
}
```

表推版本：

```cpp
vector<int> dp(n + 1, 1);
int ans = 0;
for (int i = 1; i <= n; i++) {
    for (int j = 1; j < i; j++) {
        if (a[j] < a[i]) dp[i] = max(dp[i], dp[j] + 1);
    }
    ans = max(ans, dp[i]);
}
cout << ans << '\n';
```

二分优化版本：

```cpp
vector<ll> d;
for (int i = 1; i <= n; i++) {
    auto it = lower_bound(d.begin(), d.end(), a[i]); // 严格递增
    if (it == d.end()) d.push_back(a[i]);
    else *it = a[i];
}
cout << (int)d.size() << '\n';
```

常见变体：

- 最长不下降子序列：二分用 `upper_bound`。
- 求方案数：通常用 DP + 树状数组。
- 二维偏序：排序后一维 LIS。

常见坑：

- 严格递增和不下降混淆。
- 朴素 DP 的答案是 `max(dp[i])`，不是 `dp[n]`。
- 二分数组 `d` 不一定是一条真实子序列，只能用于长度。
- 有重复值时排序和二分规则容易错。

暴力/部分分替代：

- `n <= 25`：选/不选 DFS。
- `n <= 5000`：朴素 DP。
- `n` 大：二分优化。

升级方向：

- 朴素 `O(n^2)` -> 二分 `O(n log n)`。
- 需要计数/带权：坐标压缩 + 树状数组/SegmentTree。
- 需要恢复序列：记录前驱。
- 二维偏序、重复值 tie-break、输出一条 LIS 时，优先翻 DP-23。

最小测试样例：

```text
6
10 9 2 5 3 7
输出：3
说明：2 5 7 或 2 3 7。
```
