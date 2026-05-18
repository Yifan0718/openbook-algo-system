#include <bits/stdc++.h>
using namespace std;


int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    cin.ignore(numeric_limits<streamsize>::max(), '\n');
    map<string, long long> sum;
    for (int i = 1; i <= n; i++) {
        string line;
        getline(cin, line);
        stringstream ss(line);
        string key;
        long long value;
        while (ss >> key >> value) sum[key] += value;
    }
    for (auto [k, v] : sum) cout << k << ' ' << v << '\n';
    return 0;
}
