# DP-25：两道例题的暴力 DFS 到记忆化搜索

模块编号：DP-25

模块名称：两道例题的暴力 DFS 到记忆化搜索

标签：DP、记忆化搜索、暴力升级、P1874、编辑距离、自顶向下

一句话用途：如果考场上没能直接推导出递推 DP，就先写最自然的暴力 DFS，再把 DFS 的可变参数变成 memo 下标，快速拿到部分分甚至满分。

题面触发词：

- “我能递归枚举所有选择，但复杂度爆炸”
- “同一个位置/同一组参数会被反复算”
- “字符串切分、双序列匹配、选或不选、区间递归”
- “求最大/最小/方案数/是否可行”
- “DP 方程一时想不出来”

什么时候用：

- 暴力 DFS 很容易按题意写出来。
- DFS 的参数个数较少，且每个参数范围能估算。
- 同样的参数代表同一个子问题，答案不依赖“怎么走到这里”。
- 递归深度不大，或至少不会明显到 `1e5` 以上。

不要什么时候用：

- 状态有环且没有处理“正在访问”的标记，容易递归死循环。
- DFS 参数漏掉了影响未来的全局变量，例如 `used[]`、`last`、`path`。
- 状态数量远超内存，数组 memo 开不下且哈希也会太慢。
- 递归深度极深，例如链状 `n=5e5`，可能爆栈。

复杂度：

- 纯暴力：通常是指数级，例如 `2^n` 或 `3^n`。
- 记忆化搜索：约等于 `状态数 * 每个状态的转移数`。
- P1874 快速求和：约 `O(len^2 * target)`。
- 编辑距离：`O(nm)`。

数据范围信号：

- P1874：`len <= 40`、`target <= 1e5`，`memo[pos][sum]` 可开。
- 编辑距离：`n,m <= 2000`，`memo[i][j]` 可开。
- 一般题：先估 `状态总数`，超过 `1e7` 要谨慎，超过 `1e8` 通常危险。

依赖的标准容器：

- `vector<vector<int>> memo`
- `vector<vector<char>> vis`
- `string`
- `tuple/map/unordered_map`：状态稀疏或参数不好做下标时备用。

输入如何整理：

- 把不变的输入放成全局或传引用：字符串、数组、目标值。
- DFS 参数只放“会变化且决定未来”的量。
- 先写清楚一句话：`dfs(...)` 返回什么。

接口：

```text
暴力 dfs(可变参数) -> 加 memo/vis -> 每个状态只算一次
```

输出能力：

- 最小代价。
- 最大收益。
- 方案数。
- 是否可行。
- 小数据精确解和中数据记忆化部分分。

下游可接：

- DP-03 DFS -> 记忆化 -> 表推升级图
- DP-21 P1874 快速求和
- DP-22 编辑距离
- BRUTE-07/08/09 记忆化搜索实现

可拼接模块：

- `vector` memo：参数范围小且整数下标。
- `map<tuple<...>, int>`：状态复杂但求稳。
- `unordered_map<long long, int>`：状态稀疏且能编码。

## 1. 考场口令

```text
先写暴力 DFS。
看 DFS 函数参数。
去掉全局不变参数。
剩下的可变参数就是状态。
同样状态答案相同，就加 memo。
```

要特别问自己一句：

```text
同样的 dfs 参数，未来答案是不是永远一样？
```

如果答案是“是”，就可以记忆化。

注意：表推 DP 和记忆化 DFS 可能访问同一批“位置+约束”状态，但 `dp` 值的含义不一定完全一样。

| 题目 | 表推含义 | 记忆化含义 |
|---|---|---|
| P1874 快速求和 | `dp[i][sum]`：前 `i` 个字符已经切完且和为 `sum` 的最少已用加号数 | `dfs(pos,sum)`：已经处理到 `pos`、当前和为 `sum`，后面最少还要多少加号 |
| 编辑距离 | `dp[i][j]`：`A` 前 `i` 个字符变成 `B` 前 `j` 个字符的最少操作数 | `dfs(i,j)`：从 `A[i..]` 变成 `B[j..]` 的最少后续操作数 |

