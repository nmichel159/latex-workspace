"""Theorem 8.2 on all small ZZ instances (r5-core.md Section 8.4).

usage: python enum_inter.py K [PART NPARTS]
All ZZ instances with u, v and K middle elements (every preorder on the middle elements, u below and v above
everything, every set R of strict pairs except (u, v)) as gcert.Inst, converted by gcore.from_inst; for every P2
yes-instance and every shortest valid path the proof of Theorem 8.2 is run (inter.levels, ILP mode, every claim
checked); the answer of the final intersection is compared with brute force (gcore.brute) for the instance.
Written independently of the reviewer's enumerator (verify/rv-core-65/enum_zz.py), same instance set.
"""
import sys
import time
import itertools
from collections import Counter
import gcore
from gcore import from_inst
import gcert
import gstar
import inter


def preorders(k):
    pairs = [(a, b) for a in range(k) for b in range(k) if a != b]
    out = []
    for mask in range(1 << len(pairs)):
        le = [[a == b for b in range(k)] for a in range(k)]
        for i, (a, b) in enumerate(pairs):
            if (mask >> i) & 1:
                le[a][b] = True
        if all(not (le[a][b] and le[b][c]) or le[a][c] for a in range(k) for b in range(k) for c in range(k)):
            out.append(le)
    return out


def main():
    K = int(sys.argv[1])
    part, nparts = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (0, 1)
    n = K + 2
    st = Counter()
    t0 = time.time()
    idx = 0
    for lem in preorders(K):
        le = [[False] * n for _ in range(n)]
        for a in range(n):
            le[0][a] = True
            le[a][n - 1] = True
            le[a][a] = True
        for a in range(K):
            for b in range(K):
                if lem[a][b]:
                    le[a + 1][b + 1] = True
        strict = [(a, b) for a in range(n) for b in range(n) if le[a][b] and not le[b][a] and (a, b) != (0, n - 1)]
        for mask in range(1 << len(strict)):
            idx += 1
            if idx % nparts != part:
                continue
            R = [strict[i] for i in range(len(strict)) if (mask >> i) & 1]
            I = gcert.Inst(n, le, R, 0, n - 1)
            st["instances"] += 1
            if not I.p2():
                continue
            st["P2"] += 1
            G, _ = from_inst(I)
            Lsh, _ = G.shortest()
            yes = bool(G.brute()) if G.m <= 10 else None
            if Lsh is None:
                st["no"] += 1
                if yes:
                    st["BFS SAYS NO, BRUTE SAYS YES"] += 1
                continue
            st["yes"] += 1
            if yes is False:
                st["BFS SAYS YES, BRUTE SAYS NO"] += 1
            if Lsh == 0:
                continue
            St = gstar.Stars(G)
            for P in G.all_shortest(length=Lsh):
                K_ = gstar.Skel(G, P)
                st["paths"] += 1
                res = inter.levels(G, P, St, K_)
                if res["errors"]:
                    st["ERRORS"] += 1
                    print("ERROR mask=%d R=%s P=%s %s" % (mask, R, P, res["errors"][:3]), flush=True)
                st["levels=%d" % res["nlev"]] += 1
                for lv in res["levels"]:
                    st["case " + lv.get("case", "?")] += 1
                    st["max anchors"] = max(st["max anchors"], lv.get("anchors", 0))
                _, cl = gstar.classify(G, P, St, K_)
                if cl["bad"]:
                    st["paths with bad pairs"] += 1
        if st["instances"] and st["instances"] % 50000 < 2000:
            print("  %d (%.0fs) %s" % (st["instances"], time.time() - t0, dict(st)), flush=True)
    print("enum_inter K %d part %d/%d (%.0fs)" % (K, part, nparts, time.time() - t0))
    for kk in sorted(st):
        print("  %-35s %s" % (kk, st[kk]))


if __name__ == "__main__":
    main()
