# DP-21：P1874 快速求和建模例题

模块编号：DP-21

模块名称：从暴力切分到 DP 建模：P1874 快速求和

标签：DP、建模过程、字符串切分、最小加号数、暴力到表推

一句话用途：用一道完整例题演示“为什么这样定义状态”，帮助初学者从暴力搜索自然推到 DP。

题面触发词：

- 数字字符串中插入加号。
- 让表达式结果等于目标数。
- 求最少加号数量。
- 字符串长度不大但所有切法是指数级。
- 前导零不影响数字大小。

什么时候用：

- 题目是在序列/字符串中切分若干段，并让段值的和、代价或方案数满足目标。
- 暴力枚举每个空隙切或不切，复杂度是 `2^(len-1)`。
- 后续是否能成功只取决于“处理到的位置”和“当前累计值”，不关心前面具体怎么切。

不要什么时候用：

- 段值可以为负，或后续操作能让和变小，此时 `sum > target` 不能直接剪枝。
- 目标值很大到 `dp[len][target]` 开不下，需要改记忆化搜索、map 状态或其他优化。
- 每一段的贡献不只是段值，还依赖前一段形态，此时需要额外状态，例如 `last`。

复杂度：

- 状态数：`O(len * target)`。
- 转移：枚举下一段，整体约 `O(len^2 * target)`。
- 本题 `len <= 40`、`target <= 1e5`，约 `1.6e8` 级别简单整数操作，C++ 可接受。
- 空间：`(len + 1) * (target + 1)` 个 `int`，约 16MB。

依赖的标准容器：

- `string`：数字串，0-index。
- `static int dp[MAXL][MAXT]`：DP 表，竞赛速写更稳。
- `long long`：临时解析子串值，防止中间乘 10 溢出；本题会在 `target` 以上立即停止。

输入如何整理：

```cpp
string s;
int target;
cin >> s >> target;
int len = (int)s.size();
```

接口：

```text
solve_p1874(s, target) -> 最少加号数量，不可达返回 -1
```

输出能力：

- 输出最少加号数。
- 不可达时输出 `-1`。

下游可接：

- DP-03 DFS -> 记忆化 -> 表推升级图。
- DP-03B 状态增维路由。
- DP-20 计数/可行性 DP，如果目标从“最少加号”改成“方案数/是否存在”。
- DP-25 暴力 DFS 到记忆化搜索：如果考场上先写出 `dfs(pos,sum)`，直接加 memo 也能得到同一批状态。

可拼接模块：

- `CPP-011 string`：子串和字符处理。
- `BRUTE-07`：如果先写 DFS，可加 memo。
- `DP-04`：线性前缀 DP 思路。

## 题意压缩

给定一个数字字符串 `s` 和整数 `target`。可以在相邻字符之间插入若干个 `+`，把字符串拆成若干个非负整数段。前导零不影响值，例如 `030` 的值是 `30`。要求所有段相加等于 `target`，并输出最少需要插入多少个加号；如果无论如何都不能等于 `target`，输出 `-1`。

样例：

```text
99999
45
```

输出：

```text
4
```

解释：`9+9+9+9+9=45`，需要 4 个加号。

## 第一阶段：先写暴力，找决策点

长度为 `len` 的字符串有 `len - 1` 个空隙。每个空隙只有两种选择：

```text
切：插入一个 +
不切：继续把后面的数字拼到当前段里
```

所以朴素暴力是：

```text
枚举每个空隙是否切开
计算每种表达式的和
取能等于 target 的最少加号数
```

复杂度是 `O(2^(len-1))`。本题 `len <= 40`，最大约 `2^39`，远远超过考场可承受范围。

结论：暴力可以帮助理解题目，但必须找重复状态，用记忆化或 DP 降复杂度。

## 第二阶段：找重叠子问题

从左到右处理字符串。假设已经处理完前 `i` 个字符，并且前面切出来的段之和是 `sum`。

这时后续还没处理的部分只关心两件事：

```text
1. 现在处理到哪个位置 i
2. 当前累计和是多少 sum
```

它不关心前面到底是：

```text
1 + 23
12 + 3
```

还是其他切法。只要位置和累计和相同，后续能不能凑到 `target`、还需要多少加号，都是同一个子问题。

这就是 DP 的信号：

```text
历史具体路径不重要，只保留会影响未来的摘要信息。
```

## 第三阶段：定义状态并验可行性

自然状态：

```text
dp[i][sum] = 把 s 的前 i 个字符切成若干段，段和等于 sum 时，最少需要多少个加号
```

其中：

- `i` 表示已经用掉前 `i` 个字符。
- `sum` 表示这些段的总和。
- `dp` 值表示优化目标：最少加号数。

可行性检查：

```text
i: 0..40
sum: 0..target，target <= 100000
状态数约 41 * 100001
int 表约 16MB
```

空间可行。因为每段都是非负数，如果当前和已经超过 `target`，后面再加也不会变小，所以 `sum` 只需要开到 `target`。

## 第四阶段：推导转移

看最后一段怎么来。

假设用数学上的 1-index 位置描述，最后一段是 `s[start..end]`，它的值是 `val`。在加上这一段之前，已经处理完前 `start - 1` 个字符，累计和是 `sum`。

于是：

```text
前面状态：dp[start - 1][sum]
当前段值：val
新状态：dp[end][sum + val]
```

落到 C++ 代码里，字符串本身仍然是 0-index：如果当前已经处理完前 `i` 个字符，下一段从 `s[i]` 开始，到 `s[j]` 结束，新状态就是 `dp[j + 1][sum + val]`。

