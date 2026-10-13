"""Hill climbing for DC pairs with k* >= 3 (theory-hardness.md, Section 6.4), started from the 11-vertex DC graph with
k* = 2 plus n - 11 new vertices joined at random.  Same score as search_k.py (1000 * k* + number of minimum cuts).
Usage: python search_k_seeded.py n iterations seeds.  Output: appended to results-k.txt.
"""

import os
import random
import sys
import time
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import search_k as sk  # noqa: E402

BASE = [tuple(map(int, t.split("-"))) for t in
        "0-3 0-4 0-6 0-8 0-10 1-2 1-4 1-6 1-7 2-5 2-7 2-9 2-10 3-7 3-8 3-10 5-7 9-10".split()]


def climb(args):
    n, iters, seed = args
    rng = random.Random(seed)
    allpairs = [(a, b) for a in range(n) for b in range(a + 1, n)]
    while True:
        es = set(BASE)
        for x in range(11, n):
            for y in rng.sample(range(x), 2):
                es.add((y, x))
        r = sk.analyse(n, sorted(es), True)
        if r is not None:
            break
    cur, cur_score, cur_info = es, r[0], r[1]
    for it in range(iters):
        new = set(cur)
        for _ in range(rng.randint(1, 2)):
            new ^= {rng.choice(allpairs)}
        r = sk.analyse(n, sorted(new), True)
        if r is None:
            continue
        if r[0] >= cur_score or rng.random() < 0.02:
            cur, cur_score, cur_info = new, r[0], r[1]
    return seed, cur_score, cur_info, sorted(cur)


def main():
    n, iters, seeds = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    t0 = time.time()
    with Pool(30) as pool:
        res = pool.map(climb, [(n, iters, s) for s in range(seeds)])
    res.sort(key=lambda t: -t[1])
    ks = {}
    for seed, sc, info, es in res:
        k = info[5] if info else None
        ks[k] = ks.get(k, 0) + 1
    lines = ["search_k_seeded.py n=%d iterations=%d seeds=%d (start: the 11-vertex DC graph with k* = 2)" % (n, iters, seeds),
             "  final k* over seeds: %s" % sorted(ks.items(), key=lambda t: (t[0] is None, t[0]))]
    for seed, sc, info, es in res[:3]:
        lines.append("  seed %d score %d (u, v, c, #cuts, #cuts with path, k*) = %s; edges %s"
                     % (seed, sc, info, " ".join("%d-%d" % e for e in es)))
    lines.append("  Time %.0f s." % (time.time() - t0))
    with open(os.path.join(HERE, "results-k.txt"), "a") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
