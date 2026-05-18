#include <bits/stdc++.h>
using namespace std;


int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<pair<int,int>> a(n + 1);
    for (int i = 1; i <= n; i++) cin >> a[i].first >> a[i].second;
    sort(a.begin() + 1, a.end(), [](auto x, auto y) {
        return x.second < y.second;
    });
    int points = 0, last = -2000000000;
    for (int i = 1; i <= n; i++) {
        if (last < a[i].first) {
            last = a[i].second;
            points++;
        }
    }
    cout << points << '\n';
    return 0;
}
