#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<vector<long long>> cost(n + 1, vector<long long>(n + 1, 0));
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++) {
            cin >> cost[i][j];
        }
    }

    int total_mask = 1 << n;
    const long long INF = 4'000'000'000'000'000'000LL;
    vector<vector<long long>> dp(total_mask, vector<long long>(n + 1, INF));
    int start_mask = 1 << 0;
    dp[start_mask][1] = 0;

    for (int mask = 0; mask < total_mask; mask++) {
        for (int last = 1; last <= n; last++) {
            if (dp[mask][last] == INF) continue;
            for (int next = 1; next <= n; next++) {
                int bit = 1 << (next - 1);
                if ((mask & bit) != 0) continue;
                int new_mask = mask | bit;
                dp[new_mask][next] = min(dp[new_mask][next], dp[mask][last] + cost[last][next]);
            }
        }
    }

    int full_mask = total_mask - 1;
    long long answer = INF;
    for (int last = 1; last <= n; last++) {
        answer = min(answer, dp[full_mask][last]);
    }

    cout << answer << '\n';
    return 0;
}
