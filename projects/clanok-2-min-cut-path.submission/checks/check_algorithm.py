"""Task C: the reference algorithm of S11 (algorithm.py) against brute force.

  (i)   all connected graphs with 2..7 vertices (all of them lie in DC, see README), all ordered pairs with
        c(u,v) <= 2: value of cp, and that the returned edge set really contains a u-v path and a u-v cut and
        has cp edges
  (ii)  on the same pairs with c = 2: F, its orientation, the pieces, the squares and lambda^-, lambda^+
        equal the brute-force ones (this part holds in ALL graphs, class or not)
  (iii) random instances with long decompositions in DC (chains.py); at least --instances accepted
  (iv)  graphs outside DC with c(u,v) = 2: how often the algorithm gives a wrong value (report only); the
        value is asserted to be right whenever (*) holds: every entering terminal of every square is at
        distance at most two from every leaving terminal of the same square (claimed in drafts/core.tex)
  (vi)  coarser decompositions (F' = union of some minimum cuts, S14): the algorithm is right whenever (*)
        holds for the coarser squares
  also: pairs with c >= 3 are refused (three augmentations), and the strong components of the residual digraph
        are exactly the pieces (a remark in the notes of the math core)

Run:  python check_algorithm.py [--instances 3000] [--general 3000] [--jobs 24]
Output: results-algorithm.txt
"""

import argparse
import itertools
import os
import random
import sys
import time
from collections import defaultdict
from multiprocessing import Pool

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp import *  # noqa: E402,F401,F403
from check_structure import Tally  # noqa: E402
import algorithm  # noqa: E402


def star_condition(g, u, v, res):
    """The condition (*) of the remark after the correctness proof: in every square of the decomposition in `res`,
    every entering terminal is at distance at most two (in G) from every leaving terminal."""
    comp = res["comp"]
    for sq in res["squares"]:
        ents = {u} if sq == comp[u] else {res["head"][e] for e in res["ent"][sq]}
        leas = {v} if sq == comp[v] else {res["tail"][e] for e in res["lea"][sq]}
        for x in ents:
            dist = bfs(g, x)
            if any(dist[y] > 2 for y in leas):
                return False
    return True


