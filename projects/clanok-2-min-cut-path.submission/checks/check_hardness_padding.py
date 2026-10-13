"""S12: padding a pair with c(u,v) >= 2 to a pair with c = 2.

G' is G plus three new vertices u', s1, s2 and the edges u's1, s1u, u's2, s2u (two internally disjoint paths of
length two from u' to u).  For all connected graphs with 2..6 vertices (--maxn) and all ordered pairs (u, v) with
c(u,v) >= 2 the script asserts
  c(u',v) = 2 and d(u',v) = d(u,v) + 2
  cp(u',v) = d(u',v)  iff  G has a shortest u-v path P with u, v disconnected in G - E(P)
                      iff  cp(u,v) = d(u,v)           (the second equivalence is Corollary 3.12 of article 1)
  every shortest u'-v path has the form u' s_i u + (shortest u-v path), and it separates u' from v iff its
  u-v part separates u from v
and asserts the decomposition of (G', u', v) in two separate cases:
  c_G(u,v) >= 3:  F' = the four new edges, and the whole of V(G) is one square (the piece of v), k = 2
  c_G(u,v) = 2:   the minimum cuts of G belong to F(u',v) as well: F' = F + the four new edges, the squares of G'
                  are {u'} and the squares of G, so V(G) is NOT one square
(the statement "the whole of G is one square" needs the hypothesis c_G(u,v) >= 3).  The instances produced by the
reduction of article 1 (c(u,v) between 9 and 20) are padded and checked as well.

Run:  python check_hardness_padding.py [--maxn 7]
Output: results-hardness-padding.txt
"""

import argparse
import os
import sys
import time
from collections import defaultdict
from multiprocessing import Pool

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp import *  # noqa: E402,F401,F403
from check_structure import Tally  # noqa: E402


def pad(g, u):
    n = g.n
    up, s1, s2 = n, n + 1, n + 2
    edges = list(g.edges) + [(up, s1), (s1, u), (up, s2), (s2, u)]
    return Gr(n + 3, edges), up, (s1, s2)


def shortest_paths(g, u, v):
    d = bfs(g, u)[v]
    return [(vs, es) for vs, es in simple_paths(g, u, v, maxlen=d) if len(es) == d]


