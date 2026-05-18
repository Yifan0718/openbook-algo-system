from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "04_generated_drafts" / "v02_examples_worker_G.md"


def ex(code: str, title: str, vol: str, modules: str, use: str, source: str,
       desc: str, inp: str, out: str, sample_in: str, sample_out: str,
       tests: str = "额外测试：构造最小规模、重复值、边界值各一组，和样例一起运行。") -> dict[str, str]:
    return {
        "code": code.strip() + "\n",
        "title": title,
        "vol": vol,
        "modules": modules,
        "use": use,
        "source": source,
        "desc": desc,
        "inp": inp,
        "out": out,
        "sample_in": sample_in.strip("\n"),
        "sample_out": sample_out.strip("\n"),
        "tests": tests,
    }


CPP_PREFIX = "#include <bits/stdc++.h>\nusing namespace std;\n\n"


examples: list[dict[str, str]] = []

# 第 0 卷：路由与作战组合题
examples += [
    ex(
        CPP_PREFIX + r'''
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    long long n, m;
    string feature;
    while (cin >> n >> m >> feature) {
        if (feature == "unweighted_graph") cout << "GRAPH-02 BFS\n";
        else if (feature == "weighted_nonnegative") cout << "GRAPH-03 Dijkstra\n";
        else if (feature == "range_sum_static") cout << "DS-01 PrefixSum\n";
        else if (feature == "range_update") cout << "DS-01 Difference\n";
        else if (n <= 20 && feature == "subset") cout << "BRUTE-02 Bitmask\n";
        else if (feature == "capacity") cout << "DP-06 Knapsack\n";
        else cout << "ROUTE-00 Read constraints again\n";
    }
    return 0;
}
''',
        "V00-CEX01 数据范围路由卡",
        "第 0 卷",
        "ROUTE-00、复杂度表、题型信号",
        "把题面关键词和数据范围直接映射到第一本该翻的书。",
        "参考来源：洛谷官方题单的基础/进阶分类、OI Wiki 算法分类。",
        "给出若干组 `n m feature`，输出建议优先翻的模块。",
        "多行，每行 `n m feature`，读到 EOF。",
        "每行输出一个模块建议。",
        "5 4 unweighted_graph\n200000 300000 weighted_nonnegative\n18 0 subset\n100 1000 capacity\n",
        "GRAPH-02 BFS\nGRAPH-03 Dijkstra\nBRUTE-02 Bitmask\nDP-06 Knapsack",
    ),
    ex(
        CPP_PREFIX + r'''
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    cin >> n >> q;
    vector<long long> diff(n + 3, 0);
    for (int i = 1; i <= q; i++) {
        int l, r;
        long long v;
        cin >> l >> r >> v;
        diff[l] += v;
        diff[r + 1] -= v;
    }
    long long cur = 0, mx = LLONG_MIN;
    int pos = 1;
    for (int i = 1; i <= n; i++) {
        cur += diff[i];
        if (cur > mx) {
            mx = cur;
            pos = i;
        }
    }
    cout << pos << ' ' << mx << '\n';
    return 0;
}
''',
        "V00-CEX02 先交差分部分分",
        "第 0 卷",
        "DS-01 差分、提交策略",
        "看到大量区间加，先写差分拿稳分。",
        "参考来源：洛谷入门数组/前缀差分题型。",
        "长度为 `n` 的数组初始全 0，执行区间加，输出最终最大值第一次出现的位置和值。",
        "第一行 `n q`，之后 `q` 行 `l r v`。",
        "输出 `pos maxValue`。",
        "5 3\n1 3 2\n2 5 1\n4 4 10\n",
        "4 11",
    ),
    ex(
        CPP_PREFIX + r'''
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m, s, t;
    cin >> n >> m >> s >> t;
    vector<vector<pair<int,int>>> g(n + 1);
    bool all_one = true;
    for (int i = 1; i <= m; i++) {
        int u, v, w;
        cin >> u >> v >> w;
        g[u].push_back({v, w});
        g[v].push_back({u, w});
        if (w != 1) all_one = false;
    }
    const long long INF = (long long)4e18;
    vector<long long> dist(n + 1, INF);
    if (all_one) {
        queue<int> q;
        dist[s] = 0;
        q.push(s);
        while (!q.empty()) {
            int u = q.front(); q.pop();
            for (auto [v, w] : g[u]) {
                if (dist[v] == INF) {
                    dist[v] = dist[u] + 1;
                    q.push(v);
                }
            }
        }
    } else {
        priority_queue<pair<long long,int>, vector<pair<long long,int>>, greater<pair<long long,int>>> pq;
        dist[s] = 0;
        pq.push({0, s});
        while (!pq.empty()) {
            auto [d, u] = pq.top(); pq.pop();
            if (d != dist[u]) continue;
            for (auto [v, w] : g[u]) {
                if (dist[v] > d + w) {
                    dist[v] = d + w;
                    pq.push({dist[v], v});
                }
            }
        }
    }
    cout << (dist[t] == INF ? -1 : dist[t]) << '\n';
    return 0;
}
''',
        "V00-CEX03 BFS 与 Dijkstra 路由合并",
        "第 0 卷",
        "GRAPH-02 BFS、GRAPH-03 Dijkstra",
        "同一份题面先判断边权是否全 1，再决定翻哪本图论页。",
        "参考来源：洛谷图论题单最短路分类、OI Wiki 最短路。",
        "给无向图，如果所有边权都是 1 用 BFS，否则用 Dijkstra，求 `s` 到 `t` 最短距离。",
        "第一行 `n m s t`，之后 `m` 行 `u v w`。",
        "输出最短距离，不可达输出 `-1`。",
        "4 4 1 4\n1 2 1\n2 4 1\n1 3 5\n3 4 1\n",
        "2",
    ),
    ex(
        CPP_PREFIX + r'''
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    long long target;
    cin >> n >> target;
    vector<long long> a(n + 1);
    for (int i = 1; i <= n; i++) cin >> a[i];
    long long ans = 0;
    if (n <= 25) {
        for (int mask = 0; mask < (1 << n); mask++) {
            long long sum = 0;
            for (int i = 1; i <= n; i++) if (mask & (1 << (i - 1))) sum += a[i];
            if (sum == target) ans++;
        }
    } else {
        unordered_map<long long, long long> cnt;
        cnt.reserve(n * 2 + 10);
        for (int i = 1; i <= n; i++) {
            ans += cnt[target - a[i]];
            cnt[a[i]]++;
        }
    }
    cout << ans << '\n';
    return 0;
}
''',
        "V00-CEX04 小数据暴力与大数据特判",
        "第 0 卷",
        "BRUTE 子集、哈希表、部分分策略",
        "同一题先写小数据精确，再给大数据特殊版。",
        "参考来源：洛谷搜索/哈希题型、部分分赛制策略。",
        "若 `n<=25`，统计子集和等于目标的方案数；否则只统计两数和等于目标的对数，模拟部分分兜底。",
        "第一行 `n target`，第二行 `n` 个整数。",
        "输出统计结果。",
        "4 5\n1 2 3 4\n",
        "2",
    ),
    ex(
        CPP_PREFIX + r'''
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int p, s;
    cin >> p >> s;
    vector<int> best(p + 1, -1);
    for (int i = 1; i <= s; i++) {
        int id, score;
        cin >> id >> score;
        best[id] = max(best[id], score);
    }
    int total = 0;
    for (int i = 1; i <= p; i++) total += max(0, best[i]);
    cout << total << '\n';
    return 0;
}
''',
        "V00-CEX05 最高分提交统计",
        "第 0 卷",
        "考试策略、最高分提交规则、数组",
        "把每题多次提交取最高的规则变成程序，强化先交部分分。",
        "参考来源：本次机考规则。",
        "有 `p` 道题、`s` 次提交记录，每条记录是题号和得分，输出最终总分。",
        "第一行 `p s`，之后 `s` 行 `id score`。",
        "输出最终总分。",
        "3 6\n1 20\n2 30\n1 50\n3 10\n2 25\n3 80\n",
        "160",
    ),
]

