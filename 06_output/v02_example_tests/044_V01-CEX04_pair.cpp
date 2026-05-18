#include <bits/stdc++.h>
using namespace std;


int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<pair<int,int>> seg(n + 1);
    for (int i = 1; i <= n; i++) cin >> seg[i].first >> seg[i].second;
    sort(seg.begin() + 1, seg.end());
    vector<pair<int,int>> ans;
    for (int i = 1; i <= n; i++) {
        if (ans.empty() || seg[i].first > ans.back().second) ans.push_back(seg[i]);
        else ans.back().second = max(ans.back().second, seg[i].second);
    }
    cout << ans.size() << '\n';
    for (auto [l, r] : ans) cout << l << ' ' << r << '\n';
    return 0;
}
