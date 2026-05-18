#include <bits/stdc++.h>
using namespace std;

struct Version {
    int id;
    int score;
    int risk;
    int time_need;
};

bool better(const Version &a, const Version &b) {
    if (a.score != b.score) return a.score > b.score;
    if (a.risk != b.risk) return a.risk < b.risk;
    if (a.time_need != b.time_need) return a.time_need < b.time_need;
    return a.id < b.id;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int k, R, M;
    cin >> k >> R >> M;
    bool has = false;
    Version best{0, 0, 0, 0};
    for (int i = 1; i <= k; i++) {
        Version cur;
        cur.id = i;
        cin >> cur.score >> cur.risk >> cur.time_need;
        if (cur.risk > R || cur.time_need > M) continue;
        if (!has || better(cur, best)) {
            best = cur;
            has = true;
        }
    }

    if (!has) {
        cout << "HOLD\n";
    } else {
        cout << best.id << ' ' << best.score << '\n';
    }
    return 0;
}
