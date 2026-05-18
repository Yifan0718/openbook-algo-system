#include <bits/stdc++.h>
using namespace std;

const long long INF = 4'000'000'000'000'000'000LL;
int n;
vector<long long> cost_value;
vector<long long> memo;

long long dfs(int i) {
    if (i == 0) return 0;
    if (i < 0) return INF;
    if (memo[i] != -1) return memo[i];
    long long best = min(dfs(i - 1), dfs(i - 2));
    memo[i] = best + cost_value[i];
    return memo[i];
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n;
    cost_value.assign(n + 1, 0);
    memo.assign(n + 1, -1);
    for (int i = 1; i <= n; i++) {
        cin >> cost_value[i];
    }
    cout << dfs(n) << '\n';
    return 0;
}
