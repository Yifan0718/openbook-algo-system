#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<double> dp(n + 7, 0.0);
    for (int i = n - 1; i >= 0; i--) {
        dp[i] = 1.0;
        for (int d = 1; d <= 6; d++) dp[i] += dp[i + d] / 6.0;
    }
    cout << fixed << setprecision(6) << dp[0] << '\n';
    return 0;
}
