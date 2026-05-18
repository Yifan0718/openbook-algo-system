# CPP-004 queue/deque/stack/priority_queue

模块编号：CPP-004

模块名称：队列、双端队列、栈与优先队列

标签：queue、deque、stack、priority_queue、BFS、单调队列、堆

一句话用途：处理先进先出、后进先出、两端进出和“每次取最大/最小”的场景。

题面触发词：BFS、层数、最短步数、撤销、括号匹配、滑动窗口、每次取最大、每次取最小、合并代价、Dijkstra。

什么时候用：需要固定顺序弹出元素，或需要反复取得当前最大/最小元素时。

不要什么时候用：需要按任意值删除堆中元素时，普通 `priority_queue` 不支持；需要有序遍历所有元素时用 `set/map`。

复杂度：`queue/deque/stack` 常用操作 `O(1)`；`priority_queue` 插入/弹出 `O(log n)`，取堆顶 `O(1)`。

数据范围参考：BFS 状态数 `<= 1e6` 常见；堆操作 `<= 2e5` 到 `1e6` 通常可用。

依赖的标准容器：`queue`、`deque`、`stack`、`priority_queue`、`vector`、`pair`。

输入如何整理：图/状态转移整理成可扩展的邻接表或候选状态；堆元素常存 `(距离, 点)`、`(权值, 编号)`。

接口：

- `q.push(x) / q.front() / q.pop() / q.empty()`。
- `dq.push_front(x) / dq.push_back(x) / dq.front() / dq.back()`。
- `st.push(x) / st.top() / st.pop()`。
- 最大堆：`priority_queue<int> pq`。
- 最小堆：`priority_queue<T, vector<T>, greater<T>> pq`。

输出能力：输出 BFS 距离、处理顺序、当前最大/最小值、括号是否合法等。

下游可接：图论 BFS/Dijkstra、单调队列优化 DP、贪心、模拟。

可拼接模块：CPP-002 基础容器、CPP-003 排序二分、CPP-008 整数溢出。

模板代码：

```cpp
#include <bits/stdc++.h>
using namespace std;

using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    priority_queue<int> max_heap;
    priority_queue<int, vector<int>, greater<int>> min_heap;

    int n;
    cin >> n;
    if (n <= 0) return 0;
    for (int i = 1; i <= n; i++) {
        int x;
        cin >> x;
        max_heap.push(x);
        min_heap.push(x);
    }

    cout << max_heap.top() << ' ' << min_heap.top() << '\n';

    queue<int> q;
    vector<int> dist(n + 1, -1);
    q.push(1);
    dist[1] = 0;
    while (!q.empty()) {
        int u = q.front();
        q.pop();

        int v = u + 1;
        if (v <= n && dist[v] == -1) {
            dist[v] = dist[u] + 1;
            q.push(v);
        }
    }

    cout << dist[n] << '\n';

    return 0;
}
```

调用示例：

```cpp
// Dijkstra 常用最小堆元素：{当前距离, 点}
priority_queue<pair<ll, int>, vector<pair<ll, int>>, greater<pair<ll, int>>> pq;
pq.push({0, 1});
while (!pq.empty()) {
    auto [d, u] = pq.top();
    pq.pop();
}

// 栈：括号匹配
stack<char> st;
bool ok = true;
for (char c : s) {
    if (c == '(') st.push(c);
    else if (c == ')') {
        if (st.empty()) ok = false;
        else st.pop();
    }
}
bool balanced = ok && st.empty();
```

常见坑：

- `front/top/back` 前必须确认容器非空，否则容易 RE。
- `priority_queue` 默认是最大堆。
- 最小堆写法里第二个模板参数必须是底层容器 `vector<T>`。
- 堆里旧状态不会自动删除，Dijkstra 常用 `if (d != dist[u]) continue;` 跳过旧元素。
- `stack` 只能看栈顶，不能遍历；需要遍历用 `vector`。
- `deque` 两端操作快，中间插入删除仍不适合大量使用。

暴力/部分分替代：数据小可以每次线性扫描找最小/最大，复杂度 `O(n^2)`；能过小数据后再换堆。

升级方向：BFS 接无权最短路；最小堆接 Dijkstra；`deque` 接 0-1 BFS 或单调队列优化。

最小测试样例：

```text
输入
5
3 1 4 1 5

输出
5 1
4
```
