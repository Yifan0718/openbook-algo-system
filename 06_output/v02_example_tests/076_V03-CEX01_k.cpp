#include <bits/stdc++.h>
using namespace std;


int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, k;
    cin >> n >> k;
    vector<long long> a(n + 1), pre(n + 1);
    for (int i = 1; i <= n; i++) { cin >> a[i]; pre[i] = pre[i - 1] + a[i]; }
    const long long INF = (long long)4e18;
    vector<vector<long long>> dp(k + 1, vector<long long>(n + 1, INF));
    dp[0][0] = 0;
    for (int p = 1; p <= k; p++) {
        for (int i = 1; i <= n; i++) {
            for (int j = 0; j < i; j++) {
                long long seg = pre[i] - pre[j];
                dp[p][i] = min(dp[p][i], max(dp[p - 1][j], seg));
            }
        }
    }
    cout << dp[k][n] << '\n';
    return 0;
}
