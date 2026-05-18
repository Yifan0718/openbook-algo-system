#include <bits/stdc++.h>
using namespace std;

using ll = long long;

struct BIT {
    int n = 0;
    vector<ll> bit;

    void init(int n_) {
        n = n_;
        bit.assign(n + 1, 0);
    }

    void add(int pos, ll val) {
        for (; pos <= n; pos += pos & -pos) bit[pos] += val;
    }

    ll prefix(int pos) {
        ll res = 0;
        for (; pos > 0; pos -= pos & -pos) res += bit[pos];
        return res;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<ll> a(n + 1), xs;
    xs.reserve(n);
    for (int i = 1; i <= n; i++) {
        cin >> a[i];
        xs.push_back(a[i]);
    }

    sort(xs.begin(), xs.end());
    xs.erase(unique(xs.begin(), xs.end()), xs.end());

    BIT fw;
    fw.init((int)xs.size());
    ll ans = 0;
    for (int i = 1; i <= n; i++) {
        int id = (int)(lower_bound(xs.begin(), xs.end(), a[i]) - xs.begin()) + 1;
        ll previous = i - 1;
        ll not_greater = fw.prefix(id);
        ans += previous - not_greater;
        fw.add(id, 1);
    }

    cout << ans << '\n';
    return 0;
}
