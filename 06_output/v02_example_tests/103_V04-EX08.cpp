#include <bits/stdc++.h>
using namespace std;

struct DSU {
    vector<int> fa, sz;

    void init(int n) {
        fa.resize(n + 1);
        sz.assign(n + 1, 1);
        iota(fa.begin(), fa.end(), 0);
    }

    int find(int x) {
        while (x != fa[x]) {
            fa[x] = fa[fa[x]];
            x = fa[x];
        }
        return x;
    }

    void unite(int a, int b) {
        a = find(a);
        b = find(b);
        if (a == b) return;
        if (sz[a] < sz[b]) swap(a, b);
        fa[b] = a;
        sz[a] += sz[b];
    }

    bool same(int a, int b) {
        return find(a) == find(b);
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, q;
    cin >> n >> q;
    DSU dsu;
    dsu.init(n);

    while (q--) {
        char op;
        int a, b;
        cin >> op >> a >> b;
        if (op == 'U') {
            dsu.unite(a, b);
        } else {
            cout << (dsu.same(a, b) ? "Yes" : "No") << '\n';
        }
    }
    return 0;
}
