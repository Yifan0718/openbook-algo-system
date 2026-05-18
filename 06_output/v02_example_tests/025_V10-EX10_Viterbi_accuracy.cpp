#include <bits/stdc++.h>
using namespace std;

const double NEG = -1e100;

double safe_log(double x) {
    return x <= 0 ? NEG : log(x);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m, T;
    cin >> n >> m >> T;
    vector<double> pi(n + 1);
    for (int i = 1; i <= n; i++) cin >> pi[i];
    vector<vector<double>> trans(n + 1, vector<double>(n + 1));
    for (int i = 1; i <= n; i++) for (int j = 1; j <= n; j++) cin >> trans[i][j];
    vector<vector<double>> emit(n + 1, vector<double>(m + 1));
    for (int i = 1; i <= n; i++) for (int j = 1; j <= m; j++) cin >> emit[i][j];
    vector<int> obs(T + 1), real(T + 1);
    for (int t = 1; t <= T; t++) cin >> obs[t];
    for (int t = 1; t <= T; t++) cin >> real[t];

    vector<vector<double>> dp(T + 1, vector<double>(n + 1, NEG));
    vector<vector<int>> pre(T + 1, vector<int>(n + 1, 1));
    for (int s = 1; s <= n; s++) dp[1][s] = safe_log(pi[s]) + safe_log(emit[s][obs[1]]);
    for (int t = 2; t <= T; t++) {
        for (int s = 1; s <= n; s++) {
            for (int p = 1; p <= n; p++) {
                double cur = dp[t - 1][p] + safe_log(trans[p][s]) + safe_log(emit[s][obs[t]]);
                if (cur > dp[t][s]) {
                    dp[t][s] = cur;
                    pre[t][s] = p;
                }
            }
        }
    }
    int last = 1;
    for (int s = 2; s <= n; s++) if (dp[T][s] > dp[T][last]) last = s;
    vector<int> path(T + 1);
    path[T] = last;
    for (int t = T; t >= 2; t--) path[t - 1] = pre[t][path[t]];

    int correct = 0;
    for (int t = 1; t <= T; t++) {
        if (t > 1) cout << ' ';
        cout << path[t];
        if (path[t] == real[t]) correct++;
    }
    cout << '\n' << fixed << setprecision(6) << (double)correct / T << '\n';
    return 0;
}
