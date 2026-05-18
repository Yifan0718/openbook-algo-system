#include <bits/stdc++.h>
using namespace std;

vector<int> mobius(int n) {
    vector<int> mu(n + 1), primes, is_comp(n + 1);
    if (n >= 1) mu[1] = 1;
    for (int i = 2; i <= n; i++) {
        if (!is_comp[i]) {
            primes.push_back(i);
            mu[i] = -1;
        }
        for (int p : primes) {
            if (1LL * i * p > n) break;
            is_comp[i * p] = 1;
            if (i % p == 0) {
                mu[i * p] = 0;
                break;
            }
            mu[i * p] = -mu[i];
        }
    }
    return mu;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int A, B;
    cin >> A >> B;
    int n = min(A, B);
    vector<int> mu = mobius(n);
    long long ans = 0;
    for (int d = 1; d <= n; d++) ans += 1LL * mu[d] * (A / d) * (B / d);
    cout << ans << '\n';
    return 0;
}
