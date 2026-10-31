"""Proposition 6.1 and Section 6.3 of dc-algorithm.md on the own rebuild of H(m, m') (agent verify-round3).
For each instance: ZZ axioms, P2, number of down-sets, exact answer by down-set enumeration and by path DFS,
Theorem F hypothesis and algorithm, AC and PC for odd L in a range.
Usage: python hub_check.py m mp Lmin Lmax [version ...]"""
import sys
import time

from hub3 import hub

if __name__ == "__main__":
    m, mp, Lmin, Lmax = map(int, sys.argv[1:5])
    versions = sys.argv[5:] or ['classes', 'po']
    for ver in versions:
        H = hub(m, mp, ver)
        H.check()
        t0 = time.time()
        ans, D, nd = H.solve_downsets()
        dfs = H.solve_dfs()
        print("H(%d,%d) %s: q=%d |R|=%d P2=%s downsets=%d answer(downsets)=%s answer(dfs)=%s bottomwit=%s topwit=%s"
              % (m, mp, ver, H.q, len(H.R), H.p2(), nd, ans, dfs is not None, H.bottom_witness_ok(),
                 H.top_witness_ok()), flush=True)
        fa = H.thmF()
        print("  Theorem F algorithm (bottom):", fa[0], " dual:", H.thmF(dual=True)[0], flush=True)
        for L in range(Lmin, Lmax + 1, 2):
            t1 = time.time()
            a = H.ac(L)[0]
            p = H.pc(L)
            print("  L=%d AC=%s PC=%s (%.1fs)" % (L, a, p, time.time() - t1), flush=True)
