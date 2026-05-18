# DP-17：数位 DP

模型编号：DP-17

模型名称：数位 DP

标签：DP、数字位、上界限制、计数、记忆化搜索

一句话用途：统计 `1..N` 或 `L..R` 中满足数位条件的正整数数量；如果题目把 `0` 也算合法，在 base case 里打开 `count_zero`。

题面触发词：

- “1 到 N 中有多少个数”
- “数字各位满足条件”
- “不含某个数字”
- “数位和”
- “上界很大，N 可到 10^18 或 10^100”

什么时候用：

- 判断条件和数字的每一位有关。
- 上界太大，不能枚举所有数。
- 状态能用“当前位 + 是否贴上界 + 前导零 + 附加信息”描述。

不要什么时候用：

- `N` 很小，直接枚举更简单。
- 条件不是数位局部状态能表达。
- 需要统计的是排列/组合对象，不是数字范围。

复杂度：

- `O(位数 * 状态数 * 10)`。

数据范围信号：

- `N <= 1e18`：位数最多 19。
- `N` 是长字符串：位数可达几千，也要看状态大小。

依赖的标准容器：

- `vector<int> digits`
- `map<tuple<...>, ll>` 或多维数组 memo

输入如何整理：

- 把 `N` 拆成从高位到低位的 `digits`。
- 计算 `[L,R]` 时用 `solve(R) - solve(L-1)`。

接口：

```cpp
ll solve(long long N);
```

输出能力：

- 满足数位条件的数量。
- 可扩展为数位和总和、最大/最小数字。

下游可接：

- 取模计数。
- 记忆化 DFS。

可拼接模块：

- 数学取模。
- `map<tuple>` memo。

状态句式：

```text
dfs(pos, tight, leading, state) 表示：处理到第 pos 位，是否贴着上界 tight，是否仍是前导零 leading，附加状态为 state 时，后面能组成的合法数量。
```

初始化：

```text
从 pos = 0 开始，tight = true，leading = true，state = 初始状态。
到 pos == 位数 时，按 state 判断是否计 1。
```

转移模板：

```cpp
int up = tight ? digits[pos] : 9;
for (int d = 0; d <= up; d++) {
    ntight = tight && (d == up);
    nleading = leading && (d == 0);
    nstate = update(state, d, nleading);
}
```

答案位置：

- `solve(N)`。
- 区间：`solve(R) - solve(L - 1)`。

循环顺序：

- 记忆化 DFS 通常最稳。
- 表推可按 `pos` 从高位到低位推进，状态带 `tight/leading`。

暴力 DFS 版本：

```cpp
ll dfs_plain(int pos, bool tight, bool leading, int sum) {
    bool count_zero = false; // 如果 0 也是合法数字，改成 true
    if (pos == len) return ((!leading || count_zero) && sum % K == 0) ? 1 : 0;
    int up = tight ? digits[pos] : 9;
    ll ans = 0;
    for (int d = 0; d <= up; d++) {
        bool ntight = tight && (d == up);
        bool nleading = leading && (d == 0);
        int nsum = nleading ? 0 : (sum + d) % K;
        ans += dfs_plain(pos + 1, ntight, nleading, nsum);
    }
    return ans;
}
```

记忆化版本：

