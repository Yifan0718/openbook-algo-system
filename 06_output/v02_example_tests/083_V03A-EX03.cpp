#include <bits/stdc++.h>
using namespace std;

struct Seg {
    long long l;
    long long r;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<Seg> seg(n + 1);
    for (int i = 1; i <= n; i++) cin >> seg[i].l >> seg[i].r;

    sort(seg.begin() + 1, seg.end(), [](const Seg &a, const Seg &b) {
        if (a.r != b.r) return a.r < b.r;
        return a.l < b.l;
    });

    vector<long long> points;
    long long lastPoint = -(1LL << 60);
    for (int i = 1; i <= n; i++) {
        if (lastPoint < seg[i].l) {
            lastPoint = seg[i].r;
            points.push_back(lastPoint);
        }
    }

    cout << points.size() << '\n';
    for (int i = 0; i < (int)points.size(); i++) {
        if (i) cout << ' ';
        cout << points[i];
    }
    cout << '\n';
    return 0;
}
