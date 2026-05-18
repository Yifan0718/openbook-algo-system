# DP-10：编辑距离

模型编号：DP-10

模型名称：编辑距离

标签：DP、两个字符串、插入、删除、替换、最小操作数

一句话用途：求把一个字符串变成另一个字符串的最少插入、删除、替换次数。

题面触发词：

- “插入、删除、替换”
- “一个字符串变成另一个字符串”
- “最少操作次数”
- “编辑距离”
- “纠错/相似度”

什么时候用：

- 操作对象是两个字符串/序列的前缀。
- 每次操作只影响当前末尾或当前位置。

不要什么时候用：

- 只允许删除并求最长匹配，可能是 LCS。
- 操作有复杂全局限制，需要把限制加入状态。
- 操作代价不是常数时，仍可用，但转移要改权重。

复杂度：

- 时间 `O(nm)`。
- 空间 `O(nm)`，可滚动成 `O(m)`。

数据范围信号：

- `n,m <= 3000/5000`：可尝试。
- `n,m` 很大：普通编辑距离不可直接做。

依赖的标准容器：

- `string s, t`
- `vector<vector<int>> dp`

输入如何整理：

- 字符串 0-index。
- `dp[i][j]` 的 `i/j` 表示前缀长度。

接口：

```cpp
int edit_distance(const string& s, const string& t);
```

输出能力：

- 最少操作数。
- 可扩展为恢复操作路径。

下游可接：

- 字符串相似度。
- 路径恢复。

可拼接模块：

- LCS：只允许删除时可用 LCS 转换。
- 滚动数组。
- DP-22：编辑距离完整建模例题，适合先看推导再抄模板。

状态句式：

```text
dp[i][j] 表示：把 s 的前 i 个字符变成 t 的前 j 个字符所需的最少操作数。
```

初始化：

```text
dp[i][0] = i：把前 i 个字符变成空串，需要删除 i 次。
dp[0][j] = j：把空串变成前 j 个字符，需要插入 j 次。
```

转移模板：

```cpp
if (s[i - 1] == t[j - 1]) dp[i][j] = dp[i - 1][j - 1];
else {
    dp[i][j] = 1 + min({
        dp[i - 1][j],     // 删除 s[i-1]
        dp[i][j - 1],     // 插入 t[j-1]
        dp[i - 1][j - 1]  // 替换
    });
}
```

答案位置：

- `dp[n][m]`。

循环顺序：

- `i` 从 0 到 `n` 初始化第一列。
- `j` 从 0 到 `m` 初始化第一行。
- 主循环 `i=1..n`，`j=1..m`。

暴力 DFS 版本：

```cpp
int dfs(int i, int j) {
    if (i == n) return m - j; // 只能插入剩余字符
    if (j == m) return n - i; // 只能删除剩余字符
    if (s[i] == t[j]) return dfs(i + 1, j + 1);
    int del = dfs(i + 1, j);
    int ins = dfs(i, j + 1);
    int rep = dfs(i + 1, j + 1);
    return 1 + min({del, ins, rep});
}
```

记忆化版本：

```cpp
vector<vector<int>> memo, vis;

int dfs(int i, int j) {
    if (i == n) return m - j;
    if (j == m) return n - i;
    if (vis[i][j]) return memo[i][j];
    vis[i][j] = 1;
    if (s[i] == t[j]) return memo[i][j] = dfs(i + 1, j + 1);
    int ans = 1 + min({dfs(i + 1, j), dfs(i, j + 1), dfs(i + 1, j + 1)});
    return memo[i][j] = ans;
}
```

表推版本：

```cpp
int n = s.size(), m = t.size();
vector<vector<int>> dp(n + 1, vector<int>(m + 1, 0));
for (int i = 0; i <= n; i++) dp[i][0] = i;
for (int j = 0; j <= m; j++) dp[0][j] = j;

for (int i = 1; i <= n; i++) {
    for (int j = 1; j <= m; j++) {
        if (s[i - 1] == t[j - 1]) dp[i][j] = dp[i - 1][j - 1];
        else dp[i][j] = 1 + min({dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]});
    }
}
cout << dp[n][m] << '\n';
```

常见变体：

- 插入/删除/替换代价不同：把 `+1` 改成对应代价。
- 只允许插入删除：转移去掉替换。
- 输出操作序列：从 `dp[n][m]` 反推。

常见坑：

- 第一行第一列没初始化。
- 相等字符仍加了操作代价。
- 插入和删除方向混乱，但最小值仍通常能写对；恢复路径时要小心。
- 字符串下标差 1。

暴力/部分分替代：

- 字符串很短时 DFS。
- 中等长度先记忆化。
- 只问删除次数时，可能用 LCS 简化。

升级方向：

- 二维表 -> 滚动数组。
- 带阈值的编辑距离可只算带状区域。
- 操作路径恢复。

最小测试样例：

```text
horse
ros
输出：3
```
