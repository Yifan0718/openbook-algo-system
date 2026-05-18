#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, epoch;
    double lr;
    cin >> n >> epoch >> lr;
    vector<double> x1(n + 1), x2(n + 1);
    vector<int> y(n + 1);
    for (int i = 1; i <= n; i++) cin >> x1[i] >> x2[i] >> y[i];
    double w1 = 0, w2 = 0, b = 0;
    for (int ep = 1; ep <= epoch; ep++) {
        for (int i = 1; i <= n; i++) {
            double score = w1 * x1[i] + w2 * x2[i] + b;
            if (y[i] * score <= 0) {
                w1 += lr * y[i] * x1[i];
                w2 += lr * y[i] * x2[i];
                b += lr * y[i];
            }
        }
    }
    int q;
    cin >> q;
    while (q--) {
        double a, c;
        cin >> a >> c;
        double score = w1 * a + w2 * c + b;
        cout << (score >= 0 ? 1 : -1) << '\n';
    }
    return 0;
}
