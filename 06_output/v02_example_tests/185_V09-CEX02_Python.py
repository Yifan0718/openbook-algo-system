import sys, heapq
n = int(sys.stdin.readline())
small = []
large = []
ans = []
for x in map(int, sys.stdin.readline().split()):
    heapq.heappush(small, -x)
    heapq.heappush(large, -heapq.heappop(small))
    if len(large) > len(small):
        heapq.heappush(small, -heapq.heappop(large))
    ans.append(str(-small[0]))
print(" ".join(ans))
