#include <bits/stdc++.h>
using namespace std;
using ll = long long;

ll floor_div(ll a, ll b) {
    ll q = a / b, r = a % b;
    if (r != 0 && ((r > 0) != (b > 0))) q--;
    return q;
}

ll days_from_civil(ll y, int m, int d) {
    y -= m <= 2;
    ll era = floor_div(y, 400);
    unsigned yoe = (unsigned)(y - era * 400);
    unsigned mp = (unsigned)(m + (m > 2 ? -3 : 9));
    unsigned doy = (153 * mp + 2) / 5 + (unsigned)d - 1;
    unsigned doe = yoe * 365 + yoe / 4 - yoe / 100 + doy;
    return era * 146097 + (ll)doe - 719468;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    ll y1, y2;
    int m1, d1, m2, d2;
    cin >> y1 >> m1 >> d1 >> y2 >> m2 >> d2;
    cout << days_from_civil(y2, m2, d2) - days_from_civil(y1, m1, d1) << '\n';
    return 0;
}
