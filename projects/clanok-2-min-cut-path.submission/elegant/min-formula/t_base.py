"""First measurement: least formula on the base instances of zz_design.  Usage: t_base.py SEED N"""
import random
import sys
import time

from mf_core import Measure
from zz_design import BASES

seed = int(sys.argv[1])
N = int(sys.argv[2])
rng = random.Random(seed)
for base in ["B", "A", "stair", "ties", "small", "mix", "cross", "allstrict", "kappa", "two", "margin2", "far2", "local"]:
    for k in range(N):
        d = BASES[base](rng)
        I, P = d.build()
        if not I.p2():
            print(base, "P2 fails")
            continue
        if I.shortest_walk(bound=len(P) - 1, budget=60000) is not None:
            print(base, "not shortest")
            continue
        t0 = time.time()
        M = Measure(I, P)
        t1 = time.time()
        rf, re = M.pure()
        t2 = time.time()
        fr = M.free(maxcost=10, cap=1500)
        t3 = time.time()
        print(base, "m", I.m, "q", len(P) - 1, "|B|", M.nb, "|A|", M.na, "atoms", len(M.atoms), "rep", M.nrepF, M.nrepE,
              "pureF", rf[0], "pureE", re[0], "free", fr["cost"], "exact", fr["exact"], "fronts", fr["fronts"],
              "t %.1f %.1f %.1f" % (t1 - t0, t2 - t1, t3 - t2), flush=True)
        if fr["tree"] is not None:
            print("   ", M.fmt(fr["tree"]), "distinct", M.distinct(fr["tree"]), flush=True)
        print("    F:", rf[1], flush=True)
        print("    E:", re[1], flush=True)
