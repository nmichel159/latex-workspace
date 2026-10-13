"""Exact, AC and PC answers of the K4 3-colouring encoding of k4.py (no P2), for several CSP lengths L.
Usage: python k4_base.py L1 [L2 ...]"""
import os
import sys
import time

sys.setrecursionlimit(100000)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import zz  # noqa: E402
import hunt2  # noqa: E402
import pcfast  # noqa: E402
import k4  # noqa: E402

if __name__ == "__main__":
    N, E, F, s, t, labels = k4.build()
    z = zz.from_sw(*hunt2.ch_to_sw((N, E, F, s, t)))
    print("nodes", N, "switches", len(E), "ZZ n", z.n, "|R|", len(z.R), "P2 violations", len(z.p2_bad()), flush=True)
    print("exact", zz.exact_dfs(z)[0], flush=True)
    for L in map(int, sys.argv[1:]):
        t0 = time.time()
        ac = zz.ac_answer(z, L)
        pc = pcfast.pc_answer(z, L) if ac else False
        print("L = %d: AC %s, PC %s, %.0fs" % (L, ac, pc, time.time() - t0), flush=True)
