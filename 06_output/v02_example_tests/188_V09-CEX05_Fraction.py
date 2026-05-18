import sys
from fractions import Fraction
a, b, c, d = map(int, sys.stdin.readline().split())
x = Fraction(a, b) + Fraction(c, d)
print(f"{x.numerator}/{x.denominator}")
