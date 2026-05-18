#include <bits/stdc++.h>
using namespace std;


struct State { int x, y, k; };
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<string> g(n + 1);
    for (int i = 1; i <= n; i++) { cin >> g[i]; g[i] = " " + g[i]; }
    vector<vector<array<int,2>>> dist(n + 1, vector<array<int,2>>(m + 1, { -1, -1 }));
    queue<State> q;
    dist[1][1][0] = 0;
    q.push({1, 1, 0});
    int dx[4] = {1, -1, 0, 0};
    int dy[4] = {0, 0, 1, -1};
    while (!q.empty()) {
        auto cur = q.front(); q.pop();
        for (int d = 0; d < 4; d++) {
            int nx = cur.x + dx[d], ny = cur.y + dy[d];
            if (nx < 1 || nx > n || ny < 1 || ny > m) continue;
            int nk = cur.k;
            if (g[nx][ny] == '#') {
                if (nk) continue;
                nk = 1;
            }
            if (dist[nx][ny][nk] == -1) {
                dist[nx][ny][nk] = dist[cur.x][cur.y][cur.k] + 1;
                q.push({nx, ny, nk});
            }
        }
    }
    int a = dist[n][m][0], b = dist[n][m][1];
    if (a == -1) cout << b << '\n';
    else if (b == -1) cout << a << '\n';
    else cout << min(a, b) << '\n';
    return 0;
}