def compare(g, u, v, T, mut=None, brute=None, F_checks=True, label=""):
    """algorithm.solve against brute force on one ordered pair with c(u,v) <= 2."""
    T.ctx = (g, u, v)
    c = edge_conn(g, u, v)
    d = bfs(g, u)[v]
    res = algorithm.solve(g, u, v, mutation=mut)
    cpb = brute if brute is not None else cp_brute(g, u, v)[0]
    T.ok("ALG-applies", res is not None, "the algorithm returned None for c = %d" % c)
    if res is None:
        return None
    T.ok("ALG-c-d", res["c"] == c and res["d"] == d, lambda: "algorithm c=%d d=%d, brute force c=%d d=%d" % (res["c"], res["d"], c, d))
    value_ok = res["cp"] == cpb
    T.ok("ALG-value", value_ok, lambda: "algorithm cp = %d (%s), brute force cp = %d, d = %d, c = %d" % (res["cp"], res["case"], cpb, d, c))
    S = res["cutpath"]
    T.ok("ALG-cutpath", is_cutpath(g, u, v, S) and popcount(S) == res["cp"],
         lambda: "returned set %s is not a cut-path with cp = %d edges" % (bits(S), res["cp"]))
    T.stat("pairs c = %d" % c)
    if c == 2:
        T.stat(label + "pairs with c = 2: cp = d" if cpb == d else label + "pairs with c = 2: cp = d + 1")
        if mut is None:
            star = star_condition(g, u, v, res)
            T.stat(label + "pairs where every entering terminal is within distance 2 of every leaving terminal (*)" if star
                   else label + "pairs where (*) fails")
            if star:
                T.ok("ALG-star", value_ok, lambda: "(*) holds but the algorithm gives %d, brute force %d" % (res["cp"], cpb))
            else:
                T.stat(label + "pairs where (*) fails and the algorithm is wrong" if not value_ok else label + "pairs where (*) fails and the algorithm is right")
        if not value_ok:
            T.stat(label + "wrong value: algorithm %s, brute force %s" % ("d + 1" if res["cp"] == d + 1 else "d" if res["cp"] == d else "other",
                                                                          "d + 1" if cpb == d + 1 else "d" if cpb == d else "other"))
        if mut is None:
            # (remark in the notes of the math core) the strong components of the residual digraph are exactly the pieces
            T.ok("ALG-scc", {frozenset(x for x in range(g.n) if res["scc"][x] == s) for s in set(res["scc"])}
                 == {frozenset(x for x in range(g.n) if res["comp"][x] == p) for p in set(res["comp"])},
                 lambda: "strong components of the residual digraph differ from the pieces")
        if F_checks:
            dec, cuts, problems = brute_decomp(g, u, v)
            T.ok("ALG-F", res["F"] == dec.F, lambda: "algorithm F = %s, brute force F = %s" % (res["F"], dec.F))
            T.ok("ALG-tail", res["tail"] == dec.tail, lambda: "orientation differs: %s vs %s" % (res["tail"], dec.tail))
            mine = {frozenset(x for x in range(g.n) if res["comp"][x] == p) for p in set(res["comp"])}
            theirs = {frozenset(p) for p in dec.pieces}
            T.ok("ALG-pieces", mine == theirs, lambda: "pieces differ")
            sq_mine = {frozenset(x for x in range(g.n) if res["comp"][x] == p) for p in res["squares"]}
            sq_theirs = {frozenset(dec.pieces[p]) for p in range(dec.np) if dec.is_square[p]}
            T.ok("ALG-squares", sq_mine == sq_theirs, lambda: "squares differ")
            T.ok("ALG-lambda", res["lam_minus"] == dec.vec_dist(u) and res["lam_plus"] == dec.vec_dist(v, reverse=True),
                 lambda: "lambda^- or lambda^+ differ from the breadth-first searches in G-vector")
    return res, cpb


def run_small(args):
    """Returns (graph in DC, Tally)."""
    n, es, mut = args
    g = Gr(n, es)
    dc, _ = in_dc(g)
    T = Tally()
    T.stat("graphs")
    for u in range(n):
        for v in range(n):
            if u == v:
                continue
            if edge_conn(g, u, v, limit=3) <= 2:
                compare(g, u, v, T, mut=mut)
            elif mut is None:
                # c >= 3: the decision "c <= 2" (three augmentations) must make the algorithm refuse
                T.ctx = (g, u, v)
                T.ok("ALG-c3-refused", algorithm.solve(g, u, v) is None, "the algorithm answered for a pair with c >= 3")
    return dc, T.clean()


def run_chain(args):
    seed, mut = args
    import chains
    rng = random.Random(seed)
    inst = chains.random_dc_chain(rng)
    T = Tally()
    if inst is None:
        T.stat("seeds rejected (not in DC, c != 2, or duplicate edge)")
        return T
    g, u, v = inst
    T.stat("DC instances")
    T.stat("DC instances: vertices", g.n)
    T.stat("DC instances: edges", g.m)
    dec, cuts, problems = brute_decomp(g, u, v, fast=True)
    order = dec.square_order()
    if order:
        T.stat("DC instances with k = %d squares" % len(order))
    compare(g, u, v, T, mut=mut, F_checks=False, label="DC: ")
    # F, pieces and so on are tested against the fast brute force as well
    res = algorithm.solve(g, u, v, mutation=mut)
    T.ctx = (g, u, v)
    T.ok("ALG-F", res["F"] == dec.F and res["tail"] == dec.tail, lambda: "F or orientation differ")
    return T.clean()


