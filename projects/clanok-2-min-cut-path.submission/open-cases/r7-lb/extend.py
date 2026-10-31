"""Agent r7-lb (2026-10-31): extend a structured design by new members (r7-lb.md Section 3.3).

usage: python extend.py GENOME.json PA PB SAMPLES LOG [SEED]
GENOME.json: design of ce.py with word E^K F^K and hubs bottom = 2K, top = 2K + 1.  A new E-member is inserted at
position PA (0 < PA < K, i.e. in the interior) and a new F-member at position PB of the F-chain; all old cells keep
their values, every new cell (the new row, the new column, the new same-type cells) is drawn uniformly.  SAMPLES
draws; exact least single-term cost by lbcore.mincost; records the distribution, the mean over pairs of the cheapest
and saves the best instance (by cost, then by number of minimal pairs).  Use repeatedly to grow K.
"""
import sys
import os
import time
import random
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import design
import lbcore
import ce
import nbhd
import adv

lbcore.WORK_CAP = 200000


def main():
    gpath, PA, PB, samples, logp = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    seed = int(sys.argv[6]) if len(sys.argv) > 6 else 0
    rng = random.Random(seed)
    g0 = design.load_genome(gpath)
    word, cross0, same0 = nbhd.read_cells(g0)
    K = len(word) // 2
    K2 = K + 1
    nword = "E" * K2 + "F" * K2
    ra = lambda i: i + (1 if i >= PA else 0)           # old a index -> new a index
    rb = lambda j: j + (1 if j >= PB else 0)           # old b index (0..K-1) -> new b index

    def new_abs_a(i):
        return i

    def new_abs_b(j):
        return K2 + j
    fixed_cross = {}
    for (e, f), v in cross0.items():
        fixed_cross[(new_abs_a(ra(e)), new_abs_b(rb(f - K)))] = v
    fixed_same = {}
    for (x, y), v in same0.items():
        if word[x] == "E":
            nx, ny = new_abs_a(ra(x)), new_abs_a(ra(y))
        else:
            nx, ny = new_abs_b(rb(x - K)), new_abs_b(rb(y - K))
        fixed_same[(min(nx, ny), max(nx, ny))] = v
    cells = [(i, K2 + j) for i in range(K2) for j in range(K2)]
    sames = [(i, j) for i in range(2 * K2) for j in range(i + 1, 2 * K2) if nword[i] == nword[j]]
    f = open(logp, "a", encoding="utf-8")

    def say(s):
        print(s, flush=True)
        f.write(s + "\n")
        f.flush()
    say("extend %s PA %d PB %d samples %d seed %d (K %d -> %d) pid %d" % (gpath, PA, PB, samples, seed, K, K2,
                                                                         os.getpid()))
    hist = Counter()
    best = (-1, 10 ** 9)
    t0 = time.time()
    for it in range(samples):
        cross = {c: fixed_cross.get(c) or rng.choice(ce.CROSS) for c in cells}
        same = {c: fixed_same[c] if c in fixed_same else rng.randrange(2) for c in sames}
        g = ce.build_genome(nword, cross, same, rng)
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