考场记法：状态维度相同代表可以互相启发；值的方向要按函数定义重新写清楚。

## 2. P1874 快速求和：记忆化 DFS 完整代码

定义：

```text
dfs(pos, sum) = 已经处理到 s[pos]，前面数字段总和为 sum 时，从 pos 往后凑到 target 还需要的最少加号数。
```

注意第一段前面没有加号，所以选择一段 `s[pos..end]` 后，新增加号数是：

```cpp
int add = (pos == 0 ? 0 : 1);
```

完整 C++17：

```cpp
#include <bits/stdc++.h>
using namespace std;

const int INF = 1000000000;

string s;
int target_value;
int len;
vector<vector<int>> memo;
vector<vector<char>> vis;

int dfs_fast_sum(int pos, int sum) {
    if (sum > target_value) return INF;
    if (pos == len) {
        return sum == target_value ? 0 : INF;
    }

    if (vis[pos][sum]) return memo[pos][sum];
    vis[pos][sum] = 1;

    int ans = INF;
    long long val = 0;
    for (int end = pos; end < len; end++) {
        val = val * 10 + (s[end] - '0');
        if (sum + val > target_value) break;

        int add = (pos == 0 ? 0 : 1);
        int got = dfs_fast_sum(end + 1, (int)(sum + val));
        if (got != INF) {
            ans = min(ans, add + got);
        }
    }

    memo[pos][sum] = ans;
    return ans;
}

int solve_fast_sum_memo(const string& input, int target) {
    s = input;
    target_value = target;
    len = (int)s.size();
    memo.assign(len + 1, vector<int>(target_value + 1, INF));
    vis.assign(len + 1, vector<char>(target_value + 1, 0));

    int ans = dfs_fast_sum(0, 0);
    return ans == INF ? -1 : ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string input;
    int target;
    cin >> input >> target;

    cout << solve_fast_sum_memo(input, target) << '\n';
    return 0;
}
```

为什么复杂度降下来：

```text
纯 DFS 会反复进入相同的 (pos, sum)。
加 memo 后，每个 (pos, sum) 只算一次。
每个状态枚举后面一段的 end，最多 len 次。
所以约 O(len * target * len)。
```

这道题的递归深度最多 `len <= 40`，不用担心爆栈。

## 3. 编辑距离：记忆化 DFS 完整代码

定义：

```text
dfs(i, j) = 把 a 从 i 开始的后缀变成 b 从 j 开始的后缀，最少需要多少次操作。
```

如果 `a[i] == b[j]`，当前字符不用动，直接进入 `dfs(i+1,j+1)`。

如果不同，有三种选择：

```text
删除 a[i]：dfs(i+1, j) + 1
插入 b[j]：dfs(i, j+1) + 1
替换 a[i]：dfs(i+1, j+1) + 1
```

完整 C++17：

```cpp
#include <bits/stdc++.h>
using namespace std;

string a, b;
int n, m;
vector<vector<int>> memo;
vector<vector<char>> vis;

int dfs_edit_distance(int i, int j) {
    if (i == n) return m - j;
    if (j == m) return n - i;

    if (vis[i][j]) return memo[i][j];
    vis[i][j] = 1;

    int ans;
    if (a[i] == b[j]) {
        ans = dfs_edit_distance(i + 1, j + 1);
    } else {
        int del_cost = dfs_edit_distance(i + 1, j) + 1;
        int ins_cost = dfs_edit_distance(i, j + 1) + 1;
        int rep_cost = dfs_edit_distance(i + 1, j + 1) + 1;
        ans = min({del_cost, ins_cost, rep_cost});
    }

    memo[i][j] = ans;
    return ans;
}

int solve_edit_distance_memo(const string& x, const string& y) {
    a = x;
    b = y;
    n = (int)a.size();
    m = (int)b.size();
    memo.assign(n + 1, vector<int>(m + 1, 0));
    vis.assign(n + 1, vector<char>(m + 1, 0));
    return dfs_edit_distance(0, 0);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string x, y;
    cin >> x >> y;

    cout << solve_edit_distance_memo(x, y) << '\n';
    return 0;
}
```

