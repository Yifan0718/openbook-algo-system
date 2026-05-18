#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    long long target;
    cin >> n >> target;
    vector<long long> a(n + 1);
    for (int i = 1; i <= n; i++) cin >> a[i];

    long long ans = 0;
    int totalMask = 1 << n;
    for (int mask = 0; mask < totalMask; mask++) {
        long long sum = 0;
        for (int i = 1; i <= n; i++) {
            if (mask & (1 << (i - 1))) {
                sum += a[i];
            }
        }
        if (sum == target) ans++;
    }

    cout << ans << '\n';
    return 0;
}
