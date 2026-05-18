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
