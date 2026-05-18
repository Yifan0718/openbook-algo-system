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
