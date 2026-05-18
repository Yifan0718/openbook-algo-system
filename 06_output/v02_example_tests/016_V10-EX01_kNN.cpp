#include <bits/stdc++.h>
using namespace std;

struct Sample {
    vector<double> x;
    int label;
};

double dist2(const vector<double> &a, const vector<double> &b, int d) {
    double s = 0;
    for (int i = 1; i <= d; i++) {
        double t = a[i] - b[i];
        s += t * t;
    }
    return s;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, q, d, k;
    cin >> n >> q >> d >> k;
    vector<Sample> train(n + 1);
    for (int i = 1; i <= n; i++) {
        train[i].x.assign(d + 1, 0);
        for (int j = 1; j <= d; j++) cin >> train[i].x[j];
        cin >> train[i].label;
    }
    while (q--) {
        vector<double> x(d + 1);
        for (int j = 1; j <= d; j++) cin >> x[j];
        vector<pair<double, int>> near;
        for (int i = 1; i <= n; i++) near.push_back({dist2(train[i].x, x, d), train[i].label});
        sort(near.begin(), near.end());
        map<int, int> vote;
        for (int i = 0; i < min(k, (int)near.size()); i++) vote[near[i].second]++;
        int best_label = -1, best_cnt = -1;
        for (auto [lab, cnt] : vote) {
            if (cnt > best_cnt || (cnt == best_cnt && lab < best_label)) {
                best_cnt = cnt;
                best_label = lab;
            }
        }
        cout << best_label << '\n';
    }
    return 0;
}
