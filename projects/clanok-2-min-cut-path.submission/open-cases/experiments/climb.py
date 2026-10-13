"""Planted local search (simulated annealing) for pairs whose shortest u-v path inside a minimum cut is long.

State: a graph on n vertices containing the path 0-1-...-L (u = 0, v = L, L odd) and a side s(x) in {0, 1} for
every vertex with s(i) = i mod 2 on the path (A = side 0).  The edge uv is never added.
Penalties (all zero = success):
  p1 = |delta(A)| - c(u,v)            (delta(A) is a minimum cut, so the path lies in a minimum cut)
  p2 = |d(u,v) - 2|
  p3 = number of DC violations          (mode dc)      or [no violation] (mode notdc)   or 0 (mode any)
  p4 = [some u-v path of length < L lies inside a minimum cut]   (only evaluated when p1 = p2 = 0)
score = 100 p1 + 100 p2 + 30 p3 + 50 p4 + m; moves: toggle a non-path pair, flip the side of a non-path vertex.
Successes are re-checked with mcp.cp_brute (n <= 14) and mcp.in_dc, and the one with the fewest edges is kept.
Usage: python climb.py <n> <L> <mode dc|notdc|any> <iterations> <seeds> <tag>
"""

import math
import os
import random
import sys
import time
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cutpaths as cpz  # noqa: E402
from cutpaths import mcp, Gr, PairInfo  # noqa: E402


def evaluate(n, L, mode, E, side):
    g = Gr(n, list(E))
    if not mcp.is_connected(g):
        return 10 ** 6, None, g
    u, v = 0, L
    c = mcp.edge_conn(g, u, v)
    cutA = sum(1 for a, b in g.edges if side[a] != side[b])
    p1 = cutA - c
    d = mcp.bfs(g, u)[v]
    p2 = abs(d - 2)
    if mode == "dc":
        p3 = len(cpz.dc_violations(g))
    elif mode == "notdc":
        p3 = 0 if cpz.dc_violations(g, stop=1) else 1
    else:
        p3 = 0
    p4 = 0
    if p1 == 0 and p2 == 0:
        P = PairInfo(g, u, v)
        Ls, _ = P.shortest_cut_path(maxlen=L - 2) if L >= 3 else (None, None)
        p4 = 1 if Ls is not None else 0
    pen = (p1, p2, p3, p4)
    return 100 * p1 + 100 * p2 + 30 * p3 + 50 * p4 + g.m, pen, g


def run(args):
    n, L, mode, iters, seed = args
    rng = random.Random(seed)
    path = set((i, i + 1) for i in range(L))
    side = [i % 2 for i in range(L + 1)] + [rng.randint(0, 1) for _ in range(n - L - 1)]
    E = set(path)
    # start: u joined to the even path vertices, v to the odd ones, random extra edges
    for i in range(2, L, 2):
        E.add((0, i))
    for i in range(1, L - 1, 2):
        E.add((i, L))
    for a in range(n):
        for b in range(a + 1, n):
            if (a, b) != (0, L) and rng.random() < (0.35 if side[a] == side[b] else 0.05):
                E.add((a, b))
    pairs = [(a, b) for a in range(n) for b in range(a + 1, n) if (a, b) not in path and (a, b) != (0, L)]
    cur, pen, g = evaluate(n, L, mode, E, side)
    best = None
    T0 = 6.0
    for it in range(iters):
        T = T0 * (1 - it / iters) + 0.3
        if rng.random() < 0.85 or n == L + 1:
            e = rng.choice(pairs)
            E2 = set(E)
            E2.symmetric_difference_update({e})
            side2 = side
        else:
            x = rng.randint(L + 1, n - 1)
            side2 = list(side)
            side2[x] ^= 1
            E2 = E
        s2, pen2, g2 = evaluate(n, L, mode, E2, side2)
        if s2 <= cur or rng.random() < math.exp((cur - s2) / T):
            E, side, cur, pen, g = E2, side2, s2, pen2, g2
            if pen == (0, 0, 0, 0) and (best is None or g.m < best[0]):
                best = (g.m, sorted(g.edges), list(side))
    return best


def main():
    n, L, mode, iters, seeds = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
    tag = sys.argv[6] if len(sys.argv) > 6 else "climb"
    t0 = time.time()
    with Pool(min(32, seeds)) as pool:
        results = pool.map(run, [(n, L, mode, iters, 7000 + s) for s in range(seeds)])
    found = sorted(r for r in results if r is not None)
    lines = ["climb.py n=%d L=%d mode=%s iterations=%d seeds=%d: %d seeds succeeded" % (n, L, mode, iters, seeds,
                                                                                      len(found))]
    seen = set()
    for m, es, side in found:
        if tuple(es) in seen:
            continue
        seen.add(tuple(es))
        g = Gr(n, es)
        P = PairInfo(g, 0, L)
        paths = P.cut_paths()
        lens = sorted(set(len(p) - 1 for p in paths))
        dc = mcp.in_dc(g)[0]
        cpb = mcp.cp_brute(g, 0, L)[0] if n <= 14 else None
        lines.append("  m=%d c=%d cp_brute=%s d=%d DC=%s lengths %s sideA=%s: %s"
                     % (m, P.c, cpb, mcp.bfs(g, 0)[L], dc, lens,
                        [x for x in range(n) if side[x] == 0], cpz.fmt(g)))
        if len(seen) >= 6:
            break
    lines.append("Time %.0f s." % (time.time() - t0))
    with open(os.path.join(HERE, "results-%s.txt" % tag), "w") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
