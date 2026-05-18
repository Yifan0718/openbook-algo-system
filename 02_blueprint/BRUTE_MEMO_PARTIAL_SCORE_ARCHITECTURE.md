# 第 2 卷：暴力、记忆化与部分分架构 v0.1

## 1. 定位

第 2 卷不是“低级算法卷”，而是整套资料的抢分核心。

它要解决的问题：

```text
不会正解时，怎么先写出能得分的程序？
暴力 DFS 写出来后，怎么用最小改动加记忆化？
记忆化还能不能作为 DP 的入口？
大数据不会时，怎么输出合法兜底，避免 0 分？
```

这一卷和 DP 卷的关系：

```text
第 2 卷：搜索表达问题，记忆化减少重复，优先拿部分分
第 3 卷：识别模型，把记忆化/递归转成表推 DP 或优化 DP
```

所以“记忆化搜索”必须放在第 2 卷作为核心章节，而不是只放在 DP 卷里。

## 2. 第 2 卷推荐目录

```text
BRUTE-00：部分分总策略
BRUTE-01：复杂度与数据范围速查
BRUTE-02：合法兜底输出
BRUTE-03：全排列枚举
BRUTE-04：组合/选不选 DFS
BRUTE-05：子集枚举与子集的子集
BRUTE-06：回溯与剪枝
BRUTE-07：记忆化搜索总论
BRUTE-08：数组/vector 记忆化
BRUTE-09：map<tuple,...> 记忆化
BRUTE-10：unordered_map + 编码记忆化
BRUTE-11：BFS 状态搜索
BRUTE-12：折半枚举
BRUTE-13：小数据精确 + 大数据特判
BRUTE-14：暴力版本到优化版本的提交策略
BRUTE-15：暴力/记忆化常见坑
```

## 3. 记忆化搜索的核心原则

### 3.1 一句话

```text
记忆化搜索 = 暴力 DFS + 对相同状态的答案缓存。
```

### 3.2 什么时候用

```text
已经能写出 DFS
DFS 参数能完整描述当前局面
同一个参数组合会反复出现
状态总数明显小于搜索树节点数
表推 DP 顺序想不清
想先拿部分分或中档分
```

### 3.3 不要什么时候用

```text
状态里缺了关键信息，导致同参数但后续答案不同
DFS 返回值依赖未纳入状态的全局变量
每条路径几乎都不同，没有重复状态
状态数量比暴力节点还大
递归深度可能爆栈且不能控制
```

## 4. 从暴力 DFS 到记忆化的固定改造流程

### Step 1：先写出暴力 DFS

```cpp
ll dfs(int i, int rest) {
    if (rest < 0) return -LINF;
    if (i == n + 1) return 0;

    ll ans = -LINF;

    ans = max(ans, dfs(i + 1, rest)); // 不选
    ans = max(ans, value[i] + dfs(i + 1, rest - cost[i])); // 选

    return ans;
}
```

### Step 2：确认 DFS 参数就是状态

问自己：

```text
给定 i 和 rest 后，后面最多能得到多少，是否已经确定？
是否还需要知道 last、mask、cnt、当前颜色、上一位置？
```

如果还需要，就把它加入参数。

### Step 3：选择 memo 容器

```text
状态范围小且边界明确 -> vector / 数组
状态维度复杂但数量不大 -> map<tuple,...>
状态需要速度且能安全编码 -> unordered_map<long long,...>
```

### Step 4：加查表和存表

推荐顺序：

```text
先判非法状态
再判终止状态
再查 memo
最后枚举转移并写入 memo
```

原因：

```text
非法状态可能导致数组越界，必须最先拦截。
终止状态通常很简单，也可以直接返回。
memo 查询应该发生在状态已经确定合法之后。
```

```text
if (vis[state]) return memo[state];
vis[state] = 1;
计算当前状态的答案 ans
return memo[state] = ans;
```

### Step 5：提交记忆化版本

记忆化版本本身就是正式得分版本，不必等改成表推 DP。

## 5. 三种 memo 模板

选择路线：

| 状态特点 | 推荐 memo | 考场建议 |
|---|---|---|
| 状态是小范围整数 | `vector` / 数组 | 首选，最快 |
| 状态维度复杂、范围不清 | `map<tuple,...>` | 最稳，先保证能写对 |
| 状态稀疏但数量较多 | `unordered_map` | 性能升级，但要小心编码 |
| 状态含集合 | `mask` + `vector` | `n <= 20` 时优先 |
| 状态含负数下标 | 平移 OFFSET 或 `map` | 不确定就用 `map` |

### 5.1 数组/vector memo：状态范围明确时首选

适用：

```text
0 <= i <= n
0 <= rest <= W
n * W 可承受
```

模板：

```cpp
vector<vector<ll>> memo;
vector<vector<int>> vis;

ll dfs(int i, int rest) {
    if (rest < 0) return -LINF;
    if (i == n + 1) return 0;

    if (vis[i][rest]) return memo[i][rest];
    vis[i][rest] = 1;

    ll ans = -LINF;
    ans = max(ans, dfs(i + 1, rest));
    ans = max(ans, value[i] + dfs(i + 1, rest - cost[i]));

    return memo[i][rest] = ans;
}
```

