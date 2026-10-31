"""Agent r7-lb (2026-10-31): add bad-pair extras to a structured design (r7-lb.md Section 3.3).

usage: python addbad.py GENOME.json SAMPLES LOG [SEED] [Q]
GENOME.json: design of ce.py (word E^K F^K, hubs bottom = 2K, top = 2K + 1, nx = 2).  Adds Q (default 1) pairs of
extra switches Y_i (below every X_j, above bottom, below top) and X_j: Y_i < one random F-member, X_j > one random
E-member (so that (X_j, Y_i) is a bad pair of r5-core.md Section 6.4: Y_i < X_j, X_j not a minimal E-member, Y_i not a
maximal F-member), all old cells unchanged, every contact of an incomparable pair involving a new switch drawn at
random (EE, FF, LW(bottom), UW(top)).  Exact least single-term cost, distribution and the best instance.
"""
import sys
import os
import time
import random
import copy
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import design
import lbcore

lbcore.WORK_CAP = 200000


def main():
    gpath, samples, logp = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    Q = int(sys.argv[5]) if len(sys.argv) > 5 else 1
    rng = random.Random(seed)
    g0 = design.load_genome(gpath)
    word = g0["word"]
    n = len(word)
    bottom, top = n, n + 1
    assert g0["nx"] == 2
    Epos = [i for i in range(n) if word[i] == "E"]
    Fpos = [i for i in range(n) if word[i] == "F"]
    f = open(logp, "a", encoding="utf-8")

    def say(s):
        print(s, flush=True)
        f.write(s + "\n")
        f.flush()
    say("addbad %s samples %d seed %d Q %d pid %d" % (gpath, samples, seed, Q, os.getpid()))
    hist = Counter()
    best = (-1, 10 ** 9)
    t0 = time.time()
    for it in range(samples):
        g = copy.deepcopy(g0)
        g["nx"] = 2 + 2 * Q
        m = n + g["nx"]
        Y = [n + 2 + i for i in range(Q)]
        X = [n + 2 + Q + j for j in range(Q)]
        rel = [tuple(r) for r in g["rel"]]
        for v in Y + X:
            rel.append((bottom, v))
            rel.append((v, top))
        for y in Y:
            for x in X:
                rel.append((y, x))
            rel.append((y, rng.choice(Fpos)))
        for x in X:
            rel.append((rng.choice(Epos), x))
        g["rel"] = rel
        le = design.closure(m, rel)
        for v in Y + X:
            for u in range(m):
                if u == v or le[u][v] or le[v][u]:
                    continue
                c = rng.choice(["EE", "FF", ["LW", bottom], ["UW", top]])
                g["contact"][design.pair_key(u, v)] = c
        I = design.build(g)
        if I is None:
            hist["invalid"] += 1
            continue
        pairs = lbcore.valid_pairs(I, state_cap=300000)
        if not pairs:
            hist["no"] += 1
            continue
        try:
            r = lbcore.mincost(I, cap=10, pairs=pairs)
        except RuntimeError:
            hist["workcap"] += 1
            continue
        c = r["total"] if isinstance(r["total"], int) else 99
        hist[c] += 1
        key = (c, -len(pairs))
        if key > (best[0], -best[1]):
            best = (c, len(pairs))
            design.save_genome(g, logp + ".best.json", dict(cost=c, npairs=len(pairs)))
            lbcore.dump(I, logp + ".best-inst.json", dict(cost=c, npairs=len(pairs)))
            say("  it %d new best cost %d npairs %d m %d (%.0fs)" % (it, c, len(pairs), I.m, time.time() - t0))
    say("SUMMARY %s (%.0fs)" % (dict(sorted(hist.items(), key=lambda kv: str(kv[0]))), time.time() - t0))


if __name__ == "__main__":
    main()
