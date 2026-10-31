"""Proposition D (iv): HYB (plain and refined) with every maximal parameter tuple kd + ks + s = k - 1, B = k - 1
(all smaller tuples are contained in the enumeration), on all four variants; plus boundary tuples.

usage: python sweep_d.py KMIN KMAX [refined] [kdmax]
"""
import sys
import time
from fams import yfam
from sw import hyb, prune

VARIANTS = [(c, bk) for c in (False, True) for bk in (False, True)]


def main():
    kmin, kmax = int(sys.argv[1]), int(sys.argv[2])
    refined = len(sys.argv) > 3 and sys.argv[3] == "refined"
    kdmax = int(sys.argv[4]) if len(sys.argv) > 4 else 99
    for k in range(kmin, kmax + 1):
        tot = k - 1
        tuples = [(kd, ks, tot - kd - ks) for kd in range(min(tot, kdmax) + 1) for ks in range(tot - kd + 1)]
        for (c, bk) in VARIANTS:
            if refined and not c:
                pass
            G = yfam(k, contact=c, d=True, back=bk)
            fx = prune(G)
            for (kd, ks, s) in tuples:
                t0 = time.time()
                r = hyb(G, kd, ks, s, k - 1, refined=refined, fixed=fx)
                print("k=%d contact=%s back=%s %s(kd=%d, ks=%d, s=%d, B=%d): %s [%.1fs]" % (
                    k, c, bk, "refined" if refined else "plain", kd, ks, s, k - 1, "ACCEPT" if r else "reject",
                    time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
