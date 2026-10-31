"""Exhaustive small instances (reviewer rv-core-65): all ZZ instances with u, v and K middle elements (every
preorder on the middle elements, u below and v above everything, every set R of strict pairs except {u, v}),
converted by gsf.from_zz; every P2 instance is checked by test_lemmas.check_path (every shortest valid path) and
test_thm65.analyse (Theorem 6.5 per path and cover, Corollary 6.5', GDESC(k, kappa_min, 9k) against brute force).

usage: python enum_zz.py K [GDESC_MMAX] [PART NPARTS]
"""
import sys
import time
import random
import itertools
from collections import Counter
from gsf import from_zz
from thy import Stars
import test_lemmas
import test_thm65


def preorders(k):
    pairs = [(a, b) for a in range(k) for b in range(k) if a != b]
    out = []
    for mask in range(1 << len(pairs)):
        le = [[a == b for b in range(k)] for a in range(k)]
        for i, (a, b) in enumerate(pairs):
            if (mask >> i) & 1:
                le[a][b] = True
        ok = True
        for a in range(k):
            for b in range(k):
                if le[a][b]:
                    for c in range(k):
                        if le[b][c] and not le[a][c]:
                            ok = False
                            break
                if not ok:
                    break
            if not ok:
                break
        if ok:
            out.append(le)
    return out


def main():
    K = int(sys.argv[1])
    gd = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    part, nparts = (int(sys.argv[3]), int(sys.argv[4])) if len(sys.argv) > 4 else (0, 1)
    q = K + 2
    rng = random.Random(K)
    st = Counter()
    t0 = time.time()
    pres = preorders(K)
    st["preorders"] = len(pres)
    for pi, lem in enumerate(pres):
        if pi % nparts != part:
            continue
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
        for mask in range(1 << len(strict)):
            R = [strict[i] for i in range(len(strict)) if (mask >> i) & 1]
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
        if (pi + 1) % 20 == 0:
            print("  preorder %d/%d (%.0fs) %s" % (pi + 1, len(pres), time.time() - t0, dict(st)), flush=True)
    print("enum_zz K %d part %d/%d gdesc<=%d (%.0fs)" % (K, part, nparts, gd, time.time() - t0))
    for key in sorted(st):
        print("  %-55s %s" % (key, st[key]))


if __name__ == "__main__":
    main()
