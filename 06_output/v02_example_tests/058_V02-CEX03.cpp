#include <bits/stdc++.h>
using namespace std;


int n, target;
vector<int> a;
map<pair<int,int>, long long> memo;
long long dfs(int i, int sum) {
    if (i == n + 1) return sum == target;
    auto key = make_pair(i, sum);
    if (memo.count(key)) return memo[key];
    long long ans = dfs(i + 1, sum + a[i]) + dfs(i + 1, sum - a[i]);
    return memo[key] = ans;
}
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cin >> n >> target;
    a.assign(n + 1, 0);
    for (int i = 1; i <= n; i++) cin >> a[i];
    cout << dfs(1, 0) << '\n';
    return 0;
}
