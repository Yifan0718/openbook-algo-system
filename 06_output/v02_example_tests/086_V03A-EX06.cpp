#include <bits/stdc++.h>
using namespace std;

struct Course {
    long long t;
    long long d;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<Course> c(n + 1);
    for (int i = 1; i <= n; i++) cin >> c[i].t >> c[i].d;

    sort(c.begin() + 1, c.end(), [](const Course &a, const Course &b) {
        if (a.d != b.d) return a.d < b.d;
        return a.t < b.t;
    });

    priority_queue<long long> chosen;
    long long total = 0;
    for (int i = 1; i <= n; i++) {
        total += c[i].t;
        chosen.push(c[i].t);
        if (total > c[i].d) {
            total -= chosen.top();
            chosen.pop();
        }
    }

    cout << chosen.size() << '\n';
    return 0;
}
