#include <bits/stdc++.h>
using namespace std;

int n;
vector<long long> value_node;
vector<vector<int>> graph_edges;
vector<array<long long, 2>> dp;

void dfs(int u, int parent) {
    dp[u][0] = 0;
    dp[u][1] = value_node[u];
    for (int v : graph_edges[u]) {
        if (v == parent) continue;
        dfs(v, u);
        dp[u][0] += max(dp[v][0], dp[v][1]);
        dp[u][1] += dp[v][0];
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n;
    value_node.assign(n + 1, 0);
    graph_edges.assign(n + 1, {});
    dp.assign(n + 1, {0, 0});

    for (int i = 1; i <= n; i++) cin >> value_node[i];
    for (int i = 1; i <= n - 1; i++) {
        int u, v;
        cin >> u >> v;
        graph_edges[u].push_back(v);
        graph_edges[v].push_back(u);
    }

    dfs(1, 0);
    cout << max(dp[1][0], dp[1][1]) << '\n';
    return 0;
}
