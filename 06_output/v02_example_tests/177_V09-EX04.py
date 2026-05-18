import sys
import heapq

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    heap = [int(x) for x in data[1:1 + n]]
    heapq.heapify(heap)

    total = 0
    while len(heap) > 1:
        a = heapq.heappop(heap)
        b = heapq.heappop(heap)
        s = a + b
        total += s
        heapq.heappush(heap, s)
    print(total)

if __name__ == "__main__":
    main()
