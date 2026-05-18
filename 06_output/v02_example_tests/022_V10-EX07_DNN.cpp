#include <bits/stdc++.h>
using namespace std;

void activate(vector<double> &a, const string &act) {
    int n = (int)a.size() - 1;
    if (act == "relu") {
        for (int i = 1; i <= n; i++) a[i] = max(0.0, a[i]);
    } else if (act == "softmax") {
        double mx = a[1];
        for (int i = 2; i <= n; i++) mx = max(mx, a[i]);
        double sum = 0;
        for (int i = 1; i <= n; i++) {
            a[i] = exp(a[i] - mx);
            sum += a[i];
        }
        for (int i = 1; i <= n; i++) a[i] /= sum;
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int L, d;
    cin >> L >> d;
    vector<double> cur(d + 1);
    for (int i = 1; i <= d; i++) cin >> cur[i];
    for (int layer = 1; layer <= L; layer++) {
        int out;
        string act;
        cin >> out >> act;
        vector<double> nxt(out + 1, 0);
        for (int i = 1; i <= out; i++) {
            for (int j = 1; j <= d; j++) {
                double w;
                cin >> w;
                nxt[i] += w * cur[j];
            }
            double b;
            cin >> b;
            nxt[i] += b;
        }
        activate(nxt, act);
        cur = nxt;
        d = out;
    }
    int pred = 1;
    for (int i = 2; i <= d; i++) if (cur[i] > cur[pred] + 1e-12) pred = i;
    cout << pred << '\n' << fixed << setprecision(6);
    for (int i = 1; i <= d; i++) {
        if (i > 1) cout << ' ';
        cout << cur[i];
    }
    cout << '\n';
    return 0;
}
