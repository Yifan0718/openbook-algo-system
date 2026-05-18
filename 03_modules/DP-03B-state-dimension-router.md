# DP-03B：状态增维/升维路由

模块编号：DP-03B

模块名称：状态增维/升维路由

标签：DP、状态设计、增维、升维、无后效性、有后效性、反例、记忆化

一句话用途：看到题面里有“未来会受某个历史信息影响”的信号，就把这个信息加进状态，让新状态重新满足无后效性。

题面触发词：

- “相邻不能相同”“上一个选择影响当前”
- “已经访问/已经拥有/已经使用过”
- “恰好 k 个”“还剩几次”“容量/预算”
- “不超过 N”“前导零”“数位限制”
- “颜色/奇偶/余数/父亲/阶段”

什么时候用：

- 已经会写 `dfs(...)`，但样例或手推发现同一个位置后续答案不唯一。
- 写 memo 前，需要检查 DFS 参数是否完整。
- 表推 DP 状态太少，转移里偷偷用了全局变量、路径数组或上一轮选择。

不要什么时候用：

- 这个信息只影响当前转移，不影响以后，可以不用放进状态。
- 这个信息能由现有状态唯一推出，不要重复增维。
- 状态数乘起来爆炸时，先判断能否换模型、压缩状态或只保留必要摘要。

复杂度：

```text
状态数 = 每个维度取值数量相乘
总复杂度 = 状态数 * 每个状态的选择数
```

数据范围信号：

- 多加一维 `last`：通常乘 `值域大小`。
- 多加一维 `cnt/rest/mod`：通常乘 `K/W/M`。
- 多加一维 `mask`：通常乘 `2^n`，要求 `n` 小。
- 多加 `tight/leading`：通常只乘 `2 * 2`，数位 DP 常用。

依赖的标准容器：

- `vector`
- `array`
- `map<tuple<...>, ll>`：状态维度复杂时先保命。

输入如何整理：

- 把题面限制逐条画圈。
- 每条限制问一句：未来选择还需要知道它吗？
- 需要就变成 DFS 参数或 DP 下标。

接口：

```text
题面信号 -> 必须记住的信息 -> 状态维度 -> 漏掉会错的反例
```

输出能力：

- 帮你判断 `dp[i]` 是否该升级成 `dp[i][last]`、`dp[i][cnt]`、`dp[mask][last]` 等。
- 帮你发现 memo 漏参数导致的 WA。

下游可接：

- DP-02 状态句式库
- DP-03 DFS -> 记忆化 -> 表推升级图
- DP-16 状压 DP
- DP-17 数位 DP
- DP-20 计数/可行性 DP
- DP-26 有后效性例题：用“错误状态 -> 反例 -> 升维 -> 完整代码”练习。

可拼接模块：

- `map<tuple>` 记忆化。
- Graph/Tree：`parent`、`color`、`phase` 常见。
- Math：`parity/mod` 常见。

## 核心原则

```text
看到什么题面信号，就给状态加什么维度。
```

更准确地说：

```text
如果两个局面“处理到的位置相同”，但因为某个历史信息不同，导致后续合法选择或答案不同，
那么这个历史信息必须进入状态。
```

换句话说：

```text
状态有后效性 -> 找到影响未来的关键历史 -> 升维/增维 -> 新状态无后效性。
```

状态句式固定写成：

```text
dp[处理到哪里][还必须记住什么] 表示：当前局面下的最优值/方案数/是否可行。
```

## 一眼增维表

