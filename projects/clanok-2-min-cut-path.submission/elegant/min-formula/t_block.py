"""Blocks E^n F^k and random hub-free designs: exact least formula.  Usage: t_block.py"""
import random
import time

from gen import block, rand_abs
from mf_core import Measure


def report(tag, d, cap=800, maxcost=9):
    I, P = d.build()
    I.validate()
    if not I.p2():
        print(tag, "P2 fails", I.p2_violations()[:5])
        return None
    t0 = time.time()
    sw = I.shortest_walk(bound=len(P) - 1, budget=200000)
    t1 = time.time()
    if sw is not None:
        print(tag, "not shortest: q", len(P) - 1, "new", len(sw) - 1, "m", I.m, "t %.2f" % (t1 - t0))
        return None
    M = Measure(I, P)
    rf, re = M.pure()
    fr = M.free(maxcost=maxcost, cap=cap)
    t2 = time.time()
    print(tag, "m", I.m, "q", len(P) - 1, "|B|", M.nb, "|A|", M.na, "pureF", rf[0], "pureE", re[0], "free", fr["cost"], "exact", fr["exact"],
          "fronts", fr["fronts"], "t %.2f %.2f" % (t1 - t0, t2 - t1), flush=True)
    if fr["tree"]:
        print("   ", M.fmt(fr["tree"]), "distinct", M.distinct(fr["tree"]), flush=True)
    return fr


for n, k, X in [(6, 6, 3), (8, 8, 4), (8, 8, 5), (8, 8, 6), (10, 10, 6), (10, 10, 7), (12, 12, 9)]:
    report("block %d %d %d" % (n, k, X), block(n, k, X))
rng = random.Random(5)
for i in range(10):
    report("rand%d" % i, rand_abs(rng))
