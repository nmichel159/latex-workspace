"""Points (a), (j), (k) and the preliminaries: own checks on all connected graphs with 2..N vertices.

  MINCUT   lem:minimum-cuts for every pair and every minimum cut (any cut-value), N <= 6
  UNCROSS  lem:uncrossing for random pairs of vertex sets
  CLASS    prop:class: the relation c >= 3 is an equivalence; membership in the class
  EASY     prop:easy-pairs (i)-(iv) with the statements on minimum cut-paths
  BRIDGE   rem:bridges
  OPEN     prop:open-pairs
  PAD      thm:hardness: the padding, and the description of the decomposition of G'
"""

import argparse
import itertools
import os
import random
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ref
from ref import E

done, fails = Counter(), []


def test(name, cond, detail=None):
    done[name] += 1
    if not cond and len(fails) < 30:
        fails.append((name, detail))


def atlas(nmin, nmax):
    import networkx as nx
    from networkx.generators.atlas import graph_atlas_g
    for G in graph_atlas_g():
        n = G.number_of_nodes()
        if nmin <= n <= nmax and nx.is_connected(G):
            adj = ref.graph(sorted(G.edges()))
            yield n, adj


def all_min_cuts(adj, u, v):
    """All minimum u-v cuts as (edge set) by enumeration of the sides A."""
    others = [x for x in adj if x != u and x != v]
    best, res = None, set()
    for r in range(len(others) + 1):
        for sub in itertools.combinations(others, r):
            A = set(sub) | {u}
            d = frozenset(ref.delta(adj, A))
            if best is None or len(d) < best:
                best, res = len(d), {d}
            elif len(d) == best:
                res.add(d)
    return best, res


