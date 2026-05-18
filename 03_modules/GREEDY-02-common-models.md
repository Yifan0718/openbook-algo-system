# GREEDY-02：常见贪心模型补充

模块编号：GREEDY-02

模块名称：常见贪心模型补充

标签：贪心、区间覆盖、双指针、二分答案、截止时间、相邻交换

一句话用途：补齐 GREEDY-00 之外的高频贪心：区间覆盖整段、排序双指针配对、二分答案中的贪心 `check`、截止时间收益最大。

题面触发词：

- “最少区间覆盖 `[L,R]`”
- “每艘船最多两人/两端配对/尽量多匹配”
- “最大化最小值/最小化最大值”
- “每个任务有截止时间和收益”
- “排序顺序会影响总代价”

什么时候用：

- 排序后只需要扫描、双指针或堆维护。
- 当前选择有明确不变量：覆盖最远、配对最省、保留收益最大。
- `check(x)` 能用从左到右的贪心验证可行性。

不要什么时候用：

- 区间选择有收益且要最大化总收益，常转 DP。
- 配对选择需要记复杂历史，双指针不一定成立。
- 截止时间有依赖关系或任务耗时不统一，普通收益贪心可能失效。
- 不能说明为什么当前选择不吃亏时，先回 GREEDY-01 或 DP。

复杂度：

- 排序 + 扫描/双指针/堆：`O(n log n)`。
- 二分答案 + 贪心检查：`O(n log V)` 或 `O(n log n log V)`。
- DSU 找空位：`O(n log n + n alpha(n))`。

数据范围信号：

- `n <= 2e5`：排序、堆、DSU 贪心常用。
- 答案范围很大，且有单调性：二分答案 + 贪心 `check`。
- 小数据可先枚举验证贪心。

依赖的标准容器：

- `vector`
- `sort`
- `priority_queue`
- `DSU` 或简单并查集数组。

输入如何整理：

- 区间统一成 `struct Seg { int l, r; };`
- 任务统一成 `struct Job { int deadline, profit; };`
- 双指针配对先排序数组。

接口：

```text
int cover_interval(Seg seg[], int n, int L, int R);
int min_boats(vector<int> weight, int limit);
long long max_profit_jobs(vector<Job> jobs);
```

输出能力：

- 最少覆盖区间数。
- 最少配对资源数。
- 最大可得收益。
- 二分答案可行性。

下游可接：

- GREEDY-00 贪心路由。
- GREEDY-01 贪心与 DP 判别。
- DSU 模块。
- 二分答案模块。

可拼接模块：

- Sorting：所有模型都先排序。
- PriorityQueue：收益/截止时间反悔。
- DSU：每个时间槽最多放一个任务。

## 1. 区间覆盖整段

给若干区间，问最少选几个覆盖 `[L,R]`。每一步在所有 `l <= 当前覆盖右端 + 1` 的区间里，选 `r` 最远的那个。

```cpp
#include <bits/stdc++.h>
using namespace std;

struct Seg {
    int l;
    int r;
};

const int MAXN = 200000 + 5;

int cover_interval(Seg seg[], int n, int L, int R) {
    sort(seg + 1, seg + n + 1, [](const Seg& a, const Seg& b) {
        if (a.l != b.l) return a.l < b.l;
        return a.r > b.r;
    });

    int i = 1;
    long long cur = (long long)L - 1;
    int ans = 0;

    while (cur < R) {
        long long best = cur;
        while (i <= n && seg[i].l <= cur + 1) {
            best = max(best, (long long)seg[i].r);
            i++;
        }
        if (best == cur) return -1;
        cur = best;
        ans++;
    }
    return ans;
}
```

这个模板默认整数闭区间 `[L,R]`。如果区间是实数或闭开边界，`cur + 1` 要按题意改成 `seg[i].l <= cur`。

## 2. 双指针配对：最少船

每艘船最多两人，重量和不超过 `limit`，求最少船数。

```cpp
int min_boats(int weight[], int n, int limit) {
    sort(weight + 1, weight + n + 1);
    int l = 1;
    int r = n;
    int ans = 0;

    while (l <= r) {
        if ((long long)weight[l] + weight[r] <= limit) {
            l++;
            r--;
        } else {
            r--;
        }
        ans++;
    }
    return ans;
}
```

