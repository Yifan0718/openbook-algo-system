#include <bits/stdc++.h>
using namespace std;

struct Task {
    string name;
    int priority;
    int time;
    int id;

    bool operator<(const Task &other) const {
        if (priority != other.priority) return priority < other.priority;
        if (time != other.time) return time > other.time;
        return id > other.id;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    priority_queue<Task> pq;
    for (int i = 1; i <= n; i++) {
        Task t;
        cin >> t.name >> t.priority >> t.time;
        t.id = i;
        pq.push(t);
    }

    while (!pq.empty()) {
        Task t = pq.top();
        pq.pop();
        cout << t.name << ' ' << t.priority << ' ' << t.time << '\n';
    }
    return 0;
}
