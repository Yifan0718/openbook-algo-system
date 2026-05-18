#include <bits/stdc++.h>
using namespace std;

struct Item {
    int id;
    double price;
    int count;
};

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;

    vector<Item> item(n + 1);
    double total = 0.0;
    for (int i = 1; i <= n; i++) {
        if (scanf("%d%lf%d", &item[i].id, &item[i].price, &item[i].count) != 3) return 0;
    }

    for (int i = 1; i <= n; i++) {
        double subtotal = item[i].price * item[i].count;
        total += subtotal;
        printf("%04d %.2f\n", item[i].id, subtotal);
    }
    printf("TOTAL %.2f\n", total);
    return 0;
}
