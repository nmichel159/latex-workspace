"""Task F: the named graphs.

describe(name, edges, u, v, claims) prints every computed quantity of a pair (d, c, cp, DC, minimum cuts, F with
its orientation, pieces, squares, links, terminals, general paths, the witnesses of S9, the result of the
algorithm) in the labels of the graph and compares the quantities listed in `claims` with the computed ones.

Graphs verified here:
  the two six-vertex counterexamples of the research map (knowledge/research/min-cut-path.md, Section 3)
  every graph listed under "Graphs to verify" in drafts/core-notes.md, if that file exists (see read_core_notes)

Run:  python verify_named_graphs.py
Output: results-named-graphs.txt
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp import *  # noqa: E402,F401,F403
import algorithm  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
CORE_NOTES = os.path.normpath(os.path.join(HERE, "..", "drafts", "core-notes.md"))


class Report:
    def __init__(self):
        self.lines = []
        self.mismatches = []

    def out(self, s=""):
        print(s, flush=True)
        self.lines.append(s)


def describe(R, name, edges, u, v, claims=None, show_algorithm=True):
    """edges: list of pairs of hashable labels; u, v: labels."""
    labels = sorted({x for e in edges for x in e}, key=lambda x: (str(type(x)), x))
    idx = {x: i for i, x in enumerate(labels)}
    g = Gr(len(labels), [(idx[a], idx[b]) for a, b in edges])
    U, V = idx[u], idx[v]
    L = lambda x: str(labels[x])                       # noqa: E731
    E = lambda e: "%s%s" % (L(g.edges[e][0]), L(g.edges[e][1])) if len(L(0)) == 1 else "%s-%s" % (L(g.edges[e][0]), L(g.edges[e][1]))  # noqa: E731
    out = R.out
    out("=" * 100)
    out("%s: %d vertices {%s}, %d edges {%s}; u = %s, v = %s" % (name, g.n, ", ".join(map(L, range(g.n))), g.m,
                                                                  ", ".join(E(e) for e in range(g.m)), u, v))
    d = bfs(g, U)[V]
    c = edge_conn(g, U, V)
    cp, S = cp_brute(g, U, V)
    cps = cp_subsets(g, U, V) if g.n <= 9 else None
    dc, bad = in_dc(g)
    computed = dict(d=d, c=c, cp=cp)
    out("  d(u,v) = %d, c(u,v) = %d, cp(u,v) = %d (second computation: %s), c + d - 1 = %d" % (d, c, cp, cps, c + d - 1))
    out("  an optimal cut-path: {%s}; it is a cut-path: %s" % (", ".join(E(e) for e in bits(S)), is_cutpath(g, U, V, S)))
    out("  in DC: %s%s" % (dc, "" if dc else " (pair %s, %s violates it)" % (L(bad[0]), L(bad[1]))))
    shortest = [(vs, es) for vs, es in simple_paths(g, U, V, maxlen=d) if len(es) == d]
    sep = [vs for vs, es in shortest if not connected(g, U, V, removed=mask_of(es))]
    out("  shortest u-v paths: %d; those whose removal separates u from v: %s" % (len(shortest), ["".join(map(L, vs)) for vs in sep]))
    computed["separating shortest path"] = bool(sep)
    if c == 2:
        dec, cuts, problems = brute_decomp(g, U, V)
        out("  minimum cuts: %s" % ["{%s, %s}" % (E(e), E(f)) for e, f, A in cuts])
        out("  F = {%s}" % ", ".join(E(e) for e in dec.F))
        out("  orientation (tail -> head): %s" % ", ".join("%s->%s" % (L(dec.tail[e]), L(dec.head[e])) for e in dec.F))
        order = dec.square_order()
        pc = lambda p: "{%s}" % ",".join(L(x) for x in sorted(dec.pieces[p]))   # noqa: E731
        out("  pieces: %s" % ", ".join(pc(p) for p in range(dec.np)))
        out("  squares in order S_1..S_k (k = %d): %s" % (len(order), ", ".join("S_%d = %s" % (i + 1, pc(p)) for i, p in enumerate(order))))
        out("  links: %s" % (", ".join(pc(p) for p in range(dec.np) if not dec.is_square[p]) or "none"))
        for i, p in enumerate(order):
            ent = ", ".join(L(x) for x in dec.entering_terminals(p))
            lea = ", ".join(L(x) for x in dec.leaving_terminals(p))
            out("  terminals of S_%d: entering (a, b) = (%s), leaving (c, d) = (%s)" % (i + 1, ent, lea))
            terms = sorted(dec.terminals(p))
            cs = ["c(%s,%s) = %d" % (L(s), L(t), edge_conn(g, s, t)) for s, t in itertools.combinations(terms, 2)]
            out("      S6: %s" % (", ".join(cs) or "(one terminal)"))
        for i in range(len(order) - 1):
            fs = [dec.follow(e) for e in dec.lea[order[i]]]
            out("  general paths between S_%d and S_%d: %s" % (i + 1, i + 2, " | ".join(
                "".join([E(f[0][0])] + ["[%s]%s" % (pc(Lk), E(ek)) for Lk, ek in zip(f[1], f[0][1:])]) for f in fs)))
        # S9 witnesses
        lam_minus = dec.vec_dist(U)
        lam_plus = dec.vec_dist(V, reverse=True)
        wit = []
        for i, p in enumerate(order):
            ins = dec.ent[p] if i > 0 else [None]
            outs = dec.lea[p] if i < len(order) - 1 else [None]
            for gg in ins:
                for hh in outs:
                    x = U if gg is None else dec.head[gg]
                    y = V if hh is None else dec.tail[hh]
                    alpha = U if gg is None else dec.head[[e for e in dec.ent[p] if e != gg][0]]
                    beta = V if hh is None else dec.tail[[e for e in dec.lea[p] if e != hh][0]]
                    for pvs, pes in dec.piece_paths(x, y):
                        count = ((lam_minus[dec.tail[gg]] + 1) if gg is not None else 0) + len(pes) + ((1 + lam_plus[dec.head[hh]]) if hh is not None else 0)
                        if count == d and dec.sep_in_piece(alpha, beta, mask_of(pes)):
                            wit.append("S_%d: g=%s, p=%s, h=%s (alpha=%s, beta=%s)" % (
                                i + 1, E(gg) if gg is not None else "-", "".join(map(L, pvs)), E(hh) if hh is not None else "-", L(alpha), L(beta)))
        out("  S9 witnesses (count = d and p separates alpha, beta): %s" % (wit or "none"))
        out("  S9: cp = d iff a witness exists: %s" % ((cp == d) == bool(wit)))
        computed["F"] = sorted(tuple(sorted((L(g.edges[e][0]), L(g.edges[e][1])))) for e in dec.F)
        computed["pieces"] = sorted(tuple(sorted(L(x) for x in dec.pieces[p])) for p in range(dec.np))
        computed["squares"] = sorted(tuple(sorted(L(x) for x in dec.pieces[p])) for p in order)
        computed["k"] = len(order)
        computed["links"] = sorted(tuple(sorted(L(x) for x in dec.pieces[p])) for p in range(dec.np) if not dec.is_square[p])
        if show_algorithm:
            res = algorithm.solve(g, U, V)
            if res["witness"]:
                sq, gg, hh, pe, es = res["witness"]
                walk = [U]
                for e in es:
                    walk.append(g.other(e, walk[-1]))
                out("  algorithm: cp = %d via the path %s (g = %s, p = %s, h = %s)" % (
                    res["cp"], "".join(L(x) for x in walk), E(gg) if gg is not None else "-",
                    "".join(L(a) for a, b in pe) + L(pe[-1][1]), E(hh) if hh is not None else "-"))
                out("             cut-path returned: {%s}" % ", ".join(E(e) for e in bits(res["cutpath"])))
            else:
                out("  algorithm: cp = %d (%s); cut-path returned: {%s}" % (res["cp"], res["case"], ", ".join(E(e) for e in bits(res["cutpath"]))))
            out("  algorithm agrees with brute force: cp %s, F %s, cut-path valid %s" % (
                res["cp"] == cp, res["F"] == dec.F and res["tail"] == dec.tail, is_cutpath(g, U, V, res["cutpath"]) and popcount(res["cutpath"]) == res["cp"]))
    elif c >= 3 and d == 2:
        cc, cuts = min_cuts_by_sets(g, U, V)
        out("  open case d = 2, c = %d: the algorithm does not apply (it returns %s)" % (c, algorithm.solve(g, U, V)))
        for C in cuts:
            paths = simple_paths(g, U, V, removed=g.full() ^ C)
            if paths:
                out("  minimum cut {%s} contains the u-v paths %s" % (", ".join(E(e) for e in bits(C)), ["".join(map(L, vs)) for vs, es in paths]))
        out("  minimum cuts that contain a u-v path: %d of %d; cp = c: %s" % (
            sum(1 for C in cuts if simple_paths(g, U, V, removed=g.full() ^ C)), len(cuts), cp == c))
    # claims
    if claims:
        for key, want in claims.items():
            got = computed.get(key)
            if key in ("F", "pieces", "squares", "links") and want is not None:
                want = sorted(tuple(sorted(x)) for x in want)
            ok = got == want
            out("  claim %-24s %s: claimed %s, computed %s" % (key, "OK " if ok else "MISMATCH", want, got))
            if not ok:
                R.mismatches.append((name, key, want, got))
    return computed


def read_core_notes():
    """Lines of the section 'Graphs to verify' of drafts/core-notes.md, if the file exists."""
    if not os.path.exists(CORE_NOTES):
        return None
    with open(CORE_NOTES, encoding="utf-8") as f:
        text = f.read()
    m = re.search(r"^#+\s*(?:\d+\.\s*)?Graphs to verify.*?$", text, re.M | re.I)
    if not m:
        return None
    rest = text[m.end():]
    nxt = re.search(r"^#+\s", rest, re.M)
    return rest[:nxt.start()] if nxt else rest


class Pair:
    """A graph with one-character vertex labels, given by edge strings such as "ua", and a pair (u, v)."""

    def __init__(self, edge_strs, u, v):
        self.edge_strs = list(edge_strs)
        self.labels = sorted({x for s in edge_strs for x in s} | {u, v})
        self.idx = {x: i for i, x in enumerate(self.labels)}
        self.g = Gr(len(self.labels), [(self.idx[s[0]], self.idx[s[1]]) for s in edge_strs])
        self.u, self.v = self.idx[u], self.idx[v]

    def e(self, s):
        return self.g.edge_id(self.idx[s[0]], self.idx[s[1]])

    def emask(self, strs):
        return mask_of(self.e(s) for s in strs)

    def estr(self, e):
        a, b = self.g.edges[e]
        return "".join(sorted(self.labels[a] + self.labels[b]))

    def vset(self, s):
        return frozenset(self.idx[x] for x in s)

    def names(self, vs):
        return "".join(sorted(self.labels[x] for x in vs))


def claim(R, ok, text):
    R.out("  claim %-8s %s" % ("OK" if ok else "MISMATCH", text))
    if not ok:
        R.mismatches.append(text)
    return ok


def decomposition_claims(R, P, cuts, F_missing, squares, links, ent_lea, general_paths):
    """Compare the decomposition of the pair (P.u, P.v) with the claimed one.
    cuts: list of pairs of edge strings; F_missing: edge strings NOT in F; squares, links: lists of vertex strings in order;
    ent_lea: per square (entering terminals, leaving terminals) as strings; general_paths: per i the two sequences as strings."""
    g = P.g
    dec, bcuts, problems = brute_decomp(g, P.u, P.v)
    got_cuts = {frozenset([P.estr(e), P.estr(f)]) for e, f, A in bcuts}
    claim(R, got_cuts == {frozenset("".join(sorted(x)) for x in c) for c in cuts}, "minimum u-v cuts: %s" % sorted(map(sorted, got_cuts)))
    claim(R, set(range(g.m)) - set(dec.F) == {P.e(s) for s in F_missing}, "F contains every edge except %s" % (F_missing,))
    order = dec.square_order()
    claim(R, [frozenset(dec.pieces[p]) for p in order] == [P.vset(s) for s in squares], "squares in order: %s" % squares)
    got_links = sorted(P.names(dec.pieces[p]) for p in range(dec.np) if not dec.is_square[p])
    claim(R, got_links == sorted(links), "links: %s (computed %s)" % (links, got_links))
    for i, p in enumerate(order):
        et = P.names(set(dec.entering_terminals(p)))
        lt = P.names(set(dec.leaving_terminals(p)))
        claim(R, (et, lt) == tuple("".join(sorted(set(x))) for x in ent_lea[i]),
              "terminals of S_%d: entering {%s}, leaving {%s} (computed {%s}, {%s})" % (i + 1, *ent_lea[i], et, lt))
    for i in range(len(order) - 1):
        got = set()
        for e in dec.lea[order[i]]:
            edges, lk, end = dec.follow(e)
            seq = []
            for j, ee in enumerate(edges):
                seq.append(P.estr(ee))
                if j < len(lk):
                    seq.append("{" + P.names(dec.pieces[lk[j]]) + "}")
            got.add(",".join(seq))
        want = {",".join(t if t.startswith("{") else "".join(sorted(t)) for t in x) for x in general_paths[i]}
        claim(R, got == want, "general paths between S_%d and S_%d: %s (computed %s)" % (i + 1, i + 2, sorted(want), sorted(got)))
    return dec


def core_tex_examples(R):
    """Every graph and value stated in the examples of drafts/core.tex (Examples counterexamples, decomposition,
    worked, criterion, two-edges)."""
    base = ["ua", "us", "sb", "ab", "at", "tv", "bv"]
    # ---- Example counterexamples ------------------------------------------------------------------
    R.out("=" * 100)
    R.out("core.tex, Example counterexamples (G_a and G_b)")
    for name, extra, d_want, c_want in (("G_a", [], 3, 2), ("G_b", ["av", "ub"], 2, 3)):
        P = Pair(base + extra, "u", "v")
        g = P.g
        d, c = bfs(g, P.u)[P.v], edge_conn(g, P.u, P.v)
        cp, S = cp_brute(g, P.u, P.v)
        claim(R, (d, c) == (d_want, c_want), "%s: d(u,v) = %d, c(u,v) = %d" % (name, d_want, c_want))
        claim(R, cp == 3 and c + d - 1 == 4, "%s: cp(u,v) = 3, c + d - 1 = 4 (computed cp = %d, c + d - 1 = %d)" % (name, cp, c + d - 1))
        path = P.emask(["ua", "ab", "bv"])
        comp, k = components(g, path)
        parts = sorted(P.names([x for x in range(g.n) if comp[x] == j]) for j in range(k))
        claim(R, parts == sorted(["bsu", "atv"].__class__(["".join(sorted("usb")), "".join(sorted("atv"))])),
              "%s: removing the path u,a,b,v leaves the components {u,s,b} and {a,t,v} (computed %s)" % (name, parts))
        claim(R, is_cutpath(g, P.u, P.v, path) and popcount(path) == 3, "%s: u,a,b,v is a cut-path with three edges" % name)
        claim(R, in_dc(g)[0], "%s belongs to DC" % name)
        diam = max(max(row) for row in dist_matrix(g))
        cactus = max(edge_conn(g, x, y) for x in range(g.n) for y in range(x + 1, g.n)) <= 2
        claim(R, diam != 2 and not cactus, "%s: not of diameter two (diameter %d) and not a cactus graph" % (name, diam))
        if name == "G_a":
            big = sorted(P.labels[x] for x in range(g.n) if len(g.adj[x]) > 2)
            claim(R, big == ["a", "b"] and g.has_edge(P.idx["a"], P.idx["b"]),
                  "G_a: the only vertices of degree > 2 are a and b, which are adjacent (computed %s)" % big)
        else:
            D = dist_matrix(g)
            far = [(P.labels[x], P.labels[y]) for x in range(g.n) for y in range(x + 1, g.n) if D[x][y] == 3]
            claim(R, far == [("s", "t")] and len(g.adj[P.idx["s"]]) == 2 and len(g.adj[P.idx["t"]]) == 2,
                  "G_b: the only two vertices at distance three are s and t, both of degree two (computed %s)" % far)
    # ---- Example decomposition --------------------------------------------------------------------
    R.out("=" * 100)
    R.out("core.tex, Example decomposition (G_a)")
    P = Pair(base, "u", "v")
    decomposition_claims(R, P, cuts=[("ua", "us"), ("ua", "sb"), ("at", "bv"), ("tv", "bv")], F_missing=["ab"],
                         squares=["u", "ab", "v"], links=["s", "t"], ent_lea=[("u", "u"), ("ab", "ab"), ("v", "v")],
                         general_paths=[[["ua"], ["us", "{s}", "sb"]], [["at", "{t}", "tv"], ["bv"]]])
    # ---- Example worked ---------------------------------------------------------------------------
    R.out("=" * 100)
    R.out("core.tex, Example worked (G_1)")
    G1 = ["u1", "u2", "12", "13", "23", "36", "24", "45", "57", "67", "68", "7v", "8v"]
    P = Pair(G1, "u", "v")
    g = P.g
    claim(R, edge_conn(g, P.u, P.v) == 2 and bfs(g, P.u)[P.v] == 5, "G_1: c(u,v) = 2, d(u,v) = 5")
    for nm, es in (("p_1", ["u1", "13", "36", "68", "8v"]), ("p_2", ["u2", "24", "45", "57", "7v"])):
        pm = P.emask(es)
        claim(R, connected(g, P.u, P.v, removed=g.full() ^ pm) and popcount(pm) == 5, "%s is a u-v path with 5 edges" % nm)
    claim(R, P.emask(["u1", "13", "36", "68", "8v"]) & P.emask(["u2", "24", "45", "57", "7v"]) == 0, "p_1 and p_2 are edge-disjoint")
    dec = decomposition_claims(
        R, P, cuts=[("u1", "u2"), ("36", "24"), ("36", "45"), ("36", "57"), ("68", "7v"), ("8v", "7v")],
        F_missing=["12", "13", "23", "67"], squares=["u", "123", "67", "v"], links=["4", "5", "8"],
        ent_lea=[("u", "u"), ("12", "32"), ("67", "67"), ("v", "v")],
        general_paths=[[["u1"], ["u2"]], [["36"], ["24", "{4}", "45", "{5}", "57"]], [["68", "{8}", "8v"], ["7v"]]])
    # terminals as written in the text: a_2 = 1, b_2 = d_2 = 2, c_2 = 3, a_3 = c_3 = 6, b_3 = d_3 = 7
    order = dec.square_order()
    ent2 = sorted(P.labels[x] for x in dec.entering_terminals(order[1]))
    lea2 = sorted(P.labels[x] for x in dec.leaving_terminals(order[1]))
    claim(R, ent2 == ["1", "2"] and lea2 == ["2", "3"], "S_2: entering terminals 1, 2 and leaving terminals 3, 2 (b_2 = d_2 = 2)")
    deg = {P.labels[x]: len(g.adj[x]) for x in range(g.n)}
    claim(R, all(deg[x] == 2 for x in "u v 4 5 8".split()), "every vertex outside S_2 and S_3 has degree two")
    ok_adj = all(g.has_edge(P.idx[a], P.idx[b]) for sq in ("123", "67") for a in sq for b in sq if a < b)
    claim(R, ok_adj, "two vertices of the same square are adjacent")
    claim(R, in_dc(g)[0], "G_1 belongs to DC")
    # ---- Example criterion ------------------------------------------------------------------------
    R.out("=" * 100)
    R.out("core.tex, Example criterion")
    Pa = Pair(base, "u", "v")
    ga = Pa.g
    D = bfs(ga, Pa.u)
    Dv = bfs(ga, Pa.v)
    claim(R, D[Pa.idx["a"]] + 1 + Dv[Pa.idx["b"]] == 3 == D[Pa.v] and cp_brute(ga, Pa.u, Pa.v)[0] == 3,
          "G_a: d(u,a) + |p| + d(b,v) = 3 = d(u,v) for p = a,b, and cp(u,v) = 3")
    comp, k = components(ga, Pa.emask(["ab"]) | decomp_F_mask(Pa))
    claim(R, comp[Pa.idx["a"]] != comp[Pa.idx["b"]], "G_a: S_2 minus p has no edge, so it separates alpha = b from beta = a")
    # G_1
    g = P.g
    D, Dv = bfs(g, P.u), bfs(g, P.v)
    claim(R, D[P.idx["6"]] + 1 + Dv[P.idx["7"]] == 5 == D[P.v], "G_1: d(u,6) + |p| + d(7,v) = 3 + 1 + 1 = d(u,v) for p = 6,7")
    cp1, S1 = cp_brute(g, P.u, P.v)
    claim(R, cp1 == 5, "G_1: cp(u,v) = 5 (computed %d)" % cp1)
    mc = P.emask(["u1", "13", "36", "67", "7v"])
    claim(R, is_cutpath(g, P.u, P.v, mc) and popcount(mc) == 5, "G_1: u,1,3,6,7,v is a minimum cut-path (a cut-path with 5 = cp edges)")

    def paths_with_i(Pq, squares_only=True):
        """Edge sets of the paths p with at least one edge that satisfy condition (i) of the theorem, per square."""
        gq = Pq.g
        dq, cq, pq = None, None, None
        decq, _, _ = brute_decomp(gq, Pq.u, Pq.v)
        orderq = decq.square_order()
        Du, Dvv = bfs(gq, Pq.u), bfs(gq, Pq.v)
        d = Du[Pq.v]
        found = set()
        sep_any = False
        for i, p in enumerate(orderq):
            et, lt = decq.entering_terminals(p), decq.leaving_terminals(p)
            for x, alpha in {(et[0], et[1]), (et[1], et[0])}:
                for y, beta in {(lt[0], lt[1]), (lt[1], lt[0])}:
                    for pvs, pes in decq.piece_paths(x, y):
                        if pes and Du[x] + len(pes) + Dvv[y] == d:
                            found.add(frozenset(Pq.estr(e) for e in pes))
                            if decq.sep_in_piece(alpha, beta, mask_of(pes)):
                                sep_any = True
        return found, sep_any, decq

    found, sep_any, decq = paths_with_i(P)
    claim(R, sep_any, "G_1: some path with (i) separates alpha from beta (cp = d)")
    # G_1' : vertex 9 adjacent to 6 and 7
    P2 = Pair(G1 + ["96", "97"], "u", "v")
    g2 = P2.g
    dec2, _, _ = brute_decomp(g2, P2.u, P2.v)
    decG1 = brute_decomp(P.g, P.u, P.v)[0]
    F_same = {P2.estr(e) for e in dec2.F} == {P.estr(e) for e in decG1.F}
    claim(R, F_same, "G_1': F does not change")
    claim(R, bfs(g2, P2.u)[P2.idx["6"]] == 3 and bfs(g2, P2.v)[P2.idx["7"]] == 1 and bfs(g2, P2.u)[P2.v] == 5, "G_1': distances from u and to v do not change (d(u,6) = 3, d(7,v) = 1, d(u,v) = 5)")
    sq2 = [P2.names(dec2.pieces[p]) for p in dec2.square_order()]
    claim(R, sq2 == ["u", "123", "679", "v"], "G_1': squares S_1, S_2, S_4 do not change and S_3 = {6,7,9} (computed %s)" % sq2)
    found2, sep2, _ = paths_with_i(P2)
    claim(R, found2 == {frozenset(["13"]), frozenset(["23"]), frozenset(["67"])},
          "G_1': the only paths of the squares with (i) (at least one edge) are the edges 13, 23 and 67 (computed %s)" % sorted(map(sorted, found2)))
    claim(R, not sep2, "G_1': none of S_2 minus 13, S_2 minus 23, S_3 minus 67 separates alpha from beta (all connected)")
    claim(R, cp_brute(g2, P2.u, P2.v)[0] == 6, "G_1': cp(u,v) = 6")
    # G_1'' : remove vertex 5, add the edge 47
    G1pp = [s for s in G1 if "5" not in s] + ["47"]
    P3 = Pair(G1pp, "u", "v")
    g3 = P3.g
    dec3, _, _ = brute_decomp(g3, P3.u, P3.v)
    sq3 = [P3.names(dec3.pieces[p]) for p in dec3.square_order()]
    claim(R, bfs(g3, P3.u)[P3.v] == 4, "G_1'': d(u,v) = 4")
    claim(R, sq3 == ["u", "123", "67", "v"], "G_1'': the squares are those of G_1 (computed %s)" % sq3)
    found3, sep3, _ = paths_with_i(P3)
    claim(R, not found3, "G_1'': no path with at least one edge in a square satisfies (i) (computed %s)" % sorted(map(sorted, found3)))
    claim(R, cp_brute(g3, P3.u, P3.v)[0] == 5, "G_1'': cp(u,v) = 5")
    # ---- Example two-edges ------------------------------------------------------------------------
    R.out("=" * 100)
    R.out("core.tex, Example two-edges (G_a^+)")
    P4 = Pair(base + ["ru", "rb"], "u", "v")
    g4 = P4.g
    big = sorted(P4.labels[x] for x in range(g4.n) if len(g4.adj[x]) > 2)
    D4 = dist_matrix(g4)
    claim(R, big == ["a", "b", "u"] and all(D4[P4.idx[x]][P4.idx[y]] <= 2 for x in "abu" for y in "abu") and in_dc(g4)[0],
          "G_a^+: vertices of degree > 2 are u, a, b, pairwise at distance <= 2; G_a^+ is in DC (computed %s)" % big)
    dec4 = decomposition_claims(R, P4, cuts=[("at", "bv"), ("tv", "bv")], F_missing=["ua", "us", "sb", "ab", "ru", "rb"],
                                squares=["abrsu", "v"], links=["t"], ent_lea=[("u", "ab"), ("v", "v")], general_paths=[[["at", "{t}", "tv"], ["bv"]]])
    t1 = P4.names(set(dec4.leaving_terminals(dec4.square_order()[0])))
    claim(R, t1 == "ab", "G_a^+: c_1 = a and d_1 = b (computed leaving terminals of S_1: %s)" % t1)
    res = algorithm.solve(g4, P4.u, P4.v)
    walk = [P4.u]
    for e in res["witness"][4]:
        walk.append(g4.other(e, walk[-1]))
    x, y, alpha, beta = P4.u, P4.idx["b"], P4.u, P4.idx["a"]
    ell = res["d"] - 0 - 1
    claim(R, res["d"] == 3 and ell == 2, "G_a^+: d(u,v) = 3 and l = d(u,v) - 0 - 1 = 2 for (x, alpha) = (u,u), (y, beta) = (b,a)")
    claim(R, res["cp"] == 3 and "".join(P4.labels[w] for w in walk) == "uabv",
          "G_a^+: the algorithm returns 3 and the path u,a,b,v (computed %d, %s)" % (res["cp"], "".join(P4.labels[w] for w in walk)))
    # a is isolated in S_1 minus p, p = u,a,b
    rem = P4.emask(["ua", "ab"]) | mask_of(dec4.F)
    claim(R, len(g4.adj[P4.idx["a"]]) == 3 and all(((rem >> e) & 1) for _, e in g4.adj[P4.idx["a"]]),
          "G_a^+: the vertex a is isolated in S_1 minus p for p = u,a,b")


def decomp_F_mask(P):
    dec, _, _ = brute_decomp(P.g, P.u, P.v)
    return dec.Fmask


def theorem_witnesses(P):
    """Paths p (as label strings) that satisfy (i) and (ii) of the theorem of core.tex, over all squares and all
    terminal pairs; p has at least one edge."""
    g = P.g
    dec, _, _ = brute_decomp(g, P.u, P.v)
    order = dec.square_order()
    Du, Dv = bfs(g, P.u), bfs(g, P.v)
    d = Du[P.v]
    res = []
    for i, p in enumerate(order):
        et, lt = dec.entering_terminals(p), dec.leaving_terminals(p)
        for x, alpha in {(et[0], et[1]), (et[1], et[0])}:
            for y, beta in {(lt[0], lt[1]), (lt[1], lt[0])}:
                for pvs, pes in dec.piece_paths(x, y):
                    if pes and Du[x] + len(pes) + Dv[y] == d and dec.sep_in_piece(alpha, beta, mask_of(pes)):
                        res.append("".join(P.labels[w] for w in pvs))
    return res


def notes_graphs(R):
    """The graphs of Section 4 ('Graphs to verify') of drafts/core-notes.md, with the values claimed there."""
    R.out("=" * 100)
    R.out("core-notes.md, Section 4: Graphs to verify")
    Ga = ["ua", "us", "sb", "ab", "at", "tv", "bv"]
    # G_a, the pair (s, t)
    P = Pair(Ga, "s", "t")
    g = P.g
    d, c, (cp, _) = bfs(g, P.u)[P.v], edge_conn(g, P.u, P.v), cp_brute(g, P.u, P.v)
    claim(R, (d, c, cp) == (3, 2, 3), "G_a, the pair (s,t): cp = d = 3 (computed d = %d, c = %d, cp = %d)" % (d, c, cp))
    # G_b: delta({u,s,b}) = {ua, ab, bv} is the path u,a,b,v
    P = Pair(Ga + ["av", "ub"], "u", "v")
    g = P.g
    A = sum(1 << P.idx[x] for x in "usb")
    bd = mask_of(e for e, (a, b) in enumerate(g.edges) if ((A >> a) ^ (A >> b)) & 1)
    claim(R, bd == P.emask(["ua", "ab", "bv"]) and popcount(bd) == edge_conn(g, P.u, P.v) == 3
          and connected(g, P.u, P.v, removed=g.full() ^ bd), "G_b: delta({u,s,b}) = {ua, ab, bv} is a minimum cut and the path u,a,b,v")
    # G_1
    G1 = ["u1", "u2", "12", "13", "23", "36", "24", "45", "57", "67", "68", "7v", "8v"]
    P = Pair(G1, "u", "v")
    g = P.g
    claim(R, g.n == 10 and g.m == 13, "G_1 has 10 vertices and 13 edges")
    Du, Dv = bfs(g, P.u), bfs(g, P.v)
    name = lambda D: {P.labels[x]: D[x] for x in range(g.n)}   # noqa: E731
    claim(R, name(Du) == {"u": 0, "1": 1, "2": 1, "3": 2, "4": 2, "5": 3, "6": 3, "7": 4, "8": 4, "v": 5},
          "G_1: distances from u are 1:1, 2:1, 3:2, 4:2, 5:3, 6:3, 7:4, 8:4, v:5")
    claim(R, name(Dv) == {"v": 0, "7": 1, "8": 1, "5": 2, "6": 2, "3": 3, "4": 3, "1": 4, "2": 4, "u": 5},
          "G_1: distances to v are 7:1, 8:1, 5:2, 6:2, 3:3, 4:3, 1:4, 2:4, u:5")
    sp = sorted("".join(P.labels[w] for w in vs) for vs, es in simple_paths(g, P.u, P.v, maxlen=5) if len(es) == 5)
    claim(R, sp == sorted(["u1367v", "u2367v", "u2457v", "u1368v", "u2368v"]), "G_1: the five shortest u-v paths (computed %s)" % sp)
    D = dist_matrix(g)
    claim(R, max(max(r) for r in D) == 5 and max(edge_conn(g, x, y) for x in range(g.n) for y in range(x + 1, g.n)) == 3,
          "G_1: diameter 5, largest cut-value 3")
    # G_1'
    P2 = Pair(G1 + ["96", "97"], "u", "v")
    g2 = P2.g
    cuts1 = {frozenset([P.estr(e), P.estr(f)]) for e, f, A in min_cuts2(g, P.u, P.v)}
    cuts2 = {frozenset([P2.estr(e), P2.estr(f)]) for e, f, A in min_cuts2(g2, P2.u, P2.v)}
    claim(R, (bfs(g2, P2.u)[P2.v], edge_conn(g2, P2.u, P2.v), cp_brute(g2, P2.u, P2.v)[0]) == (5, 2, 6) and cuts1 == cuts2 and in_dc(g2)[0],
          "G_1': d = 5, c = 2, cp = 6, the same minimum cuts as G_1, in DC")
    claim(R, not theorem_witnesses(P2), "G_1': no path with (i) satisfies (ii)")
    # G_1''
    G1pp = ["u1", "u2", "12", "13", "23", "36", "24", "47", "67", "68", "7v", "8v"]
    P3 = Pair(G1pp, "u", "v")
    g3 = P3.g
    claim(R, sorted(G1pp) == sorted([s for s in G1 if "5" not in s] + ["47"]), "G_1'': the edge list of the notes is G_1 without vertex 5 plus 47")
    claim(R, (bfs(g3, P3.u)[P3.v], edge_conn(g3, P3.u, P3.v), cp_brute(g3, P3.u, P3.v)[0]) == (4, 2, 5) and in_dc(g3)[0], "G_1'': d = 4, c = 2, cp = 5, in DC")
    decomposition_claims(R, P3, cuts=[("u1", "u2"), ("36", "24"), ("36", "47"), ("68", "7v"), ("8v", "7v")],
                         F_missing=["12", "13", "23", "67"], squares=["u", "123", "67", "v"], links=["4", "8"],
                         ent_lea=[("u", "u"), ("12", "32"), ("67", "67"), ("v", "v")],
                         general_paths=[[["u1"], ["u2"]], [["36"], ["24", "{4}", "47"]], [["68", "{8}", "8v"], ["7v"]]])
    sp3 = ["".join(P3.labels[w] for w in vs) for vs, es in simple_paths(g3, P3.u, P3.v, maxlen=4) if len(es) == 4]
    claim(R, sp3 == ["u247v"], "G_1'': the only shortest path is u,2,4,7,v (computed %s)" % sp3)
    # G_a^+
    P4 = Pair(Ga + ["ur", "rb"], "u", "v")
    claim(R, (bfs(P4.g, P4.u)[P4.v], edge_conn(P4.g, P4.u, P4.v), cp_brute(P4.g, P4.u, P4.v)[0]) == (3, 2, 3) and in_dc(P4.g)[0],
          "G_a^+: d = 3, c = 2, cp = 3, in DC")
    # further graphs
    R.out("  further graphs used in the checks of the math core:")
    P5 = Pair(Ga + ["wa", "wb"], "u", "v")
    d5, cp5 = bfs(P5.g, P5.u)[P5.v], cp_brute(P5.g, P5.u, P5.v)[0]
    claim(R, (d5, cp5) == (3, 4), "G_a plus a vertex w adjacent to a, b: cp = 4 = d + 1 (computed d = %d, cp = %d)" % (d5, cp5))
    P6 = Pair(["ux", "uk", "kl", "lA", "xB", "xz", "zB", "Ay", "Aq", "qy", "xw", "wy", "yv", "Bm", "mn", "nv"], "u", "v")
    g6 = P6.g
    dec6, _, _ = brute_decomp(g6, P6.u, P6.v)
    sq6 = [P6.names(dec6.pieces[p]) for p in dec6.square_order()]
    claim(R, g6.n == 13 and (bfs(g6, P6.u)[P6.v], edge_conn(g6, P6.u, P6.v), cp_brute(g6, P6.u, P6.v)[0]) == (4, 2, 4) and not in_dc(g6)[0],
          "13-vertex graph with a separating trace of two edges: d = 4, c = 2, cp = 4, not in DC")
    claim(R, sq6 == ["u", "".join(sorted("ABqwxyz")), "v"], "  its squares are {u}, {A,B,q,w,x,y,z}, {v} (computed %s)" % sq6)
    claim(R, "xwy" in theorem_witnesses(P6) or "ywx" in theorem_witnesses(P6), "  the path p = x,w,y satisfies (i) and (ii) (witnesses %s)" % theorem_witnesses(P6))
    S6terms = P6.names(dec6.terminals(dec6.square_order()[1]))
    claim(R, S6terms == "".join(sorted("ABxy")), "  the middle square has four distinct terminals alpha = A, beta = B, x, y (computed %s)" % S6terms)
    # FINDING: doubt 8 of the notes ("in the class a separating trace has at most three distinct terminals") is false.
    # Minimal instance found (greedy deletion from a random chain with 31 vertices); vertices 0..20 are written
    # 0-9, a-k (a = 10, b = 11, c = 12, d = 13, e = 14, f = 15, g = 16, h = 17, i = 18, j = 19, k = 20); u = 1, v = 11 = b.
    R.out("  FINDING (contradicts doubt 8 of core-notes.md): a graph in DC with a separating trace that has four distinct terminals")
    P10 = Pair(["01", "02", "1d", "2d", "2e", "2f", "34", "39", "4f", "5e", "5g", "68", "6a", "6i", "79", "7a", "7j", "89", "8a",
                "ab", "bc", "ck", "gh", "hi", "jk"], "1", "b")
    g10 = P10.g
    d10 = bfs(g10, P10.u)[P10.v]
    dec10, _, _ = brute_decomp(g10, P10.u, P10.v)
    sq10 = [P10.names(dec10.pieces[p]) for p in dec10.square_order()]
    claim(R, (g10.n, g10.m, d10, edge_conn(g10, P10.u, P10.v), cp_brute(g10, P10.u, P10.v)[0]) == (21, 25, 9, 2, 9) and in_dc(g10)[0],
          "  21 vertices, 25 edges, d = 9, c = 2, cp = 9 = d, in DC")
    sep10 = sorted("".join(P10.labels[w] for w in vs) for vs, es in simple_paths(g10, P10.u, P10.v, maxlen=9)
                   if len(es) == 9 and not connected(g10, P10.u, P10.v, removed=mask_of(es)))
    claim(R, sep10 == ["102f4397ab", "1d2f4397ab"],
          "  the separating shortest paths are u,0,2,f,4,3,9,7,a,b and u,d,2,f,4,3,9,7,a,b (computed %s)" % sep10)
    claim(R, sq10[2] == "".join(sorted("67 89a".replace(" ", ""))) and set(P10.names(dec10.terminals(dec10.square_order()[2]))) == set("679a"),
          "  the third square {6,7,8,9,a} has the four distinct terminals 9, 6 (entering) and 7, a (leaving) (computed square %s)" % sq10[2])
    claim(R, "97a" in theorem_witnesses(P10) or "a79" in theorem_witnesses(P10),
          "  the trace p = 9,7,a (x = 9, y = a, alpha = 6, beta = 7) satisfies (i) and (ii) (witnesses %s)" % theorem_witnesses(P10))
    P7 = Pair(["12", "23", "34", "45", "56", "61"], "1", "4")
    dec7, _, _ = brute_decomp(P7.g, P7.u, P7.v)
    claim(R, cp_brute(P7.g, P7.u, P7.v)[0] == 4 and sorted(P7.names(dec7.pieces[p]) for p in dec7.square_order()) == ["1", "4"]
          and sum(1 for p in range(dec7.np) if not dec7.is_square[p]) == 4, "C_6 with antipodal u, v: cp = 4, squares {u}, {v}, four links")
    P8 = Pair(["ua", "aw", "wb", "bu", "wc", "cv", "ve", "ew"], "u", "v")
    dec8, _, _ = brute_decomp(P8.g, P8.u, P8.v)
    claim(R, cp_brute(P8.g, P8.u, P8.v)[0] == 5 and [P8.names(dec8.pieces[p]) for p in dec8.square_order()] == ["u", "w", "v"],
          "two 4-cycles sharing a vertex w: cp = 5, squares {u}, {w}, {v}")
    P9 = Pair(["12", "13", "14", "23", "24", "34", "u1", "u2", "v3", "v4"], "u", "v")
    dec9, _, _ = brute_decomp(P9.g, P9.u, P9.v)
    claim(R, cp_brute(P9.g, P9.u, P9.v)[0] == 4 and [P9.names(dec9.pieces[p]) for p in dec9.square_order()] == ["u", "1234", "v"]
          and all(dec9.is_square[p] for p in range(dec9.np)), "K_4 on 1..4 with u adjacent to 1, 2 and v adjacent to 3, 4: cp = 4, squares {u}, {1,2,3,4}, {v}, no link")


def main():
    R = Report()
    R.out("verify_named_graphs.py")
    base = ["ta", "tv", "au", "ab", "vb", "us", "sb"]
    # (a): c = 2, d = 3, cp = 3 (a shortest path that is also a cut)
    describe(R, "counterexample (a) of the research map", [tuple(s) for s in base], "u", "v",
             claims=dict(d=3, c=2, cp=3, k=3))
    # (b): d = 2, c = 3, cp = 3 (a minimum cut that is also a path)
    describe(R, "counterexample (b) of the research map", [tuple(s) for s in base + ["av", "ub"]], "u", "v",
             claims=dict(d=2, c=3, cp=3))
    core_tex_examples(R)
    notes = read_core_notes()
    R.out("=" * 100)
    if notes is None:
        R.out("drafts/core-notes.md: no section 'Graphs to verify' found (file missing or section absent at the time of this run)")
    else:
        R.out("drafts/core-notes.md has a section 'Graphs to verify'; each graph in it is verified by the calls below "
              "(edge lists and values copied from the section by hand).")
        notes_graphs(R)
    R.out("=" * 100)
    R.out("claims checked: %d mismatches" % len(R.mismatches))
    for m in R.mismatches:
        R.out("  MISMATCH: %s" % (m,))
    with open(os.path.join(HERE, "results-named-graphs.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(R.lines) + "\n")
    if R.mismatches:
        print("MISMATCHES:", R.mismatches)


if __name__ == "__main__":
    main()
