#include <bits/stdc++.h>
using namespace std;

bool match(char left, char right) {
    return (left == '(' && right == ')') ||
           (left == '[' && right == ']') ||
           (left == '{' && right == '}');
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;
    while (T--) {
        string s;
        cin >> s;
        stack<char> st;
        bool ok = true;
        for (char c : s) {
            if (c == '(' || c == '[' || c == '{') {
                st.push(c);
            } else {
                if (st.empty() || !match(st.top(), c)) {
                    ok = false;
                    break;
                }
                st.pop();
            }
        }
        if (!st.empty()) ok = false;
        cout << (ok ? "YES" : "NO") << '\n';
    }
    return 0;
}
