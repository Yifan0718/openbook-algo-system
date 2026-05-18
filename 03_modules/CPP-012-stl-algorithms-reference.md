# CPP-012 STL 常用算法速查

模块编号：CPP-012

模块名称：常用 STL 算法速查模块

标签：C++17、STL、algorithm、numeric、排序、二分、去重、排列、前缀和、考场速查

一句话用途：把常用 STL 算法按“考场能直接抄”的方式集中列出，快速拿排序、二分、统计、去重、排列和前缀处理的基础分。

题面触发词：排序、稳定排序、去重、删除所有、查找第一个、区间计数、是否存在、最大最小、第 k 小、下一个排列、旋转数组、填充、编号、前缀和、总和、gcd、lcm。

什么时候用：数据已经放进 `vector/string/array`，需要对一段连续区间做排序、查找、统计、批量赋值或数值累加时。

不要什么时候用：需要频繁动态插入删除并保持有序时，优先用 `set/multiset/map`；需要复杂区间修改查询时，优先用树状数组、Segment Tree 或 Sparse Table。

复杂度：

- 排序类：`sort/stable_sort/nth_element` 通常 `O(n log n)`，其中 `nth_element` 平均 `O(n)`。
- 二分类：`lower_bound/upper_bound/binary_search/equal_range` 为 `O(log n)`，前提是区间已按同一规则有序。
- 线性扫描类：`reverse/unique/erase-remove/rotate/fill/iota/accumulate/partial_sum/count/find/count_if/find_if/all_of/any_of/none_of` 为 `O(n)`。
- `gcd/lcm` 为 `O(log min(a,b))`。

数据范围参考：

- `n <= 2e5`：排序、线性扫描、前缀和都很稳。
- `n <= 1e6`：排序仍常见，注意常数、内存和多测清空。
- `q` 很大且每次问区间数量：先排序，再用二分，避免每次线性扫。

依赖的标准容器：

- `vector`、`array`、`string`：连续区间算法最常用。
- `deque`：也支持随机访问迭代器，可用于 `sort`，但算法题通常转 `vector` 更直观。
- `set/map` 等有序容器有自己的 `lower_bound`，不要把全局 `lower_bound` 当成 `O(log n)` 用在普通双向迭代器上。

接口：

```text
sort(begin, end)
lower_bound(begin, end, x)
v.erase(unique(begin, end), end)
v.erase(remove(begin, end, x), end)
iota(begin, end, start)
accumulate(begin, end, 0LL)
partial_sum(begin, end, output_begin)
```

依赖头文件：

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;
```

## 1. 考场总表

| 算法 | 常用写法 | 用途 | 坑点 |
|---|---|---|---|
| `sort` | `sort(v.begin(), v.end())` | 升序排序 | 会打乱原顺序 |
| `stable_sort` | `stable_sort(v.begin(), v.end(), cmp)` | 相等元素保持原相对顺序 | 比 `sort` 常数大 |
| `reverse` | `reverse(v.begin(), v.end())` | 整段反转 | 区间仍是半开 `[l,r)` |
| `unique` | `v.erase(unique(v.begin(), v.end()), v.end())` | 删除相邻重复 | 要“值去重”通常先排序 |
| `erase-remove` | `v.erase(remove(v.begin(), v.end(), x), v.end())` | 删除所有等于 `x` 的元素 | `remove` 不会真的缩短容器 |
| `lower_bound` | `lower_bound(v.begin(), v.end(), x)` | 第一个 `>= x` | 必须有序 |
| `upper_bound` | `upper_bound(v.begin(), v.end(), x)` | 第一个 `> x` | 必须有序 |
| `binary_search` | `binary_search(v.begin(), v.end(), x)` | 判断 `x` 是否存在 | 只返回 `bool` |
| `equal_range` | `equal_range(v.begin(), v.end(), x)` | 一次拿 `[第一个 >=x, 第一个 >x)` | 计数用 `second - first` |
| `min/max` | `min(a,b)`, `max(a,b)` | 两个值取较小/较大 | 类型尽量一致 |
| `minmax_element` | `minmax_element(v.begin(), v.end())` | 一次找最小和最大元素位置 | 空区间不能解引用 |
| `nth_element` | `nth_element(v.begin(), v.begin()+k, v.end())` | 把 0-index 下标 `k` 的元素放到位，也就是第 `k+1` 小 | 题目问第 k 小时通常写 `begin()+k-1` |
| `next_permutation` | `next_permutation(v.begin(), v.end())` | 下一个字典序排列 | 枚举全排列前先排序 |
| `prev_permutation` | `prev_permutation(v.begin(), v.end())` | 上一个字典序排列 | 降序起点才能枚举全部逆向排列 |
| `rotate` | `rotate(v.begin(), v.begin()+k, v.end())` | 把中点搬到开头 | `k` 是迭代器位置，不是次数本身 |
| `fill` | `fill(v.begin(), v.end(), val)` | 批量赋值 | 多维数组更推荐循环逐行填 |
| `iota` | `iota(v.begin(), v.end(), start)` | 生成连续编号 | 头文件在 `numeric`，`bits` 已含 |
| `accumulate` | `accumulate(v.begin(), v.end(), 0LL)` | 求和或折叠 | 初值决定返回类型 |
| `partial_sum` | `partial_sum(v.begin(), v.end(), pre.begin()+1)` | 前缀和 | 目标空间要提前开够 |
| `gcd` | `gcd(a,b)` | 最大公约数 | C++17 在 `<numeric>` |
| `lcm` | `lcm(a,b)` | 最小公倍数 | 可能溢出 |
| `count` | `count(v.begin(), v.end(), x)` | 统计等于 `x` 的数量 | 线性复杂度 |
| `find` | `find(v.begin(), v.end(), x)` | 找第一个等于 `x` 的位置 | 找不到返回 `end()` |
| `count_if` | `count_if(v.begin(), v.end(), pred)` | 统计满足条件的数量 | `pred` 返回 bool |
| `find_if` | `find_if(v.begin(), v.end(), pred)` | 找第一个满足条件的位置 | 找不到返回 `end()` |
| `all_of` | `all_of(v.begin(), v.end(), pred)` | 是否全部满足 | 空区间返回 `true` |
| `any_of` | `any_of(v.begin(), v.end(), pred)` | 是否存在一个满足 | 空区间返回 `false` |
| `none_of` | `none_of(v.begin(), v.end(), pred)` | 是否没有元素满足 | 空区间返回 `true` |

## 2. 排序、比较函数与 lambda 正确写法

考场优先记住一句：比较函数 `cmp(a,b)` 表示“`a` 是否应该排在 `b` 前面”，相等时必须返回 `false`。

```cpp
struct Node {
    int id;
    int score;
    int age;
};

