"""Question 1: far-pair atoms plus a window search.  For every family: the best any number of far pairs can do (union of all FR, intersection of all ER, on the true A_P, B_P),
then a window search with window k.  A locally valid walk shorter than q is invalid, so it refutes "every shortest locally valid walk in the allowed part is valid" for that k.

Usage: q1_window.py SEED SECONDS LOG
"""
import random
import sys
import time
from collections import Counter

from wd import Budget, WS, best_atoms, conflicts, window_search, bits, popcnt

from zz_design import BASES

FAMS = ["A", "B", "stair", "ties", "mix", "cross", "allstrict", "small", "kappa", "two"]
KS = [1, 2, 4, 6, 8, 12]


def main():
    seed, secs, logf = int(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
    rng = random.Random(seed)
    t0 = time.time()
    res = {}
    while time.time() - t0 < secs:
        for fam in FAMS:
            if time.time() - t0 > secs:
                break
            d = BASES[fam](rng)
            I, P = d.build()
            if not I.p2():
                continue
            try:
                if I.shortest_walk(bound=len(P) - 1, budget=60000) is not None:
                    continue
            except Budget:
                continue
            W = WS(I, P)
            F, E = best_atoms(I, W)
            lowok = E
            highok = I.ALL & ~F
            st = res.setdefault(fam, Counter())
            st["inst"] += 1
            st["m"] = max(st["m"], I.m)
            st["q"] = max(st["q"], W.q)
            st["|A|"] = max(st["|A|"], len(W.A))
            Z = E & ~F
            st["max |Z|"] = max(st["max |Z|"], popcnt(Z))
            # conflicts possible among allowed: pairs h <= l, both in Z
            for k in KS:
                try:
                    w = window_search(I, lowok, highok, k)
                except Budget:
                    st["k=%d budget" % k] += 1
                    continue
                if w is None:
                    st["k=%d NONE" % k] += 1
                elif len(w) - 1 < W.q:
                    st["k=%d short" % k] += 1
                    c = conflicts(I, w)
                    span = max(abs(i - j) for i, j in c) if c else 0
                    st["k=%d maxspan" % k] = max(st["k=%d maxspan" % k], span)
                elif not conflicts(I, w):
                    st["k=%d ok" % k] += 1
                else:
                    st["k=%d eqlen-invalid" % k] += 1
            with open(logf, "w", encoding="utf-8") as f:
                for fam2 in sorted(res):
                    print(fam2, dict(sorted(res[fam2].items())), file=f)
    print("done")


if __name__ == "__main__":
    main()
