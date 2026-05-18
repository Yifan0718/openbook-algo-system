#include <bits/stdc++.h>
using namespace std;
using ll = long long;

ll gcd_ll(ll a, ll b) {
    if (a < 0) a = -a;
    if (b < 0) b = -b;
    while (b) {
        ll t = a % b;
        a = b;
        b = t;
    }
    return a;
}

ll lcm_limit(ll a, ll b, ll limit) {
    if (a == 0 || b == 0) return 0;
    __int128 aa = a, bb = b;
    if (aa < 0) aa = -aa;
    if (bb < 0) bb = -bb;
    ll g = gcd_ll(a, b);
    aa /= g;
    if (aa > (__int128)limit / bb) return limit + 1;
    __int128 res = aa * bb;
    return res > limit ? limit + 1 : (ll)res;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    ll limit;
    cin >> n >> limit;
    vector<ll> a(n + 1);
    ll g = 0, l = 1;
    bool over = false;
    for (int i = 1; i <= n; i++) {
        cin >> a[i];
        g = gcd_ll(g, a[i]);
        if (!over) {
            l = lcm_limit(l, a[i], limit);
            if (l > limit) over = true;
        }
    }
    cout << g << '\n';
    if (over) cout << "OVER\n";
    else cout << l << '\n';
    return 0;
}
