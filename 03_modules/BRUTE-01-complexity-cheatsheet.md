# BRUTE-01：复杂度与数据范围速查

模块编号：BRUTE-01

模块名称：复杂度与数据范围速查

标签：复杂度、数据范围、算法选择、时间预算

一句话用途：用数据范围快速判断暴力、记忆化、折半或正式算法是否值得写。

题面触发词：

- `1 <= n <= ...`
- `T` 组数据。
- 时间限制 `1s/2s/3s`。
- 子任务中出现小范围。

适用场景：

- 写代码前判断版本能拿哪一档分。
- TLE 后判断是算法复杂度问题还是常数问题。
- 在暴力和记忆化之间做取舍。

什么时候用：

- 每道题读完输入范围后立刻用。
- 每次新增一层循环或一维状态时用。

不要什么时候用：

- 不要只看 `n`，还要看 `T`、边数 `m`、值域 `W`、状态转移数量。
- 不要把 `O(2^n)` 当作永远不能写，小数据子任务正是它的目标。

复杂度：

本模块本身无运行复杂度；用于估算其他模块。

数据范围参考：

| 估计操作数 | 通常可行性 |
|---:|---|
| `<= 1e6` | 很稳 |
| `1e7` | 通常可过 |
| `1e8` | C++ 勉强，常数要小 |
| `> 1e8` | 大概率 TLE |

| 数据范围 | 常见可用方案 |
|---:|---|
| `n <= 10` | `n!`、复杂回溯 |
| `n <= 20` | `2^n`、状压、子集枚举 |
| `n <= 25` | DFS + 剪枝 / memo |
| `n <= 40` | 折半枚举 `2^(n/2)` |
| `n <= 300` | `O(n^3)` |
| `n <= 3000` | `O(n^2)` |
| `n <= 2e5` | `O(n log n)` 或 `O(n)` |

依赖的标准容器：

- 无强依赖。
- 估算状态时常配合 `vector`、`map`、`unordered_map`。

输入如何整理：

先在草稿纸上列出：

```text
n =
m =
T =
值域/容量 W =
状态维度 =
每个状态转移数 =
```

接口：

```cpp
// 估算总操作数：状态数 * 每状态转移数 * 测试组数。
__int128 estimate_ops(long long states, long long transitions, long long T) {
    return (__int128)states * transitions * T;
}
```

输出能力：

- 判断某个版本是否适合提交。
- 确定优先写暴力、memo、折半还是换模型。

下游可接：

- 所有 BRUTE 模块。
- DP 卷的数据范围路由。
- 图论卷的最短路、连通性、拓扑模块。

可拼接模块：

- BRUTE-00 部分分总策略。
- BRUTE-07 记忆化搜索总论。
- BRUTE-12 折半枚举。

模板代码：

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

string judge_ops(long double ops) {
    if (ops <= 1e6) return "very_safe";
    if (ops <= 1e7) return "safe";
    if (ops <= 1e8) return "maybe";
    return "danger";
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    ll states, transitions, T;
    cin >> states >> transitions >> T;
    long double ops = (long double)states * transitions * T;
    cout << judge_ops(ops) << '\n';
    return 0;
}
```

调用示例：

```cpp
// 0/1 背包 memo: n * W 个状态，每个状态 2 个转移。
long double ops = (long double)n * W * 2;
if (ops <= 1e8) {
    // vector memo 可以尝试
}
```

常见坑：

- 忘记乘 `T`。
- 忘记每个状态还要枚举 `k` 或邻接边。
- `map` / `unordered_map` 常数比数组大很多。
- `2^25` 看起来不大，但转移复杂时会爆。
- 递归深度和内存也要算，不只算时间。

暴力/部分分替代：

- 若 `n <= 20` 子任务存在，先写子集或 DFS。
- 若 `n <= 40`，优先考虑折半。
- 若 `n * W` 可承受，优先写 vector memo。
- 若状态不清晰，用 `map<tuple,...>` 先拿中档。

升级方向：

- `O(n!)` -> 回溯剪枝 / 状压 DP。
- `O(2^n)` -> 折半 / 状压 DP / 记忆化。
- `O(n^3)` -> 前缀和 / 单调队列 / 数据结构优化。
- `map memo` -> `vector memo` 或编码 `unordered_map`。

最小测试样例：

```text
输入：
1000 1000 1

输出：
very_safe
```
