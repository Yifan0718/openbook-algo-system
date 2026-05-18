#include <bits/stdc++.h>
using namespace std;


int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    cin >> n >> q;
    vector<int> a(n + 1);
    for (int i = 1; i <= n; i++) cin >> a[i];
    sort(a.begin() + 1, a.end());
    while (q--) {
        int x;
        cin >> x;
        auto it = lower_bound(a.begin() + 1, a.end(), x);
        if (it == a.end()) cout << "NONE\n";
        else cout << *it << '\n';
    }
    return 0;
}
