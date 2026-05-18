#include <bits/stdc++.h>
using namespace std;

struct Student {
    string name;
    int score;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<Student> a(n + 1);
    for (int i = 1; i <= n; i++) {
        cin >> a[i].name >> a[i].score;
    }

    sort(a.begin() + 1, a.end(), [](const Student &lhs, const Student &rhs) {
        if (lhs.score != rhs.score) return lhs.score > rhs.score;
        return lhs.name < rhs.name;
    });

    for (int i = 1; i <= n; i++) {
        cout << i << ' ' << a[i].name << ' ' << a[i].score << '\n';
    }
    return 0;
}
