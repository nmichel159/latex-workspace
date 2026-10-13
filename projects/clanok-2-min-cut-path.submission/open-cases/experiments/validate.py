"""Task 1, 3 (O1) and 3 (O5): validate cutpaths.py against brute force on all connected graphs with <= 8 vertices.

For every connected graph (networkx atlas for n <= 7, the cached list of 11117 graphs for n = 8) and every ordered
pair (u, v) (n <= 7) or unordered pair u < v (n = 8):
  V1  c(u,v) of PairInfo equals c of mcp.min_cuts_by_sets;
  V2  the set of u-v paths found by the residual-closure search equals the union, over all minimum cuts delta(A)
      (all vertex sets enumerated), of the simple u-v paths of the subgraph (V, delta(A));
  V3  the shortest length found by iterative deepening equals the minimum over that union;
  V4  mcp.cp_brute(u,v) == c(u,v) iff the union is non-empty;
  V5  the length-3 paths accepted by the set-to-set test O3 are exactly the length-3 paths of the union;
  O1  if c(u,v) >= 3, every vertex of every path of the union has c(u,x) >= 3 (x = u allowed);
  O5  (n <= 7 only) G + w, w adjacent to u and v only: c' = c + 1, d' = min(d, 2), the same set of paths.
Usage: python validate.py [nmax]
"""

import os
import sys
import time
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cutpaths as cpz  # noqa: E402
from cutpaths import mcp, Gr, PairInfo  # noqa: E402

CACHE = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "tmp", "clanok-2-checks"))


def brute_paths(g, u, v):
    c, cuts = mcp.min_cuts_by_sets(g, u, v)
    full = g.full()
    paths = set()
    for C in cuts:
        for vs, es in mcp.simple_paths(g, u, v, removed=full ^ C):
            paths.add(vs)
    return c, paths, len(cuts)


def check_graph(item):
    n, edges = item
    g = Gr(n, edges)
    out = {"pairs": 0, "fail": [], "o1_tested": 0, "o1_fail": [], "o5_tested": 0, "o5_fail": [],
           "with_paths": 0, "lengths": {}}
    pairs = [(u, v) for u in range(n) for v in range(n) if u != v] if n <= 7 else \
        [(u, v) for u in range(n) for v in range(u + 1, n)]
    D = mcp.dist_matrix(g)
    for u, v in pairs:
        out["pairs"] += 1
        P = PairInfo(g, u, v)
        found = set(P.cut_paths())
        c, bp, ncuts = brute_paths(g, u, v)
        L, _ = P.shortest_cut_path()
        bl = min((len(p) - 1 for p in bp), default=None)
        cpb = mcp.cp_brute(g, u, v)[0]
        o3 = set(cpz.o3_paths(g, u, v, c))
        b3 = set(p for p in bp if len(p) == 4)
        errs = []
        if P.c != c:
            errs.append("V1")
        if found != bp:
            errs.append("V2")
        if L != bl:
            errs.append("V3")
        if (cpb == c) != bool(bp):
            errs.append("V4")
        if o3 != b3:
            errs.append("V5")
        if errs:
            out["fail"].append((n, edges, u, v, errs))
        if bp:
            out["with_paths"] += 1
            key = (D[u][v], tuple(sorted(set(len(p) - 1 for p in bp))))
            out["lengths"][key] = out["lengths"].get(key, 0) + 1
        if c >= 3 and bp:
            out["o1_tested"] += 1
            Q = cpz.class3(g, u)
            on = 0
            for p in bp:
                for x in p:
                    on |= 1 << x
            if on & ~Q:
                out["o1_fail"].append((n, edges, u, v))
        if n <= 7:
            out["o5_tested"] += 1
            h = cpz.add_vertex(g, [u, v])
            Ph = PairInfo(h, u, v)
            dh = mcp.bfs(h, u)[v]
            fh = set(Ph.cut_paths())
            if Ph.c != c + 1 or dh != min(D[u][v], 2) or fh != found:
                out["o5_fail"].append((n, edges, u, v))
    return out


def main():
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    t0 = time.time()
    lines = []
    tot = {"graphs": 0, "pairs": 0, "fail": [], "o1_tested": 0, "o1_fail": [], "o5_tested": 0, "o5_fail": [],
           "with_paths": 0, "lengths": {}}
    with Pool(32) as pool:
        for n in range(2, nmax + 1):
            items = mcp.connected_graphs(n, CACHE)
            sub = {"pairs": 0, "fail": 0, "with_paths": 0}
            for out in pool.imap_unordered(check_graph, items, chunksize=8):
                tot["graphs"] += 1
                for k in ("pairs", "o1_tested", "o5_tested", "with_paths"):
                    tot[k] += out[k]
                for k in ("fail", "o1_fail", "o5_fail"):
                    tot[k] += out[k]
                for k, val in out["lengths"].items():
                    tot["lengths"][k] = tot["lengths"].get(k, 0) + val
                sub["pairs"] += out["pairs"]
                sub["fail"] += len(out["fail"])
                sub["with_paths"] += out["with_paths"]
            lines.append("n=%d: %d graphs, %d %s pairs, %d with a path inside a minimum cut, %d validation failures"
                         % (n, len(items), sub["pairs"], "ordered" if n <= 7 else "unordered", sub["with_paths"],
                            sub["fail"]))
            print(lines[-1], flush=True)
    lines.append("")
    lines.append("Validation failures (V1-V5): %d" % len(tot["fail"]))
    for f in tot["fail"][:20]:
        lines.append("  %r" % (f,))
    lines.append("O1 (c >= 3 and a path inside a minimum cut => all its vertices x have c(u,x) >= 3): tested on %d pairs, "
                 "%d failures" % (tot["o1_tested"], len(tot["o1_fail"])))
    for f in tot["o1_fail"][:20]:
        lines.append("  %r" % (f,))
    lines.append("O5 (add w adjacent to u, v: c+1, d<=2, same paths inside minimum cuts): tested on %d ordered pairs "
                 "(n <= 7), %d failures" % (tot["o5_tested"], len(tot["o5_fail"])))
    for f in tot["o5_fail"][:20]:
        lines.append("  %r" % (f,))
    lines.append("")
    lines.append("Pairs with a path inside a minimum cut, by (d(u,v), set of lengths of such paths):")
    for k in sorted(tot["lengths"]):
        lines.append("  d=%d lengths %s: %d" % (k[0], list(k[1]), tot["lengths"][k]))
    lines.append("Time %.0f s." % (time.time() - t0))
    with open(os.path.join(HERE, "results-validate.txt"), "w") as f:
        f.write("validate.py: all connected graphs with 2..%d vertices\n\n" % nmax)
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines[-12:]))


if __name__ == "__main__":
    main()