# 第 1 卷：C++ / STL / IO
examples += [
    ex(
        CPP_PREFIX + r'''
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    cin.ignore(numeric_limits<streamsize>::max(), '\n');
    map<string, long long> sum;
    for (int i = 1; i <= n; i++) {
        string line;
        getline(cin, line);
        stringstream ss(line);
        string key;
        long long value;
        while (ss >> key >> value) sum[key] += value;
    }
    for (auto [k, v] : sum) cout << k << ' ' << v << '\n';
    return 0;
}
''',
        "V01-CEX01 多行键值记录合并",
        "第 1 卷",
        "getline、stringstream、map",
        "处理含空格记录并按字典序输出。",
        "参考来源：洛谷入门字符串/模拟题型。",
        "每行由若干 `名字 数值` 对组成，合并所有名字的数值。",
        "第一行 `n`，接下来 `n` 行记录。",
        "按名字字典序输出合计。",
        "3\nalice 3 bob 2\nalice 4\ncarl 5 bob 1\n",
        "alice 7\nbob 3\ncarl 5",
    ),
    ex(
        CPP_PREFIX + r'''
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    cout << fixed << setprecision(2);
    for (int i = 1; i <= n; i++) {
        string name;
        double a, b;
        cin >> name >> a >> b;
        cout << setw(10) << left << name << right << setw(8) << a + b << '\n';
    }
    return 0;
}
''',
        "V01-CEX02 固定宽度成绩表",
        "第 1 卷",
        "iomanip、fixed、setprecision、setw",
        "复杂格式输出时直接套。",
        "参考来源：洛谷入门格式化输出题型。",
        "输入若干学生两项成绩，左对齐姓名、右对齐总分并保留两位小数。",
        "第一行 `n`，之后 `name a b`。",
        "每行输出宽度固定的姓名和总分。",
        "2\nLi 90 5.5\nWang 80.25 10\n",
        "Li           95.50\nWang         90.25",
    ),
    ex(
        CPP_PREFIX + r'''
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, k;
    cin >> n >> k;
    unordered_map<string, int> cnt;
    cnt.reserve(n * 2 + 10);
    for (int i = 1; i <= n; i++) {
        string s;
        cin >> s;
        cnt[s]++;
    }
    priority_queue<pair<int,string>> pq;
    for (auto [s, c] : cnt) pq.push({c, s});
    for (int i = 1; i <= k && !pq.empty(); i++) {
        auto [c, s] = pq.top(); pq.pop();
        cout << s << ' ' << c << '\n';
    }
    return 0;
}
''',
        "V01-CEX03 哈希表加堆 TopK",
        "第 1 卷",
        "unordered_map、priority_queue",
        "词频统计后取最高频。",
        "参考来源：洛谷/ICPC 常见词频 TopK 模拟。",
        "统计字符串出现次数，输出出现次数最高的前 `k` 个；次数相同按字典序大的先出。",
        "第一行 `n k`，之后 `n` 个字符串。",
        "输出前 `k` 项。",
        "7 2\na b a c b a c\n",
        "a 3\nc 2",
    ),
    ex(
        CPP_PREFIX + r'''
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<pair<int,int>> seg(n + 1);
    for (int i = 1; i <= n; i++) cin >> seg[i].first >> seg[i].second;
    sort(seg.begin() + 1, seg.end());
    vector<pair<int,int>> ans;
    for (int i = 1; i <= n; i++) {
        if (ans.empty() || seg[i].first > ans.back().second) ans.push_back(seg[i]);
        else ans.back().second = max(ans.back().second, seg[i].second);
    }
    cout << ans.size() << '\n';
    for (auto [l, r] : ans) cout << l << ' ' << r << '\n';
    return 0;
}
''',
        "V01-CEX04 pair 排序合并区间",
        "第 1 卷",
        "vector<pair>、sort",
        "用 STL 排序把模拟题变成标准区间合并。",
        "参考来源：洛谷区间合并/模拟题型。",
        "给出若干闭区间，合并相交区间并输出。",
        "第一行 `n`，之后 `n` 行 `l r`。",
        "输出合并后区间个数和区间。",
        "4\n1 3\n2 5\n8 9\n5 7\n",
        "2\n1 7\n8 9",
    ),
    ex(
        CPP_PREFIX + r'''
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    cin >> n >> q;
    vector<int> a(n + 1);
    for (int i = 1; i <= n; i++) cin >> a[i];
    sort(a.begin() + 1, a.end());
    while (q--) {
        int x;
        cin >> x;
        auto it = lower_bound(a.begin() + 1, a.end(), x);
        if (it == a.end()) cout << "NONE\n";
        else cout << *it << '\n';
    }
    return 0;
}
''',
        "V01-CEX05 排序后二分答询问",
        "第 1 卷",
        "sort、lower_bound、vector 1-index",
        "二分函数的标准调用。",
        "参考来源：洛谷二分查找题型。",
        "每次询问输出数组中第一个不小于 `x` 的数。",
        "第一行 `n q`，第二行数组，之后 `q` 行询问。",
        "每行输出答案，不存在输出 `NONE`。",
        "5 4\n7 1 5 3 9\n4\n9\n10\n1\n",
        "5\n9\nNONE\n1",
    ),
]

# 第 2 卷
examples += [
    ex(
        CPP_PREFIX + r'''
int n;
vector<int> a;
long long best = (long long)4e18;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cin >> n;
    a.assign(n + 1, 0);
    for (int i = 1; i <= n; i++) cin >> a[i];
    vector<int> p(n);
    iota(p.begin(), p.end(), 1);
    do {
        long long cost = 0;
        for (int i = 1; i < n; i++) cost += abs(a[p[i]] - a[p[i - 1]]);
        best = min(best, cost);
    } while (next_permutation(p.begin(), p.end()));
    cout << best << '\n';
    return 0;
}
''',
        "V02-CEX01 全排列最小相邻差",
        "第 2 卷",
        "next_permutation、暴力",
        "n 小时直接枚举顺序拿满小数据。",
        "参考来源：洛谷搜索/排列枚举题型。",
        "重排数组，使相邻差绝对值之和最小。",
        "第一行 `n`，第二行 `n` 个数，保证 `n<=8`。",
        "输出最小代价。",
        "4\n10 1 4 7\n",
        "9",
    ),
    ex(
        CPP_PREFIX + r'''
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<int> need(m + 1), cover(n + 1);
    for (int i = 1; i <= m; i++) cin >> need[i];
    for (int i = 1; i <= n; i++) cin >> cover[i];
    int ans = n + 1;
    for (int mask = 0; mask < (1 << n); mask++) {
        int have = 0, cnt = 0;
        for (int i = 1; i <= n; i++) if (mask & (1 << (i - 1))) {
            have |= cover[i];
            cnt++;
        }
        bool ok = true;
        for (int i = 1; i <= m; i++) if ((have & need[i]) != need[i]) ok = false;
        if (ok) ans = min(ans, cnt);
    }
    cout << (ans == n + 1 ? -1 : ans) << '\n';
    return 0;
}
''',
        "V02-CEX02 子集覆盖最小选择",
        "第 2 卷",
        "子集枚举、位运算",
        "把小集合覆盖问题压成 bitmask。",
        "参考来源：洛谷状态压缩/集合覆盖题型。",
        "有 `n` 个工具，每个工具覆盖若干能力位；给出 `m` 个需求掩码，求最少选几个工具满足所有需求。",
        "第一行 `n m`，第二行 `m` 个需求掩码，第三行 `n` 个工具掩码。",
        "输出最少工具数。",
        "4 2\n3 12\n1 2 4 8\n",
        "4",
    ),
    ex(
        CPP_PREFIX + r'''
int n, target;
vector<int> a;
map<pair<int,int>, long long> memo;
long long dfs(int i, int sum) {
    if (i == n + 1) return sum == target;
    auto key = make_pair(i, sum);
    if (memo.count(key)) return memo[key];
    long long ans = dfs(i + 1, sum + a[i]) + dfs(i + 1, sum - a[i]);
    return memo[key] = ans;
}
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cin >> n >> target;
    a.assign(n + 1, 0);
    for (int i = 1; i <= n; i++) cin >> a[i];
    cout << dfs(1, 0) << '\n';
    return 0;
}
''',
        "V02-CEX03 加减号记忆化搜索",
        "第 2 卷",
        "DFS、记忆化、map 状态",
        "暴力每个数加/减，直接加 memo 升级。",
        "参考来源：经典 Target Sum 搜索题型。",
        "给每个数前放 `+` 或 `-`，统计表达式值等于目标的方案数。",
        "第一行 `n target`，第二行数组。",
        "输出方案数。",
        "5 3\n1 1 1 1 1\n",
        "5",
    ),
    ex(
        CPP_PREFIX + r'''
struct State { int x, y, k; };
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<string> g(n + 1);
    for (int i = 1; i <= n; i++) { cin >> g[i]; g[i] = " " + g[i]; }
    vector<vector<array<int,2>>> dist(n + 1, vector<array<int,2>>(m + 1, { -1, -1 }));
    queue<State> q;
    dist[1][1][0] = 0;
    q.push({1, 1, 0});
    int dx[4] = {1, -1, 0, 0};
    int dy[4] = {0, 0, 1, -1};
    while (!q.empty()) {
        auto cur = q.front(); q.pop();
        for (int d = 0; d < 4; d++) {
            int nx = cur.x + dx[d], ny = cur.y + dy[d];
            if (nx < 1 || nx > n || ny < 1 || ny > m) continue;
            int nk = cur.k;
            if (g[nx][ny] == '#') {
                if (nk) continue;
                nk = 1;
            }
            if (dist[nx][ny][nk] == -1) {
                dist[nx][ny][nk] = dist[cur.x][cur.y][cur.k] + 1;
                q.push({nx, ny, nk});
            }
        }
    }
    int a = dist[n][m][0], b = dist[n][m][1];
    if (a == -1) cout << b << '\n';
    else if (b == -1) cout << a << '\n';
    else cout << min(a, b) << '\n';
    return 0;
}
''',
        "V02-CEX04 网格破墙一次 BFS",
        "第 2 卷",
        "BFS 状态搜索、状态升维",
        "把“是否用过一次破墙”作为状态。",
        "参考来源：洛谷/ICPC 网格 BFS 变体。",
        "从左上走到右下，可经过至多一个障碍，求最少步数。",
        "第一行 `n m`，之后网格，`.` 可走，`#` 障碍。",
        "输出最少步数，不可达输出 `-1`。",
        "3 3\n.#.\n##.\n...\n",
        "4",
    ),
    ex(
        CPP_PREFIX + r'''
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    long long S;
    cin >> n >> S;
    int n1 = n / 2, n2 = n - n1;
    vector<long long> a(n + 1), left, right;
    for (int i = 1; i <= n; i++) cin >> a[i];
    for (int mask = 0; mask < (1 << n1); mask++) {
        long long s = 0;
        for (int i = 0; i < n1; i++) if (mask & (1 << i)) s += a[i + 1];
        left.push_back(s);
    }
    for (int mask = 0; mask < (1 << n2); mask++) {
        long long s = 0;
        for (int i = 0; i < n2; i++) if (mask & (1 << i)) s += a[n1 + i + 1];
        right.push_back(s);
    }
    sort(right.begin(), right.end());
    long long ans = 0;
    for (long long x : left) ans += upper_bound(right.begin(), right.end(), S - x) - right.begin();
    cout << ans << '\n';
    return 0;
}
''',
        "V02-CEX05 折半统计子集和不超过 S",
        "第 2 卷",
        "meet-in-the-middle、二分",
        "n 约 40 时替代 2^n 暴力。",
        "参考来源：洛谷折半搜索题型。",
        "统计子集和不超过 `S` 的方案数。",
        "第一行 `n S`，第二行数组，`n<=40`。",
        "输出方案数。",
        "4 5\n1 2 3 4\n",
        "9",
    ),
]

