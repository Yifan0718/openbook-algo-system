# GREEDY-00 贪心路由与短模板

模块编号：GREEDY-00

模块名称：贪心路由与短模板

标签：贪心、区间选点、活动选择、排序贪心、堆贪心、反悔贪心

一句话用途：看到“每次选当前最优”或“排序后一扫”时，先用本表判断是哪类贪心，再抄最短模板。

题面触发词：

- 最少点覆盖所有区间、最多不重叠活动。
- 按截止时间、结束时间、代价、收益排序。
- 每次取最小、每次取最大、合并代价最小。
- 先选进去，超过限制再删掉一个最差的。

什么时候用：

- 局部选择可以通过交换论证变成全局最优。
- 题面有明确的“最早结束”“当前最小”“保留最好若干个”等信号。
- 数据范围要求 `O(n log n)` 或 `O(n)`，暴力枚举会超时。
- 可以把所有对象先排序，再从左到右扫描。

不要什么时候用：

- 当前选择会影响未来状态，且没有明显可交换性。
- 需要记录多个维度历史状态，通常是 DP。
- 图上最短路、连通性、树形依赖不要硬套普通贪心。
- 只凭样例猜规则，不能解释为什么删这个、选这个。

复杂度：

- 排序贪心：`O(n log n)`。
- 区间选点/活动选择：排序 `O(n log n)`，扫描 `O(n)`。
- 堆贪心：`O(n log n)`。
- 反悔贪心：排序加堆，`O(n log n)`。

数据范围参考：

- `n <= 2e5`：排序、堆贪心常用。
- `n <= 1e6`：能线性更好，排序也可能可过但注意常数。
- `n <= 20`：可先暴力枚举验证贪心猜想。

依赖的标准容器：

- `vector<Seg>`：区间，默认 1-index。
- `vector<Item>`：多字段任务。
- `priority_queue`：堆贪心和反悔贪心。

输入如何整理：

```cpp
struct Seg {
    int l;
    int r;
    int id;
};

int n;
cin >> n;
vector<Seg> seg(n + 1);
for (int i = 1; i <= n; i++) {
    cin >> seg[i].l >> seg[i].r;
    seg[i].id = i;
}
```

整理顺序：

1. 先把对象变成 `struct`，保留 `id`。
2. 明确排序关键字：结束时间、开始时间、截止时间、收益、代价。
3. 扫描时维护当前答案、当前资源或堆。
4. 遇到超限时，反悔贪心从堆里删掉最差选择。

接口：

```text
choose_points(seg) -> 闭区间最少选点覆盖，每次选当前右端点。
activity_select(seg) -> 半开区间 [l,r) 或允许端点相接时的最多互不冲突活动。
min_merge_cost(a) -> 每次合并最小两项，Huffman/合并果子。
min_rooms(seg) -> 半开区间 [l,r) 或结束即释放资源时的最少会议室/机器数。
regret_max_count(course) -> 截止时间内最多完成任务，超时删耗时最大。
```

输出能力：

- 输出最少点数、最多活动数、最小合并代价。
- 输出所选点、所选活动编号。
- 输出最少资源数或最多可完成任务数。

下游可接：

- CPP-003 排序与比较函数。
- CPP-004 优先队列。
- BRUTE 暴力枚举验证。
- 二分答案中的 `check`。
- GREEDY-01 贪心与 DP 判别卡：证明不了贪心时，回到 DFS/DP。

可拼接模块：

| 题面信号 | 路由 | 核心选择 |
|---|---|---|
| 最少点覆盖所有闭区间 | 区间选点 | 按右端点升序，没覆盖就选右端点 |
| 最多不重叠活动 | 活动选择 | 按结束时间升序，能接就选 |
| 排队等待、按代价处理 | 排序贪心 | 按题面最紧约束排序后扫描 |
| 合并果子、每次合并代价 | 堆贪心 | 每次取两个最小 |
| 最少会议室/机器 | 堆贪心 | 小根堆维护当前结束时间 |
| 截止时间内最多任务 | 反悔贪心 | 按截止时间扫，超时删耗时最大 |
| 最多收益且数量/时间受限 | 反悔贪心 | 先放入堆，超限删最差收益或最大耗时 |

模板代码：

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

struct Seg {
    int l;
    int r;
    int id;
};

struct Course {
    int t;
    int d;
    int id;
};

bool by_right(const Seg &a, const Seg &b) {
    if (a.r != b.r) return a.r < b.r;
    return a.l < b.l;
}

vector<int> choose_points(vector<Seg> seg) {
    int n = (int)seg.size() - 1;
    sort(seg.begin() + 1, seg.end(), by_right);

    vector<int> ans;
    int last = numeric_limits<int>::min();
    for (int i = 1; i <= n; i++) {
        if (seg[i].l > last) {
            last = seg[i].r;
            ans.push_back(last);
        }
    }
    return ans;
}

