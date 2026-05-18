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

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    ll a, b, c, x, y;
    cin >> a >> b >> c;
    ll g = exgcd(a, b, x, y);
    if (c % g != 0) {
        cout << "NO\n";
    } else {
        x *= c / g;
        y *= c / g;
        cout << "YES\n" << x << ' ' << y << '\n';
    }
    return 0;
}
