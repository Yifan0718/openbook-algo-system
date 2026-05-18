#include <bits/stdc++.h>
using namespace std;

int mex_value(const vector<int> &v) {
    vector<int> seen(v.size() + 5, 0);
    for (int x : v) if (0 <= x && x < (int)seen.size()) seen[x] = 1;
    for (int i = 0; ; i++) if (!seen[i]) return i;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N, m;
    cin >> N >> m;
    vector<int> moves(m + 1);
    for (int i = 1; i <= m; i++) cin >> moves[i];
    vector<int> sg(N + 1, 0);
    for (int x = 1; x <= N; x++) {
        vector<int> next_values;
        for (int i = 1; i <= m; i++) {
            if (moves[i] > 0 && x >= moves[i]) next_values.push_back(sg[x - moves[i]]);
        }
        sg[x] = mex_value(next_values);
    }
    cout << (sg[N] ? "WIN\n" : "LOSE\n");
    return 0;
}
