import sys
from itertools import permutations

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    k = int(data[1])
    a = [int(x) for x in data[2:2 + n]]

    ans = 0
    for p in permutations(a):
        ok = True
        for i in range(1, n):
            if abs(p[i] - p[i - 1]) > k:
                ok = False
                break
        if ok:
            ans += 1
    print(ans)

if __name__ == "__main__":
    main()
