#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, W;
    cin >> n >> W;
    vector<int> w(n + 1);
    vector<ll> v(n + 1);
    for (int i = 1; i <= n; i++) cin >> w[i] >> v[i];

    vector<ll> correct(W + 1, 0), forward_wrong(W + 1, 0);
    for (int i = 1; i <= n; i++) {
        for (int cap = W; cap >= w[i]; cap--) {
            correct[cap] = max(correct[cap], correct[cap - w[i]] + v[i]);
        }
        for (int cap = w[i]; cap <= W; cap++) {
            forward_wrong[cap] = max(forward_wrong[cap], forward_wrong[cap - w[i]] + v[i]);
        }
    }

    cout << correct[W] << '\n';
    cout << (correct[W] == forward_wrong[W] ? "SAME" : "LOOP_RISK") << '\n';
    return 0;
}
