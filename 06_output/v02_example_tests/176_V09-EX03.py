import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    points = set()
    for _ in range(n):
        x = int(next(it))
        y = int(next(it))
        points.add((x, y))

    ans = sorted(points)
    print(len(ans))
    for x, y in ans:
        print(x, y)

if __name__ == "__main__":
    main()
