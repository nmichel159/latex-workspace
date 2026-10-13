"""A family of DC pairs whose shortest u-v path inside a minimum cut has length 2k+1 (k >= 1).

F(k, cliques): path x_0 ... x_{2k+1}, u = x_0, v = x_{2k+1} (vertex x_i = i);
  u is adjacent to every x_{2i} (1 <= i <= k) and joined to it by an ear u - y_i - x_{2i};
  v is adjacent to every x_{2i+1} (0 <= i <= k-1) and joined to it by an ear x_{2i+1} - z_i - v;
  with cliques=True also all edges among the even x's and among the odd x's.
n = 4k + 2.  delta(A) for A = {even x's} + {y_i} consists of the 2k+1 path edges; the 2k+1 units of flow are
  u - x_1 - (v or z_0 - v) ...  (each x_{2i} gets one unit on the edge u x_{2i} and one through y_i, each odd x
  sends one unit on its edge to v and one through z_i), so c(u,v) = 2k+1 and the path lies in a minimum cut.
The script checks: in DC, d(u,v), c(u,v), cp(u,v) (cp_brute up to n = 14), all paths inside minimum cuts.
"""

import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cutpaths as cpz  # noqa: E402
from cutpaths import mcp, Gr, PairInfo  # noqa: E402


def family(k, cliques):
    L = 2 * k + 1
    xs = list(range(L + 1))
    u, v = 0, L
    es = [(i, i + 1) for i in range(L)]
    nxt = L + 1
    for i in range(1, k + 1):
        x = 2 * i
        es.append((u, x))
        es.append((u, nxt))
        es.append((nxt, x))
        nxt += 1
    for i in range(0, k):
        x = 2 * i + 1
        es.append((x, v))
        es.append((x, nxt))
        es.append((nxt, v))
        nxt += 1
    if cliques:
        ev = [x for x in xs if x % 2 == 0]
        od = [x for x in xs if x % 2 == 1]
        for grp in (ev, od):
            for a in range(len(grp)):
                for b in range(a + 1, len(grp)):
                    es.append((grp[a], grp[b]))
    return Gr(nxt, es), u, v


def main():
    lines = ["family.py: F(k) as described in the docstring", ""]
    for k in range(1, 6):
        for cliques in (False, True):
            t0 = time.time()
            g, u, v = family(k, cliques)
            P = PairInfo(g, u, v)
            paths = P.cut_paths()
            lens = sorted(set(len(p) - 1 for p in paths))
            dcv = cpz.dc_violations(g)
            d = mcp.bfs(g, u)[v]
            cpb = mcp.cp_brute(g, u, v)[0] if g.n <= 14 else None
            lines.append("k=%d cliques=%s: n=%d m=%d d(u,v)=%d c(u,v)=%d cp_brute=%s; paths in minimum cuts: %d, "
                         "lengths %s; DC violations: %d %s; candidate O3 says cp=c: %s  (%.1f s)"
                         % (k, cliques, g.n, g.m, d, P.c, cpb, len(paths), lens, len(dcv), dcv[:4],
                            cpz.candidate_dc(g, u, v, P.c), time.time() - t0))
            lines.append("    edges: " + cpz.fmt(g))
            print(lines[-2], flush=True)
            # independent check: all minimum cuts by vertex sets, paths inside them by plain path enumeration
            t1 = time.time()
            cb, cuts = mcp.min_cuts_by_sets(g, u, v)
            full = g.full()
            bp = set()
            for C in cuts:
                for vs, es in mcp.simple_paths(g, u, v, removed=full ^ C):
                    bp.add(vs)
            A = 0
            for x in range(0, 2 * k + 2, 2):
                A |= 1 << x
            for x in range(2 * k + 2, 3 * k + 2):      # the ears y_i lie on the side of u
                A |= 1 << x
            cutA = bin(cpz.cut_mask_of_side(g, A)).count("1")
            lines.append("    brute force: c=%d, %d minimum cuts, |delta(A)|=%d, paths inside minimum cuts %s, "
                         "same as the closure search: %s (%.1f s)"
                         % (cb, len(cuts), cutA, sorted(bp), bp == set(paths), time.time() - t1))
            print(lines[-1], flush=True)
    with open(os.path.join(HERE, "results-family.txt"), "w") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
