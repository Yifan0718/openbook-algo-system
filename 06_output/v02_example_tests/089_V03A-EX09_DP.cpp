#include <bits/stdc++.h>
using namespace std;

struct Job {
    long long l;
    long long r;
    long long w;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<Job> job(n + 1);
    for (int i = 1; i <= n; i++) cin >> job[i].l >> job[i].r >> job[i].w;

    sort(job.begin() + 1, job.end(), [](const Job &a, const Job &b) {
        if (a.r != b.r) return a.r < b.r;
        return a.l < b.l;
    });

    vector<long long> ends(n + 1, 0);
    for (int i = 1; i <= n; i++) ends[i] = job[i].r;

    vector<long long> dp(n + 1, 0);
    for (int i = 1; i <= n; i++) {
        int p = int(upper_bound(ends.begin() + 1, ends.begin() + i, job[i].l) - ends.begin()) - 1;
        dp[i] = max(dp[i - 1], dp[p] + job[i].w);
    }

    cout << dp[n] << '\n';
    return 0;
}
