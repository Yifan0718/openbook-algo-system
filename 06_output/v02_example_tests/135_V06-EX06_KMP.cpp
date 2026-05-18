#include <bits/stdc++.h>
using namespace std;

vector<int> prefix_function(const string &s) {
    int n = (int)s.size();
    vector<int> pi(n, 0);
    for (int i = 1; i < n; i++) {
        int j = pi[i - 1];
        while (j > 0 && s[i] != s[j]) j = pi[j - 1];
        if (s[i] == s[j]) j++;
        pi[i] = j;
    }
    return pi;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string text, pat;
    cin >> text >> pat;
    string s = pat + char(1) + text;
    vector<int> pi = prefix_function(s);
    int m = (int)pat.size();
    vector<int> ans;
    for (int i = m + 1; i < (int)s.size(); i++) {
        if (pi[i] == m) ans.push_back(i - 2 * m + 1);
    }
    if (ans.empty()) {
        cout << "NONE\n";
    } else {
        for (int i = 0; i < (int)ans.size(); i++) {
            if (i) cout << ' ';
            cout << ans[i];
        }
        cout << '\n';
    }
    return 0;
}
