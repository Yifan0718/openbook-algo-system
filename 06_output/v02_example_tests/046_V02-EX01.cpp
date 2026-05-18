#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<vector<long long>> w(n + 1, vector<long long>(n + 1));
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++) {
            cin >> w[i][j];
        }
    }

    vector<int> p(n + 1);
    for (int i = 1; i <= n; i++) p[i] = i;

    long long best = (1LL << 62);
    vector<int> bestPath;
    do {
        long long cost = 0;
        for (int i = 1; i < n; i++) {
            cost += w[p[i]][p[i + 1]];
        }
        vector<int> cur(p.begin() + 1, p.end());
        if (cost < best || (cost == best && cur < bestPath)) {
            best = cost;
            bestPath = cur;
        }
    } while (next_permutation(p.begin() + 1, p.end()));

    cout << best << '\n';
    for (int i = 0; i < n; i++) {
        if (i) cout << ' ';
        cout << bestPath[i];
    }
    cout << '\n';
    return 0;
}
