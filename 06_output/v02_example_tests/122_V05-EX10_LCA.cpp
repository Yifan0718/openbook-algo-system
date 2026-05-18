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
