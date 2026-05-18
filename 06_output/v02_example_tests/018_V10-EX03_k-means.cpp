#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, k, iter;
    cin >> n >> k >> iter;
    vector<double> x(n + 1), center(k + 1);
    for (int i = 1; i <= n; i++) cin >> x[i];
    for (int i = 1; i <= k; i++) center[i] = x[i];
    vector<int> label(n + 1, 1);
    for (int it = 1; it <= iter; it++) {
        for (int i = 1; i <= n; i++) {
            int best = 1;
            double best_dist = fabs(x[i] - center[1]);
            for (int c = 2; c <= k; c++) {
                double cur = fabs(x[i] - center[c]);
                if (cur < best_dist - 1e-12) {
                    best_dist = cur;
                    best = c;
                }
            }
            label[i] = best;
        }
        vector<double> sum(k + 1, 0);
        vector<int> cnt(k + 1, 0);
        for (int i = 1; i <= n; i++) {
            sum[label[i]] += x[i];
            cnt[label[i]]++;
        }
        for (int c = 1; c <= k; c++) if (cnt[c]) center[c] = sum[c] / cnt[c];
    }
    for (int i = 1; i <= n; i++) {
        if (i > 1) cout << ' ';
        cout << label[i];
    }
    cout << '\n' << fixed << setprecision(6);
    for (int c = 1; c <= k; c++) {
        if (c > 1) cout << ' ';
        cout << center[c];
    }
    cout << '\n';
    return 0;
}
