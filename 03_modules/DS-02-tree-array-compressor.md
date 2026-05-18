# DS-02 树状数组与坐标压缩

模块编号：DS-02

模块名称：树状数组、双树状数组与 Compressor

标签：[数据结构][树状数组][坐标压缩]

一句话用途：树状数组解决单点加与区间和，坐标压缩把大值域转成可维护的小下标。

命名约定：正文统一叫“树状数组”；代码里统一把类名写成 `BIT`，短、好抄、不会再出现陌生英文术语。

题面触发词：

- 单点修改，区间求和。
- 动态前缀和。
- 逆序对。
- 排名统计。
- 值域很大但元素个数不多。
- 区间加，单点查。
- 区间加，区间和。

什么时候用：

- 只需要和相关操作，树状数组比线段树短。
- 坐标值可达 `1e9/1e18`，但出现次数 `<= 2e5`。

不要什么时候用：

- 树状数组不适合直接维护区间 min/max 的复杂修改。
- 下标可能为 0 且未平移时不能直接用树状数组。
- 坐标范围查询时不要假设端点已经出现在压缩数组里。

复杂度：

- 树状数组：更新/查询 `O(log n)`。
- Compressor：排序 `O(n log n)`，查询 id `O(log n)`。

数据范围参考：

- `n,q <= 2e5` 常用。
- `n <= 1e6` 也可用，注意内存。

依赖的标准容器：

- 1-index 数组。
- 闭区间 `[l, r]`。
- 压缩后编号 `1..m`。

输入如何整理：

```cpp
vector<ll> all_x;
// 把所有会出现的坐标 push 到 all_x
Compressor cp;
cp.build(all_x);
```

接口：

```text
树状数组: init(n), build(a), add(pos,val), prefix(pos), query(l,r), at(pos)
Compressor: build(xs), id(x), lower_id(x), upper_id(x), val(pos), size()
```

输出能力：

- 前缀和。
- 区间和。
- 单点值。
- 压缩编号。

下游可接：

- 逆序对。
- 扫描线。
- DP 优化。
- 动态排名。

可拼接模块：

- `Compressor + 树状数组`。
- `树状数组 + BinarySearch`。
- `差分树状数组 + range add point query`。
- `双树状数组 + range add range sum`。

模板代码：

```cpp
struct BIT {
    int n;
    vector<ll> bit;

    void init(int n_) {
        n = n_;
        bit.assign(n + 1, 0);
    }

    void build(const vector<ll> &a) {
        init((int)a.size() - 1);
        for (int i = 1; i <= n; i++) add(i, a[i]);
    }

    void add(int pos, ll val) {
        if (pos <= 0 || pos > n) return;
        for (; pos <= n; pos += pos & -pos) bit[pos] += val;
    }

    ll prefix(int pos) {
        if (pos <= 0) return 0;
        if (pos > n) pos = n;
        ll res = 0;
        for (; pos > 0; pos -= pos & -pos) res += bit[pos];
        return res;
    }

    ll query(int l, int r) {
        if (l > r) return 0;
        return prefix(r) - prefix(l - 1);
    }

    ll at(int pos) {
        return query(pos, pos);
    }
};

struct Compressor {
    vector<ll> xs;

    void build(vector<ll> v) {
        xs = v;
        sort(xs.begin(), xs.end());
        xs.erase(unique(xs.begin(), xs.end()), xs.end());
    }

    int id(ll x) {
        return lower_bound(xs.begin(), xs.end(), x) - xs.begin() + 1;
    }

    int lower_id(ll x) {
        return lower_bound(xs.begin(), xs.end(), x) - xs.begin() + 1;
    }

    int upper_id(ll x) {
        return upper_bound(xs.begin(), xs.end(), x) - xs.begin();
    }

    ll val(int pos) {
        return xs[pos - 1];
    }

    int size() {
        return (int)xs.size();
    }
};

struct BITDiff {
    BIT bit;

    void init(int n) {
        bit.init(n);
    }

    void range_add(int l, int r, ll val) {
        if (l < 1) l = 1;
        if (r > bit.n) r = bit.n;
        if (l > r) return;
        bit.add(l, val);
        bit.add(r + 1, -val);
    }

    ll at(int pos) {
        return bit.prefix(pos);
    }
};

struct RangeBIT {
    int n;
    BIT b1, b2;

    void init(int n_) {
        n = n_;
        b1.init(n);
        b2.init(n);
    }

    void internal_add(int pos, ll val) {
        b1.add(pos, val);
        b2.add(pos, val * (pos - 1));
    }

    void range_add(int l, int r, ll val) {
        if (l < 1) l = 1;
        if (r > n) r = n;
        if (l > r) return;
        internal_add(l, val);
        internal_add(r + 1, -val);
    }

    ll prefix(int pos) {
        if (pos <= 0) return 0;
        if (pos > n) pos = n;
        return b1.prefix(pos) * pos - b2.prefix(pos);
    }

    ll query(int l, int r) {
        if (l > r) return 0;
        return prefix(r) - prefix(l - 1);
    }
};
```

调用示例：

```cpp
BIT fw;
fw.build(a);
fw.add(pos, delta);
cout << fw.query(l, r) << "\n";

Compressor cp;
cp.build(all_x);
BIT bit;
bit.init(cp.size());
bit.add(cp.id(x), 1);
int L = cp.lower_id(left_value);
int R = cp.upper_id(right_value);
cout << bit.query(L, R) << "\n";
```

常见坑：

- 树状数组下标不能为 0。
- 单点 `add(pos, val)` 中 `pos <= 0` 或 `pos > n` 会自动跳过；区间修改模板会先裁剪到 `[1,n]`，避免误传 `l=0` 只改到右边界。
- `r + 1` 可能是 `n + 1`，树状数组的 `add` 会自动跳过，但数组大小要正常。
- `id(x)` 只适合 `x` 已经在 `xs` 中；范围查询用 `lower_id/upper_id`。
- 双树状数组公式容易错，确认闭区间 `[l,r]`。

暴力/部分分替代：

- 直接数组修改，查询时循环求和。
- 逆序对小数据双重循环。

升级方向：

- 树状数组无法处理复杂最值 -> SegmentTree。
- 值域大 -> 先 Compressor。
- 只静态区间和 -> PrefixSum 更简单。

最小测试样例：

```text
a = [1,2,3]
query(1,3)=6
add(2,5) 后 query(2,2)=7
坐标 [100, 1000000000] 压缩为 [1,2]
```
