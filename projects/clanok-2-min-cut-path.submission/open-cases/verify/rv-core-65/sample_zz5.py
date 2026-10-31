"""Sampled small instances (reviewer rv-core-65): for EVERY preorder on K middle elements (K = 5: 4231 preorders),
SAMPLES random edge sets R of strict pairs (each strict pair with probability p, p drawn from {0.3, 0.5, 0.7} per
sample), converted by gsf.from_zz; every P2 instance gets the checks of enum_zz.py (test_lemmas.check_path on every
shortest valid path, test_thm65.analyse with exhaustive GDESC for m <= GD).

usage: python sample_zz5.py K SAMPLES SEED [GD] [PART NPARTS]
"""
import sys
import time
import random
from collections import Counter
from gsf import from_zz
from thy import Stars
from enum_zz import preorders
import test_lemmas
import test_thm65


def main():
    K, samples, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    gd = int(sys.argv[4]) if len(sys.argv) > 4 else 6
    part, nparts = (int(sys.argv[5]), int(sys.argv[6])) if len(sys.argv) > 6 else (0, 1)
    q = K + 2
    rng = random.Random(seed * 1000 + part)
    st = Counter()
    t0 = time.time()
    pres = preorders(K)
    st["preorders (all parts)"] = len(pres)
    for pi, lem in enumerate(pres):
        if pi % nparts != part:
            continue
        st["preorders"] += 1
        le = [[False] * q for _ in range(q)]
        for a in range(q):
            le[0][a] = True
            le[a][1] = True
            le[a][a] = True
        for a in range(K):
            for b in range(K):
                le[a + 2][b + 2] = lem[a][b]
        strict = [(0, w) for w in range(2, q)] + [(w, 1) for w in range(2, q)]
        strict += [(a + 2, b + 2) for a in range(K) for b in range(K) if lem[a][b] and not lem[b][a]]
        for _ in range(samples):
            p = rng.choice([0.3, 0.5, 0.7])
            R = [e for e in strict if rng.random() < p]
            I = from_zz(q, 0, 1, le, R)
            st["instances"] += 1
            if not I.p2():
                continue
            st["P2 instances"] += 1
            r, paths = I.all_shortest_paths(cap=30)
            if r is not None and r > 0:
                St = Stars(I)
                for P in paths:
                    test_lemmas.check_path(I, St, P, st, 3)
            test_thm65.analyse(I, st, 30, rng, gd)
        if st["preorders"] % 200 == 0:
            print("  preorders %d (%.0fs)" % (st["preorders"], time.time() - t0), flush=True)
    print("sample_zz5 K %d samples %d seed %d part %d/%d gdesc<=%d (%.0fs)" % (K, samples, seed, part, nparts, gd,
                                                                             time.time() - t0))
    for key in sorted(st):
        print("  %-55s %s" % (key, st[key]))


if __name__ == "__main__":
    main()
