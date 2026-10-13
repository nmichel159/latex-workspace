"""Search: DC pairs (d(u,v) = 2, c(u,v) >= 3) where some minimum cut contains a u-v path but no minimum cut generated
by one vertex does (theory-hardness.md, Section 6, conjecture C6.2).

For a vertex x let down(x) be the smallest minimum u-v cut containing x and up(x) the largest one avoiding x.
The 2n cuts down(x), up(x) are the "single-generated" cuts.  If in DC a single-generated cut always contains a path
when some minimum cut does, PATH-IN-MIN-CUT is polynomial on DC (O(n) closures and searches after one max-flow).

Method: hill climbing over graphs with n vertices (edge flips), staying in DC (mode dc) or not (mode any);
score = (pair found: 1000) + number of minimum cuts of the best yes-pair + 10 * (minimum number of generators of
a path-containing cut).  Usage: python search_generators.py n iterations seeds mode.
Output: appended to results-generators.txt.
"""

import os
import random
import sys
import time
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "checks")))

import mcp  # noqa: E402
import exact as ex  # noqa: E402


def analyse(n, es, need_dc):
    g = ex.UG(n, es)
    if not all(d is not None for d in ex.bfs_dist(g, 0)):
        return None
    if need_dc:
        G = mcp.Gr(n, es)
        if not mcp.in_dc(G)[0]:
            return None
    best = (0, None)
    for u in range(n):
        du = ex.bfs_dist(g, u)
        for v in range(u + 1, n):
            if du[v] != 2:
                continue
            if ex.cut_value(g, u, v, limit=3) < 3:
                continue
            try:
                c, cuts = ex.min_cuts_pq(g, u, v, max_free_classes=14)
            except ValueError:
                continue
            good = set(A for A in cuts if ex.cut_graph_path(g, A, u, v) is not None)
            if not good:
                continue
            gen = set()
            for x in range(n):
                inc = [A for A in cuts if x in A]
                exc = [A for A in cuts if x not in A]
                if inc:
                    gen.add(min(inc, key=len))
                if exc:
                    gen.add(max(exc, key=len))
            single_ok = bool(good & gen)
            score = len(cuts) + (1000 if not single_ok else 0)
            if score > best[0]:
                best = (score, (u, v, c, len(cuts), len(good), single_ok))
    return best


def climb(args):
    n, iters, seed, need_dc = args
    rng = random.Random(seed)
    allpairs = [(a, b) for a in range(n) for b in range(a + 1, n)]
    while True:
        es = set(p for p in allpairs if rng.random() < 0.45)
        r = analyse(n, sorted(es), need_dc)
        if r is not None:
            break
    cur, cur_score = es, r[0]
    found = []
    for it in range(iters):
        new = set(cur)
        for _ in range(rng.randint(1, 2)):
            p = rng.choice(allpairs)
            new ^= {p}
        r = analyse(n, sorted(new), need_dc)
        if r is None:
            continue
        if r[0] >= cur_score or rng.random() < 0.02:
            cur, cur_score = new, r[0]
            if r[0] >= 1000 and r[1] is not None:
                found.append((sorted(new), r[1]))
                break
    return seed, cur_score, found


def main():
    n = int(sys.argv[1])
    iters = int(sys.argv[2])
    seeds = int(sys.argv[3])
    mode = sys.argv[4]
    t0 = time.time()
    with Pool(30) as pool:
        res = pool.map(climb, [(n, iters, s, mode == "dc") for s in range(seeds)])
    lines = ["search_generators.py n=%d iterations=%d seeds=%d mode=%s" % (n, iters, seeds, mode)]
    nf = 0
    for seed, sc, found in res:
        for es, info in found:
            nf += 1
            if nf <= 5:
                lines.append("  seed %d: pair (u,v,c,#cuts,#cuts with path,single ok) = %s; edges %s"
                             % (seed, info, " ".join("%d-%d" % e for e in es)))
    lines.append("  seeds that found a pair with no single-generated cut containing a path: %d of %d" % (nf, seeds))
    lines.append("  best scores: %s" % sorted((sc for _, sc, _ in res), reverse=True)[:10])
    lines.append("  Time %.0f s." % (time.time() - t0))
    with open(os.path.join(HERE, "results-generators.txt"), "a") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