# 第 3 卷：DP
examples += [
    ex(
        CPP_PREFIX + r'''
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, k;
    cin >> n >> k;
    vector<long long> a(n + 1), pre(n + 1);
    for (int i = 1; i <= n; i++) { cin >> a[i]; pre[i] = pre[i - 1] + a[i]; }
    const long long INF = (long long)4e18;
    vector<vector<long long>> dp(k + 1, vector<long long>(n + 1, INF));
    dp[0][0] = 0;
    for (int p = 1; p <= k; p++) {
        for (int i = 1; i <= n; i++) {
            for (int j = 0; j < i; j++) {
                long long seg = pre[i] - pre[j];
                dp[p][i] = min(dp[p][i], max(dp[p - 1][j], seg));
            }
        }
    }
    cout << dp[k][n] << '\n';
    return 0;
}
''',
        "V03-CEX01 分成 k 段最小化最大段和",
        "第 3 卷",
        "线性 DP、前缀和、最后一段",
        "练习用最后一段位置推转移。",
        "参考来源：洛谷 DP 分段模型、OI Wiki DP 基础。",
        "把数组切成 `k` 个连续非空段，使最大段和最小。",
        "第一行 `n k`，第二行数组。",
        "输出最小可能最大段和。",
        "5 2\n7 2 5 10 8\n",
        "18",
    ),
    ex(
        CPP_PREFIX + r'''
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, W;
    cin >> n >> W;
    vector<int> weight(n + 1), value(n + 1), cnt(n + 1);
    for (int i = 1; i <= n; i++) cin >> weight[i] >> value[i] >> cnt[i];
    vector<long long> dp(W + 1, 0);
    for (int i = 1; i <= n; i++) {
        int c = cnt[i];
        for (int b = 1; c > 0; b <<= 1) {
            int take = min(b, c);
            c -= take;
            int w = weight[i] * take, v = value[i] * take;
            for (int j = W; j >= w; j--) dp[j] = max(dp[j], dp[j - w] + v);
        }
    }
    cout << *max_element(dp.begin(), dp.end()) << '\n';
    return 0;
}
''',
        "V03-CEX02 多重背包二进制拆分",
        "第 3 卷",
        "多重背包、0/1 背包复用",
        "把有限件物品拆成若干 0/1 物品。",
        "参考来源：洛谷背包问题题单。",
        "每种物品有重量、价值和数量，容量为 `W`，求最大价值。",
        "第一行 `n W`，之后 `w v c`。",
        "输出最大价值。",
        "2 10\n3 4 3\n4 5 2\n",
        "13",
    ),
    ex(
        CPP_PREFIX + r'''
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string s;
    cin >> s;
    int n = (int)s.size();
    s = " " + s;
    vector<vector<int>> dp(n + 2, vector<int>(n + 2, 0));
    for (int len = 1; len <= n; len++) {
        for (int l = 1; l + len - 1 <= n; l++) {
            int r = l + len - 1;
            dp[l][r] = 1 + dp[l + 1][r];
            for (int k = l + 1; k <= r; k++) {
                if (s[k] == s[l]) dp[l][r] = min(dp[l][r], dp[l + 1][k - 1] + dp[k][r]);
            }
        }
    }
    cout << dp[1][n] << '\n';
    return 0;
}
''',
        "V03-CEX03 相同字符一起删除",
        "第 3 卷",
        "区间 DP、删除模型",
        "练习区间删除不是只枚举切点。",
        "参考来源：经典区间 DP 删除题型。",
        "每次可删除一段相同字符，删除后两侧合并，求删完整串最少次数。",
        "输入一个小写字符串。",
        "输出最少次数。",
        "aba\n",
        "2",
    ),
    ex(
        CPP_PREFIX + r'''
int n, W;
vector<vector<pair<int,int>>> child;
vector<int> w, v;
vector<vector<long long>> dp;
void dfs(int u) {
    dp[u].assign(W + 1, -4e18);
    dp[u][w[u]] = v[u];
    for (auto [to, dummy] : child[u]) {
        dfs(to);
        vector<long long> ndp = dp[u];
        for (int i = 0; i <= W; i++) if (dp[u][i] > -3e18) {
            for (int j = 0; i + j <= W; j++) if (dp[to][j] > -3e18) {
                ndp[i + j] = max(ndp[i + j], dp[u][i] + dp[to][j]);
            }
        }
        dp[u] = ndp;
    }
}
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cin >> n >> W;
    child.assign(n + 1, {});
    w.assign(n + 1, 0); v.assign(n + 1, 0);
    int root = 1;
    for (int i = 1; i <= n; i++) {
        int p;
        cin >> p >> w[i] >> v[i];
        if (p == 0) root = i;
        else child[p].push_back({i, 0});
    }
    dp.resize(n + 1);
    dfs(root);
    cout << *max_element(dp[root].begin(), dp[root].end()) << '\n';
    return 0;
}
''',
        "V03-CEX04 依赖树背包",
        "第 3 卷",
        "树形 DP、背包合并",
        "选子节点必须选父节点的依赖型模型。",
        "参考来源：洛谷树形背包/依赖背包题型。",
        "每个物品有父依赖、重量和价值，选子必须选父，容量 `W`，求最大价值。",
        "第一行 `n W`，之后每行 `parent weight value`，`parent=0` 是根。",
        "输出最大价值。",
        "4 5\n0 2 3\n1 2 4\n1 3 5\n2 1 2\n",
        "9",
    ),
    ex(
        CPP_PREFIX + r'''
long long memo[20][2][2][200];
vector<int> digits;
long long dfs(int pos, int tight, int started, int sum) {
    if (pos == (int)digits.size()) return started && sum % 3 == 0;
    long long &res = memo[pos][tight][started][sum];
    if (!tight && res != -1) return res;
    long long ans = 0;
    int lim = tight ? digits[pos] : 9;
    for (int d = 0; d <= lim; d++) {
        ans += dfs(pos + 1, tight && d == lim, started || d != 0, sum + (started || d != 0 ? d : 0));
    }
    if (!tight) res = ans;
    return ans;
}
long long solve(long long x) {
    if (x <= 0) return 0;
    digits.clear();
    string s = to_string(x);
    for (char c : s) digits.push_back(c - '0');
    memset(memo, -1, sizeof(memo));
    return dfs(0, 1, 0, 0);
}
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    long long L, R;
    cin >> L >> R;
    cout << solve(R) - solve(L - 1) << '\n';
    return 0;
}
''',
        "V03-CEX05 数位 DP 统计数字和被 3 整除",
        "第 3 卷",
        "数位 DP、tight、started",
        "把范围计数转成 `solve(R)-solve(L-1)`。",
        "参考来源：OI Wiki 数位 DP、洛谷数位 DP 题型。",
        "统计 `[L,R]` 中正整数的数位和能被 3 整除的个数。",
        "输入 `L R`。",
        "输出个数。",
        "1 20\n",
        "6",
    ),
]

