import sys
from collections import deque
n, m = map(int, sys.stdin.readline().split())
g = [[] for _ in range(n + 1)]
for _ in range(m):
    u, v = map(int, sys.stdin.readline().split())
    g[u].append(v)
    g[v].append(u)
dist = [-1] * (n + 1)
q = deque([1])
dist[1] = 0
while q:
    u = q.popleft()
    for v in g[u]:
        if dist[v] == -1:
            dist[v] = dist[u] + 1
            q.append(v)
print(dist[n])
