# v0.2 例题扩展 Worker A：第 0 / 7 / 8 卷

- 交付范围：第 0 卷作战路由、第 7 卷调试对拍、第 8 卷洛谷覆盖索引。
- 例题数量：第 0 卷 10 题，第 7 卷 10 题，第 8 卷 10 题。
- 代码口径：C++17，标准输入输出，不使用文件读写，默认 1-index。

## 第 0 卷：作战路由与模块拼接

### V00-EX01 静态区间和路由

- 归属卷：第 0 卷
- 覆盖模块：ROUTE-00、DS-01、OPS-00
- 考场用途：训练看到“数组不修改，多次问区间和”时立即路由到前缀和。

**题目描述：** 给定长度为 `n` 的整数数组，回答 `q` 次闭区间 `[l,r]` 的元素和。数组不会修改。

**输入格式：** 第一行两个整数 `n q`。第二行 `n` 个整数。接下来 `q` 行，每行两个整数 `l r`。

**输出格式：** 每次询问输出一行区间和。

**样例输入：**
```text
5 3
1 -2 3 4 5
1 3
2 5
4 4
```

**样例输出：**
```text
2
10
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
    vector<ll> prefix(n + 1, 0);
    for (int i = 1; i <= n; i++) {
        ll x;
        cin >> x;
        prefix[i] = prefix[i - 1] + x;
    }
    while (q--) {
        int l, r;
        cin >> l >> r;
        cout << prefix[r] - prefix[l - 1] << '\n';
    }
    return 0;
}
```

**测试设计：**

- 测试 1 输入：
```text
1 2
7
1 1
1 1
```
期望输出：
```text
7
7
```
- 测试 2 输入：
```text
3 1
-5 -6 -7
1 3
```
期望输出：
```text
-18
```

### V00-EX02 离线区间加最终数组

- 归属卷：第 0 卷
- 覆盖模块：ROUTE-00、DS-01、OPS-00
- 考场用途：训练“区间加但只在最后输出”路由到差分数组。

**题目描述：** 给定数组，执行 `q` 次操作：把闭区间 `[l,r]` 内所有数加上 `x`。所有操作结束后输出最终数组。

**输入格式：** 第一行两个整数 `n q`。第二行 `n` 个整数。接下来 `q` 行，每行 `l r x`。

**输出格式：** 输出一行 `n` 个整数，表示最终数组。

**样例输入：**
```text
5 3
1 2 3 4 5
1 3 2
2 5 -1
5 5 10
```

**样例输出：**
```text
3 3 4 3 14
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
    while (q--) {
        int l, r;
        ll x;
        cin >> l >> r >> x;
        diff[l] += x;
        diff[r + 1] -= x;
    }
    ll add = 0;
    for (int i = 1; i <= n; i++) {
        add += diff[i];
        if (i > 1) cout << ' ';
        cout << a[i] + add;
    }
    cout << '\n';
    return 0;
}
```

**测试设计：**

- 测试 1 输入：
```text
4 1
0 0 0 0
1 4 5
```
期望输出：
```text
5 5 5 5
```
- 测试 2 输入：
```text
3 2
1 1 1
1 2 -3
2 3 4
```
期望输出：
```text
-2 2 5
```

### V00-EX03 单点赋值与区间和

- 归属卷：第 0 卷
- 覆盖模块：ROUTE-00、DS-02、OPS-00
- 考场用途：训练“单点赋值加区间和”路由到 树状数组，并把赋值转换成差量。

**题目描述：** 维护一个数组，支持两种操作：`S p x` 表示把 `a[p]` 赋值为 `x`；`Q l r` 表示查询 `[l,r]` 的和。

**输入格式：** 第一行两个整数 `n q`。第二行 `n` 个整数。接下来 `q` 行，每行一个操作。

**输出格式：** 每个 `Q` 操作输出一行答案。

**样例输入：**
```text
5 5
1 2 3 4 5
Q 1 5
S 3 10
Q 2 4
S 1 -1
Q 1 3
```

**样例输出：**
```text
15
16
11
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct BIT {
    int n;
    vector<ll> bit;

    void init(int n_) {
        n = n_;
        bit.assign(n + 1, 0);
    }

    void add(int pos, ll delta) {
        for (int i = pos; i <= n; i += i & -i) bit[i] += delta;
    }

    ll prefix(int pos) const {
        ll res = 0;
        for (int i = pos; i > 0; i -= i & -i) res += bit[i];
        return res;
    }

    ll query(int l, int r) const {
        return prefix(r) - prefix(l - 1);
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, q;
    cin >> n >> q;
    vector<ll> a(n + 1);
    BIT fw;
    fw.init(n);
    for (int i = 1; i <= n; i++) {
        cin >> a[i];
        fw.add(i, a[i]);
    }
    while (q--) {
        char op;
        cin >> op;
        if (op == 'S') {
            int p;
            ll x;
            cin >> p >> x;
            fw.add(p, x - a[p]);
            a[p] = x;
        } else {
            int l, r;
            cin >> l >> r;
            cout << fw.query(l, r) << '\n';
        }
    }
    return 0;
}
```

**测试设计：**

- 测试 1 输入：
```text
1 4
5
Q 1 1
S 1 7
S 1 -2
Q 1 1
```
期望输出：
```text
5
-2
```
- 测试 2 输入：
```text
3 2
1 2 3
Q 1 1
Q 3 3
```
期望输出：
```text
1
3
```

### V00-EX04 大坐标频次统计

- 归属卷：第 0 卷
- 覆盖模块：ROUTE-00、CPP-007、DS-02
- 考场用途：训练“值域巨大但出现值有限”路由到离散化加 树状数组。

**题目描述：** 依次处理 `q` 个操作：`A x` 表示加入一个值为 `x` 的数，可重复加入；`C l r` 表示询问当前数中有多少个值落在 `[l,r]`。

**输入格式：** 第一行一个整数 `q`。接下来 `q` 行，每行一个操作。

**输出格式：** 每个 `C` 操作输出一行答案。

**样例输入：**
```text
6
A 1000000000
A -5
C -10 100
A 7
C 7 1000000000
C 8 9
```