# 第 3A 卷：贪心与 DP 辨析
examples += [
    ex(CPP_PREFIX + r'''
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<pair<int,int>> a(n + 1);
    for (int i = 1; i <= n; i++) cin >> a[i].second >> a[i].first;
    sort(a.begin() + 1, a.end());
    int cnt = 0, last = -2000000000;
    for (int i = 1; i <= n; i++) if (a[i].second >= last) {
        cnt++;
        last = a[i].first;
    }
    cout << cnt << '\n';
    return 0;
}
''', "V03A-CEX01 活动选择结束时间贪心", "第 3A 卷", "区间贪心、交换论证", "最经典可贪心模型。", "参考来源：洛谷区间贪心题型。", "给出若干活动起止时间，求最多选多少个互不重叠活动。", "第一行 n，之后 n 行 l r。", "输出最多数量。", "4\n1 3\n2 4\n3 5\n6 7\n", "3"),
    ex(CPP_PREFIX + r'''
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<pair<int,int>> a(n + 1);
    for (int i = 1; i <= n; i++) cin >> a[i].first >> a[i].second;
    sort(a.begin() + 1, a.end());
    priority_queue<int, vector<int>, greater<int>> pq;
    for (int i = 1; i <= n; i++) {
        if (!pq.empty() && pq.top() <= a[i].first) pq.pop();
        pq.push(a[i].second);
    }
    cout << pq.size() << '\n';
    return 0;
}
''', "V03A-CEX02 会议室最少数量", "第 3A 卷", "排序、堆贪心", "同时占用区间数量用小根堆。", "参考来源：经典会议室/区间调度题型。", "给出会议时间，求最少会议室数量。", "第一行 n，之后 n 行 l r。", "输出最少数量。", "3\n0 30\n5 10\n15 20\n", "2"),
    ex(CPP_PREFIX + r'''
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<pair<int,int>> a(n + 1);
    for (int i = 1; i <= n; i++) cin >> a[i].first >> a[i].second;
    sort(a.begin() + 1, a.end(), [](auto x, auto y) {
        return x.second < y.second;
    });
    int points = 0, last = -2000000000;
    for (int i = 1; i <= n; i++) {
        if (last < a[i].first) {
            last = a[i].second;
            points++;
        }
    }
    cout << points << '\n';
    return 0;
}
''', "V03A-CEX03 最少点刺破区间", "第 3A 卷", "区间按右端排序", "证明每次选最早结束点。", "参考来源：洛谷区间选点题型。", "选择尽量少的点，使每个闭区间至少包含一个点。", "第一行 n，之后 n 行 l r。", "输出最少点数。", "3\n1 3\n2 5\n6 8\n", "2"),
    ex(CPP_PREFIX + r'''
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, W;
    cin >> n >> W;
    vector<int> w(n + 1), v(n + 1);
    for (int i = 1; i <= n; i++) cin >> w[i] >> v[i];
    vector<int> dp(W + 1, 0);
    for (int i = 1; i <= n; i++) {
        for (int j = W; j >= w[i]; j--) dp[j] = max(dp[j], dp[j - w[i]] + v[i]);
    }
    cout << dp[W] << '\n';
    return 0;
}
''', "V03A-CEX04 单价贪心失败的 0/1 背包", "第 3A 卷", "反例、0/1 背包", "看到选/不选和容量，别按性价比硬贪。", "参考来源：洛谷背包题单。", "给 0/1 背包，输出最大价值。", "第一行 n W，之后 w v。", "输出最大价值。", "3 50\n10 60\n20 100\n30 120\n", "220"),
    ex(CPP_PREFIX + r'''
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, T;
    cin >> n >> T;
    vector<pair<int,int>> jobs(n + 1);
    for (int i = 1; i <= n; i++) cin >> jobs[i].first >> jobs[i].second;
    sort(jobs.begin() + 1, jobs.end());
    priority_queue<int, vector<int>, greater<int>> pq;
    long long sum = 0;
    for (int i = 1; i <= n; i++) {
        pq.push(jobs[i].second);
        sum += jobs[i].second;
        if ((int)pq.size() > jobs[i].first) {
            sum -= pq.top();
            pq.pop();
        }
    }
    cout << sum << '\n';
    return 0;
}
''', "V03A-CEX05 截止日任务反悔贪心", "第 3A 卷", "排序、堆、反悔贪心", "先收下，超过容量就反悔删最小收益。", "参考来源：经典课程安排/反悔贪心题型。", "每个任务有截止日和收益，每天最多做一个，求最大收益。", "第一行 n T，之后 deadline profit。", "输出最大收益。", "4 4\n1 10\n2 20\n2 15\n3 5\n", "40"),
]

# 第 4 卷：数据结构
examples += [
    ex(CPP_PREFIX + r'''
struct BIT {
    int n; vector<long long> t;
    BIT(int n=0): n(n), t(n+1,0) {}
    void add(int x,long long v){ for(;x<=n;x+=x&-x)t[x]+=v; }
    long long sum(int x){ long long r=0; for(;x>0;x-=x&-x)r+=t[x]; return r; }
};
int main(){
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n; cin>>n; vector<int>a(n+1),xs;
    for(int i=1;i<=n;i++){cin>>a[i]; xs.push_back(a[i]);}
    sort(xs.begin(),xs.end()); xs.erase(unique(xs.begin(),xs.end()),xs.end());
    BIT bit(xs.size()); long long inv=0;
    for(int i=n;i>=1;i--){ int id=lower_bound(xs.begin(),xs.end(),a[i])-xs.begin()+1; inv+=bit.sum(id-1); bit.add(id,1); }
    cout<<inv<<"\n"; return 0;
}
''', "V04-CEX01 坐标压缩加树状数组逆序对", "第 4 卷", "坐标压缩、树状数组", "值域很大但个数不大时直接压缩。", "参考来源：洛谷逆序对模板题型。", "求数组逆序对数量。", "第一行 n，第二行数组。", "输出逆序对数。", "5\n5 4 2 6 3\n", "6"),
    ex(CPP_PREFIX + r'''
const int MAXN=200005;
long long tree[MAXN*4], lazyv[MAXN*4];
void push(int p,int l,int r){ if(!lazyv[p])return; int m=(l+r)/2; long long v=lazyv[p]; tree[p*2]+=v*(m-l+1); tree[p*2+1]+=v*(r-m); lazyv[p*2]+=v; lazyv[p*2+1]+=v; lazyv[p]=0; }
void add(int p,int l,int r,int ql,int qr,long long v){ if(ql<=l&&r<=qr){tree[p]+=v*(r-l+1); lazyv[p]+=v; return;} push(p,l,r); int m=(l+r)/2; if(ql<=m)add(p*2,l,m,ql,qr,v); if(qr>m)add(p*2+1,m+1,r,ql,qr,v); tree[p]=tree[p*2]+tree[p*2+1]; }
long long query(int p,int l,int r,int ql,int qr){ if(ql<=l&&r<=qr)return tree[p]; push(p,l,r); int m=(l+r)/2; long long ans=0; if(ql<=m)ans+=query(p*2,l,m,ql,qr); if(qr>m)ans+=query(p*2+1,m+1,r,ql,qr); return ans; }
int main(){ ios::sync_with_stdio(false); cin.tie(nullptr); int n,q; cin>>n>>q; while(q--){int op,l,r; long long v; cin>>op>>l>>r; if(op==1){cin>>v; add(1,1,n,l,r,v);} else cout<<query(1,1,n,l,r)<<"\n";} return 0; }
''', "V04-CEX02 线段树区间加区间和", "第 4 卷", "线段树、lazy", "动态区间修改查询。", "参考来源：洛谷线段树模板题型。", "支持区间加和区间和查询。", "第一行 n q，操作 `1 l r v` 或 `2 l r`。", "查询输出区间和。", "5 4\n1 1 3 2\n2 2 5\n1 4 5 1\n2 1 5\n", "4\n8"),
    ex(CPP_PREFIX + r'''
int main(){ ios::sync_with_stdio(false); cin.tie(nullptr); int n,k; long long C; cin>>n>>k>>C; vector<long long>a(n+1),dp(n+1); for(int i=1;i<=n;i++)cin>>a[i]; deque<int> dq; dq.push_back(0); for(int i=1;i<=n;i++){ while(!dq.empty()&&dq.front()<i-k)dq.pop_front(); dp[i]=dp[dq.front()]+a[i]-C; while(!dq.empty()&&dp[dq.back()]<=dp[i])dq.pop_back(); dq.push_back(i);} cout<<*max_element(dp.begin()+1,dp.end())<<"\n"; return 0; }
''', "V04-CEX03 单调队列优化 DP", "第 4 卷", "单调队列、DP优化", "转移只看最近 k 个最大 dp。", "参考来源：洛谷单调队列优化题型。", "定义 `dp[i]=max(dp[j])+a[i]-C`，其中 `i-k<=j<i`，求最大 dp。", "第一行 n k C，第二行数组。", "输出最大值。", "5 2 1\n3 2 5 1 4\n", "10"),
    ex(CPP_PREFIX + r'''
struct DSU{ vector<int> fa,sz; DSU(int n=0){fa.resize(n+1);sz.assign(n+1,1);iota(fa.begin(),fa.end(),0);} int find(int x){while(x!=fa[x]){fa[x]=fa[fa[x]];x=fa[x];}return x;} bool unite(int a,int b){a=find(a);b=find(b);if(a==b)return false;if(sz[a]<sz[b])swap(a,b);fa[b]=a;sz[a]+=sz[b];return true;} };
int main(){ ios::sync_with_stdio(false); cin.tie(nullptr); int n,m; cin>>n>>m; vector<pair<int,int>> e(m+1); for(int i=1;i<=m;i++)cin>>e[i].first>>e[i].second; int q; cin>>q; vector<int> del(q+1),ban(m+1); for(int i=1;i<=q;i++){cin>>del[i];ban[del[i]]=1;} DSU d(n); int comp=n; for(int i=1;i<=m;i++)if(!ban[i]&&d.unite(e[i].first,e[i].second))comp--; vector<int> ans(q+1); for(int i=q;i>=1;i--){ans[i]=comp; if(d.unite(e[del[i]].first,e[del[i]].second))comp--;} for(int i=1;i<=q;i++)cout<<ans[i]<<"\n"; return 0; }
''', "V04-CEX04 离线删边转加边", "第 4 卷", "DSU、逆序离线", "删边不好做，就倒过来加边。", "参考来源：洛谷并查集离线题型。", "给一张图和删边序列，输出每次删除后连通块个数。", "第一行 n m，之后 m 条边；再 q 和 q 个边编号。", "每次删除后输出连通块数。", "4 3\n1 2\n2 3\n3 4\n2\n2\n1\n", "2\n3"),
    ex(CPP_PREFIX + r'''
int main(){ ios::sync_with_stdio(false); cin.tie(nullptr); int n,q; cin>>n>>q; vector<int>a(n+1),lg(n+1); for(int i=1;i<=n;i++)cin>>a[i]; for(int i=2;i<=n;i++)lg[i]=lg[i/2]+1; int K=lg[n]+1; vector<vector<int>> st(K,vector<int>(n+1)); st[0]=a; for(int k=1;k<K;k++)for(int i=1;i+(1<<k)-1<=n;i++)st[k][i]=min(st[k-1][i],st[k-1][i+(1<<(k-1))]); while(q--){int l,r;cin>>l>>r;int k=lg[r-l+1];cout<<min(st[k][l],st[k][r-(1<<k)+1])<<"\n";} return 0; }
''', "V04-CEX05 Sparse Table 静态 RMQ", "第 4 卷", "Sparse Table、静态区间最小值", "没有修改时比线段树简单。", "参考来源：洛谷 ST 表模板题型。", "静态数组多次查询区间最小值。", "第一行 n q，第二行数组，之后 q 个 l r。", "每次输出最小值。", "5 3\n4 2 7 1 5\n1 3\n2 5\n4 4\n", "2\n1\n1"),
]

