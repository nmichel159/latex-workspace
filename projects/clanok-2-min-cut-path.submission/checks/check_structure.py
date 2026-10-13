"""Brute-force tests of the statements S0-S10 and S15 of the blueprint (SPEC.md, Section 5).

For every connected graph with 2..7 vertices (networkx atlas, 995 graphs) and every ordered pair (u, v):
  all pairs:        S0 (c = 1 or d = 1), S15 (d = 2, c >= 3), the class DC, the three computations of cp
  pairs with c = 2: S1-S10, each statement as its own counted assertion (names S1a, S1b, S2a, ...)
The statements for c = 2 are also tested on random long chains of squares (--chains N, see chains.py), where
the number of simple u-v paths is capped.

A failing assertion is recorded with the smallest graph (vertices, then edges) on which it failed.

Run:  python check_structure.py [--chains N] [--seed S] [--jobs J] [--maxn 7]
Output: results-structure.txt
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
import algorithm  # noqa: E402  (only its strongly-connected-components routine is used here)


# ---------------------------------------------------------------------------------------------------------
# bookkeeping
# ---------------------------------------------------------------------------------------------------------

class Tally:
    def __init__(self):
        self.count = defaultdict(int)
        self.nfail = defaultdict(int)
        self.first = {}
        self.stats = defaultdict(int)
        self.ctx = None

    def ok(self, name, cond, info=None):
        self.count[name] += 1
        if not cond:
            self.nfail[name] += 1
            g, u, v = self.ctx
            key = (g.n, g.m)
            if name not in self.first or key < self.first[name][0]:
                text = info() if callable(info) else (info or "")
                self.first[name] = (key, dict(n=g.n, edges=list(g.edges), u=u, v=v, info=text))
        return cond

    def stat(self, name, k=1):
        self.stats[name] += k

    def merge(self, other):
        for k, x in other.count.items():
            self.count[k] += x
        for k, x in other.nfail.items():
            self.nfail[k] += x
        for k, x in other.stats.items():
            self.stats[k] += x
        for k, rec in other.first.items():
            if k not in self.first or rec[0] < self.first[k][0]:
                self.first[k] = rec

    def clean(self):
        self.ctx = None
        return self


# ---------------------------------------------------------------------------------------------------------
# statements for all pairs: S0, S15, cp, DC
# ---------------------------------------------------------------------------------------------------------

def check_easy(g, u, v, T, dc, mut=None):
    """S0, S15 and the consistency of the computations of cp for one ordered pair (any c)."""
    T.ctx = (g, u, v)
    d = bfs(g, u)[v]
    c = edge_conn(g, u, v)
    cp, S = cp_brute(g, u, v)
    T.stat("ordered pairs")
    # -- the three computations of cp ---------------------------------------------------------------
    T.ok("CP-optimal", is_cutpath(g, u, v, S) and popcount(S) == cp,
         lambda: "the returned set %s is not a cut-path of size cp = %d" % (bits(S), cp))
    if g.n <= 8:
        T.ok("CP-subsets", cp == cp_subsets(g, u, v), lambda: "cp_brute = %d, cp_subsets = %d" % (cp, cp_subsets(g, u, v)))
    if g.n <= 6:
        T.ok("CP-definition", cp == cp_definition(g, u, v),
             lambda: "cp_brute = %d, literal definition = %d" % (cp, cp_definition(g, u, v)))
    T.ok("CP-bounds", max(c, d) <= cp <= c + d - 1, lambda: "c=%d d=%d cp=%d" % (c, d, cp))
    # -- S0 -----------------------------------------------------------------------------------------
    if c == 1 or d == 1:
        T.stat("S0 pairs with c = 1 or d = 1")
        T.ok("S0a", cp == c + d - 1, lambda: "c=%d d=%d cp=%d" % (c, d, cp))
    if dc:
        # in DC a pair with d >= 3 has c <= 2
        if d >= 3:
            T.ok("S0b", c <= 2, lambda: "d=%d c=%d" % (d, c))
    if c == 2:
        # bridges: K = 2-edge-connected component of u; d, c between its vertices and cp(u,v) are the same in K and G
        br = bits(mask_of(bridges(g)))
        if br:
            T.stat("S0c pairs with c = 2 in graphs with a bridge")
            Kmask = component_mask(g, u, mask_of(br))
            K = [x for x in range(g.n) if (Kmask >> x) & 1]
            H, idx, emap = induced(g, K)
            T.ok("S0c-v", (Kmask >> v) & 1 == 1, "v is not in the 2-edge-connected component of u")
            if (Kmask >> v) & 1:
                hu, hv = idx[u], idx[v]
                same_d = all(bfs(H, idx[x])[idx[y]] == bfs(g, x)[y] for x in K for y in K)
                same_c = all(edge_conn(H, idx[x], idx[y]) == edge_conn(g, x, y) for x in K for y in K if x < y)
                T.ok("S0c-d", same_d, "distances in K and G differ")
                T.ok("S0c-c", same_c, "cut-values in K and G differ")
                T.ok("S0c-cp", cp_brute(H, hu, hv)[0] == cp, lambda: "cp in K = %d, in G = %d" % (cp_brute(H, hu, hv)[0], cp))
    # -- S15 ----------------------------------------------------------------------------------------
    if d == 2 and c >= 3:
        T.stat("S15 pairs (d = 2, c >= 3)")
        T.ok("S15a", cp in (c, c + 1), lambda: "c=%d cp=%d" % (c, cp))
        cc, cuts = min_cuts_by_sets(g, u, v)
        full = g.full()
        lengths = []
        for C in cuts:
            for vs, es in simple_paths(g, u, v, removed=full ^ C):
                lengths.append(len(es))
        T.ok("S15b", (cp == c) == bool(lengths), lambda: "cp=%d c=%d paths in minimum cuts: %s" % (cp, c, sorted(set(lengths))))
        T.ok("S15c", all(x % 2 == 1 and x >= 3 for x in lengths), lambda: "lengths %s" % sorted(set(lengths)))
        if lengths:
            T.stat("S15 pairs with cp = c")
        else:
            T.stat("S15 pairs with cp = c + 1")
    return d, c, cp


# ---------------------------------------------------------------------------------------------------------
# statements for pairs with c = 2: S1-S10
# ---------------------------------------------------------------------------------------------------------

def terminals_of(dec, order, i, pset):
    """(x, y, alpha, beta) of square number i (0-based) for the path with edge set pset; None if the path does
    not use exactly one entering and one leaving edge."""
    p = order[i]
    k = len(order)
    u, v = dec.u, dec.v
    if i == 0:
        x = alpha = u
    else:
        used = [e for e in dec.ent[p] if e in pset]
        if len(used) != 1 or len(dec.ent[p]) != 2:
            return None
        x = dec.head[used[0]]
        alpha = dec.head[[e for e in dec.ent[p] if e != used[0]][0]]
    if i == k - 1:
        y = beta = v
    else:
        used = [e for e in dec.lea[p] if e in pset]
        if len(used) != 1 or len(dec.lea[p]) != 2:
            return None
        y = dec.tail[used[0]]
        beta = dec.tail[[e for e in dec.lea[p] if e != used[0]][0]]
    return x, y, alpha, beta


def s7_sides(g, u, v, dec, order, pset, pmask, swap=False):
    """(left, right, wellformed) of S7 for the path with edge set pset / mask pmask: left = u, v disconnected in
    G - R; right = alpha_i, beta_i disconnected in S_i - R for some i (with swap: x_i, y_i instead)."""
    left = not connected(g, u, v, removed=pmask)
    right = False
    for i in range(len(order)):
        t = terminals_of(dec, order, i, pset)
        if t is None:
            return left, right, False
        x, y, alpha, beta = t
        a, b = (x, y) if swap else (alpha, beta)
        if dec.sep_in_piece(a, b, pmask):
            right = True
    return left, right, True


def check_s14(T, g, u, v, dec, cuts, paths, pm, pathsets, d, cpb, rng, nsub=6, piece_limit=20000):
    """S14: the criteria S7 and S9 for coarser decompositions, obtained from a subset of the minimum cuts
    (F' = the edges of the chosen cuts, the orientation of S2, the pieces = components of G - F')."""
    q = len(cuts)
    if q < 2:
        return
    subs = set()
    if q <= 5:
        subs = {s for r in range(1, q) for s in itertools.combinations(range(q), r)}
    else:
        for _ in range(nsub):
            r = rng.randint(1, min(q - 1, 6))
            subs.add(tuple(sorted(rng.sample(range(q), r))))
    for sub in sorted(subs):
        Fsub = sorted({e for i in sub for e in cuts[i][:2]})
        dec2 = Decomp(g, u, v, Fsub, {e: dec.tail[e] for e in Fsub})
        order2 = dec2.square_order()
        T.ok("S14pre", order2 is not None and not dec2.inside_F and all(len(dec2.ent[p]) <= 2 and len(dec2.lea[p]) <= 2 for p in range(dec2.np)),
             lambda: "coarse decomposition from the cuts %s is not a chain of squares" % (sub,))
        if order2 is None:
            continue
        T.stat("S14 coarse decompositions (subsets of the minimum cuts)")
        for (vs, es), pset, pmask in zip(paths, pathsets, pm):
            left, right, wellformed = s7_sides(g, u, v, dec2, order2, pset, pmask)
            if wellformed:
                T.ok("S14-S7", left == right, lambda: "coarse decomposition %s, path %s: u,v disconnected is %s, criterion says %s" % (sub, vs, left, right))
        try:
            lam_minus = dec2.vec_dist(u)
            lam_plus = dec2.vec_dist(v, reverse=True)
            cond = False
            k2 = len(order2)
            for i, p in enumerate(order2):
                ins = dec2.ent[p] if i > 0 else [None]
                outs = dec2.lea[p] if i < k2 - 1 else [None]
                for gg, hh in itertools.product(ins, outs):
                    x = u if gg is None else dec2.head[gg]
                    y = v if hh is None else dec2.tail[hh]
                    alpha = u if gg is None else dec2.head[[e for e in dec2.ent[p] if e != gg][0]]
                    beta = v if hh is None else dec2.tail[[e for e in dec2.lea[p] if e != hh][0]]
                    pre = (lam_minus[dec2.tail[gg]] + 1) if gg is not None else 0
                    post = (1 + lam_plus[dec2.head[hh]]) if hh is not None else 0
                    for pvs, pes in dec2.piece_paths(x, y, limit=piece_limit):
                        if pre + len(pes) + post == d and dec2.sep_in_piece(alpha, beta, mask_of(pes)):
                            cond = True
            T.ok("S14-S9", (cpb == d) == cond, lambda: "coarse decomposition %s: cp = %d, d = %d, condition %s" % (sub, cpb, d, cond))
        except TooMany:
            T.stat("S14 coarse decompositions skipped (too many paths inside a piece)")

def check_c2(g, u, v, T, dc=True, mut=None, path_limit=40000, rng=None, cpval=None, fast_cuts=False):
    """All of S1-S10 for one ordered pair with c(u,v) = 2.  Returns a small dict of facts (k, cp, d).
    fast_cuts: find the minimum cuts only among the pairs (e on p1, f on p2) of two edge-disjoint paths
    (every minimum cut has one edge on each; used for the large chain instances)."""
    T.ctx = (g, u, v)
    rng = rng or random.Random(g.n * 1000003 + g.m * 101 + u * 7 + v)
    d = bfs(g, u)[v]
    try:
        paths = simple_paths(g, u, v, limit=path_limit)
    except TooMany:
        T.stat("pairs skipped: more than %d simple paths" % path_limit)
        return None
    T.stat("pairs with c = 2")
    T.stat("simple u-v paths", len(paths))
    dec, cuts, problems = brute_decomp(g, u, v, fast=fast_cuts)
    F, Fmask = dec.F, dec.Fmask
    cutmasks = [(1 << e) | (1 << f) for e, f, A in cuts]
    pm = [mask_of(es) for vs, es in paths]
    pathsets = [set(es) for vs, es in paths]

    # ---- S1 -----------------------------------------------------------------------------------------
    pairs = []
    if len(paths) <= 250:
        pairs = [(i, j) for i in range(len(paths)) for j in range(i + 1, len(paths)) if pm[i] & pm[j] == 0]
    else:
        for _ in range(4000):
            i, j = rng.randrange(len(paths)), rng.randrange(len(paths))
            if i != j and pm[i] & pm[j] == 0:
                pairs.append((i, j))
    if len(pairs) > 300:
        pairs = rng.sample(pairs, 300)
    flow = two_disjoint_paths(g, u, v)
    extra = []
    if flow is not None:
        fm = [mask_of(g.edge_id(a, b) for a, b in zip(p, p[1:])) for p in flow]
        extra = [(tuple(flow[0]), tuple(g.edge_id(a, b) for a, b in zip(flow[0], flow[0][1:])),
                  tuple(flow[1]), tuple(g.edge_id(a, b) for a, b in zip(flow[1], flow[1][1:])))]
    T.stat("S1 pairs of edge-disjoint paths", len(pairs) + len(extra))
    quads = [(paths[i][0], paths[i][1], paths[j][0], paths[j][1]) for i, j in pairs] + extra
    T.ok("S1-exist", bool(quads), "no two edge-disjoint paths found although c = 2")
    for vs1, es1, vs2, es2 in quads:
        m1, m2 = mask_of(es1), mask_of(es2)
        T.ok("S1a", Fmask & ~(m1 | m2) == 0, lambda: "F = %s, paths %s | %s" % (F, es1, es2))
        T.ok("S1b", all(popcount(C & m1) == 1 and popcount(C & m2) == 1 for C in cutmasks),
             lambda: "a minimum cut does not have exactly one edge on each path")
        ok = True
        for vs, es in ((vs1, es1), (vs2, es2)):
            for j, e in enumerate(es):
                if (Fmask >> e) & 1 and dec.tail[e] != vs[j]:
                    ok = False
        T.ok("S2b", ok, lambda: "orientation by the paths differs from the orientation by the cuts")

    # ---- S2 -----------------------------------------------------------------------------------------
    T.ok("S2a", not problems, lambda: "problems: %s" % problems)
    for (vs, es), pmask in zip(paths, pm):
        T.ok("S2c", all(popcount(C & pmask) == 1 for C in cutmasks), lambda: "path %s meets a minimum cut not exactly once" % (vs,))
        okd = True
        for j, e in enumerate(es):
            if (Fmask >> e) & 1 and (dec.tail[e] == vs[j]) == (mut == "S2-flip"):
                okd = False
        T.ok("S2d", okd, lambda: "path %s traverses an F-edge from head to tail" % (vs,))

    # ---- S3 -----------------------------------------------------------------------------------------
    T.ok("S3a", not dec.inside_F, lambda: "F-edges inside a piece: %s" % dec.inside_F)
    for vs, es in paths:
        seq = [dec.comp[x] for x in vs]
        runs = [seq[0]] + [b for a, b in zip(seq, seq[1:]) if a != b]
        T.ok("S3b", len(runs) == len(set(runs)), lambda: "path %s visits a piece twice" % (vs,))

    # ---- S4 -----------------------------------------------------------------------------------------
    ent, lea = dec.ent, dec.lea
    s4a = all(len(ent[p]) <= 2 and len(lea[p]) <= 2 for p in range(dec.np))
    s4b = (dec.pu != dec.pv and len(ent[dec.pu]) == 0 and len(lea[dec.pu]) == 2
           and len(ent[dec.pv]) == 2 and len(lea[dec.pv]) == 0)
    s4c = all(len(ent[p]) == len(lea[p]) and len(ent[p]) in (1, 2)
              for p in range(dec.np) if p != dec.pu and p != dec.pv)
    T.ok("S4a", s4a, lambda: "entering %s leaving %s" % ([len(x) for x in ent], [len(x) for x in lea]))
    T.ok("S4b", s4b, lambda: "piece of u: %d in %d out; piece of v: %d in %d out; same piece: %s"
         % (len(ent[dec.pu]), len(lea[dec.pu]), len(ent[dec.pv]), len(lea[dec.pv]), dec.pu == dec.pv))
    T.ok("S4c", s4c, lambda: "entering %s leaving %s" % ([len(x) for x in ent], [len(x) for x in lea]))
    s4_ok = s4a and s4b and s4c
    # (the dependent tests below need a well-formed decomposition)
    order = dec.square_order()
    T.ok("S5o", order is not None and len(order) >= 2,
         lambda: "the squares %s are not totally ordered by reachability" % [p for p in range(dec.np) if dec.is_square[p]])
    if order is None or dec.inside_F or not s4_ok:
        T.stat("pairs where the dependent tests were skipped")
        return None
    k = len(order)
    T.stat("pairs by number of squares k = %d" % k)

    # ---- S5 -----------------------------------------------------------------------------------------
    for i in range(1, k):
        if mut == "S5-cut":
            E2 = [ent[order[i]][0], lea[order[i]][0]] if lea[order[i]] else ent[order[i]]
        else:
            E2 = ent[order[i]]
        T.ok("S5a", len(E2) == 2 and not connected(g, u, v, removed=mask_of(E2)),
             lambda: "entering edges of square %d: %s do not form a cut" % (i + 1, E2))
    for i in range(0, k - 1):
        E2 = lea[order[i]]
        T.ok("S5b", len(E2) == 2 and not connected(g, u, v, removed=mask_of(E2)),
             lambda: "leaving edges of square %d: %s do not form a cut" % (i + 1, E2))
    expected_order = list(order)
    if mut == "S5-order":
        expected_order = expected_order[::-1]
    for vs, es in paths:
        seq = []
        for x in vs:
            p = dec.comp[x]
            if dec.is_square[p] and p not in seq:
                seq.append(p)
        T.ok("S5c", seq == expected_order, lambda: "path %s visits the squares in the order %s, not %s" % (vs, seq, expected_order))
    seqs_per_i = []
    covered_links = []
    covered_edges = []
    for i in range(0, k - 1):
        leas = lea[order[i]]
        fs = [dec.follow(e) for e in leas] if len(leas) == 2 else [None, None]
        good = (None not in fs and fs[0][2] == order[i + 1] and fs[1][2] == order[i + 1]
                and fs[0][0][-1] != fs[1][0][-1] and set(fs[0][1]).isdisjoint(fs[1][1]))
        T.ok("S5d", good, lambda: "between square %d and %d the two sequences are %s" % (i + 1, i + 2, fs))
        seqs_per_i.append(fs if good else None)
        if good:
            for f in fs:
                covered_links.extend(f[1])
                covered_edges.extend(f[0])
    nonsquare = [p for p in range(dec.np) if not dec.is_square[p]]
    T.ok("S5d-cover", sorted(covered_links) == sorted(nonsquare) and sorted(covered_edges) == sorted(F),
         lambda: "links covered %s of %s; F-edges covered %s of %s" % (sorted(covered_links), nonsquare, sorted(covered_edges), F))
    for (vs, es), pset in zip(paths, pathsets):
        vcomp = {dec.comp[x] for x in vs}
        for i in range(0, k - 1):
            fs = seqs_per_i[i]
            if fs is None:
                continue
            states = []
            for f in fs:
                used = [e in pset for e in f[0]]
                visited = [L in vcomp for L in f[1]]
                states.append((all(used), not any(used), all(visited), not any(visited)))
            (a_all, a_none, a_vall, a_vnone), (b_all, b_none, b_vall, b_vnone) = states
            if mut == "S5-both":
                good = a_all and b_all
            else:
                good = (a_all and b_none and a_vall and b_vnone) or (b_all and a_none and b_vall and a_vnone)
            T.ok("S5e", good, lambda: "path %s and the sequences %s between squares %d and %d" % (vs, fs, i + 1, i + 2))

    # ---- S6 -----------------------------------------------------------------------------------------
    for i, p in enumerate(order):
        terms = sorted(dec.terminals(p))
        if mut == "S6-all":
            terms = sorted(dec.pieces[p])
        thr = 4 if mut == "S6-4" else 3
        for s, t in itertools.combinations(terms, 2):
            val = edge_conn(g, s, t, limit=thr)
            T.ok("S6", val >= thr, lambda: "terminals %d, %d of square %d have c = %d" % (s, t, i + 1, val))

    # ---- S7 -----------------------------------------------------------------------------------------
    for (vs, es), pset, pmask in zip(paths, pathsets, pm):
        left, right, wellformed = s7_sides(g, u, v, dec, order, pset, pmask, swap=(mut == "S7-swap"))
        T.ok("S7pre", wellformed, lambda: "path %s does not use exactly one entering/leaving edge of a square" % (vs,))
        if wellformed:
            T.ok("S7", left == right, lambda: "path %s: u,v disconnected in G-R is %s, criterion says %s" % (vs, left, right))
            T.stat("S7 paths that separate" if left else "S7 paths that do not separate")

    # ---- S8 -----------------------------------------------------------------------------------------
    try:
        vp = set(dec.vec_paths(limit=path_limit + 1))
    except TooMany:
        vp = None
    if vp is not None:
        T.ok("S8a", vp == {vs for vs, es in paths}, lambda: "directed paths of G-vector: %d, paths of G: %d" % (len(vp), len(paths)))
    lam_minus = dec.vec_dist(u)
    lam_plus = dec.vec_dist(v, reverse=True)
    table = {}
    best_path = {}
    for vs, es in paths:
        for i, p in enumerate(order):
            pos = [j for j, x in enumerate(vs) if dec.comp[x] == p]
            if not pos:
                continue
            s, t = pos[0], pos[-1]
            if t - s + 1 != len(pos):
                continue
            gg = es[s - 1] if s > 0 else None
            hh = es[t] if t < len(vs) - 1 else None
            key = (i, gg, hh, vs[s:t + 1])
            if key not in table or len(es) < table[key]:
                table[key] = len(es)
                best_path[key] = (vs, es)
    cands = []        # (i, g, h, p vertices, p edges, count, alpha, beta)
    for i, p in enumerate(order):
        ins = ent[p] if i > 0 else [None]
        outs = lea[p] if i < k - 1 else [None]
        for gg, hh in itertools.product(ins, outs):
            x = u if gg is None else dec.head[gg]
            y = v if hh is None else dec.tail[hh]
            alpha = u if gg is None else dec.head[[e for e in ent[p] if e != gg][0]]
            beta = v if hh is None else dec.tail[[e for e in lea[p] if e != hh][0]]
            lm = lam_minus[dec.tail[gg]] if gg is not None else 0
            lp = lam_plus[dec.head[hh]] if hh is not None else 0
            T.ok("S8pre", lm is not None and lp is not None,
                 lambda: "lambda undefined: tail of g unreachable from u or head of h cannot reach v in G-vector")
            if lm is None or lp is None:
                continue
            pre = (lm + 1) if gg is not None else 0
            post = (1 + lp) if hh is not None else 0
            for pvs, pes in dec.piece_paths(x, y):
                cands.append((i, gg, hh, pvs, pes, pre + len(pes) + post, alpha, beta))
    T.stat("S8 triples (g, p, h)", len(cands))
    candkeys = set()
    for i, gg, hh, pvs, pes, count, alpha, beta in cands:
        key = (i, gg, hh, pvs)
        candkeys.add(key)
        T.ok("S8b", table.get(key) == (count + 1 if mut == "S8-off" else count),
             lambda: "square %d, g=%s, h=%s, p=%s: formula %d, shortest path through it %s" % (i + 1, gg, hh, pvs, count, table.get(key)))
        if key in best_path:
            vs, es = best_path[key]
            inpiece = {x for x in vs if dec.comp[x] == order[i]}
            ein = {e for e in es if dec.comp[g.edges[e][0]] == order[i] and dec.comp[g.edges[e][1]] == order[i]}
            T.ok("S8c", inpiece == set(pvs) and ein == set(pes),
                 lambda: "shortest path %s meets square %d in %s / %s, not in p = %s" % (vs, i + 1, inpiece, ein, pvs))
    T.ok("S8d", set(table) <= candkeys, lambda: "a u-v path leaves a square along a (g, p, h) that is not enumerated")

    # ---- S9, S10 ------------------------------------------------------------------------------------
    cpb = cpval if cpval is not None else cp_brute(g, u, v)[0]
    cond = False
    witnesses = []
    for i, gg, hh, pvs, pes, count, alpha, beta in cands:
        len_ok = (count == d) or mut == "S9-nolen"
        if not len_ok:
            continue
        sep = dec.sep_in_piece(alpha, beta, mask_of(pes)) or mut == "S9-nosep"
        if sep:
            cond = True
            witnesses.append((i, gg, hh, pvs, pes, count, alpha, beta))
    T.ok("S9a", (cpb == d) == cond, lambda: "cp = %d, d = %d, condition of S9 = %s" % (cpb, d, cond))
    T.ok("S9b", cpb in (d, d + 1), lambda: "cp = %d, d = %d" % (cpb, d))
    T.stat("pairs with cp = d" if cpb == d else "pairs with cp = d + 1")
    if dc and cond and mut is None:
        # S10: in the class DC, such a path is a shortest x-y path of length at most 2
        for i, gg, hh, pvs, pes, count, alpha, beta in witnesses:
            x, y = pvs[0], pvs[-1]
            T.ok("S10", len(pes) == bfs(g, x)[y] and len(pes) <= 2, lambda: "witness p = %s has length %d, d(x,y) = %d" % (pvs, len(pes), bfs(g, x)[y]))
            # observation 8 of the notes of the math core: in the class a separating trace has at most three distinct
            # terminals, and alpha, beta are at distance at most two
            T.ok("OBS8-terminals", len({x, y, alpha, beta}) <= 3, lambda: "witness p = %s has four distinct terminals x=%d y=%d alpha=%d beta=%d" % (pvs, x, y, alpha, beta))
            T.ok("OBS8-distance", bfs(g, alpha)[beta] <= 2, lambda: "d(alpha, beta) > 2 for the witness p = %s" % (pvs,))
            pattern = ",".join(n for n, c_ in (("x=alpha", x == alpha), ("y=beta", y == beta), ("y=alpha", y == alpha), ("x=beta", x == beta)) if c_)
            T.stat("DC witnesses by equalities among x, y, alpha, beta: " + (pattern or "none"))
    elif cond and mut is None:
        # outside DC S10 is not claimed; count how often a witness is longer than two
        T.stat("outside DC: pairs with cp = d")
        if all(len(pes) >= 3 for i, gg, hh, pvs, pes, count, alpha, beta in witnesses):
            T.stat("outside DC: pairs with cp = d where every witness p has |p| >= 3")
        for i, gg, hh, pvs, pes, count, alpha, beta in witnesses:
            x, y = pvs[0], pvs[-1]
            if len({x, y, alpha, beta}) == 4:
                T.stat("outside DC: witnesses with four distinct terminals")
            T.ok("S9-witness-shortest", len(pes) == bfs(g, x)[y], lambda: "witness p = %s is not a shortest x-y path" % (pvs,))
    if mut is None:
        check_s14(T, g, u, v, dec, cuts, paths, pm, pathsets, d, cpb, rng)
    if mut is None or mut in ("S9core-nolen", "S11-res-flip", "S11-res-both"):
        check_core_tex(T, g, u, v, dec, order, paths, quads, d, cpb, dc, mut)
    return dict(k=k, d=d, cp=cpb, npaths=len(paths))


def check_core_tex(T, g, u, v, dec, order, paths, quads, d, cpb, dc, mut=None):
    """The statements of drafts/core.tex in the form in which they are written there:
    Theorem 'Separating shortest paths' (G-distances d(u,x) + |p| + d(y,v) = d(u,v) and terminal pairs),
    Corollary 'two edges' (in DC), and Lemma 'residual graph' (D from two edge-disjoint paths)."""
    Du, Dv = bfs(g, u), bfs(g, v)
    cond = False
    cand = []
    for i, p in enumerate(order):
        et, lt = dec.entering_terminals(p), dec.leaving_terminals(p)
        for x, alpha in {(et[0], et[1]), (et[1], et[0])}:
            for y, beta in {(lt[0], lt[1]), (lt[1], lt[0])}:
                for pvs, pes in dec.piece_paths(x, y):
                    if Du[x] + len(pes) + Dv[y] == d or mut == "S9core-nolen":           # condition (i)
                        cand.append((i, x, y, pvs, pes))
                        if dec.sep_in_piece(alpha, beta, mask_of(pes)):                  # condition (ii)
                            cond = True
    T.ok("S9-core", (cpb == d) == cond, lambda: "theorem of core.tex: cp = %d, d = %d, condition %s" % (cpb, d, cond))
    if dc:
        T.ok("S10-core-p", all(len(pes) == bfs(g, x)[y] and len(pes) <= 2 for i, x, y, pvs, pes in cand),
             lambda: "a path p with (i) is not a shortest x-y path of length at most 2")
        ok = True
        for (vs, es) in paths:
            if len(es) == d:
                per = {}
                for e in es:
                    a, b = g.edges[e]
                    if dec.comp[a] == dec.comp[b]:
                        per[dec.comp[a]] = per.get(dec.comp[a], 0) + 1
                if any(c > 2 for c in per.values()):
                    ok = False
        T.ok("S10-core-shortest", ok, lambda: "a shortest u-v path has more than two edges in a square")
    elif cand:
        T.stat("outside DC: paths p with (i) of length >= 3 exist in %s" % ("some pair" if any(len(c[4]) >= 3 for c in cand) else "no pair"))
    # Lemma "residual graph": D built from two edge-disjoint paths p1, p2
    n = g.n
    for vs1, es1, vs2, es2 in quads[:6]:
        trav = {}
        for vs, es in ((vs1, es1), (vs2, es2)):
            for j, e in enumerate(es):
                trav[e] = (vs[j], vs[j + 1])
        out = [[] for _ in range(n)]
        for e, (a, b) in enumerate(g.edges):
            if e in trav:
                x, y = trav[e]
                if mut == "S11-res-flip":
                    x, y = y, x               # mutation: the arc of a path edge points along the path
                out[y].append(x)
                if mut == "S11-res-both":
                    out[x].append(y)          # mutation: a path edge keeps both arcs (as if it carried no flow)
            else:
                out[a].append(b)
                out[b].append(a)
        scc = algorithm._scc(n, out)
        T.ok("S11-res-ii", all((e in set(dec.F)) == (scc[x] != scc[y]) for e, (x, y) in trav.items()),
             lambda: "an edge of p1 u p2 is in F iff its ends lie in different strong components of D: violated")
        if n <= 10:
            ok = True
            for A in range(1 << n):
                if (A >> u) & 1 and not (A >> v) & 1:
                    boundary = sum(1 for (a, b) in g.edges if ((A >> a) ^ (A >> b)) & 1)
                    no_arc = not any((A >> x) & 1 and not (A >> y) & 1 for x in range(n) for y in out[x])
                    if (boundary == 2) != no_arc:
                        ok = False
                        break
            T.ok("S11-res-i", ok, lambda: "delta(A) is a minimum cut iff no arc of D leaves A: violated")


# ---------------------------------------------------------------------------------------------------------
# drivers
# ---------------------------------------------------------------------------------------------------------

def run_graph(args):
    n, es, mut = args
    g = Gr(n, es)
    T = Tally()
    dc, _ = in_dc(g)
    T.ctx = (g, 0, 1)
    T.stat("graphs")
    T.stat("graphs in DC" if dc else "graphs not in DC")
    for u in range(n):
        for v in range(n):
            if u == v:
                continue
            d, c, cp = check_easy(g, u, v, T, dc, mut)
            if c == 2:
                check_c2(g, u, v, T, dc=dc, mut=mut, cpval=cp)
    return T.clean()


def run_chain(args):
    seed, mut, path_limit = args[:3]
    kind = args[3] if len(args) > 3 else "dc"
    import chains
    rng = random.Random(seed)
    inst = chains.random_dc_chain(rng) if kind == "dc" else chains.random_general_chain(rng)
    T = Tally()
    if inst is None:
        T.stat("chain instances rejected")
        return T
    g, u, v = inst
    T.ctx = (g, u, v)
    T.stat("chain instances (%s, c = 2)" % ("in DC" if kind == "dc" else "not in DC"))
    T.stat("chain instances: vertices", g.n)
    res = check_c2(g, u, v, T, dc=(kind == "dc"), mut=mut, path_limit=path_limit, rng=rng, fast_cuts=True)
    if res is not None:
        T.stat("chain instances checked")
    return T.clean()


NAMES = [
    ("CP-optimal", "cp_brute returns a cut-path of size cp"), ("CP-subsets", "cp_brute = cp_subsets (article 1's method)"),
    ("CP-definition", "cp_brute = literal definition (n <= 6)"), ("CP-bounds", "max(c,d) <= cp <= c+d-1"),
    ("S0a", "S0: c = 1 or d = 1  =>  cp = c + d - 1"), ("S0b", "S0: in DC a pair with d >= 3 has c <= 2"),
    ("S0c-v", "S0: v in the 2-edge-connected component K of u"), ("S0c-d", "S0: distances in K and G"),
    ("S0c-c", "S0: cut-values in K and G"), ("S0c-cp", "S0: cp(u,v) in K and G"),
    ("S1-exist", "S1: two edge-disjoint paths exist"), ("S1a", "S1: F within E(p1) u E(p2)"),
    ("S1b", "S1: every minimum cut has one edge on each path"),
    ("S2a", "S2: orientation well defined (same tail for every cut)"), ("S2b", "S2: orientation agrees with p1, p2"),
    ("S2c", "S2: every path meets every minimum cut exactly once"), ("S2d", "S2: every path traverses F tail->head"),
    ("S3a", "S3: F-edges join different pieces"), ("S3b", "S3: every path visits a piece in one block"),
    ("S4a", "S4: at most 2 entering, 2 leaving"), ("S4b", "S4: pieces of u and v"), ("S4c", "S4: other pieces"),
    ("S5o", "S5: squares totally ordered, k >= 2"),
    ("S5a", "S5: entering edges of S_i (i >= 2) form a minimum cut"), ("S5b", "S5: leaving edges of S_i (i < k) form a minimum cut"),
    ("S5c", "S5: every path visits the squares in the common order"),
    ("S5d", "S5: two sequences between consecutive squares"), ("S5d-cover", "S5: sequences cover all links and F-edges once"),
    ("S5e", "S5: a path uses exactly one sequence completely"),
    ("S6", "S6: distinct terminals of a square have c >= 3"),
    ("S7pre", "S7: a path uses exactly one entering and one leaving edge"), ("S7", "S7: separation criterion"),
    ("S8a", "S8: u-v paths of G = directed u-v paths of G-vector"), ("S8b", "S8: shortest path through (g, p, h) has the formula length"),
    ("S8c", "S8: it meets the square exactly in p"), ("S8d", "S8: every path leaves a square along an enumerated (g, p, h)"),
    ("S9a", "S9: cp = d  iff  the condition holds"), ("S9b", "S9: cp in {d, d+1}"), ("S10", "S10: witness p has |p| = d(x,y) <= 2 in DC"),
    ("S9-witness-shortest", "outside DC: witness p is a shortest x-y path"),
    ("OBS8-terminals", "notes, doubt 8: in DC a separating trace has at most three distinct terminals"),
    ("OBS8-distance", "notes, doubt 8: in DC alpha and beta of a separating trace are at distance <= 2"),
    ("S9-core", "core.tex theorem: cp = d iff (i) d(u,x)+|p|+d(y,v) = d, (ii) p separates alpha, beta"),
    ("S10-core-p", "core.tex corollary: a path p with (i) has |p| = d(x,y) <= 2 (DC)"),
    ("S10-core-shortest", "core.tex corollary: a shortest u-v path has <= 2 edges in every square (DC)"),
    ("S11-res-i", "core.tex residual lemma (i): delta(A) minimum cut iff no arc of D leaves A"),
    ("S11-res-ii", "core.tex residual lemma (ii): edge of p1 u p2 in F iff ends in different strong components of D"),
    ("S14pre", "S14: a subset of the minimum cuts gives a chain of squares"), ("S14-S7", "S14: criterion S7 on the coarser decomposition"),
    ("S14-S9", "S14: criterion S9 on the coarser decomposition"),
    ("S15a", "S15: cp in {c, c+1}"), ("S15b", "S15: cp = c iff a minimum cut contains a path"),
    ("S15c", "S15: such paths have odd length >= 3"),
]


def report(T, out, label):
    out("%-14s %-62s %10s %8s" % ("assertion", "statement", "count", "failed"))
    for name, text in NAMES:
        if T.count.get(name, 0) or T.nfail.get(name, 0):
            out("%-14s %-62s %10d %8d  %s" % (name, text, T.count[name], T.nfail[name], "PASS" if not T.nfail[name] else "FAIL"))
    fails = [(name, T.first[name]) for name, _ in NAMES if name in T.first]
    if fails:
        out("")
        out("FAILURES (smallest graph per assertion)")
        for name, (key, rec) in fails:
            out("  %s: n=%d, edges=%s, u=%d, v=%d" % (name, rec["n"], fmt_edges(rec["edges"]), rec["u"], rec["v"]))
            out("      %s" % rec["info"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chains", type=int, default=0)
    ap.add_argument("--general", type=int, default=0, help="seeds for random instances outside DC")
    ap.add_argument("--seed", type=int, default=20261012)
    ap.add_argument("--jobs", type=int, default=24)
    ap.add_argument("--maxn", type=int, default=7)
    ap.add_argument("--mutate", default=None)
    ap.add_argument("--path-limit", type=int, default=20000)
    ap.add_argument("--out", default="results-structure.txt")
    opts = ap.parse_args()
    lines = []

    def out(s=""):
        print(s, flush=True)
        lines.append(s)

    started = time.time()
    graphs = []
    for n in range(2, opts.maxn + 1):
        graphs.extend(connected_graphs(n, SCRATCH))
    out("check_structure.py: S0-S10 and S15, all connected graphs with 2..%d vertices (%d graphs), all ordered pairs" % (opts.maxn, len(graphs)))
    out("graphs by number of vertices: %s" % ", ".join("%d: %d" % (n, sum(1 for x in graphs if x[0] == n)) for n in range(2, opts.maxn + 1)))
    if opts.mutate:
        out("MUTATION: %s" % opts.mutate)
    T = Tally()
    with Pool(opts.jobs) as pool:
        for r in pool.imap(run_graph, [(n, es, opts.mutate) for n, es in graphs], chunksize=4):
            T.merge(r)
        out("  done in %.0f s" % (time.time() - started))
        out("")
        out("Statistics, small graphs")
        for key in sorted(T.stats):
            out("  %-60s %d" % (key, T.stats[key]))
        out("")
        report(T, out, "small")
        if opts.chains:
            out("")
            out("Random chains of squares (chains.py): %d seeds, at most %d simple paths per instance" % (opts.chains, opts.path_limit))
            C = Tally()
            for r in pool.imap(run_chain, [(opts.seed + i, opts.mutate, opts.path_limit) for i in range(opts.chains)], chunksize=4):
                C.merge(r)
            for key in sorted(C.stats):
                out("  %-60s %d" % (key, C.stats[key]))
            out("")
            report(C, out, "chains")
            T.merge(C)
        if opts.general:
            out("")
            out("Random instances outside DC (chains.py, larger blocks; S10 not asserted): %d seeds" % opts.general)
            N = Tally()
            for r in pool.imap(run_chain, [(opts.seed + i, opts.mutate, opts.path_limit, "general") for i in range(opts.general)], chunksize=4):
                N.merge(r)
            for key in sorted(N.stats):
                out("  %-60s %d" % (key, N.stats[key]))
            out("")
            report(N, out, "general")
            T.merge(N)
    out("")
    total = sum(T.count.values())
    failed = sum(T.nfail.values())
    out("Assertions: %d, failed: %d.  Total time %.0f s." % (total, failed, time.time() - started))
    if not opts.mutate:
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), opts.out), "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
    return T


if __name__ == "__main__":
    main()
