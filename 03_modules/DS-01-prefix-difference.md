# DS-01 前缀和与差分

模块编号：DS-01

模块名称：PrefixSum 与 Difference

标签：[数据结构][前缀和][差分][区间]

一句话用途：前缀和用于静态快速查区间和，差分用于批量区间加后一次性还原。

题面触发词：

- 多次询问区间和。
- 数组不变。
- 多次区间加，最后输出结果。
- 对一段 `[l,r]` 同时增加/减少。

什么时候用：

- `PrefixSum`：数组不修改，频繁查询区间和。
- `Difference`：有很多区间加操作，但中间不需要查询完整区间和。

不要什么时候用：

- `PrefixSum` 不适合有动态修改的区间和。
- `Difference` 不适合每次修改后马上查区间和。
- 查询 min/max/gcd 不用前缀和。

复杂度：

- PrefixSum：预处理 `O(n)`，查询 `O(1)`。
- Difference：每次区间加 `O(1)`，还原 `O(n)`。

数据范围参考：

- `n,q <= 1e6` 时仍可用，注意内存和 `long long`。

依赖的标准容器：

- 1-index `vector<ll> a(n + 1)`。
- 闭区间 `[l, r]`。

输入如何整理：

```cpp
vector<ll> a(n + 1);
for (int i = 1; i <= n; i++) cin >> a[i];
```

接口：

```text
PrefixSum: build(a), prefix(pos), query(l,r)
Difference: build(a), range_add(l,r,val), restore()
```

输出能力：

- 区间和。
- 批量区间加后的最终数组。

下游可接：

- 区间 DP 的 `cost(l,r)`。
- 枚举区间时 `O(1)` 求和。
- 差分可接扫描线思想。

可拼接模块：

- `IntervalDP + PrefixSum`。
- `BinarySearchAnswer + PrefixSum`。
- `Difference + final scan`。

模板代码：

```cpp
struct PrefixSum {
    int n;
    vector<ll> pre;

    void build(const vector<ll> &a) {
        n = (int)a.size() - 1;
        pre.assign(n + 1, 0);
        for (int i = 1; i <= n; i++) pre[i] = pre[i - 1] + a[i];
    }

    ll prefix(int pos) {
        if (pos <= 0) return 0;
        if (pos > n) pos = n;
        return pre[pos];
    }

    ll query(int l, int r) {
        if (l > r) return 0;
        return prefix(r) - prefix(l - 1);
    }
};

struct Difference {
    int n;
    vector<ll> d;

    void init(int n_) {
        n = n_;
        d.assign(n + 2, 0);
    }

    void build(const vector<ll> &a) {
        init((int)a.size() - 1);
        for (int i = 1; i <= n; i++) d[i] = a[i] - a[i - 1];
    }

    void range_add(int l, int r, ll val) {
        l = max(l, 1);
        r = min(r, n);
        if (l > r) return;
        d[l] += val;
        d[r + 1] -= val;
    }

    vector<ll> restore() {
        vector<ll> a(n + 1, 0);
        for (int i = 1; i <= n; i++) a[i] = a[i - 1] + d[i];
        return a;
    }
};
```

调用示例：

```cpp
PrefixSum ps;
ps.build(a);
cout << ps.query(l, r) << "\n";

Difference df;
df.build(a);
df.range_add(l, r, x);
a = df.restore();
```

常见坑：

- `query(l,r)` 中 `l=1` 时要用 `pre[0]`。
- 区间加时 `d[r+1]` 需要数组开到 `n+2`。
- 区间和可能超过 `int`，用 `ll`。
- Difference 中间查询原数组要先还原，不能直接读 `d[i]`。

暴力/部分分替代：

- 区间和：每次 `for i=l..r` 求和。
- 区间加：每次 `for i=l..r` 修改数组。

升级方向：

- 前缀和动态修改 -> 树状数组。
- 差分需要在线查询 -> 树状数组差分版或 LazySegmentTree。

最小测试样例：

```text
a = [5]
query(1,1) = 5
range_add(1,1,3) 后 a=[8]
```
