#include <bits/stdc++.h>
using namespace std;
using ll = long long;

bool can_split(const vector<ll> &a, int n, int k, ll limit) {
    int groups = 1;
    ll current = 0;
    for (int i = 1; i <= n; i++) {
        if (a[i] > limit) return false;
        if (current + a[i] <= limit) {
            current += a[i];
        } else {
            groups++;
            current = a[i];
        }
    }
    return groups <= k;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, k;
    cin >> n >> k;
    vector<ll> a(n + 1);
    ll left = 0, right = 0;
    for (int i = 1; i <= n; i++) {
        cin >> a[i];
        left = max(left, a[i]);
        right += a[i];
    }
    while (left < right) {
        ll mid = left + (right - left) / 2;
        if (can_split(a, n, k, mid)) right = mid;
        else left = mid + 1;
    }
    cout << left << '\n';
    return 0;
}
