#include <bits/stdc++.h>
using namespace std;


int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, T;
    cin >> n >> T;
    vector<pair<int,int>> jobs(n + 1);
    for (int i = 1; i <= n; i++) cin >> jobs[i].first >> jobs[i].second;
    sort(jobs.begin() + 1, jobs.end());
    priority_queue<int, vector<int>, greater<int>> pq;
    long long sum = 0;
    for (int i = 1; i <= n; i++) {
        pq.push(jobs[i].second);
        sum += jobs[i].second;
        if ((int)pq.size() > jobs[i].first) {
            sum -= pq.top();
            pq.pop();
        }
    }
    cout << sum << '\n';
    return 0;
}
