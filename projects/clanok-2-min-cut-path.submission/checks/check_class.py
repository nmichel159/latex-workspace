"""S13: the class DC.

For every connected graph with 2..--maxn vertices:
  S13-eq       the relation c(x,y) >= 3 is transitive (so it is an equivalence relation on the vertices)
  S13-iff      G is in DC  iff  any two vertices of one class of the relation are at distance at most two
  S13-diam2    diameter at most two implies G in DC
  S13-cactus   a cactus graph (every block an edge or a cycle; equivalently c(x,y) <= 2 for all pairs) is in DC
  S13-formula  cp = c + d - 1 for every pair of every graph of diameter at most two and every cactus graph
and the graphs of DC in which the formula fails (counts per number of vertices; the two six-vertex graphs are
identified with the counterexamples (a) and (b) of the research map).

The preliminaries of drafts/core.tex are tested as well (names PRE-...): Corollary 3.12 of article 1 (cp = d iff
a shortest path separates), the bounds, Proposition "easy pairs" (i)-(iv), the lemma on minimum cuts (two
components, C = delta(A) for exactly one A; n <= 7) and the parity of |P n delta(A)| (n <= 6), the uncrossing
identity (n <= 6, all pairs of vertex sets) and the remark that the 2-edge-connected components of a graph
in DC lie in DC.

Run:  python check_class.py [--maxn 8]
Output: results-class.txt
"""

import argparse
import os
import sys
import time
from collections import Counter
from multiprocessing import Pool

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp import *  # noqa: E402,F401,F403
from check_structure import Tally  # noqa: E402


def is_cactus(g):
    """Every block is an edge or a cycle (networkx)."""
    import networkx as nx
    G = nx.Graph(g.edges)
    for block in nx.biconnected_components(G):
        k = len(block)
        if k > 2 and G.subgraph(block).number_of_edges() != k:
            return False
    return True


def preliminaries_pair(g, x, y, d, c, cp, T):
    """Statements of the preliminaries of drafts/core.tex for one pair: Corollary 3.12 of article 1 (Lemma
    'basic bounds'), the lemma on minimum cuts, and Proposition 'easy pairs'."""
    full = g.full()
    n = g.n
    shortest = [es for vs, es in simple_paths(g, x, y, maxlen=d) if len(es) == d]
    sep = any(not connected(g, x, y, removed=mask_of(es)) for es in shortest)
    T.ok("PRE-cor312", (cp == d) == sep, lambda: "cp = %d, d = %d, separating shortest path: %s" % (cp, d, sep))
    T.ok("PRE-bounds", max(c, d) <= cp <= c + d - 1, lambda: "c=%d d=%d cp=%d" % (c, d, cp))
    if c == 2:
        T.ok("PRE-easy-iii", cp in (d, d + 1), lambda: "c=2 d=%d cp=%d" % (d, cp))
    if d == 2:
        T.ok("PRE-easy-iv", cp in (c, c + 1), lambda: "d=2 c=%d cp=%d" % (c, cp))
    if n > 7:
        return
    cc, cuts = min_cuts_by_sets(g, x, y)
    # Lemma "minimum cuts": two components, C = delta(A) for exactly one A (the component of x)
    ok = True
    for C in cuts:
        comp, k = components(g, C)
        As = [A for A in range(1 << n) if (A >> x) & 1 and not (A >> y) & 1
              and sum(1 << e for e, (a, b) in enumerate(g.edges) if ((A >> a) ^ (A >> b)) & 1) == C]
        if k != 2 or len(As) != 1 or As[0] != component_mask(g, x, C):
            ok = False
    T.ok("PRE-minimum-cuts", ok, "a minimum cut leaves not exactly two components or is not the boundary of exactly one set A")
    # Proposition "open pairs": cp = c iff some minimum cut contains a u-v path; such a path has an odd number of
    # edges, at least three if d = 2 (any graph, any pair)
    lens = [len(es) for C in cuts for vs, es in simple_paths(g, x, y, removed=full ^ C)]
    T.ok("PRE-open-pairs", (cp == c) == bool(lens) and all(L % 2 == 1 for L in lens) and (d != 2 or all(L >= 3 for L in lens)),
         lambda: "cp = %d, c = %d, d = %d, lengths of the paths in minimum cuts %s" % (cp, c, d, sorted(set(lens))))
    if n <= 6:
        paths = simple_paths(g, x, y)
        ok = True
        for A in range(1 << n):
            if (A >> x) & 1 and not (A >> y) & 1:
                bmask = sum(1 << e for e, (a, b) in enumerate(g.edges) if ((A >> a) ^ (A >> b)) & 1)
                if any(popcount(bmask & mask_of(es)) % 2 != 1 for vs, es in paths):
                    ok = False
        T.ok("PRE-parity", ok, "a u-v path meets some delta(A) in an even number of edges")
    if d == 1:
        e = g.edge_id(x, y)
        T.ok("PRE-easy-i", cp == c and all(((C >> e) & 1) and is_cutpath(g, x, y, C) and popcount(C) == cp for C in cuts),
             lambda: "d = 1: cp = %d, c = %d" % (cp, c))
    if c == 1:
        T.ok("PRE-easy-ii", cp == d and all(is_cutpath(g, x, y, mask_of(es)) and len(es) == cp for es in shortest),
             lambda: "c = 1: cp = %d, d = %d" % (cp, d))


