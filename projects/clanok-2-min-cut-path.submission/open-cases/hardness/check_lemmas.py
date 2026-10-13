"""Checks of the lemmas of theory-hardness.md, Sections 1 and 3, on small graphs.

Graphs: all connected graphs with 2..7 vertices (networkx atlas, via checks/mcp.py, imported read-only) and all
connected graphs with 8 vertices from the cache tmp/clanok-2-checks/graphs8.json if present (read-only).
For every ordered pair (u, v) (n <= 7) or unordered pair (n = 8) with c(u,v) >= 1:

  L1.1  cp(u,v) = c(u,v)  <=>  some minimum cut contains a u-v path            (n <= 7: against mcp.cp_brute)
  L1.3  a u-v path P lies in a minimum cut  <=>  c(even(P), odd(P)) = c(u,v)   (every path inside a minimum cut,
        and every alternating flow path of length <= 5 that is not inside one)
  O5    G' = G + w, N(w) = {u, v}: c' = c + 1, d' = min(d, 2), same answer      (n <= 7)
  L3.1  no vertex of a path inside a minimum cut lies in a set X subset V - {u,v} with |delta(X)| <= 3
  L3.2  internal vertices of such a path have degree >= 4; if c(u,v) >= 3 (>= 4) they have c(x,u) >= 3 (>= 4)
  L3.4  for any two minimum cuts A, B: no edge between A - B and B - A; A & B and A | B are minimum cuts;
        no vertex of degree 2 other than u, v is adjacent to both A - B and B - A (u or v can be: the 4-cycle)
Output: results-lemmas.txt.
"""

import itertools
import json
import os
import sys
import time
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
CHECKS = os.path.normpath(os.path.join(HERE, "..", "..", "checks"))
sys.path.insert(0, CHECKS)

import mcp  # noqa: E402  (read-only)
import exact as ex  # noqa: E402

CACHE8 = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "tmp", "clanok-2-checks", "graphs8.json"))


def paths_in_cut(g, u, v, A):
    """All simple u-v paths of the graph (V, delta(A)) as vertex tuples."""
    allowed = set(ex.boundary(g, A))
    res = []
    vis = {u}
    path = [u]

    def rec(x):
        if x == v:
            res.append(tuple(path))
            return
        for y, e in g.adj[x]:
            if e in allowed and y not in vis:
                vis.add(y)
                path.append(y)
                rec(y)
                path.pop()
                vis.discard(y)

    rec(u)
    return res


def small_sets(g, u, v, bound=3):
    """All X subset V - {u, v}, X non-empty, |delta(X)| <= bound (as frozensets)."""
    others = [x for x in range(g.n) if x != u and x != v]
    res = []
    for r in range(1, len(others) + 1):
        for X in itertools.combinations(others, r):
            Xs = set(X)
            if len(ex.boundary(g, Xs)) <= bound:
                res.append(frozenset(Xs))
    return res


