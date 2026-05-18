# BRUTE-06：回溯与剪枝

模块编号：BRUTE-06

模块名称：回溯与剪枝

标签：DFS、回溯、剪枝、搜索优化

一句话用途：在枚举选择时及时撤销现场，并用明显不可能更优的条件提前返回。

题面触发词：

- 搜索所有方案。
- 选若干个满足限制。
- 最大/最小答案。
- 字典序方案。
- `n` 小但纯暴力可能超时。

适用场景：

- 需要维护当前路径。
- 每一步做选择，递归返回后要恢复。
- 可以估计“当前分支最多/最少还能达到什么”。

什么时候用：

- DFS 已经能写，但跑得慢。
- 有容量、数量、剩余收益、排序后上界等限制。
- 题目要求找任意方案，找到后可以停止。

不要什么时候用：

- 分支之间存在大量重复状态，此时优先 memo。
- 剪枝条件不确定正确性，可能剪掉答案。
- 状态是图最短步数，通常 BFS 更稳。

复杂度：

- 最坏仍可能是指数级。
- 实际复杂度依赖剪枝强度。
- 空间通常为递归深度 `O(n)`。

数据范围参考：

- `n <= 25`：DFS + 剪枝常可作为部分分。
- `n <= 40`：若无强剪枝，优先折半。
- 分支因子小、限制强时，可以处理更大数据。

依赖的标准容器：

- `vector`
- `algorithm`

输入如何整理：

- 把物品按“更容易剪枝”的顺序排序，例如价值大、代价小、候选少的先枚举。
- 预处理后缀上界，例如 `suffix_sum[i]` 表示从 `i..n` 全选最多还能加多少。

接口：

```cpp
void dfs(int i, long long current_value, long long current_cost);
```

输出能力：

- 最大值 / 最小值。
- 任意可行方案。
- 方案计数。

下游可接：

- BRUTE-07 记忆化搜索。
- BRUTE-12 折半枚举。
- DP 卷背包/状压 DP。

可拼接模块：

- BRUTE-03 全排列枚举。
- BRUTE-04 组合 DFS。
- BRUTE-05 子集枚举。

模板代码：

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int n;
ll W;
vector<ll> cost, value, suffix_value;
ll best = 0;

void dfs(int i, ll used, ll got) {
    if (used > W) return; // 可行性剪枝
    if (i == n + 1) {
        best = max(best, got);
        return;
    }

    // 最优性剪枝：即使后面全选也不可能超过当前 best。
    if (got + suffix_value[i] <= best) return;

    // 优先尝试价值大的选择，有时能更早提高 best。
    dfs(i + 1, used + cost[i], got + value[i]);
    dfs(i + 1, used, got);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n >> W;
    cost.assign(n + 1, 0);
    value.assign(n + 2, 0);
    for (int i = 1; i <= n; i++) cin >> cost[i] >> value[i];

    suffix_value.assign(n + 3, 0);
    for (int i = n; i >= 1; i--) {
        suffix_value[i] = suffix_value[i + 1] + max(0LL, value[i]);
    }

    dfs(1, 0, 0);
    cout << best << '\n';
    return 0;
}
```

调用示例：

```cpp
best = 0;
dfs(1, 0, 0);
cout << best << '\n';
```

常见坑：

- 修改 `chosen`、`used`、`cnt` 后没有恢复。
- 剪枝条件用了估计下界/上界但方向写反。
- 用 `got + suffix_value[i] <= best` 时，`suffix_value` 必须真的是乐观上界。
- 找任意方案时，递归返回后没有停止，导致输出被覆盖。
- 多测时 `best` 和路径没有清空。

暴力/部分分替代：

- 先写不剪枝 DFS。
- 再加可行性剪枝：超容量、数量不够、越界。
- 再加最优性剪枝：后面全选也不可能更优。
- 仍慢时考虑 memo 或折半。

升级方向：

- 回溯 -> 记忆化 `dfs(i, rest)`。
- 回溯 -> 0/1 背包。
- 回溯 -> 分支限界 / A*，低优先级。

最小测试样例：

```text
输入：
3 5
3 10
4 20
2 8

输出：
20
```

