# DP-03：DFS -> 记忆化 -> 表推升级图

模块编号：DP-03

模块名称：DFS -> 记忆化 -> 表推升级图

标签：DP、暴力、记忆化、表推、升级路径

一句话用途：模型匹配不上时，先用 DFS 表达选择，再把 DFS 参数升级成 memo 和 DP 表。

题面触发词：

- “每一步有多个选择”
- “同一局面会重复出现”
- “表推顺序想不清”
- “想先拿部分分”

什么时候用：

- 题面不像标准背包/LCS/区间，但能写出递归枚举。
- 想从可运行的小数据暴力开始，逐步升级。

不要什么时候用：

- 状态图存在环且没有拓扑顺序或最短路性质。
- 递归深度可能到 `2e5` 且无法改迭代。
- DFS 参数没有包含完整历史信息。

复杂度：

- 暴力：选择数的指数级。
- 记忆化：不同状态数 * 每状态选择数。
- 表推：状态表大小 * 转移数。

数据范围参考：

- `n <= 20`：暴力或状压。
- 状态数 `<= 1e7` 且转移少：数组 memo/表推。
- 状态复杂且稀疏：`map<tuple<...>, ll>` 先保命。

依赖的标准容器：

- `map<tuple<...>, ll>`
- `vector<vector<ll>>`
- `vector<vector<int>> vis`

输入如何整理：

- 先把每一步的选择列出来。
- 再把“未来答案需要知道的东西”列为 DFS 参数。

接口：

```cpp
ll dfs(State s);
```

输出能力：

- 暴力小数据。
- 记忆化中档分。
- 表推满分或接近满分。

下游可接：

- 全部 DP 模型。

可拼接模块：

- BRUTE-07 记忆化总论
- BRUTE-09 `map<tuple,...>` 记忆化
- DP-18 优化 DP

## 升级图

```text
题面选择
  -> 写 dfs(当前进度, 资源, 必须记住的历史)
  -> 检查参数是否完整
  -> 加 memo：同参数直接返回
  -> 把 dfs 参数变成 dp 下标
  -> 把 dfs 终止条件变成初始化
  -> 把 dfs 枚举选择变成转移
  -> 找到依赖顺序后表推
```

## 什么时候可以直接加 memo

记忆化的判断口令：

```text
同样的 dfs 参数 -> 未来可选集合完全一样 -> 最优答案也完全一样。
```

如果同样的参数下，未来还会被“没放进参数里的历史”影响，就不能直接 memo，必须升维。常见漏掉的历史：

```text
last：上一次选了谁、上一步方向、上一个颜色。
used/mask：哪些点/物品已经用过。
path property：当前连续次数、是否已经触发过某个限制。
```

反例：

```text
dfs(i) 表示走到第 i 步的最好结果。
题目限制“不能连续向下走两步”。
如果不把 last_direction 放进参数，dfs(i) 不知道上一步是不是向下，后续选择集合不同，memo 会错。
正确状态应类似 dfs(i, last_direction)。
```

## 通用暴力 DFS 版本

```cpp
ll dfs(int i, int rest) {
    if (rest < 0) return -LINF;
    if (i == n + 1) return 0;

    ll ans = -LINF;
    ans = max(ans, dfs(i + 1, rest));                  // 不选
    ans = max(ans, val[i] + dfs(i + 1, rest - cost[i])); // 选
    return ans;
}
```

## 通用记忆化版本

```cpp
vector<vector<ll>> memo;
vector<vector<int>> vis;

ll dfs(int i, int rest) {
    if (rest < 0) return -LINF;
    if (i == n + 1) return 0;
    if (vis[i][rest]) return memo[i][rest];
    vis[i][rest] = 1;

    ll ans = -LINF;
    ans = max(ans, dfs(i + 1, rest));
    ans = max(ans, val[i] + dfs(i + 1, rest - cost[i]));
    return memo[i][rest] = ans;
}
```

## 通用表推版本

```cpp
vector<vector<ll>> dp(n + 2, vector<ll>(W + 1, -LINF));
for (int rest = 0; rest <= W; rest++) dp[n + 1][rest] = 0;

for (int i = n; i >= 1; i--) {
    for (int rest = 0; rest <= W; rest++) {
        dp[i][rest] = max(dp[i][rest], dp[i + 1][rest]);
        if (rest >= cost[i]) {
            dp[i][rest] = max(dp[i][rest], val[i] + dp[i + 1][rest - cost[i]]);
        }
    }
}

cout << dp[1][W] << '\n';
```

## 从 DFS 到表推的对照表

| DFS 元素 | 表推 DP 元素 |
|---|---|
| `dfs` 参数 | `dp` 下标 |
| 非法状态 | 不转移或设 `LINF/-LINF` |
| 结束状态 | 初始化 |
| 递归选择 | 状态转移 |
| 返回值 | `dp` 值 |
| 初始调用 | 答案位置 |

## `map<tuple>` 救场版本

```cpp
map<tuple<int,int,int>, ll> memo;

ll dfs(int i, int rest, int last) {
    if (rest < 0) return -LINF;
    if (i == n + 1) return 0;

    auto key = make_tuple(i, rest, last);
    if (memo.count(key)) return memo[key];

    ll ans = -LINF;
    // 按题意枚举选择
    return memo[key] = ans;
}
```

## 什么时候不改表推

```text
状态范围不清楚。
依赖顺序会绕回来。
只需要中档分，memo 已经过样例。
表推写法比 memo 更容易错。
```

常见坑：

- 记忆化先查 `memo` 再判非法，可能数组越界。
- `vis=1` 代表“算完”，不能用于有环状态的“正在算”。
- 表推初始化忘记对应 DFS 的结束状态。
- 最大值题非法返回 `0`，导致选非法方案。
- 改成滚动数组后循环方向错。

暴力/部分分替代：

- 用 `map<tuple>` 版本提交，哪怕慢，也比空着强。
- 大数据不会时，加简单特判：空集、全相同、容量为 0、`n=1`。

升级方向：

- 数组 memo 替换 `map<tuple>`。
- 二维表推替换递归。
- 滚动数组省空间。
- 用前缀和/树状数组/线段树/单调队列优化转移。

最小测试样例：

```text
3 5
cost: 2 3 4
val : 3 4 5
答案：7
```
