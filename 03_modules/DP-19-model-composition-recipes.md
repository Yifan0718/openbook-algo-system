# DP-19：DP 模型拼接食谱

模型编号：DP-19

模型名称：DP 模型拼接食谱

标签：DP、拼接、PrefixSum、树状数组、Tree、Graph、Topo、Digit

一句话用途：当题目不是单纯 DP，而是“DP + 图论/数据结构/数学预处理”时，按固定食谱把模块接起来。

题面触发词：

- “区间代价反复出现”
- “从前面满足条件的位置转移”
- “树上选 k 个/容量限制”
- “访问关键点，原图有边权”
- “依赖关系、有向无环”
- “1..N 计数，要求取模/余数/组合数量”

什么时候用：

- 已经识别出主 DP 模型，但转移里的 `cost/query/dist/order/count` 需要别的模块提供。
- 朴素转移能写出来，但复杂度差一截。
- 题面同时出现 DP 信号和图论/数据结构/数学信号。

不要什么时候用：

- 单个 DP 模型已经足够，不要强行拼接。
- 辅助模块会改变问题本质，例如一般图最长路不能靠 DAG DP 解决。
- 还没写出状态句式，就先不要急着上数据结构。

复杂度：

```text
总复杂度 = 预处理复杂度 + DP 状态数 * 转移复杂度
```

数据范围信号：

- `n <= 300/500` 且区间：区间 DP + PrefixSum。
- `n <= 2e5` 且前驱范围查询：线性 DP/LIS + 树状数组/SegmentTree。
- `n <= 2000, K <= 2000` 且树上选数量：树形 DP + 背包合并。
- 关键点 `k <= 20`，原图大：最短路预处理 + 状压 DP。
- 有向无环依赖 `n,m <= 2e5`：Topo + DAG DP。
- `N` 很大且数位条件：数位 DP + 取模/组合。

依赖的标准容器：

- `vector`
- `queue`
- `priority_queue`
- `array`
- `tuple`

输入如何整理：

- 先确定主 DP 状态。
- 再问转移里缺什么：区间和、前驱最值、子树合并、关键点距离、拓扑序、组合数。
- 辅助模块只负责提供这个缺口，不要把状态含义写乱。

接口：

```text
主 DP 状态句式 + 辅助模块预处理 + 转移骨架 + 答案位置
```

输出能力：

- 一组可直接复用的拼接套路。
- 每个套路都给“先做什么，再做什么”的考场顺序。

下游可接：

- DP-13 区间 DP
- DP-14 树形 DP
- DP-15 DAG DP
- DP-16 状压 DP
- DP-17 数位 DP
- DP-18 DP + 数据结构优化

可拼接模块：

- DS-01 PrefixSum
- DS-02 树状数组
- GRAPH-03 Dijkstra
- GRAPH-04 Floyd
- GRAPH-05 Topo
- MATH-03 组合数

## 拼接总原则

```text
先写 DP 状态句式，再写辅助模块负责什么。
```

不要一上来就写大模板。考场顺序固定为：

```text
1. 主模型：这题的 dp 下标是什么？
2. 缺口：转移里反复需要算什么？
3. 辅助模块：用谁把缺口变成 O(1)、O(log n) 或有序处理？
4. 拼接点：辅助模块的输出喂给哪一行转移？
5. 答案位置：最后从哪个 dp 位置取？
```

## 食谱 1：区间 DP + PrefixSum

题面信号：

```text
区间合并、区间删除、合并石子
转移里反复用 sum(l,r) 或 cost(l,r)
n <= 300/500
```

拼接顺序：

```text
1. 先预处理 prefix[i] = a[1] + ... + a[i]
2. 写 sum(l,r) = prefix[r] - prefix[l-1]
3. 区间 DP 按 len 从小到大
4. 转移里直接调用 sum(l,r)
```

状态句式：

