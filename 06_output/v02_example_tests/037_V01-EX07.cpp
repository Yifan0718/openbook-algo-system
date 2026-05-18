#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<int> a(n + 1);
    for (int i = 1; i <= n; i++) cin >> a[i];

    sort(a.begin() + 1, a.end());

    int q;
    cin >> q;
    for (int i = 1; i <= q; i++) {
        int x;
        cin >> x;
        auto it = lower_bound(a.begin() + 1, a.end(), x);
        if (it == a.end()) {
            cout << -1 << '\n';
        } else {
            int pos = (int)(it - a.begin());
            cout << pos << ' ' << *it << '\n';
        }
    }
    return 0;
}