def run_graph(args):
    n, es = args
    g = Gr(n, es)
    T = Tally()
    T.stat("graphs")
    for u in range(n):
        for v in range(n):
            if u == v:
                continue
            c = edge_conn(g, u, v)
            if c < 2:
                continue
            T.ctx = (g, u, v)
            T.stat("pairs (u, v) with c >= 2")
            d = bfs(g, u)[v]
            gp, up, (s1, s2) = pad(g, u)
            T.ctx = (gp, up, v)
            dp = bfs(gp, up)[v]
            cp_g = cp_brute(g, u, v)[0]
            cp_gp = cp_brute(gp, up, v)[0]
            T.ok("S12-c", edge_conn(gp, up, v) == 2, "c(u', v) != 2")
            T.ok("S12-d", dp == d + 2, lambda: "d(u',v) = %d, d(u,v) = %d" % (dp, d))
            # independent: separating shortest path in G
            sep_G = any(not connected(g, u, v, removed=mask_of(es)) for vs, es in shortest_paths(g, u, v))
            sep_Gp = any(not connected(gp, up, v, removed=mask_of(es)) for vs, es in shortest_paths(gp, up, v))
            T.ok("S12-iff", (cp_gp == dp) == sep_G, lambda: "cp(u',v) = %d, d(u',v) = %d, G has a separating shortest path: %s" % (cp_gp, dp, sep_G))
            T.ok("S12-cp(G)", (cp_g == d) == sep_G, lambda: "cp(u,v) = %d, d = %d, separating shortest path in G: %s" % (cp_g, d, sep_G))
            T.ok("S12-sep", sep_Gp == sep_G, "a shortest u'-v path separates iff its u-v part does: existence differs")
            # shape of the shortest u'-v paths
            shape = True
            part_ok = True
            inner = {w for w, _ in shortest_paths(g, u, v)}
            for vs, es_ in shortest_paths(gp, up, v):
                if not (vs[0] == up and vs[1] in (s1, s2) and vs[2] == u and tuple(vs[2:]) in inner):
                    shape = False
                    continue
                rest = mask_of(g.edge_id(a, b) for a, b in zip(vs[2:], vs[3:]))
                if (not connected(gp, up, v, removed=mask_of(es_))) != (not connected(g, u, v, removed=rest)):
                    part_ok = False
            # core.tex: every u'-v path consists of u', s_j, u and a u-v path of G
            expected_paths = {(up, s) + vs for s in (s1, s2) for vs, _ in simple_paths(g, u, v)}
            T.ok("S12-allpaths", {vs for vs, _ in simple_paths(gp, up, v)} == expected_paths,
                 "the u'-v paths of G' are not exactly u', s_j, u followed by a u-v path of G")
            T.ok("S12-shape", shape, "a shortest u'-v path is not u' s_i u followed by a shortest u-v path")
            T.ok("S12-part", part_ok, "a shortest u'-v path separates u' from v, but its u-v part does not separate u from v (or conversely)")
            T.stat("pairs with cp(u',v) = d(u',v)" if cp_gp == dp else "pairs with cp(u',v) = d(u',v) + 1")
            # decomposition of (G', u', v)
            dec, cuts, problems = brute_decomp(gp, up, v)
            decG, _, _ = brute_decomp(g, u, v) if c == 2 else (None, None, None)
            new_edges = {gp.edge_id(up, s1), gp.edge_id(s1, u), gp.edge_id(up, s2), gp.edge_id(s2, u)}
            order = dec.square_order()
            k = len(order) if order else -1
            T.stat("decomposition of (G', u', v): k = %d squares, c(u,v) %s" % (k, "= 2" if c == 2 else ">= 3"))
            if c >= 3:
                whole = (dec.comp[v] == dec.comp[u] and sorted(dec.pieces[dec.pv]) == list(range(n)))
                T.ok("S12-one-square", set(dec.F) == new_edges and whole and k == 2 and len(dec.pieces) == 4,
                     lambda: "F' = %s, pieces %s" % (dec.F, dec.pieces))
                # core.tex: S_1 = {u'}, S_2 = V, links {s_1}, {s_2}; a_2 = b_2 = u and c_2 = d_2 = v
                T.ok("S12-terminals", dec.entering_terminals(dec.pv) == (u, u) and dec.leaving_terminals(dec.pv) == (v, v)
                     and sorted(sorted(dec.pieces[p]) for p in range(dec.np) if not dec.is_square[p]) == [[s1], [s2]]
                     and dec.pieces[dec.pu] == [up],
                     lambda: "terminals of S_2: %s, %s" % (dec.entering_terminals(dec.pv), dec.leaving_terminals(dec.pv)))
            else:
                # compared by endpoints, because the edge ids of G and G' differ
                ok_f = ({gp.edges[e] for e in dec.F} == {g.edges[e] for e in decG.F} | {gp.edges[e] for e in new_edges})
                sq_G = sorted(sorted(decG.pieces[p]) for p in range(decG.np) if decG.is_square[p])
                sq_Gp = sorted(sorted(dec.pieces[p]) for p in range(dec.np) if dec.is_square[p] and p != dec.comp[up])
                T.stat("c = 2: F' = F + 4 new edges" if ok_f else "c = 2: F' differs from F + 4 new edges")
                T.stat("c = 2: squares of G' = {u'} + squares of G" if sq_G == sq_Gp else "c = 2: squares of G' differ from {u'} + squares of G")
                # for c(u,v) = 2 the minimum cuts of G belong to F(u', v) as well, so V(G) is NOT one square
                T.ok("S12-c2-F", ok_f, lambda: "F' = %s, F = %s" % (sorted(dec.F), sorted(decG.F)))
                T.ok("S12-c2-squares", sq_G == sq_Gp, lambda: "squares of G': %s, squares of G: %s" % (sq_Gp, sq_G))
                T.ok("S12-c2-not-one-square", not any(set(range(n)) <= set(p) for p in dec.pieces),
                     "all of V(G) lies in one piece of G' although c(u,v) = 2")
    return T.clean()


