#include <bits/stdc++.h>
using namespace std;


int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, k;
    cin >> n >> k;
    unordered_map<string, int> cnt;
    cnt.reserve(n * 2 + 10);
    for (int i = 1; i <= n; i++) {
        string s;
        cin >> s;
        cnt[s]++;
    }
    priority_queue<pair<int,string>> pq;
    for (auto [s, c] : cnt) pq.push({c, s});
    for (int i = 1; i <= k && !pq.empty(); i++) {
        auto [c, s] = pq.top(); pq.pop();
        cout << s << ' ' << c << '\n';
    }
    return 0;
}