def check_graph(args):
    n, es, ordered, with_cp = args
    g = ex.UG(n, es)
    G = mcp.Gr(n, es)
    cnt = dict(pairs=0, yes=0, paths=0, l13_neg=0)
    fails = []
    pairs = [(u, v) for u in range(n) for v in range(n) if u != v and (ordered or u < v)]
    smalls = {}
    lam = {}
    for u, v in pairs:
        c, cuts = ex.min_cuts_pq(g, u, v)
        if c == 0:
            continue
        cnt["pairs"] += 1
        allpaths = set()
        for A in cuts:
            for p in paths_in_cut(g, u, v, A):
                allpaths.add(p)
        ans = bool(allpaths)
        cnt["yes"] += ans
        cnt["paths"] += len(allpaths)
        if with_cp:
            cp = mcp.cp_brute(G, u, v)[0]
            if (cp == c) != ans:
                fails.append(("L1.1", n, es, u, v))
        # L1.3 positive direction and L3.1, L3.2
        if allpaths:
            key = (u, v) if u < v else (v, u)
            if key not in smalls:
                smalls[key] = small_sets(g, u, v, 3)
        for p in allpaths:
            ev = [p[i] for i in range(0, len(p), 2)]
            od = [p[i] for i in range(1, len(p), 2)]
            if ex.maxflow_sets(g, ev, od, limit=c + 1)[0] != c:
                fails.append(("L1.3+", n, es, u, v, p))
            inner = set(p[1:-1])
            for X in smalls[(u, v) if u < v else (v, u)]:
                if X & inner:
                    fails.append(("L3.1", n, es, u, v, p, sorted(X)))
                    break
            for x in inner:
                if len(g.adj[x]) < 4:
                    fails.append(("L3.2deg", n, es, u, v, p))
                for t in (3, 4):
                    if c >= t:
                        if (x, u) not in lam:
                            lam[(x, u)] = ex.cut_value(g, x, u)
                        if lam[(x, u)] < t:
                            fails.append(("L3.2c%d" % t, n, es, u, v, p))
        # L1.3 negative direction: alternating flow paths of length <= 5 that are not inside a minimum cut
        _, _, flow = ex.maxflow_sets(g, [u], [v], want_flow=True)
        edges = g.edges

        def fwd(x, e):
            return (flow[e] > 0) == (x == edges[e][0])

        stack = [((u,), )]
        cand = []

        def rec(path):
            x = path[-1]
            if x == v:
                cand.append(path)
                return
            if len(path) - 1 >= 5:
                return
            want_out = ((len(path) - 1) % 2 == 0)
            for y, e in g.adj[x]:
                if flow[e] != 0 and y not in path and fwd(x, e) == want_out:
                    rec(path + (y,))

        rec((u,))
        for p in cand:
            ev = [p[i] for i in range(0, len(p), 2)]
            od = [p[i] for i in range(1, len(p), 2)]
            inside = ex.maxflow_sets(g, ev, od, limit=c + 1)[0] == c
            if inside != (p in allpaths):
                fails.append(("L1.3", n, es, u, v, p))
            if not inside:
                cnt["l13_neg"] += 1
        # L3.4 crossing minimum cuts
        cutset = set(cuts)
        for A, B in itertools.combinations(cuts, 2):
            AB, BA = A - B, B - A
            if any((a in AB and b in BA) or (a in BA and b in AB) for a, b in edges):
                fails.append(("L3.4edge", n, es, u, v))
            if (A & B) not in cutset or (A | B) not in cutset:
                fails.append(("L3.4lattice", n, es, u, v))
            for z in range(n):
                if z != u and z != v and len(g.adj[z]) == 2:
                    nb = [y for y, _ in g.adj[z]]
                    if (nb[0] in AB and nb[1] in BA) or (nb[0] in BA and nb[1] in AB):
                        fails.append(("L3.4ear", n, es, u, v))
        if with_cp and ordered:
            # O5
            gp = ex.UG(n + 1, list(es) + [(u, n), (v, n)])
            c2, cuts2 = ex.min_cuts_pq(gp, u, v)
            d = ex.bfs_dist(g, u)[v]
            d2 = ex.bfs_dist(gp, u)[v]
            ans2 = any(ex.cut_graph_path(gp, A, u, v) is not None for A in cuts2)
            if c2 != c + 1 or d2 != min(d, 2) or ans2 != ans:
                fails.append(("O5", n, es, u, v))
    return cnt, fails


def main():
    t0 = time.time()
    jobs = [(n, es, True, True) for n, es in mcp.atlas_pairs(2, 7)]
    n8 = 0
    if os.path.exists(CACHE8):
        with open(CACHE8) as f:
            g8 = json.load(f)
        jobs += [(8, [tuple(e) for e in es], False, False) for es in g8]
        n8 = len(g8)
    with Pool(30) as pool:
        res = pool.map(check_graph, jobs, chunksize=20)
    tot = dict(pairs=0, yes=0, paths=0, l13_neg=0)
    fails = []
    for cnt, f in res:
        for k in tot:
            tot[k] += cnt[k]
        fails += f
    lines = ["check_lemmas.py: lemmas of theory-hardness.md on all connected graphs with 2..7 vertices (ordered pairs)"
             " and %d connected graphs with 8 vertices (unordered pairs)" % n8, "",
             "graphs: %d; pairs with c(u,v) >= 1: %d; pairs with a path inside a minimum cut: %d; such paths: %d"
             % (len(jobs), tot["pairs"], tot["yes"], tot["paths"]),
             "alternating flow paths of length <= 5 not inside a minimum cut (negative cases of L1.3): %d" % tot["l13_neg"],
             "checks: L1.1 (n <= 7), L1.3 both directions, O5 (n <= 7, ordered pairs), L3.1, L3.2, L3.4",
             "failures: %d" % len(fails)]
    by = {}
    for f in fails:
        by[f[0]] = by.get(f[0], 0) + 1
    lines.append("failures by check: %s" % by)
    for f in fails[:15]:
        lines.append("  " + repr(f))
    lines.append("Time %.0f s." % (time.time() - t0))
    with open(os.path.join(HERE, "results-lemmas.txt"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
