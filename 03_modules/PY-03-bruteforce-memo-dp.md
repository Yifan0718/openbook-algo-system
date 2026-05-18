# PY-03 Python 暴力、记忆化与 DP 原型

模块编号：PY-03

模块名称：Python 快速写暴力搜索、记忆化搜索和 DP

标签：Python、DFS、记忆化、lru_cache、DP、部分分、BFS、状态搜索

一句话用途：疑似 DP 或搜索题时，先用 Python 写最直白的 DFS/BFS，再用 `lru_cache` 或字典记忆化快速降低复杂度。

题面触发词：

- 每一步有若干选择，问最优值、可行性、方案数。
- `n` 小、状态复杂、需要先拿部分分。
- 状态由位置、和、上一个选择、mask、字符串等组成。
- 最短步数、迷宫、状态变化。
- C++ 写 hash 编码麻烦，Python tuple key 很自然。

什么时候用：

- 你能写出暴力递归，但暂时推不出表格式 DP。
- 递归深度不大，状态数量可控。
- 状态参数可以直接是整数、字符串、tuple。
- 小数据部分分非常明确。

不要什么时候用：

- 递归深度可能超过 `1e5`，Python 函数调用和栈风险很高。
- 状态数量巨大，`lru_cache` 会占用大量内存。
- 每个状态转移需要遍历很多对象，Python 常数可能 TLE。
- 已经有 C++ 稳模板能更快满分。

复杂度：

- 纯暴力：分支数的指数级。
- 记忆化：约等于 `状态数 * 每个状态转移代价`。
- BFS：`O(状态数 + 转移数)`。
- Python 里状态用 tuple 做 key，会有额外哈希常数。

依赖的标准容器：

- `functools.lru_cache`
- `collections.deque`
- `dict`
- `set`
- `tuple`
- `list`

输入如何整理：

```python
import sys
from functools import lru_cache

data = sys.stdin.buffer.read().split()
it = iter(data)
s = next(it).decode()
target = int(next(it))
```

接口：

```text
DFS 记忆化：
@lru_cache(None)
def dfs(可变状态参数):
    先写 base case
    再枚举选择
    return 答案

BFS：
deque + set/dict dist
```

## 记忆化搜索通用骨架

模板代码：

```python
from functools import lru_cache

INF = 10 ** 18

@lru_cache(None)
def dfs(i, state):
    if i == 0:
        return 0

    ans = INF
    # 枚举选择，把问题变成更小状态
    # ans = min(ans, dfs(i - 1, new_state) + cost)
    return ans
```

## 例 1：快速求和 P1874 的 Python 记忆化版

思路：

- 暴力是从左到右切数字。
- 状态写成 `dfs(pos, total)`：已经处理到字符串位置 `pos`，当前和是 `total`，后面最少还要多少个加号。
- 如果 `total > target`，直接无效。
- 每次枚举下一段数字 `s[pos:nxt]`。
- 第一次切出来的数字不需要加号；之后每多切一段需要 `+1`。为了简单，`dfs` 返回从当前状态到结束还需要的段数连接代价，在转移时用 `add = 0 if pos == 0 else 1`。

完整代码：

```python
import sys
from functools import lru_cache

INF = 10 ** 9

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    s = data[0].decode()
    target = int(data[1])
    n = len(s)

    @lru_cache(None)
    def dfs(pos, total):
        if total > target:
            return INF
        if pos == n:
            return 0 if total == target else INF

        ans = INF
        val = 0
        for nxt in range(pos + 1, n + 1):
            val = val * 10 + ord(s[nxt - 1]) - 48
            if total + val > target:
                break
            add = 0 if pos == 0 else 1
            ans = min(ans, add + dfs(nxt, total + val))
        return ans

    ans = dfs(0, 0)
    print(-1 if ans >= INF else ans)

if __name__ == "__main__":
    solve()
```

## 例 2：编辑距离的 Python 稳定版

思路：

- 状态 `dfs(i, j)`：把 `a[i:]` 变成 `b[j:]` 的最少操作数。
- 如果某个串空了，只能全部插入或删除。
- 末字符/首字符相等就跳过，否则三选一。
- Python 递归记忆化适合小数据推模型；`|a|,|b|` 到 2000 时，优先写滚动数组 DP，避免递归深度和 `lru_cache` 内存问题。

完整代码：

```python
import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if len(data) < 2:
        return
    a = data[0].decode()
    b = data[1].decode()
    n, m = len(a), len(b)

    prev = list(range(m + 1))
    for i in range(1, n + 1):
        cur = [0] * (m + 1)
        cur[0] = i
        ai = a[i - 1]
        for j in range(1, m + 1):
            cost = 0 if ai == b[j - 1] else 1
            cur[j] = min(
                prev[j] + 1,        # delete a[i]
                cur[j - 1] + 1,     # insert b[j]
                prev[j - 1] + cost  # replace or keep
            )
        prev = cur

    print(prev[m])

if __name__ == "__main__":
    solve()
```

## BFS 状态搜索

```python
from collections import deque

def bfs(start, target):
    q = deque([start])
    dist = {start: 0}
    neighbors = {
        1: [2, 3],
        2: [4],
        3: [4],
        4: [],
    }
    while q:
        cur = q.popleft()
        if cur == target:
            return dist[cur]
        for nxt in neighbors.get(cur, []):
            if nxt not in dist:
                dist[nxt] = dist[cur] + 1
                q.append(nxt)
    return -1
```

调用示例：

```python
# 把 list 状态转 tuple，才能放进 set/dict/lru_cache
state = [1, 2, 3]
key = tuple(state)
seen = {key}
```

常见坑：

- `@lru_cache(None)` 放在函数定义上一行；函数参数必须可哈希。
- base case 要先写，避免递归无限下去。
- Python 递归深度默认较小，可写 `sys.setrecursionlimit(1000000)`，但深递归仍不稳。
- `lru_cache` 缓存不会自动释放，状态太多时会 MLE。
- 字符串切片会复制；高频大切片时尽量传下标。
- BFS 的 `set` 里不要放 list，改放 tuple。

暴力/部分分替代：

- 先写无记忆化 DFS，确认样例正确。
- 把 DFS 函数中真正决定未来的可变参数留下，加 `@lru_cache(None)`；如果参数里有 `list/set/dict`，先转成 `tuple/frozenset`。
- 状态太大无法数组化时，用 Python 字典/缓存先拿中等分。
- 如果 Python 记忆化满分不稳，保留思路后翻译成 C++ 数组 DP。

最小测试样例：

```text
快速求和输入
99999
45

输出
4

编辑距离输入
sfdqxbw
gfdgw

输出
4
```
