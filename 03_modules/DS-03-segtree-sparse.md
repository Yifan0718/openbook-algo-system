# DS-03 线段树与 Sparse Table

模块编号：DS-03

模块名称：SegmentTree、LazySegmentTree 与 SparseTable

标签：[数据结构][线段树][懒标记][SparseTable]

一句话用途：线段树处理动态区间查询/修改，SparseTable 处理静态区间最值或 gcd。

题面触发词：

- 区间最大/最小。
- 单点修改。
- 区间修改。
- 多次查询。
- 静态 RMQ。

什么时候用：

- 树状数组不够处理 min/max 或复杂维护。
- 有动态修改和区间查询。
- 静态区间最值很多次查询时用 SparseTable。

不要什么时候用：

- 只是静态区间和，用 PrefixSum。
- 只是单点加区间和，用树状数组更短。
- SparseTable 不支持修改。

复杂度：

- SegmentTree：建树 `O(n)`，更新/查询 `O(log n)`。
- LazySegmentTree：区间修改/查询 `O(log n)`。
- SparseTable：预处理 `O(n log n)`，查询 `O(1)`。

数据范围参考：

- `n,q <= 2e5` 常见。
- 线段树数组通常开 `4*n + 5`。

依赖的标准容器：

- 1-index 数组。
- 闭区间 `[l,r]`。

输入如何整理：

```cpp
vector<ll> a(n + 1);
for (int i = 1; i <= n; i++) cin >> a[i];
```

接口：

```text
SegTreeSum / SegmentTree: build(a), setv(pos,val), add(pos,val), query(l,r)
LazySegTreeSum / LazySegmentTree: build(a), range_add(l,r,val), query(l,r)
SparseTable: build(a), query(l,r)
```

输出能力：

- 区间和。
- 区间最值。
- 区间加后的区间和。
- 静态 RMQ。

下游可接：

- DP 优化。
- 二分答案。
- 扫描线。

可拼接模块：

- `Compressor + SegmentTree`。
- `DP + SegmentTree`。
- `Static Array + SparseTable`。

模板代码：

