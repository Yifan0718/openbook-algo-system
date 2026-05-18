#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, q;
    cin >> n >> q;
    vector<ll> a(n + 1), prefix(n + 1, 0);
    for (int i = 1; i <= n; i++) {
        cin >> a[i];
        prefix[i] = prefix[i - 1] + a[i];
    }
    while (q--) {
        int l, r;
        cin >> l >> r;
        ll fast = prefix[r] - prefix[l - 1];
        ll slow = 0;
        for (int i = l; i <= r; i++) slow += a[i];
        if (fast != slow) {
            cout << "CHECK_FAILED\n";
            return 0;
        }
        cout << fast << '\n';
    }
    return 0;
}
