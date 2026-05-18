# DS-05 线段树进阶

模块编号：DS-05

模块名称：动态开点、可持久化线段树、线段树合并

标签：[数据结构][线段树][动态开点][主席树][可持久化][线段树合并]

一句话用途：在线段树基础上处理超大值域、历史版本查询、多个线段树合并等进阶场景。

题面触发词：

- 值域 `1..1e9` 或 `1..1e18`，但操作次数不多。
- 动态开点线段树。
- 可持久化线段树、主席树、区间第 k 小。
- 每个节点维护一棵权值线段树，需要合并。
- 区间 `chmin/chmax`、Segment Tree Beats。

什么时候用：

- 坐标范围巨大，不能开 `4*V`，但实际访问点数约 `q log V`。
- 需要保留每个前缀/每次修改后的历史版本。
- 树上/集合中有很多权值线段树，DFS 回来要合并。
- 线段树普通 lazy 无法处理特殊区间最值约束时，再考虑 beats。

不要什么时候用：

- 值域可以离线压缩，普通线段树或树状数组更短。
- 只要静态区间第 k 小且数据很小，排序子数组可拿部分分。
- 没有历史版本需求，不要强行可持久化。
- Beats 难写难调，除非题目明显要求区间取 min/max 与和/最值混合维护。

复杂度：

- 动态开点：单次修改/查询 `O(log V)`，空间约 `O(访问次数 * log V)`。
- 可持久化线段树：每次单点更新新建 `O(log V)` 个点。
- 区间第 k 小主席树：建 `O(n log n)`，查询 `O(log n)`。
- 线段树合并：总复杂度通常与被创建节点数同阶。

数据范围参考：

- `q <= 2e5`，值域 `<= 1e9`：动态开点常用。
- 主席树节点数估算：`(n + q) * (log2(m) + 2)`。
- `n <= 2e5`：主席树常开 `4e6` 左右或用 `vector.reserve`。

依赖的标准容器：

- 1-index 值域闭区间 `[L,R]`。
- 节点数组或 `vector<Node>`。
- 坐标压缩数组 `xs`。

输入如何整理：

```cpp
// 动态开点：保留真实坐标范围
DynamicSegTree seg(1, 1000000000LL);

// 主席树：先离散化值，再建前缀版本
vector<ll> xs;
for (int i = 1; i <= n; i++) xs.push_back(a[i]);
sort(xs.begin(), xs.end());
xs.erase(unique(xs.begin(), xs.end()), xs.end());
```

接口：

```text
DynamicSegTree: range_add(l,r,val), point_add(pos,val), query(l,r)
PersistentSegTree: update(oldRoot,l,r,pos), kth(rootL,rootR,l,r,k)
MergeSegTree: point_add(root,pos,val), merge(x,y,l,r)
```

输出能力：

- 超大值域区间加、区间和。
- 静态区间第 `k` 小。
- 多棵权值线段树合并后的计数/和。

下游可接：

- 扫描线。
- 树上启发式合并。
- 区间第 k 小。
- 权值统计。

可拼接模块：

- `DS-05 + DS-02 Compressor`。
- `DS-05 + TREE/GRAPH DFS`。
- `DS-05 + DS-03 SegmentTree`。

