#include <bits/stdc++.h>
using namespace std;


int n;
vector<int> a;
long long best = (long long)4e18;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cin >> n;
    a.assign(n + 1, 0);
    for (int i = 1; i <= n; i++) cin >> a[i];
    vector<int> p(n);
    iota(p.begin(), p.end(), 1);
    do {
        long long cost = 0;
        for (int i = 1; i < n; i++) cost += abs(a[p[i]] - a[p[i - 1]]);
        best = min(best, cost);
    } while (next_permutation(p.begin(), p.end()));
    cout << best << '\n';
    return 0;
}
