"""Agent r7-lb (2026-10-31): neighbourhood of a structured design in the cell parameterisation of ce.py.

usage: python nbhd.py GENOME.json D MODE LOG [SEED] [SAMPLES]
Cells: cross cells (E-member, F-member) with values E F L U C and same-type cells with two values (ce.py).  The cells
of GENOME.json are read back (word E^K F^K, hubs bottom = n, top = n + 1, no other switch).  MODE 'all': every design
at Hamming distance 1..D (D <= 2 is feasible); MODE 'sample': SAMPLES random designs at distance exactly D.
Evaluates the exact least single-term cost (lbcore.mincost) and records the distribution and the first instance of
every cost above that of the centre.
"""
import sys
import os
import time
import random
import itertools
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import design
import lbcore
import ce

lbcore.WORK_CAP = 200000


def read_cells(g):
    word = g["word"]
    n = len(word)
    rel = {tuple(r) for r in g["rel"]}
    cross, same = {}, {}
    for i in range(n):
        for j in range(i + 1, n):
            c = g["contact"].get(design.pair_key(i, j))
            if word[i] == word[j]:
                if word[i] == "E":
                    same[(i, j)] = 0 if c == "FF" else 1
                else:
                    same[(i, j)] = 0 if c == "EE" else 1
            else:
                e, f = (i, j) if word[i] == "E" else (j, i)
                if c is None:
                    cross[(e, f)] = "C"
                elif c == "EE":
                    cross[(e, f)] = "E"
                elif c == "FF":
                    cross[(e, f)] = "F"
                elif c[0] == "LW":
                    cross[(e, f)] = "L"
                else:
                    cross[(e, f)] = "U"
    return word, cross, same


def cost_of(word, cross, same, rng):
    g = ce.build_genome(word, cross, same, rng)
    I = design.build(g)
    if I is None:
        return None, None, None
    pairs = lbcore.valid_pairs(I, state_cap=300000)
    if not pairs:
        return None, None, None
    try:
        r = lbcore.mincost(I, cap=10, pairs=pairs)
    except RuntimeError:
        return None, None, None
    return (r["total"] if isinstance(r["total"], int) else 99), g, (I, len(pairs))


def main():
    gpath, D, mode, logp = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
    seed = int(sys.argv[5]) if len(sys.argv) > 5 else 0
    samples = int(sys.argv[6]) if len(sys.argv) > 6 else 10000
    rng = random.Random(seed)
    g0 = design.load_genome(gpath)
    word, cross0, same0 = read_cells(g0)
    c0, gg, _ = cost_of(word, cross0, same0, rng)
    f = open(logp, "a", encoding="utf-8")

    def say(s):
        print(s, flush=True)
        f.write(s + "\n")
        f.flush()
    say("nbhd %s D %d mode %s centre cost %s pid %d" % (gpath, D, mode, c0, os.getpid()))
    cells = [("x", k) for k in cross0] + [("s", k) for k in same0]
    alts = {}
    for t, k in cells:
        if t == "x":
            alts[(t, k)] = [v for v in "EFLUC" if v != cross0[k]]
        else:
            alts[(t, k)] = [1 - same0[k]]
    hist = Counter()
    best = c0
    t0 = time.time()

    def evaluate_change(change):
        nonlocal best
        cross, same = dict(cross0), dict(same0)
        for (t, k), v in change:
            (cross if t == "x" else same)[k] = v
        c, g, extra = cost_of(word, cross, same, rng)
        if c is None:
            hist["none"] += 1
            return
        hist[c] += 1
        if c > best:
            best = c
            design.save_genome(g, logp + ".cost%d.json" % c, dict(cost=c, npairs=extra[1]))
            lbcore.dump(extra[0], logp + ".cost%d-inst.json" % c, dict(cost=c, npairs=extra[1]))
            say("  new max cost %d npairs %d (%.0fs)" % (c, extra[1], time.time() - t0))

    if mode == "all":
        for d in range(1, D + 1):
            for sub in itertools.combinations(cells, d):
                for vals in itertools.product(*[alts[s] for s in sub]):
                    evaluate_change(list(zip(sub, vals)))
            say("distance %d done: %s (%.0fs)" % (d, dict(hist), time.time() - t0))
    else:
        for _ in range(samples):
            sub = rng.sample(cells, D)
            evaluate_change([(s, rng.choice(alts[s])) for s in sub])
        say("sampled %d designs at distance %d: %s" % (samples, D, dict(hist)))
    say("END best cost %d centre %s (%.0fs)" % (best, c0, time.time() - t0))


if __name__ == "__main__":
    main()