动态开点线段树模板：区间加、区间和

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct DynamicSegTree {
    struct Node {
        int lc = 0, rc = 0;
        ll sum = 0, lazy = 0;
    };

    vector<Node> tr;
    int root;
    ll L, R;

    DynamicSegTree(ll L_ = 1, ll R_ = 1000000000LL) {
        init(L_, R_);
    }

    void init(ll L_, ll R_) {
        L = L_;
        R = R_;
        root = 0;
        tr.clear();
        tr.push_back(Node());
    }

    int new_node() {
        tr.push_back(Node());
        return (int)tr.size() - 1;
    }

    void apply(int p, ll l, ll r, ll val) {
        tr[p].sum += val * (r - l + 1);
        tr[p].lazy += val;
    }

    void push(int p, ll l, ll r) {
        if (tr[p].lazy == 0 || l == r) return;
        ll mid = l + (r - l) / 2;
        if (tr[p].lc == 0) tr[p].lc = new_node();
        if (tr[p].rc == 0) tr[p].rc = new_node();
        apply(tr[p].lc, l, mid, tr[p].lazy);
        apply(tr[p].rc, mid + 1, r, tr[p].lazy);
        tr[p].lazy = 0;
    }

    void pull(int p) {
        tr[p].sum = 0;
        if (tr[p].lc) tr[p].sum += tr[tr[p].lc].sum;
        if (tr[p].rc) tr[p].sum += tr[tr[p].rc].sum;
    }

    void range_add(int &p, ll l, ll r, ll ql, ll qr, ll val) {
        if (qr < l || r < ql) return;
        if (p == 0) p = new_node();
        if (ql <= l && r <= qr) {
            apply(p, l, r, val);
            return;
        }
        push(p, l, r);
        ll mid = l + (r - l) / 2;
        range_add(tr[p].lc, l, mid, ql, qr, val);
        range_add(tr[p].rc, mid + 1, r, ql, qr, val);
        pull(p);
    }

    ll query(int p, ll l, ll r, ll ql, ll qr) {
        if (p == 0 || qr < l || r < ql) return 0;
        if (ql <= l && r <= qr) return tr[p].sum;
        push(p, l, r);
        ll mid = l + (r - l) / 2;
        return query(tr[p].lc, l, mid, ql, qr) +
               query(tr[p].rc, mid + 1, r, ql, qr);
    }

    void range_add(ll l, ll r, ll val) {
        if (l > r) return;
        range_add(root, L, R, l, r, val);
    }

    void point_add(ll pos, ll val) {
        range_add(pos, pos, val);
    }

    ll query(ll l, ll r) {
        if (l > r) return 0;
        return query(root, L, R, l, r);
    }
};
```

可持久化线段树入门：静态区间第 k 小

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct PersistentSegTree {
    struct Node {
        int lc = 0, rc = 0;
        int sum = 0;
    };

    vector<Node> tr;

    PersistentSegTree() {
        tr.push_back(Node());
    }

    int clone(int p) {
        tr.push_back(tr[p]);
        return (int)tr.size() - 1;
    }

    int update(int p, int l, int r, int pos) {
        int q = clone(p);
        tr[q].sum++;
        if (l == r) return q;
        int mid = (l + r) / 2;
        if (pos <= mid) tr[q].lc = update(tr[p].lc, l, mid, pos);
        else tr[q].rc = update(tr[p].rc, mid + 1, r, pos);
        return q;
    }

    int kth(int leftRoot, int rightRoot, int l, int r, int k) {
        if (l == r) return l;
        int mid = (l + r) / 2;
        int left_count = tr[tr[rightRoot].lc].sum - tr[tr[leftRoot].lc].sum;
        if (k <= left_count) {
            return kth(tr[leftRoot].lc, tr[rightRoot].lc, l, mid, k);
        }
        return kth(tr[leftRoot].rc, tr[rightRoot].rc, mid + 1, r, k - left_count);
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, q;
    cin >> n >> q;
    vector<ll> a(n + 1), xs;
    for (int i = 1; i <= n; i++) {
        cin >> a[i];
        xs.push_back(a[i]);
    }
    sort(xs.begin(), xs.end());
    xs.erase(unique(xs.begin(), xs.end()), xs.end());

    int m = (int)xs.size();
    PersistentSegTree pst;
    pst.tr.reserve((n + 5) * 20);
    vector<int> root(n + 1, 0);

    for (int i = 1; i <= n; i++) {
        int id = lower_bound(xs.begin(), xs.end(), a[i]) - xs.begin() + 1;
        root[i] = pst.update(root[i - 1], 1, m, id);
    }

    while (q--) {
        int l, r, k;
        cin >> l >> r >> k;
        if (l < 1 || r > n || l > r || k < 1 || k > r - l + 1) {
            cout << "-1\n";
            continue;
        }
        int id = pst.kth(root[l - 1], root[r], 1, m, k);
        cout << xs[id - 1] << '\n';
    }
    return 0;
}
```

线段树合并简表：

