#include <bits/stdc++.h>
using namespace std;


int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<pair<int,int>> a(n + 1);
    for (int i = 1; i <= n; i++) cin >> a[i].second >> a[i].first;
    sort(a.begin() + 1, a.end());
    int cnt = 0, last = -2000000000;
    for (int i = 1; i <= n; i++) if (a[i].second >= last) {
        cnt++;
        last = a[i].first;
    }
    cout << cnt << '\n';
    return 0;
}
