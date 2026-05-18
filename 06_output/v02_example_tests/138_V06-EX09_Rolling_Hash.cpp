#include <bits/stdc++.h>
using namespace std;
using ull = unsigned long long;

struct RollingHash {
    static const ull BASE = 1315423911ULL;
    vector<ull> h, pw;

    void build(const string &s) {
        int n = (int)s.size();
        h.assign(n + 1, 0);
        pw.assign(n + 1, 1);
        for (int i = 0; i < n; i++) {
            h[i + 1] = h[i] * BASE + (unsigned char)s[i] + 1;
            pw[i + 1] = pw[i] * BASE;
        }
    }

    ull get(int l, int r) const {
        return h[r + 1] - h[l] * pw[r - l + 1];
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string s;
    cin >> s;
    RollingHash rh;
    rh.build(s);
    int q;
    cin >> q;
    while (q--) {
        int l1, r1, l2, r2;
        cin >> l1 >> r1 >> l2 >> r2;
        --l1; --r1; --l2; --r2;
        if (r1 - l1 != r2 - l2) cout << "NO\n";
        else cout << (rh.get(l1, r1) == rh.get(l2, r2) ? "YES\n" : "NO\n");
    }
    return 0;
}