def run_general(args):
    seed, mut = args
    import chains
    rng = random.Random(seed)
    inst = chains.random_general_chain(rng)
    T = Tally()
    if inst is None:
        T.stat("seeds rejected (in DC, c != 2, or duplicate edge)")
        return T
    g, u, v = inst
    T.stat("non-DC instances")
    T.stat("non-DC instances: vertices", g.n)
    r = compare(g, u, v, T, mut=mut, F_checks=False, label="non-DC: ")
    if r is not None:
        res, cpb = r
        T.stat("non-DC: algorithm value below the true cp (unsound)" if res["cp"] < cpb else "non-DC: algorithm value not below the true cp")
        if res["cp"] != cpb:
            # smallest wrong instance is kept in T.first under ALG-value by compare
            pass
    return T.clean()


def coarse_pair(g, u, v, T, rng, fast):
    """The algorithm on coarser decompositions (F' = union of some minimum cuts): whenever the distance
    condition (*) holds for the coarser squares, the value and the cut-path must be right."""
    dec, cuts, problems = brute_decomp(g, u, v, fast=fast)
    q = len(cuts)
    if q < 2:
        return
    subs = set()
    if q <= 5:
        subs = {s for r in range(1, q) for s in itertools.combinations(range(q), r)}
    else:
        for _ in range(6):
            subs.add(tuple(sorted(rng.sample(range(q), rng.randint(1, min(q - 1, 6))))))
    cpb = cp_brute(g, u, v)[0]
    for sub in sorted(subs):
        Fsub = {e for i in sub for e in cuts[i][:2]}
        res = algorithm.solve(g, u, v, restrict_F=Fsub)
        ok = res["cp"] == cpb and is_cutpath(g, u, v, res["cutpath"]) and popcount(res["cutpath"]) == res["cp"]
        T.stat("coarser decompositions tried")
        if star_condition(g, u, v, res):
            T.stat("coarser decompositions with (*)")
            T.ok("ALG-coarse", ok, lambda: "coarser decomposition from the cuts %s: algorithm cp = %d, brute force %d" % (sub, res["cp"], cpb))
        else:
            T.stat("coarser decompositions where (*) fails: algorithm right" if ok else "coarser decompositions where (*) fails: algorithm wrong")


def run_coarse_small(args):
    n, es = args
    g = Gr(n, es)
    T = Tally()
    rng = random.Random(n * 7919 + g.m)
    for u in range(n):
        for v in range(n):
            if u != v and edge_conn(g, u, v, limit=3) == 2:
                T.ctx = (g, u, v)
                coarse_pair(g, u, v, T, rng, fast=False)
    return T.clean()


def run_coarse_chain(args):
    seed, kind = args
    import chains
    rng = random.Random(seed)
    inst = chains.random_dc_chain(rng) if kind == "dc" else chains.random_general_chain(rng)
    T = Tally()
    if inst is None:
        return T
    g, u, v = inst
    T.ctx = (g, u, v)
    coarse_pair(g, u, v, T, rng, fast=True)
    return T.clean()


