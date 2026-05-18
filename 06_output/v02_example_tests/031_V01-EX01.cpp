#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<int> score(n + 1);
    long long sum = 0;
    int best = 0;
    for (int i = 1; i <= n; i++) {
        cin >> score[i];
        sum += score[i];
        best = max(best, score[i]);
    }

    double avg = 1.0 * sum / n;
    cout << "sum=" << sum << '\n';
    cout << fixed << setprecision(2) << "average=" << avg << '\n';
    cout << "max=" << best << '\n';
    return 0;
}