vector<Node> a;

// 分数高在前；分数相同，年龄小在前；仍相同，编号小在前。
sort(a.begin(), a.end(), [](const Node &x, const Node &y) {
    if (x.score != y.score) return x.score > y.score;
    if (x.age != y.age) return x.age < y.age;
    return x.id < y.id;
});
```

错误写法：

```cpp
// 错：相等时也可能返回 true，破坏严格弱序。
sort(a.begin(), a.end(), [](const Node &x, const Node &y) {
    return x.score >= y.score;
});
```

常用排序抄法：

```cpp
sort(v.begin(), v.end());                 // 升序
sort(v.rbegin(), v.rend());               // 降序，适合 int/ll/string/pair
stable_sort(v.begin(), v.end(), cmp);     // 相等元素保留原相对顺序
```

`pair/tuple` 默认按字典序排序：

```cpp
vector<pair<int, int>> p;
sort(p.begin(), p.end()); // 先按 first，再按 second，都是升序
```

## 3. 半开区间与闭区间换算

STL 统一使用半开区间 `[first, last)`：包含左端点，不包含右端点。

1-index 数组闭区间 `[L, R]` 换成 STL 迭代器：

```cpp
// a[0] 不用，处理 a[L] 到 a[R]
sort(a.begin() + L, a.begin() + R + 1);
reverse(a.begin() + L, a.begin() + R + 1);
fill(a.begin() + L, a.begin() + R + 1, 0);
```

静态数组也可以直接用指针：

```cpp
sort(a + L, a + R + 1);
```

半开区间 `[l, r)` 的长度永远是：

```cpp
int len = r - l;
```

二分返回下标：

```cpp
int pos = (int)(lower_bound(v.begin(), v.end(), x) - v.begin());
```

## 4. 去重与删除

值去重标准三连：

```cpp
sort(v.begin(), v.end());
v.erase(unique(v.begin(), v.end()), v.end());
```

只删除相邻重复，不排序：

```cpp
v.erase(unique(v.begin(), v.end()), v.end());
```

删除所有等于 `x` 的元素：

```cpp
v.erase(remove(v.begin(), v.end(), x), v.end());
```

按条件删除：

```cpp
v.erase(remove_if(v.begin(), v.end(), [](int x) {
    return x < 0;
}), v.end());
```

考场口令：`unique/remove/remove_if` 都只是把“保留的元素”搬到前面并返回新尾巴，真正缩短 `vector` 要再接 `erase`。

## 5. 二分查找与区间计数

前提：`v` 已经升序排序。

```cpp
sort(v.begin(), v.end());

int x;
cin >> x;

auto it1 = lower_bound(v.begin(), v.end(), x); // 第一个 >= x
auto it2 = upper_bound(v.begin(), v.end(), x); // 第一个 > x

