#include <bits/stdc++.h>
using namespace std;

using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m, q;
    cin >> n >> m >> q;
    vector<vector<ll>> diff(n + 2, vector<ll>(m + 2, 0));

    while (q--) {
        int x1, y1, x2, y2;
        ll v;
        cin >> x1 >> y1 >> x2 >> y2 >> v;
        diff[x1][y1] += v;
        diff[x2 + 1][y1] -= v;
        diff[x1][y2 + 1] -= v;
        diff[x2 + 1][y2 + 1] += v;
    }

    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            diff[i][j] += diff[i - 1][j] + diff[i][j - 1] - diff[i - 1][j - 1];
            if (j > 1) cout << ' ';
            cout << diff[i][j];
        }
        cout << '\n';
    }
    return 0;
}
