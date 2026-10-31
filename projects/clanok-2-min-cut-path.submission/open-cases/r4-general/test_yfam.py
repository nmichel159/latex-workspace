"""Checks of the family Y_k (yfam.py): P2, number of solutions (brute force over order-consistent mode vectors),
exact answer, the generalized side-set search gsw.decide for a ladder of parameters, NG budgets, GC.

Usage: python test_yfam.py KMIN KMAX [helly] [base]
  helly: Helly form; base: R(E^k F^k) without mates (control)
"""
import sys
import time
from common_r4 import gcert, check_solution
from yfam import rword
from xfam import brute
from gsw import GSW
from ng import ng

kmin, kmax = int(sys.argv[1]), int(sys.argv[2])
helly = "helly" in sys.argv[3:]
base = "base" in sys.argv[3:]
LADDER = [(1, 0, 2, 6), (1, 1, 4, 8), (2, 1, 4, 10), (2, 2, 6, 12), (3, 3, 8, 16)]

for k in range(kmin, kmax + 1):
    I, names, info = rword("E" * k + "F" * k, mates=not base, helly=helly)
    t0 = time.time()
    p2 = I.p2()
    nsw = len(info["E"])
    nsol = len(brute(info)) if nsw <= 16 else None
    ex = gcert.exact(I)
    line = "Y_%d%s%s q=%d switches=%d P2=%s solutions=%s exact=%s" % (
        k, " helly" if helly else "", " base" if base else "", I.n, nsw, p2, nsol, ex)
    G = GSW(I)
    found = None
    for par in LADDER:
        if sum(par) > 3 * k + 12 and found is None and par != LADDER[0]:
            pass
        r = G.decide(*par, want_walk=True)
        if r[0]:
            found = par
            break
    line += " | side-set minimal params in ladder: %s" % (found,)
    for b in (1, 2):
        r = ng(I, b, 0)
        if r is not None:
            assert check_solution(I, r[1])
            line += " | NG(%d)=True" % b
            break
    else:
        line += " | NG(<=2)=False"
    line += " | %.1fs" % (time.time() - t0)
    print(line, flush=True)
