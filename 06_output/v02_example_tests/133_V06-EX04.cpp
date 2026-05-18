#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int N, q;
    cin >> N >> q;
    vector<int> spf(N + 1), primes, pref(N + 1);
    for (int i = 2; i <= N; i++) {
        if (spf[i] == 0) {
            spf[i] = i;
            primes.push_back(i);
        }
        for (int p : primes) {
            if (p > spf[i] || 1LL * i * p > N) break;
            spf[i * p] = p;
        }
    }
    for (int i = 1; i <= N; i++) pref[i] = pref[i - 1] + (spf[i] == i);

    while (q--) {
        int x;
        cin >> x;
        x = max(0, min(x, N));
        cout << pref[x] << '\n';
    }
    return 0;
}
