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
    if (n <= 25) {
        for (int mask = 0; mask < (1 << n); mask++) {
            long long sum = 0;
            for (int i = 1; i <= n; i++) if (mask & (1 << (i - 1))) sum += a[i];
            if (sum == target) ans++;
        }
    } else {
        unordered_map<long long, long long> cnt;
        cnt.reserve(n * 2 + 10);
        for (int i = 1; i <= n; i++) {
            ans += cnt[target - a[i]];
            cnt[a[i]]++;
        }
    }
    cout << ans << '\n';
    return 0;
}
