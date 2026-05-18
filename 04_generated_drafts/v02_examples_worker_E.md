# 0.2 版本例题扩展 Worker E

范围：第 4 卷 数据结构；第 5 卷 图论与树。

约定：所有 C++17 代码均为完整可运行程序，使用标准输入输出，不使用文件读写；数组、图点、查询区间默认 1-index。

## 第 4 卷：数据结构例题

### V04-EX01 区间和查询

- 归属卷：第 4 卷
- 覆盖模块：前缀和
- 考场用途：静态数组多次区间求和，`O(nq)` 会超时，前缀和可把每问降到 `O(1)`。

**题目描述：** 给定长度为 `n` 的整数数组，回答 `q` 次闭区间 `[l,r]` 的元素和。

**输入格式：** 第一行两个整数 `n q`。第二行 `n` 个整数。接下来 `q` 行，每行两个整数 `l r`。

**输出格式：** 对每个询问输出一行区间和。

**样例输入：**
```text
5 3
1 2 3 4 5
1 3
2 5
4 4
```

**样例输出：**
```text
6
14
4
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, q;
    cin >> n >> q;
    vector<ll> pre(n + 1, 0);
    for (int i = 1; i <= n; i++) {
        ll x;
        cin >> x;
        pre[i] = pre[i - 1] + x;
    }

    while (q--) {
        int l, r;
        cin >> l >> r;
        cout << pre[r] - pre[l - 1] << '\n';
    }
    return 0;
}
```

**测试设计：**
- 用例 1：单点数组和重复查询。
```text
输入：
1 2
-5
1 1
1 1
期望输出：
-5
-5
```
- 用例 2：含负数区间。
```text
输入：
4 3
10 -2 3 7
1 4
2 3
3 4
期望输出：
18
1
10
```

### V04-EX02 矩形区域求和

- 归属卷：第 4 卷
- 覆盖模块：二维前缀和
- 考场用途：静态矩阵多次子矩形求和，用容斥公式 `O(1)` 回答。

**题目描述：** 给定 `n*m` 矩阵，回答 `q` 次子矩形 `(x1,y1)` 到 `(x2,y2)` 的元素和。

**输入格式：** 第一行三个整数 `n m q`。接下来 `n` 行每行 `m` 个整数。接下来 `q` 行每行四个整数 `x1 y1 x2 y2`。

**输出格式：** 对每个询问输出一行矩形和。

**样例输入：**
```text
3 4 3
1 2 3 4
5 6 7 8
9 10 11 12
1 1 1 4
2 2 3 3
1 1 3 4
```

**样例输出：**
```text
10
34
78
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m, q;
    cin >> n >> m >> q;
    vector<vector<ll>> pre(n + 1, vector<ll>(m + 1, 0));

    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            ll x;
            cin >> x;
            pre[i][j] = pre[i - 1][j] + pre[i][j - 1] - pre[i - 1][j - 1] + x;
        }
    }

    while (q--) {
        int x1, y1, x2, y2;
        cin >> x1 >> y1 >> x2 >> y2;
        ll ans = pre[x2][y2] - pre[x1 - 1][y2] - pre[x2][y1 - 1] + pre[x1 - 1][y1 - 1];
        cout << ans << '\n';
    }
    return 0;
}
```

**测试设计：**
- 用例 1：单格矩形。
```text
输入：
2 2 2
1 2
3 4
1 1 1 1
2 2 2 2
期望输出：
1
4
```
- 用例 2：含负数整矩阵。
```text
输入：
2 3 2
1 -1 2
3 4 -2
1 1 2 3
1 2 2 2
期望输出：
7
3
```

### V04-EX03 批量区间加

- 归属卷：第 4 卷
- 覆盖模块：差分
- 考场用途：多次区间加，最后一次性输出最终数组。

**题目描述：** 给定长度为 `n` 的数组，执行 `q` 次操作：把闭区间 `[l,r]` 中所有数加上 `x`。输出所有操作后的数组。

**输入格式：** 第一行两个整数 `n q`。第二行 `n` 个整数。接下来 `q` 行每行三个整数 `l r x`。

**输出格式：** 输出一行 `n` 个整数，表示最终数组。

**样例输入：**
```text
5 3
1 2 3 4 5
1 3 10
2 5 -2
4 4 7
```

**样例输出：**
```text
11 10 11 9 3
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, q;
    cin >> n >> q;
    vector<ll> a(n + 1), diff(n + 2, 0);
    for (int i = 1; i <= n; i++) cin >> a[i];

    for (int i = 1; i <= n; i++) {
        diff[i] += a[i] - a[i - 1];
    }

    while (q--) {
        int l, r;
        ll x;
        cin >> l >> r >> x;
        diff[l] += x;
        diff[r + 1] -= x;
    }

    vector<ll> ans(n + 1, 0);
    for (int i = 1; i <= n; i++) {
        ans[i] = ans[i - 1] + diff[i];
        if (i > 1) cout << ' ';
        cout << ans[i];
    }
    cout << '\n';
    return 0;
}
```

**测试设计：**
- 用例 1：没有变化的抵消操作。
```text
输入：
3 2
5 5 5
1 3 2
1 3 -2
期望输出：
5 5 5
```
- 用例 2：单点区间加。
```text
输入：
4 2
0 0 0 0
2 2 7
4 4 -1
期望输出：
0 7 0 -1
```

### V04-EX04 最长和不超过 S 的连续子数组

- 归属卷：第 4 卷
- 覆盖模块：双指针、滑动窗口
- 考场用途：非负数组上维护单调窗口，线性求最长合法区间。

**题目描述：** 给定长度为 `n` 的非负整数数组和整数 `S`，求元素和不超过 `S` 的最长连续子数组长度。

**输入格式：** 第一行两个整数 `n S`。第二行 `n` 个非负整数。

**输出格式：** 输出一个整数，表示最长长度。

**样例输入：**
```text
5 7
2 1 3 2 4
```

