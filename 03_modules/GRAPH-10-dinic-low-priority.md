# GRAPH-10 Dinic 最大流低优先级补充

模块编号：GRAPH-10

模块名称：Dinic 最大流

标签：[图论][网络流][Dinic][低优先级]

一句话用途：当题目能建成容量网络时，用 Dinic 求从源点到汇点的最大可发送流量。

题面触发词：

- 最大流、容量、源点、汇点。
- 每条边最多通过多少。
- 二分图匹配的大规模版本。
- 割、最少删除容量。

什么时候用：

- 题目明确是流量从源点流到汇点。
- 每条边有容量限制。
- 二分图匹配用普通匹配会超时，想换最大流。
- 需要最小割值，最大流等于最小割。

不要什么时候用：

- 普通最短路、MST、连通性不要用流。
- 有费用最小化不是 Dinic，要最小费用最大流。
- 标准 `Graph` 不适合残量网络，必须用独立 `FlowGraph`。
- 没想清楚建图时不要硬套。

复杂度：

- 常见竞赛规模表现较好。
- 理论上界较复杂，纸质版只按“中等规模网络流”使用。

数据范围参考：

- 点边几千到几万视图结构和时限而定。
- 二分图匹配网络通常可用。

依赖的标准容器：

- 独立 `FlowGraph`。
- 不使用 `Graph`，因为需要反向边和残量容量。
- `LINF` 依赖主骨架 `const ll LINF = 4'000'000'000'000'000'000LL;`。

输入如何整理：

```cpp
FlowGraph F(n);
F.add_edge(u, v, cap);
// addEdge 只是旧题解兼容别名；新写统一用 add_edge。
```

接口：

```text
FlowGraph.init(n)
FlowGraph.add_edge(u, v, cap)
FlowGraph.addEdge(u, v, cap)  // 旧题解兼容包装别名，新写不推荐
FlowGraph.maxflow(s, t)
```

输出能力：

- 最大流值。
- 残量网络可进一步推出最小割集合。

下游可接：

- 二分图匹配。
- 最小割判定。
- 可行流进阶。

可拼接模块：

- `Bipartite Matching -> Dinic`。
- `Binary Answer + Dinic Check`。

模板代码：

```cpp
struct FlowEdge {
    int to;
    int rev;
    ll cap;
};

struct FlowGraph {
    int n;
    vector<vector<FlowEdge>> g;
    vector<int> level, it;

    FlowGraph(int n = 0) {
        init(n);
    }

    void init(int n_) {
        n = n_;
        g.assign(n + 1, {});
    }

    void add_edge(int u, int v, ll cap) {
        FlowEdge a{v, (int)g[v].size(), cap};
        FlowEdge b{u, (int)g[u].size(), 0};
        g[u].push_back(a);
        g[v].push_back(b);
    }

    void addEdge(int u, int v, ll cap) {
        add_edge(u, v, cap);
    }

    bool bfs(int s, int t) {
        level.assign(n + 1, -1);
        queue<int> q;
        level[s] = 0;
        q.push(s);
        while (!q.empty()) {
            int u = q.front();
            q.pop();
            for (auto e : g[u]) {
                if (e.cap > 0 && level[e.to] == -1) {
                    level[e.to] = level[u] + 1;
                    q.push(e.to);
                }
            }
        }
        return level[t] != -1;
    }

    ll dfs(int u, int t, ll f) {
        if (u == t) return f;
        for (int &i = it[u]; i < (int)g[u].size(); i++) {
            FlowEdge &e = g[u][i];
            if (e.cap <= 0 || level[e.to] != level[u] + 1) continue;
            ll ret = dfs(e.to, t, min(f, e.cap));
            if (ret > 0) {
                e.cap -= ret;
                g[e.to][e.rev].cap += ret;
                return ret;
            }
        }
        return 0;
    }

    ll maxflow(int s, int t) {
        ll flow = 0;
        while (bfs(s, t)) {
            it.assign(n + 1, 0);
            while (true) {
                ll f = dfs(s, t, LINF);
                if (f == 0) break;
                flow += f;
            }
        }
        return flow;
    }
};
```

调用示例：

```cpp
FlowGraph F(n);
F.add_edge(s, a, cap1);
F.add_edge(a, t, cap2);
cout << F.maxflow(s, t) << "\n";
```

常见坑：

- Dinic 必须有反向边，不能用标准 `Graph` 直接替代。
- `add_edge` 只加有向容量边；无向容量边通常要加两条有向边。
- 容量和答案用 `ll`。
- `dfs` 找到流后要同时改正向和反向容量。
- 多组数据要 `init(n)`。
- 递归深度过大时可能有栈风险。

暴力/部分分替代：

- 小图可枚举割集或路径增广。
- 二分图匹配小规模用 Kuhn。
- 容量都为 1 且图小，可每次 BFS 找增广路。

升级方向：

- 有费用：最小费用最大流。
- 只求二分图最大匹配：Hopcroft-Karp 更专门。
- 需要割边集合：最大流后从源点在残量网络 DFS 标记可达点。

最小测试样例：

```text
s=1,t=4
1->2 cap 3
1->3 cap 2
2->4 cap 2
3->4 cap 4
最大流 = 4
```
