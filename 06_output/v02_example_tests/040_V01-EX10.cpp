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
        int l, r;
        cin >> l >> r;
        auto left_it = lower_bound(a.begin() + 1, a.end(), l);
        auto right_it = upper_bound(a.begin() + 1, a.end(), r);
        cout << (right_it - left_it) << '\n';
    }
    return 0;
}
