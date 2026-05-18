# BRUTE-00：部分分总策略

模块编号：BRUTE-00

模块名称：部分分总策略

标签：部分分、提交策略、考场节奏、先活下来

一句话用途：不会正解时，先写一个合法且能过小数据的版本，再逐步升级到剪枝、记忆化或正式算法。

题面触发词：

- 多个子任务 / 部分分 / 数据范围分档。
- `n <= 10`、`n <= 20`、`n <= 40`、`n <= 2000` 等明显分层。
- 正解想不清，但能枚举所有选择。
- 题目允许多次提交，且取最高分。

适用场景：

- 机考时间紧，每题先保证有分。
- 题面很长，正解模型一时匹配不上。
- 可以写出暴力、特判或小数据精确解。

什么时候用：

- 看到小数据子任务。
- 看到选择、排列、子集、路径、方案数等可以搜索的结构。
- 需要先提交一个可运行版本验证输入输出格式。

不要什么时候用：

- 输出格式还没确认。
- 题目是交互题或答案必须完全正确才给分。
- 暴力会在最小数据都跑不完。

复杂度：

| 版本 | 常见复杂度 | 能拿的数据 |
|---|---:|---|
| 合法兜底 | `O(1)` 或 `O(n)` | 格式分、特判分 |
| 暴力 DFS | `O(2^n)`、`O(n!)` | `n <= 10~25` |
| DFS + 剪枝 | 依剪枝而定 | 比暴力略大 |
| 记忆化搜索 | `O(状态数 * 转移数)` | 中档分，经常可过 |
| 正式算法 | 题目要求 | 冲满分 |

数据范围参考：

- `n <= 10`：全排列、指数搜索通常可试。
- `n <= 20`：子集枚举、状压、DFS + memo。
- `n <= 40`：折半枚举。
- `n <= 2000`：`O(n^2)` 可能可过。
- `n <= 2e5`：通常要 `O(n log n)` 或 `O(n)`，暴力只拿小数据。

依赖的标准容器：

- `vector`
- `string`
- `queue`
- `map`
- `unordered_map`
- `tuple`

输入如何整理：

把输入先整理成最容易枚举的标准容器：

- 序列：`vector<long long> a(n + 1)`，默认 1-index。
- 图：暂时用邻接表 `vector<vector<int>> g(n + 1)`。
- 状态：尽量变成若干个整数参数，例如 `i, rest, last, mask`。

接口：

```cpp
// 考场版本路线，不是固定函数。
// V0: legal_fallback()
// V1: brute_force()
// V2: brute_force_with_pruning()
// V3: memoized_search()
// V4: official_or_optimized_solution()
```

输出能力：

- 能输出合法格式。
- 能处理样例和小数据。
- 能在有时间时继续升级，不推翻前一版代码。

下游可接：

- BRUTE-06 回溯与剪枝。
- BRUTE-07 记忆化搜索总论。
- DP 卷的模型 DP。
- 图论卷的 BFS / Dijkstra / Topo。

可拼接模块：

- BRUTE-01 复杂度与数据范围速查。
- BRUTE-02 合法兜底输出。
- BRUTE-03 全排列枚举。
- BRUTE-04 组合/选不选 DFS。
- BRUTE-05 子集枚举。

模板代码：

注意：下面完整程序只是“先交小数据/部分分”的演示，以最大子集和为例。它只保证 `n <= 20` 的暴力分支是精确的；大数据分支输出兜底值，不代表正确答案，不能当作正解模板直接提交。

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int n;
const int MAXN = 200000 + 5;
static ll a[MAXN];

// V0: 题目允许任意合法解时使用。实际输出要按题意改。
void legal_fallback() {
    cout << 0 << '\n';
}

// V1: 小数据暴力，先保证思路和输入输出能跑。
ll brute_force() {
    if (n > 20) return 0; // 子集暴力只给小数据；大数据走合法兜底或优化版。
    ll ans = 0;
    // 示例：枚举子集，求最大子集和。实际题目把 sum/check 部分替换掉。
    for (int mask = 0; mask < (1 << n); mask++) {
        ll sum = 0;
        for (int i = 1; i <= n; i++) {
            if (mask & (1 << (i - 1))) sum += a[i];
        }
        ans = max(ans, sum);
    }
    return ans;
}

// V2/V3: 后续把 brute_force 里的递归改成剪枝或 memo。
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n;
    for (int i = 1; i <= n; i++) cin >> a[i];

    if (n == 0) {
        legal_fallback();
        return 0;
    }

    cout << brute_force() << '\n';
    return 0;
}
```

调用示例：

```cpp
// 第一次提交：只写 legal_fallback 或最小特判。
// 第二次提交：补 brute_force。
// 第三次提交：把 brute_force 中的 dfs 加 memo。
cout << brute_force() << '\n';
```

常见坑：

- 只顾写正解，最后一个版本都没提交。
- 小数据暴力忘记处理 `n = 0/1`。
- 输出格式错，导致合法兜底也没分。
- 多测时没有清空全局数组、memo、答案。
- 最大值题把初值设成 `0`，但答案可能是负数。

暴力/部分分替代：

- 不会做：先输出题目允许的最小合法值。
- 会枚举：写 `2^n` 或 `n!`。
- 会状态：把 DFS 参数变成 memo key。
- 会模型：再翻 DP / 图论 / 数据结构卷升级。

升级方向：

```text
合法输出 -> 特判 -> 暴力 DFS -> 剪枝 -> 记忆化搜索 -> 表推 DP/正解
```

最小测试样例：

```text
输入：
1
5

期望：
程序不崩溃，输出一行合法答案。
```