每切出一个新段，段数加一。加号数 = 段数 - 1。

最直观的写法是：

```text
dp[0][0] = 0
其他状态 = INF
```

当从位置 `i` 新开一段 `s[i..j]` 时：

```cpp
int add = (i == 0 ? 0 : 1);
dp[j + 1][sum + val] = min(dp[j + 1][sum + val], dp[i][sum] + add);
```

解释：

- 如果 `i == 0`，这是第一段，前面没有加号，所以加 `0`。
- 如果 `i > 0`，这段前面必须插入一个加号，所以加 `1`。

这个版本最贴近题目问法：`dp` 表里直接存“最少加号数”，不需要最后再减一。

## 第五阶段：细节与陷阱

1. 大数字剪枝：

   子串长度可能很长，不能直接 `stoll`。边枚举边计算 `val = val * 10 + digit`，一旦 `sum + val > target` 就停止扩展这一段。

2. 前导零：

   题目说前导零不影响大小。逐位计算天然支持：`"003"` 会得到 `3`。

3. 不可达：

   `dp[len][target]` 仍是 `INF` 时输出 `-1`。

4. 加号数量：

   不要把段数当答案。`a+b+c` 有 3 段但只有 2 个加号。

5. 目标为正：

   本题 `target >= 1`。如果遇到目标可为 0 的变体，也能用同一代码；只是注意全零字符串会有很多 0 段。

模板代码：

```cpp
#include <bits/stdc++.h>
using namespace std;

const int INF = 1000000000;
const int MAXL = 45;
const int MAXT = 100000 + 5;
static int dp[MAXL][MAXT];

int solve_p1874(const string &s, int target) {
    int len = (int)s.size();

    for (int i = 0; i <= len; i++) {
        for (int sum = 0; sum <= target; sum++) {
            dp[i][sum] = INF;
        }
    }
    dp[0][0] = 0;

    for (int i = 0; i < len; i++) {
        for (int sum = 0; sum <= target; sum++) {
            if (dp[i][sum] == INF) continue;

            long long val = 0;
            for (int j = i; j < len; j++) {
                val = val * 10 + (s[j] - '0');
                if (sum + val > target) break;

                int add = (i == 0 ? 0 : 1);
                int ns = (int)(sum + val);
                dp[j + 1][ns] = min(dp[j + 1][ns], dp[i][sum] + add);
            }
        }
    }

    if (dp[len][target] == INF) return -1;
    return dp[len][target];
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string s;
    int target;
    cin >> s >> target;

    cout << solve_p1874(s, target) << '\n';
    return 0;
}
```

调用示例：

```cpp
cout << solve_p1874("99999", 45) << '\n'; // 4
cout << solve_p1874("12", 3) << '\n';    // 1: 1+2
cout << solve_p1874("303", 6) << '\n';   // 1: 3+03
cout << solve_p1874("0003", 3) << '\n';  // 0: 整段 0003
```

常见坑：

- 用 `stoll(s.substr(...))`：长子串可能越界或抛异常，不适合考场稳写。
- 忘记前导零：`303 -> 3+03` 是合法的。
- 每开一段都无脑 `+1`，会把第一段前面也算一个加号；要写 `i == 0 ? 0 : 1`。
- 只初始化 `dp[i][整段值] = 0`，却忘记从 `dp[0][0]` 或前缀状态统一转移，容易漏情况。
- `sum + v` 越界：循环条件写成 `sum + v <= target`。
- `sum + val > target` 后继续扩展：既浪费时间，也可能让 `val` 变大后溢出。

暴力/部分分替代：

本题非常适合从暴力 DFS 升级成记忆化搜索。纯 DFS 只适合小数据；若给 `dfs(pos,sum)` 加 `memo/vis`，每个位置和累计和只计算一次，复杂度会降到 `O(len^2 * target)`。完整可抄代码见 DP-25。

```cpp
#include <bits/stdc++.h>
using namespace std;

const int INF = 1000000000;

string s;
int target_value;
int len;
int best_answer;

void dfs_bruteforce(int pos, long long sum, int plus_count) {
    if (sum > target_value) return;
    if (plus_count >= best_answer) return;

    if (pos == len) {
        if (sum == target_value) best_answer = min(best_answer, plus_count);
        return;
    }

    long long val = 0;
    for (int end = pos; end < len; end++) {
        val = val * 10 + (s[end] - '0');
        if (sum + val > target_value) break;
        int add = (pos == 0 ? 0 : 1);
        dfs_bruteforce(end + 1, sum + val, plus_count + add);
    }
}

int solve_fast_sum_bruteforce(const string& input, int target) {
    s = input;
    target_value = target;
    len = (int)s.size();
    best_answer = INF;
    dfs_bruteforce(0, 0, 0);
    return best_answer == INF ? -1 : best_answer;
}
```

这个 DFS 可以过很小数据。若改成 `memo[pos][sum] = 当前位置和当前累计和下最少还要多少加号`，就是 DP-25 的记忆化版本。

最小测试样例：

```text
输入：
99999
45
输出：
4

输入：
12
12
输出：
0

输入：
12
3
输出：
1

输入：
303
6
输出：
1

输入：
0003
3
输出：
0

输入：
111
100
输出：
-1
```

建模口令：

```text
先问：我处理到哪里？
再问：未来还需要知道什么？
本题答案：处理到 start/end，未来只需要知道当前 sum。
所以状态是 dp[i][sum]，值是最少加号数。
```
