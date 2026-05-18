# PY-04 Python 常用算法模板

模块编号：PY-04

模块名称：Python 可快速复用的算法与数据结构模板

标签：Python、BFS、Dijkstra、DSU、树状数组、子集和、排序、二分、图

一句话用途：在 Python 适合的中小规模题里，直接抄这些短模板；大规模卡常题仍优先 C++。

题面触发词：

- 无权最短路、网格 BFS。
- 非负权最短路，但规模不太卡。
- 连通性、合并集合。
- 动态前缀和、逆序对、排名。
- 子集和可行性、大整数位运算。
- 排序后二分、答案二分。

什么时候用：

- 数据规模中等，Python 复杂度足够。
- C++ 模板较长，Python 可以更快写出正确版本。
- 目标是快速拿分或验证思路。

不要什么时候用：

- 数据规模巨大且时间限制严格。
- 需要复杂线段树、最大流、重型图论。
- 需要稳定通过所有强数据，且你已有 C++ 模板。

复杂度：

- BFS：`O(n + m)`。
- Dijkstra：`O((n + m) log m)`。
- DSU：近似 `O(1)`。
- 树状数组：单次 `O(log n)`。
- Python int 位集子集和：约 `O(n * sum / word_size)`，常数由底层大整数优化承担。

依赖的标准容器：

- `list`
- `deque`
- `heapq`
- `bisect`
- `set`
- `dict`

输入如何整理：

```python
import sys

data = sys.stdin.buffer.read().split()
it = iter(data)
n = int(next(it))
m = int(next(it))
g = [[] for _ in range(n + 1)]
for _ in range(m):
    u = int(next(it))
    v = int(next(it))
    g[u].append(v)
    g[v].append(u)
```

接口：

```text
BFS：dist = bfs(n, g, s)
Dijkstra：dist = dijkstra(n, g, s)
DSU：find(x), union(a,b)
树状数组：add(i,v), sum(i), range_sum(l,r)
```

## BFS 最短路

模板代码：

```python
from collections import deque

def bfs(n, g, s):
    dist = [-1] * (n + 1)
    dist[s] = 0
    q = deque([s])
    while q:
        u = q.popleft()
        for v in g[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist
```

## Dijkstra 非负权最短路

```python
from heapq import heappush, heappop

INF = 10 ** 30

def dijkstra(n, g, s):
    dist = [INF] * (n + 1)
    dist[s] = 0
    heap = [(0, s)]
    while heap:
        d, u = heappop(heap)
        if d != dist[u]:
            continue
        for v, w in g[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heappush(heap, (nd, v))
    return dist
```

## DSU 并查集

```python
class DSU:
    def __init__(self, n):
        self.fa = list(range(n + 1))
        self.sz = [1] * (n + 1)

    def find(self, x):
        while x != self.fa[x]:
            self.fa[x] = self.fa[self.fa[x]]
            x = self.fa[x]
        return x

    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)
        if a == b:
            return False
        if self.sz[a] < self.sz[b]:
            a, b = b, a
        self.fa[b] = a
        self.sz[a] += self.sz[b]
        return True
```

## 树状数组

```python
class BIT:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i, v):
        while i <= self.n:
            self.bit[i] += v
            i += i & -i

    def sum(self, i):
        res = 0
        while i > 0:
            res += self.bit[i]
            i -= i & -i
        return res

    def range_sum(self, l, r):
        if l > r:
            return 0
        return self.sum(r) - self.sum(l - 1)
```

## Python int 位集做子集和

这个是 Python 的强项之一，适合非负权值、目标和不太大。

```python
def subset_sum_possible(a, target):
    bits = 1
    mask = (1 << (target + 1)) - 1
    for x in a:
        if 0 <= x <= target:
            bits |= bits << x
            bits &= mask
    return (bits >> target) & 1
```

## 二分答案

```python
def first_true(lo, hi, check):
    while lo < hi:
        mid = (lo + hi) // 2
        if check(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
```

调用示例：

```python
n = 5
dsu = DSU(n)
dsu.union(1, 2)
print(dsu.find(1) == dsu.find(2))
```

常见坑：

- Python 图邻接表对象开销大，`m` 很大时优先 C++。
- `heapq` 没有 decrease-key，用“新距离入堆 + 弹出时跳过旧状态”。
- 树状数组仍按 1-index；`i = 0` 会死循环。
- Python 类方法调用有常数，极限卡常时可以改成函数和列表。
- 子集和位集只适合非负整数；有负数要先偏移或换方法。
- `INF` 要足够大，Python 不溢出，但别用浮点 `inf` 混整数。

暴力/部分分替代：

- 图最短路：无权先 BFS；带权小图可先 Floyd 或 DFS 枚举。
- 连通性：不会复杂图算法时，DSU 先拿合并查询分。
- 区间求和：树状数组不会写时，先前缀和处理静态区间。
- 子集和：目标小用位集；`n` 小用枚举。

最小测试样例：

```text
BFS 输入
4 3
1 2
2 3
1 4

从 1 出发 dist[3] = 2
```

