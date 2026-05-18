# BRUTE-03：全排列枚举

模块编号：BRUTE-03

模块名称：全排列枚举

标签：排列、DFS、next_permutation、暴力

一句话用途：当题目要求尝试所有顺序时，枚举 `1..n` 或给定数组的所有排列。

题面触发词：

- 排列顺序。
- 访问顺序。
- 安排任务顺序。
- 每个元素恰好用一次。
- `n <= 8/10/11`。

适用场景：

- 需要枚举所有访问顺序。
- TSP 小数据。
- 调度、排列计分、暴力找最优顺序。

什么时候用：

- `n <= 10` 且每个排列检查较快。
- 题目显式要求每个元素用一次。
- 可以通过剪枝提前停止无效排列。

不要什么时候用：

- `n >= 12` 且无强剪枝。
- 元素可重复选择，这时是 DFS 选序列，不是排列。
- 只关心集合不关心顺序，应改用组合或子集。

复杂度：

- `O(n! * check_cost)`。
- DFS 版本空间 `O(n)`。

数据范围参考：

- `n <= 9`：通常稳。
- `n = 10/11`：看 `check_cost` 和时限。
- `n >= 12`：只适合部分分或强剪枝。

依赖的标准容器：

- `algorithm`

输入如何整理：

- 若是 `1..n`，用静态数组 `p[1..n]` 存。
- 若是给定数组，先排序再 `next_permutation`，可自动避免重复排列。

接口：

```cpp
ll solve_by_next_permutation();
```

输出能力：

- 最大/最小排列得分。
- 找到任意满足条件的排列。
- 统计满足条件的排列数。

下游可接：

- BRUTE-06 回溯与剪枝。
- BRUTE-07 记忆化搜索总论。
- 状压 DP。

可拼接模块：

- BRUTE-01 复杂度速查。
- BRUTE-14 提交版本路线。

模板代码：

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const ll LINF = (1LL << 60);

int n;
const int MAXN = 12 + 5;
int p[MAXN];

ll score_permutation() {
    ll score = 0;
    for (int i = 1; i <= n; i++) {
        score += 1LL * i * p[i];
    }
    return score;
}

ll solve_by_next_permutation() {
    sort(p + 1, p + n + 1);
    ll best = -LINF;
    do {
        best = max(best, score_permutation());
    } while (next_permutation(p + 1, p + n + 1));
    return best;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n;
    for (int i = 1; i <= n; i++) cin >> p[i];
    cout << solve_by_next_permutation() << '\n';
    return 0;
}
```

调用示例：

```cpp
int p[4] = {0, 1, 2, 3}; // p[1..3]
sort(p + 1, p + 4);
do {
    // check p
} while (next_permutation(p + 1, p + 4));
```

常见坑：

- 忘记先 `sort`，导致漏掉字典序前面的排列。
- 给定数组有重复元素时，手写 DFS 可能重复枚举；`next_permutation` 更省心。
- `n!` 爆炸，别对 `n = 15` 硬跑。
- 最大值初值不能随便设成 `0`。

暴力/部分分替代：

- `n <= 10`：全排列直接交。
- `n > 10`：只处理小数据，或加剪枝，或换状压/贪心/DP。

升级方向：

- 全排列 -> 回溯剪枝。
- 全排列 -> 状压 DP：`dp[mask][last]`。
- 全排列 -> BFS 状态搜索：最少交换次数等问题。

最小测试样例：

```text
输入：
3
1 2 3

输出：
14
```