初始化：

```cpp
memo.assign(n + 2, vector<ll>(W + 1, 0));
vis.assign(n + 2, vector<int>(W + 1, 0));
```

### 5.2 map<tuple,...> memo：考场最稳通用版

适用：

```text
状态维度不固定
范围不方便开数组
先追求写对，不追求最快
```

模板：

```cpp
map<tuple<int,int,int>, ll> memo;

ll dfs(int i, int rest, int last) {
    if (rest < 0) return -LINF;
    if (i == n + 1) return 0;

    auto key = make_tuple(i, rest, last);
    if (memo.count(key)) return memo[key];

    ll ans = -LINF;
    // enumerate choices

    return memo[key] = ans;
}
```

优点：

```text
不需要手写哈希
不容易因为编码冲突出错
非常适合纸质开卷临场改造
```

缺点：

```text
常数大
状态太多时会慢
```

### 5.3 unordered_map + 编码：性能升级版

适用：

```text
状态范围已知
map 太慢
能保证编码不冲突
```

模板：

```cpp
unordered_map<long long, ll> memo;

long long encode(int i, int rest, int last) {
    return ((long long)i << 42) ^ ((long long)rest << 21) ^ last;
}

ll dfs(int i, int rest, int last) {
    if (rest < 0) return -LINF;
    if (i == n + 1) return 0;

    long long key = encode(i, rest, last);
    if (memo.count(key)) return memo[key];

    ll ans = -LINF;
    // enumerate choices

    return memo[key] = ans;
}
```

警告：

```text
每一维范围必须小于分配的位数
不确定时不要用，退回 map<tuple,...>
```

## 6. 返回值类型四件套

记忆化模板要按题目目标替换。

### 最大值

```cpp
ll ans = -LINF;
非法返回 -LINF;
ans = max(ans, candidate);
```

### 最小值

```cpp
ll ans = LINF;
非法返回 LINF;
ans = min(ans, candidate);
```

### 方案数

```cpp
ll ans = 0;
非法返回 0;
成功边界返回 1;
ans = (ans + candidate) % MOD;
```

### 可行性

```cpp
bool ans = false;
非法返回 false;
成功边界返回 true;
ans = ans || candidate;
```

## 7. 记忆化状态设计卡片

每次加 memo 前填这张卡：

```text
dfs 参数：
dfs 返回值：
非法状态：
结束状态：
选择列表：
状态是否完整：
memo 容器：
预计状态数：
```

示例：

```text
dfs(i, rest)
返回：从第 i 个物品开始，剩余容量 rest 时最大价值
非法：rest < 0
结束：i == n + 1 返回 0
选择：不选/选
状态完整：是，不需要知道已选路径
memo：vector<vector<ll>>
预计状态数：n * W
```

## 8. 与 DP 模型的连接

记忆化搜索不是“失败方案”，而是 DP 的自然入口。

```text
dfs(i, rest)
  -> memo[i][rest]
  -> dp[i][rest]
```

改表推时：

```text
DFS 参数变成 DP 下标
DFS 边界变成 DP 初始化
DFS 选择变成 DP 转移
DFS 依赖方向决定循环顺序
```

如果循环顺序想不清：

```text
不要强行表推，保留记忆化提交
```

## 9. 部分分提交策略

DP/搜索类题建议：

```text
Version 0：特判 + 合法输出
Version 1：暴力 DFS
Version 2：DFS + 剪枝
Version 3：记忆化搜索
Version 4：表推 DP / 优化 DP
```

记忆化版一旦样例和小极端过，就值得提交。因为每题取最高分，没必要等满分正解。

## 10. 常见坑

```text
memo 没有按多测清空
边界返回值没有存 memo，导致重复算
非法状态先访问数组，导致越界
状态遗漏 last/mask/cnt，导致错误缓存
用全局变量记录路径，却没纳入状态
有环状态直接递归，导致死循环
map 状态太多导致 TLE，但仍可拿部分分
unordered_map 编码冲突或位数不够
递归太深爆栈
最大值题初值误设为 0，导致全负数错
计数题忘记取模
```

有环状态额外处理：

```cpp
// 0 = 未访问，1 = 正在访问，2 = 已算完
vector<int> color;
```

如果 `dfs(u)` 可能递归回 `dfs(u)`，不能只用普通 `vis` 当作已完成标记；需要检测环，或换成图论/拓扑/最短路模型。

## 11. 最小验错样例思路

每个记忆化模块至少测：

```text
n=1
容量/资源为 0
所有选择都非法
所有选择都合法
存在重复状态的小例子
答案为负数的最大值题
```

## 12. 一句话结论

第 2 卷必须让使用者形成这个肌肉记忆：

```text
先写能枚举所有选择的 DFS；
确认参数完整；
相同参数会重复就加 memo；
memo 版本先提交；
有时间再翻 DP 卷改表推。
```
