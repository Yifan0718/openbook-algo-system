# AI-09 强化学习、MDP 与值迭代

模块编号：AI-09

模块名称：状态、动作、奖励、策略与 Value Iteration

标签：AI、强化学习、MDP、状态、动作、奖励、策略、值迭代、C++17

一句话用途：当题目出现状态、动作、奖励、折扣因子、最优策略时，把它看成图上的 DP：`V[s] = max_a(reward + gamma * V[next])`。

题面触发词：

- 状态、动作、奖励、策略。
- 折扣因子 gamma。
- value、Q value、value iteration。
- grid world、智能体每步获得 reward。

什么时候用：

- 状态和动作数量明确，转移规则给定。
- 题目要求迭代固定轮数或直到收敛。
- 转移是确定性的或概率转移可枚举。

不要什么时候用：

- 不要把 RL 想复杂；机考大概率是按公式模拟。
- 如果是普通最短路/最长路，直接图算法更清晰。
- gamma 接近 1 且有正环时，值可能不断变大，题面应给迭代次数或终止状态。

复杂度：

- 确定性 value iteration：`O(iter * states * actions)`。
- 概率转移：`O(iter * states * actions * next_states)`。

依赖的标准容器：

- `vector<vector<int>> next_state`
- `vector<vector<double>> reward`
- `vector<double> V`

输入如何整理：

```cpp
int n, m, iter;
double gamma;
cin >> n >> m >> iter >> gamma;
```

接口：

```text
next_state[s][a]：状态 s 执行动作 a 后到达的状态。
reward[s][a]：该动作即时奖励。
V[s]：状态价值。
```

模板代码：

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m, iter;
    double gamma;
    cin >> n >> m >> iter >> gamma;

    vector<vector<int>> nxt(n + 1, vector<int>(m + 1));
    vector<vector<double>> reward(n + 1, vector<double>(m + 1));
    for (int s = 1; s <= n; s++) {
        for (int a = 1; a <= m; a++) {
            cin >> nxt[s][a] >> reward[s][a];
        }
    }

    vector<double> V(n + 1, 0);
    for (int it = 1; it <= iter; it++) {
        vector<double> nV(n + 1, 0);
        for (int s = 1; s <= n; s++) {
            nV[s] = reward[s][1] + gamma * V[nxt[s][1]];
            for (int a = 2; a <= m; a++) {
                nV[s] = max(nV[s], reward[s][a] + gamma * V[nxt[s][a]]);
            }
        }
        V = nV;
    }

    cout << fixed << setprecision(6);
    for (int s = 1; s <= n; s++) {
        if (s > 1) cout << ' ';
        cout << V[s];
    }
    cout << '\n';

    return 0;
}
```

## Q-learning 路由

如果题面给经验序列 `(s,a,r,next)` 和学习率 `alpha`：

```text
Q[s][a] = Q[s][a] + alpha * (r + gamma * max Q[next][*] - Q[s][a])
```

这就是按公式模拟，不需要理解复杂理论。

调用示例：

```cpp
// 固定 iter 轮 value iteration 后输出 V[1..n]。
```

常见坑：

- value iteration 每一轮要用上一轮 V 更新新 V，不要原地更新，除非题目要求。
- gamma 是 double，输出精度按题面。
- 状态编号、动作编号按题面，资料默认 1-index。
- 终止状态通常所有动作回到自己、奖励 0，或题面单独说明。
- Q-learning 是在线更新，value iteration 是整轮同步更新。

暴力/部分分替代：

- 不会 value iteration：先模拟给定策略，不取 max。
- 不会概率转移：先处理确定性转移子任务。
- 不会收敛判断：按固定迭代次数输出。

最小测试样例：

```text
输入
3 2 3 1.0
2 0 3 1
3 5 1 0
3 0 3 0

输出
5.000000 5.000000 0.000000
```

