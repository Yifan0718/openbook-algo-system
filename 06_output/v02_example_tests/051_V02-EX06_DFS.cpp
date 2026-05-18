#include <bits/stdc++.h>
using namespace std;

int n;
long long C;
vector<long long> w, suffixSum;
long long best = 0;

void dfs(int idx, long long cur) {
    if (cur > C) return;
    if (idx == n + 1) {
        best = max(best, cur);
        return;
    }
    if (cur + suffixSum[idx] <= best) return;

    dfs(idx + 1, cur + w[idx]);
    dfs(idx + 1, cur);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n >> C;
    w.assign(n + 1, 0);
    for (int i = 1; i <= n; i++) cin >> w[i];
    sort(w.begin() + 1, w.end(), greater<long long>());

    suffixSum.assign(n + 2, 0);
    for (int i = n; i >= 1; i--) {
        suffixSum[i] = suffixSum[i + 1] + w[i];
    }

    dfs(1, 0);
    cout << best << '\n';
    return 0;
}