def sep_shortest(adj, u, v):
    d = ref.bfs(adj, u)[v]
    return any(len(p) - 1 == d and not ref.connected(adj, u, v, set(ref.path_edges(p)))
               for p in ref.all_simple_paths(adj, u, v, maxlen=d))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--maxn", type=int, default=6)
    args = ap.parse_args()
    rng = random.Random(3)
    for n, adj in atlas(2, args.maxn):
        vs = sorted(adj)
        cv = {(x, y): ref.cutvalue(adj, x, y) for x in vs for y in vs if x != y}
        dist = {x: ref.bfs(adj, x) for x in vs}
        alle = ref.edges_of(adj)
        # UNCROSS
        for _ in range(6):
            A = {x for x in vs if rng.random() < 0.5}
            B = {x for x in vs if rng.random() < 0.5}
            mm = sum(1 for e in alle if any(x in A - B for x in e) and any(x in B - A for x in e))
            test("UNCROSS", len(ref.delta(adj, A & B)) + len(ref.delta(adj, A | B)) ==
                 len(ref.delta(adj, A)) + len(ref.delta(adj, B)) - 2 * mm)
        # CLASS
        for x, y, z in itertools.permutations(vs, 3):
            if cv[(x, y)] >= 3 and cv[(y, z)] >= 3:
                test("CLASS-transitive", cv[(x, z)] >= 3)
        inc = all(dist[x][y] <= 2 or cv[(x, y)] <= 2 for x in vs for y in vs if x != y)
        test("CLASS-own-test-agrees", inc == ref.in_class(adj)[0])
        # bridges
        br = {e for e in alle if not ref.connected(adj, min(e), max(e), {e})}
        for u in vs:
            for v in vs:
                if u == v:
                    continue
                c, d = cv[(u, v)], dist[u][v]
                cuts = None
                cp, P = ref.cp_bruteforce(adj, u, v)
                test("BOUNDS", max(c, d) <= cp <= c + d - 1)
                test("BOUNDS-cp=d-iff-separating-shortest", (cp == d) == sep_shortest(adj, u, v))
                if n <= 6:
                    best, cuts = all_min_cuts(adj, u, v)
                    test("MINCUT-value", best == c)
                    for C in cuts:
                        comps = ref.components(adj, C)
                        test("MINCUT-two-components", len(comps) == 2)
                        A = ref.comp(adj, u, C)
                        test("MINCUT-delta-unique",
                             [frozenset(ref.delta(adj, set(s) | {u})) == C
                              for r in range(n - 1) for s in itertools.combinations([x for x in vs if x != u], r)
                              ].count(True) == 1 and frozenset(ref.delta(adj, A)) == C)
                    # parity for all A
                    paths = ref.all_simple_paths(adj, u, v)
                    for r in range(n - 1):
                        for s in itertools.combinations([x for x in vs if x != u and x != v], r):
                            dA = ref.delta(adj, set(s) | {u})
                            test("MINCUT-parity", all(len(dA & set(ref.path_edges(p))) % 2 == 1 for p in paths))
                    # OPEN
                    contains = [C for C in cuts
                                if ref.connected({x: {y for y in adj[x] if E(x, y) in C} for x in adj}, u, v)]
                    test("OPEN-iff", (cp == c) == bool(contains))
                    for C in contains:
                        sub = {x: {y for y in adj[x] if E(x, y) in C} for x in adj}
                        for p in ref.all_simple_paths(sub, u, v):
                            test("OPEN-odd", (len(p) - 1) % 2 == 1 and (d != 2 or len(p) - 1 >= 3))
                    # EASY
                    if d == 1:
                        test("EASY-i", cp == c and all(E(u, v) in C for C in cuts))
                    if c == 1:
                        test("EASY-ii", cp == d)
                    if c == 2:
                        test("EASY-iii", cp in (d, d + 1))
                    if d == 2:
                        test("EASY-iv", cp in (c, c + 1))
                # BRIDGE
                if br:
                    K = ref.comp(adj, u, br)
                    if v in K:
                        sub = {x: {y for y in adj[x] if y in K and E(x, y) not in br} for x in K}
                        test("BRIDGE-d-c-cp", ref.bfs(sub, u)[v] == d and ref.cutvalue(sub, u, v) == c and
                             ref.cp_bruteforce(sub, u, v)[0] == cp)
                        test("BRIDGE-paths", all(set(p) <= K for p in ref.all_simple_paths(adj, u, v)))
                    else:
                        test("BRIDGE-v-outside-K-means-c=1", c == 1)
                # PAD
                if c >= 2 and n <= 6:
                    g2 = {x: set(adj[x]) for x in adj}
                    for a, b in (("u'", "s1"), ("s1", u), ("u'", "s2"), ("s2", u)):
                        g2.setdefault(a, set()).add(b)
                        g2.setdefault(b, set()).add(a)
                    test("PAD-distance", ref.bfs(g2, "u'")[v] == d + 2)
                    test("PAD-cut-value", ref.cutvalue(g2, "u'", v) == 2)
                    test("PAD-equivalence", sep_shortest(g2, "u'", v) == sep_shortest(adj, u, v))
                    pp = ref.all_simple_paths(g2, "u'", v)
                    test("PAD-paths", all(p[0] == "u'" and p[1] in ("s1", "s2") and p[2] == u and
                                          not {"u'", "s1", "s2"} & set(p[3:]) for p in pp))
                    cuts2 = ref.min_cuts2(g2, "u'", v)
                    p1, p2 = ref.two_disjoint_paths(g2, "u'", v)
                    D = ref.Decomposition(g2, "u'", v, cuts2, p1, p2, allcuts=cuts2)
                    new = {E("u'", "s1"), E("s1", u), E("u'", "s2"), E("s2", u)}
                    if c >= 3:
                        test("PAD-F-is-the-four-new-edges", D.F == new)
                        test("PAD-squares", D.squares == [frozenset(["u'"]), frozenset(adj)])
                        test("PAD-links", set(D.links) == {frozenset(["s1"]), frozenset(["s2"])})
                        test("PAD-terminals", D.terminals(1) == (u, u, v, v))
                    else:
                        Fg = set().union(*ref.min_cuts2(adj, u, v))
                        test("PAD-c=2-F", D.F == new | Fg)
    for name in sorted(done):
        print("  %-40s %d" % (name, done[name]))
    print("FAILURES: %d" % len(fails))
    for f in fails:
        print("  ", f)


if __name__ == "__main__":
    main()
