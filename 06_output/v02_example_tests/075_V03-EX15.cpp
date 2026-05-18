#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<long long> price(n + 1);
    for (int i = 1; i <= n; i++) {
        cin >> price[i];
    }

    const long long NEG = -4'000'000'000'000'000'000LL;
    vector<array<long long, 3>> dp(n + 1);
    for (int i = 0; i <= n; i++) {
        dp[i] = {NEG, NEG, NEG};
    }

    dp[0][0] = 0;
    for (int i = 1; i <= n; i++) {
        dp[i][0] = max(dp[i - 1][0], dp[i - 1][2]);
        dp[i][1] = max(dp[i - 1][1], dp[i - 1][0] - price[i]);
        dp[i][2] = dp[i - 1][1] + price[i];
    }

    cout << max(dp[n][0], dp[n][2]) << '\n';
    return 0;
}
