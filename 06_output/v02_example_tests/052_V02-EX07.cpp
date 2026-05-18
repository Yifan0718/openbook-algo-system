#include <bits/stdc++.h>
using namespace std;

const int INF = 1000000000;

string s;
long long target;
int n;
vector<unordered_map<long long, int>> memo;

int dfs(int pos, long long sum) {
    if (sum > target) return INF;
    if (pos == n) {
        return sum == target ? 0 : INF;
    }
    if (memo[pos].count(sum)) return memo[pos][sum];

    long long val = 0;
    int best = INF;
    for (int nxt = pos; nxt < n; nxt++) {
        val = val * 10 + (s[nxt] - '0');
        if (sum + val > target) break;
        int add = (pos == 0 ? 0 : 1);
        best = min(best, add + dfs(nxt + 1, sum + val));
    }
    memo[pos][sum] = best;
    return best;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> s >> target;
    n = (int)s.size();
    memo.assign(n + 1, unordered_map<long long, int>());

    int ans = dfs(0, 0);
    cout << (ans >= INF ? -1 : ans) << '\n';
    return 0;
}