**样例输出：**
```text
1
2
0
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct BIT {
    int n;
    vector<int> bit;

    void init(int n_) {
        n = n_;
        bit.assign(n + 1, 0);
    }

    void add(int pos, int delta) {
        for (int i = pos; i <= n; i += i & -i) bit[i] += delta;
    }

    int prefix(int pos) const {
        int res = 0;
        for (int i = pos; i > 0; i -= i & -i) res += bit[i];
        return res;
    }
};

struct Operation {
    char type;
    ll x;
    ll y;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int q;
    cin >> q;
    vector<Operation> ops(q + 1);
    vector<ll> coords;
    for (int i = 1; i <= q; i++) {
        cin >> ops[i].type >> ops[i].x;
        if (ops[i].type == 'A') {
            ops[i].y = 0;
            coords.push_back(ops[i].x);
        } else {
            cin >> ops[i].y;
        }
    }
    sort(coords.begin(), coords.end());
    coords.erase(unique(coords.begin(), coords.end()), coords.end());

    BIT fw;
    fw.init((int)coords.size());
    for (int i = 1; i <= q; i++) {
        if (ops[i].type == 'A') {
            int id = int(lower_bound(coords.begin(), coords.end(), ops[i].x) - coords.begin()) + 1;
            fw.add(id, 1);
        } else {
            int right = int(upper_bound(coords.begin(), coords.end(), ops[i].y) - coords.begin());
            int left = int(lower_bound(coords.begin(), coords.end(), ops[i].x) - coords.begin());
            cout << fw.prefix(right) - fw.prefix(left) << '\n';
        }
    }
    return 0;
}
```

**测试设计：**

- 测试 1 输入：
```text
4
A 5
A 5
C 5 5
C 6 7
```
期望输出：
```text
2
0
```
- 测试 2 输入：
```text
3
A -100
A 0
C -200 -1
```
期望输出：
```text
1
```

### V00-EX05 网格最少步数

- 归属卷：第 0 卷
- 覆盖模块：ROUTE-00、GRAPH-02、OPS-00
- 考场用途：训练“无权最少步数”路由到 BFS，而不是 DFS。

**题目描述：** 给定 `n` 行 `m` 列网格，`.` 可走，`#` 不可走，`S` 是起点，`T` 是终点。每步可向上下左右走一格，求最少步数。不可达输出 `-1`。

**输入格式：** 第一行两个整数 `n m`。接下来 `n` 行，每行一个长度为 `m` 的字符串。

**输出格式：** 输出最少步数。

**样例输入：**
```text
3 4
S..#
.#..
..T.
```

**样例输出：**
```text
4
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;
    vector<string> grid(n + 1);
    pair<int, int> start = {-1, -1};
    pair<int, int> target = {-1, -1};
    for (int i = 1; i <= n; i++) {
        string row;
        cin >> row;
        grid[i] = " " + row;
        for (int j = 1; j <= m; j++) {
            if (grid[i][j] == 'S') start = {i, j};
            if (grid[i][j] == 'T') target = {i, j};
        }
    }

    vector<vector<int>> dist(n + 1, vector<int>(m + 1, -1));
    queue<pair<int, int>> q;
    dist[start.first][start.second] = 0;
    q.push(start);
    int dx[4] = {1, -1, 0, 0};
    int dy[4] = {0, 0, 1, -1};
    while (!q.empty()) {
        auto [x, y] = q.front();
        q.pop();
        for (int d = 0; d < 4; d++) {
            int nx = x + dx[d];
            int ny = y + dy[d];
            if (nx < 1 || nx > n || ny < 1 || ny > m) continue;
            if (grid[nx][ny] == '#') continue;
            if (dist[nx][ny] != -1) continue;
            dist[nx][ny] = dist[x][y] + 1;
            q.push({nx, ny});
        }
    }
    cout << dist[target.first][target.second] << '\n';
    return 0;
}
```

**测试设计：**

- 测试 1 输入：
```text
1 2
ST
```
期望输出：
```text
1
```
- 测试 2 输入：
```text
1 3
S#T
```
期望输出：
```text
-1
```

### V00-EX06 非负权道路最短路

- 归属卷：第 0 卷
- 覆盖模块：ROUTE-00、GRAPH-03、CPP-004
- 考场用途：训练“非负边权最短路”路由到 Dijkstra 和小根堆。

**题目描述：** 给定无向非负权图和起点 `s`，回答若干目标点的最短距离。不可达输出 `-1`。

**输入格式：** 第一行三个整数 `n m s`。接下来 `m` 行为 `u v w`。然后一行整数 `q`。接下来 `q` 行每行一个目标点。

**输出格式：** 每个目标点输出一行距离。

**样例输入：**
```text
4 5 1
1 2 5
1 3 2
3 2 1
2 4 2
3 4 10
3
2
4
1
```

**样例输出：**
```text
3
5
0
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const ll INF = 4'000'000'000'000'000'000LL;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m, s;
    cin >> n >> m >> s;
    vector<vector<pair<int, ll>>> graph(n + 1);
    for (int i = 1; i <= m; i++) {
        int u, v;
        ll w;
        cin >> u >> v >> w;
        graph[u].push_back({v, w});
        graph[v].push_back({u, w});
    }

    vector<ll> dist(n + 1, INF);
    priority_queue<pair<ll, int>, vector<pair<ll, int>>, greater<pair<ll, int>>> pq;
    dist[s] = 0;
    pq.push({0, s});
    while (!pq.empty()) {
        auto [du, u] = pq.top();
        pq.pop();
        if (du != dist[u]) continue;
        for (auto [v, w] : graph[u]) {
            if (dist[v] > du + w) {
                dist[v] = du + w;
                pq.push({dist[v], v});
            }
        }
    }

    int q;
    cin >> q;
    while (q--) {
        int t;
        cin >> t;
        cout << (dist[t] == INF ? -1 : dist[t]) << '\n';
    }
    return 0;
}
```

**测试设计：**

- 测试 1 输入：
```text
3 1 1
1 2 5
1
3
```
期望输出：
```text
-1
```
- 测试 2 输入：
```text
2 2 1
1 2 10
1 2 3
1
2
```
期望输出：
```text
3
```

### V00-EX07 依赖任务排序

- 归属卷：第 0 卷
- 覆盖模块：ROUTE-00、GRAPH-05、OPS-00
- 考场用途：训练“先后依赖”路由到拓扑排序，并检查有环。

