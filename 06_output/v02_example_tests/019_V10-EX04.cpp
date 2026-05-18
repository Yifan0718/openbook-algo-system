#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, epoch;
    double lr;
    cin >> n >> epoch >> lr;
    vector<double> x(n + 1), y(n + 1);
    for (int i = 1; i <= n; i++) cin >> x[i] >> y[i];
    double w = 0, b = 0;
    for (int ep = 1; ep <= epoch; ep++) {
        for (int i = 1; i <= n; i++) {
            double pred = w * x[i] + b;
            double err = pred - y[i];
            w -= lr * err * x[i];
            b -= lr * err;
        }
    }
    int q;
    cin >> q;
    cout << fixed << setprecision(6);
    while (q--) {
        double t;
        cin >> t;
        cout << w * t + b << '\n';
    }
    return 0;
}
