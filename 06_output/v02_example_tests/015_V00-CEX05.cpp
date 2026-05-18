#include <bits/stdc++.h>
using namespace std;


int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int p, s;
    cin >> p >> s;
    vector<int> best(p + 1, -1);
    for (int i = 1; i <= s; i++) {
        int id, score;
        cin >> id >> score;
        best[id] = max(best[id], score);
    }
    int total = 0;
    for (int i = 1; i <= p; i++) total += max(0, best[i]);
    cout << total << '\n';
    return 0;
}
