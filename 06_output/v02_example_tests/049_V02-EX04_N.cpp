#include <bits/stdc++.h>
using namespace std;

int n;
long long ans = 0;
vector<int> colUsed, diag1Used, diag2Used;

void dfs(int row) {
    if (row == n + 1) {
        ans++;
        return;
    }
    for (int col = 1; col <= n; col++) {
        int d1 = row + col;
        int d2 = row - col + n;
        if (colUsed[col] || diag1Used[d1] || diag2Used[d2]) continue;
        colUsed[col] = diag1Used[d1] = diag2Used[d2] = 1;
        dfs(row + 1);
        colUsed[col] = diag1Used[d1] = diag2Used[d2] = 0;
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n;
    colUsed.assign(n + 1, 0);
    diag1Used.assign(2 * n + 2, 0);
    diag2Used.assign(2 * n + 2, 0);

    dfs(1);
    cout << ans << '\n';
    return 0;
}