为什么复杂度降下来：

```text
纯 DFS 每次最多分出 3 个分支，复杂度接近指数级。
加 memo 后，状态只有 (i,j)，总数约 n*m。
每个状态 O(1) 转移，所以 O(nm)。
```

本题 `n,m <= 2000`，递归深度大约 `n+m <= 4000`，通常安全。

## 4. 什么时候记忆化能直接满分

满足这四条，记忆化搜索经常和表推 DP 一样强：

```text
1. 状态没有环，或者递归天然走向更小/更后的状态。
2. 状态数能承受。
3. 每个状态转移不太多。
4. 递归深度不爆栈。
```

P1874 和编辑距离都满足：

| 题目 | 状态 | 递归方向 | 状态数 | 结果 |
|---|---|---|---|---|
| P1874 | `(pos,sum)` | `pos` 变大 | `len * target` | 可满分 |
| 编辑距离 | `(i,j)` | `i/j` 变大 | `n * m` | 可满分 |

## 5. 什么时候只能拿部分分

记忆化不一定总是满分，但仍然很值得写：

- 状态范围大，但实际访问状态少，用 `map/unordered_map` 可拿中档分。
- 转移很多，状态数乘转移数仍偏大，但比纯暴力好很多。
- 状态漏了一些信息，先补全状态可能会变大，但小数据仍可过。
- 递归深度太深时可能 RE，要准备表推或迭代版。

## 6. 数组 memo 与 map memo 的选择

优先级：

```text
参数范围小、连续整数 -> vector/数组
状态是 tuple 且范围不清 -> map
状态稀疏且能编码成 long long -> unordered_map
```

复杂状态求稳模板：

```cpp
#include <bits/stdc++.h>
using namespace std;

map<tuple<int, int, int>, int> memo;

int dfs(int i, int sum, int last) {
    auto key = make_tuple(i, sum, last);
    auto it = memo.find(key);
    if (it != memo.end()) return it->second;

    int ans = 0;
    // 在这里枚举选择，更新 ans。

    memo[key] = ans;
    return ans;
}
```

## 7. 考场策略总结

```text
第一步：写最直白 DFS，不要一开始硬想 for 循环 DP。
第二步：把函数参数写成一句状态定义。
第三步：删掉不变参数，留下决定未来的参数。
第四步：估算状态数，能开数组就开数组。
第五步：先判非法和终止，确认下标合法后查 memo，在返回前写 memo。
第六步：样例过后交一版，后面再考虑表推、滚动数组或数据结构优化。
```

关键判断：

```text
如果同一个 dfs 参数再次出现，答案完全一样，就能 memo。
如果答案还依赖 used/path/last/当前方向，这些也必须进状态。
```

常见坑：

- 用 `-1` 表示没算过，但合法答案也可能是 `-1`；稳妥用 `vis`。
- base case 放在查 memo 后面，导致空状态访问越界；正确顺序通常是先判非法/终止，再查 memo。
- 参数漏信息，例如只写 `dfs(pos)`，但其实还依赖 `sum` 或 `last`。
- `sum` 可能超过目标，没剪枝导致数组越界。
- 多组数据忘记清空 `memo/vis`。
- 递归深度很深时爆栈。

暴力/部分分替代：

- 完全不会 DP：先交纯 DFS 小数据版。
- DFS 会重复：加 memo。
- 递归深度危险：把 memo DFS 改成表推。
- 状态太大：删掉无关历史，或只用 `map` 存实际访问状态。

升级方向：

```text
纯 DFS -> DFS + memo -> 表推 DP -> 滚动数组/数据结构优化
```

最小测试样例：

```text
P1874:
99999
45
输出：4

编辑距离:
sfdqxbw
gfdgw
输出：4
```
