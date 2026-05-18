#include <bits/stdc++.h>
using namespace std;


int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, W;
    cin >> n >> W;
    vector<int> weight(n + 1), value(n + 1), cnt(n + 1);
    for (int i = 1; i <= n; i++) cin >> weight[i] >> value[i] >> cnt[i];
    vector<long long> dp(W + 1, 0);
    for (int i = 1; i <= n; i++) {
        int c = cnt[i];
        for (int b = 1; c > 0; b <<= 1) {
            int take = min(b, c);
            c -= take;
            int w = weight[i] * take, v = value[i] * take;
            for (int j = W; j >= w; j--) dp[j] = max(dp[j], dp[j - w] + v);
        }
    }
    cout << *max_element(dp.begin(), dp.end()) << '\n';
    return 0;
}
