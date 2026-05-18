#include <bits/stdc++.h>
using namespace std;


int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    long long S;
    cin >> n >> S;
    int n1 = n / 2, n2 = n - n1;
    vector<long long> a(n + 1), left, right;
    for (int i = 1; i <= n; i++) cin >> a[i];
    for (int mask = 0; mask < (1 << n1); mask++) {
        long long s = 0;
        for (int i = 0; i < n1; i++) if (mask & (1 << i)) s += a[i + 1];
        left.push_back(s);
    }
    for (int mask = 0; mask < (1 << n2); mask++) {
        long long s = 0;
        for (int i = 0; i < n2; i++) if (mask & (1 << i)) s += a[n1 + i + 1];
        right.push_back(s);
    }
    sort(right.begin(), right.end());
    long long ans = 0;
    for (long long x : left) ans += upper_bound(right.begin(), right.end(), S - x) - right.begin();
    cout << ans << '\n';
    return 0;
}
