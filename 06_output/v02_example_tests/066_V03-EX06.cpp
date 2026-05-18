#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int G, W;
    cin >> G >> W;
    vector<long long> dp(W + 1, 0);

    for (int group_id = 1; group_id <= G; group_id++) {
        int k;
        cin >> k;
        vector<int> weight(k + 1), value(k + 1);
        for (int i = 1; i <= k; i++) {
            cin >> weight[i] >> value[i];
        }

        vector<long long> old = dp;
        for (int j = 0; j <= W; j++) {
            dp[j] = old[j];
        }
        for (int i = 1; i <= k; i++) {
            for (int j = weight[i]; j <= W; j++) {
                dp[j] = max(dp[j], old[j - weight[i]] + value[i]);
            }
        }
    }

    cout << dp[W] << '\n';
    return 0;
}
