#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    double x, y, w1, b1, w2, b2, lr;
    cin >> x >> y >> w1 >> b1 >> w2 >> b2 >> lr;
    double z1 = w1 * x + b1;
    double a1 = max(0.0, z1);
    double yhat = w2 * a1 + b2;
    double dz2 = yhat - y;
    double dw2 = dz2 * a1;
    double db2 = dz2;
    double da1 = dz2 * w2;
    double dz1 = z1 > 0 ? da1 : 0.0;
    double dw1 = dz1 * x;
    double db1 = dz1;
    w1 -= lr * dw1;
    b1 -= lr * db1;
    w2 -= lr * dw2;
    b2 -= lr * db2;
    cout << fixed << setprecision(6) << w1 << ' ' << b1 << ' ' << w2 << ' ' << b2 << '\n';
    return 0;
}