**题目描述：** 有 `n` 个任务和 `m` 条依赖关系 `u v`，表示任务 `u` 必须在任务 `v` 前完成。输出字典序尽量小的合法顺序；如果不存在，输出 `CYCLE`。

**输入格式：** 第一行两个整数 `n m`。接下来 `m` 行，每行两个整数 `u v`。

**输出格式：** 合法时输出一行任务顺序；否则输出 `CYCLE`。

**样例输入：**
```text
4 3
1 3
2 3
3 4
```

**样例输出：**
```text
1 2 3 4
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;
    vector<vector<int>> graph(n + 1);
    vector<int> indeg(n + 1, 0);
    for (int i = 1; i <= m; i++) {
        int u, v;
        cin >> u >> v;
        graph[u].push_back(v);
        indeg[v]++;
    }

    priority_queue<int, vector<int>, greater<int>> pq;
    for (int i = 1; i <= n; i++) {
        if (indeg[i] == 0) pq.push(i);
    }

    vector<int> order;
    while (!pq.empty()) {
        int u = pq.top();
        pq.pop();
        order.push_back(u);
        for (int v : graph[u]) {
            indeg[v]--;
            if (indeg[v] == 0) pq.push(v);
        }
    }

    if ((int)order.size() != n) {
        cout << "CYCLE\n";
    } else {
        for (int i = 0; i < n; i++) {
            if (i) cout << ' ';
            cout << order[i];
        }
        cout << '\n';
    }
    return 0;
}
```

**测试设计：**

- 测试 1 输入：
```text
3 3
1 2
2 3
3 1
```
期望输出：
```text
CYCLE
```
- 测试 2 输入：
```text
3 1
2 3
```
期望输出：
```text
1 2 3
```

### V00-EX08 容量选择路线

- 归属卷：第 0 卷
- 覆盖模块：ROUTE-00、DP-06、OPS-00
- 考场用途：训练“每个物品最多选一次”路由到 0/1 背包，容量循环倒序。

**题目描述：** 有 `n` 个物品，每个物品有重量 `w` 和价值 `v`，每个物品最多选一次。背包容量为 `W`，求最大总价值。

**输入格式：** 第一行两个整数 `n W`。接下来 `n` 行，每行两个整数 `w v`。

**输出格式：** 输出最大价值。

**样例输入：**
```text
4 7
3 4
4 5
2 3
3 7
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

    int n, W;
    cin >> n >> W;
    vector<ll> dp(W + 1, 0);
    for (int i = 1; i <= n; i++) {
        int w;
        ll v;
        cin >> w >> v;
        for (int cap = W; cap >= w; cap--) {
            dp[cap] = max(dp[cap], dp[cap - w] + v);
        }
    }
    cout << dp[W] << '\n';
    return 0;
}
```

**测试设计：**

- 测试 1 输入：
```text
1 2
1 1
```
期望输出：
```text
1
```
- 测试 2 输入：
```text
2 3
4 10
5 20
```
期望输出：
```text
0
```

### V00-EX09 模式串出现次数

- 归属卷：第 0 卷
- 覆盖模块：ROUTE-00、STR-02、CPP-011
- 考场用途：训练“长文本查模式串”路由到 KMP，并处理重叠出现。

**题目描述：** 给定文本串 `s` 和模式串 `p`，统计 `p` 在 `s` 中出现了多少次，允许重叠。

**输入格式：** 第一行一个字符串 `s`。第二行一个字符串 `p`。

**输出格式：** 输出出现次数。

**样例输入：**
```text
aaaaa
aa
```

**样例输出：**
```text
4
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string s_raw, p_raw;
    cin >> s_raw >> p_raw;
    string s = " " + s_raw;
    string p = " " + p_raw;
    int n = (int)s_raw.size();
    int m = (int)p_raw.size();
    vector<int> pi(m + 1, 0);
    for (int i = 2; i <= m; i++) {
        int j = pi[i - 1];
        while (j > 0 && p[i] != p[j + 1]) j = pi[j];
        if (p[i] == p[j + 1]) j++;
        pi[i] = j;
    }

    int ans = 0;
    int j = 0;
    for (int i = 1; i <= n; i++) {
        while (j > 0 && s[i] != p[j + 1]) j = pi[j];
        if (s[i] == p[j + 1]) j++;
        if (j == m) {
            ans++;
            j = pi[j];
        }
    }
    cout << ans << '\n';
    return 0;
}
```

**测试设计：**

- 测试 1 输入：
```text
abc
d
```
期望输出：
```text
0
```
- 测试 2 输入：
```text
abababa
aba
```
期望输出：
```text
3
```

### V00-EX10 提交版本选择器

- 归属卷：第 0 卷
- 覆盖模块：OPS-01、ROUTE-01、TRAIN-00
- 考场用途：训练“先保分，再修正解”的提交路线选择。

**题目描述：** 你有 `k` 个候选提交版本。每个版本有预计得分 `score`、风险值 `risk` 和剩余调试时间 `time`。只考虑 `risk <= R` 且 `time <= M` 的版本。在可选版本中，优先选得分最高；得分相同选风险更低；仍相同选用时更短；仍相同选编号更小。若没有可选版本，输出 `HOLD`。

**输入格式：** 第一行三个整数 `k R M`。接下来 `k` 行，每行三个整数 `score risk time`。

**输出格式：** 可选时输出版本编号和预计得分；不可选时输出 `HOLD`。

**样例输入：**
```text
4 30 20
60 10 8
80 40 12
80 25 25
70 20 18
```

**样例输出：**
```text
4 70
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

struct Version {
    int id;
    int score;
    int risk;
    int time_need;
};

bool better(const Version &a, const Version &b) {
    if (a.score != b.score) return a.score > b.score;
    if (a.risk != b.risk) return a.risk < b.risk;
    if (a.time_need != b.time_need) return a.time_need < b.time_need;
    return a.id < b.id;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int k, R, M;
    cin >> k >> R >> M;
    bool has = false;
    Version best{0, 0, 0, 0};
    for (int i = 1; i <= k; i++) {
        Version cur;
        cur.id = i;
        cin >> cur.score >> cur.risk >> cur.time_need;
        if (cur.risk > R || cur.time_need > M) continue;
        if (!has || better(cur, best)) {
            best = cur;
            has = true;
        }
    }

    if (!has) {
        cout << "HOLD\n";
    } else {
        cout << best.id << ' ' << best.score << '\n';
    }
    return 0;
}
```