| 需求 | 做法 | 注意 |
| --- | --- | --- |
| 多棵权值线段树合成一棵 | `merge(x,y)` 返回合并后根 | 通常会破坏 `y`，不能再单独用 |
| 子树颜色/权值计数 | 每个树点一个根，DFS 后合并儿子根 | 总复杂度看总节点数 |
| 只维护出现次数 | 叶子 `sum += sum` | 最容易写 |
| 还要维护最大值位置 | 合并后 `pull` 更新答案 | tie 规则提前定 |

线段树合并最小模板：单点计数

```cpp
struct MergeSegTree {
    struct Node {
        int lc = 0, rc = 0;
        long long sum = 0;
    };

    vector<Node> tr;

    MergeSegTree() {
        tr.push_back(Node());
    }

    int new_node() {
        tr.push_back(Node());
        return (int)tr.size() - 1;
    }

    void point_add(int &p, int l, int r, int pos, long long val) {
        if (p == 0) p = new_node();
        if (l == r) {
            tr[p].sum += val;
            return;
        }
        int mid = (l + r) / 2;
        if (pos <= mid) point_add(tr[p].lc, l, mid, pos, val);
        else point_add(tr[p].rc, mid + 1, r, pos, val);
        tr[p].sum = tr[tr[p].lc].sum + tr[tr[p].rc].sum;
    }

    int merge(int x, int y, int l, int r) {
        if (x == 0 || y == 0) return x + y;
        if (l == r) {
            tr[x].sum += tr[y].sum;
            return x;
        }
        int mid = (l + r) / 2;
        tr[x].lc = merge(tr[x].lc, tr[y].lc, l, mid);
        tr[x].rc = merge(tr[x].rc, tr[y].rc, mid + 1, r);
        tr[x].sum = tr[tr[x].lc].sum + tr[tr[x].rc].sum;
        return x;
    }
};
```

Segment Tree Beats 低优先级说明：

```text
常见能力：
  区间 chmin：把区间内所有大于 x 的数改成 x。
  区间 chmax：把区间内所有小于 x 的数改成 x。
  同时查询区间 sum/max/min。

核心字段示例：
  max1 最大值、max2 严格次大值、cntMax 最大值出现次数、sum 区间和。

考场建议：
  只有当题面明确出现 range chmin/chmax + sum/max 查询，且普通 lazy 做不了时再写。
  没背熟不要现场硬造，优先骗部分分。
```

调用示例：

```cpp
DynamicSegTree seg(1, 1000000000LL);
seg.range_add(10, 20, 3);
cout << seg.query(1, 100) << '\n';

// 主席树区间第 k 小：
int id = pst.kth(root[l - 1], root[r], 1, m, k);
cout << xs[id - 1] << '\n';
```

常见坑：

- 动态开点的 `0` 是空节点，`tr[0]` 必须存在且全为 0。
- `mid` 用 `l + (r-l)/2`，值域 `1e18` 时避免溢出。
- 动态开点区间长度很大时，`val * (r-l+1)` 可能爆 `long long`。
- 主席树查询第 `k` 小要用 `root[r] - root[l-1]` 两个版本相减。
- 主席树 `k` 必须满足 `1 <= k <= r-l+1`。
- 可持久化更新必须克隆旧点，不能原地改旧版本。
- 线段树合并会破坏被合并的根，后续别再把旧根当独立版本用。
- Beats 不是普通 lazy，多维护的最大/次大关系错一点就会 WA。

暴力/部分分替代：

- 值域大但操作可离线：坐标压缩 + 普通线段树。
- 区间第 `k` 小小数据：复制子数组排序。
- 历史版本不多：每次复制整个数组或整棵树拿部分分。
- 多集合合并小数据：`map` / `unordered_map` 计数。
- Beats 题：分块或暴力扫区间，先拿低档分。

升级方向：

- 动态开点 + 懒标记 -> 扫描线、区间覆盖。
- 主席树 -> 带修改主席树，难度较高。
- 线段树合并 -> 树上权值统计。
- Segment Tree Beats -> 区间取 min/max 与区间和混合维护。

最小测试样例：

```text
动态开点：
add [10,20] += 3
query [1,100] = 33

主席树：
a = [5,1,4,2,3]
区间 [2,5] 第 3 小 = 3
```