**样例输出：**
```text
3
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    ll S;
    cin >> n >> S;
    vector<ll> a(n + 1);
    for (int i = 1; i <= n; i++) cin >> a[i];

    int ans = 0;
    int l = 1;
    ll sum = 0;
    for (int r = 1; r <= n; r++) {
        sum += a[r];
        while (l <= r && sum > S) {
            sum -= a[l];
            l++;
        }
        ans = max(ans, r - l + 1);
    }

    cout << ans << '\n';
    return 0;
}
```

**测试设计：**
- 用例 1：所有元素都可选。
```text
输入：
4 100
1 2 3 4
期望输出：
4
```
- 用例 2：没有任何正数元素能进入，但 0 可以形成窗口。
```text
输入：
5 0
0 0 3 0 0
期望输出：
2
```

### V04-EX05 左侧最近严格更大元素

- 归属卷：第 4 卷
- 覆盖模块：单调栈
- 考场用途：每个位置找最近满足大小关系的位置，把朴素向左扫描降为 `O(n)`。

**题目描述：** 给定长度为 `n` 的数组，对每个位置 `i` 输出左侧最近的 `j`，满足 `j<i` 且 `a[j]>a[i]`。不存在则输出 `0`。

**输入格式：** 第一行整数 `n`。第二行 `n` 个整数。

**输出格式：** 输出一行 `n` 个整数，第 `i` 个为答案。

**样例输入：**
```text
5
2 1 3 2 5
```

**样例输出：**
```text
0 1 0 3 0
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<ll> a(n + 1);
    for (int i = 1; i <= n; i++) cin >> a[i];

    vector<int> ans(n + 1, 0), st;
    for (int i = 1; i <= n; i++) {
        while (!st.empty() && a[st.back()] <= a[i]) st.pop_back();
        ans[i] = st.empty() ? 0 : st.back();
        st.push_back(i);
    }

    for (int i = 1; i <= n; i++) {
        if (i > 1) cout << ' ';
        cout << ans[i];
    }
    cout << '\n';
    return 0;
}
```

**测试设计：**
- 用例 1：严格递减数组。
```text
输入：
4
9 7 5 3
期望输出：
0 1 2 3
```
- 用例 2：相等元素不算严格更大。
```text
输入：
4
2 2 1 2
期望输出：
0 0 2 0
```

### V04-EX06 滑动窗口最大值

- 归属卷：第 4 卷
- 覆盖模块：单调队列
- 考场用途：固定长度窗口查询最大值，避免每个窗口重新扫描。

**题目描述：** 给定长度为 `n` 的数组和窗口长度 `k`，输出每个长度为 `k` 的连续窗口最大值。

**输入格式：** 第一行两个整数 `n k`。第二行 `n` 个整数。

**输出格式：** 输出 `n-k+1` 个整数，依次为每个窗口最大值。

**样例输入：**
```text
8 3
1 3 -1 -3 5 3 6 7
```

**样例输出：**
```text
3 3 5 5 6 7
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, k;
    cin >> n >> k;
    vector<ll> a(n + 1);
    for (int i = 1; i <= n; i++) cin >> a[i];

    deque<int> dq;
    vector<ll> ans;
    for (int i = 1; i <= n; i++) {
        while (!dq.empty() && dq.front() <= i - k) dq.pop_front();
        while (!dq.empty() && a[dq.back()] <= a[i]) dq.pop_back();
        dq.push_back(i);
        if (i >= k) ans.push_back(a[dq.front()]);
    }

    for (int i = 0; i < (int)ans.size(); i++) {
        if (i) cout << ' ';
        cout << ans[i];
    }
    cout << '\n';
    return 0;
}
```

**测试设计：**
- 用例 1：窗口长度为 1。
```text
输入：
4 1
4 1 3 2
期望输出：
4 1 3 2
```
- 用例 2：窗口覆盖全数组。
```text
输入：
5 5
-2 -8 -1 -3 -4
期望输出：
-1
```

### V04-EX07 合并果子最小代价

- 归属卷：第 4 卷
- 覆盖模块：堆、STL `priority_queue`
- 考场用途：每次取当前最小的两个元素合并，典型小根堆贪心。

**题目描述：** 有 `n` 堆果子，每次选择两堆合并，代价为两堆重量之和，新堆重量也为该和。求把所有果子合成一堆的最小总代价。

**输入格式：** 第一行整数 `n`。第二行 `n` 个正整数表示每堆重量。

**输出格式：** 输出最小总代价。若 `n=1`，答案为 `0`。

**样例输入：**
```text
4
1 2 3 4
```

**样例输出：**
```text
19
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    priority_queue<ll, vector<ll>, greater<ll>> pq;
    for (int i = 1; i <= n; i++) {
        ll x;
        cin >> x;
        pq.push(x);
    }

    ll ans = 0;
    while ((int)pq.size() >= 2) {
        ll a = pq.top();
        pq.pop();
        ll b = pq.top();
        pq.pop();
        ans += a + b;
        pq.push(a + b);
    }

    cout << ans << '\n';
    return 0;
}
```

**测试设计：**
- 用例 1：只有一堆。
```text
输入：
1
10
期望输出：
0
```
- 用例 2：权值相同。
```text
输入：
4
5 5 5 5
期望输出：
40
```

### V04-EX08 在线合并与连通查询

- 归属卷：第 4 卷
- 覆盖模块：DSU 并查集
- 考场用途：只合并、不删除的连通性维护。

**题目描述：** 初始有 `n` 个互不相交的集合。执行 `q` 次操作：`U a b` 合并 `a,b` 所在集合；`Q a b` 询问 `a,b` 是否在同一集合。

**输入格式：** 第一行两个整数 `n q`。接下来 `q` 行，每行一个字符 `op` 和两个整数 `a b`。

**输出格式：** 对每个 `Q` 输出 `Yes` 或 `No`。

**样例输入：**
```text
5 6
Q 1 2
U 1 2
Q 1 2
U 3 4
U 2 3
Q 1 4
```

