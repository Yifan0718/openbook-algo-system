#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int q;
    cin >> q;
    while (q--) {
        ll a, b, limit;
        cin >> a >> b >> limit;
        __int128 product = (__int128)a * b;
        cout << (product <= limit ? "YES" : "NO") << '\n';
    }
    return 0;
}
