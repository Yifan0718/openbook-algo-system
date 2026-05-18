#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<long long> t(n + 1);
    for (int i = 1; i <= n; i++) cin >> t[i];
    sort(t.begin() + 1, t.end());

    long long elapsed = 0;
    long long ans = 0;
    for (int i = 1; i <= n; i++) {
        ans += elapsed;
        elapsed += t[i];
    }

    cout << ans << '\n';
    return 0;
}
