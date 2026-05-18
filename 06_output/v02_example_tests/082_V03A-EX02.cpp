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

    long long lastEnd = -(1LL << 60);
    int ans = 0;
    for (int i = 1; i <= n; i++) {
        if (seg[i].l >= lastEnd) {
            ans++;
            lastEnd = seg[i].r;
        }
    }

    cout << ans << '\n';
    return 0;
}
