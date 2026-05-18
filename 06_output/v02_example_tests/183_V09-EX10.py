import sys
from collections import deque

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    k = int(data[1])
    a = [0] + [int(x) for x in data[2:2 + n]]

    q = deque()
    ans = []
    for i in range(1, n + 1):
        while q and q[0] <= i - k:
            q.popleft()
        while q and a[q[-1]] <= a[i]:
            q.pop()
        q.append(i)
        if i >= k:
            ans.append(str(a[q[0]]))

    print(" ".join(ans))

if __name__ == "__main__":
    main()