int activity_select(vector<Seg> seg) {
    int n = (int)seg.size() - 1;
    sort(seg.begin() + 1, seg.end(), by_right);

    int cnt = 0;
    int last_end = numeric_limits<int>::min();
    for (int i = 1; i <= n; i++) {
        if (seg[i].l >= last_end) {
            cnt++;
            last_end = seg[i].r;
        }
    }
    return cnt;
}

ll min_merge_cost(const vector<ll> &a) {
    int n = (int)a.size() - 1;
    priority_queue<ll, vector<ll>, greater<ll>> pq;
    for (int i = 1; i <= n; i++) {
        pq.push(a[i]);
    }

    ll ans = 0;
    while (pq.size() > 1) {
        ll x = pq.top();
        pq.pop();
        ll y = pq.top();
        pq.pop();
        ans += x + y;
        pq.push(x + y);
    }
    return ans;
}

int min_rooms(vector<Seg> seg) {
    int n = (int)seg.size() - 1;
    sort(seg.begin() + 1, seg.end(), [](const Seg &a, const Seg &b) {
        if (a.l != b.l) return a.l < b.l;
        return a.r < b.r;
    });

    priority_queue<int, vector<int>, greater<int>> ends;
    int ans = 0;
    for (int i = 1; i <= n; i++) {
        // 半开区间 [l,r) 可用 <=；闭区间 [l,r] 且端点相同算冲突时改成 <。
        while (!ends.empty() && ends.top() <= seg[i].l) {
            ends.pop();
        }
        ends.push(seg[i].r);
        ans = max(ans, (int)ends.size());
    }
    return ans;
}

int regret_max_count(vector<Course> c) {
    int n = (int)c.size() - 1;
    sort(c.begin() + 1, c.end(), [](const Course &a, const Course &b) {
        if (a.d != b.d) return a.d < b.d;
        return a.t < b.t;
    });

    priority_queue<int> chosen_time;
    ll used = 0;
    for (int i = 1; i <= n; i++) {
        used += c[i].t;
        chosen_time.push(c[i].t);
        if (used > c[i].d) {
            used -= chosen_time.top();
            chosen_time.pop();
        }
    }
    return (int)chosen_time.size();
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<Seg> seg(n + 1);
    for (int i = 1; i <= n; i++) {
        cin >> seg[i].l >> seg[i].r;
        seg[i].id = i;
    }

    cout << choose_points(seg).size() << '\n';
    cout << activity_select(seg) << '\n';

    return 0;
}
```

调用示例：

```cpp
// 区间选点：输出最少点数和点的位置。
vector<int> pts = choose_points(seg);
cout << pts.size() << '\n';
for (int x : pts) cout << x << ' ';
cout << '\n';

// 合并果子。
vector<ll> a(n + 1);
for (int i = 1; i <= n; i++) cin >> a[i];
cout << min_merge_cost(a) << '\n';

// 反悔贪心：课程 t 为耗时，d 为截止时间。
vector<Course> c(n + 1);
for (int i = 1; i <= n; i++) {
    cin >> c[i].t >> c[i].d;
    c[i].id = i;
}
cout << regret_max_count(c) << '\n';
```

常见坑：

- 区间选点是闭区间覆盖，判断通常是 `l > last` 才需要新点。
- 活动选择是否允许首尾相接要看题面；允许用 `l >= last_end`，不允许改成 `l > last_end`。
- 排序比较函数不能写 `<=`。
- 贪心排序关键字错了很难从样例看出，至少用小数据暴力对拍。
- 堆贪心默认 `priority_queue` 是大根堆，小根堆要写 `greater<T>`。
- 反悔贪心的堆里存“将来要删的最差项”：超时删最大耗时，保收益删最小收益。
- 区间端点可能到 `1e9`，端点用 `int` 多数够；代价、答案用 `long long`。
- 无法说出交换论证、领先性或反悔不变量时，不要硬套贪心，先用小数据暴力或 DP-25 记忆化保底。

暴力/部分分替代：

- `n <= 20`：枚举子集，检查覆盖或互不冲突，验证贪心。
- 合并果子小数据：每次线性找两个最小，`O(n^2)`。
- 会议室小数据：按时间点或每个活动扫描已有房间。
- 截止时间任务小数据：全排列或子集枚举，检查能否按截止时间完成。

升级方向：

```text
枚举所有选法 -> 按右端点排序的区间贪心
每次线性找最小 -> priority_queue
排序后超限失败 -> 加堆做反悔
贪心无法证明 -> 改 DFS/DP，先拿小数据
```

最小测试样例：

```text
输入
3
1 3
2 5
6 7

输出
2
2
```

补充自测：

```text
区间选点：[1,3],[2,5],[6,7] -> 选点 3,7
活动选择：[1,3],[2,5],[6,7] -> 最多 2 个
合并果子：1 2 3 4 -> 19
反悔任务：(3,5),(4,6),(2,6) -> 最多 2 个
```