**样例输出：**
```text
No
Yes
Yes
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

struct DSU {
    vector<int> fa, sz;

    void init(int n) {
        fa.resize(n + 1);
        sz.assign(n + 1, 1);
        iota(fa.begin(), fa.end(), 0);
    }

    int find(int x) {
        while (x != fa[x]) {
            fa[x] = fa[fa[x]];
            x = fa[x];
        }
        return x;
    }

    void unite(int a, int b) {
        a = find(a);
        b = find(b);
        if (a == b) return;
        if (sz[a] < sz[b]) swap(a, b);
        fa[b] = a;
        sz[a] += sz[b];
    }

    bool same(int a, int b) {
        return find(a) == find(b);
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, q;
    cin >> n >> q;
    DSU dsu;
    dsu.init(n);

    while (q--) {
        char op;
        int a, b;
        cin >> op >> a >> b;
        if (op == 'U') {
            dsu.unite(a, b);
        } else {
            cout << (dsu.same(a, b) ? "Yes" : "No") << '\n';
        }
    }
    return 0;
}
```

**测试设计：**
- 用例 1：重复合并同一集合。
```text
输入：
3 4
U 1 2
U 2 1
Q 1 2
Q 1 3
期望输出：
Yes
No
```
- 用例 2：自查询。
```text
输入：
2 2
Q 1 1
Q 1 2
期望输出：
Yes
No
```

### V04-EX09 逆序对数量

- 归属卷：第 4 卷
- 覆盖模块：树状数组、坐标压缩
- 考场用途：值域大但只出现 `n` 个数时，压缩后用树状数组统计排名。

**题目描述：** 给定长度为 `n` 的数组，求逆序对数量，即满足 `i<j` 且 `a[i]>a[j]` 的二元组个数。

**输入格式：** 第一行整数 `n`。第二行 `n` 个整数。

**输出格式：** 输出逆序对数量。

**样例输入：**
```text
5
5 3 2 4 1
```

**样例输出：**
```text
8
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

struct BIT {
    int n = 0;
    vector<ll> bit;

    void init(int n_) {
        n = n_;
        bit.assign(n + 1, 0);
    }

    void add(int pos, ll val) {
        for (; pos <= n; pos += pos & -pos) bit[pos] += val;
    }

    ll prefix(int pos) {
        ll res = 0;
        for (; pos > 0; pos -= pos & -pos) res += bit[pos];
        return res;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<ll> a(n + 1), xs;
    xs.reserve(n);
    for (int i = 1; i <= n; i++) {
        cin >> a[i];
        xs.push_back(a[i]);
    }

    sort(xs.begin(), xs.end());
    xs.erase(unique(xs.begin(), xs.end()), xs.end());

    BIT fw;
    fw.init((int)xs.size());
    ll ans = 0;
    for (int i = 1; i <= n; i++) {
        int id = (int)(lower_bound(xs.begin(), xs.end(), a[i]) - xs.begin()) + 1;
        ll previous = i - 1;
        ll not_greater = fw.prefix(id);
        ans += previous - not_greater;
        fw.add(id, 1);
    }

    cout << ans << '\n';
    return 0;
}
```

**测试设计：**
- 用例 1：已经升序。
```text
输入：
4
1 2 3 4
期望输出：
0
```
- 用例 2：有重复值，严格大于才算。
```text
输入：
4
2 2 1 1
期望输出：
4
```

### V04-EX10 区间加与区间和

- 归属卷：第 4 卷
- 覆盖模块：线段树、懒标记
- 考场用途：动态区间修改和区间查询同时存在时使用 lazy segment tree。

**题目描述：** 给定数组，支持两种操作：`A l r x` 表示把 `[l,r]` 全部加 `x`；`Q l r` 表示查询 `[l,r]` 的区间和。

**输入格式：** 第一行两个整数 `n q`。第二行 `n` 个整数。接下来 `q` 行，每行一个操作。

**输出格式：** 对每个 `Q` 输出一行答案。

**样例输入：**
```text
5 5
1 2 3 4 5
Q 1 5
A 2 4 10
Q 1 3
A 5 5 -2
Q 4 5
```

**样例输出：**
```text
15
26
17
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

struct SegTree {
    int n = 0;
    vector<ll> tree, lazy;

    void init(int n_) {
        n = n_;
        tree.assign(4 * n + 4, 0);
        lazy.assign(4 * n + 4, 0);
    }

    void build(int p, int l, int r, const vector<ll>& a) {
        if (l == r) {
            tree[p] = a[l];
            return;
        }
        int mid = (l + r) / 2;
        build(p * 2, l, mid, a);
        build(p * 2 + 1, mid + 1, r, a);
        tree[p] = tree[p * 2] + tree[p * 2 + 1];
    }

    void build(const vector<ll>& a) {
        init((int)a.size() - 1);
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
        range_add(p * 2, l, mid, ql, qr, val);
        range_add(p * 2 + 1, mid + 1, r, ql, qr, val);
        tree[p] = tree[p * 2] + tree[p * 2 + 1];
    }

    ll query(int p, int l, int r, int ql, int qr) {
        if (qr < l || r < ql) return 0;
        if (ql <= l && r <= qr) return tree[p];
        push(p, l, r);
        int mid = (l + r) / 2;
        return query(p * 2, l, mid, ql, qr) + query(p * 2 + 1, mid + 1, r, ql, qr);
    }

    void range_add(int l, int r, ll val) {
        range_add(1, 1, n, l, r, val);
    }

    ll query(int l, int r) {
        return query(1, 1, n, l, r);
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, q;
    cin >> n >> q;
    vector<ll> a(n + 1);
    for (int i = 1; i <= n; i++) cin >> a[i];

    SegTree seg;
    seg.build(a);

    while (q--) {
        char op;
        int l, r;
        cin >> op >> l >> r;
        if (op == 'A') {
            ll x;
            cin >> x;
            seg.range_add(l, r, x);
        } else {
            cout << seg.query(l, r) << '\n';
        }
    }
    return 0;
}
```

**测试设计：**
- 用例 1：单点修改后查询。
```text
输入：
3 3
1 1 1
A 2 2 5
Q 1 3
Q 2 2
期望输出：
8
6
```
- 用例 2：负数修改。
```text
输入：
4 4
10 20 30 40
Q 2 4
A 1 4 -10
Q 1 1
Q 1 4
期望输出：
90
0
60
```

