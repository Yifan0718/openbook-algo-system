#include <bits/stdc++.h>
using namespace std;


long long memo[20][2][2][200];
vector<int> digits;
long long dfs(int pos, int tight, int started, int sum) {
    if (pos == (int)digits.size()) return started && sum % 3 == 0;
    long long &res = memo[pos][tight][started][sum];
    if (!tight && res != -1) return res;
    long long ans = 0;
    int lim = tight ? digits[pos] : 9;
    for (int d = 0; d <= lim; d++) {
        ans += dfs(pos + 1, tight && d == lim, started || d != 0, sum + (started || d != 0 ? d : 0));
    }
    if (!tight) res = ans;
    return ans;
}
long long solve(long long x) {
    if (x <= 0) return 0;
    digits.clear();
    string s = to_string(x);
    for (char c : s) digits.push_back(c - '0');
    memset(memo, -1, sizeof(memo));
    return dfs(0, 1, 0, 0);
}
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    long long L, R;
    cin >> L >> R;
    cout << solve(R) - solve(L - 1) << '\n';
    return 0;
}
