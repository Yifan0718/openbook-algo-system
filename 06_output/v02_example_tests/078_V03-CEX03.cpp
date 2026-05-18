#include <bits/stdc++.h>
using namespace std;


int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string s;
    cin >> s;
    int n = (int)s.size();
    s = " " + s;
    vector<vector<int>> dp(n + 2, vector<int>(n + 2, 0));
    for (int len = 1; len <= n; len++) {
        for (int l = 1; l + len - 1 <= n; l++) {
            int r = l + len - 1;
            dp[l][r] = 1 + dp[l + 1][r];
            for (int k = l + 1; k <= r; k++) {
                if (s[k] == s[l]) dp[l][r] = min(dp[l][r], dp[l + 1][k - 1] + dp[k][r]);
            }
        }
    }
    cout << dp[1][n] << '\n';
    return 0;
}
