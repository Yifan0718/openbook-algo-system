#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, W;
    cin >> n >> W;
    vector<ll> dp(W + 1, 0);
    for (int i = 1; i <= n; i++) {
        int w;
        ll v;
        cin >> w >> v;
        for (int cap = W; cap >= w; cap--) {
            dp[cap] = max(dp[cap], dp[cap - w] + v);
        }
    }
    cout << dp[W] << '\n';
    return 0;
}
