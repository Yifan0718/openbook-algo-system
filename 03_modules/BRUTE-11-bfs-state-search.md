# BRUTE-11：BFS 状态搜索

模块编号：BRUTE-11

模块名称：BFS 状态搜索

标签：BFS、最少步数、状态图、去重

一句话用途：当每一步代价相同、要求最少操作次数时，把局面当作状态，用 BFS 按层扩展。

题面触发词：

- 最少几步。
- 最少操作次数。
- 每次可以做若干种操作。
- 从初始状态变到目标状态。
- 状态数量不大。

适用场景：

- 字符串变换。
- 小拼图、小迷宫、开锁。
- 图上附带额外状态，例如位置 + 钥匙集合。
- 每条边权都是 1。

什么时候用：

- 目标是最少步数。
- 每次操作代价相同。
- 状态可以编码并去重。

不要什么时候用：

- 边权不等，应该用 Dijkstra。
- 状态转移有负权或收益，不是最短步数。
- 状态数量不可控。
- DFS + memo 适合求最优值，但 BFS 更适合最短层数。

复杂度：

- 时间：`O(状态数 * 每状态转移数)`。
- 空间：`O(状态数)`。

数据范围参考：

- 网格 `n*m` 可控时可用。
- `位置 * mask` 通常要求关键点数 `<= 20`。
- 字符串状态若排列长度 `<= 9` 可尝试。

依赖的标准容器：

- `queue`
- `unordered_map`
- `map`
- `vector`
- `string`

输入如何整理：

- 先定义状态，例如 `(x, y, mask)`。
- 能用整数编码就用整数；复杂状态先用 `string` 或 `tuple`。
- 用 `dist` 记录是否访问和步数。

接口：

```cpp
int bfs(State start, State target);
```

输出能力：

- 最少步数。
- 是否可达。
- 可通过 `pre` 数组还原路径。

下游可接：

- 图论卷 BFS / Dijkstra。
- BRUTE-10 unordered_map 编码 memo。
- 状压 DP。

可拼接模块：

- BRUTE-01 复杂度速查。
- BRUTE-05 子集枚举。
- DP-16 状压 DP。
- GRAPH-02 BFS。

模板代码：

```cpp
#include <bits/stdc++.h>
using namespace std;

struct State {
    int x, y, mask;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;
    vector<string> grid(n + 1);
    for (int i = 1; i <= n; i++) {
        string row;
        cin >> row;
        grid[i] = " " + row; // grid[i][1..m]
    }

    int sx = 1, sy = 1, tx = 1, ty = 1;
    bool hasS = false, hasT = false;
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            if (grid[i][j] == 'S') sx = i, sy = j, hasS = true;
            if (grid[i][j] == 'T') tx = i, ty = j, hasT = true;
        }
    }
    if (!hasS || !hasT) {
        cout << -1 << '\n';
        return 0;
    }

    vector<vector<int>> dist(n + 1, vector<int>(m + 1, -1));
    queue<pair<int, int>> q;
    q.push({sx, sy});
    dist[sx][sy] = 0;

    int dx[4] = {1, -1, 0, 0};
    int dy[4] = {0, 0, 1, -1};

    while (!q.empty()) {
        auto [x, y] = q.front();
        q.pop();
        for (int dir = 0; dir < 4; dir++) {
            int nx = x + dx[dir];
            int ny = y + dy[dir];
            if (nx < 1 || nx > n || ny < 1 || ny > m) continue;
            if (grid[nx][ny] == '#') continue;
            if (dist[nx][ny] != -1) continue;
            dist[nx][ny] = dist[x][y] + 1;
            q.push({nx, ny});
        }
    }

    cout << dist[tx][ty] << '\n';
    return 0;
}
```

调用示例：

```cpp
queue<State> q;
dist[start_key] = 0;
q.push(start);
while (!q.empty()) {
    State s = q.front();
    q.pop();
    // enumerate next states
}
```

## 真正的状态 BFS：网格 + 钥匙 mask

