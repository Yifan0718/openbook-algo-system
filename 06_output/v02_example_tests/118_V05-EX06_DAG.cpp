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
