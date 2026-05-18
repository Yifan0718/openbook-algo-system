#include <bits/stdc++.h>
using namespace std;


int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    cout << fixed << setprecision(2);
    for (int i = 1; i <= n; i++) {
        string name;
        double a, b;
        cin >> name >> a >> b;
        cout << setw(10) << left << name << right << setw(8) << a + b << '\n';
    }
    return 0;
}