| 题面信号 | 常加维度 | 状态句式 | 漏状态反例 |
|---|---|---|---|
| 相邻、递增、上一步影响当前 | `last` | `dfs(i,last)` | 二进制串相邻不能相同，只知道 `i` 不知道上一位，无法判断下一位能不能放 `0` |
| 访问过、拥有钥匙、集合状态 | `mask` | `dp[mask][last]` | 同在一个房间，拿过钥匙和没拿钥匙能打开的门不同 |
| 恰好 k 个、还剩次数、容量 | `cnt/rest` | `dp[i][cnt]` / `dp[i][rest]` | 处理到第 `i` 个时，已选 0 个和已选 2 个，离“恰好 2 个”的答案不同 |
| 数字上界、不超过 N | `tight` | `dfs(pos,tight,...)` | 前缀等于上界时本位最多取 `digits[pos]`，前缀已经小于上界时本位可取 `9` |
| 前导零是否还在 | `leading` | `dfs(pos,leading,...)` | 统计不含数字 0 时，数字 `7` 前面的补位 `0007` 不能算出现了 0 |
| 染色、类别、模式 | `color` | `dp[u][color]` | 树染色时父亲是红色和蓝色，儿子可选颜色不同 |
| 奇偶、余数、整除 | `parity/mod` | `dp[i][rem]` | 只知道前 `i` 个，不知道和模 3 的余数，无法判断最后是否整除 3 |
| 树/图从哪里来 | `parent/prev` | `dfs(u,parent)` | 在无向树上到达 `2`，父亲是 `1` 和父亲是 `3` 时，能继续处理的子树不同 |
| 分阶段、冷却、持有状态 | `phase` | `dp[i][phase]` | 买卖股票只用 `dp[i]`，分不清今天结束后是手里有股票还是没股票 |

## 维度 1：`last`

题面信号：

```text
相邻不能相同
上一个数字/字符影响当前
递增、递减、不下降
路径最后停在哪里
```

状态句式：

```text
dfs(i, last) 表示：已经处理到第 i 位/第 i 步，上一位或最后位置是 last 时，后续答案。
```

漏状态反例：

```text
问长度为 n 的 0/1 串数量，要求相邻字符不同。

如果只写 dfs(i)，那么处理完第 1 位以后：
前缀 "0" 和前缀 "1" 都是 i=2，
但前缀 "0" 下一位只能放 1，前缀 "1" 下一位只能放 0。
后续合法选择不同，所以 last 必须进状态。
```

小模板：

```cpp
ll dfs(int pos, int last) {
    if (pos == n) return 1;
    ll ans = 0;
    for (int x = 0; x <= 1; x++) {
        if (x == last) continue;
        ans += dfs(pos + 1, x);
    }
    return ans;
}
```

## 维度 2：`mask`

题面信号：

```text
n <= 20
已经访问哪些点
已经拿到哪些钥匙
哪些任务已经完成
集合中的元素会影响后续选择
```

状态句式：

```text
dp[mask][last] 表示：已经访问/选择集合 mask，最后停在 last 时的最优值/方案数。
last 保持 1..n 的业务编号；第 last 个元素对应 mask 的第 last-1 位。
```

漏状态反例：

```text
迷宫里同一个格子 (x,y)，如果已经拿到钥匙 A，可以打开 A 门；
没拿到钥匙 A，就不能打开。

只写 dp[x][y] 会把两种局面合并，导致把不能走的门当成能走，或把能走的路剪掉。
```

小模板：

```cpp
for (int mask = 0; mask < (1 << n); mask++) {
    for (int last = 1; last <= n; last++) {
        if (dp[mask][last] == LINF) continue;
        for (int nxt = 1; nxt <= n; nxt++) {
            if (mask >> (nxt - 1) & 1) continue;
            int nmask = mask | (1 << (nxt - 1));
            dp[nmask][nxt] = min(dp[nmask][nxt], dp[mask][last] + dist[last][nxt]);
        }
    }
}
```

## 维度 3：`cnt/rest`

题面信号：

```text
恰好/至多/至少选 k 个
还剩几次机会
容量、预算、体力、时间
```

状态句式：

```text
dp[i][cnt] 表示：处理完前 i 个元素，已经选 cnt 个时的答案。
dp[i][rest] 表示：处理到第 i 个元素，还剩 rest 资源时的答案。
```

漏状态反例：

```text
从 5 个数中恰好选 2 个，使和最大。

处理到第 4 个数时，如果只写 dp[i]，
不知道前面已经选了 0 个、1 个还是 2 个。
这些局面后续能不能继续选、答案是否已经合法都不同。
```

小模板：

