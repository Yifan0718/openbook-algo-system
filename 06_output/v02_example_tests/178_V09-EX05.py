import sys
from collections import deque

def main():
    lines = sys.stdin.read().splitlines()
    if not lines:
        return
    n, m = map(int, lines[0].split())
    grid = lines[1:1 + n]

    start = target = None
    for i in range(n):
        for j in range(m):
            if grid[i][j] == "S":
                start = (i, j)
            elif grid[i][j] == "T":
                target = (i, j)

    dist = [[-1] * m for _ in range(n)]
    q = deque()
    si, sj = start
    dist[si][sj] = 0
    q.append((si, sj))

    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    while q:
        x, y = q.popleft()
        for dx, dy in directions:
            nx = x + dx
            ny = y + dy
            if 0 <= nx < n and 0 <= ny < m:
                if grid[nx][ny] != "#" and dist[nx][ny] == -1:
                    dist[nx][ny] = dist[x][y] + 1
                    q.append((nx, ny))

    ti, tj = target
    print(dist[ti][tj])

if __name__ == "__main__":
    main()
