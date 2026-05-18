#include <bits/stdc++.h>
using namespace std;

using ll = long long;
const ll INF = (1LL << 60);
const int MAXN = 505;

ll dista[MAXN][MAXN];

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m, q;
    cin >> n >> m >> q;
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++) {
            dista[i][j] = (i == j ? 0 : INF);
        }
    }

    for (int i = 1; i <= m; i++) {
        int u, v;
        ll w;
        cin >> u >> v >> w;
        dista[u][v] = min(dista[u][v], w);
    }

    for (int k = 1; k <= n; k++) {
        for (int i = 1; i <= n; i++) {
            if (dista[i][k] == INF) continue;
            for (int j = 1; j <= n; j++) {
                if (dista[k][j] == INF) continue;
                dista[i][j] = min(dista[i][j], dista[i][k] + dista[k][j]);
            }
        }
    }

    while (q--) {
        int s, t;
        cin >> s >> t;
        cout << (dista[s][t] == INF ? -1 : dista[s][t]) << '\n';
    }
    return 0;
}