```cpp
vector<vector<ll>> dp(n + 1, vector<ll>(K + 1, -LINF));
dp[0][0] = 0;
for (int i = 1; i <= n; i++) {
    for (int cnt = 0; cnt <= K; cnt++) {
        dp[i][cnt] = max(dp[i][cnt], dp[i - 1][cnt]); // 不选
        if (cnt > 0) {
            if (dp[i - 1][cnt - 1] != -LINF) {
                dp[i][cnt] = max(dp[i][cnt], dp[i - 1][cnt - 1] + a[i]); // 选
            }
        }
    }
}
```

## 维度 4：`tight`

题面信号：

```text
统计 0..N 或 1..N
上界很大
数字逐位构造
```

状态句式：

```text
dfs(pos, tight, state) 表示：处理到第 pos 位，当前前缀是否仍贴着上界 tight。
```

漏状态反例：

```text
N = 523。

处理第 2 位时：
前缀是 5，下一位最多只能取 2；
前缀是 4，下一位可以取 0..9。

如果不记 tight，会把两种上界混在一起。
```

小模板：

```cpp
int up = tight ? digits[pos] : 9;
for (int d = 0; d <= up; d++) {
    bool ntight = tight && (d == up);
    ans += dfs(pos + 1, ntight, next_state);
}
```

注意：`tight == true` 的状态通常不要缓存；只缓存 `tight == false` 更稳。

## 维度 5：`leading`

题面信号：

```text
数字可以有前导零补齐位数
统计是否出现某个数字
相邻数位限制
不允许数字 0 被前导零误算
```

状态句式：

```text
dfs(pos, leading, state) 表示：处理到第 pos 位，当前是否仍没有放过非零数字。
```

漏状态反例：

```text
统计 1..100 中“不含数字 0”的数。

数字 7 在三位写法里是 007。
前两个 0 是补位，不应该算作“出现了数字 0”。
如果不记 leading，就会错误排除 7。
```

小模板：

```cpp
bool nleading = leading && (d == 0);
int nlast = nleading ? 10 : d; // 10 表示还没有真实上一位
```

## 维度 6：`color`

题面信号：

```text
染色
相邻点颜色不同
某点属于某类
父子状态限制
```

状态句式：

```text
dp[u][color] 表示：u 的颜色为 color 时，u 子树的方案数/最优值。
```

漏状态反例：

```text
一棵树相邻点不能同色，有 3 种颜色。

如果只写 dp[u]，父亲是什么颜色不知道。
父亲是红色时 u 不能选红色；父亲是蓝色时 u 不能选蓝色。
合法选择不同，所以 color 必须进入状态或在转移中枚举。
```

小模板：

```cpp
for (int c = 0; c < C; c++) {
    dp[u][c] = 1;
    for (int v : g[u]) {
        if (v == p) continue;
        dfs(v, u);
        ll sum = 0;
        for (int vc = 0; vc < C; vc++) {
            if (vc == c) continue;
            sum = (sum + dp[v][vc]) % MOD;
        }
        dp[u][c] = dp[u][c] * sum % MOD;
    }
}
```

## 维度 7：`parity/mod`

题面信号：

```text
和为偶数/奇数
能被 K 整除
余数为 r
路径长度模 M
```

状态句式：

```text
dp[i][rem] 表示：处理完前 i 个元素，当前结果模 K 为 rem 时的方案数/是否可行。
```

漏状态反例：

```text
问选若干数，使总和能被 3 整除。

处理到同一个 i 时，当前和模 3 为 0、1、2 的后续完全不同。
只写 dp[i] 无法知道再加一个数后会到哪个余数。
```

小模板：

```cpp
vector<vector<ll>> dp(n + 1, vector<ll>(K, 0));
dp[0][0] = 1;
for (int i = 1; i <= n; i++) {
    for (int r = 0; r < K; r++) {
        dp[i][r] = (dp[i][r] + dp[i - 1][r]) % MOD;
        int nr = (r + a[i]) % K;
        dp[i][nr] = (dp[i][nr] + dp[i - 1][r]) % MOD;
    }
}
```

## 维度 8：`parent/prev`

题面信号：

```text
无向树 DFS
从哪个方向进入会影响可走边
不能立刻走回上一点
换根或路径状态
```

状态句式：

```text
dfs(u, parent) 表示：当前在 u，父亲是 parent，只处理不走回 parent 的部分。
```

