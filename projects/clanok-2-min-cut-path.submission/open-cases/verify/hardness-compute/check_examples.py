"""Specific numbers stated in theory-hardness.md for the reduction graphs.

  E1  Corollary 2.6 (d): phi = (x1) and (x1): 20 vertices, 84 edges, c = 7, d = 2, diameter 3, two minimum cuts,
      every u-v path inside a minimum cut has length 5 (all simple u-v paths of both cut graphs enumerated)
  E2  Section 6.4: phi = (x1)(x2)(not x3)(not x4): 16 minimum cuts, one contains a path, A_tau = down(o1) u down(o2),
      k* = 2; phi = (x1)(x2)(x3)(not x4)(not x5)(not x6): k* = 3
  E3  Remark (2) of Section 2.2: fillers of K_A and K_B are at distance 3 "with c = M - 1"
  E4  Corollary 2.6 (d) for small satisfiable formulas: every u-v path inside a minimum cut (all simple paths of
      every path-containing cut graph) has odd length >= 2m + 1; distribution of the lengths
Output: results-examples.txt
"""

import os
import sys

import networkx as nx

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import vlib  # noqa: E402
import vred  # noqa: E402

out = []


def say(s):
    out.append(s)
    print(s)


def cut_graph_paths(g, A, u, v):
    H = nx.Graph()
    H.add_nodes_from(range(g.n))
    H.add_edges_from((a, b) for a, b in g.edges if (a in A) != (b in A))
    return list(nx.all_simple_paths(H, u, v))


def down_up(g, u, v, cuts):
    """down(x): smallest minimum cut containing x; up(x): largest minimum cut avoiding x (None if none)."""
    down, up = {}, {}
    for x in range(g.n):
        cont = [A for A in cuts if x in A]
        avoid = [A for A in cuts if x not in A]
        if cont:
            I = frozenset.intersection(*cont)
            assert I in set(cuts)
            down[x] = I
        if avoid:
            U = frozenset.union(*avoid)
            assert U in set(cuts)
            up[x] = U
    return down, up


def kstar(g, u, v, cuts):
    down, up = down_up(g, u, v, cuts)
    Amin = frozenset.intersection(*cuts)
    Amax = frozenset.union(*cuts)
    best = None
    for A in cuts:
        if not vlib.cut_graph_connects(g, A, u, v):
            continue
        ds = {down[x] for x in A - Amin}
        dmax = [D for D in ds if not any(D < E for E in ds)]
        us = {up[y] for y in Amax - A}
        umin = [U for U in us if not any(E < U for E in us)]
        gen = min(len(dmax), len(umin))
        best = gen if best is None else min(best, gen)
    return best


def main():
    # E1
    R = vred.build([[1], [1]])
    g, u, v = R["g"], R["u"], R["v"]
    c, cuts = vlib.min_cuts_residual(g, u, v)
    D = vlib.distances(g)
    lens = set()
    for A in cuts:
        for p in cut_graph_paths(g, A, u, v):
            lens.add(len(p) - 1)
    say("E1 (x1)(x1): n=%d e=%d c=%d d=%d diam=%d cuts=%d path lengths in minimum cuts=%s  [claimed 20, 84, 7, 2, 3, 2, {5}]"
        % (g.n, g.m, c, D[u, v], D.max(), len(cuts), sorted(lens)))
    # E2
    for f, claim in [([[1], [2], [-3], [-4]], 2), ([[1], [2], [3], [-4], [-5], [-6]], 3)]:
        R = vred.build(f)
        g, u, v = R["g"], R["u"], R["v"]
        c, cuts = vlib.min_cuts_residual(g, u, v)
        yes = [A for A in cuts if vlib.cut_graph_connects(g, A, u, v)]
        down, up = down_up(g, u, v, cuts)
        extra = ""
        if len(f) == 4:
            o1, o2 = R["O"][1][0], R["O"][2][0]
            extra = " A_tau == down(o1) | down(o2): %s;" % (yes[0] == (down[o1] | down[o2]))
            single = any(yes[0] == down[x] for x in down) or any(yes[0] == up[x] for x in up)
            extra += " single-generated: %s;" % single
        say("E2 %s: cuts=%d path-containing=%d;%s k*=%s [claimed k*=%d]" % (f, len(cuts), len(yes), extra,
                                                                          kstar(g, u, v, cuts), claim))
    # E3
    for f in ([[1], [1]], [[1, 2, 3]], [[1, -2, 3], [-1, 2, -3]]):
        R = vred.build(f)
        g = R["g"]
        fa, fb = R["KA"][-1], R["KB"][-1]
        D = vlib.distances(g)
        say("E3 %s: M=%d c0=%d filler pair d=%d c=%d  [Remark (2) says c = M - 1 = %d]"
            % (f, R["M"], R["c0"], D[fa, fb], vlib.flow_value(g, [fa], [fb]), R["M"] - 1))
    # E4
    import itertools
    lits = [1, -1, 2, -2]
    cnt = 0
    bad = 0
    hist = {}
    for m in (1, 2, 3):
        for f in itertools.product([(a,) for a in lits] + [tuple(s) for s in itertools.combinations_with_replacement(lits, 2)], repeat=m):
            f = [list(C) for C in f]
            if not vred.is_sat(f):
                continue
            R = vred.build(f)
            g, u, v = R["g"], R["u"], R["v"]
            c, cuts = vlib.min_cuts_residual(g, u, v)
            for A in cuts:
                if not vlib.cut_graph_connects(g, A, u, v):
                    continue
                for p in cut_graph_paths(g, A, u, v):
                    l = len(p) - 1
                    hist[(m, l)] = hist.get((m, l), 0) + 1
                    if l < 2 * m + 1 or l % 2 == 0 or l > c:
                        bad += 1
            cnt += 1
    say("E4 %d satisfiable formulas (clauses of 1-2 literals over x1, x2, m <= 3): paths violating odd length in "
        "[2m+1, c]: %d; (m, length): count = %s" % (cnt, bad, dict(sorted(hist.items()))))
    with open(os.path.join(HERE, "results-examples.txt"), "w") as fh:
        fh.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
