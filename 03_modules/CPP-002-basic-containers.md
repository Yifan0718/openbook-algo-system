# CPP-002 vector/string/pair/tuple 基础容器

模块编号：CPP-002

模块名称：`vector` / `string` / `pair` / `tuple` 基础容器

标签：vector、string、pair、tuple、结构化绑定、1-index 数组

一句话用途：把题目输入整理成全卷统一的数组、字符串、二元组和多元组形态。

题面触发词：数组、序列、字符串、坐标、物品属性、二元关系、三元状态、按多个字段保存。

什么时候用：需要保存一串数、一张表、一个字符串、若干 `(值, 编号)` 或 `(x, y, w)` 记录时。

不要什么时候用：需要频繁在中间插入删除且数据量很大时，优先考虑链式结构或其他专用数据结构；需要自动去重/排序时用 `set/map`。

复杂度：`vector` 尾部插入均摊 `O(1)`，随机访问 `O(1)`；`string` 下标访问 `O(1)`；`pair/tuple` 只是打包字段。

数据范围参考：`n <= 2e5` 常用 `vector`；二维 `n*m` 容器先估算内存，`int` 约 4 字节，`long long` 约 8 字节。

依赖的标准容器：`vector`、`string`、`pair`、`tuple`。

输入如何整理：

- 数组：上限明确时优先 `static ll a[MAXN]`；运行时尺寸才用 `vector<ll> a(n + 1)`，都使用 `1..n`。
- 字符串：`string s`，使用 C++ 自然 `0..s.size()-1`。
- 二元记录：`vector<pair<ll, int>> v` 保存 `(值, 原编号)`。
- 多字段记录：简单时用 `tuple`，字段含义复杂时改 `struct`。

接口：

- `a[i]`：访问 1-index 数组元素。
- `s[i]`：访问 0-index 字符。
- `v.push_back(x)`：尾部加入；若元素有题面编号，记录里的 `id` 仍保存 `1..n`。
- `v.size()`：元素个数，比较或循环时常转成 `int`。
- `auto [x, y] = p`：拆 `pair`。
- `auto [x, y, z] = t`：拆 `tuple`。

输出能力：按题面输出数组、字符串、记录的字段；容器本身不能直接 `cout`，要循环输出。

下游可接：排序、二分、前缀和、树状数组、线段树、DP、图论边表。

可拼接模块：CPP-003 排序二分、CPP-007 坐标压缩、CPP-008 整数溢出。

模板代码：

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using pii = pair<int, int>;
using pll = pair<ll, ll>;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    string s;
    cin >> n >> s;

    vector<ll> a(n + 1);
    for (int i = 1; i <= n; i++) cin >> a[i];

    vector<pair<ll, int>> value_id;
    for (int i = 1; i <= n; i++) {
        value_id.push_back({a[i], i});
    }

    if (n == 0 || s.empty() || value_id.empty()) return 0;

    tuple<int, int, ll> state = {1, (int)s.size(), a[1]};
    auto [l, r, val] = state;

    cout << s[0] << ' ' << value_id[0].first << ' ' << value_id[0].second << '\n';
    cout << l << ' ' << r << ' ' << val << '\n';

    return 0;
}
```

调用示例：

```cpp
const int MAXN = 1000 + 5;
const int MAXM = 1000 + 5;
static int grid[MAXN][MAXM];

for (int i = 1; i <= n; i++) {
    for (int j = 1; j <= m; j++) {
        cin >> grid[i][j];
    }
}

vector<tuple<int, int, ll>> edges;
edges.push_back({u, v, w});
for (auto [from, to, weight] : edges) {
    // 使用 from, to, weight
}
```

常见坑：

- 普通数组/DP 表不要写 `vector<int> a(n)` 后再按 `1..n` 用；上限明确直接全局静态数组，动态 vector 也开 `n + 1`。
- `s.size()` 是无符号类型，倒着循环时先写 `int len = (int)s.size()`。
- 空 `vector/string` 不能访问 `[0]`、`back()`。
- `pair` 默认先按 `first` 排，再按 `second` 排。
- `tuple` 字段多了可读性会变差，复杂记录建议写 `struct`。
- `vector` 扩容可能让旧引用、旧指针失效；保存下标通常更稳。

暴力/部分分替代：小数据直接用 `vector` 暴力双循环；记录原编号时用 `pair` 避免排序后丢失位置。

升级方向：`vector` 接前缀和/树状数组/线段树；`pair/tuple` 接排序、离线查询、Kruskal 边表。

最小测试样例：

```text
输入
3 abc
5 6 7

输出
a 5 1
1 3 5
```
