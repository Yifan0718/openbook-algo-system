# DP-09：LCS 最长公共子序列

模型编号：DP-09

模型名称：LCS

标签：DP、两个序列、字符串、公共子序列

一句话用途：求两个序列的最长公共子序列长度，或作为两个序列匹配类 DP 的入口。

题面触发词：

- “最长公共子序列”
- “两个字符串/两个序列”
- “保持相对顺序”
- “可以删除一些字符”
- “相似度/匹配长度”

什么时候用：

- 两个序列都只能按原相对顺序匹配。
- 不要求连续；要求连续时是最长公共子串，不是 LCS。

不要什么时候用：

- 允许插入、删除、替换并问最少操作，转编辑距离。
- 只问一个序列的递增子序列，转 LIS。
- 要求公共子串连续，需另写 `dp[i][j]` 表示以 `i,j` 结尾的连续长度。

复杂度：

- 时间 `O(nm)`。
- 空间 `O(nm)`，可滚动成 `O(m)`。

数据范围信号：

- `n,m <= 3000/5000`：`O(nm)` 可能可接受，视内存。
- `n,m >= 1e5`：普通 LCS 不可直接做。

依赖的标准容器：

- `string s, t`
- `vector<vector<int>> dp`

输入如何整理：

- 字符串保持 0-index。
- DP 的 `i/j` 表示前缀长度，访问字符用 `s[i-1]`、`t[j-1]`。

接口：

```cpp
int lcs(const string& s, const string& t);
```

输出能力：

- LCS 长度。
- 可扩展为输出一条 LCS 路径。

下游可接：

- 编辑距离。
- 路径恢复。
- DP-23 LIS/LCS 常见变体速查：恢复一条 LCS、最长公共子串、只插删关系。

可拼接模块：

- 滚动数组。
- 字符串基础模块。

状态句式：

```text
dp[i][j] 表示：s 的前 i 个字符和 t 的前 j 个字符的 LCS 长度。
```

初始化：

```text
dp[0][j] = 0：空串和任何前缀的 LCS 长度为 0。
dp[i][0] = 0：任何前缀和空串的 LCS 长度为 0。
```

转移模板：

```cpp
if (s[i - 1] == t[j - 1]) dp[i][j] = dp[i - 1][j - 1] + 1;
else dp[i][j] = max(dp[i - 1][j], dp[i][j - 1]);
```

答案位置：

- `dp[n][m]`。

循环顺序：

- `i` 从 1 到 `n`。
- `j` 从 1 到 `m`。
- 因为依赖左、上、左上，二维表自然从小到大。

暴力 DFS 版本：

```cpp
int dfs(int i, int j) {
    if (i == n || j == m) return 0;
    int ans = max(dfs(i + 1, j), dfs(i, j + 1));
    if (s[i] == t[j]) ans = max(ans, 1 + dfs(i + 1, j + 1));
    return ans;
}
```

记忆化版本：

```cpp
vector<vector<int>> memo, vis;

int dfs(int i, int j) {
    if (i == n || j == m) return 0;
    if (vis[i][j]) return memo[i][j];
    vis[i][j] = 1;
    int ans = max(dfs(i + 1, j), dfs(i, j + 1));
    if (s[i] == t[j]) ans = max(ans, 1 + dfs(i + 1, j + 1));
    return memo[i][j] = ans;
}
```

表推版本：

```cpp
int n = s.size(), m = t.size();
vector<vector<int>> dp(n + 1, vector<int>(m + 1, 0));
for (int i = 1; i <= n; i++) {
    for (int j = 1; j <= m; j++) {
        if (s[i - 1] == t[j - 1]) dp[i][j] = dp[i - 1][j - 1] + 1;
        else dp[i][j] = max(dp[i - 1][j], dp[i][j - 1]);
    }
}
cout << dp[n][m] << '\n';
```

滚动数组版本：

```cpp
vector<int> dp(m + 1, 0), ndp(m + 1, 0);
for (int i = 1; i <= n; i++) {
    fill(ndp.begin(), ndp.end(), 0);
    for (int j = 1; j <= m; j++) {
        if (s[i - 1] == t[j - 1]) ndp[j] = dp[j - 1] + 1;
        else ndp[j] = max(dp[j], ndp[j - 1]);
    }
    dp.swap(ndp);
}
cout << dp[m] << '\n';
```

常见变体：

- 输出一条 LCS：从 `dp[n][m]` 反向走。
- 最长公共子串：相等时 `dp[i][j]=dp[i-1][j-1]+1`，不等时 `0`。
- 三个序列 LCS：三维，复杂度很高。

常见坑：

- 把子序列误写成子串。
- 字符访问 `s[i]` 与 `dp[i]` 前缀长度混淆。
- 滚动数组更新时覆盖左上角。
- 内存 `n*m` 太大。

暴力/部分分替代：

- 短字符串直接 DFS。
- `n*m` 较大但样例小：记忆化版先交。
- 一个串很短时可考虑状压优化，但初学者低优先级。

升级方向：

- 二维表 -> 滚动数组。
- 路径恢复。
- 若字符集小且数据大，再查高级优化。
- 公共子串、只允许插删、输出具体序列时，优先翻 DP-23。

最小测试样例：

```text
abcde
ace
输出：3
```