漏状态反例：

```text
链 1-2-3。

如果写 dfs(2)：
当 2 的父亲是 1 时，2 的子树应该继续处理 3；
当 2 的父亲是 3 时，2 的子树应该继续处理 1。

只用 u 不能区分这两种方向。
```

小模板：

```cpp
void dfs(int u, int parent) {
    for (int v : g[u]) {
        if (v == parent) continue;
        dfs(v, u);
    }
}
```

注意：固定根的树形 DP 中，`parent` 常作为 DFS 参数，不一定作为 `dp[u][...]` 的下标。只有同一个 `u` 可能从不同方向进入并缓存时，才需要把 `parent/prev` 放进 memo key。

## 维度 9：`phase`

题面信号：

```text
买入/卖出/冷却
已经使用优惠券/尚未使用
正在匹配模式串第几步
第几阶段任务
```

状态句式：

```text
dp[i][phase] 表示：处理完第 i 天/第 i 个元素，当前处于 phase 阶段时的最优值。
```

漏状态反例：

```text
股票买卖题。

处理完第 i 天时，手里有股票和手里没股票的后续选择不同：
有股票可以卖，没股票可以买。
只写 dp[i] 会把两种状态混掉。
```

小模板：

```cpp
vector<array<ll, 2>> dp(n + 1);
dp[0][0] = 0;      // 0: 没持有
dp[0][1] = -LINF;  // 1: 持有
for (int i = 1; i <= n; i++) {
    dp[i][0] = max(dp[i - 1][0], dp[i - 1][1] + price[i]); // 不动或卖出
    dp[i][1] = max(dp[i - 1][1], dp[i - 1][0] - price[i]); // 不动或买入
}
```

## `map<tuple>` 完整状态救场

状态维度一多，先用 `map<tuple>` 写对：

```cpp
map<tuple<int,int,int,int>, ll> memo;

ll dfs(int i, int last, int rest, int rem) {
    if (rest < 0) return -LINF;
    if (i == n + 1) return (rem == 0 ? 0 : -LINF);

    auto key = make_tuple(i, last, rest, rem);
    if (memo.count(key)) return memo[key];

    ll ans = -LINF;
    // 按题意枚举选择，更新 last/rest/rem
    return memo[key] = ans;
}
```

能过样例后，再看每个维度范围，改成数组。

## 状态完整性检查卡

```text
1. 同样的 dp 下标，未来合法选择是否完全一样？
2. 同样的 dp 下标，最终答案类型是否完全一样？
3. 转移中是否偷偷用了 path、sum、last、used 这类没进状态的变量？
4. memo key 是否包含所有会影响未来的参数？
5. 多加一维后，状态数是否还能承受？
```

常见坑：

- 为了省维度，把 `last/cnt/rem` 写成全局变量，memo 立即失效。
- `tight/leading` 没处理清楚，数位 DP 容易多算 0 或越过上界。
- `mask` 和 `last` 缺一个：访问集合知道了，但不知道当前停在哪里。
- `parent` 作为参数传了，但 memo 只按 `u` 缓存。
- 只因为题面出现一个词就盲目增维，没有检查这个信息是否影响未来。

暴力/部分分替代：

- 状态不确定：先写不带 memo 的 DFS，用参数显式表达所有历史。
- 参数完整后：直接 `map<tuple>` memo。
- 状态数太大：只保留题面真正会影响未来的摘要，例如 `sum % K`，不要保留完整 `sum`。

升级方向：

- `dfs(i,last)` -> `memo[i][last]` -> `dp[i][last]`。
- `dfs(i,cnt,rem)` -> 三维数组或滚动数组。
- `dfs(pos,tight,leading,last,rem)` -> 数位 DP。
- `dfs(mask,last)` -> 状压 DP。
- `dfs(i,j,lastMove/used)` -> DP-26 网格升维例题。

最小测试样例：

```text
题面摘要：长度为 3 的 0/1 串，相邻不能相同，问方案数。

正确状态：dfs(pos,last)
答案：2
合法串：010, 101
如果只写 dfs(pos)，说明状态漏了 last。
```
