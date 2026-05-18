# BRUTE-09：map<tuple,...> 记忆化

模块编号：BRUTE-09

模块名称：`map<tuple,...>` 记忆化

标签：map、tuple、通用 memo、稳妥版

一句话用途：状态维度复杂或范围不清时，用 `map<tuple<...>, value>` 快速写出不容易错的记忆化。

题面触发词：

- 状态里有多个整数。
- 某些参数可能为负数。
- 状态范围不好开数组。
- 先追求写对，不追求极限速度。

适用场景：

- `dfs(i, rest, last)`。
- `dfs(pos, balance, tight)`。
- `dfs(u, parent_state, used)`。
- 临场从暴力改 memo。

什么时候用：

- 不确定每维最大值。
- 想避免手写哈希和编码冲突。
- 状态数量中等。

不要什么时候用：

- 状态数极大，`map` 常数会导致 TLE。
- key 中含大对象，例如整个 `vector`，除非只是小数据部分分。
- 状态范围清楚且需要速度，应该用 vector。

复杂度：

- 每次查询/写入：`O(log 状态数)`。
- 总时间：`O(状态数 * 转移数 * log 状态数)`。
- 空间：`O(状态数)`。

数据范围参考：

- `1e5` 级状态通常可用。
- `1e6` 级状态要谨慎，可能慢。
- 适合“先交中档”的稳妥版本。

依赖的标准容器：

- `map`
- `tuple`
- `vector`

输入如何整理：

- DFS 参数尽量用 `int` / `long long`。
- key 的字段顺序和 DFS 参数顺序保持一致。
- 如果状态字段是 bool，也可以直接放进 tuple。

接口：

```cpp
map<tuple<int,int,int>, long long> memo;
long long dfs(int i, int rest, int last);
```

输出能力：

- 最大值 / 最小值 / 计数 / 可行性。
- 可处理负数状态和稀疏状态。

下游可接：

- BRUTE-10 unordered_map 编码 memo。
- DP 卷表推转换。

可拼接模块：

- BRUTE-07 记忆化搜索总论。
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
map<tuple<int, int, int>, ll> memo;

// last: 上一个选择的物品编号，0 表示还没选。
ll dfs(int i, int rest, int last) {
    if (rest < 0) return -LINF;
    if (i == n + 1) return 0;

    auto key = make_tuple(i, rest, last);
    auto it = memo.find(key);
    if (it != memo.end()) return it->second;

    ll ans = dfs(i + 1, rest, last);
    if (last == 0 || i - last >= 2) {
        ans = max(ans, value[i] + dfs(i + 1, rest - cost[i], i));
    }

    memo[key] = ans;
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n >> W;
    cost.assign(n + 1, 0);
    value.assign(n + 1, 0);
    for (int i = 1; i <= n; i++) cin >> cost[i] >> value[i];

    cout << dfs(1, W, 0) << '\n';
    return 0;
}
```

调用示例：

```cpp
memo.clear();
ll ans = dfs(1, W, 0);
```

常见坑：

- 用 `memo[key]` 判断是否存在，会把不存在的 key 插入进去。
- 多测没有 `memo.clear()`。
- key 漏字段，导致错误缓存。
- `map` 过慢时要改 vector 或 unordered_map。
- `tuple` 字段类型不一致，例如把 `long long` 强塞成 `int` 溢出。

暴力/部分分替代：

- 先写 `map<tuple>`，不必一开始想编码。
- 若 TLE，再看每维范围，改成 vector 或编码。
- 若状态数很小，`map` 就是最终版本。

升级方向：

- `map<tuple>` -> `unordered_map<long long, value>`。
- `map<tuple>` -> 多维 vector。
- `dfs` -> 表推 DP。

最小测试样例：

```text
输入：
3 5
2 5
2 6
3 7

输出：
12
```