**测试设计：**

- 测试 1 输入：
```text
2 10 5
100 20 1
80 5 6
```
期望输出：
```text
HOLD
```
- 测试 2 输入：
```text
2 50 50
90 30 10
90 20 20
```
期望输出：
```text
2 90
```

## 第 7 卷：调试、反例与对拍训练

### V07-EX01 多组图连通块清空

- 归属卷：第 7 卷
- 覆盖模块：TRAIN-00、TRAIN-01、GRAPH-01
- 考场用途：训练多组数据时每组重新建图、清空 `visited` 和邻接表。

**题目描述：** 给定 `T` 组无向图，分别输出每组图的连通块个数。

**输入格式：** 第一行一个整数 `T`。每组第一行两个整数 `n m`，接下来 `m` 行每行一条无向边 `u v`。

**输出格式：** 每组输出一行连通块个数。

**样例输入：**
```text
2
4 2
1 2
3 4
3 0
```

**样例输出：**
```text
2
3
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;
    while (T--) {
        int n, m;
        cin >> n >> m;
        vector<vector<int>> graph(n + 1);
        for (int i = 1; i <= m; i++) {
            int u, v;
            cin >> u >> v;
            graph[u].push_back(v);
            graph[v].push_back(u);
        }
        vector<int> visited(n + 1, 0);
        int components = 0;
        for (int start = 1; start <= n; start++) {
            if (visited[start]) continue;
            components++;
            queue<int> q;
            q.push(start);
            visited[start] = 1;
            while (!q.empty()) {
                int u = q.front();
                q.pop();
                for (int v : graph[u]) {
                    if (!visited[v]) {
                        visited[v] = 1;
                        q.push(v);
                    }
                }
            }
        }
        cout << components << '\n';
    }
    return 0;
}
```

**测试设计：**

- 测试 1 输入：
```text
1
1 0
```
期望输出：
```text
1
```
- 测试 2 输入：
```text
2
3 2
1 2
2 3
2 0
```
期望输出：
```text
1
2
```

### V07-EX02 前缀和暴力核验

- 归属卷：第 7 卷
- 覆盖模块：TRAIN-00、TRAIN-02、DS-01
- 考场用途：训练优化版写完后保留暴力版，对每个查询做小规模核验。

**题目描述：** 给定数组和若干区间和询问。程序同时用前缀和与暴力循环计算答案；若发现不一致，输出 `CHECK_FAILED` 并结束，否则输出每次询问答案。

**输入格式：** 第一行两个整数 `n q`。第二行 `n` 个整数。接下来 `q` 行，每行两个整数 `l r`。

**输出格式：** 若核验通过，每个询问输出一行答案；否则输出 `CHECK_FAILED`。

**样例输入：**
```text
4 3
2 -1 5 3
1 4
2 3
4 4
```

**样例输出：**
```text
9
4
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

    int n, q;
    cin >> n >> q;
    vector<ll> a(n + 1), prefix(n + 1, 0);
    for (int i = 1; i <= n; i++) {
        cin >> a[i];
        prefix[i] = prefix[i - 1] + a[i];
    }
    while (q--) {
        int l, r;
        cin >> l >> r;
        ll fast = prefix[r] - prefix[l - 1];
        ll slow = 0;
        for (int i = l; i <= r; i++) slow += a[i];
        if (fast != slow) {
            cout << "CHECK_FAILED\n";
            return 0;
        }
        cout << fast << '\n';
    }
    return 0;
}
```

**测试设计：**

- 测试 1 输入：
```text
1 1
-8
1 1
```
期望输出：
```text
-8
```
- 测试 2 输入：
```text
3 2
10 20 30
1 1
1 3
```
期望输出：
```text
10
60
```

### V07-EX03 背包循环顺序反例

- 归属卷：第 7 卷
- 覆盖模块：TRAIN-01、DP-06、BRUTE-15
- 考场用途：训练用最小反例识别 0/1 背包容量正序导致重复选择的问题。

**题目描述：** 给定 0/1 背包数据。程序输出正确答案，并判断“错误的容量正序写法”是否会得到不同结果。若不同，第二行输出 `LOOP_RISK`，否则输出 `SAME`。

**输入格式：** 第一行两个整数 `n W`。接下来 `n` 行，每行 `w v`。

**输出格式：** 第一行输出 0/1 背包正确最大价值。第二行输出 `LOOP_RISK` 或 `SAME`。

**样例输入：**
```text
1 2
1 1
```

**样例输出：**
```text
1
LOOP_RISK
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, W;
    cin >> n >> W;
    vector<int> w(n + 1);
    vector<ll> v(n + 1);
    for (int i = 1; i <= n; i++) cin >> w[i] >> v[i];

    vector<ll> correct(W + 1, 0), forward_wrong(W + 1, 0);
    for (int i = 1; i <= n; i++) {
        for (int cap = W; cap >= w[i]; cap--) {
            correct[cap] = max(correct[cap], correct[cap - w[i]] + v[i]);
        }
        for (int cap = w[i]; cap <= W; cap++) {
            forward_wrong[cap] = max(forward_wrong[cap], forward_wrong[cap - w[i]] + v[i]);
        }
    }

    cout << correct[W] << '\n';
    cout << (correct[W] == forward_wrong[W] ? "SAME" : "LOOP_RISK") << '\n';
    return 0;
}
```

**测试设计：**

- 测试 1 输入：
```text
2 3
2 5
3 7
```
期望输出：
```text
7
SAME
```
- 测试 2 输入：
```text
1 3
1 2
```
期望输出：
```text
2
LOOP_RISK
```

### V07-EX04 最短路双算法核验

- 归属卷：第 7 卷
- 覆盖模块：TRAIN-00、GRAPH-03、GRAPH-04
- 考场用途：训练用慢速 Bellman-Ford 核验 Dijkstra，抓旧堆状态、重边和不可达输出问题。

**题目描述：** 给定无向非负权图和起点 `s`。程序分别用 Dijkstra 和 Bellman-Ford 求最短路；若结果不一致，输出 `CHECK_FAILED`，否则输出从 `s` 到每个点的最短距离，不可达输出 `-1`。

