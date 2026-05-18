#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    map<string, int> cnt;
    string line;
    while (getline(cin, line)) {
        stringstream ss(line);
        string word;
        while (ss >> word) {
            cnt[word]++;
        }
    }

    for (const auto &kv : cnt) {
        cout << kv.first << ' ' << kv.second << '\n';
    }
    return 0;
}
