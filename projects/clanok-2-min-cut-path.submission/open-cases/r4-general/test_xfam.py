"""Checks of the family X_L (xfam.py): P2, number of solutions (brute force over the order-consistent mode vectors
for small L, enumeration of down-sets for q <= 40 elements when feasible), exact answer, NG with several budgets and
junk allowances, the certificate search GC of dc-general (gcert.certificate) with k <= KGC.

Usage: python test_xfam.py LMIN LMAX MATES BUDGETS S KGC
  MATES in {none, even, odd, both}; BUDGETS e.g. 1,2,3; S = junk allowance s; KGC = largest GC pin-set size (0: skip)
"""
import sys
import time
from common_r4 import gcert, check_solution
from xfam import xfam, brute
from ng import ng

lmin, lmax = int(sys.argv[1]), int(sys.argv[2])
mates = sys.argv[3]
mates = None if mates == "none" else mates
budgets = [int(b) for b in sys.argv[4].split(",")]
s = int(sys.argv[5])
kgc = int(sys.argv[6])

for L in range(lmin, lmax + 1):
    I, names, info = xfam(L, mates)
    t0 = time.time()
    p2 = I.p2()
    nsol = len(brute(info)) if len(info["E"]) <= 16 else None
    ex = gcert.exact(I)
    line = "X_%d mates=%s q=%d |R|=%d switches=%d P2=%s solutions=%s exact=%s" % (
        L, mates, I.n, len(I.R), len(info["E"]), p2, nsol, ex)
    for b in budgets:
        st = {}
        r = ng(I, b, s, stats=st)
        ok = r is not None and check_solution(I, r[1])
        line += " | NG(%d,%d)=%s%s tried=%d" % (b, s, r is not None, "" if (r is None or ok) else " INVALID",
                                               st.get("tried", 0))
        if r is not None:
            line += " %s Pi=%s" % (r[0], [names[p] for p in r[3][1]])
            break
    if kgc:
        c = gcert.certificate(I, kgc)
        line += " | GC(<=%d)=%s" % (kgc, None if c is None else (c[0], c[1]))
    line += " | %.1fs" % (time.time() - t0)
    print(line, flush=True)
