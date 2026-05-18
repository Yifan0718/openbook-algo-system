import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    print(a)

if __name__ == "__main__":
    main()
