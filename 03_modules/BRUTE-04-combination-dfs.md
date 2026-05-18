# BRUTE-04：组合 / 选不选 DFS

模块编号：BRUTE-04

模块名称：组合 / 选不选 DFS

标签：组合、DFS、选不选、搜索树、子序列

一句话用途：每个元素只考虑选或不选，枚举所有组合或满足限制的选择集合。

题面触发词：

- 选若干个。
- 每个物品最多选一次。
- 从 `n` 个中选 `k` 个。
- 容量、预算、代价限制。
- `n <= 20/30`。

适用场景：

- 枚举所有子集。
- 枚举大小为 `k` 的组合。
- 0/1 背包小数据暴力。
- 需要保留当前选择路径。

什么时候用：

- 顺序不重要，只关心选了哪些元素。
- 每个元素最多一次。
- 可以根据剩余数量或当前代价剪枝。

不要什么时候用：

- 元素可以无限次选，应转完全背包或递归枚举次数。
- 顺序有意义，应使用排列或序列 DFS。
- `n` 很大且没有剪枝或 memo。

复杂度：

- 选/不选：`O(2^n)`。
- 选 `k` 个：`O(C(n,k))`。
- 递归空间：`O(n)`。

数据范围参考：

- `n <= 25`：常见可尝试。
- `n <= 40`：考虑折半枚举。
- `n * W` 较小：考虑记忆化或背包 DP。

依赖的标准容器：

- `vector`

输入如何整理：

- 物品属性用 1-index：`cost[i]`、`value[i]`。
- 当前选择可用 `vector<int> chosen`。

接口：

```cpp
void dfs(int i, long long sum);
```

输出能力：

- 最大值 / 最小值。
- 方案计数。
- 输出一个合法组合。
- 精确枚举所有组合。

下游可接：

- BRUTE-06 回溯与剪枝。
- BRUTE-07 记忆化搜索。
- DP 卷 0/1 背包。

可拼接模块：

- BRUTE-01 复杂度速查。
- BRUTE-08 vector memo。
- BRUTE-12 折半枚举。

模板代码：

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

const ll LINF = (1LL << 62);
int n, k;
vector<ll> a;
vector<int> chosen;
ll best = -LINF; // 如果必须选 k 个，允许所有数都为负

void dfs_choose_k(int i, ll sum) {
    if ((int)chosen.size() == k) {
        best = max(best, sum);
        return;
    }
    if (i == n + 1) return;

    int need = k - (int)chosen.size();
    int left = n - i + 1;
    if (left < need) return;

    chosen.push_back(i);
    dfs_choose_k(i + 1, sum + a[i]);
    chosen.pop_back();

    dfs_choose_k(i + 1, sum);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n >> k;
    a.assign(n + 1, 0);
    for (int i = 1; i <= n; i++) cin >> a[i];

    if (k < 0 || k > n) {
        cout << "-1\n";
        return 0;
    }

    dfs_choose_k(1, 0);
    cout << best << '\n';
    return 0;
}
```

调用示例：

```cpp
// 从第 1 个元素开始枚举，当前和为 0。
dfs_choose_k(1, 0);
```

常见坑：

- `chosen.push_back` 后忘记 `pop_back`。
- 结束条件顺序错，导致选满 `k` 后还继续递归。
- `left < need` 剪枝写错，漏答案。
- 组合不关心顺序，不要在递归里从头重新枚举。

暴力/部分分替代：

- `n <= 25`：直接选/不选。
- `n <= 40`：折半枚举两边结果再合并。
- 容量 `W` 小：改成 `dfs(i, rest)` + memo 或背包 DP。

升级方向：

- 组合 DFS -> 加上下界/上界剪枝。
- 组合 DFS -> 记忆化 `dfs(i, rest)`。
- 组合 DFS -> 0/1 背包表推。

最小测试样例：

```text
输入：
4 2
1 5 3 2

输出：
8
```
