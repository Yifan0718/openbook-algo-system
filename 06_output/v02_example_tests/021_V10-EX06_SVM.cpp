#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, epoch;
    double lr, lambda;
    cin >> n >> epoch >> lr >> lambda;
    vector<double> x(n + 1);
    vector<int> y(n + 1);
    for (int i = 1; i <= n; i++) cin >> x[i] >> y[i];
    double w = 0, b = 0;
    for (int ep = 1; ep <= epoch; ep++) {
        for (int i = 1; i <= n; i++) {
            double margin = y[i] * (w * x[i] + b);
            w -= lr * lambda * w;
            if (margin < 1.0) {
                w += lr * y[i] * x[i];
                b += lr * y[i];
            }
        }
    }
    int q;
    cin >> q;
    while (q--) {
        double t;
        cin >> t;
        cout << (w * t + b >= 0 ? 1 : -1) << '\n';
    }
    return 0;
}
