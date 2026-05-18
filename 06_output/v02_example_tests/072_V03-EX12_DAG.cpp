#include <bits/stdc++.h>
using namespace std;

struct Edge {
    int to;
    long long weight;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;
    vector<vector<Edge>> graph_edges(n + 1);
    vector<int> indegree(n + 1, 0);
    for (int i = 1; i <= m; i++) {
        int u, v;
        long long w;
        cin >> u >> v >> w;
        graph_edges[u].push_back({v, w});
        indegree[v]++;
    }

    queue<int> q;
    for (int i = 1; i <= n; i++) {
        if (indegree[i] == 0) q.push(i);
    }

    vector<long long> dp(n + 1, 0);
    long long answer = 0;
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        answer = max(answer, dp[u]);
        for (const Edge& edge : graph_edges[u]) {
            int v = edge.to;
            dp[v] = max(dp[v], dp[u] + edge.weight);
            indegree[v]--;
            if (indegree[v] == 0) q.push(v);
        }
    }

    cout << answer << '\n';
    return 0;
}
