#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Mat {
    ll a[2][2]{};
};

Mat mul(const Mat &A, const Mat &B, ll mod) {
    Mat C;
    for (int i = 0; i < 2; i++) {
        for (int k = 0; k < 2; k++) {
            for (int j = 0; j < 2; j++) {
                C.a[i][j] = (C.a[i][j] + (__int128)A.a[i][k] * B.a[k][j]) % mod;
            }
        }
    }
    return C;
}

Mat mpow(Mat A, long long e, ll mod) {
    Mat R;
    R.a[0][0] = R.a[1][1] = 1 % mod;
    while (e > 0) {
        if (e & 1) R = mul(R, A, mod);
        A = mul(A, A, mod);
        e >>= 1;
    }
    return R;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    long long n;
    ll mod;
    cin >> n >> mod;
    if (n == 0) {
        cout << 0 << '\n';
        return 0;
    }
    Mat T;
    T.a[0][0] = 1 % mod;
    T.a[0][1] = 1 % mod;
    T.a[1][0] = 1 % mod;
    Mat P = mpow(T, n - 1, mod);
    cout << P.a[0][0] % mod << '\n';
    return 0;
}
