"""DC instances that need many generators: F(k) without cliques, repaired into DC.

G(k): start from F(k) without the cliques (family.family(k, False)); while some pair of path vertices violates DC,
take the first violating pair (a, b) with a even, b odd (they are on different sides of the planted cut) and add
three degree-2 vertices: an ear a - w - b, an ear u - y - a and an ear b - z - v (one more unit of flow
u -> y -> a -> w -> b -> z -> v; one more edge of the planted cut).  New vertices have degree 2, so new
violations can only involve path vertices.
Report: DC, d(u,v), c(u,v), lengths of the cut paths, gen_A and gen_B of generators.py.
"""

import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cutpaths as cpz  # noqa: E402
from cutpaths import mcp, Gr, PairInfo  # noqa: E402
import family  # noqa: E402
from generators import gen_numbers, gen_numbers_fast  # noqa: E402


def repaired(k):
    g, u, v = family.family(k, False)
    L = 2 * k + 1
    es = list(g.edges)
    n = g.n
    while True:
        h = Gr(n, es)
        bad = [(a, b) for a, b in cpz.dc_violations(h)]
        if not bad:
            return h, u, v
        a, b = bad[0]
        if a > L or b > L:
            raise RuntimeError("violation outside the path: %r" % ((a, b),))
        if a % 2 == 1:
            a, b = b, a
        if a % 2 == 1 or b % 2 == 0:
            raise RuntimeError("violation between vertices of one side: %r" % ((a, b),))
        w, y, z = n, n + 1, n + 2
        es += [(a, w), (w, b), (u, y), (y, a), (b, z), (z, v)]
        n += 3


def main():
    lines = ["repaired_family.py: G(k) (see docstring)", ""]
    for k in range(2, 8):
        t0 = time.time()
        g, u, v = repaired(k)
        P = PairInfo(g, u, v)
        paths = P.cut_paths()
        lens = sorted(set(len(p) - 1 for p in paths))
        cpb = mcp.cp_brute(g, u, v)[0] if g.n <= 18 else None
        ga, gb = gen_numbers_fast(g, u, v, P, paths)
        if g.n <= 20:
            assert (ga, gb) == gen_numbers(g, u, v, P, jmax=k)
        lines.append("k=%d: n=%d m=%d DC=%s (mcp.in_dc %s) d(u,v)=%d c(u,v)=%d cp_brute=%s cut paths %d, lengths %s, "
                     "gen_A=%s gen_B=%s (%.0f s)"
                     % (k, g.n, g.m, cpz.in_dc(g), mcp.in_dc(g)[0], mcp.bfs(g, u)[v], P.c, cpb, len(paths), lens,
                        ga, gb, time.time() - t0))
        lines.append("    edges: " + cpz.fmt(g))
        print(lines[-2], flush=True)
        with open(os.path.join(HERE, "results-repaired-family.txt"), "w") as f:
            f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
