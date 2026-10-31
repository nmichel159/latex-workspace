"""Check of the reviewer's remark (rv-core-65.md Section 2.8): if every y in N_E lies in at most d bad pairs (or every
x in N_F does), then min(tau_E*, tau_F*) <= 4d + 4, where tau_E* (tau_F*) is the LP cover number of N_E (N_F) by the
cheap tools of Corollary 6.5'.  Also records min(tau) against kappa and against the bad-pair degrees.

usage: python test_remark.py SEED COUNT MMIN MMAX [GEN] [PATHCAP]
"""
import sys
import time
import random
from fractions import Fraction
from collections import Counter
from gsf import bits
from thy import Stars, Skel, bad_pairs, min_vertex_cover, frac_cover
import test_thm65


def main():
    seed, count, mmin, mmax = (int(a) for a in sys.argv[1:5])
    kind = sys.argv[5] if len(sys.argv) > 5 else "both"
    cap = int(sys.argv[6]) if len(sys.argv) > 6 else 10
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
        St = Stars(I)
        for P in paths:
            K = Skel(I, P)
            bp = bad_pairs(I, K)
            if not bp:
                continue
            st["paths with bad pairs"] += 1
            degx = Counter(x for x, _ in bp)
            degy = Counter(y for _, y in bp)
            d = min(max(degx.values()), max(degy.values()))
            kap, _ = min_vertex_cover(bp)
            taus = []
            for kd in (0, 1):
                items = bits(K.NEi if kd == 0 else K.NFi)
                tools = test_thm65.cheap_tools(I, St, K, kd)
                taus.append(frac_cover([set(bits(c)) for _, c, _ in tools], items) if items else Fraction(0))
            mn = min(taus)
            if mn > 4 * d + 4:
                st["REMARK 2.8 FAILS"] += 1
            if d == 1:
                st["paths whose bad pairs have degree 1 on one side"] += 1
                st["max min tau at d = 1"] = max(st["max min tau at d = 1"], mn)
            st["max d"] = max(st["max d"], d)
            st["max kappa"] = max(st["max kappa"], kap)
            st["max min tau"] = max(st["max min tau"], mn)
            st["max min tau / (d + 1)"] = max(st["max min tau / (d + 1)"], mn / (d + 1))
            if kap >= 3:
                st["paths with kappa >= 3"] += 1
                st["max min tau at kappa >= 3"] = max(st["max min tau at kappa >= 3"], mn)
    print("test_remark seed %d count %d m %d-%d gen %s cap %d (%.0fs)" % (seed, count, mmin, mmax, kind, cap,
                                                                        time.time() - t0))
    for key in sorted(st):
        print("  %-55s %s" % (key, st[key]))


if __name__ == "__main__":
    main()
