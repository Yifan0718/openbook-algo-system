#include <bits/stdc++.h>
using namespace std;

using ll = long long;

struct SegTree {
    int n = 0;
    vector<ll> tree, lazy;

    void init(int n_) {
        n = n_;
        tree.assign(4 * n + 4, 0);
        lazy.assign(4 * n + 4, 0);
    }

    void build(int p, int l, int r, const vector<ll>& a) {
        if (l == r) {
            tree[p] = a[l];
            return;
        }
        int mid = (l + r) / 2;
        build(p * 2, l, mid, a);
        build(p * 2 + 1, mid + 1, r, a);
        tree[p] = tree[p * 2] + tree[p * 2 + 1];
    }

    void build(const vector<ll>& a) {
        init((int)a.size() - 1);
        build(1, 1, n, a);
    }

    void apply(int p, int l, int r, ll val) {
        tree[p] += val * (r - l + 1);
        lazy[p] += val;
    }

    void push(int p, int l, int r) {
        if (lazy[p] == 0 || l == r) return;
        int mid = (l + r) / 2;
        apply(p * 2, l, mid, lazy[p]);
        apply(p * 2 + 1, mid + 1, r, lazy[p]);
        lazy[p] = 0;
    }

    void range_add(int p, int l, int r, int ql, int qr, ll val) {
        if (qr < l || r < ql) return;
        if (ql <= l && r <= qr) {
            apply(p, l, r, val);
            return;
        }
        push(p, l, r);
        int mid = (l + r) / 2;
        range_add(p * 2, l, mid, ql, qr, val);
        range_add(p * 2 + 1, mid + 1, r, ql, qr, val);
        tree[p] = tree[p * 2] + tree[p * 2 + 1];
    }

    ll query(int p, int l, int r, int ql, int qr) {
        if (qr < l || r < ql) return 0;
        if (ql <= l && r <= qr) return tree[p];
        push(p, l, r);
        int mid = (l + r) / 2;
        return query(p * 2, l, mid, ql, qr) + query(p * 2 + 1, mid + 1, r, ql, qr);
    }

    void range_add(int l, int r, ll val) {
        range_add(1, 1, n, l, r, val);
    }

    ll query(int l, int r) {
        return query(1, 1, n, l, r);
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, q;
    cin >> n >> q;
    vector<ll> a(n + 1);
    for (int i = 1; i <= n; i++) cin >> a[i];

    SegTree seg;
    seg.build(a);

    while (q--) {
        char op;
        int l, r;
        cin >> op >> l >> r;
        if (op == 'A') {
            ll x;
            cin >> x;
            seg.range_add(l, r, x);
        } else {
            cout << seg.query(l, r) << '\n';
        }
    }
    return 0;
}