```text
dp[l][r] 表示：合并/处理区间 [l,r] 的最小代价。
```

代码骨架：

```cpp
const int MAXN = 505;
static ll prefix[MAXN], dp[MAXN][MAXN];

for (int i = 1; i <= n; i++) prefix[i] = prefix[i - 1] + a[i];

auto sum = [&](int l, int r) {
    return prefix[r] - prefix[l - 1];
};

for (int len = 2; len <= n; len++) {
    for (int l = 1; l + len - 1 <= n; l++) {
        int r = l + len - 1;
        dp[l][r] = LINF;
        for (int k = l; k < r; k++) {
            dp[l][r] = min(dp[l][r], dp[l][k] + dp[k + 1][r] + sum(l, r));
        }
    }
}
cout << dp[1][n] << '\n';
```

常见坑：

- 没有 PrefixSum，每次 `sum(l,r)` 再循环求和，复杂度多乘一层。
- `prefix` 是 1-index，`sum(l,r)` 要用 `prefix[l - 1]`。
- 区间 DP 必须小区间先算，大区间后算。

## 食谱 2：LIS/线性 DP + 树状数组

题面信号：

```text
n <= 2e5
dp[i] 需要从前面满足 a[j] < a[i] 或 a[j] <= a[i] 的 j 转移
要求最大权值递增子序列、前缀最优、值域范围最优
```

拼接顺序：

```text
1. 先写朴素转移：dp[i] = max(dp[j] + gain)
2. 把前驱条件改写成 key[j] 的前缀/区间查询
3. 值域大时坐标压缩
4. 树状数组维护“已经处理过的 key 的最大 dp”
5. 每个 i 先 query，再 add
```

状态句式：

```text
dp[i] 表示：以第 i 个元素作为最后一个元素时的最大收益。
```

树状数组最大值模板：

```cpp
struct BITMax {
    int n;
    vector<ll> bit;
    BITMax(int n = 0) { init(n); }
    void init(int n_) {
        n = n_;
        bit.assign(n + 1, -LINF);
    }
    void add(int idx, ll val) {
        for (; idx <= n; idx += idx & -idx) bit[idx] = max(bit[idx], val);
    }
    ll prefix(int idx) {
        ll ans = -LINF;
        for (; idx > 0; idx -= idx & -idx) ans = max(ans, bit[idx]);
        return ans;
    }
};
```

拼接代码：

```cpp
vector<ll> vals;
for (int i = 1; i <= n; i++) vals.push_back(a[i]);
sort(vals.begin(), vals.end());
vals.erase(unique(vals.begin(), vals.end()), vals.end());

auto pos = [&](ll x) {
    return int(lower_bound(vals.begin(), vals.end(), x) - vals.begin()) + 1;
};

BITMax bit((int)vals.size());
ll ans = 0; // 如果必须选至少一个且权值可能全负，改成 -LINF
for (int i = 1; i <= n; i++) {
    int p = pos(a[i]);
    ll best = bit.prefix(p - 1); // 严格递增：a[j] < a[i]
    ll dp_i = w[i] + max(0LL, best);
    bit.add(p, dp_i);
    ans = max(ans, dp_i);
}
cout << ans << '\n';
```

常见坑：

- 严格递增用 `p - 1`，不下降用 `p`。
- 必须先 `query` 再 `add`，否则会把自己当成前驱。
- 如果空前驱不合法，不能写 `max(0LL, best)`，要按题意处理。
- 如果必须选至少一个且权值可能全负，`ans` 初始化为 `-LINF`，每个 `dp_i` 至少可以等于 `w[i]`。

## 食谱 3：树形 DP + 背包合并

题面信号：

```text
树上选择 k 个点
每个子树贡献若干容量/数量
父亲要合并多个儿子的方案
n*K 能接受
```

拼接顺序：

