#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n;
    vector<int> a(n + 1);
    for (int i = 1; i <= n; i++) cin >> a[i];
    cin >> m;
    vector<int> b(m + 1);
    for (int j = 1; j <= m; j++) cin >> b[j];

    vector<int> dp(m + 1, 0);
    for (int i = 1; i <= n; i++) {
        int best = 0;
        for (int j = 1; j <= m; j++) {
            if (a[i] == b[j]) {
                dp[j] = max(dp[j], best + 1);
            } else if (b[j] < a[i]) {
                best = max(best, dp[j]);
            }
        }
    }

    int answer = 0;
    for (int j = 1; j <= m; j++) answer = max(answer, dp[j]);
    cout << answer << '\n';
    return 0;
}
