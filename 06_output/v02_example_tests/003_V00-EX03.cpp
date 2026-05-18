#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct BIT {
    int n;
    vector<ll> bit;

    void init(int n_) {
        n = n_;
        bit.assign(n + 1, 0);
    }

    void add(int pos, ll delta) {
        for (int i = pos; i <= n; i += i & -i) bit[i] += delta;
    }

    ll prefix(int pos) const {
        ll res = 0;
        for (int i = pos; i > 0; i -= i & -i) res += bit[i];
        return res;
    }

    ll query(int l, int r) const {
        return prefix(r) - prefix(l - 1);
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, q;
    cin >> n >> q;
    vector<ll> a(n + 1);
    BIT fw;
    fw.init(n);
    for (int i = 1; i <= n; i++) {
        cin >> a[i];
        fw.add(i, a[i]);
    }
    while (q--) {
        char op;
        cin >> op;
        if (op == 'S') {
            int p;
            ll x;
            cin >> p >> x;
            fw.add(p, x - a[p]);
            a[p] = x;
        } else {
            int l, r;
            cin >> l >> r;
            cout << fw.query(l, r) << '\n';
        }
    }
    return 0;
}