```text
1. 树形 DP 后序 DFS
2. dp[u][j] 表示 u 子树选 j 个的最优值/方案数
3. 每合并一个儿子 v，就做一次背包合并
4. 用 ndp 防止同一个儿子被重复使用
```

状态句式：

```text
dp[u][j] 表示：只考虑 u 的子树，选 j 个点时的最大收益。
```

代码骨架：

```cpp
const int MAXN = 2000 + 5;
const int MAXK = 2000 + 5; // dp[MAXN][MAXK] 约 32MB，按题目内存调小
static ll dp[MAXN][MAXK], val[MAXN];
static int sz[MAXN];

for (int u = 1; u <= n; u++) {
    for (int j = 0; j <= K; j++) dp[u][j] = -LINF;
}

void dfs(int u, int p) {
    sz[u] = 1;
    dp[u][0] = 0;
    if (K >= 1) dp[u][1] = val[u]; // 选择 u

    for (int v : g[u]) {
        if (v == p) continue;
        dfs(v, u);

        static ll ndp[MAXK];
        for (int x = 0; x <= K; x++) ndp[x] = -LINF;
        for (int i = 0; i <= min(sz[u], K); i++) {
            if (dp[u][i] == -LINF) continue;
            for (int j = 0; j <= min(sz[v], K - i); j++) {
                if (dp[v][j] == -LINF) continue;
                ndp[i + j] = max(ndp[i + j], dp[u][i] + dp[v][j]);
            }
        }
        sz[u] += sz[v];
        for (int i = 0; i <= min(sz[u], K); i++) dp[u][i] = ndp[i];
    }
}

dfs(1, 0);
cout << dp[1][K] << '\n';
```

常见坑：

- 合并儿子时直接写回 `dp[u]`，导致一个儿子贡献被重复用。
- `sz[u]` 没维护，循环跑太大。
- `dp[u][0]` 忘记初始化为 0，导致“不选子树点”的状态不可达。

## 食谱 4：状压 DP + Floyd/Dijkstra

题面信号：

```text
访问所有关键点
关键点 k <= 20
原图上有边权或障碍
要求最短访问代价
```

拼接顺序：

```text
1. 找出关键点 key[1..k]
2. 在原图上求关键点两两最短路
   - n <= 300：Floyd
   - 稀疏大图：从每个关键点跑 Dijkstra
3. 得到 dist[i][j]，其中 i,j 都是 1..k 的关键点编号
4. 在关键点编号 1..k 上做状压 DP；第 i 个关键点对应 mask 的第 i-1 位
```

状态句式：

```text
dp[mask][last] 表示：已经访问关键点集合 mask，最后停在 last 时的最小代价。
last 是 1..k 的关键点编号，不要改成 0-index。
```

Floyd 拼接：

```cpp
const int MAXN = 305;
ll d[MAXN][MAXN];
for (int i = 1; i <= n; i++) {
    for (int j = 1; j <= n; j++) d[i][j] = (i == j ? 0 : LINF);
}
for (auto [u, v, w] : edges) {
    d[u][v] = min(d[u][v], w);
    d[v][u] = min(d[v][u], w);
}
for (int k = 1; k <= n; k++) {
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++) {
            if (d[i][k] == LINF || d[k][j] == LINF) continue;
            d[i][j] = min(d[i][j], d[i][k] + d[k][j]);
        }
    }
}

const int KMAX = 20;
ll dist[KMAX + 1][KMAX + 1];
for (int i = 1; i <= k; i++) {
    for (int j = 1; j <= k; j++) {
        dist[i][j] = d[key[i]][key[j]];
    }
}
```

Dijkstra 拼接：

