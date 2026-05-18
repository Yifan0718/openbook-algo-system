import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    graph = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u = int(next(it))
        v = int(next(it))
        graph[u].append(v)
        graph[v].append(u)

    sys.setrecursionlimit(max(1000000, n * 2 + 10))
    size = [0] * (n + 1)

    def dfs(u, parent):
        size[u] = 1
        for v in graph[u]:
            if v == parent:
                continue
            dfs(v, u)
            size[u] += size[v]

    dfs(1, 0)
    print(" ".join(str(size[i]) for i in range(1, n + 1)))

if __name__ == "__main__":
    main()
