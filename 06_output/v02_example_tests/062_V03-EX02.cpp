#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string s;
    int target;
    cin >> s >> target;
    int n = (int)s.size();
    const int INF = 1'000'000'000;
    vector<vector<int>> dp(n + 1, vector<int>(target + 1, INF));
    dp[0][0] = 0;

    for (int i = 0; i < n; i++) {
        for (int sum = 0; sum <= target; sum++) {
            if (dp[i][sum] == INF) continue;
            long long value = 0;
            for (int j = i + 1; j <= n; j++) {
                value = value * 10 + (s[j - 1] - '0');
                if (value > target) break;
                if (sum + value <= target) {
                    dp[j][sum + (int)value] = min(dp[j][sum + (int)value], dp[i][sum] + 1);
                }
            }
        }
    }

    if (dp[n][target] == INF) {
        cout << -1 << '\n';
    } else {
        cout << dp[n][target] - 1 << '\n';
    }
    return 0;
}
