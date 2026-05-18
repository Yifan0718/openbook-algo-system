#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    set<int> values;
    for (int i = 1; i <= n; i++) {
        int x;
        cin >> x;
        values.insert(x);
    }

    cout << "count=" << values.size() << '\n';
    bool first = true;
    for (int x : values) {
        if (!first) cout << ' ';
        first = false;
        cout << x;
    }
    cout << '\n';
    return 0;
}