NAMES = ["S12-c", "S12-d", "S12-iff", "S12-cp(G)", "S12-sep", "S12-allpaths", "S12-shape", "S12-part", "S12-one-square", "S12-terminals",
         "S12-c2-F", "S12-c2-squares", "S12-c2-not-one-square"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--maxn", type=int, default=6)
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
    out("check_hardness_padding.py: S12, all %d connected graphs with 2..%d vertices, all ordered pairs with c(u,v) >= 2" % (len(graphs), opts.maxn))
    T = Tally()
    with Pool(opts.jobs) as pool:
        for r in pool.imap(run_graph, graphs, chunksize=2):
            T.merge(r)
    out("")
    for key in sorted(T.stats):
        out("  %-70s %d" % (key, T.stats[key]))
    out("")
    for name in NAMES:
        if T.count.get(name):
            out("  %-16s %8d assertions, %d failed  %s" % (name, T.count[name], T.nfail[name], "PASS" if not T.nfail[name] else "FAIL"))
    for name in NAMES:
        if name in T.first:
            key, rec = T.first[name]
            out("  FAILURE %s: n=%d, u=%d, v=%d, edges %s" % (name, rec["n"], rec["u"], rec["v"], fmt_edges(rec["edges"])))
            out("      %s" % rec["info"])
    # -- the hard instances of article 1 ------------------------------------------------------------
    out("")
    out("Instances produced by the reduction of article 1 (checks of article 1, imported read-only; connecting paths of one edge,")
    out("which does not change any connectivity between u and v):")
    sys.dont_write_bytecode = True
    a1 = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "clanok-1-min-cut-path.submission", "checks"))
    sys.path.insert(1, a1)
    from reduction import Reduction
    A = Tally()
    for n, clauses in [(1, [(1, 1, 1)]), (2, [(1, 2, -2), (-1, 2, 2)]), (3, [(1, 2, 3), (-1, -2, 3)]), (3, [(1, 2, 3)])]:
        R = Reduction(n, clauses, seed=1, lengthen=False)
        verts = sorted(R.adj)
        idx = {x: i for i, x in enumerate(verts)}
        g = Gr(len(verts), [(idx[a], idx[b]) for a in R.adj for b in R.adj[a] if a < b])
        u, v = idx[R.u], idx[R.v]
        gp, up, (s1, s2) = pad(g, u)
        A.ctx = (gp, up, v)
        c, d = edge_conn(g, u, v), bfs(g, u)[v]
        dec, cuts, problems = brute_decomp(gp, up, v, fast=True)
        new_edges = {gp.edge_id(up, s1), gp.edge_id(s1, u), gp.edge_id(up, s2), gp.edge_id(s2, u)}
        order = dec.square_order()
        ok = (edge_conn(gp, up, v) == 2 and bfs(gp, up)[v] == d + 2 and set(dec.F) == new_edges
              and len(dec.pieces) == 4 and sorted(dec.pieces[dec.pv]) == list(range(g.n)) and order is not None and len(order) == 2)
        A.ok("S12-article1", ok, "padded instance: F' = %s, pieces %s" % (dec.F, dec.pieces))
        out("  formula with %d variables, %d clauses: |V| = %d, |E| = %d, c(u,v) = %d, d(u,v) = %d;  padded: c(u',v) = %d, d(u',v) = %d, "
            "F' = the four new edges: %s, V(G) is one piece (the piece of v): %s, k = %d squares"
            % (n, len(clauses), g.n, g.m, c, d, edge_conn(gp, up, v), bfs(gp, up)[v], set(dec.F) == new_edges,
               sorted(dec.pieces[dec.pv]) == list(range(g.n)), len(order)))
    out("  S12-article1: %d assertions, %d failed  %s" % (A.count["S12-article1"], A.nfail["S12-article1"], "PASS" if not A.nfail["S12-article1"] else "FAIL"))
    out("")
    out("Time %.0f s." % (time.time() - started))
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "results-hardness-padding.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
