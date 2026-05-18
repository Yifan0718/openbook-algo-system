#include <bits/stdc++.h>
using namespace std;
using ll = long long;

ll gcd_ll(ll a, ll b) {
    while (b) {
        ll t = a % b;
        a = b;
        b = t;
    }
    return a >= 0 ? a : -a;
}

ll lcm_limit(ll a, ll b, ll limit) {
    ll g = gcd_ll(a, b);
    __int128 aa = a / g;
    __int128 bb = b;
    if (aa > (__int128)limit / bb) return limit + 1;
    return (ll)(aa * bb);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    ll n;
    int m;
    cin >> n >> m;
    vector<ll> d(m + 1);
    for (int i = 1; i <= m; i++) cin >> d[i];
    __int128 ans = 0;
    for (int mask = 1; mask < (1 << m); mask++) {
        ll l = 1;
        int bits = 0;
        bool over = false;
        for (int i = 1; i <= m; i++) {
            if (mask >> (i - 1) & 1) {
                bits++;
                l = lcm_limit(l, d[i], n);
                if (l > n) {
                    over = true;
                    break;
                }
            }
        }
        if (over) continue;
        if (bits & 1) ans += n / l;
        else ans -= n / l;
    }
    cout << (long long)ans << '\n';
    return 0;
}
