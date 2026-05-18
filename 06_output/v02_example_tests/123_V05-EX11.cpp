#include <bits/stdc++.h>
using namespace std;

using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<ll> w(n + 1);
    for (int i = 1; i <= n; i++) cin >> w[i];

    vector<vector<int>> g(n + 1);
    for (int i = 1; i <= n - 1; i++) {
        int u, v;
        cin >> u >> v;
        g[u].push_back(v);
        g[v].push_back(u);
    }

    vector<array<ll, 2>> dp(n + 1);
    function<void(int, int)> dfs = [&](int u, int p) {
        dp[u][0] = 0;
        dp[u][1] = w[u];
        for (int v : g[u]) {
            if (v == p) continue;
            dfs(v, u);
            dp[u][0] += max(dp[v][0], dp[v][1]);
            dp[u][1] += dp[v][0];
        }
    };

    dfs(1, 0);
    cout << max(dp[1][0], dp[1][1]) << '\n';
    return 0;
}
