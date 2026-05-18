#include <bits/stdc++.h>
using namespace std;

long long exactSmall(const vector<long long> &a, int n, long long C) {
    long long best = 0;
    int totalMask = 1 << n;
    for (int mask = 0; mask < totalMask; mask++) {
        long long sum = 0;
        for (int i = 1; i <= n; i++) {
            if (mask & (1 << (i - 1))) {
                sum += a[i];
            }
        }
        if (sum <= C) best = max(best, sum);
    }
    return best;
}

long long fallbackLarge(const vector<long long> &a, int n, long long C) {
    long long sum = 0;
    for (int i = 1; i <= n; i++) {
        if (sum + a[i] <= C) {
            sum += a[i];
        }
    }
    return sum;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    long long C;
    cin >> n >> C;
    vector<long long> a(n + 1);
    for (int i = 1; i <= n; i++) cin >> a[i];

    if (n <= 20) {
        cout << exactSmall(a, n, C) << '\n';
    } else {
        cout << fallbackLarge(a, n, C) << '\n';
    }
    return 0;
}