**输入格式：** 第一行三个整数 `n m s`。接下来 `m` 行，每行 `u v w`。

**输出格式：** 输出一行 `n` 个整数，表示到 `1..n` 的距离。

**样例输入：**
```text
4 4 1
1 2 10
1 2 3
2 3 4
4 4 0
```

**样例输出：**
```text
0 3 7 -1
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const ll INF = 4'000'000'000'000'000'000LL;

struct Edge {
    int u;
    int v;
    ll w;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m, s;
    cin >> n >> m >> s;
    vector<vector<pair<int, ll>>> graph(n + 1);
    vector<Edge> edges;
    for (int i = 1; i <= m; i++) {
        int u, v;
        ll w;
        cin >> u >> v >> w;
        graph[u].push_back({v, w});
        graph[v].push_back({u, w});
        edges.push_back({u, v, w});
        edges.push_back({v, u, w});
    }

    vector<ll> dijkstra(n + 1, INF);
    priority_queue<pair<ll, int>, vector<pair<ll, int>>, greater<pair<ll, int>>> pq;
    dijkstra[s] = 0;
    pq.push({0, s});
    while (!pq.empty()) {
        auto [du, u] = pq.top();
        pq.pop();
        if (du != dijkstra[u]) continue;
        for (auto [v, w] : graph[u]) {
            if (dijkstra[v] > du + w) {
                dijkstra[v] = du + w;
                pq.push({dijkstra[v], v});
            }
        }
    }

    vector<ll> bellman(n + 1, INF);
    bellman[s] = 0;
    for (int round = 1; round <= n - 1; round++) {
        bool changed = false;
        for (const Edge &e : edges) {
            if (bellman[e.u] == INF) continue;
            if (bellman[e.v] > bellman[e.u] + e.w) {
                bellman[e.v] = bellman[e.u] + e.w;
                changed = true;
            }
        }
        if (!changed) break;
    }

    for (int i = 1; i <= n; i++) {
        if (dijkstra[i] != bellman[i]) {
            cout << "CHECK_FAILED\n";
            return 0;
        }
    }
    for (int i = 1; i <= n; i++) {
        if (i > 1) cout << ' ';
        cout << (dijkstra[i] == INF ? -1 : dijkstra[i]);
    }
    cout << '\n';
    return 0;
}
```

**测试设计：**

- 测试 1 输入：
```text
3 1 1
1 2 5
```
期望输出：
```text
0 5 -1
```
- 测试 2 输入：
```text
3 3 1
1 2 0
2 3 2
1 3 5
```
期望输出：
```text
0 0 2
```

### V07-EX05 KMP 与暴力重叠核验

- 归属卷：第 7 卷
- 覆盖模块：TRAIN-00、STR-02、CPP-011
- 考场用途：训练字符串算法用暴力版核验，重点覆盖重叠匹配。

**题目描述：** 给定文本串 `s` 和模式串 `p`。程序用 KMP 和暴力匹配分别统计出现次数；若不一致，输出 `CHECK_FAILED`，否则输出出现次数。

**输入格式：** 第一行字符串 `s`。第二行字符串 `p`。

**输出格式：** 输出核验后的出现次数，或 `CHECK_FAILED`。

**样例输入：**
```text
aaaaa
aa
```

**样例输出：**
```text
4
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string s_raw, p_raw;
    cin >> s_raw >> p_raw;
    string s = " " + s_raw;
    string p = " " + p_raw;
    int n = (int)s_raw.size();
    int m = (int)p_raw.size();

    vector<int> pi(m + 1, 0);
    for (int i = 2; i <= m; i++) {
        int j = pi[i - 1];
        while (j > 0 && p[i] != p[j + 1]) j = pi[j];
        if (p[i] == p[j + 1]) j++;
        pi[i] = j;
    }

    int kmp_count = 0;
    int j = 0;
    for (int i = 1; i <= n; i++) {
        while (j > 0 && s[i] != p[j + 1]) j = pi[j];
        if (s[i] == p[j + 1]) j++;
        if (j == m) {
            kmp_count++;
            j = pi[j];
        }
    }

    int brute_count = 0;
    for (int i = 1; i + m - 1 <= n; i++) {
        bool ok = true;
        for (int t = 1; t <= m; t++) {
            if (s[i + t - 1] != p[t]) ok = false;
        }
        if (ok) brute_count++;
    }

    if (kmp_count != brute_count) {
        cout << "CHECK_FAILED\n";
    } else {
        cout << kmp_count << '\n';
    }
    return 0;
}
```

**测试设计：**

- 测试 1 输入：
```text
abababa
aba
```
期望输出：
```text
3
```
- 测试 2 输入：
```text
abcde
f
```
期望输出：
```text
0
```

### V07-EX06 空栈保护括号匹配

- 归属卷：第 7 卷
- 覆盖模块：TRAIN-00、CPP-004、CPP-009
- 考场用途：训练访问 `top` 前先判空，避免空容器运行错误。

**题目描述：** 给定 `T` 个只含括号字符的字符串，判断每个字符串是否合法。括号包含 `()[]{} ` 三种，必须正确嵌套。

**输入格式：** 第一行一个整数 `T`。接下来 `T` 行，每行一个字符串。

**输出格式：** 每个字符串输出 `YES` 或 `NO`。

**样例输入：**
```text
3
([])
([)]
)(
```

**样例输出：**
```text
YES
NO
NO
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

bool match(char left, char right) {
    return (left == '(' && right == ')') ||
           (left == '[' && right == ']') ||
           (left == '{' && right == '}');
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;
    while (T--) {
        string s;
        cin >> s;
        stack<char> st;
        bool ok = true;
        for (char c : s) {
            if (c == '(' || c == '[' || c == '{') {
                st.push(c);
            } else {
                if (st.empty() || !match(st.top(), c)) {
                    ok = false;
                    break;
                }
                st.pop();
            }
        }
        if (!st.empty()) ok = false;
        cout << (ok ? "YES" : "NO") << '\n';
    }
    return 0;
}
```

**测试设计：**

- 测试 1 输入：
```text
2
()
(
```
期望输出：
```text
YES
NO
```
- 测试 2 输入：
```text
2
]
{[]}
```
期望输出：
```text
NO
YES
```

### V07-EX07 乘法溢出上限判断

