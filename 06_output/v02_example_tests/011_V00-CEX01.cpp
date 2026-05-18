#include <bits/stdc++.h>
using namespace std;


int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    long long n, m;
    string feature;
    while (cin >> n >> m >> feature) {
        if (feature == "unweighted_graph") cout << "GRAPH-02 BFS\n";
        else if (feature == "weighted_nonnegative") cout << "GRAPH-03 Dijkstra\n";
        else if (feature == "range_sum_static") cout << "DS-01 PrefixSum\n";
        else if (feature == "range_update") cout << "DS-01 Difference\n";
        else if (n <= 20 && feature == "subset") cout << "BRUTE-02 Bitmask\n";
        else if (feature == "capacity") cout << "DP-06 Knapsack\n";
        else cout << "ROUTE-00 Read constraints again\n";
    }
    return 0;
}
