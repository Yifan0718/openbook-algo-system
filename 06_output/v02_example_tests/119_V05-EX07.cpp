#include <bits/stdc++.h>
using namespace std;

using ll = long long;

struct Edge {
    int u, v;
    ll w;
};

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

    bool unite(int a, int b) {
        a = find(a);
        b = find(b);
        if (a == b) return false;
        if (sz[a] < sz[b]) swap(a, b);
        fa[b] = a;
        sz[a] += sz[b];
        return true;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;
    vector<Edge> edges(m);
    for (int i = 0; i < m; i++) cin >> edges[i].u >> edges[i].v >> edges[i].w;

    sort(edges.begin(), edges.end(), [](const Edge& a, const Edge& b) {
        return a.w < b.w;
    });

    DSU dsu;
    dsu.init(n);
    ll total = 0;
    int used = 0;
    for (auto e : edges) {
        if (dsu.unite(e.u, e.v)) {
            total += e.w;
            used++;
        }
    }

    if (used != n - 1) cout << "orz\n";
    else cout << total << '\n';
    return 0;
}
