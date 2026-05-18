#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    unordered_map<string, string> phone;
    phone.reserve(n * 2 + 10);
    phone.max_load_factor(0.7);

    for (int i = 1; i <= n; i++) {
        string name, number;
        cin >> name >> number;
        phone[name] = number;
    }

    int q;
    cin >> q;
    for (int i = 1; i <= q; i++) {
        string name;
        cin >> name;
        auto it = phone.find(name);
        if (it == phone.end()) {
            cout << "NOT FOUND\n";
        } else {
            cout << it->second << '\n';
        }
    }
    return 0;
}