# 第 5 卷：图树
examples += [
    ex(CPP_PREFIX + r'''
int main(){ ios::sync_with_stdio(false); cin.tie(nullptr); int n,m,s,t;cin>>n>>m>>s>>t; vector<vector<pair<int,int>>> g(n+1); for(int i=1;i<=m;i++){int u,v,w;cin>>u>>v>>w;g[u].push_back({v,w});g[v].push_back({u,w});} const long long INF=4e18; vector<long long>d(n+1,INF),cnt(n+1); priority_queue<pair<long long,int>,vector<pair<long long,int>>,greater<pair<long long,int>>>pq; d[s]=0;cnt[s]=1;pq.push({0,s}); while(!pq.empty()){auto [du,u]=pq.top();pq.pop(); if(du!=d[u])continue; for(auto [v,w]:g[u]){ if(d[v]>du+w){d[v]=du+w;cnt[v]=cnt[u];pq.push({d[v],v});} else if(d[v]==du+w)cnt[v]+=cnt[u]; }} cout<<(d[t]==INF?-1:d[t])<<" "<<(d[t]==INF?0:cnt[t])<<"\n"; return 0; }
''', "V05-CEX01 Dijkstra 同时统计最短路条数", "第 5 卷", "Dijkstra、路径计数", "图题经常不只要距离。", "参考来源：洛谷最短路题单。", "求 `s` 到 `t` 最短距离和最短路条数。", "第一行 n m s t，之后无向边 u v w。", "输出距离和条数。", "4 4 1 4\n1 2 1\n2 4 1\n1 3 1\n3 4 1\n", "2 2"),
    ex(CPP_PREFIX + r'''
int main(){ ios::sync_with_stdio(false); cin.tie(nullptr); int n,m;cin>>n>>m; vector<vector<pair<int,int>>>g(n+1); for(int i=1;i<=m;i++){int u,v,w;cin>>u>>v>>w;g[u].push_back({v,w});g[v].push_back({u,w});} deque<int>dq; vector<int>d(n+1,1e9); d[1]=0;dq.push_back(1); while(!dq.empty()){int u=dq.front();dq.pop_front(); for(auto [v,w]:g[u]) if(d[v]>d[u]+w){d[v]=d[u]+w; if(w==0)dq.push_front(v);else dq.push_back(v);} } cout<<(d[n]==(int)1e9?-1:d[n])<<"\n"; return 0; }
''', "V05-CEX02 0-1 BFS", "第 5 卷", "deque、边权 0/1 最短路", "边权只有 0/1 时替代 Dijkstra。", "参考来源：OI Wiki 0-1 BFS。", "无向图边权 0 或 1，求 1 到 n 最短路。", "第一行 n m，之后 u v w。", "输出距离。", "4 4\n1 2 0\n2 4 1\n1 3 1\n3 4 0\n", "1"),
    ex(CPP_PREFIX + r'''
struct DSU{vector<int>f;DSU(int n){f.resize(n+1);iota(f.begin(),f.end(),0);}int find(int x){return x==f[x]?x:f[x]=find(f[x]);}bool unite(int a,int b){a=find(a);b=find(b);if(a==b)return false;f[b]=a;return true;}};
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);int n,m;cin>>n>>m; struct E{int u,v,w;}; vector<E>e(m); for(auto &x:e)cin>>x.u>>x.v>>x.w; sort(e.begin(),e.end(),[](E a,E b){return a.w<b.w;}); DSU d(n); long long ans=0;int cnt=0,last=0; for(auto x:e)if(d.unite(x.u,x.v)){ans+=x.w;cnt++;last=x.w;} if(cnt<n-1)cout<<"orz\n"; else cout<<ans<<" "<<last<<"\n"; return 0;}
''', "V05-CEX03 Kruskal 输出总权和最大边", "第 5 卷", "MST、DSU", "MST 后常要附加统计。", "参考来源：洛谷最小生成树题单。", "求最小生成树权值和及树中最大边权。", "第一行 n m，之后 u v w。", "不连通输出 orz。", "4 5\n1 2 1\n2 3 2\n3 4 3\n1 4 10\n2 4 4\n", "6 3"),
    ex(CPP_PREFIX + r'''
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);int n,m;cin>>n>>m; vector<vector<int>>g(n+1); vector<int>ind(n+1); for(int i=1;i<=m;i++){int u,v;cin>>u>>v;g[u].push_back(v);ind[v]++;} queue<int>q; vector<int>sem(n+1,1); for(int i=1;i<=n;i++)if(!ind[i])q.push(i); int seen=0,ans=1; while(!q.empty()){int u=q.front();q.pop();seen++;ans=max(ans,sem[u]); for(int v:g[u]){sem[v]=max(sem[v],sem[u]+1); if(--ind[v]==0)q.push(v);}} if(seen<n)cout<<"CYCLE\n"; else cout<<ans<<"\n"; return 0;}
''', "V05-CEX04 拓扑排序最少学期", "第 5 卷", "拓扑排序、DAG DP", "依赖题常把拓扑和 DP 拼起来。", "参考来源：洛谷拓扑排序题单。", "课程依赖 `u->v` 表示先学 u，求最少学期数；有环输出 CYCLE。", "第一行 n m，之后 u v。", "输出学期数或 CYCLE。", "4 3\n1 2\n1 3\n3 4\n", "3"),
    ex(CPP_PREFIX + r'''
const int LOG=20;
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);int n,q;cin>>n>>q; vector<vector<pair<int,int>>>g(n+1); for(int i=1;i<n;i++){int u,v,w;cin>>u>>v>>w;g[u].push_back({v,w});g[v].push_back({u,w});} vector<array<int,LOG>>up(n+1),mn(n+1); vector<int>dep(n+1); function<void(int,int)>dfs=[&](int u,int p){up[u][0]=p; for(int k=1;k<LOG;k++){up[u][k]=up[up[u][k-1]][k-1];mn[u][k]=min(mn[u][k-1],mn[up[u][k-1]][k-1]);} for(auto [v,w]:g[u])if(v!=p){dep[v]=dep[u]+1;mn[v][0]=w;dfs(v,u);}}; for(int k=0;k<LOG;k++)mn[1][k]=1e9; dfs(1,1); while(q--){int a,b;cin>>a>>b;int ans=1e9;if(dep[a]<dep[b])swap(a,b);int diff=dep[a]-dep[b];for(int k=0;k<LOG;k++)if(diff>>k&1){ans=min(ans,mn[a][k]);a=up[a][k];} if(a!=b){for(int k=LOG-1;k>=0;k--)if(up[a][k]!=up[b][k]){ans=min(ans,mn[a][k]);ans=min(ans,mn[b][k]);a=up[a][k];b=up[b][k];} ans=min(ans,mn[a][0]);ans=min(ans,mn[b][0]);} cout<<ans<<"\n";} return 0;}
''', "V05-CEX05 LCA 查询路径最小边", "第 5 卷", "LCA、倍增、树上路径", "LCA 常和路径聚合值一起考。", "参考来源：洛谷 LCA/树上路径题型。", "给树，查询两点路径上的最小边权。", "第一行 n q，之后 n-1 边，之后 q 个查询。", "每次输出最小边权。", "4 2\n1 2 5\n2 3 4\n2 4 7\n3 4\n1 3\n", "4\n4"),
]

