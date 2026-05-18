#include <bits/stdc++.h>
using namespace std;
using ll = long long;

ll exgcd(ll a, ll b, ll &x, ll &y) {
    if (b == 0) {
        x = (a >= 0 ? 1 : -1);
        y = 0;
        return a >= 0 ? a : -a;
    }
    ll x1, y1;
    ll g = exgcd(b, a % b, x1, y1);
    x = y1;
    y = x1 - a / b * y1;
    return g;
}

ll norm(ll x, ll mod) {
    x %= mod;
    if (x < 0) x += mod;
    return x;
}

bool merge_crt(ll &r, ll &m, ll r2, ll m2) {
    ll x, y;
    ll g = exgcd(m, m2, x, y);
    __int128 diff = (__int128)r2 - r;
    if (diff % g != 0) return false;
    ll mod2 = m2 / g;
    ll k = (ll)((diff / g * x) % mod2);
    k = norm(k, mod2);
    __int128 nr = (__int128)r + (__int128)m * k;
    __int128 nm = (__int128)m / g * m2;
    if (nm > LLONG_MAX) return false;
    m = (ll)nm;
    r = (ll)(nr % nm);
    if (r < 0) r += m;
    return true;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int k;
    cin >> k;
    ll r, m;
    cin >> r >> m;
    r = norm(r, m);
    for (int i = 2; i <= k; i++) {
        ll r2, m2;
        cin >> r2 >> m2;
        if (!merge_crt(r, m, norm(r2, m2), m2)) {
            cout << "NO\n";
            return 0;
        }
    }
    cout << r << '\n';
    return 0;
}
