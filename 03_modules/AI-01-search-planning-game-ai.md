# AI-01 启发式搜索、路径规划与博弈 AI

模块编号：AI-01

模块名称：A* 路径规划、启发式搜索与 Minimax 思想

标签：AI、A*、启发式搜索、路径规划、游戏 AI、Minimax、Alpha-Beta、C++17

一句话用途：AI 背景中的“机器人找路”和“游戏最优策略”通常就是图搜索和博弈搜索，本模块给出可直接抄的 A* 网格模板和 minimax 路由。

题面触发词：

- 机器人、智能体、地图、起点、终点、障碍、路径规划。
- 启发式函数、估价函数、曼哈顿距离。
- 游戏 AI、双方轮流、当前玩家、最优行动。
- 搜索树、剪枝、估值函数。

什么时候用：

- 网格每步代价相同或非负，且有明确目标点。
- 需要比普通 BFS/Dijkstra 更像 AI 路径规划的写法。
- 博弈题状态规模小，可以搜索到终局或限定深度。

不要什么时候用：

- 无权最短路普通 BFS 已足够时，不要为了 AI 背景硬写 A*。
- 启发式可能高估真实距离时，A* 不保证最短路。
- 博弈状态大且有明显 DP 结构时，优先状态 DP/记忆化。
- 有负边权最短路不要用 A* 或 Dijkstra。

复杂度：

- A* 最坏仍可能访问大量状态，通常不超过 Dijkstra 数量级。
- 网格 A* 每个格子入堆若干次，常写成 `O(n*m*log(n*m))`。
- Minimax 不剪枝约 `O(b^d)`，`b` 是分支数，`d` 是搜索深度。

依赖的标准容器：

- `vector<string>`：1-index 网格。
- `priority_queue`：A* open set。
- `vector<vector<int>>`：距离数组。
- `map/unordered_map`：复杂状态记忆化。

输入如何整理：

```cpp
int n, m;
cin >> n >> m;
vector<string> grid(n + 1);
for (int i = 1; i <= n; i++) {
    string row;
    cin >> row;
    grid[i] = " " + row; // 1-index 列
}
```

接口：

```text
astar_grid(grid, n, m, sx, sy, tx, ty) -> 最短步数，不可达返回 -1。
启发式 h(x,y)=abs(x-tx)+abs(y-ty)。
```

模板代码：

```cpp
#include <bits/stdc++.h>
using namespace std;

struct State {
    int f;
    int g;
    int x;
    int y;
    bool operator<(const State &other) const {
        if (f != other.f) return f > other.f;
        return g > other.g;
    }
};

int astar_grid(const vector<string> &grid, int n, int m, int sx, int sy, int tx, int ty) {
    const int INF = 1e9;
    vector<vector<int>> dist(n + 1, vector<int>(m + 1, INF));
    priority_queue<State> pq;

    auto inside = [&](int x, int y) {
        return 1 <= x && x <= n && 1 <= y && y <= m && grid[x][y] != '#';
    };
    auto h = [&](int x, int y) {
        return abs(x - tx) + abs(y - ty);
    };

    dist[sx][sy] = 0;
    pq.push({h(sx, sy), 0, sx, sy});

    int dx[5] = {0, -1, 1, 0, 0};
    int dy[5] = {0, 0, 0, -1, 1};

    while (!pq.empty()) {
        State cur = pq.top();
        pq.pop();
        if (cur.g != dist[cur.x][cur.y]) continue;
        if (cur.x == tx && cur.y == ty) return cur.g;

        for (int dir = 1; dir <= 4; dir++) {
            int nx = cur.x + dx[dir];
            int ny = cur.y + dy[dir];
            if (!inside(nx, ny)) continue;
            int ng = cur.g + 1;
            if (ng < dist[nx][ny]) {
                dist[nx][ny] = ng;
                pq.push({ng + h(nx, ny), ng, nx, ny});
            }
        }
    }

    return -1;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;
    vector<string> grid(n + 1);
    int sx = -1, sy = -1, tx = -1, ty = -1;

    for (int i = 1; i <= n; i++) {
        string row;
        cin >> row;
        grid[i] = " " + row;
        for (int j = 1; j <= m; j++) {
            if (grid[i][j] == 'S') {
                sx = i;
                sy = j;
            } else if (grid[i][j] == 'T') {
                tx = i;
                ty = j;
            }
        }
    }

    if (sx == -1 || tx == -1) {
        cout << -1 << '\n';
        return 0;
    }

    cout << astar_grid(grid, n, m, sx, sy, tx, ty) << '\n';
    return 0;
}
```

## Minimax / Alpha-Beta 怎么接

概念骨架：

```text
score(state, player):
    如果终局，返回当前局面对“我方”的分数
    如果轮到我方，取所有后继的最大分
    如果轮到对方，取所有后继的最小分
```

能加速的地方：

- 终局判断。
- 估价函数：深度到头时用局面评分。
- Alpha-Beta：当前分支已经不可能更优就剪掉。
- 记忆化：同一个状态和当前玩家不重复算。

调用示例：

```cpp
// 网格路径规划：
// int ans = astar_grid(grid, n, m, sx, sy, tx, ty);
```

常见坑：

- A* 的 `f = g + h`，`g` 是已走代价，`h` 是估计剩余代价。
- 曼哈顿距离适合四方向无障碍估计；有障碍也不高估，仍可用。
- 如果每步代价不同，`g` 要加真实边权，`h` 也不能高估。
- 如果 `h=0`，A* 退化成 Dijkstra。
- 博弈题要明确评分是从谁的视角。
- 记忆化 key 必须包含当前玩家/轮次，否则会错。

暴力/部分分替代：

- A* 不会写：无权先 BFS，非负权先 Dijkstra。
- 启发式不会设计：令 `h=0`，至少正确。
- Minimax 不会剪枝：先 DFS 限深。
- 状态重复多：加 `map<state,int>` 记忆化。
- 对局太大：只搜索小深度，用估价函数拿部分分。

最小测试样例：

```text
输入
3 4
S..#
.#..
...T

输出
5
```

