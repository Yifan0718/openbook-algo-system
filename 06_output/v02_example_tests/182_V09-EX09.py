import sys
from functools import lru_cache

def main():
    lines = sys.stdin.read().splitlines()
    if not lines:
        return
    n, m = map(int, lines[0].split())
    grid = lines[1:1 + n]
    sys.setrecursionlimit(max(1000000, n + m + 10))

    @lru_cache(None)
    def dfs(i, j):
        if i >= n or j >= m:
            return 0
        if grid[i][j] == "#":
            return 0
        if i == n - 1 and j == m - 1:
            return 1
        return dfs(i + 1, j) + dfs(i, j + 1)

    print(dfs(0, 0))

if __name__ == "__main__":
    main()
