#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    cin.ignore(numeric_limits<streamsize>::max(), '\n');

    vector<string> line(n + 1);
    for (int i = 1; i <= n; i++) {
        getline(cin, line[i]);
    }

    for (int i = 1; i <= n; i++) {
        stringstream ss(line[i]);
        string word;
        int words = 0;
        while (ss >> word) words++;
        cout << i << ' ' << line[i].size() << ' ' << words << '\n';
    }
    return 0;
}
