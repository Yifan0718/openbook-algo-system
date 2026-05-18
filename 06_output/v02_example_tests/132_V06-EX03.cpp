#include <bits/stdc++.h>
using namespace std;
using ll = long long;

ll mod_pow(ll a, ll e, ll mod) {
    ll r = 1 % mod;
    a %= mod;
    if (a < 0) a += mod;
    while (e > 0) {
        if (e & 1) r = (ll)((__int128)r * a % mod);
        a = (ll)((__int128)a * a % mod);
        e >>= 1;
    }
    return r;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N, q;
    ll MOD;
    cin >> N >> MOD >> q;
    vector<ll> fac(N + 1), ifac(N + 1);
    fac[0] = 1;
    for (int i = 1; i <= N; i++) fac[i] = fac[i - 1] * i % MOD;
    ifac[N] = mod_pow(fac[N], MOD - 2, MOD);
    for (int i = N; i >= 1; i--) ifac[i - 1] = ifac[i] * i % MOD;

    while (q--) {
        int n, k;
        cin >> n >> k;
        if (n < 0 || n > N || k < 0 || k > n) {
            cout << 0 << '\n';
        } else {
            cout << fac[n] * ifac[k] % MOD * ifac[n - k] % MOD << '\n';
        }
    }
    return 0;
}
