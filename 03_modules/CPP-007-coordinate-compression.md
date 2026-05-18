# CPP-007 坐标压缩 Compressor

模块编号：CPP-007

模块名称：坐标压缩

标签：坐标压缩、离散化、lower_bound、upper_bound、1-index 编号

一句话用途：把很大的值域压成 `1..k`，方便接 树状数组、线段树、差分和数组。

题面触发词：坐标很大、值域到 `1e9/1e18`、只出现少量点、离散化、排名、逆序对、区间覆盖、扫描线。

什么时候用：值很大但不同值数量不多，并且需要用数组下标维护这些值时。

不要什么时候用：原值之间的距离有实际长度意义且需要保留每段长度时，必须额外保存相邻原坐标差；不能只看压缩编号差。

复杂度：建表排序 `O(n log n)`；每次取编号 `O(log n)`。

数据范围参考：原坐标可到 `1e18`；不同坐标数 `k` 通常 `<= 2e5` 时适合压缩后接数组结构。

依赖的标准容器：`vector<ll>`、`sort`、`unique`、`lower_bound`、`upper_bound`。

输入如何整理：先收集所有会用到的坐标和值；如果是区间覆盖题，通常要收集端点，必要时也收集 `r + 1`。

接口：

- `build(v)`：用所有候选坐标建表。
- `id(x)`：`x` 确定出现过时取 1-index 编号。
- `lower_id(x)`：第一个原值 `>= x` 的编号。
- `upper_id(x)`：最后一个原值 `<= x` 的编号。
- `val(pos)`：压缩编号还原成原值。
- `size()`：压缩后坐标数量。

输出能力：输出压缩编号、排名、区间 `[L, R]` 对应的压缩下标范围。

下游可接：树状数组、线段树、差分、扫描线、逆序对、动态排名。

可拼接模块：CPP-003 排序二分、CPP-008 整数溢出、数据结构卷 树状数组/SegmentTree。

模板代码：

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

struct Compressor {
    vector<ll> xs;

    void build(vector<ll> v) {
        xs = v;
        sort(xs.begin(), xs.end());
        xs.erase(unique(xs.begin(), xs.end()), xs.end());
    }

    int id(ll x) const {
        return (int)(lower_bound(xs.begin(), xs.end(), x) - xs.begin()) + 1;
    }

    int lower_id(ll x) const {
        return (int)(lower_bound(xs.begin(), xs.end(), x) - xs.begin()) + 1;
    }

    int upper_id(ll x) const {
        return (int)(upper_bound(xs.begin(), xs.end(), x) - xs.begin());
    }

    ll val(int pos) const {
        return xs[pos - 1];
    }

    int size() const {
        return (int)xs.size();
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;

    vector<ll> a(n + 1), all;
    for (int i = 1; i <= n; i++) {
        cin >> a[i];
        all.push_back(a[i]);
    }

    Compressor comp;
    comp.build(all);

    for (int i = 1; i <= n; i++) {
        cout << comp.id(a[i]) << (i == n ? '\n' : ' ');
    }

    ll L, R;
    cin >> L >> R;
    int l = comp.lower_id(L);
    int r = comp.upper_id(R);
    cout << (l <= r ? r - l + 1 : 0) << '\n';

    return 0;
}
```

调用示例：

```cpp
Compressor comp;
comp.build(all_values);

int pos = comp.id(x);        // x 出现过
int l = comp.lower_id(L);    // 第一个 >= L
int r = comp.upper_id(R);    // 最后一个 <= R
if (l <= r) {
    // 压缩区间 [l, r] 非空
}
```

常见坑：

- 只压缩出现过的点，压缩编号差不等于原坐标距离。
- 查询 `[L, R]` 时，`L/R` 不一定出现过；要用 `lower_id/upper_id`。
- 压缩后本卷约定从 `1` 开始，方便直接接 树状数组/SegmentTree。
- 区间覆盖如果需要半开边界，常要加入 `r + 1`；当 `r` 很大时注意溢出。
- 忘记 `unique` 前先 `sort` 会去重失败。
- `id(x)` 默认 `x` 在表中；不确定时先判断 `lower_bound` 结果。

暴力/部分分替代：值域小可以直接开数组；数据小可以用 `map<ll, int>` 动态分配编号。

升级方向：接树状数组做逆序对/排名；接线段树做区间维护；接扫描线做矩形/区间统计。

最小测试样例：

```text
输入
5
100 50 100 1000000000 50
60 1000000000

输出
2 1 2 3 1
2
```