### V04-EX11 静态区间最小值

- 归属卷：第 4 卷
- 覆盖模块：Sparse Table
- 考场用途：数组不修改，区间最值大量查询，用 `O(n log n)` 预处理和 `O(1)` 查询。

**题目描述：** 给定长度为 `n` 的数组，回答 `q` 次闭区间 `[l,r]` 的最小值。

**输入格式：** 第一行两个整数 `n q`。第二行 `n` 个整数。接下来 `q` 行每行两个整数 `l r`。

**输出格式：** 对每个询问输出一行最小值。

**样例输入：**
```text
6 3
5 2 4 7 1 3
1 3
2 5
5 6
```

**样例输出：**
```text
2
1
1
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, q;
    cin >> n >> q;
    vector<ll> a(n + 1);
    for (int i = 1; i <= n; i++) cin >> a[i];

    vector<int> lg(n + 1, 0);
    for (int i = 2; i <= n; i++) lg[i] = lg[i / 2] + 1;
    int K = lg[n] + 1;
    vector<vector<ll>> st(K, vector<ll>(n + 1, 0));
    for (int i = 1; i <= n; i++) st[0][i] = a[i];

    for (int k = 1; k < K; k++) {
        for (int i = 1; i + (1 << k) - 1 <= n; i++) {
            st[k][i] = min(st[k - 1][i], st[k - 1][i + (1 << (k - 1))]);
        }
    }

    while (q--) {
        int l, r;
        cin >> l >> r;
        int len = r - l + 1;
        int k = lg[len];
        cout << min(st[k][l], st[k][r - (1 << k) + 1]) << '\n';
    }
    return 0;
}
```

**测试设计：**
- 用例 1：单点查询。
```text
输入：
3 2
8 6 7
2 2
1 1
期望输出：
6
8
```
- 用例 2：全负数。
```text
输入：
5 2
-1 -5 -3 -4 -2
1 5
3 5
期望输出：
-5
-4
```

### V04-EX12 矩形批量加

- 归属卷：第 4 卷
- 覆盖模块：二维差分
- 考场用途：多次矩形加，最后输出整张矩阵。

**题目描述：** 初始 `n*m` 矩阵全为 `0`。执行 `q` 次操作，每次给子矩形 `(x1,y1)` 到 `(x2,y2)` 全部加 `v`。输出最终矩阵。

**输入格式：** 第一行三个整数 `n m q`。接下来 `q` 行每行五个整数 `x1 y1 x2 y2 v`。

**输出格式：** 输出 `n` 行，每行 `m` 个整数。

**样例输入：**
```text
3 3 2
1 1 2 2 5
2 2 3 3 1
```

**样例输出：**
```text
5 5 0
5 6 1
0 1 1
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m, q;
    cin >> n >> m >> q;
    vector<vector<ll>> diff(n + 2, vector<ll>(m + 2, 0));

    while (q--) {
        int x1, y1, x2, y2;
        ll v;
        cin >> x1 >> y1 >> x2 >> y2 >> v;
        diff[x1][y1] += v;
        diff[x2 + 1][y1] -= v;
        diff[x1][y2 + 1] -= v;
        diff[x2 + 1][y2 + 1] += v;
    }

    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            diff[i][j] += diff[i - 1][j] + diff[i][j - 1] - diff[i - 1][j - 1];
            if (j > 1) cout << ' ';
            cout << diff[i][j];
        }
        cout << '\n';
    }
    return 0;
}
```

**测试设计：**
- 用例 1：单格加。
```text
输入：
2 2 1
2 2 2 2 9
期望输出：
0 0
0 9
```
- 用例 2：整矩阵加后局部抵消。
```text
输入：
2 3 2
1 1 2 3 4
1 2 1 3 -1
期望输出：
4 3 3
4 4 4
```

## 第 5 卷：图论与树论例题

### V05-EX01 统一 1-index 建图统计

- 归属卷：第 5 卷
- 覆盖模块：统一 1-index 建图、邻接表、边权
- 考场用途：把有向/无向边统一放进 `Graph`，后续算法都从同一套邻接表出发。

**题目描述：** 给定一张带权图，点编号为 `1..n`。如果 `type=0` 表示无向图，如果 `type=1` 表示有向图。对每个点输出邻接边条数和从该点出发的邻接边权值和。无向边会同时出现在两个端点的邻接表中。

**输入格式：** 第一行三个整数 `n m type`。接下来 `m` 行每行三个整数 `u v w`。

**输出格式：** 输出 `n` 行，第 `i` 行两个整数：点 `i` 的邻接边条数和邻接边权值和。

**样例输入：**
```text
4 3 0
1 2 5
2 3 7
1 4 1
```

**样例输出：**
```text
2 6
2 12
1 7
1 1
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

struct AdjEdge {
    int to;
    ll w;
};

struct Graph {
    int n = 0;
    vector<vector<AdjEdge>> g;

    Graph(int n_ = 0) {
        init(n_);
    }

    void init(int n_) {
        n = n_;
        g.assign(n + 1, {});
    }

    void add_directed(int u, int v, ll w) {
        g[u].push_back({v, w});
    }

    void add_undirected(int u, int v, ll w) {
        g[u].push_back({v, w});
        g[v].push_back({u, w});
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m, type;
    cin >> n >> m >> type;
    Graph G(n);
    for (int i = 1; i <= m; i++) {
        int u, v;
        ll w;
        cin >> u >> v >> w;
        if (type == 0) G.add_undirected(u, v, w);
        else G.add_directed(u, v, w);
    }

    for (int u = 1; u <= n; u++) {
        ll sum = 0;
        for (auto e : G.g[u]) sum += e.w;
        cout << G.g[u].size() << ' ' << sum << '\n';
    }
    return 0;
}
```

**测试设计：**
- 用例 1：有向图中出度为 0 的点。
```text
输入：
3 2 1
1 2 4
1 3 5
期望输出：
2 9
0 0
0 0
```
- 用例 2：无边图。
```text
输入：
3 0 0
期望输出：
0 0
0 0
0 0
```