bool ok = binary_search(v.begin(), v.end(), x);
int cnt_x = (int)(it2 - it1);
```

统计闭区间 `[L, R]` 内有多少个数：

```cpp
int cnt = (int)(upper_bound(v.begin(), v.end(), R)
              - lower_bound(v.begin(), v.end(), L));
```

`equal_range` 一次拿到等值范围：

```cpp
auto range = equal_range(v.begin(), v.end(), x);
int cnt = (int)(range.second - range.first);
```

找最后一个 `<= x` 的位置：

```cpp
auto it = upper_bound(v.begin(), v.end(), x);
if (it == v.begin()) {
    // 不存在 <= x 的元素
} else {
    --it;
    int pos = (int)(it - v.begin());
}
```

降序数组二分容易写错。考场建议：能升序就升序；如果必须降序，排序和二分要使用同一个比较规则。

```cpp
sort(v.begin(), v.end(), greater<int>());
auto it = lower_bound(v.begin(), v.end(), x, greater<int>());
```

## 6. 最大最小、第 k 小与重排

两个值取最小最大：

```cpp
int lo = min(a, b);
int hi = max(a, b);
ll best = min({x, y, z});
```

区间一次找最小最大元素位置：

```cpp
auto [mn_it, mx_it] = minmax_element(v.begin(), v.end());
if (mn_it != v.end()) {
    int mn = *mn_it;
    int mx = *mx_it;
}
```

第 `k` 小，题面 `k` 通常按 1-index 理解：

```cpp
// a[1..n]，第 k 小会被放到 a[k]
nth_element(a + 1, a + k, a + n + 1);
int kth = a[k];
```

拿最小的 `k` 个数，但这 `k` 个内部不要求有序：

```cpp
nth_element(a + 1, a + k, a + n + 1);
// a[1..k] 是 k 个较小元素，但内部乱序。
```

如果还要输出有序结果，再补一刀：

```cpp
sort(a + 1, a + k + 1);
```

`reverse` 和 `rotate`：

```cpp
reverse(v.begin(), v.end());

int k = 3;
rotate(v.begin(), v.begin() + k, v.end()); // [0,k) 搬到末尾，原 k 位置变开头
```

右旋 `k` 位：

```cpp
int n = (int)v.size();
if (n > 0) {
    k %= n;
    rotate(v.begin(), v.end() - k, v.end());
}
```

## 7. 排列枚举

从小到大枚举所有不同排列：

```cpp
sort(v.begin(), v.end());
do {
    // 使用当前排列
} while (next_permutation(v.begin(), v.end()));
```

从大到小枚举：

```cpp
sort(v.rbegin(), v.rend());
do {
    // 使用当前排列
} while (prev_permutation(v.begin(), v.end()));
```

考场提醒：全排列是阶乘复杂度，`n > 10` 通常只能拿部分分或需要换思路。

## 8. 批量赋值、编号、求和与前缀和

批量赋值：

```cpp
fill(v.begin(), v.end(), 0);
```

二维 `vector` 清空：

```cpp
for (auto &row : dp) fill(row.begin(), row.end(), INF);
```

生成连续编号：

```cpp
static int id[MAXN];
iota(id + 1, id + n + 1, 1); // 1,2,...,n
```

求和必须注意初值类型：

```cpp
ll sum = accumulate(v.begin(), v.end(), 0LL);
```

前缀和，`pre[0]=0`，`pre[i]` 表示 `a[1..i]` 之和：

```cpp
static ll a[MAXN], pre[MAXN];
partial_sum(a + 1, a + n + 1, pre + 1);

// 1-index 闭区间 [L, R] 的和
ll ans = pre[R] - pre[L - 1];
```

如果原数组是 `int` 且和可能超过 `int`，考场更稳的写法是手写 `long long` 前缀：

```cpp
static ll pre[MAXN];
for (int i = 1; i <= n; i++) pre[i] = pre[i - 1] + a[i];
```

自定义累加：

```cpp
ll total_abs = accumulate(v.begin(), v.end(), 0LL, [](ll s, int x) {
    return s + llabs((ll)x);
});
```

## 9. gcd 与 lcm

C++17 可直接用：

```cpp
ll g = gcd(a, b);
ll l = lcm(a, b);
```

防溢出版 `lcm` 更适合考场：

```cpp
ll lcm_limit(ll a, ll b, ll limit) {
    if (a == 0 || b == 0) return 0;
    __int128 aa = a, bb = b;
    if (aa < 0) aa = -aa;
    if (bb < 0) bb = -bb;
    ll g = gcd(a, b);
    aa /= g;
    __int128 lim = limit;
    ll over = (limit == LLONG_MAX ? limit : limit + 1);
    if (bb != 0 && aa > lim / bb) return over;
    __int128 res = aa * bb;
    if (res > lim) return over;
    return (ll)res;
}
```

多个数合并：

```cpp
ll g = 0;
for (ll x : v) g = gcd(g, x);

