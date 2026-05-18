# BRUTE-07：记忆化搜索总论

模块编号：BRUTE-07

模块名称：记忆化搜索总论

标签：记忆化、DFS、状态、DP 入口、核心章节

一句话用途：把暴力 DFS 中重复计算的相同状态缓存起来，用最小改动得到中档甚至满分版本。

题面触发词：

- 每一步有选择。
- 暴力 DFS 能写出来。
- 同一个局面会从不同路径到达。
- 表推 DP 循环顺序想不清。
- `n * W`、`mask * last`、`pos * tight * state` 等状态数可估算。

适用场景：

- 背包、区间、树、DAG、数位、状压等 DP 的递归写法。
- 递归参数能完整描述后续问题。
- 状态总数远小于搜索树节点数。

什么时候用：

- 已经能写出 `dfs(...)`。
- `dfs` 的返回值只由参数决定。
- 相同参数组合会重复出现。
- 状态数量可承受。

不要什么时候用：

- `dfs` 返回值依赖没有写进参数的全局变量。
- 相同参数下，后续答案还会因为路径不同而不同。
- 状态有环且没有环检测。
- 状态几乎不重复，memo 只会增加常数。
- 递归深度可能爆栈且无法改写。

复杂度：

```text
记忆化复杂度 = 状态数 * 每个状态的转移数
空间复杂度 = 状态数
```

数据范围参考：

- `n * W <= 1e7`：数组/vector memo 可尝试。
- 状态数量 `<= 1e5~1e6`：`map<tuple>` 可作为稳妥版。
- 状态数量较多且能安全编码：`unordered_map`。
- `mask` 状态通常要求 `n <= 20`。

依赖的标准容器：

- `vector`
- `map`
- `unordered_map`
- `tuple`

输入如何整理：

- 把 DFS 参数尽量整理成整数：`i, rest, last, mask, cnt`。
- 若参数有负数，用 OFFSET 平移，或改用 `map<tuple,...>`。
- 若参数是集合，用 `mask` 表示。

接口：

```cpp
// 固定句式：
// dfs(状态参数) 返回：从这个状态继续走，能得到的答案。
long long dfs(int i, int rest);
```

输出能力：

- 最大值。
- 最小值。
- 方案数。
- 可行性。
- 也可保存选择用于还原方案。

下游可接：

- DP 卷：把 DFS 参数变成 DP 下标。
- BRUTE-08 vector memo。
- BRUTE-09 map<tuple> memo。
- BRUTE-10 unordered_map 编码 memo。

可拼接模块：

- BRUTE-04 组合 DFS。
- BRUTE-05 子集枚举。
- BRUTE-06 回溯剪枝。
- BRUTE-15 常见坑。

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
    if (rest < 0) return -LINF;       // 1. 先判非法，防止数组越界
    if (i == n + 1) return 0;         // 2. 再判终止

    if (vis[i][rest]) return memo[i][rest]; // 3. 查缓存
    vis[i][rest] = 1;

    ll ans = -LINF;
    ans = max(ans, dfs(i + 1, rest)); // 不选
    if (cost[i] <= rest) {
        ans = max(ans, value[i] + dfs(i + 1, rest - cost[i])); // 选
    }

    return memo[i][rest] = ans;       // 4. 存缓存
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
// 暴力版本：
// ll dfs(int i, int rest);
// 记忆化版本只加三件事：
// 1. memo/vis 容器
// 2. if (vis[state]) return memo[state]
// 3. return memo[state] = ans
cout << dfs(1, W) << '\n';
```

状态能否缓存判断：

```text
1. dfs 参数是什么？
2. dfs 返回值是什么？
3. 给定这些参数后，未来答案是否唯一？
4. 是否还依赖当前路径、已选集合、上一个元素、剩余次数、颜色、方向？
5. 如果依赖，把它加入参数；如果无法加入，不要缓存。
```

可缓存例子：

```text
dfs(i, rest) = 从第 i 个物品开始，剩余容量 rest 的最大价值。
给定 i 和 rest 后，前面怎么选不影响后面，所以可缓存。
```

不可缓存例子：

```text
dfs(i, sum) 里还用全局 vector<int> chosen 判断相邻冲突。
如果 chosen 没有进入参数，相同 i 和 sum 可能有不同后续，不能缓存。
```

返回值四件套：

```text
最大值：ans = -LINF；非法返回 -LINF；转移用 max。
最小值：ans = LINF；非法返回 LINF；转移用 min。
方案数：ans = 0；成功边界返回 1；非法返回 0；转移用加法取模。
可行性：ans = false；成功边界返回 true；非法返回 false；转移用 ||。
```

有环状态风险：

普通记忆化默认状态依赖是无环的。如果 `dfs(a)` 可能还没算完又调用回 `dfs(a)`，只用 `vis` 会出错。

```cpp
// 0 = 未访问，1 = 正在访问，2 = 已完成
vector<int> color;

bool dfs_cycle(int u) {
    if (color[u] == 1) return false; // 发现环，按题意处理
    if (color[u] == 2) return true;
    color[u] = 1;
    // for (int v : g[u]) if (!dfs_cycle(v)) return false;
    color[u] = 2;
    return true;
}
```

常见坑：

- 非法状态晚于 memo 查询，导致数组下标越界。
- 漏掉 `last`、`mask`、`cnt` 等影响未来的参数。
- 多测不清空 memo。
- 最大值题初始化为 `0`，全负数时错。
- 计数题忘记取模。
- 有环状态直接递归，死循环。
- `vis=1` 表示“算完”，不要在状态仍在计算中就当成答案可用。

暴力/部分分替代：

- 没有重复状态：保留 DFS + 剪枝。
- 状态范围不清：先用 `map<tuple,...>`。
- 状态范围清楚：换 `vector`。
- 表推顺序不会：保留记忆化提交。

升级方向：

```text
暴力 DFS -> 记忆化 DFS -> 表推 DP -> 滚动数组/数据结构优化
```

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