```cpp
const int MAXD = 20;   // long long 上界最多 19 位；大数字字符串按题目改大
const int MAXK = 205;  // 按题目 K 调大
static ll memo[MAXD][MAXK][2];
static char vis[MAXD][MAXK][2];
bool count_zero = false; // 如果 0 也是合法数字，改成 true

ll dfs(int pos, bool tight, bool leading, int sum) {
    if (pos == len) return ((!leading || count_zero) && sum % K == 0) ? 1 : 0;
    if (!tight && vis[pos][sum][leading]) return memo[pos][sum][leading];

    int up = tight ? digits[pos] : 9;
    ll ans = 0;
    for (int d = 0; d <= up; d++) {
        bool ntight = tight && (d == up);
        bool nleading = leading && (d == 0);
        int nsum = nleading ? 0 : (sum + d) % K;
        ans += dfs(pos + 1, ntight, nleading, nsum);
    }

    if (!tight) {
        vis[pos][sum][leading] = 1;
        memo[pos][sum][leading] = ans;
    }
    return ans;
}

ll solve(long long N) {
    if (N < 0) return 0;
    digits.clear();
    string s = to_string(N);
    for (char c : s) digits.push_back(c - '0');
    len = (int)digits.size();

    // 每次 solve 都清空 vis，避免 solve(R) 与 solve(L-1) 串缓存。
    memset(vis, 0, sizeof(vis));
    return dfs(0, true, true, 0);
}
```

如果 `N` 是长字符串，把 `solve(long long N)` 改成 `solve_string(const string& s)`，不要再 `to_string`：

```cpp
ll solve_string(const string& s) {
    digits.clear();
    for (char c : s) digits.push_back(c - '0');
    len = (int)digits.size();
    memset(vis, 0, sizeof(vis)); // MAXD 必须开到最大位数 + 1
    return dfs(0, true, true, 0);
}
```

如果位数或 `K` 由输入决定，固定 `MAXD/MAXK` 不够时改用动态 `vector` 或 `map<tuple<...>, ll>`，别硬抄固定数组。

表推版本：

```cpp
// 统计 1..N 中数位和 mod K == 0 的正整数数量；若 0 合法，另行按题意处理
static ll dp[MAXD][MAXK][2][2];
memset(dp, 0, sizeof(dp));
dp[0][0][1][1] = 1; // pos=0, sum=0, tight=true, leading=true

for (int pos = 0; pos < len; pos++) {
    for (int sum = 0; sum < K; sum++) {
        for (int tight = 0; tight <= 1; tight++) {
            for (int leading = 0; leading <= 1; leading++) {
                ll cur = dp[pos][sum][tight][leading];
                if (!cur) continue;
                int up = tight ? digits[pos] : 9;
                for (int d = 0; d <= up; d++) {
                    int ntight = tight && (d == up);
                    int nleading = leading && (d == 0);
                    int nsum = nleading ? 0 : (sum + d) % K;
                    dp[pos + 1][nsum][ntight][nleading] += cur;
                }
            }
        }
    }
}
ll ans = dp[len][0][0][0] + dp[len][0][1][0];
```

常见变体：

- 不含数字 `x`：遇到 `d==x` 跳过。
- 相邻位不能相同：状态加 `lastDigit`。
- 数字模 `M`：状态加 `rem`。

常见坑：

- `tight` 状态直接缓存，导致不同上界前缀混淆；通常只缓存 `tight=false`。
- 前导零是否算入条件没想清。
- 默认模板不统计数字 `0`；如果题目要求统计 `0..N` 且 `0` 合法，设置 `count_zero` 或对答案单独 `+1`。
- `[L,R]` 忘记处理 `L=0`。
- 若 `N` 是上百位长字符串，答案可能超过 `long long`；此时必须按题目要求取模，或改用大整数。
- `ntight` 写成 `d == up` 在 `tight=false` 时也为真；正确是 `tight && d == up`。
- `K` 可能很大时不要用固定数组；按 `len + 1` 和 `K` 动态开 `memo/vis` 更稳。
- 每次 `solve(N)` 要重建 `digits` 并清空 `memo/vis`，区间 `solve(R)-solve(L-1)` 不能串缓存。

暴力/部分分替代：

- `N <= 1e6`：直接枚举检查数位。
- 位数小但状态复杂：先写无 memo DFS。
- 状态清楚后，只缓存 `tight=false` 的状态。

升级方向：

- 暴力枚举数字 -> 数位 DFS。
- DFS -> 记忆化。
- 需要避免递归时改表推。

最小测试样例：

```text
N=20 K=3
输出：6
说明：3,6,9,12,15,18 的数位和能被 3 整除。
```
