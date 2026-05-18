#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string s_raw, p_raw;
    cin >> s_raw >> p_raw;
    string s = " " + s_raw;
    string p = " " + p_raw;
    int n = (int)s_raw.size();
    int m = (int)p_raw.size();

    vector<int> pi(m + 1, 0);
    for (int i = 2; i <= m; i++) {
        int j = pi[i - 1];
        while (j > 0 && p[i] != p[j + 1]) j = pi[j];
        if (p[i] == p[j + 1]) j++;
        pi[i] = j;
    }

    int kmp_count = 0;
    int j = 0;
    for (int i = 1; i <= n; i++) {
        while (j > 0 && s[i] != p[j + 1]) j = pi[j];
        if (s[i] == p[j + 1]) j++;
        if (j == m) {
            kmp_count++;
            j = pi[j];
        }
    }

    int brute_count = 0;
    for (int i = 1; i + m - 1 <= n; i++) {
        bool ok = true;
        for (int t = 1; t <= m; t++) {
            if (s[i + t - 1] != p[t]) ok = false;
        }
        if (ok) brute_count++;
    }

    if (kmp_count != brute_count) {
        cout << "CHECK_FAILED\n";
    } else {
        cout << kmp_count << '\n';
    }
    return 0;
}
