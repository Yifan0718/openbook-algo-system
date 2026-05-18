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
