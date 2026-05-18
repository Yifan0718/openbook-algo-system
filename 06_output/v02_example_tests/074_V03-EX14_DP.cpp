#include <bits/stdc++.h>
using namespace std;

string digits;
long long memo[25][11][2];
bool visited[25][11][2];

long long dfs(int pos, int prev, bool tight, bool started) {
    int len = (int)digits.size() - 1;
    if (pos > len) {
        return started ? 1 : 0;
    }
    int prev_index = prev + 1;
    if (!tight && visited[pos][prev_index][started ? 1 : 0]) {
        return memo[pos][prev_index][started ? 1 : 0];
    }

    int limit = tight ? digits[pos] - '0' : 9;
    long long ways = 0;
    for (int d = 0; d <= limit; d++) {
        bool next_tight = tight && (d == limit);
        if (!started && d == 0) {
            ways += dfs(pos + 1, -1, next_tight, false);
        } else {
            if (started && d == prev) continue;
            ways += dfs(pos + 1, d, next_tight, true);
        }
    }

    if (!tight) {
        visited[pos][prev_index][started ? 1 : 0] = true;
        memo[pos][prev_index][started ? 1 : 0] = ways;
    }
    return ways;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string n;
    cin >> n;
    digits = " " + n;
    cout << dfs(1, -1, true, false) << '\n';
    return 0;
}