# 第 6 卷：数学与字符串
examples += [
    ex(CPP_PREFIX + r'''
long long modpow(long long a,long long b,long long mod){long long r=1%mod;for(a%=mod;b;b>>=1,a=a*a%mod)if(b&1)r=r*a%mod;return r;}
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);int n,q;long long mod;cin>>n>>q>>mod; vector<long long>fac(n+1),inv(n+1);fac[0]=1%mod;for(int i=1;i<=n;i++)fac[i]=fac[i-1]*i%mod;inv[n]=modpow(fac[n],mod-2,mod);for(int i=n;i>=1;i--)inv[i-1]=inv[i]*i%mod;while(q--){int a,b;cin>>a>>b;if(b<0||b>a)cout<<0<<"\n";else cout<<fac[a]*inv[b]%mod*inv[a-b]%mod<<"\n";}return 0;}
''', "V06-CEX01 组合数查询", "第 6 卷", "快速幂、逆元、组合数", "模数是质数时的 C(n,k)。", "参考来源：洛谷组合数学题型。", "预处理阶乘，回答组合数。", "第一行 n q mod，之后 q 行 a b。", "输出 C(a,b) mod。", "5 3 1000000007\n5 2\n4 0\n3 5\n", "10\n1\n0"),
    ex(CPP_PREFIX + r'''
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);int n;cin>>n; vector<int>is(n+1,1),pr; if(n>=0)is[0]=0;if(n>=1)is[1]=0; for(int i=2;i<=n;i++){if(is[i])pr.push_back(i); for(int p:pr){if(1LL*i*p>n)break;is[i*p]=0;if(i%p==0)break;}} cout<<pr.size()<<"\n"; for(int p:pr) if(n-p>=2&&is[n-p]){cout<<p<<" "<<n-p<<"\n"; return 0;} cout<<"NONE\n";return 0;}
''', "V06-CEX02 筛法加哥德巴赫拆分", "第 6 卷", "欧拉筛、质数判定", "筛完再做构造/查询。", "参考来源：洛谷素数筛/数论基础题型。", "输出不超过 n 的质数个数，并找一组质数和为 n。", "输入偶数 n。", "输出质数个数和一组拆分。", "20\n", "8\n3 17"),
    ex(CPP_PREFIX + r'''
vector<int> prefix_function(const string&s){int n=s.size();vector<int>pi(n);for(int i=1;i<n;i++){int j=pi[i-1];while(j&&s[i]!=s[j])j=pi[j-1];if(s[i]==s[j])j++;pi[i]=j;}return pi;}
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);string p,t;cin>>p>>t;string s=p+"#"+t;auto pi=prefix_function(s);int ans=0;for(int x:pi)if(x==(int)p.size())ans++;cout<<ans<<"\n";return 0;}
''', "V06-CEX03 KMP 统计出现次数", "第 6 卷", "KMP、前缀函数", "匹配题直接套。", "参考来源：洛谷 KMP 模板题型。", "统计模式串在文本中出现次数，允许重叠。", "第一行模式串，第二行文本。", "输出次数。", "aba\nababaaba\n", "3"),
    ex(CPP_PREFIX + r'''
struct Node{int nxt[26];int cnt;Node(){memset(nxt,0,sizeof(nxt));cnt=0;}};
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);int n,q;cin>>n>>q;vector<Node>tr(1); for(int i=1;i<=n;i++){string s;cin>>s;int u=0;for(char c:s){int x=c-'a';if(!tr[u].nxt[x]){tr[u].nxt[x]=tr.size();tr.push_back(Node());}u=tr[u].nxt[x];tr[u].cnt++;}} while(q--){string s;cin>>s;int u=0,ok=1;for(char c:s){int x=c-'a';if(!tr[u].nxt[x]){ok=0;break;}u=tr[u].nxt[x];}cout<<(ok?tr[u].cnt:0)<<"\n";}return 0;}
''', "V06-CEX04 Trie 前缀数量查询", "第 6 卷", "Trie、字符串前缀", "前缀类题目比 map 枚举稳。", "参考来源：洛谷 Trie 模板题型。", "插入单词，查询每个前缀是多少单词的前缀。", "第一行 n q，之后 n 个单词和 q 个前缀。", "输出数量。", "4 3\napple app apt bat\nap\napp\nb\n", "3\n2\n1"),
    ex(CPP_PREFIX + r'''
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);string s;cin>>s;string t="@";for(char c:s){t+="#";t+=c;}t+="#$";int n=t.size();vector<int>p(n);int c=0,r=0,ans=0;for(int i=1;i<n-1;i++){int mir=2*c-i;if(i<r)p[i]=min(r-i,p[mir]);while(t[i+1+p[i]]==t[i-1-p[i]])p[i]++;if(i+p[i]>r){c=i;r=i+p[i];}ans=max(ans,p[i]);}cout<<ans<<"\n";return 0;}
''', "V06-CEX05 Manacher 最长回文子串", "第 6 卷", "Manacher、回文", "回文长度题的线性模板。", "参考来源：洛谷回文字符串题型。", "输出字符串最长回文子串长度。", "输入字符串。", "输出长度。", "babad\n", "3"),
]

# 第 6A 卷
examples += [
    ex(CPP_PREFIX + r'''
long long exgcd(long long a,long long b,long long&x,long long&y){if(!b){x=1;y=0;return a;}long long x1,y1,g=exgcd(b,a%b,x1,y1);x=y1;y=x1-a/b*y1;return g;}
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);long long a,b,c;cin>>a>>b>>c;long long x,y,g=exgcd(abs(a),abs(b),x,y);if(c%g){cout<<"NO\n";return 0;}x*=c/g;y*=c/g;if(a<0)x=-x;if(b<0)y=-y;cout<<x<<" "<<y<<"\n";return 0;}
''', "V06A-CEX01 线性丢番图方程", "第 6A 卷", "exgcd、整数方程", "同余和方程都从 exgcd 来。", "参考来源：OI Wiki exgcd、洛谷扩欧题型。", "求 `ax+by=c` 的一组整数解。", "输入 a b c。", "输出 x y 或 NO。", "6 9 3\n", "-1 1"),
    ex(CPP_PREFIX + r'''
struct Mat{long long a[2][2];};
Mat mul(Mat x,Mat y,long long mod){Mat z{{{0,0},{0,0}}};for(int i=0;i<2;i++)for(int k=0;k<2;k++)for(int j=0;j<2;j++)z.a[i][j]=(z.a[i][j]+x.a[i][k]*y.a[k][j])%mod;return z;}
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);long long n,mod;cin>>n>>mod;if(n==0){cout<<0<<"\n";return 0;}Mat r{{{1,0},{0,1}}},b{{{1,1},{1,0}}};long long e=n-1;while(e){if(e&1)r=mul(r,b,mod);b=mul(b,b,mod);e>>=1;}cout<<r.a[0][0]%mod<<"\n";return 0;}
''', "V06A-CEX02 矩阵快速幂 Fibonacci", "第 6A 卷", "矩阵快速幂、线性递推", "递推项 n 很大时用矩阵。", "参考来源：OI Wiki 矩阵快速幂。", "求第 n 个 Fibonacci 数 mod m，F1=1,F2=1。", "输入 n mod。", "输出答案。", "10 1000\n", "55"),
    ex(CPP_PREFIX + r'''
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);long long n;int k;cin>>n>>k;vector<long long>a(k+1);for(int i=1;i<=k;i++)cin>>a[i];long long ans=0;for(int mask=1;mask<(1<<k);mask++){__int128 l=1;int bits=0;for(int i=1;i<=k;i++)if(mask>>(i-1)&1){bits++;l=l/std::gcd((long long)l,a[i])*a[i];if(l>n)break;}if(l>n)continue;long long cnt=n/(long long)l;if(bits&1)ans+=cnt;else ans-=cnt;}cout<<ans<<"\n";return 0;}
''', "V06A-CEX03 容斥统计倍数", "第 6A 卷", "容斥、lcm、防溢出", "多条件“至少一个满足”常用容斥。", "参考来源：组合数学容斥题型。", "统计 `1..n` 中能被给定任一数整除的个数。", "第一行 n k，第二行 k 个数。", "输出个数。", "20 2\n2 3\n", "13"),
    ex(CPP_PREFIX + r'''
bool leap(int y){return y%400==0||(y%4==0&&y%100!=0);}
int mdays(int y,int m){int d[]={0,31,28,31,30,31,30,31,31,30,31,30,31};return m==2?d[m]+leap(y):d[m];}
long long days(int y,int m,int d){long long ans=0;for(int yy=1;yy<y;yy++)ans+=365+leap(yy);for(int mm=1;mm<m;mm++)ans+=mdays(y,mm);return ans+d;}
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);int y1,m1,d1,y2,m2,d2;cin>>y1>>m1>>d1>>y2>>m2>>d2;cout<<llabs(days(y2,m2,d2)-days(y1,m1,d1))<<"\n";return 0;}
''', "V06A-CEX04 日期差天数", "第 6A 卷", "日期、闰年、模拟", "日历题先统一转绝对天数。", "参考来源：洛谷日期模拟题型。", "给两个公历日期，求相差天数。", "输入两个日期 `y m d`。", "输出天数差绝对值。", "2024 2 28\n2024 3 1\n", "2"),
    ex(CPP_PREFIX + r'''
struct P{double x,y;};
double cross(P a,P b,P c){return (b.x-a.x)*(c.y-a.y)-(b.y-a.y)*(c.x-a.x);}
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);int n;cin>>n;vector<P>p(n+1);for(int i=1;i<=n;i++)cin>>p[i].x>>p[i].y;double area=0;for(int i=1;i<=n;i++){int j=i==n?1:i+1;area+=p[i].x*p[j].y-p[i].y*p[j].x;}cout<<fixed<<setprecision(1)<<fabs(area)/2<<"\n";return 0;}
''', "V06A-CEX05 多边形面积", "第 6A 卷", "计算几何、叉积", "几何题先准备基本叉积。", "参考来源：OI Wiki 计算几何基础。", "按顺序给多边形顶点，输出面积。", "第一行 n，之后 n 个点。", "输出一位小数面积。", "4\n0 0\n2 0\n2 2\n0 2\n", "4.0"),
]

