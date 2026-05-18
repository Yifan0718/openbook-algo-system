#include <bits/stdc++.h>
using namespace std;


int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    cin >> n >> q;
    vector<long long> diff(n + 3, 0);
    for (int i = 1; i <= q; i++) {
        int l, r;
        long long v;
        cin >> l >> r >> v;
        diff[l] += v;
        diff[r + 1] -= v;
    }
    long long cur = 0, mx = LLONG_MIN;
    int pos = 1;
    for (int i = 1; i <= n; i++) {
        cur += diff[i];
        if (cur > mx) {
            mx = cur;
            pos = i;
        }
    }
    cout << pos << ' ' << mx << '\n';
    return 0;
}
