#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct BIT {
    int n;
    vector<int> bit;

    void init(int n_) {
        n = n_;
        bit.assign(n + 1, 0);
    }

    void add(int pos, int delta) {
        for (int i = pos; i <= n; i += i & -i) bit[i] += delta;
    }

    int prefix(int pos) const {
        int res = 0;
        for (int i = pos; i > 0; i -= i & -i) res += bit[i];
        return res;
    }
};

struct Operation {
    char type;
    ll x;
    ll y;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int q;
    cin >> q;
    vector<Operation> ops(q + 1);
    vector<ll> coords;
    for (int i = 1; i <= q; i++) {
        cin >> ops[i].type >> ops[i].x;
        if (ops[i].type == 'A') {
            ops[i].y = 0;
            coords.push_back(ops[i].x);
        } else {
            cin >> ops[i].y;
        }
    }
    sort(coords.begin(), coords.end());
    coords.erase(unique(coords.begin(), coords.end()), coords.end());

    BIT fw;
    fw.init((int)coords.size());
    for (int i = 1; i <= q; i++) {
        if (ops[i].type == 'A') {
            int id = int(lower_bound(coords.begin(), coords.end(), ops[i].x) - coords.begin()) + 1;
            fw.add(id, 1);
        } else {
            int right = int(upper_bound(coords.begin(), coords.end(), ops[i].y) - coords.begin());
            int left = int(lower_bound(coords.begin(), coords.end(), ops[i].x) - coords.begin());
            cout << fw.prefix(right) - fw.prefix(left) << '\n';
        }
    }
    return 0;
}