不变量：最重的人必须上船；如果能和最轻的人配，就配掉最轻的，否则最重的人只能单独走。

## 3. 二分答案 + 贪心 check

最大化最小距离：给若干位置，选 `k` 个点，使相邻距离至少 `dist` 是否可行。

```cpp
bool can_pick_with_distance(int x[], int n, int k, int dist) {
    int cnt = 1;
    int last = x[1];
    for (int i = 2; i <= n; i++) {
        if (x[i] - last >= dist) {
            cnt++;
            last = x[i];
        }
    }
    return cnt >= k;
}

int maximize_min_distance(int x[], int n, int k) {
    sort(x + 1, x + n + 1);
    int lo = 0;
    int hi = x[n] - x[1];
    while (lo < hi) {
        int mid = (lo + hi + 1) / 2;
        if (can_pick_with_distance(x, n, k, mid)) lo = mid;
        else hi = mid - 1;
    }
    return lo;
}
```

## 4. 截止时间收益最大：DSU 找空位

每个任务耗时 1 天，有截止时间和收益，每天最多做一个任务。按收益从大到小，尽量塞到不超过 deadline 的最晚空位。

```cpp
struct Job {
    int deadline;
    int profit;
};

struct SlotDSU {
    vector<int> fa;

    void init(int n) {
        fa.resize(n + 1);
        iota(fa.begin(), fa.end(), 0);
    }

    int find(int x) {
        while (x != fa[x]) {
            fa[x] = fa[fa[x]];
            x = fa[x];
        }
        return x;
    }

    bool occupy(int x) {
        int p = find(x);
        if (p == 0) return false;
        fa[p] = find(p - 1);
        return true;
    }
};

long long max_profit_jobs(vector<Job> jobs) {
    int max_deadline = 0;
    for (auto job : jobs) max_deadline = max(max_deadline, job.deadline);
    int limit = min(max_deadline, (int)jobs.size());

    sort(jobs.begin(), jobs.end(), [](const Job& a, const Job& b) {
        if (a.profit != b.profit) return a.profit > b.profit;
        return a.deadline < b.deadline;
    });

    SlotDSU dsu;
    dsu.init(limit);

    long long ans = 0;
    for (auto job : jobs) {
        if (job.deadline <= 0 || job.profit <= 0) continue;
        int slot = min(job.deadline, limit);
        if (dsu.occupy(slot)) ans += job.profit;
    }
    return ans;
}
```

## 5. 相邻交换排序思路

当题目问“怎样排序使总代价最小”，常用相邻交换。比较相邻两个元素 `a,b`，看顺序 `a,b` 和 `b,a` 哪个总代价小，再推出排序比较函数。

示例：若代价是等待时间总和，短任务优先通常更好。

```cpp
long long min_total_waiting_time(vector<int> t) {
    sort(t.begin(), t.end());
    long long elapsed = 0;
    long long ans = 0;
    for (int x : t) {
        ans += elapsed;
        elapsed += x;
    }
    return ans;
}
```

常见坑：

- 区间覆盖和区间选点不是一个模型：覆盖整段选“最远右端”，选点覆盖区间选“当前右端点”。
- 双指针配对必须先排序。
- 二分答案的 `check` 必须有单调性：可行后更宽松也可行，或不可行后更严格也不可行。
- 截止时间收益最大里要放到“不超过 deadline 的最晚空位”，不是最早空位。
- 相邻交换推出的比较函数不能写 `<=`。

暴力/部分分替代：

- `n <= 20`：子集枚举检查区间覆盖或任务收益。
- 配对题小数据可 DFS 枚举配对。
- 二分答案不会写时，先枚举小答案或写贪心构造。
- 截止时间任务小数据可枚举任务子集，再按 deadline 排序验证。

升级方向：

```text
区间覆盖小暴力 -> 按左端排序 + 选最远右端
配对暴力 -> 排序双指针
枚举答案 -> 二分答案 + 贪心 check
收益任务枚举 -> 收益排序 + DSU 找空位
排序猜想 -> 相邻交换推出比较函数
```

最小测试样例：

```text
区间覆盖 [1,10]:
[1,3] [2,6] [4,10]
输出：3

最少船:
weights = 3 2 2 1, limit = 3
输出：3

截止时间收益:
(deadline=1, profit=10), (deadline=1, profit=20), (deadline=2, profit=5)
输出：25
```