- 归属卷：第 7 卷
- 覆盖模块：TRAIN-00、CPP-008、MATH-02
- 考场用途：训练大数乘法比较时使用 `__int128`，避免 `long long` 中间乘法溢出。

**题目描述：** 给定 `q` 个询问，每个询问包含非负整数 `a b limit`。判断 `a*b` 是否不超过 `limit`。

**输入格式：** 第一行一个整数 `q`。接下来 `q` 行，每行三个整数 `a b limit`。

**输出格式：** 每个询问输出 `YES` 或 `NO`。

**样例输入：**
```text
3
3 4 12
3 5 14
1000000000000 1000000000000 1000000000000000000
```

**样例输出：**
```text
YES
NO
NO
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int q;
    cin >> q;
    while (q--) {
        ll a, b, limit;
        cin >> a >> b >> limit;
        __int128 product = (__int128)a * b;
        cout << (product <= limit ? "YES" : "NO") << '\n';
    }
    return 0;
}
```

**测试设计：**

- 测试 1 输入：
```text
2
0 999999999999999999 0
1 999999999999999999 999999999999999999
```
期望输出：
```text
YES
YES
```
- 测试 2 输入：
```text
1
3037000500 3037000500 9223372036854775807
```
期望输出：
```text
NO
```

### V07-EX08 二分答案边界核验

- 归属卷：第 7 卷
- 覆盖模块：TRAIN-02、ROUTE-00、GREEDY-02
- 考场用途：训练二分答案的左右边界、`check` 单调性和 `k=1`、`k=n` 反例。

**题目描述：** 给定 `n` 个正整数任务量，按原顺序分成不超过 `k` 个连续段。最小化所有段和的最大值。

**输入格式：** 第一行两个整数 `n k`。第二行 `n` 个正整数。

**输出格式：** 输出最小可能的最大段和。

**样例输入：**
```text
5 2
7 2 5 10 8
```

**样例输出：**
```text
18
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

bool can_split(const vector<ll> &a, int n, int k, ll limit) {
    int groups = 1;
    ll current = 0;
    for (int i = 1; i <= n; i++) {
        if (a[i] > limit) return false;
        if (current + a[i] <= limit) {
            current += a[i];
        } else {
            groups++;
            current = a[i];
        }
    }
    return groups <= k;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, k;
    cin >> n >> k;
    vector<ll> a(n + 1);
    ll left = 0, right = 0;
    for (int i = 1; i <= n; i++) {
        cin >> a[i];
        left = max(left, a[i]);
        right += a[i];
    }
    while (left < right) {
        ll mid = left + (right - left) / 2;
        if (can_split(a, n, k, mid)) right = mid;
        else left = mid + 1;
    }
    cout << left << '\n';
    return 0;
}
```

**测试设计：**

- 测试 1 输入：
```text
3 1
1 2 3
```
期望输出：
```text
6
```
- 测试 2 输入：
```text
3 3
1 2 3
```
期望输出：
```text
3
```

### V07-EX09 RMQ 暴力对拍

- 归属卷：第 7 卷
- 覆盖模块：TRAIN-00、DS-03、TRAIN-01
- 考场用途：训练静态区间最小值用 Sparse Table，并用暴力循环核验边界。

**题目描述：** 给定数组和若干区间最小值询问。程序用 Sparse Table 和暴力分别计算；若不一致输出 `CHECK_FAILED`，否则输出每个询问的最小值。

**输入格式：** 第一行两个整数 `n q`。第二行 `n` 个整数。接下来 `q` 行，每行 `l r`。

**输出格式：** 每个询问输出一行最小值，或输出 `CHECK_FAILED`。

**样例输入：**
```text
5 3
4 2 7 1 3
1 5
2 3
4 4
```

**样例输出：**
```text
1
2
1
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, q;
    cin >> n >> q;
    vector<int> a(n + 1);
    for (int i = 1; i <= n; i++) cin >> a[i];

    vector<int> lg(n + 1, 0);
    for (int i = 2; i <= n; i++) lg[i] = lg[i / 2] + 1;
    int K = lg[n] + 1;
    vector<vector<int>> st(K, vector<int>(n + 1));
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
        int fast = min(st[k][l], st[k][r - (1 << k) + 1]);
        int slow = a[l];
        for (int i = l; i <= r; i++) slow = min(slow, a[i]);
        if (fast != slow) {
            cout << "CHECK_FAILED\n";
            return 0;
        }
        cout << fast << '\n';
    }
    return 0;
}
```

**测试设计：**

- 测试 1 输入：
```text
1 1
-5
1 1
```
期望输出：
```text
-5
```
- 测试 2 输入：
```text
4 2
8 8 8 8
1 4
2 2
```
期望输出：
```text
8
8
```

### V07-EX10 极端数组分类器

- 归属卷：第 7 卷
- 覆盖模块：TRAIN-01、CPP-009、ROUTE-00
- 考场用途：训练提交前主动构造 `n=1`、全相等、递增、递减、负数等反例形状。

**题目描述：** 给定一个数组，输出它命中的极端形状标签。标签固定按顺序输出：`SINGLE`、`ALL_EQUAL`、`STRICT_INC`、`STRICT_DEC`、`HAS_NEGATIVE`。若没有命中任何标签，输出 `NORMAL`。

**输入格式：** 第一行一个整数 `n`。第二行 `n` 个整数。

**输出格式：** 输出一行标签，多个标签用空格分隔。

**样例输入：**
```text
3
-1 -2 -3
```

**样例输出：**
```text
STRICT_DEC HAS_NEGATIVE
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<long long> a(n + 1);
    for (int i = 1; i <= n; i++) cin >> a[i];

    bool single = (n == 1);
    bool all_equal = true;
    bool strict_inc = true;
    bool strict_dec = true;
    bool has_negative = false;
    for (int i = 1; i <= n; i++) {
        if (a[i] < 0) has_negative = true;
        if (i >= 2) {
            if (a[i] != a[i - 1]) all_equal = false;
            if (a[i] <= a[i - 1]) strict_inc = false;
            if (a[i] >= a[i - 1]) strict_dec = false;
        }
    }

    vector<string> tags;
    if (single) tags.push_back("SINGLE");
    if (all_equal) tags.push_back("ALL_EQUAL");
    if (strict_inc) tags.push_back("STRICT_INC");
    if (strict_dec) tags.push_back("STRICT_DEC");
    if (has_negative) tags.push_back("HAS_NEGATIVE");
    if (tags.empty()) tags.push_back("NORMAL");

    for (int i = 0; i < (int)tags.size(); i++) {
        if (i) cout << ' ';
        cout << tags[i];
    }
    cout << '\n';
    return 0;
}
```

