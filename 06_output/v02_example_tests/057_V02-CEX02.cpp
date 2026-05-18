#include <bits/stdc++.h>
using namespace std;


int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<int> need(m + 1), cover(n + 1);
    for (int i = 1; i <= m; i++) cin >> need[i];
    for (int i = 1; i <= n; i++) cin >> cover[i];
    int ans = n + 1;
    for (int mask = 0; mask < (1 << n); mask++) {
        int have = 0, cnt = 0;
        for (int i = 1; i <= n; i++) if (mask & (1 << (i - 1))) {
            have |= cover[i];
            cnt++;
        }
        bool ok = true;
        for (int i = 1; i <= m; i++) if ((have & need[i]) != need[i]) ok = false;
        if (ok) ans = min(ans, cnt);
    }
    cout << (ans == n + 1 ? -1 : ans) << '\n';
    return 0;
}
