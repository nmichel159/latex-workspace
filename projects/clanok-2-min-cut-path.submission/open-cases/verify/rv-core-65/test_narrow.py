"""Theorem 6.5 with the narrower notion of bad pair used by the code of r5-core (gstar.classify): a pair of N_F x N_E
that is bad by the order (y < x, x not in A, y not in B) AND covered by neither star (y not in NE(E#x), x not in
NF(F#y)).  The proof of Theorem 6.5 needs only the duality on R x C, so it should hold with a vertex cover of these
pairs.  Reviewer's own code; checks of test_thm65.check_cover for every minimum cover of the narrow pairs, and
exhaustive GDESC(k, kappa_narrow, 9k) for m <= GD.

usage: python test_narrow.py SEED COUNT MMIN MMAX [GEN] [PATHCAP] [GD]
"""
import sys
import math
import time
import random
from collections import Counter
from gsf import bits
from thy import Stars, Skel, bad_pairs, min_vertex_cover, gdesc
import test_thm65


def main():
    seed, count, mmin, mmax = (int(a) for a in sys.argv[1:5])
    kind = sys.argv[5] if len(sys.argv) > 5 else "both"
    cap = int(sys.argv[6]) if len(sys.argv) > 6 else 20
    gd = int(sys.argv[7]) if len(sys.argv) > 7 else 0
    rng = random.Random(seed)
    st = Counter()
    t0 = time.time()
    for it in range(count):
        I = test_thm65.gen(rng, mmin, mmax, kind, it)
        if not I.p2() or I.s == I.t:
            continue
        r, paths = I.shortest_paths(cap=cap)
        if r is None:
            continue
        st["yes-instances"] += 1
        m = I.m
        k = int(math.floor(math.log2(m))) + 1
        St = Stars(I)
        kmin_n = None
        kmin_o = None
        for P in paths:
            K = Skel(I, P)
            bp = bad_pairs(I, K)
            nar = [(x, y) for x, y in bp if not (St.NEstar[x] >> y) & 1 and not (St.NFstar[y] >> x) & 1]
            ko, _ = min_vertex_cover(bp)
            kn, covers = min_vertex_cover(nar)
            kmin_n = kn if kmin_n is None else min(kmin_n, kn)
            kmin_o = ko if kmin_o is None else min(kmin_o, ko)
            st["paths"] += 1
            st["paths with narrow bad pairs"] += bool(nar)
            st["paths with kappa_narrow < kappa_order"] += kn < ko
            st["max kappa_narrow"] = max(st["max kappa_narrow"], kn)
            for X0, Y0 in covers[:6]:
                test_thm65.check_cover(I, St, K, set(X0), set(Y0), k, st, rng)
        st["instances with kappa_min narrow < order"] += kmin_n < kmin_o
        if m <= gd:
            st["GDESC(k, kappa_narrow_min, 9k) runs"] += 1
            if not gdesc(I, St, k, kmin_n, 9 * k):
                st["GDESC(k, kappa_narrow_min, 9k) REJECTS A YES-INSTANCE"] += 1
    print("test_narrow seed %d count %d m %d-%d gen %s cap %d gd %d (%.0fs)" % (seed, count, mmin, mmax, kind, cap,
                                                                             gd, time.time() - t0))
    for key in sorted(st):
        print("  %-55s %s" % (key, st[key]))


if __name__ == "__main__":
    main()