### V05-EX02 无权最短路

- 归属卷：第 5 卷
- 覆盖模块：BFS、无权图最短路
- 考场用途：所有边代价相同，求最少边数。

**题目描述：** 给定无向无权图和两个点 `s,t`，求从 `s` 到 `t` 的最少边数。若不可达，输出 `-1`。

**输入格式：** 第一行四个整数 `n m s t`。接下来 `m` 行每行两个整数 `u v`。

**输出格式：** 输出一个整数，表示最短距离或 `-1`。

**样例输入：**
```text
5 5 1 5
1 2
2 3
3 5
1 4
4 5
```

**样例输出：**
```text
2
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m, s, t;
    cin >> n >> m >> s >> t;
    vector<vector<int>> g(n + 1);
    for (int i = 1; i <= m; i++) {
        int u, v;
        cin >> u >> v;
        g[u].push_back(v);
        g[v].push_back(u);
    }

    vector<int> dist(n + 1, -1);
    queue<int> q;
    dist[s] = 0;
    q.push(s);
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        for (int v : g[u]) {
            if (dist[v] != -1) continue;
            dist[v] = dist[u] + 1;
            q.push(v);
        }
    }

    cout << dist[t] << '\n';
    return 0;
}
```

**测试设计：**
- 用例 1：起点等于终点。
```text
输入：
3 2 2 2
1 2
2 3
期望输出：
0
```
- 用例 2：不可达。
```text
输入：
4 1 1 4
1 2
期望输出：
-1
```

### V05-EX03 非负权单源最短路

- 归属卷：第 5 卷
- 覆盖模块：Dijkstra、优先队列
- 考场用途：边权非负的大图单源最短路。

**题目描述：** 给定一张有向非负权图和源点 `s`，输出 `s` 到所有点的最短距离。不可达点输出 `-1`。

**输入格式：** 第一行三个整数 `n m s`。接下来 `m` 行每行三个整数 `u v w`，表示有向边 `u -> v`。

**输出格式：** 输出一行 `n` 个整数，第 `i` 个为 `s` 到 `i` 的最短距离或 `-1`。

**样例输入：**
```text
4 4 1
1 2 2
1 3 5
2 3 1
3 4 4
```

**样例输出：**
```text
0 2 3 7
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;
const ll INF = (1LL << 62);

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m, s;
    cin >> n >> m >> s;
    vector<vector<pair<int, ll>>> g(n + 1);
    for (int i = 1; i <= m; i++) {
        int u, v;
        ll w;
        cin >> u >> v >> w;
        g[u].push_back({v, w});
    }

    vector<ll> dist(n + 1, INF);
    priority_queue<pair<ll, int>, vector<pair<ll, int>>, greater<pair<ll, int>>> pq;
    dist[s] = 0;
    pq.push({0, s});

    while (!pq.empty()) {
        auto [du, u] = pq.top();
        pq.pop();
        if (du != dist[u]) continue;
        for (auto [v, w] : g[u]) {
            if (du + w < dist[v]) {
                dist[v] = du + w;
                pq.push({dist[v], v});
            }
        }
    }

    for (int i = 1; i <= n; i++) {
        if (i > 1) cout << ' ';
        cout << (dist[i] == INF ? -1 : dist[i]);
    }
    cout << '\n';
    return 0;
}
```

**测试设计：**
- 用例 1：存在不可达点。
```text
输入：
4 1 1
1 2 7
期望输出：
0 7 -1 -1
```
- 用例 2：重边取更短。
```text
输入：
3 3 1
1 2 10
1 2 3
2 3 4
期望输出：
0 3 7
```

### V05-EX04 小图任意两点最短路

- 归属卷：第 5 卷
- 覆盖模块：Floyd
- 考场用途：`n` 较小且有多次任意两点最短路询问。

**题目描述：** 给定有向带权图，边权可以为负但保证没有负环。回答 `q` 次任意两点最短路询问，不可达输出 `-1`。

**输入格式：** 第一行三个整数 `n m q`，通常 `n <= 500`。接下来 `m` 行每行三个整数 `u v w`。接下来 `q` 行每行两个整数 `s t`。

**输出格式：** 对每个询问输出一行最短距离或 `-1`。

**样例输入：**
```text
3 3 3
1 2 4
1 3 10
2 3 -2
1 3
3 1
1 2
```

**样例输出：**
```text
2
-1
4
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;
const ll INF = (1LL << 60);
const int MAXN = 505;

ll dista[MAXN][MAXN];

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m, q;
    cin >> n >> m >> q;
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++) {
            dista[i][j] = (i == j ? 0 : INF);
        }
    }

    for (int i = 1; i <= m; i++) {
        int u, v;
        ll w;
        cin >> u >> v >> w;
        dista[u][v] = min(dista[u][v], w);
    }

    for (int k = 1; k <= n; k++) {
        for (int i = 1; i <= n; i++) {
            if (dista[i][k] == INF) continue;
            for (int j = 1; j <= n; j++) {
                if (dista[k][j] == INF) continue;
                dista[i][j] = min(dista[i][j], dista[i][k] + dista[k][j]);
            }
        }
    }

    while (q--) {
        int s, t;
        cin >> s >> t;
        cout << (dista[s][t] == INF ? -1 : dista[s][t]) << '\n';
    }
    return 0;
}
```

**测试设计：**
- 用例 1：重边。
```text
输入：
2 2 1
1 2 5
1 2 3
1 2
期望输出：
3
```
- 用例 2：通过中转更短。
```text
输入：
4 4 2
1 2 2
2 4 2
1 3 10
3 4 1
1 4
3 2
期望输出：
4
-1
```

### V05-EX05 负权单源最短路与负环检测

- 归属卷：第 5 卷
- 覆盖模块：Bellman-Ford
- 考场用途：有负权边时稳妥求单源最短路，并判断源点可达负环。

