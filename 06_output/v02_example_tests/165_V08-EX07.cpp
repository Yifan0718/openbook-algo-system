#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Point {
    ll x, y;
};

Point operator-(Point a, Point b) {
    return {a.x - b.x, a.y - b.y};
}

__int128 cross(Point a, Point b) {
    return (__int128)a.x * b.y - (__int128)a.y * b.x;
}

__int128 cross(Point a, Point b, Point c) {
    return cross(b - a, c - a);
}

bool on_segment(Point a, Point b, Point p) {
    return cross(a, b, p) == 0 &&
           min(a.x, b.x) <= p.x && p.x <= max(a.x, b.x) &&
           min(a.y, b.y) <= p.y && p.y <= max(a.y, b.y);
}

void print_i128(__int128 x) {
    if (x == 0) {
        cout << 0;
        return;
    }
    if (x < 0) {
        cout << '-';
        x = -x;
    }
    string s;
    while (x > 0) {
        s.push_back(char('0' + x % 10));
        x /= 10;
    }
    reverse(s.begin(), s.end());
    cout << s;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<Point> p(n + 1);
    for (int i = 1; i <= n; i++) cin >> p[i].x >> p[i].y;
    Point A, B, P;
    cin >> A.x >> A.y >> B.x >> B.y >> P.x >> P.y;
    __int128 area2 = 0;
    for (int i = 1; i <= n; i++) area2 += cross(p[i], p[i == n ? 1 : i + 1]);
    if (area2 < 0) area2 = -area2;
    print_i128(area2);
    cout << '\n' << (on_segment(A, B, P) ? "YES\n" : "NO\n");
    return 0;
}
