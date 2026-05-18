import sys
from math import comb
n, k = map(int, sys.stdin.readline().split())
print(comb(n, k))
