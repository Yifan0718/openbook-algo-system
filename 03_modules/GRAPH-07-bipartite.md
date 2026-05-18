# GRAPH-07 二分图染色与二分图匹配

模块编号：GRAPH-07

模块名称：二分图染色、二分图匹配

标签：[图论][二分图][染色][匹配]

一句话用途：用 BFS/DFS 染色判断图能否分成左右两部；已知左右部时用匹配求最多配对数。

题面触发词：

- 分成两组，组内不能有冲突。
- 奇环判断。
- 男生女生、机器任务、左部右部配对。
- 每个对象最多匹配一个。

什么时候用：

- 二分图判断：无向图，要求相邻点颜色不同。
- 二分图匹配：左部点和右部点之间有可选边，每点最多选一条。
- 数据规模中等，匈牙利/Kuhn 能过。

不要什么时候用：

- 一般图最大匹配不是这个模板。
- 带权匹配不是这个模板。
- 需要最大流建模也可以用 Dinic，但本模块更短。
- 图不是天然左右部时，先染色再决定左右部。

复杂度：

- 染色：`O(n + m)`。
- Kuhn 匹配：`O(nL * m)` 最坏，常用于中小规模。

数据范围参考：

- 染色可到 `2e5`。
- Kuhn 匹配适合 `nL,nR,m <= 2000~5000` 视时限而定。
- 更大二分图匹配建议 Dinic 或 Hopcroft-Karp。

依赖的标准容器：

- `Graph`。
- 染色遍历 `G.g[u]`。
- 匹配模板独立用 `adjL[left].push_back(right)`，右部也保持 `1..nR`，不做偏移。

输入如何整理：

```cpp
// 二分图判断：无向冲突边
Graph G(n);
G.add_undirected(u, v);

// 二分图匹配：左部 1..nL，右部 1..nR
adjL[left].push_back(right);
```

接口：

```text
BipartiteColorResult bipartite_color(const Graph& G)
MatchingResult bipartite_matching_kuhn_result(vector<int> adjL[], int nL, int nR)
int bipartite_matching_kuhn(vector<int> adjL[], int nL, int nR)
```

输出能力：

- 是否为二分图。
- 每个点颜色 `1/2`。
- 最大匹配数。
- 右部每个点匹配到的左部点。

下游可接：

- 分组可行性。
- 最小点覆盖、最大独立集等进阶结论。
- Dinic 最大流替代。

可拼接模块：

- `Graph + BFS Color`。
- `adjL[1..nL] + Kuhn Matching`。
- `Bipartite + Dinic`。

模板代码：

```cpp
struct BipartiteColorResult {
    bool ok = true;
    vector<int> color;
};

BipartiteColorResult bipartite_color(const Graph &G) {
    BipartiteColorResult res;
    res.color.assign(G.n + 1, 0);
    for (int s = 1; s <= G.n; s++) {
        if (res.color[s]) continue;
        queue<int> q;
        res.color[s] = 1;
        q.push(s);
        while (!q.empty()) {
            int u = q.front();
            q.pop();
            for (auto e : G.g[u]) {
                int v = e.to;
                if (!res.color[v]) {
                    res.color[v] = 3 - res.color[u];
                    q.push(v);
                } else if (res.color[v] == res.color[u]) {
                    res.ok = false;
                }
            }
        }
    }
    return res;
}

bool kuhn_dfs(int u, vector<int> adjL[], vector<int> &vis, vector<int> &matchR, int tag) {
    vis[u] = tag;
    for (int r : adjL[u]) {
        if (matchR[r] == 0 || (vis[matchR[r]] != tag && kuhn_dfs(matchR[r], adjL, vis, matchR, tag))) {
            matchR[r] = u;
            return true;
        }
    }
    return false;
}

struct MatchingResult {
    int size = 0;
    vector<int> matchR; // matchR[r] = matched left node, 0 means unmatched
};

MatchingResult bipartite_matching_kuhn_result(vector<int> adjL[], int nL, int nR) {
    vector<int> matchR(nR + 1, 0);
    vector<int> vis(nL + 1, 0);
    MatchingResult res;
    for (int u = 1; u <= nL; u++) {
        if (kuhn_dfs(u, adjL, vis, matchR, u)) res.size++;
    }
    res.matchR = matchR;
    return res;
}

int bipartite_matching_kuhn(vector<int> adjL[], int nL, int nR) {
    return bipartite_matching_kuhn_result(adjL, nL, nR).size;
}
```

调用示例：

```cpp
auto color = bipartite_color(G);
cout << (color.ok ? "YES" : "NO") << "\n";

const int MAXL = 200000 + 5;
static vector<int> adjL[MAXL];
adjL[1].push_back(2);
cout << bipartite_matching_kuhn(adjL, nL, nR) << "\n";

auto mt = bipartite_matching_kuhn_result(adjL, nL, nR);
for (int r = 1; r <= nR; r++) {
    if (mt.matchR[r]) cout << mt.matchR[r] << " - " << r << '\n';
}
```

常见坑：

- 二分图染色针对无向冲突图最常见，有向边要先理解题意。
- 图不连通也要从每个未染色点启动。
- 自环一定破坏二分图。
- 匹配模板要求左部 `1..nL`、右部 `1..nR`；不要把右部偏移成全局点号。
- Kuhn 的 `vis` 是每轮 DFS 的访问标记，不是全局永久访问。
- 大规模匹配 Kuhn 可能 TLE。

暴力/部分分替代：

- `n <= 20` 可枚举每个点颜色判断冲突。
- 小规模匹配可枚举左部每个点选哪个右部。
- 最大匹配也可用 Dinic 建流网络，代码更长但更稳。

升级方向：

- 大规模二分图匹配：Hopcroft-Karp 或 Dinic。
- 带权匹配：费用流或 KM。
- 二分图最小点覆盖：在最大匹配后用经典构造。

最小测试样例：

```text
染色：
3 3
1 2
2 3
3 1
输出 NO

匹配：
nL=2,nR=2, edges: 1-1, 1-2, 2-2
最大匹配 = 2
```
