"""The numeric inequalities of the proof of Lemma 8.1 for every m = 1 .. MMAX (exact where possible):
  (a) 2^k > m for k = floor(log2 m) + 1          (integers, exact)
  (b) (1 - 1/(2k))^N <= 1/m for N = ceil(2k ln m)  (checked as N * log(1 - 1/(2k)) <= -log m with a margin, and
      exactly with Fractions for m <= 60)
  (c) N >= 1 for m >= 2 (strictness of the heavy-row bound), N = 0 for m = 1
usage: python probcheck.py MMAX
"""
import sys
import math
from fractions import Fraction

MMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 10 ** 6
bad = []
minmargin = None
for m in range(1, MMAX + 1):
    k = m.bit_length()
    if k != math.floor(math.log2(m)) + 1 and m < 2 ** 50:
        # bit_length is the exact floor(log2 m) + 1; math.log2 may round for huge m
        bad.append(("k", m))
    if not (2 ** k > m):
        bad.append(("a", m))
    N = math.ceil(2 * k * math.log(m))
    lhs = N * math.log1p(-1.0 / (2 * k))
    margin = -math.log(m) - lhs
    if m >= 2:
        if margin < -1e-12:
            bad.append(("b", m, margin))
        minmargin = margin if minmargin is None else min(minmargin, margin)
        if N < 1:
            bad.append(("c", m))
    else:
        if N != 0:
            bad.append(("c1", m))
    if m <= 60 and m >= 2:
        if not (Fraction(2 * k - 1, 2 * k) ** N <= Fraction(1, m)):
            bad.append(("b-exact", m))
print("probcheck m = 1 ..", MMAX, ": violations", bad[:10], "count", len(bad), "; min margin of (b) for m >= 2:",
      minmargin)
