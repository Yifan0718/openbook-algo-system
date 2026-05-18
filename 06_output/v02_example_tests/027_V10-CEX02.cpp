#include <bits/stdc++.h>
using namespace std;


int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;
    vector<vector<double>> x(n + 1, vector<double>(m + 1));
    vector<int> y(n + 1);

    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) cin >> x[i][j];
        cin >> y[i];
    }

    vector<double> q(m + 1);
    for (int j = 1; j <= m; j++) cin >> q[j];

    int ans_label = -1;
    double best_dist = 1e100;
    for (int i = 1; i <= n; i++) {
        double d = 0;
        for (int j = 1; j <= m; j++) {
            d += (x[i][j] - q[j]) * (x[i][j] - q[j]);
        }
        if (d < best_dist) {
            best_dist = d;
            ans_label = y[i];
        }
    }

    cout << ans_label << '\n';
    return 0;
}
