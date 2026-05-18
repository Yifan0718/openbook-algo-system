#include <bits/stdc++.h>
using namespace std;

int n, k;
long long target;
vector<long long> a;
long long ans = 0;

void dfs(int start, int chosen, long long sum) {
    if (chosen == k) {
        if (sum == target) ans++;
        return;
    }
    if (start > n) return;
    int need = k - chosen;
    if (n - start + 1 < need) return;

    for (int i = start; i <= n; i++) {
        dfs(i + 1, chosen + 1, sum + a[i]);
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n >> k >> target;
    a.assign(n + 1, 0);
    for (int i = 1; i <= n; i++) cin >> a[i];

    dfs(1, 0, 0);
    cout << ans << '\n';
    return 0;
}
