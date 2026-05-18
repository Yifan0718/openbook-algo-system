#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, S;
    cin >> n >> S;
    vector<int> coin(n + 1);
    for (int i = 1; i <= n; i++) cin >> coin[i];

    const int INF = 1000000000;
    vector<int> dp(S + 1, INF);
    dp[0] = 0;
    for (int i = 1; i <= n; i++) {
        for (int sum = coin[i]; sum <= S; sum++) {
            dp[sum] = min(dp[sum], dp[sum - coin[i]] + 1);
        }
    }

    cout << (dp[S] == INF ? -1 : dp[S]) << '\n';
    return 0;
}
