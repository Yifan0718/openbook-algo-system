#include <bits/stdc++.h>
using namespace std;


int n, W;
vector<vector<pair<int,int>>> child;
vector<int> w, v;
vector<vector<long long>> dp;
void dfs(int u) {
    dp[u].assign(W + 1, -4e18);
    dp[u][w[u]] = v[u];
    for (auto [to, dummy] : child[u]) {
        dfs(to);
        vector<long long> ndp = dp[u];
        for (int i = 0; i <= W; i++) if (dp[u][i] > -3e18) {
            for (int j = 0; i + j <= W; j++) if (dp[to][j] > -3e18) {
                ndp[i + j] = max(ndp[i + j], dp[u][i] + dp[to][j]);
            }
        }
        dp[u] = ndp;
    }
}
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cin >> n >> W;
    child.assign(n + 1, {});
    w.assign(n + 1, 0); v.assign(n + 1, 0);
    int root = 1;
    for (int i = 1; i <= n; i++) {
        int p;
        cin >> p >> w[i] >> v[i];
        if (p == 0) root = i;
        else child[p].push_back({i, 0});
    }
    dp.resize(n + 1);
    dfs(root);
    cout << *max_element(dp[root].begin(), dp[root].end()) << '\n';
    return 0;
}
