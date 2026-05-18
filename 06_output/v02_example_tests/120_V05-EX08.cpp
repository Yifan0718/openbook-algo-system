#include <bits/stdc++.h>
using namespace std;

bool dfs(int u, const vector<vector<int>>& adj, vector<int>& seen, vector<int>& matchR, int tag) {
    if (seen[u] == tag) return false;
    seen[u] = tag;
    for (int r : adj[u]) {
        if (matchR[r] == 0 || dfs(matchR[r], adj, seen, matchR, tag)) {
            matchR[r] = u;
            return true;
        }
    }
    return false;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int nL, nR, m;
    cin >> nL >> nR >> m;
    vector<vector<int>> adj(nL + 1);
    for (int i = 1; i <= m; i++) {
        int u, v;
        cin >> u >> v;
        adj[u].push_back(v);
    }

    vector<int> matchR(nR + 1, 0), seen(nL + 1, 0);
    int ans = 0;
    for (int u = 1; u <= nL; u++) {
        if (dfs(u, adj, seen, matchR, u)) ans++;
    }

    cout << ans << '\n';
    return 0;
}