def run_graph(args):
    n, es = args
    g = Gr(n, es)
    T = Tally()
    T.ctx = (g, 0, 1)
    D = dist_matrix(g)
    C = [[0] * n for _ in range(n)]
    for x in range(n):
        for y in range(x + 1, n):
            C[x][y] = C[y][x] = edge_conn(g, x, y)
    R = [[x != y and C[x][y] >= 3 for y in range(n)] for x in range(n)]
    trans = all(not (R[x][y] and R[y][z]) or x == z or R[x][z] for x in range(n) for y in range(n) for z in range(n))
    T.ok("S13-eq", trans, "c(x,y) >= 3 and c(y,z) >= 3 but c(x,z) < 3")
    dc = all(D[x][y] <= 2 or C[x][y] <= 2 for x in range(n) for y in range(x + 1, n))
    # classes of the relation
    cls = list(range(n))

    def find(a):
        while cls[a] != a:
            cls[a] = cls[cls[a]]
            a = cls[a]
        return a
    for x in range(n):
        for y in range(x + 1, n):
            if R[x][y]:
                cls[find(x)] = find(y)
    classes_ok = all(D[x][y] <= 2 for x in range(n) for y in range(x + 1, n) if find(x) == find(y))
    T.ok("S13-iff", dc == classes_ok, "DC is %s, classes condition is %s" % (dc, classes_ok))
    diam = max(max(row) for row in D)
    cactus = max(C[x][y] for x in range(n) for y in range(x + 1, n)) <= 2
    T.ok("S13-cactus-def", cactus == is_cactus(g), "c <= 2 for all pairs differs from the block characterization")
    if diam <= 2:
        T.ok("S13-diam2", dc, "a graph of diameter two outside DC")
    if cactus:
        T.ok("S13-cactus", dc, "a cactus outside DC")
    all_formula = True
    for x in range(n):
        for y in range(x + 1, n):
            cp = cp_brute(g, x, y)[0]
            if cp != C[x][y] + D[x][y] - 1:
                all_formula = False
            preliminaries_pair(g, x, y, D[x][y], C[x][y], cp, T)
    if n <= 6:
        # Lemma "uncrossing": |d(A n B)| + |d(A u B)| = |d(A)| + |d(B)| - 2 m(A, B), for all A, B
        full = (1 << n) - 1

        def bd(A):
            return sum(1 for (a, b) in g.edges if ((A >> a) ^ (A >> b)) & 1)
        ok = True
        for A in range(1 << n):
            for B in range(1 << n):
                m_ab = sum(1 for (a, b) in g.edges if (((A & ~B) >> a & 1) and ((B & ~A) >> b & 1)) or (((A & ~B) >> b & 1) and ((B & ~A) >> a & 1)))
                if bd(A & B) + bd(A | B) != bd(A) + bd(B) - 2 * m_ab:
                    ok = False
        T.ok("PRE-uncrossing", ok, "the identity of the uncrossing lemma fails")
    if dc:
        # Remark "bridges": the 2-edge-connected components K of a graph of DC lie in DC
        br = mask_of(bridges(g))
        comp, k = components(g, br)
        for j in range(k):
            K = [x for x in range(n) if comp[x] == j]
            H, _, _ = induced(g, K)
            T.ok("PRE-bridges-DC", in_dc(H)[0], "a 2-edge-connected component of a graph in DC is not in DC")
    if diam <= 2 or cactus:
        T.ok("S13-formula", all_formula, "cp != c + d - 1 in a graph of diameter two or a cactus")
    T.stat("graphs with %d vertices" % n)
    if dc:
        T.stat("in DC, %d vertices" % n)
        if not all_formula:
            T.stat("in DC with a pair cp < c + d - 1, %d vertices" % n)
            T.stat("FAIL:%d:%s" % (n, ";".join("%d-%d" % e for e in g.edges)))
    else:
        T.stat("not in DC, %d vertices" % n)
    return T.clean()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--maxn", type=int, default=8)
    ap.add_argument("--jobs", type=int, default=24)
    opts = ap.parse_args()
    lines = []

    def out(s=""):
        print(s, flush=True)
        lines.append(s)

    started = time.time()
    graphs = []
    for n in range(2, opts.maxn + 1):
        graphs.extend(connected_graphs(n, SCRATCH))
    out("check_class.py: S13, all %d connected graphs with 2..%d vertices" % (len(graphs), opts.maxn))
    T = Tally()
    with Pool(opts.jobs) as pool:
        for r in pool.imap(run_graph, graphs, chunksize=8):
            T.merge(r)
    out("")
    for key in sorted(k for k in T.stats if not k.startswith("FAIL:")):
        out("  %-60s %d" % (key, T.stats[key]))
    for name in ("S13-eq", "S13-iff", "S13-cactus-def", "S13-diam2", "S13-cactus", "S13-formula",
                 "PRE-cor312", "PRE-bounds", "PRE-easy-i", "PRE-easy-ii", "PRE-easy-iii", "PRE-easy-iv",
                 "PRE-minimum-cuts", "PRE-open-pairs", "PRE-parity", "PRE-uncrossing", "PRE-bridges-DC"):
        if T.count[name]:
            out("  %-16s %7d assertions, %d failed  %s" % (name, T.count[name], T.nfail[name], "PASS" if not T.nfail[name] else "FAIL"))
        if name in T.first:
            key, rec = T.first[name]
            out("  FAILURE %s: n=%d, edges %s: %s" % (name, rec["n"], fmt_edges(rec["edges"]), rec["info"]))
    # identify the six-vertex graphs
    import networkx as nx
    base = [("t", "a"), ("t", "v"), ("a", "u"), ("a", "b"), ("v", "b"), ("u", "s"), ("s", "b")]
    known = [nx.Graph(base), nx.Graph(base + [("a", "v"), ("u", "b")])]
    six = [k for k in T.stats if k.startswith("FAIL:6:")]
    out("")
    out("Graphs with 6 vertices in DC in which cp < c + d - 1 for some pair: %d" % len(six))
    for k in six:
        G = nx.Graph([tuple(map(int, e.split("-"))) for e in k.split(":")[2].split(";")])
        out("  edges %s: isomorphic to counterexample (a): %s, to (b): %s" % (k.split(":")[2], nx.is_isomorphic(G, known[0]), nx.is_isomorphic(G, known[1])))
    out("Time %.0f s." % (time.time() - started))
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "results-class.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
