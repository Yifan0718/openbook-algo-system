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