**测试设计：**

- 测试 1 输入：
```text
1
5
```
期望输出：
```text
SINGLE ALL_EQUAL STRICT_INC STRICT_DEC
```
- 测试 2 输入：
```text
4
2 2 3 1
```
期望输出：
```text
NORMAL
```

## 第 8 卷：洛谷覆盖索引主题例题

### V08-EX01 总分与平均分

- 归属卷：第 8 卷
- 覆盖模块：BASIC、CPP-001
- 考场用途：覆盖顺序结构、输入输出和固定小数格式。

**题目描述：** 输入 `n` 个学生成绩，输出总分和平均分，平均分保留两位小数。

**输入格式：** 第一行一个整数 `n`。第二行 `n` 个整数表示成绩。

**输出格式：** 输出一行，总分和平均分，中间用一个空格分隔。

**样例输入：**
```text
4
80 90 70 60
```

**样例输出：**
```text
300 75.00
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    int sum = 0;
    for (int i = 1; i <= n; i++) {
        int x;
        cin >> x;
        sum += x;
    }
    double average = 1.0 * sum / n;
    cout << sum << ' ' << fixed << setprecision(2) << average << '\n';
    return 0;
}
```

**测试设计：**

- 测试 1 输入：
```text
1
100
```
期望输出：
```text
100 100.00
```
- 测试 2 输入：
```text
3
1 2 2
```
期望输出：
```text
5 1.67
```

### V08-EX02 三角形分类

- 归属卷：第 8 卷
- 覆盖模块：BASIC、CPP-001
- 考场用途：覆盖分支结构、排序简化判断和边界等号。

**题目描述：** 给定三条边长，判断是否能组成三角形。不能组成输出 `INVALID`；能组成时，若为等边输出 `EQUILATERAL`，若为等腰输出 `ISOSCELES`，否则输出 `SCALENE`。

**输入格式：** 一行三个整数 `a b c`。

**输出格式：** 输出一个分类字符串。

**样例输入：**
```text
3 4 5
```

**样例输出：**
```text
SCALENE
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    vector<long long> a(4);
    cin >> a[1] >> a[2] >> a[3];
    sort(a.begin() + 1, a.end());
    if (a[1] + a[2] <= a[3]) {
        cout << "INVALID\n";
    } else if (a[1] == a[3]) {
        cout << "EQUILATERAL\n";
    } else if (a[1] == a[2] || a[2] == a[3]) {
        cout << "ISOSCELES\n";
    } else {
        cout << "SCALENE\n";
    }
    return 0;
}
```

**测试设计：**

- 测试 1 输入：
```text
1 2 3
```
期望输出：
```text
INVALID
```
- 测试 2 输入：
```text
5 5 8
```
期望输出：
```text
ISOSCELES
```

### V08-EX03 数位和循环

- 归属卷：第 8 卷
- 覆盖模块：BASIC、BRUTE-01
- 考场用途：覆盖循环结构、`0` 的特殊处理和整数拆位。

**题目描述：** 输入一个非负整数 `x`，输出它的十进制位数和各位数字之和。

**输入格式：** 一行一个非负整数 `x`。

**输出格式：** 输出两个整数：位数和数字和。

**样例输入：**
```text
12030
```

**样例输出：**
```text
5 6
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    ll x;
    cin >> x;
    if (x == 0) {
        cout << "1 0\n";
        return 0;
    }
    int digits = 0;
    int sum = 0;
    while (x > 0) {
        sum += (int)(x % 10);
        digits++;
        x /= 10;
    }
    cout << digits << ' ' << sum << '\n';
    return 0;
}
```

**测试设计：**

- 测试 1 输入：
```text
0
```
期望输出：
```text
1 0
```
- 测试 2 输入：
```text
999
```
期望输出：
```text
3 27
```

### V08-EX04 最长连续上升段

- 归属卷：第 8 卷
- 覆盖模块：CPP-002、DP-04
- 考场用途：覆盖数组扫描、初始化和 `n=1` 边界。

**题目描述：** 给定长度为 `n` 的整数数组，求最长连续严格上升子段的长度。

**输入格式：** 第一行一个整数 `n`。第二行 `n` 个整数。

**输出格式：** 输出一个整数表示最长长度。

**样例输入：**
```text
7
1 2 2 3 4 1 2
```

**样例输出：**
```text
3
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<int> a(n + 1);
    for (int i = 1; i <= n; i++) cin >> a[i];
    int best = 1;
    int current = 1;
    for (int i = 2; i <= n; i++) {
        if (a[i] > a[i - 1]) current++;
        else current = 1;
        best = max(best, current);
    }
    cout << best << '\n';
    return 0;
}
```

**测试设计：**

- 测试 1 输入：
```text
1
5
```
期望输出：
```text
1
```
- 测试 2 输入：
```text
5
5 4 3 2 1
```
期望输出：
```text
1
```

### V08-EX05 回文串判断

- 归属卷：第 8 卷
- 覆盖模块：CPP-011、STR-01
- 考场用途：覆盖字符串读入、双指针和 1-index 字符访问。

**题目描述：** 给定一个只含小写字母的字符串，判断它是否为回文串。

**输入格式：** 一行一个字符串。

**输出格式：** 是回文输出 `YES`，否则输出 `NO`。

**样例输入：**
```text
abccba
```

**样例输出：**
```text
YES
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string raw;
    cin >> raw;
    string s = " " + raw;
    int n = (int)raw.size();
    bool ok = true;
    for (int l = 1, r = n; l < r; l++, r--) {
        if (s[l] != s[r]) ok = false;
    }
    cout << (ok ? "YES" : "NO") << '\n';
    return 0;
}
```

**测试设计：**

- 测试 1 输入：
```text
a
```
期望输出：
```text
YES
```
- 测试 2 输入：
```text
abca
```
期望输出：
```text
NO
```

### V08-EX06 学生排序

- 归属卷：第 8 卷
- 覆盖模块：CPP-003、CPP-012
- 考场用途：覆盖排序、自定义比较器和相等元素的稳定规则。