```cpp
const int MAXN = 200000 + 5;
vector<pair<int,ll>> g[MAXN];

void dijkstra(int s, ll one[]) {
    for (int i = 1; i <= n; i++) one[i] = LINF;
    priority_queue<pair<ll,int>, vector<pair<ll,int>>, greater<pair<ll,int>>> pq;
    one[s] = 0;
    pq.push({0, s});

    while (!pq.empty()) {
        auto [du, u] = pq.top();
        pq.pop();
        if (du != one[u]) continue;
        for (auto [v, w] : g[u]) {
            if (one[v] > du + w) {
                one[v] = du + w;
                pq.push({one[v], v});
            }
        }
    }
}

const int KMAX = 20;
ll dist[KMAX + 1][KMAX + 1];
ll one[MAXN];
for (int i = 1; i <= k; i++) {
    dijkstra(key[i], one);
    for (int j = 1; j <= k; j++) {
        dist[i][j] = one[key[j]];
    }
}
```

状压拼接：

```cpp
const int SMAX = 1 << KMAX;
ll dp[SMAX][KMAX + 1];

int total = 1 << k;
int full = total - 1;
for (int mask = 0; mask < total; mask++) {
    for (int i = 1; i <= k; i++) dp[mask][i] = LINF;
}
dp[1 << (start - 1)][start] = 0;

for (int mask = 0; mask < total; mask++) {
    for (int last = 1; last <= k; last++) {
        if (dp[mask][last] == LINF) continue;
        for (int nxt = 1; nxt <= k; nxt++) {
            if (mask >> (nxt - 1) & 1) continue;
            if (dist[last][nxt] == LINF) continue;
            int nmask = mask | (1 << (nxt - 1));
            dp[nmask][nxt] = min(dp[nmask][nxt], dp[mask][last] + dist[last][nxt]);
        }
    }
}
```

常见坑：

- 原图点号和关键点编号都保持 1-index；只有 mask 取位时写 `(i - 1)`。
- 两个关键点不可达时，`dist == LINF` 要跳过。
- `1 << k` 要确认 `k <= 20` 左右，否则内存爆。

## 食谱 5：DAG DP + Topo

题面信号：

```text
依赖关系
任务先后顺序
有向无环图
路径计数/最长路/最早完成时间
```

拼接顺序：

```text
1. 建有向图，确认边方向
2. 拓扑排序
3. 按拓扑序做 dp 转移
4. 如果拓扑点数不足 n，说明有环，不能套普通 DAG DP
```

状态句式：

```text
dp[u] 表示：到达 u 的最大收益/最短时间/方案数。
```

代码骨架：

```cpp
const int MAXN = 200000 + 5;
static vector<pair<int,ll>> g[MAXN];
static int indeg[MAXN];
static ll dp[MAXN];

for (auto [u, v, w] : edges) {
    g[u].push_back({v, w});
    indeg[v]++;
}

queue<int> q;
for (int i = 1; i <= n; i++) {
    if (indeg[i] == 0) q.push(i);
}

vector<int> topo;
while (!q.empty()) {
    int u = q.front();
    q.pop();
    topo.push_back(u);
    for (auto [v, w] : g[u]) {
        if (--indeg[v] == 0) q.push(v);
    }
}

if ((int)topo.size() < n) {
    cout << "-1\n"; // 有环，不能直接用 DAG DP。
    return;
}

for (int i = 1; i <= n; i++) dp[i] = -LINF;
dp[s] = 0;
for (int u : topo) {
    if (dp[u] == -LINF) continue;
    for (auto [v, w] : g[u]) {
        dp[v] = max(dp[v], dp[u] + w);
    }
}
cout << dp[t] << '\n';
```

方案数改法：

```cpp
vector<ll> ways(n + 1, 0);
ways[s] = 1;
for (int u : topo) {
    for (auto [v, w] : g[u]) {
        ways[v] = (ways[v] + ways[u]) % MOD;
    }
}
```

常见坑：

- “u 依赖 v”时，边可能应建成 `v -> u`。
- 有多个起点时，方案数/最早时间要初始化所有起点。
- 拓扑排序会修改 `indeg`，后面还要用原入度就先备份。

## 食谱 6：数位 DP + 取模/组合