# 第 7 卷：调试对拍
examples += [
    ex(CPP_PREFIX + r'''
long long slow(vector<int>a){long long ans=0;for(int i=0;i<(int)a.size();i++)for(int j=i+1;j<(int)a.size();j++)if(a[i]>a[j])ans++;return ans;}
long long fast(vector<int>a){int n=a.size();vector<int>xs=a;sort(xs.begin(),xs.end());xs.erase(unique(xs.begin(),xs.end()),xs.end());vector<int>bit(xs.size()+2);auto add=[&](int x){for(;x<(int)bit.size();x+=x&-x)bit[x]++;};auto sum=[&](int x){int r=0;for(;x>0;x-=x&-x)r+=bit[x];return r;};long long ans=0;for(int i=n-1;i>=0;i--){int id=lower_bound(xs.begin(),xs.end(),a[i])-xs.begin()+1;ans+=sum(id-1);add(id);}return ans;}
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);int n;cin>>n;vector<int>a(n);for(int&i:a)cin>>i;cout<<(slow(a)==fast(a)?"OK":"BAD")<<" "<<fast(a)<<"\n";return 0;}
''', "V07-CEX01 快慢算法核验逆序对", "第 7 卷", "对拍、暴力核验", "写完高级算法先用慢算法对照小数据。", "参考来源：竞赛对拍常规做法。", "同时用 O(n^2) 和树状数组算逆序对，输出是否一致。", "第一行 n，第二行数组。", "输出 OK/BAD 和答案。", "5\n3 1 2 5 4\n", "OK 3"),
    ex(CPP_PREFIX + r'''
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);int n;cin>>n;vector<long long>a(n+1);for(int i=1;i<=n;i++)cin>>a[i];bool ok=true;for(int i=1;i<=n;i++){if(a[i]<-1000000000LL||a[i]>1000000000LL)ok=false;}cout<<(ok?"INPUT_OK":"INPUT_OUT_OF_RANGE")<<"\n";return 0;}
''', "V07-CEX02 输入范围守卫", "第 7 卷", "边界检查、调试", "本地调试时先检查数据是否满足题面。", "参考来源：调试训练经验。", "检查数组元素是否都在 [-1e9,1e9]。", "第一行 n，第二行数组。", "输出检查结果。", "3\n1 -2 1000000001\n", "INPUT_OUT_OF_RANGE"),
    ex(CPP_PREFIX + r'''
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);long long l=1,r=100,ans=-1,target;cin>>target;while(l<=r){long long mid=(l+r)/2;if(mid*mid>=target){ans=mid;r=mid-1;}else l=mid+1;}cout<<ans<<"\n";return 0;}
''', "V07-CEX03 二分边界可视化", "第 7 卷", "二分答案、边界", "用最小满足模型避免死循环。", "参考来源：二分答案常见错误清单。", "求最小 x，使 x^2 >= target，范围 1..100。", "输入 target。", "输出 x。", "50\n", "8"),
    ex(CPP_PREFIX + r'''
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);long long a,b,limit;cin>>a>>b>>limit;__int128 prod=(__int128)a*b;cout<<(prod>limit?"OVER":"OK")<<"\n";return 0;}
''', "V07-CEX04 乘法溢出探针", "第 7 卷", "__int128、防溢出", "判断乘积时不要先溢出。", "参考来源：数值边界调试经验。", "判断 a*b 是否超过 limit。", "输入 a b limit。", "输出 OK 或 OVER。", "1000000000000 1000000000000 1000000000000000000\n", "OVER"),
    ex(CPP_PREFIX + r'''
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);string s;cin>>s;vector<char>st;for(char c:s){if(c=='('||c=='[')st.push_back(c);else{if(st.empty()){cout<<"NO\n";return 0;}char t=st.back();st.pop_back();if((c==')'&&t!='(')||(c==']'&&t!='[')){cout<<"NO\n";return 0;}}}cout<<(st.empty()?"YES":"NO")<<"\n";return 0;}
''', "V07-CEX05 空容器访问保护", "第 7 卷", "stack、RE 防御", "top/pop 前先判空。", "参考来源：括号匹配调试题型。", "判断只含括号的字符串是否合法。", "输入字符串。", "输出 YES/NO。", "([]())\n", "YES"),
]

# 第 8 卷
examples += [
    ex(CPP_PREFIX + r'''int main(){ios::sync_with_stdio(false);cin.tie(nullptr);long long a,b;cin>>a>>b;cout<<a+b<<"\n";return 0;}''', "V08-CEX01 A+B 快速热身", "第 8 卷", "顺序结构、输入输出", "最基础热身，检查环境。", "参考来源：洛谷 P1001 类入门题。", "输入两个整数，输出和。", "一行两个整数。", "输出和。", "123 456\n", "579"),
    ex(CPP_PREFIX + r'''int main(){ios::sync_with_stdio(false);cin.tie(nullptr);int n;cin>>n;for(int i=1;i<=n;i++){for(int j=1;j<=n;j++)cout<<setw(3)<<(i-1)*n+j;cout<<"\n";}return 0;}''', "V08-CEX02 方阵顺序输出", "第 8 卷", "循环、格式", "基础循环与宽度输出。", "参考来源：洛谷循环结构题型。", "输出 n*n 方阵。", "输入 n。", "每行 n 个宽度 3 的数。", "3\n", "  1  2  3\n  4  5  6\n  7  8  9"),
    ex(CPP_PREFIX + r'''int main(){ios::sync_with_stdio(false);cin.tie(nullptr);int n;cin>>n;vector<int>a(n+1);for(int i=1;i<=n;i++)cin>>a[i];sort(a.begin()+1,a.end());for(int i=1;i<=n;i++){if(i>1)cout<<" ";cout<<a[i];}cout<<"\n";return 0;}''', "V08-CEX03 数组排序", "第 8 卷", "数组、排序", "基础数组题常直接 sort。", "参考来源：洛谷数组排序题型。", "输入数组，升序输出。", "第一行 n，第二行数组。", "输出排序结果。", "5\n5 1 4 2 3\n", "1 2 3 4 5"),
    ex(CPP_PREFIX + r'''int main(){ios::sync_with_stdio(false);cin.tie(nullptr);string s;cin>>s;string t=s;reverse(t.begin(),t.end());cout<<(s==t?"YES":"NO")<<"\n";return 0;}''', "V08-CEX04 回文串", "第 8 卷", "字符串、reverse", "字符串基础判断。", "参考来源：洛谷字符串入门题型。", "判断字符串是否回文。", "输入字符串。", "输出 YES/NO。", "level\n", "YES"),
    ex(CPP_PREFIX + r'''string add(string a,string b){reverse(a.begin(),a.end());reverse(b.begin(),b.end());int n=max(a.size(),b.size()),c=0;string s;for(int i=0;i<n||c;i++){int x=c;if(i<(int)a.size())x+=a[i]-'0';if(i<(int)b.size())x+=b[i]-'0';s.push_back('0'+x%10);c=x/10;}reverse(s.begin(),s.end());return s;}int main(){ios::sync_with_stdio(false);cin.tie(nullptr);string a,b;cin>>a>>b;cout<<add(a,b)<<"\n";return 0;}''', "V08-CEX05 高精度加法", "第 8 卷", "高精度、字符串", "基础高精度模板。", "参考来源：洛谷高精度入门题型。", "输入两个非负大整数，输出和。", "两行或一行两个数。", "输出和。", "999999999999999999\n1\n", "1000000000000000000"),
]