题面常见：网格里有钥匙 `a,b,c` 和门 `A,B,C`，拿到对应钥匙才能过门。状态必须是 `(x,y,mask)`，因为同一个格子，拿过哪些钥匙会影响后面能走哪些门。

```cpp
#include <bits/stdc++.h>
using namespace std;

struct State {
    int x;
    int y;
    int mask;
};

int shortest_path_with_keys(vector<string>& grid, int n, int m) {
    const int KMAX = 10;
    const int SMAX = 1 << KMAX;
    static int dist[105][105][SMAX];
    if (n <= 0 || n > 104 || m <= 0 || m > 104) return -1;

    int sx = 1, sy = 1, tx = 1, ty = 1;
    bool hasS = false, hasT = false;
    int key_id[26];
    fill(key_id, key_id + 26, -1);
    int key_count = 0;
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            char c = grid[i][j];
            if (c == 'S') sx = i, sy = j, hasS = true;
            if (c == 'T') tx = i, ty = j, hasT = true;
            if ('a' <= c && c <= 'z' && key_id[c - 'a'] == -1) {
                key_id[c - 'a'] = key_count++;
            }
        }
    }

    if (!hasS || !hasT) return -1;
    if (key_count > KMAX) return -1; // 状态太多，本模板只拿小数据/常见钥匙数
    int full = 1 << key_count;
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            for (int mask = 0; mask < full; mask++) dist[i][j][mask] = -1;
        }
    }
    queue<State> q;

    dist[sx][sy][0] = 0;
    q.push({sx, sy, 0});

    int dx[4] = {1, -1, 0, 0};
    int dy[4] = {0, 0, 1, -1};

    while (!q.empty()) {
        State cur = q.front();
        q.pop();

        if (cur.x == tx && cur.y == ty) {
            return dist[cur.x][cur.y][cur.mask];
        }

        for (int dir = 0; dir < 4; dir++) {
            int nx = cur.x + dx[dir];
            int ny = cur.y + dy[dir];
            int nmask = cur.mask;

            if (nx < 1 || nx > n || ny < 1 || ny > m) continue;
            char c = grid[nx][ny];
            if (c == '#') continue;

            if ('A' <= c && c <= 'Z' && c != 'S' && c != 'T') {
                int need = key_id[c - 'A'];
                if (need == -1) continue;
                if (((cur.mask >> need) & 1) == 0) continue;
            }

            if ('a' <= c && c <= 'z') {
                nmask |= 1 << key_id[c - 'a'];
            }

            if (dist[nx][ny][nmask] != -1) continue;
            dist[nx][ny][nmask] = dist[cur.x][cur.y][cur.mask] + 1;
            q.push({nx, ny, nmask});
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
    for (int i = 1; i <= n; i++) {
        string row;
        cin >> row;
        grid[i] = " " + row; // grid[i][1..m]
    }

    cout << shortest_path_with_keys(grid, n, m) << '\n';
    return 0;
}
```

如果钥匙种类太多，`n*m*2^key_count` 会爆，只能拿小数据或换思路。

常见坑：

- 入队时不标记访问，导致同一状态重复入队。
- BFS 只适用于等权最短路，不适合边权不同。
- 状态编码漏掉 `mask`、方向、剩余资源等字段。
- 网格坐标越界。
- 目标可能不可达，要输出题目要求的无解值。
- 看到同一个 `(x,y)` 但钥匙不同，不能共用一个 `dist[x][y]`。

暴力/部分分替代：

- 状态很复杂：先用 `map<tuple,...>` 或 `unordered_map<string,int>` 去重。
- 只会普通网格：先写无附加状态版本。
- 边权不同：先做小数据 BFS，后续升级 Dijkstra。

升级方向：

- BFS -> 双向 BFS。
- BFS -> Dijkstra。
- BFS 状态 `(pos, mask)` -> 状压 DP。
- 普通网格 BFS -> `dist[x][y][mask]` 状态 BFS。

最小测试样例：

```text
输入：
3 3
S..
.#.
..T

输出：
4
```