```cpp
struct SegTreeSum {
    int n;
    vector<ll> tree;

    void init(int n_) {
        n = n_;
        tree.assign(4 * n + 4, 0);
    }

    void build(int p, int l, int r, const vector<ll> &a) {
        if (l == r) {
            tree[p] = a[l];
            return;
        }
        int mid = (l + r) / 2;
        build(p * 2, l, mid, a);
        build(p * 2 + 1, mid + 1, r, a);
        tree[p] = tree[p * 2] + tree[p * 2 + 1];
    }

    void build(const vector<ll> &a) {
        init((int)a.size() - 1);
        if (n == 0) return;
        build(1, 1, n, a);
    }

    void setv(int p, int l, int r, int pos, ll val) {
        if (l == r) {
            tree[p] = val;
            return;
        }
        int mid = (l + r) / 2;
        if (pos <= mid) setv(p * 2, l, mid, pos, val);
        else setv(p * 2 + 1, mid + 1, r, pos, val);
        tree[p] = tree[p * 2] + tree[p * 2 + 1];
    }

    void setv(int pos, ll val) {
        if (pos < 1 || pos > n) return;
        setv(1, 1, n, pos, val);
    }

    void add(int pos, ll val) {
        ll cur = query(pos, pos);
        setv(pos, cur + val);
    }

    ll query(int p, int l, int r, int ql, int qr) {
        if (qr < l || r < ql) return 0;
        if (ql <= l && r <= qr) return tree[p];
        int mid = (l + r) / 2;
        ll res = 0;
        if (ql <= mid) res += query(p * 2, l, mid, ql, qr);
        if (qr > mid) res += query(p * 2 + 1, mid + 1, r, ql, qr);
        return res;
    }

    ll query(int l, int r) {
        l = max(l, 1);
        r = min(r, n);
        if (l > r) return 0;
        return query(1, 1, n, l, r);
    }
};

struct LazySegTreeSum {
    int n;
    vector<ll> tree, lazy;

    void init(int n_) {
        n = n_;
        tree.assign(4 * n + 4, 0);
        lazy.assign(4 * n + 4, 0);
    }

    void build(int p, int l, int r, const vector<ll> &a) {
        if (l == r) {
            tree[p] = a[l];
            return;
        }
        int mid = (l + r) / 2;
        build(p * 2, l, mid, a);
        build(p * 2 + 1, mid + 1, r, a);
        tree[p] = tree[p * 2] + tree[p * 2 + 1];
    }

    void build(const vector<ll> &a) {
        init((int)a.size() - 1);
        if (n == 0) return;
        build(1, 1, n, a);
    }

    void apply(int p, int l, int r, ll val) {
        tree[p] += val * (r - l + 1);
        lazy[p] += val;
    }

    void push(int p, int l, int r) {
        if (lazy[p] == 0 || l == r) return;
        int mid = (l + r) / 2;
        apply(p * 2, l, mid, lazy[p]);
        apply(p * 2 + 1, mid + 1, r, lazy[p]);
        lazy[p] = 0;
    }

    void range_add(int p, int l, int r, int ql, int qr, ll val) {
        if (qr < l || r < ql) return;
        if (ql <= l && r <= qr) {
            apply(p, l, r, val);
            return;
        }
        push(p, l, r);
        int mid = (l + r) / 2;
        if (ql <= mid) range_add(p * 2, l, mid, ql, qr, val);
        if (qr > mid) range_add(p * 2 + 1, mid + 1, r, ql, qr, val);
        tree[p] = tree[p * 2] + tree[p * 2 + 1];
    }

    void range_add(int l, int r, ll val) {
        l = max(l, 1);
        r = min(r, n);
        if (l > r) return;
        range_add(1, 1, n, l, r, val);
    }

    ll query(int p, int l, int r, int ql, int qr) {
        if (qr < l || r < ql) return 0;
        if (ql <= l && r <= qr) return tree[p];
        push(p, l, r);
        int mid = (l + r) / 2;
        ll res = 0;
        if (ql <= mid) res += query(p * 2, l, mid, ql, qr);
        if (qr > mid) res += query(p * 2 + 1, mid + 1, r, ql, qr);
        return res;
    }

    ll query(int l, int r) {
        l = max(l, 1);
        r = min(r, n);
        if (l > r) return 0;
        return query(1, 1, n, l, r);
    }
};

using SegmentTree = SegTreeSum;
using LazySegmentTree = LazySegTreeSum;

// 动态 max/min 只需要把单点线段树里的 merge 和 neutral 换掉。
// ll neutral() { return -LINF; }              // max；min 改成 LINF
// ll merge(ll a, ll b) { return max(a, b); } // min 改成 min(a, b)
// 对应替换位置：
// tree[p] = merge(tree[p * 2], tree[p * 2 + 1]);
// query 空贡献 res 从 neutral 开始。

struct SparseTableMin {
    int n, K;
    vector<int> lg;
    vector<vector<ll>> st;

    void build(const vector<ll> &a) {
        n = (int)a.size() - 1;
        if (n == 0) {
            K = 0;
            lg.assign(1, 0);
            st.clear();
            return;
        }
        lg.assign(n + 1, 0);
        for (int i = 2; i <= n; i++) lg[i] = lg[i / 2] + 1;
        K = lg[n] + 1;
        st.assign(K, vector<ll>(n + 1));
        for (int i = 1; i <= n; i++) st[0][i] = a[i];
        for (int k = 1; k < K; k++) {
            for (int i = 1; i + (1 << k) - 1 <= n; i++) {
                st[k][i] = min(st[k - 1][i], st[k - 1][i + (1 << (k - 1))]);
            }
        }
    }

    ll query(int l, int r) {
        l = max(l, 1);
        r = min(r, n);
        if (l > r) return LINF;
        int k = lg[r - l + 1];
        return min(st[k][l], st[k][r - (1 << k) + 1]);
    }
};
```

调用示例：

```cpp
LazySegTreeSum seg;
seg.build(a);
seg.range_add(l, r, x);
cout << seg.query(l, r) << "\n";

SparseTableMin st;
st.build(a);
cout << st.query(l, r) << "\n";
```

常见坑：

- 线段树 `4*n+4`。
- Lazy 查询前要 `push`。
- `range_add` 是闭区间。
- SparseTable 不支持修改。
- SparseTable 查询区间长度 `r-l+1`。

暴力/部分分替代：

- 单点/区间修改直接改数组。
- 查询直接循环扫描。

升级方向：

- 暴力 -> 树状数组/SegmentTree。
- 静态 min/max -> SparseTable。
- 区间修改 -> LazySegmentTree。

最小测试样例：

```text
a=[1,2,3,4]
query(2,3)=5
range_add(2,4,10)
query(1,4)=40
min(2,4)=2 before update
```
