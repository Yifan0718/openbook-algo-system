#include <bits/stdc++.h>
using namespace std;
using ll = long long;

vector<pair<ll, int>> factorize(ll x) {
    vector<pair<ll, int>> res;
    for (ll d = 2; d <= x / d; d += (d == 2 ? 1 : 2)) {
        if (x % d == 0) {
            int c = 0;
            while (x % d == 0) {
                x /= d;
                c++;
            }
            res.push_back({d, c});
        }
    }
    if (x > 1) res.push_back({x, 1});
    return res;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int q;
    cin >> q;
    while (q--) {
        ll x;
        cin >> x;
        auto f = factorize(x);
        if (f.empty()) {
            cout << "1\n1\n";
            continue;
        }
        ll cnt = 1;
        for (int i = 0; i < (int)f.size(); i++) {
            if (i) cout << ' ';
            cout << f[i].first << '^' << f[i].second;
            cnt *= f[i].second + 1;
        }
        cout << '\n' << cnt << '\n';
    }
    return 0;
}