# 第 9 卷：Python
examples += [
    ex(r'''
import sys
from math import comb
n, k = map(int, sys.stdin.readline().split())
print(comb(n, k))
''', "V09-CEX01 Python 大组合数", "第 9 卷", "math.comb、大整数", "C++ 要写高精度时 Python 明显省事。", "参考来源：Python 标准库文档、组合数学题型。", "输出 C(n,k) 的精确值。", "输入 n k。", "输出组合数。", "50 6\n", "15890700"),
    ex(r'''
import sys, heapq
n = int(sys.stdin.readline())
small = []
large = []
ans = []
for x in map(int, sys.stdin.readline().split()):
    heapq.heappush(small, -x)
    heapq.heappush(large, -heapq.heappop(small))
    if len(large) > len(small):
        heapq.heappush(small, -heapq.heappop(large))
    ans.append(str(-small[0]))
print(" ".join(ans))
''', "V09-CEX02 Python 双堆中位数", "第 9 卷", "heapq、在线维护", "heapq 写起来短，适合模拟。", "参考来源：经典在线中位数题型。", "依次插入数，输出每次插入后的较小中位数。", "第一行 n，第二行 n 个数。", "输出 n 个中位数。", "5\n5 2 7 1 3\n", "5 2 5 2 3"),
    ex(r'''
import sys
from collections import deque
n, m = map(int, sys.stdin.readline().split())
g = [[] for _ in range(n + 1)]
for _ in range(m):
    u, v = map(int, sys.stdin.readline().split())
    g[u].append(v)
    g[v].append(u)
dist = [-1] * (n + 1)
q = deque([1])
dist[1] = 0
while q:
    u = q.popleft()
    for v in g[u]:
        if dist[v] == -1:
            dist[v] = dist[u] + 1
            q.append(v)
print(dist[n])
''', "V09-CEX03 Python deque BFS", "第 9 卷", "deque、图 BFS", "小中规模无权图可用 Python 快速写。", "参考来源：洛谷 BFS 基础题型。", "无向无权图求 1 到 n 最短路。", "第一行 n m，之后边。", "输出距离。", "4 3\n1 2\n2 3\n3 4\n", "3"),
    ex(r'''
import sys
from itertools import combinations
n, k, target = map(int, sys.stdin.readline().split())
a = list(map(int, sys.stdin.readline().split()))
cnt = 0
for combi in combinations(a, k):
    if sum(combi) == target:
        cnt += 1
print(cnt)
''', "V09-CEX04 itertools 组合枚举", "第 9 卷", "itertools.combinations", "小规模组合题 Python 写法非常短。", "参考来源：搜索枚举题型。", "从 n 个数选 k 个，统计和为 target 的方案数。", "第一行 n k target，第二行数组。", "输出方案数。", "5 2 5\n1 2 3 4 5\n", "2"),
    ex(r'''
import sys
from fractions import Fraction
a, b, c, d = map(int, sys.stdin.readline().split())
x = Fraction(a, b) + Fraction(c, d)
print(f"{x.numerator}/{x.denominator}")
''', "V09-CEX05 Fraction 精确分数", "第 9 卷", "fractions.Fraction", "需要精确有理数时 Python 标准库很省事。", "参考来源：Python 标准库 fractions。", "计算 a/b + c/d 的最简分数。", "输入 a b c d。", "输出 numerator/denominator。", "1 6 1 3\n", "1/2"),
]

# 第 10 卷：AI
examples += [
    ex(CPP_PREFIX + r'''
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);int n;cin>>n; vector<double>x(n+1),y(n+1); for(int i=1;i<=n;i++)cin>>x[i]>>y[i]; double dot=0,nx=0,ny=0; for(int i=1;i<=n;i++){dot+=x[i]*y[i];nx+=x[i]*x[i];ny+=y[i]*y[i];} cout<<fixed<<setprecision(6)<<dot/(sqrt(nx)*sqrt(ny))<<"\n";return 0;}
''', "V10-CEX01 余弦相似度", "第 10 卷", "向量、相似度", "文本/推荐题常见基础组件。", "参考来源：TF-IDF/向量检索基础。", "给两个向量，输出余弦相似度。", "第一行 n，之后 n 行 xi yi。", "输出 6 位小数。", "3\n1 1\n2 0\n0 2\n", "0.200000"),
    ex(CPP_PREFIX + r'''
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);int n,m;cin>>n>>m; vector<vector<double>>x(n+1,vector<double>(m+1)); vector<int>y(n+1); for(int i=1;i<=n;i++){for(int j=1;j<=m;j++)cin>>x[i][j];cin>>y[i];} vector<double>q(m+1);for(int j=1;j<=m;j++)cin>>q[j]; int best=-1,lab=-1;double bd=1e100; for(int i=1;i<=n;i++){double d=0;for(int j=1;j<=m;j++)d+=(x[i][j]-q[j])*(x[i][j]-q[j]); if(d<bd){bd=d;lab=y[i];best=i;}} cout<<lab<<"\n";return 0;}
''', "V10-CEX02 最近邻分类", "第 10 卷", "KNN、欧氏距离", "AI 题里最容易模拟的分类器。", "参考来源：监督学习 KNN 基础。", "给训练样本和查询点，输出最近样本标签。", "第一行 n m，之后特征和标签，最后查询点。", "输出标签。", "3 2\n0 0 1\n5 5 2\n1 0 1\n0 1\n", "1"),
    ex(CPP_PREFIX + r'''
double sigmoid(double z){return 1.0/(1.0+exp(-z));}
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);int n;double lr;cin>>n>>lr;double w=0,b=0; for(int i=1;i<=n;i++){double x,y;cin>>x>>y;double p=sigmoid(w*x+b);double e=p-y;w-=lr*e*x;b-=lr*e;}cout<<fixed<<setprecision(6)<<w<<" "<<b<<"\n";return 0;}
''', "V10-CEX03 逻辑回归一轮 SGD", "第 10 卷", "监督学习、梯度下降", "模拟训练规则，不追求真实模型效果。", "参考来源：机器学习 logistic regression 基础。", "用每个样本做一次 SGD 更新。", "第一行 n lr，之后 x y。", "输出 w b。", "2 1\n0 0\n1 1\n", "0.622459 0.122459"),
    ex(CPP_PREFIX + r'''
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);double x,w,b,target,lr;cin>>x>>w>>b>>target>>lr;double y=w*x+b;double loss=(y-target)*(y-target);double gw=2*(y-target)*x;double gb=2*(y-target);w-=lr*gw;b-=lr*gb;cout<<fixed<<setprecision(4)<<loss<<" "<<w<<" "<<b<<"\n";return 0;}
''', "V10-CEX04 单神经元反向传播", "第 10 卷", "反向传播、梯度", "把链式法则落实成代码。", "参考来源：反向传播基础。", "单神经元 y=wx+b，平方损失，做一次梯度下降。", "输入 x w b target lr。", "输出 loss 新w 新b。", "2 1 0 3 0.1\n", "1.0000 1.4000 0.2000"),
    ex(CPP_PREFIX + r'''
struct Var{double val,grad;};
int main(){ios::sync_with_stdio(false);cin.tie(nullptr);double x,y;cin>>x>>y;Var a{x,0},b{y,0};double c=a.val*b.val;double d=c+a.val;double e=d*d;double ge=1;double gd=ge*2*d;double gc=gd; a.grad+=gd; a.grad+=gc*b.val; b.grad+=gc*a.val;cout<<fixed<<setprecision(4)<<e<<" "<<a.grad<<" "<<b.grad<<"\n";return 0;}
''', "V10-CEX05 手算反向模式自动求导", "第 10 卷", "自动求导、计算图", "AI 模拟题可能要求按规则反传。", "参考来源：自动微分/反向模式基础。", "计算 `e=(x*y+x)^2` 及对 x,y 的梯度。", "输入 x y。", "输出 e dx dy。", "2 3\n", "64.0000 64.0000 32.0000"),
]


def main() -> None:
    lines = [
        "# v0.2 组合例题补充 Worker G",
        "",
        "本文件为再次审计后新增的组合例题区。每卷补 5 道，题型参考洛谷题单、OI Wiki 和经典 NOI/ICPC 模板题；题面均为考场版简化描述，代码为完整可运行版本。",
        "",
    ]
    for item in examples:
        lines.extend([
            f"### {item['title']}",
            "",
            f"- 归属卷：{item['vol']}",
            f"- 覆盖模块：{item['modules']}",
            f"- 考场用途：{item['use']}",
            f"- 参考题型来源：{item['source']}",
            "",
            f"**题目描述：** {item['desc']}",
            "",
            f"**输入格式：** {item['inp']}",
            "",
            f"**输出格式：** {item['out']}",
            "",
            "**样例输入：**",
            "```text",
            item["sample_in"],
            "```",
            "",
            "**样例输出：**",
            "```text",
            item["sample_out"],
            "```",
            "",
            "**完整代码：**",
            "```python" if item["vol"] == "第 9 卷" else "```cpp",
            item["code"].rstrip(),
            "```",
            "",
            f"**测试设计：** {item['tests']}",
            "",
            "***",
            "",
        ])
    OUT.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"examples={len(examples)}")


if __name__ == "__main__":
    main()