**题目描述：** 给定有向图和源点 `s`，边权可能为负。若从 `s` 可达某个负环，输出 `NEGATIVE CYCLE`；否则输出 `s` 到所有点的最短距离，不可达输出 `-1`。

**输入格式：** 第一行三个整数 `n m s`。接下来 `m` 行每行三个整数 `u v w`。

**输出格式：** 若存在源点可达负环，输出一行 `NEGATIVE CYCLE`。否则输出一行 `n` 个整数。

**样例输入：**
```text
3 3 1
1 2 4
1 3 10
2 3 -2
```

**样例输出：**
```text
0 4 2
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;
const ll INF = (1LL << 60);

struct Edge {
    int u, v;
    ll w;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m, s;
    cin >> n >> m >> s;
    vector<Edge> edges(m + 1);
    for (int i = 1; i <= m; i++) cin >> edges[i].u >> edges[i].v >> edges[i].w;

    vector<ll> dist(n + 1, INF);
    dist[s] = 0;
    for (int round = 1; round <= n - 1; round++) {
        bool changed = false;
        for (int i = 1; i <= m; i++) {
            auto e = edges[i];
            if (dist[e.u] != INF && dist[e.u] + e.w < dist[e.v]) {
                dist[e.v] = dist[e.u] + e.w;
                changed = true;
            }
        }
        if (!changed) break;
    }

    bool neg = false;
    for (int i = 1; i <= m; i++) {
        auto e = edges[i];
        if (dist[e.u] != INF && dist[e.u] + e.w < dist[e.v]) neg = true;
    }

    if (neg) {
        cout << "NEGATIVE CYCLE\n";
        return 0;
    }

    for (int i = 1; i <= n; i++) {
        if (i > 1) cout << ' ';
        cout << (dist[i] == INF ? -1 : dist[i]);
    }
    cout << '\n';
    return 0;
}
```

**测试设计：**
- 用例 1：源点可达负环。
```text
输入：
3 3 1
1 2 1
2 3 -2
3 2 -2
期望输出：
NEGATIVE CYCLE
```
- 用例 2：负环存在但源点不可达，不影响答案。
```text
输入：
4 2 1
2 3 -5
3 2 1
期望输出：
0 -1 -1 -1
```

### V05-EX06 DAG 最长路

- 归属卷：第 5 卷
- 覆盖模块：拓扑排序、DAG DP
- 考场用途：依赖关系无环时，按拓扑序做路径 DP。

**题目描述：** 给定有向带权图和起终点 `s,t`。若图有环，输出 `CYCLE`；否则输出从 `s` 到 `t` 的最长路径长度。若 `t` 不可达，输出 `-1`。

**输入格式：** 第一行四个整数 `n m s t`。接下来 `m` 行每行三个整数 `u v w`。

**输出格式：** 输出 `CYCLE`、`-1` 或最长路径长度。

**样例输入：**
```text
4 5 1 4
1 2 3
1 3 2
2 3 1
2 4 4
3 4 5
```

**样例输出：**
```text
9
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;
const ll NEG = -(1LL << 60);

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m, s, t;
    cin >> n >> m >> s >> t;
    vector<vector<pair<int, ll>>> g(n + 1);
    vector<int> indeg(n + 1, 0);
    for (int i = 1; i <= m; i++) {
        int u, v;
        ll w;
        cin >> u >> v >> w;
        g[u].push_back({v, w});
        indeg[v]++;
    }

    queue<int> q;
    for (int i = 1; i <= n; i++) {
        if (indeg[i] == 0) q.push(i);
    }

    vector<int> topo;
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        topo.push_back(u);
        for (auto [v, w] : g[u]) {
            indeg[v]--;
            if (indeg[v] == 0) q.push(v);
        }
    }

    if ((int)topo.size() != n) {
        cout << "CYCLE\n";
        return 0;
    }

    vector<ll> dp(n + 1, NEG);
    dp[s] = 0;
    for (int u : topo) {
        if (dp[u] == NEG) continue;
        for (auto [v, w] : g[u]) {
            dp[v] = max(dp[v], dp[u] + w);
        }
    }

    cout << (dp[t] == NEG ? -1 : dp[t]) << '\n';
    return 0;
}
```

**测试设计：**
- 用例 1：存在环。
```text
输入：
3 3 1 3
1 2 1
2 3 1
3 2 1
期望输出：
CYCLE
```
- 用例 2：终点不可达。
```text
输入：
4 2 1 4
1 2 5
2 3 5
期望输出：
-1
```

### V05-EX07 最小生成树总权值

- 归属卷：第 5 卷
- 覆盖模块：MST、Kruskal、DSU
- 考场用途：无向带权图连接所有点的最小成本。

**题目描述：** 给定无向带权图，求最小生成树总权值。若图不连通，输出 `orz`。

**输入格式：** 第一行两个整数 `n m`。接下来 `m` 行每行三个整数 `u v w`。

**输出格式：** 输出最小生成树总权值，或 `orz`。

**样例输入：**
```text
4 5
1 2 1
2 3 2
3 4 3
1 4 10
1 3 5
```

**样例输出：**
```text
6
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

struct Edge {
    int u, v;
    ll w;
};

struct DSU {
    vector<int> fa, sz;

    void init(int n) {
        fa.resize(n + 1);
        sz.assign(n + 1, 1);
        iota(fa.begin(), fa.end(), 0);
    }

    int find(int x) {
        while (x != fa[x]) {
            fa[x] = fa[fa[x]];
            x = fa[x];
        }
        return x;
    }

    bool unite(int a, int b) {
        a = find(a);
        b = find(b);
        if (a == b) return false;
        if (sz[a] < sz[b]) swap(a, b);
        fa[b] = a;
        sz[a] += sz[b];
        return true;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;
    vector<Edge> edges(m);
    for (int i = 0; i < m; i++) cin >> edges[i].u >> edges[i].v >> edges[i].w;

    sort(edges.begin(), edges.end(), [](const Edge& a, const Edge& b) {
        return a.w < b.w;
    });

    DSU dsu;
    dsu.init(n);
    ll total = 0;
    int used = 0;
    for (auto e : edges) {
        if (dsu.unite(e.u, e.v)) {
            total += e.w;
            used++;
        }
    }

    if (used != n - 1) cout << "orz\n";
    else cout << total << '\n';
    return 0;
}
```

