#include <bits/stdc++.h>
using namespace std;

struct Node {
    string op;
    int l = 0, r = 0;
    double val = 0, grad = 0;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<Node> a(n + 1);
    vector<int> vars;
    for (int i = 1; i <= n; i++) {
        cin >> a[i].op;
        if (a[i].op == "var" || a[i].op == "const") {
            cin >> a[i].val;
            if (a[i].op == "var") vars.push_back(i);
        } else if (a[i].op == "add" || a[i].op == "mul") {
            cin >> a[i].l >> a[i].r;
            if (a[i].op == "add") a[i].val = a[a[i].l].val + a[a[i].r].val;
            else a[i].val = a[a[i].l].val * a[a[i].r].val;
        } else if (a[i].op == "sin") {
            cin >> a[i].l;
            a[i].val = sin(a[a[i].l].val);
        }
    }
    a[n].grad = 1;
    for (int i = n; i >= 1; i--) {
        double g = a[i].grad;
        if (a[i].op == "add") {
            a[a[i].l].grad += g;
            a[a[i].r].grad += g;
        } else if (a[i].op == "mul") {
            int l = a[i].l, r = a[i].r;
            a[l].grad += g * a[r].val;
            a[r].grad += g * a[l].val;
        } else if (a[i].op == "sin") {
            int l = a[i].l;
            a[l].grad += g * cos(a[l].val);
        }
    }
    cout << fixed << setprecision(6) << a[n].val << '\n';
    for (int i = 0; i < (int)vars.size(); i++) {
        if (i) cout << ' ';
        cout << a[vars[i]].grad;
    }
    cout << '\n';
    return 0;
}
