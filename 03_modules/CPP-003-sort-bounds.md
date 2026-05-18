# CPP-003 sort/lambda/比较函数/lower_bound/upper_bound

模块编号：CPP-003

模块名称：排序、lambda、自定义比较与二分位置

标签：sort、stable_sort、lambda、比较函数、lower_bound、upper_bound、离线排序

一句话用途：处理“排序后扫描”“按多个关键字排序”“在有序数组里找位置/计数”。

题面触发词：从小到大、从大到小、排名、第一个不小于、最后一个不大于、区间内有多少数、按分数排序、离线处理。

什么时候用：需要重排数组、按字段优先级排序、在有序 `vector` 中查找边界时。

不要什么时候用：数据会频繁动态插入删除并保持有序时，用 `set/multiset/map`；数组未排序时不能直接二分。

复杂度：排序 `O(n log n)`；`lower_bound/upper_bound` 每次 `O(log n)`。

数据范围参考：`n <= 2e5` 排序很常见；`n <= 1e6` 也通常可接受，但注意常数和内存。

依赖的标准容器：`vector`、`pair`、`tuple`、自定义 `struct`。

输入如何整理：先把需要排序/二分的值放入 `vector`；需要保留原位置就存 `(值, 原编号)`。

接口：

- `sort(v.begin(), v.end())`：升序。
- `sort(v.rbegin(), v.rend())`：降序，适合基础类型。
- `sort(v.begin(), v.end(), cmp)`：自定义比较。
- `lower_bound(v.begin(), v.end(), x)`：第一个 `>= x`。
- `upper_bound(v.begin(), v.end(), x)`：第一个 `> x`。

输出能力：可输出排序后的顺序、排名、满足区间 `[L, R]` 的数量或位置。

下游可接：坐标压缩、贪心、离线查询、双指针、Kruskal、扫描线。

可拼接模块：CPP-002 基础容器、CPP-005 关联容器、CPP-007 坐标压缩。

模板代码：

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

struct Node {
    int id;
    ll score;
    int age;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;

    vector<Node> a(n + 1);
    vector<ll> xs;
    for (int i = 1; i <= n; i++) {
        cin >> a[i].score >> a[i].age;
        a[i].id = i;
        xs.push_back(a[i].score);
    }

    sort(a.begin() + 1, a.end(), [](const Node &x, const Node &y) {
        if (x.score != y.score) return x.score > y.score; // 分数高在前
        if (x.age != y.age) return x.age < y.age;         // 年龄小在前
        return x.id < y.id;                               // 编号小在前
    });

    sort(xs.begin(), xs.end());

    ll L, R;
    cin >> L >> R;
    int left = (int)(lower_bound(xs.begin(), xs.end(), L) - xs.begin());
    int right = (int)(upper_bound(xs.begin(), xs.end(), R) - xs.begin());
    int count_in_range = right - left;

    if (n == 0) return 0;
    cout << a[1].id << '\n';
    cout << count_in_range << '\n';

    return 0;
}
```

调用示例：

```cpp
vector<int> v = {1, 2, 2, 4, 7};
int x = 2;
int first_ge = (int)(lower_bound(v.begin(), v.end(), x) - v.begin()); // 1
int first_gt = (int)(upper_bound(v.begin(), v.end(), x) - v.begin()); // 3
int count_x = first_gt - first_ge;                                    // 2
```

常见坑：

- 二分前必须保证 `vector` 已经按同一种规则排序。
- 自定义比较必须写严格顺序：相等时返回 `false`，不要写 `<=`。
- 降序数组不能直接用默认 `lower_bound`，除非额外传同样的比较规则；考场上更推荐升序二分。
- `lower_bound` 返回的是迭代器，转下标要减 `begin()`。
- 返回 `v.end()` 表示没找到可用位置，不能直接解引用。
- 排序会打乱原顺序，需要原编号时先存 `id`。

暴力/部分分替代：小数据可每次线性扫描找第一个满足条件的位置，复杂度 `O(nq)`。

升级方向：大量区间计数接坐标压缩 + 树状数组；动态有序接 `set/multiset/map`。

最小测试样例：

```text
输入
3
90 18
90 17
80 20
85 100

输出
2
2
```
