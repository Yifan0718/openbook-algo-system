import sys
from itertools import combinations
n, k, target = map(int, sys.stdin.readline().split())
a = list(map(int, sys.stdin.readline().split()))
cnt = 0
for combi in combinations(a, k):
    if sum(combi) == target:
        cnt += 1
print(cnt)