def crossed_path_instance(k):
    """Hand-built instance outside DC on 3k + 3 vertices: u joined to x by an edge and to y by a path with k + 1
    edges; v joined to y by an edge and to x by a path with k + 1 edges; x and y joined by a path of k edges (the
    square, with d(x,y) = k >= 3 and c(x,y) = 3).  The path u-x-...-y-v has k + 2 = d edges and separates u from v."""
    edges = []
    n = 4          # 0 = u, 1 = x, 2 = y, 3 = v

    def path(a, b, length):
        nonlocal n
        prev = a
        for _ in range(length - 1):
            edges.append((prev, n))
            prev = n
            n += 1
        edges.append((prev, b))

    edges.append((0, 1))
    edges.append((2, 3))
    path(0, 2, k + 1)
    path(1, 3, k + 1)
    path(1, 2, k)
    return Gr(n, edges), 0, 3


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instances", type=int, default=4500, help="seeds for the DC chain instances")
    ap.add_argument("--general", type=int, default=12000, help="seeds for the non-DC instances")
    ap.add_argument("--seed", type=int, default=20261012)
    ap.add_argument("--jobs", type=int, default=24)
    ap.add_argument("--maxn", type=int, default=8)
    ap.add_argument("--coarse", type=int, default=1500, help="seeds of chain instances for the coarser decompositions")
    ap.add_argument("--out", default="results-algorithm.txt")
    opts = ap.parse_args()
    lines = []

    def out(s=""):
        print(s, flush=True)
        lines.append(s)

    started = time.time()
    graphs = []
    for n in range(2, opts.maxn + 1):
        graphs.extend(connected_graphs(n, SCRATCH))
    out("check_algorithm.py: algorithm.py (S11) against brute force")
    out("")
    with Pool(opts.jobs) as pool:
        out("(i), (ii): all %d connected graphs with 2..%d vertices, all ordered pairs with c <= 2" % (len(graphs), opts.maxn))
        S = Tally()
        S8 = Tally()
        for dc, r in pool.imap(run_small, [(n, es, None) for n, es in graphs], chunksize=4):
            (S if dc else S8).merge(r)
        out("  graphs in DC: %d, graphs not in DC: %d (graphs with at most 7 vertices are all in DC)" % (S.stats["graphs"], S8.stats["graphs"]))
        out("  graphs in DC")
        for key in sorted(S.stats):
            out("    %-64s %d" % (key, S.stats[key]))
        report_alg(S, out)
        out("  graphs NOT in DC (report only: the algorithm is claimed for DC)")
        for key in sorted(S8.stats):
            out("    %-64s %d" % (key, S8.stats[key]))
        out("    wrong value on %d of %d pairs with c <= 2, invalid cut-path on %d; F, orientation, pieces, squares and lambda wrong on %d/%d/%d/%d/%d"
            % (S8.nfail["ALG-value"], S8.count["ALG-value"], S8.nfail["ALG-cutpath"], S8.nfail["ALG-F"], S8.nfail["ALG-tail"],
               S8.nfail["ALG-pieces"], S8.nfail["ALG-squares"], S8.nfail["ALG-lambda"]))
        out("    ALG-star (value right whenever (*) holds), non-DC graphs: %d assertions, %d failed  %s"
            % (S8.count["ALG-star"], S8.nfail["ALG-star"], "PASS" if not S8.nfail["ALG-star"] else "FAIL"))
        out("")
        out("(iii): random chains in DC with long decompositions, seeds %d..%d" % (opts.seed, opts.seed + opts.instances - 1))
        C = Tally()
        for r in pool.imap(run_chain, [(opts.seed + i, None) for i in range(opts.instances)], chunksize=4):
            C.merge(r)
        for key in sorted(C.stats):
            out("  %-66s %d" % (key, C.stats[key]))
        report_alg(C, out)
        n_inst = C.stats["DC instances"]
        out("  mean vertices %.1f, mean edges %.1f" % (C.stats["DC instances: vertices"] / n_inst, C.stats["DC instances: edges"] / n_inst))
        out("")
        out("(iv): random graphs outside DC with c(u,v) = 2, seeds %d..%d (report only)" % (opts.seed, opts.seed + opts.general - 1))
        N = Tally()
        for r in pool.imap(run_general, [(opts.seed + i, None) for i in range(opts.general)], chunksize=4):
            N.merge(r)
        for key in sorted(N.stats):
            out("  %-66s %d" % (key, N.stats[key]))
        wrong = N.nfail["ALG-value"]
        total = N.count["ALG-value"]
        out("  algorithm wrong on %d of %d instances (%.1f%%); cut-path invalid on %d" % (wrong, total, 100.0 * wrong / max(total, 1), N.nfail["ALG-cutpath"]))
        out("  ALG-star (value right whenever (*) holds): %d assertions, %d failed  %s"
            % (N.count["ALG-star"], N.nfail["ALG-star"], "PASS" if not N.nfail["ALG-star"] else "FAIL"))
        if "ALG-star" in N.first:
            key, rec = N.first["ALG-star"]
            out("  FAILURE ALG-star: n=%d, u=%d, v=%d, edges %s" % (rec["n"], rec["u"], rec["v"], fmt_edges(rec["edges"])))
            out("      %s" % rec["info"])
        if "ALG-value" in N.first:
            key, rec = N.first["ALG-value"]
            out("  smallest random instance with a wrong value: n=%d, u=%d, v=%d, edges %s" % (rec["n"], rec["u"], rec["v"], fmt_edges(rec["edges"])))
            out("      %s" % rec["info"])
        out("  hand-built family (crossed path of k edges as a square; vertices 0 = u, 1 = x, 2 = y, 3 = v):")
        for k in (3, 4, 5, 6):
            g, u, v = crossed_path_instance(k)
            dc, bad = in_dc(g)
            res = algorithm.solve(g, u, v)
            cpb = cp_brute(g, u, v)[0]
            out("    k = %d: n = %d, in DC: %s%s, c = %d, d = %d, cp (brute force) = %d, algorithm = %d%s"
                % (k, g.n, dc, "" if dc else " (pair %s)" % (bad,), edge_conn(g, u, v), res["d"], cpb, res["cp"],
                   "  <- WRONG" if res["cp"] != cpb else ""))
            if k == 3:
                out("      edges: %s" % fmt_edges(g.edges))
        out("")
        out("(vi): the algorithm on coarser decompositions (F' = union of some minimum cuts); graphs with 2..7 vertices, "
            "%d DC chains, %d non-DC instances" % (opts.coarse, opts.coarse))
        K = Tally()
        small = [(n, es) for n, es in graphs if n <= 7]
        for r in pool.imap(run_coarse_small, small, chunksize=4):
            K.merge(r)
        for r in pool.imap(run_coarse_chain, [(opts.seed + i, "dc") for i in range(opts.coarse)], chunksize=4):
            K.merge(r)
        for r in pool.imap(run_coarse_chain, [(opts.seed + i, "general") for i in range(opts.coarse)], chunksize=4):
            K.merge(r)
        for key in sorted(K.stats):
            out("  %-80s %d" % (key, K.stats[key]))
        out("  ALG-coarse: %d assertions, %d failed  %s" % (K.count["ALG-coarse"], K.nfail["ALG-coarse"], "PASS" if not K.nfail["ALG-coarse"] else "FAIL"))
        if "ALG-coarse" in K.first:
            key, rec = K.first["ALG-coarse"]
            out("  FAILURE ALG-coarse: n=%d, u=%d, v=%d, edges %s" % (rec["n"], rec["u"], rec["v"], fmt_edges(rec["edges"])))
            out("      %s" % rec["info"])
    out("")
    out("(the running time of the algorithm is measured in time_algorithm.py)")
    out("Total time %.0f s." % (time.time() - started))
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), opts.out), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


ALG_NAMES = ["ALG-applies", "ALG-c3-refused", "ALG-c-d", "ALG-value", "ALG-cutpath", "ALG-star", "ALG-coarse", "ALG-F", "ALG-tail", "ALG-pieces",
             "ALG-scc", "ALG-squares", "ALG-lambda"]


def report_alg(T, out):
    for name in ALG_NAMES:
        if T.count.get(name, 0):
            out("  %-14s %9d assertions, %d failed  %s" % (name, T.count[name], T.nfail[name], "PASS" if not T.nfail[name] else "FAIL"))
    for name in ALG_NAMES:
        if name in T.first:
            key, rec = T.first[name]
            out("  FAILURE %s: n=%d, u=%d, v=%d, edges %s" % (name, rec["n"], rec["u"], rec["v"], fmt_edges(rec["edges"])))
            out("      %s" % rec["info"])


if __name__ == "__main__":
    main()
