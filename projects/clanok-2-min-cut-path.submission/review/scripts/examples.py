"""Point (l): recompute every value stated in the examples of drafts/core.tex.

Own code (ref.py) for everything; cp is cross-checked with checks/mcp.py (cp_brute) and, for small graphs,
with the literal definition.  Prints one line per claim: OK or MISMATCH.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(1, os.path.normpath(os.path.join(HERE, "..", "..", "checks")))

import ref
from ref import E, fmt, fmt_e

import mcp  # read-only import of the checks library

bad = 0
count = 0


def claim(name, got, want):
    global bad, count
    count += 1
    ok = got == want
    if not ok:
        bad += 1
    print("%-8s %s: got %s, text says %s" % ("OK" if ok else "MISMATCH", name, got, want))


def es(s):
    """'ua us sb' -> list of pairs; vertex names are single characters."""
    return [(w[0], w[1:]) for w in s.split()]


def cp_all(adj, u, v, literal=True):
    val, P = ref.cp_bruteforce(adj, u, v)
    names = sorted(adj, key=str)
    idx = {x: i for i, x in enumerate(names)}
    g = mcp.Gr(len(names), [(idx[a], idx[b]) for a in adj for b in adj[a] if idx[a] < idx[b]])
    val2 = mcp.cp_brute(g, idx[u], idx[v])[0]
    vals = {val, val2}
    if literal:
        vals.add(ref.cp_literal(adj, u, v)[0])
    assert len(vals) == 1, vals
    return val


def cutset(s):
    return frozenset(frozenset(E(w[0], w[1:]) for w in c.split()) for c in s.split("|"))


def describe(adj, u, v, p1, p2):
    cuts = ref.min_cuts2(adj, u, v)
    D = ref.Decomposition(adj, u, v, cuts, p1, p2)
    return cuts, D


# ---------------------------------------------------------------------------------------------------------
print("== ex:counterexamples: G_a, G_b ==")
Ga = ref.graph(es("ua us sb ab at tv bv"))
Gb = ref.graph(es("ua us sb ab at tv bv av ub"))
for name, G in (("G_a", Ga), ("G_b", Gb)):
    rem = {E("u", "a"), E("a", "b"), E("b", "v")}
    claim(name + " components after removing u,a,b,v",
          sorted(fmt(c) for c in ref.components(G, rem)), sorted([fmt("usb"), fmt("atv")]))
claim("G_a c(u,v)", ref.cutvalue(Ga, "u", "v"), 2)
claim("G_a d(u,v)", ref.bfs(Ga, "u")["v"], 3)
claim("G_b c(u,v)", ref.cutvalue(Gb, "u", "v"), 3)
claim("G_b d(u,v)", ref.bfs(Gb, "u")["v"], 2)
claim("G_a cp(u,v)", cp_all(Ga, "u", "v"), 3)
claim("G_b cp(u,v)", cp_all(Gb, "u", "v"), 3)
claim("G_a in the class", ref.in_class(Ga)[0], True)
claim("G_b in the class", ref.in_class(Gb)[0], True)
claim("G_a vertices of degree > 2", sorted(x for x in Ga if len(Ga[x]) > 2), ["a", "b"])
claim("G_a: a, b adjacent", "b" in Ga["a"], True)
far = sorted(tuple(sorted((x, y))) for x in Gb for y in Gb if x < y and ref.bfs(Gb, x)[y] >= 3)
claim("G_b pairs at distance >= 3", far, [("s", "t")])
claim("G_b d(s,t)", ref.bfs(Gb, "s")["t"], 3)
claim("G_b degrees of s, t", (len(Gb["s"]), len(Gb["t"])), (2, 2))
claim("G_a diameter", max(max(ref.bfs(Ga, x).values()) for x in Ga), 3)
claim("G_b diameter", max(max(ref.bfs(Gb, x).values()) for x in Gb), 3)


def is_cactus(adj):
    # connected and c(x,y) <= 2 for all pairs (Lemma 6.1 of article 1)
    vs = sorted(adj)
    return all(ref.cutvalue(adj, x, y, limit=3) <= 2 for i, x in enumerate(vs) for y in vs[i + 1:])


claim("G_a is a cactus graph", is_cactus(Ga), False)
claim("G_b is a cactus graph", is_cactus(Gb), False)

# ---------------------------------------------------------------------------------------------------------
print("== ex:decomposition: G_a ==")
p1, p2 = tuple("uatv"), tuple("usbv")
cuts, D = describe(Ga, "u", "v", p1, p2)
claim("G_a minimum cuts", frozenset(cuts), cutset("ua us|ua sb|at bv|tv bv"))
claim("G_a F = E minus ab", D.F, ref.edges_of(Ga) - {E("a", "b")})
claim("G_a squares in order", [fmt(S) for S in D.squares], [fmt("u"), fmt("ab"), fmt("v")])
claim("G_a links", sorted(fmt(L) for L in D.links), sorted([fmt("s"), fmt("t")]))
claim("G_a terminals of S_2 (a,b,c,d)", D.terminals(1), ("a", "b", "a", "b"))
gp = {fmt_e(e): ([fmt_e(x) for x in D.general_path(e)[0]], [fmt(L) for L in D.general_path(e)[1]])
      for S in D.squares for e in D.lea[S]}
claim("G_a P_{1,1}", gp["au"], (["au"], []))
claim("G_a P_{1,2}", gp["su"], (["su", "bs"], [fmt("s")]))
claim("G_a P_{2,1}", gp["at"], (["at", "tv"], [fmt("t")]))
claim("G_a P_{2,2}", gp["bv"], (["bv"], []))
claim("tail conflicts", D.tail_conflict, False)

# ---------------------------------------------------------------------------------------------------------
print("== ex:worked: G_1 ==")
G1 = ref.graph(es("u1 u2 12 13 23 36 24 45 57 67 68 7v 8v"))
claim("G_1 number of vertices, edges", (len(G1), len(ref.edges_of(G1))), (10, 13))
claim("G_1 c(u,v)", ref.cutvalue(G1, "u", "v"), 2)
claim("G_1 d(u,v)", ref.bfs(G1, "u")["v"], 5)
p1, p2 = tuple("u1368v"), tuple("u2457v")
claim("G_1 p_1, p_2 are edge-disjoint paths",
      all(e in ref.edges_of(G1) for e in ref.path_edges(p1) + ref.path_edges(p2))
      and not set(ref.path_edges(p1)) & set(ref.path_edges(p2)), True)
cuts, D = describe(G1, "u", "v", p1, p2)
claim("G_1 minimum cuts", frozenset(cuts), cutset("u1 u2|36 24|36 45|36 57|68 7v|8v 7v"))
claim("G_1 F = E minus {12,13,23,67}", D.F,
      ref.edges_of(G1) - {E("1", "2"), E("1", "3"), E("2", "3"), E("6", "7")})
claim("G_1 squares in order", [fmt(S) for S in D.squares], [fmt("u"), fmt("123"), fmt("67"), fmt("v")])
claim("G_1 links", sorted(fmt(L) for L in D.links), sorted([fmt("4"), fmt("5"), fmt("8")]))
claim("G_1 terminals of S_2", D.terminals(1), ("1", "2", "3", "2"))
claim("G_1 terminals of S_3", D.terminals(2), ("6", "7", "6", "7"))
gp = {fmt_e(e): ([fmt_e(x) for x in D.general_path(e)[0]], [fmt(L) for L in D.general_path(e)[1]])
      for S in D.squares for e in D.lea[S]}
claim("G_1 P_{1,1}, P_{1,2}, P_{2,1}, P_{3,2} single edges",
      [gp[k] for k in ("1u", "2u", "36", "7v")], [(["1u"], []), (["2u"], []), (["36"], []), (["7v"], [])])
claim("G_1 P_{2,2}", gp["24"], (["24", "45", "57"], [fmt("4"), fmt("5")]))
claim("G_1 P_{3,1}", gp["68"], (["68", "8v"], [fmt("8")]))
outside = [x for x in G1 if x not in "12367"]
claim("G_1 vertices outside S_2, S_3 have degree two", all(len(G1[x]) == 2 for x in outside), True)
claim("G_1 squares S_2, S_3 are cliques",
      all(y in G1[x] for S in ("123", "67") for x in S for y in S if x != y), True)
claim("G_1 cut {36,24} separates S_2 from S_3",
      not any(ref.connected(G1, x, y, {E("3", "6"), E("2", "4")}) for x in "123" for y in "67"), True)
claim("G_1 in the class", ref.in_class(G1)[0], True)

# ---------------------------------------------------------------------------------------------------------
print("== ex:criterion ==")


def witnesses(adj, u, v, p1, p2):
    """All (i, x, alpha, y, beta, p) with p having at least one edge and condition (i); flag = condition (ii)."""
    cuts = ref.min_cuts2(adj, u, v)
    D = ref.Decomposition(adj, u, v, cuts, p1, p2)
    du, dv = ref.bfs(adj, u), ref.bfs(adj, v)
    out = []
    for i, S in enumerate(D.squares):
        a, b, c, d = D.terminals(i)
        for x, al in ((a, b), (b, a)):
            for y, be in ((c, d), (d, c)):
                for p in ref.all_simple_paths(adj, x, y, allowed=S):
                    if len(p) - 1 >= 1 and du[x] + len(p) - 1 + dv[y] == du[v]:
                        sep = be not in ref.bfs(adj, al, set(ref.path_edges(p)), allowed=S)
                        out.append((i + 1, x, al, y, be, p, sep))
    return D, sorted(set(out))


D, W = witnesses(Ga, "u", "v", tuple("uatv"), tuple("usbv"))
claim("G_a witness (2,(a,b),(b,a),p=a,b) with (i) and (ii)", (2, "a", "b", "b", "a", ("a", "b"), True) in W, True)
claim("G_a d(u,a)+|p|+d(b,v)", ref.bfs(Ga, "u")["a"] + 1 + ref.bfs(Ga, "b")["v"], 3)

D, W = witnesses(G1, "u", "v", tuple("u1368v"), tuple("u2457v"))
claim("G_1 witness (3,(6,7),(7,6),p=6,7)", (3, "6", "7", "7", "6", ("6", "7"), True) in W, True)
claim("G_1 d(u,6), d(7,v)", (ref.bfs(G1, "u")["6"], ref.bfs(G1, "7")["v"]), (3, 1))
claim("G_1 cp(u,v)", cp_all(G1, "u", "v", literal=False), 5)
P = tuple("u1367v")
claim("G_1: u,1,3,6,7,v is a cut-path with 5 edges",
      (len(P) - 1, all(e in ref.edges_of(G1) for e in ref.path_edges(P)),
       ref.connected(G1, "u", "v", set(ref.path_edges(P)))), (5, True, False))

G1p = ref.graph(es("u1 u2 12 13 23 36 24 45 57 67 68 7v 8v 69 79"))
cuts1 = frozenset(ref.min_cuts2(G1, "u", "v"))
cutsp, Dp = describe(G1p, "u", "v", tuple("u1368v"), tuple("u2457v"))
claim("G_1' same minimum cuts (same F)", frozenset(cutsp), cuts1)
claim("G_1' distances from u unchanged", all(ref.bfs(G1p, "u")[x] == ref.bfs(G1, "u")[x] for x in G1), True)
claim("G_1' distances to v unchanged", all(ref.bfs(G1p, "v")[x] == ref.bfs(G1, "v")[x] for x in G1), True)
claim("G_1' squares", [fmt(S) for S in Dp.squares], [fmt("u"), fmt("123"), fmt("679"), fmt("v")])
Dp, W = witnesses(G1p, "u", "v", tuple("u1368v"), tuple("u2457v"))
claim("G_1' paths with an edge and (i)", sorted({(w[0], w[5]) for w in W}),
      sorted([(2, ("1", "3")), (2, ("2", "3")), (3, ("6", "7"))]))
claim("G_1' none of them satisfies (ii)", any(w[6] for w in W), False)
claim("G_1' S_2 minus 13, S_2 minus 23, S_3 minus 67 connected",
      [len(ref.bfs(G1p, "1", {E("1", "3")}, allowed=set("123"))),
       len(ref.bfs(G1p, "1", {E("2", "3")}, allowed=set("123"))),
       len(ref.bfs(G1p, "6", {E("6", "7")}, allowed=set("679")))], [3, 3, 3])
claim("G_1' cp(u,v)", cp_all(G1p, "u", "v", literal=False), 6)
claim("G_1' in the class (not claimed in the text)", ref.in_class(G1p)[0], True)

G1pp = ref.graph(es("u1 u2 12 13 23 36 24 47 67 68 7v 8v"))
claim("G_1'' d(u,v)", ref.bfs(G1pp, "u")["v"], 4)
claim("G_1'' c(u,v)", ref.cutvalue(G1pp, "u", "v"), 2)
p1, p2 = tuple("u1368v"), tuple("u247v")
cutspp, Dpp = describe(G1pp, "u", "v", p1, p2)
claim("G_1'' squares are those of G_1", [fmt(S) for S in Dpp.squares],
      [fmt("u"), fmt("123"), fmt("67"), fmt("v")])
Dpp, W = witnesses(G1pp, "u", "v", p1, p2)
claim("G_1'' no path with an edge satisfies (i)", W, [])
claim("G_1'' cp(u,v)", cp_all(G1pp, "u", "v", literal=False), 5)
claim("G_1'' in the class (not claimed in the text)", ref.in_class(G1pp)[0], True)

# ---------------------------------------------------------------------------------------------------------
print("== ex:two-edges: G_a^+ ==")
Gap = ref.graph(es("ua us sb ab at tv bv ur rb"))
claim("G_a^+ vertices of degree > 2", sorted(x for x in Gap if len(Gap[x]) > 2), ["a", "b", "u"])
claim("G_a^+ pairwise distances of u, a, b at most two",
      max(ref.bfs(Gap, x)[y] for x in "uab" for y in "uab"), 2)
claim("G_a^+ in the class", ref.in_class(Gap)[0], True)
claim("G_a^+ c(u,v), d(u,v)", (ref.cutvalue(Gap, "u", "v"), ref.bfs(Gap, "u")["v"]), (2, 3))
p1, p2 = tuple("uatv"), tuple("usbv")
cuts, D = describe(Gap, "u", "v", p1, p2)
claim("G_a^+ minimum cuts", frozenset(cuts), cutset("at bv|tv bv"))
claim("G_a^+ squares", [fmt(S) for S in D.squares], [fmt("usrab"), fmt("v")])
claim("G_a^+ links", [fmt(L) for L in D.links], [fmt("t")])
claim("G_a^+ terminals of S_1", D.terminals(0), ("u", "u", "a", "b"))
claim("G_a^+ l for x=u, y=b", ref.bfs(Gap, "u")["v"] - 0 - ref.bfs(Gap, "b")["v"], 2)
S1 = set("usrab")
claim("G_a^+ u,a is a path of S_1 and u,a,b is a path of S_1", ("a" in Gap["u"], "b" in Gap["a"]), (True, True))
rest = ref.bfs(Gap, "a", {E("u", "a"), E("a", "b")}, allowed=S1)
claim("G_a^+ a isolated in S_1 minus p", sorted(rest), ["a"])
claim("G_a^+ cp(u,v)", cp_all(Gap, "u", "v", literal=False), 3)
P = tuple("uabv")
claim("G_a^+ u,a,b,v separates u from v", ref.connected(Gap, "u", "v", set(ref.path_edges(P))), False)

# ---------------------------------------------------------------------------------------------------------
print("== sec:distance-two: G_b ==")
claim("G_b delta({u,s,b})", ref.delta(Gb, set("usb")), {E("u", "a"), E("a", "b"), E("b", "v")})

print()
print("claims: %d, mismatches: %d" % (count, bad))
sys.exit(1 if bad else 0)
