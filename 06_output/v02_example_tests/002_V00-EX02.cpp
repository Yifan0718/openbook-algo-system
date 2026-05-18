#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, q;
    cin >> n >> q;
    vector<ll> a(n + 1), diff(n + 2, 0);
    for (int i = 1; i <= n; i++) cin >> a[i];
    while (q--) {
        int l, r;
        ll x;
        cin >> l >> r >> x;
        diff[l] += x;
        diff[r + 1] -= x;
    }
    ll add = 0;
    for (int i = 1; i <= n; i++) {
        add += diff[i];
        if (i > 1) cout << ' ';
        cout << a[i] + add;
    }
    cout << '\n';
    return 0;
}
