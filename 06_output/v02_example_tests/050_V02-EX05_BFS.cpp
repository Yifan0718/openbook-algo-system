#include <bits/stdc++.h>
using namespace std;

int parseState(const string &s) {
    return (s[0] - '0') * 100 + (s[1] - '0') * 10 + (s[2] - '0');
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string targetStr;
    int m;
    cin >> targetStr >> m;

    vector<int> forbidden(1000, 0);
    for (int i = 1; i <= m; i++) {
        string s;
        cin >> s;
        forbidden[parseState(s)] = 1;
    }

    int start = 0;
    int target = parseState(targetStr);
    if (forbidden[start] || forbidden[target]) {
        cout << -1 << '\n';
        return 0;
    }

    vector<int> dist(1000, -1);
    queue<int> q;
    dist[start] = 0;
    q.push(start);

    int base[3] = {100, 10, 1};
    while (!q.empty()) {
        int cur = q.front();
        q.pop();
        if (cur == target) break;

        for (int pos = 0; pos < 3; pos++) {
            int digit = (cur / base[pos]) % 10;
            for (int delta : {-1, 1}) {
                int nd = (digit + delta + 10) % 10;
                int nxt = cur + (nd - digit) * base[pos];
                if (!forbidden[nxt] && dist[nxt] == -1) {
                    dist[nxt] = dist[cur] + 1;
                    q.push(nxt);
                }
            }
        }
    }

    cout << dist[target] << '\n';
    return 0;
}
