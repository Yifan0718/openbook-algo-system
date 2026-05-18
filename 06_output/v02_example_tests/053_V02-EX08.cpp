#include <bits/stdc++.h>
using namespace std;

const long long NEG = -(1LL << 60);

int n, m;
vector<vector<long long>> grid, memo;
vector<vector<int>> vis;

long long dfs(int i, int j) {
    if (i > n || j > m) return NEG;
    if (grid[i][j] == -1) return NEG;
    if (i == n && j == m) return grid[i][j];
    if (vis[i][j]) return memo[i][j];
    vis[i][j] = 1;

    long long bestNext = max(dfs(i + 1, j), dfs(i, j + 1));
    if (bestNext == NEG) memo[i][j] = NEG;
    else memo[i][j] = grid[i][j] + bestNext;
    return memo[i][j];
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n >> m;
    grid.assign(n + 1, vector<long long>(m + 1, 0));
    memo.assign(n + 1, vector<long long>(m + 1, NEG));
    vis.assign(n + 1, vector<int>(m + 1, 0));

    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            cin >> grid[i][j];
        }
    }

    long long ans = dfs(1, 1);
    cout << (ans == NEG ? -1 : ans) << '\n';
    return 0;
}
