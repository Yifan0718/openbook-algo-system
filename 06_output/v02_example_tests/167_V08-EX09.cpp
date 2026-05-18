#include <bits/stdc++.h>
using namespace std;
using ll = long long;

ll floor_div(ll a, ll b) {
    __int128 aa = a, bb = b;
    __int128 q = aa / bb, r = aa % bb;
    if (r != 0 && ((r > 0) != (bb > 0))) q--;
    return (ll)q;
}

ll ceil_div(ll a, ll b) {
    __int128 aa = a, bb = b;
    __int128 q = aa / bb, r = aa % bb;
    if (r != 0 && ((r > 0) == (bb > 0))) q++;
    return (ll)q;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int q;
    cin >> q;
    while (q--) {
        ll a, b;
        cin >> a >> b;
        cout << floor_div(a, b) << ' ' << ceil_div(a, b) << '\n';
    }
    return 0;
}
