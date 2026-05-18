#include <bits/stdc++.h>
using namespace std;

struct Tarjan {
    int n = 0;
    int timer = 0;
    vector<vector<int>> g;
    vector<int> dfn, low, inStack, st, compSize;

    void init(int n_) {
        n = n_;
        g.assign(n + 1, {});
        dfn.assign(n + 1, 0);
        low.assign(n + 1, 0);
        inStack.assign(n + 1, 0);
        st.clear();
        compSize.clear();
        timer = 0;
    }

    void add_edge(int u, int v) {
        g[u].push_back(v);
    }

    void dfs(int u) {
        dfn[u] = low[u] = ++timer;
        st.push_back(u);
        inStack[u] = 1;
        for (int v : g[u]) {
            if (!dfn[v]) {
                dfs(v);
                low[u] = min(low[u], low[v]);
            } else if (inStack[v]) {
                low[u] = min(low[u], dfn[v]);
            }
        }
        if (low[u] == dfn[u]) {
            int cnt = 0;
            while (true) {
                int x = st.back();
                st.pop_back();
                inStack[x] = 0;
                cnt++;
                if (x == u) break;
            }
            compSize.push_back(cnt);
        }
    }

    vector<int> run() {
        for (int i = 1; i <= n; i++) {
            if (!dfn[i]) dfs(i);
        }
        sort(compSize.begin(), compSize.end());
        return compSize;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;
    Tarjan solver;
    solver.init(n);
    for (int i = 1; i <= m; i++) {
        int u, v;
        cin >> u >> v;
        solver.add_edge(u, v);
    }

    vector<int> sizes = solver.run();
    cout << sizes.size() << '\n';
    for (int i = 0; i < (int)sizes.size(); i++) {
        if (i) cout << ' ';
        cout << sizes[i];
    }
    cout << '\n';
    return 0;
}