ll l = 1;
for (ll x : v) l = lcm_limit(l, x, 4'000'000'000'000'000'000LL);
```

## 10. 统计、查找与判定

线性统计：

```cpp
int c = (int)count(v.begin(), v.end(), x);
int odd = (int)count_if(v.begin(), v.end(), [](int x) {
    return x % 2 != 0;
});
```

线性查找：

```cpp
auto it = find(v.begin(), v.end(), x);
if (it != v.end()) {
    int pos = (int)(it - v.begin());
}

auto first_big = find_if(v.begin(), v.end(), [](int x) {
    return x > 100;
});
```

全部满足：

```cpp
bool all_pos = all_of(v.begin(), v.end(), [](int x) {
    return x > 0;
});
```

存在满足：

```cpp
bool has_even = any_of(v.begin(), v.end(), [](int x) {
    return x % 2 == 0;
});

bool no_negative = none_of(v.begin(), v.end(), [](int x) {
    return x < 0;
});
```

考场选择：

- 无序数组找一次：`find/count/all_of/any_of`，简单稳。
- 有序数组查很多次：`lower_bound/upper_bound/binary_search/equal_range`。
- 需要频繁查存在性且不关心顺序：`unordered_set`。

## 11. 综合模板

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;
const int MAXN = 200000 + 5;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, q;
    cin >> n >> q;

    static ll a[MAXN], sorted[MAXN], pre[MAXN];
    for (int i = 1; i <= n; i++) cin >> a[i];

    for (int i = 1; i <= n; i++) sorted[i] = a[i];
    sort(sorted + 1, sorted + n + 1);

    partial_sum(a + 1, a + n + 1, pre + 1);

    while (q--) {
        ll L, R;
        cin >> L >> R;

        int cnt_value_range =
            (int)(upper_bound(sorted + 1, sorted + n + 1, R)
                - lower_bound(sorted + 1, sorted + n + 1, L));

        cout << cnt_value_range << '\n';
    }

    return 0;
}
```

调用示例：

```cpp
int v[6] = {0, 3, 1, 2, 2, 5};
int n = 5;

sort(v + 1, v + n + 1);                            // 1 2 2 3 5
int cnt2 = (int)(upper_bound(v + 1, v + n + 1, 2)
               - lower_bound(v + 1, v + n + 1, 2)); // 2

n = unique(v + 1, v + n + 1) - (v + 1);             // v[1..n] = 1 2 3 5

bool has3 = binary_search(v + 1, v + n + 1, 3);     // true
ll sum = accumulate(v + 1, v + n + 1, 0LL);         // 11
```

常见坑：

- STL 区间是半开 `[first,last)`；闭区间 `[L,R]` 要写到 `begin()+R+1`。
- `lower_bound/upper_bound/binary_search/equal_range` 只能用于已按同一规则排序的区间。
- 自定义 `cmp` 不能写 `<=` 或 `>=`，相等必须返回 `false`。
- `sort` 不稳定；相等元素要保留原相对顺序时用 `stable_sort`。
- `unique` 只删除相邻重复；值去重前先 `sort`。
- `remove/remove_if` 不会改变 `vector` 长度，必须配合 `erase`。
- `find/lower_bound/minmax_element` 返回迭代器，解引用前检查是否为 `end()`。
- `accumulate(v.begin(), v.end(), 0)` 会按 `int` 累加，容易溢出；写 `0LL`。
- `partial_sum` 的累加类型来自输入元素，`vector<int>` 求大前缀和时优先手写 `long long` 循环。
- `nth_element` 只能保证第 `k` 小到位，不能保证整段有序。
- `next_permutation` 要从升序开始才会枚举所有排列。
- `lcm` 可能溢出，涉及上限判断时用 `a / gcd(a,b) * b` 并先检查乘法。
- 空区间下 `all_of` 返回 `true`，`any_of` 返回 `false`，不要被边界样例骗。

暴力/部分分替代：

- 小数据查询区间数量：每次线性扫 `O(nq)`。
- 小数据找第 `k` 小：每次完整 `sort`。
- 小数据判断存在：直接 `find`，不用先建复杂结构。

升级方向：

- 大量动态插入删除 + 有序查询：`multiset` 或平衡树思路。
- 大量区间和/区间修改：树状数组或 Segment Tree。
- 大量区间最值静态查询：Sparse Table。
- 排序后还要映射回原值范围：接坐标压缩模块。

最小测试样例：

```text
v = {3, 1, 2, 2, 5}
sort -> {1, 2, 2, 3, 5}
unique after erase -> {1, 2, 3, 5}
count of [2,3] by bounds -> 2
accumulate with 0LL -> 11
gcd(12,18) -> 6
lcm(12,18) -> 36
```