题面信号：

```text
默认统计 1..N 或 L..R 中的正整数；如果 0 合法，base case 要单独打开
数字本身模 M 为某个余数
数位和模 K
恰好有 k 个非零位/某数字出现 k 次
答案对 MOD 取模
```

拼接顺序：

```text
1. 把 N 拆成 digits
2. 数位 DP 保留 tight/leading
3. 需要整除或余数时，加 rem 维度
4. 需要出现次数时，加 cnt/rest 维度
5. 如果 tight=false 后剩余位只和数量有关，可以用组合数加速；不会加速就保留 DP
```

状态句式：

```text
dfs(pos, tight, leading, rem, cnt) 表示：处理到 pos 位，当前余数 rem、已用数量 cnt 时的方案数。
```

取模 DP 骨架：

```cpp
ll dfs(int pos, bool tight, bool leading, int rem) {
    if (pos == len) {
        bool count_zero = false; // 如果 0 是合法数字，改成 true
        return ((!leading || count_zero) && rem == 0) ? 1 : 0;
    }

    if (!tight && vis[pos][leading][rem]) return memo[pos][leading][rem];

    int up = tight ? digits[pos] : 9;
    ll ans = 0;
    for (int d = 0; d <= up; d++) {
        bool nleading = leading && (d == 0);
        bool ntight = tight && (d == up);
        int nrem = nleading ? 0 : (rem * 10 + d) % M;
        ans = (ans + dfs(pos + 1, ntight, nleading, nrem)) % MOD;
    }

    if (!tight) {
        vis[pos][leading][rem] = 1;
        memo[pos][leading][rem] = ans;
    }
    return ans;
}
```

组合数加速句式：

```text
如果后面还剩 len 位，且只要求“恰好再放 need 个非零数字”，
数量可以是 C[len][need] * 9^need。
```

组合数预处理：

```cpp
const int MAXL = 105;
static ll C[MAXL][MAXL];

for (int i = 0; i <= maxLen; i++) {
    C[i][0] = C[i][i] = 1;
    for (int j = 1; j < i; j++) {
        C[i][j] = (C[i - 1][j - 1] + C[i - 1][j]) % MOD;
    }
}
```

常见坑：

- `rem` 是数字本身的余数时，更新应是 `(rem * 10 + d) % M`，不是 `(rem + d) % M`。
- 数位和余数才写 `(rem + d) % M`。
- `leading` 时是否更新 `rem/cnt` 要按题意决定。
- `tight=true` 的状态不要随便缓存。
- 区间 `[L,R]` 用 `solve(R) - solve(L-1)`，取模时要加回 `MOD`。

## 拼接检查卡

```text
1. 主 DP 状态是否已经写清楚？
2. 辅助模块的输出是什么变量？
3. 这个变量进入哪一行转移？
4. 预处理下标和 DP 下标是否一致？
5. 复杂度是否是“预处理 + DP”，没有暗中多一层循环？
```

暴力/部分分替代：

- 拼接写不出来时，先交朴素 DP：区间和暴力、前驱枚举、DFS 路径枚举。
- 图上关键点距离不会预处理时，先只处理完全图输入的版本。
- 数位 DP 想不清组合加速时，保留完整 `cnt/rem` 记忆化。

升级方向：

- 区间转移代价重复计算 -> PrefixSum。
- 线性 DP 前驱枚举 -> 树状数组/SegmentTree。
- 树上多个子树数量分配 -> 背包合并。
- 原图访问关键点 -> 最短路预处理 + 状压。
- 依赖图 -> Topo 后 DP。
- 数位范围计数 -> `tight/leading` + `mod/cnt/comb`。

最小测试样例：

```text
检查任意拼接题时，先写这三行：

主状态：dp[...]
辅助模块：负责提供 ...
转移拼接点：dp[...] = merge(dp[...], 辅助模块输出 + ...)
```