**题目描述：** 给定 `n` 名学生的编号和分数。按分数从高到低排序；分数相同按编号从小到大排序。

**输入格式：** 第一行一个整数 `n`。接下来 `n` 行，每行两个整数 `id score`。

**输出格式：** 输出排序后的学生编号，每行一个。

**样例输入：**
```text
4
3 90
1 100
2 90
4 60
```

**样例输出：**
```text
1
2
3
4
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

struct Student {
    int id;
    int score;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<Student> a(n + 1);
    for (int i = 1; i <= n; i++) cin >> a[i].id >> a[i].score;
    sort(a.begin() + 1, a.end(), [](const Student &x, const Student &y) {
        if (x.score != y.score) return x.score > y.score;
        return x.id < y.id;
    });
    for (int i = 1; i <= n; i++) cout << a[i].id << '\n';
    return 0;
}
```

**测试设计：**

- 测试 1 输入：
```text
1
10 0
```
期望输出：
```text
10
```
- 测试 2 输入：
```text
3
2 80
1 80
3 80
```
期望输出：
```text
1
2
3
```

### V08-EX07 高精度加法

- 归属卷：第 8 卷
- 覆盖模块：SIM-01、CPP-011
- 考场用途：覆盖高精度基础、字符串逆序处理和进位边界。

**题目描述：** 给定两个非负整数 `a` 和 `b`，它们可能超过 `long long` 范围。输出 `a+b`。

**输入格式：** 两行，每行一个非负整数。

**输出格式：** 输出它们的和。

**样例输入：**
```text
999
1
```

**样例输出：**
```text
1000
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string a, b;
    cin >> a >> b;
    reverse(a.begin(), a.end());
    reverse(b.begin(), b.end());
    int n = max((int)a.size(), (int)b.size());
    string ans;
    int carry = 0;
    for (int i = 0; i < n; i++) {
        int x = (i < (int)a.size() ? a[i] - '0' : 0);
        int y = (i < (int)b.size() ? b[i] - '0' : 0);
        int sum = x + y + carry;
        ans.push_back(char('0' + sum % 10));
        carry = sum / 10;
    }
    if (carry) ans.push_back(char('0' + carry));
    while ((int)ans.size() > 1 && ans.back() == '0') ans.pop_back();
    reverse(ans.begin(), ans.end());
    cout << ans << '\n';
    return 0;
}
```

**测试设计：**

- 测试 1 输入：
```text
0
0
```
期望输出：
```text
0
```
- 测试 2 输入：
```text
123456789123456789
987654321987654321
```
期望输出：
```text
1111111111111111110
```

### V08-EX08 有序数组下界查询

- 归属卷：第 8 卷
- 覆盖模块：CPP-003、ROUTE-00
- 考场用途：覆盖二分查找、`lower_bound` 和未找到时的输出。

**题目描述：** 给定一个非降序数组，回答 `q` 次询问。每次给定 `x`，输出第一个大于等于 `x` 的元素位置；若不存在输出 `0`。

**输入格式：** 第一行两个整数 `n q`。第二行 `n` 个非降序整数。接下来 `q` 行每行一个整数 `x`。

**输出格式：** 每个询问输出一行位置。

**样例输入：**
```text
5 4
1 2 2 4 8
2
3
9
0
```

**样例输出：**
```text
2
4
0
1
```

**完整代码：**
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, q;
    cin >> n >> q;
    vector<int> a(n + 1);
    for (int i = 1; i <= n; i++) cin >> a[i];
    while (q--) {
        int x;
        cin >> x;
        int pos = int(lower_bound(a.begin() + 1, a.end(), x) - a.begin());
        if (pos == n + 1) cout << 0 << '\n';
        else cout << pos << '\n';
    }
    return 0;
}
```

**测试设计：**

- 测试 1 输入：
```text
1 2
5
5
6
```
期望输出：
```text
1
0
```
- 测试 2 输入：
```text
4 3
1 1 1 1
1
0
2
```
期望输出：
```text
1
1
0
```

### V08-EX09 合并果子

- 归属卷：第 8 卷
- 覆盖模块：CPP-004、GREEDY-02
- 考场用途：覆盖二叉堆、贪心和 `long long` 累加答案。

**题目描述：** 有 `n` 堆果子，每次可以合并两堆，代价为两堆果子数之和，合并后形成新的一堆。求把所有果子合成一堆的最小总代价。

**输入格式：** 第一行一个整数 `n`。第二行 `n` 个整数表示每堆果子数。

**输出格式：** 输出最小总代价。

**样例输入：**
```text
4
1 2 9 10
```

**样例输出：**
```text
37
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
    while ((int)pq.size() > 1) {
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

- 测试 1 输入：
```text
1
7
```
期望输出：
```text
0
```
- 测试 2 输入：
```text
3
5 5 5
```
期望输出：
```text
25
```

### V08-EX10 无权图最短路

- 归属卷：第 8 卷
- 覆盖模块：GRAPH-00、GRAPH-02
- 考场用途：覆盖图的基本应用、邻接表、BFS 和不可达判断。

**题目描述：** 给定无向无权图和起点 `s`、终点 `t`，求从 `s` 到 `t` 的最少边数。不可达输出 `-1`。

**输入格式：** 第一行四个整数 `n m s t`。接下来 `m` 行，每行一条无向边 `u v`。

**输出格式：** 输出最少边数。

**样例输入：**
```text
5 4 1 5
1 2
2 3
3 5
1 4
```

**样例输出：**
```text
3
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
    vector<vector<int>> graph(n + 1);
    for (int i = 1; i <= m; i++) {
        int u, v;
        cin >> u >> v;
        graph[u].push_back(v);
        graph[v].push_back(u);
    }

    vector<int> dist(n + 1, -1);
    queue<int> q;
    dist[s] = 0;
    q.push(s);
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        for (int v : graph[u]) {
            if (dist[v] == -1) {
                dist[v] = dist[u] + 1;
                q.push(v);
            }
        }
    }
    cout << dist[t] << '\n';
    return 0;
}
```

**测试设计：**

- 测试 1 输入：
```text
1 0 1 1
```
期望输出：
```text
0
```
- 测试 2 输入：
```text
3 1 1 3
1 2
```
期望输出：
```text
-1
```