**测试设计：**
- 用例 1：不连通。
```text
输入：
4 2
1 2 1
3 4 2
期望输出：
orz
```
- 用例 2：存在负边。
```text
输入：
3 3
1 2 -5
2 3 2
1 3 10
期望输出：
-3
```

### V05-EX08 二分图最大匹配

- 归属卷：第 5 卷
- 覆盖模块：二分图、Kuhn 匹配
- 考场用途：左右部点各最多匹配一次，求最大配对数。

**题目描述：** 给定一个二分图，左部有 `nL` 个点，右部有 `nR` 个点，边只从左部连向右部。求最大匹配数。

**输入格式：** 第一行三个整数 `nL nR m`。接下来 `m` 行每行两个整数 `u v`，表示左部点 `u` 可匹配右部点 `v`。

**输出格式：** 输出最大匹配数。

**样例输入：**
```text
3 3 4
1 1
1 2
2 2
3 2
```

**样例输出：**
```text
2
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

bool dfs(int u, const vector<vector<int>>& adj, vector<int>& seen, vector<int>& matchR, int tag) {
    if (seen[u] == tag) return false;
    seen[u] = tag;
    for (int r : adj[u]) {
        if (matchR[r] == 0 || dfs(matchR[r], adj, seen, matchR, tag)) {
            matchR[r] = u;
            return true;
        }
    }
    return false;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int nL, nR, m;
    cin >> nL >> nR >> m;
    vector<vector<int>> adj(nL + 1);
    for (int i = 1; i <= m; i++) {
        int u, v;
        cin >> u >> v;
        adj[u].push_back(v);
    }

    vector<int> matchR(nR + 1, 0), seen(nL + 1, 0);
    int ans = 0;
    for (int u = 1; u <= nL; u++) {
        if (dfs(u, adj, seen, matchR, u)) ans++;
    }

    cout << ans << '\n';
    return 0;
}
```

**测试设计：**
- 用例 1：完美匹配。
```text
输入：
2 2 2
1 1
2 2
期望输出：
2
```
- 用例 2：所有左部都只能抢同一个右部。
```text
输入：
3 1 3
1 1
2 1
3 1
期望输出：
1
```

### V05-EX09 强连通分量大小

- 归属卷：第 5 卷
- 覆盖模块：SCC、Tarjan
- 考场用途：有向图先缩强连通分量，再接 DAG 处理。

**题目描述：** 给定有向图，求强连通分量个数，并输出每个分量的大小。为了输出稳定，分量大小按升序输出。

**输入格式：** 第一行两个整数 `n m`。接下来 `m` 行每行两个整数 `u v`，表示有向边。

**输出格式：** 第一行输出 SCC 个数。第二行按升序输出所有 SCC 大小。

**样例输入：**
```text
4 4
1 2
2 1
2 3
3 4
```

**样例输出：**
```text
3
1 1 2
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

struct Tarjan {
    int n = 0;
    int timer = 0;
    vector<vector<int>> g;
    vector<int> dfn, low, inStack, st, compSize;

    void init(int n_) {
        n = n_;
        g.assign(n + 1, {});
        dfn.assign(n + 1, 0);
        low.assign(n + 1, 0);
        inStack.assign(n + 1, 0);
        st.clear();
        compSize.clear();
        timer = 0;
    }

    void add_edge(int u, int v) {
        g[u].push_back(v);
    }

    void dfs(int u) {
        dfn[u] = low[u] = ++timer;
        st.push_back(u);
        inStack[u] = 1;
        for (int v : g[u]) {
            if (!dfn[v]) {
                dfs(v);
                low[u] = min(low[u], low[v]);
            } else if (inStack[v]) {
                low[u] = min(low[u], dfn[v]);
            }
        }
        if (low[u] == dfn[u]) {
            int cnt = 0;
            while (true) {
                int x = st.back();
                st.pop_back();
                inStack[x] = 0;
                cnt++;
                if (x == u) break;
            }
            compSize.push_back(cnt);
        }
    }

    vector<int> run() {
        for (int i = 1; i <= n; i++) {
            if (!dfn[i]) dfs(i);
        }
        sort(compSize.begin(), compSize.end());
        return compSize;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;
    Tarjan solver;
    solver.init(n);
    for (int i = 1; i <= m; i++) {
        int u, v;
        cin >> u >> v;
        solver.add_edge(u, v);
    }

    vector<int> sizes = solver.run();
    cout << sizes.size() << '\n';
    for (int i = 0; i < (int)sizes.size(); i++) {
        if (i) cout << ' ';
        cout << sizes[i];
    }
    cout << '\n';
    return 0;
}
```

**测试设计：**
- 用例 1：整图一个 SCC。
```text
输入：
3 3
1 2
2 3
3 1
期望输出：
1
3
```
- 用例 2：无边图。
```text
输入：
3 0
期望输出：
3
1 1 1
```

### V05-EX10 LCA 与树上距离

- 归属卷：第 5 卷
- 覆盖模块：LCA、倍增、树上距离
- 考场用途：多次询问树上两点最近公共祖先和路径长度。

**题目描述：** 给定一棵带权无向树，以 `1` 为根。对每个询问 `u v`，输出 `LCA(u,v)` 和两点距离。

**输入格式：** 第一行两个整数 `n q`。接下来 `n-1` 行每行三个整数 `u v w`。接下来 `q` 行每行两个整数 `u v`。

**输出格式：** 对每个询问输出一行两个整数：最近公共祖先和距离。

**样例输入：**
```text
5 3
1 2 3
1 3 2
2 4 4
2 5 1
4 5
4 3
2 3
```

