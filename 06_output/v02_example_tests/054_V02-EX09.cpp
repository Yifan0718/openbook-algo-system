#include <bits/stdc++.h>
using namespace std;

void genSums(const vector<long long> &a, int l, int r, long long C, vector<long long> &sums) {
    int len = r - l + 1;
    int totalMask = 1 << len;
    for (int mask = 0; mask < totalMask; mask++) {
        long long sum = 0;
        for (int i = 0; i < len; i++) {
            if (mask & (1 << i)) {
                sum += a[l + i];
            }
        }
        if (sum <= C) sums.push_back(sum);
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    long long C;
    cin >> n >> C;
    vector<long long> a(n + 1);
    for (int i = 1; i <= n; i++) cin >> a[i];

    int mid = n / 2;
    vector<long long> leftSums, rightSums;
    genSums(a, 1, mid, C, leftSums);
    genSums(a, mid + 1, n, C, rightSums);

    sort(rightSums.begin(), rightSums.end());
    long long ans = 0;
    for (long long x : leftSums) {
        long long remain = C - x;
        auto it = upper_bound(rightSums.begin(), rightSums.end(), remain);
        if (it == rightSums.begin()) {
            ans = max(ans, x);
        } else {
            --it;
            ans = max(ans, x + *it);
        }
    }

    cout << ans << '\n';
    return 0;
}