**样例输出：**
```text
2 5
1 9
1 5
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, q;
    cin >> n >> q;
    vector<vector<pair<int, ll>>> g(n + 1);
    for (int i = 1; i <= n - 1; i++) {
        int u, v;
        ll w;
        cin >> u >> v >> w;
        g[u].push_back({v, w});
        g[v].push_back({u, w});
    }

    int LOG = 1;
    while ((1 << LOG) <= n) LOG++;
    vector<vector<int>> up(LOG, vector<int>(n + 1, 1));
    vector<int> depth(n + 1, 0);
    vector<ll> distRoot(n + 1, 0);

    queue<int> bfs;
    vector<int> vis(n + 1, 0);
    bfs.push(1);
    vis[1] = 1;
    up[0][1] = 1;
    depth[1] = 0;
    while (!bfs.empty()) {
        int u = bfs.front();
        bfs.pop();
        for (auto [v, w] : g[u]) {
            if (vis[v]) continue;
            vis[v] = 1;
            up[0][v] = u;
            depth[v] = depth[u] + 1;
            distRoot[v] = distRoot[u] + w;
            bfs.push(v);
        }
    }

    for (int k = 1; k < LOG; k++) {
        for (int v = 1; v <= n; v++) {
            up[k][v] = up[k - 1][up[k - 1][v]];
        }
    }

    auto lift = [&](int u, int steps) {
        for (int k = 0; k < LOG; k++) {
            if (steps & (1 << k)) u = up[k][u];
        }
        return u;
    };

    auto lca = [&](int a, int b) {
        if (depth[a] < depth[b]) swap(a, b);
        a = lift(a, depth[a] - depth[b]);
        if (a == b) return a;
        for (int k = LOG - 1; k >= 0; k--) {
            if (up[k][a] != up[k][b]) {
                a = up[k][a];
                b = up[k][b];
            }
        }
        return up[0][a];
    };

    while (q--) {
        int u, v;
        cin >> u >> v;
        int c = lca(u, v);
        ll d = distRoot[u] + distRoot[v] - 2LL * distRoot[c];
        cout << c << ' ' << d << '\n';
    }
    return 0;
}
```

**测试设计：**
- 用例 1：同一点查询。
```text
输入：
2 1
1 2 8
2 2
期望输出：
2 0
```
- 用例 2：链状树。
```text
输入：
4 2
1 2 1
2 3 2
3 4 3
4 2
1 4
期望输出：
2 5
1 6
```

### V05-EX11 树上最大独立集

- 归属卷：第 5 卷
- 覆盖模块：树形 DP
- 考场用途：父子不能同时选的树上选点最优值。

**题目描述：** 给定一棵无向树，每个点有权值。选择若干点，使任意一条边的两个端点不能同时被选，求最大权值和。

**输入格式：** 第一行整数 `n`。第二行 `n` 个整数表示点权。接下来 `n-1` 行每行两个整数 `u v`。

**输出格式：** 输出最大权值和。

**样例输入：**
```text
5
1 2 3 4 5
1 2
1 3
2 4
2 5
```

**样例输出：**
```text
12
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<ll> w(n + 1);
    for (int i = 1; i <= n; i++) cin >> w[i];

    vector<vector<int>> g(n + 1);
    for (int i = 1; i <= n - 1; i++) {
        int u, v;
        cin >> u >> v;
        g[u].push_back(v);
        g[v].push_back(u);
    }

    vector<array<ll, 2>> dp(n + 1);
    function<void(int, int)> dfs = [&](int u, int p) {
        dp[u][0] = 0;
        dp[u][1] = w[u];
        for (int v : g[u]) {
            if (v == p) continue;
            dfs(v, u);
            dp[u][0] += max(dp[v][0], dp[v][1]);
            dp[u][1] += dp[v][0];
        }
    };

    dfs(1, 0);
    cout << max(dp[1][0], dp[1][1]) << '\n';
    return 0;
}
```

**测试设计：**
- 用例 1：单点树。
```text
输入：
1
7
期望输出：
7
```
- 用例 2：星形树，中心很大。
```text
输入：
4
10 3 4 5
1 2
1 3
1 4
期望输出：
12
```

### V05-EX12 无向图桥边

- 归属卷：第 5 卷
- 覆盖模块：Lowlink、桥、1-index 边号
- 考场用途：找删除后会增加连通块数量的关键边，并正确处理重边。

**题目描述：** 给定无向图，边按输入顺序编号为 `1..m`。输出所有桥的边号，按升序排列。

**输入格式：** 第一行两个整数 `n m`。接下来 `m` 行每行两个整数 `u v`。

**输出格式：** 第一行输出桥的数量。第二行输出所有桥的边号；若没有桥，第二行为空行。

**样例输入：**
```text
5 5
1 2
2 3
3 1
3 4
4 5
```

**样例输出：**
```text
2
4 5
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

struct Edge {
    int to;
    int eid;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;
    vector<vector<Edge>> g(n + 1);
    for (int id = 1; id <= m; id++) {
        int u, v;
        cin >> u >> v;
        g[u].push_back({v, id});
        g[v].push_back({u, id});
    }

    vector<int> dfn(n + 1, 0), low(n + 1, 0), bridges;
    int timer = 0;

    function<void(int, int)> dfs = [&](int u, int parentEdge) {
        dfn[u] = low[u] = ++timer;
        for (auto e : g[u]) {
            int v = e.to;
            if (!dfn[v]) {
                dfs(v, e.eid);
                low[u] = min(low[u], low[v]);
                if (low[v] > dfn[u]) bridges.push_back(e.eid);
            } else if (e.eid != parentEdge) {
                low[u] = min(low[u], dfn[v]);
            }
        }
    };

    for (int i = 1; i <= n; i++) {
        if (!dfn[i]) dfs(i, 0);
    }

    sort(bridges.begin(), bridges.end());
    cout << bridges.size() << '\n';
    for (int i = 0; i < (int)bridges.size(); i++) {
        if (i) cout << ' ';
        cout << bridges[i];
    }
    cout << '\n';
    return 0;
}
```

**测试设计：**
- 用例 1：环图没有桥。
```text
输入：
3 3
1 2
2 3
3 1
期望输出：
0

```
- 用例 2：重边不是桥，尾部单边是桥。
```text
输入：
3 3
1 2
1 2
2 3
期望输出：
1
3
```
