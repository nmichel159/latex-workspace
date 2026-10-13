"""How many generators does a minimum cut containing a cut path need?

For a pair (u, v), a maximum flow and its residual digraph R, let gen_A(u,v) be the least j such that the
R-closure of {u} + (j vertices) spans a minimum cut containing a u-v path, and gen_B(u,v) the least j such that the
complement of the co-closure (vertices that reach v or one of j vertices) does.  (A cut path P lies in the cut
spanned by the closure of its even vertices, so gen_A <= number of inner even vertices of P; similarly gen_B.)
The tests H1, H1', H2 of test_generated_cuts.py are gen_A <= 1, gen_B <= 1, gen_A <= 2.

This script computes gen_A and gen_B exactly (search over subsets of increasing size, n <= 22) for the family
variants F(k) with both cliques, with the odd clique only, with the even clique only, and with none.
"""

import itertools
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cutpaths as cpz  # noqa: E402
from cutpaths import mcp, Gr, PairInfo  # noqa: E402
import family  # noqa: E402


def coreach(P):
    n = P.g.n
    co = [0] * n
    for x in range(n):
        r = P.reach[x]
        for y in range(n):
            if (r >> y) & 1:
                co[y] |= 1 << x
    return co


def cut_has_path(g, A, u, v):
    C = cpz.cut_mask_of_side(g, A)
    return mcp.connected(g, u, v, removed=g.full() ^ C)


def gen_numbers(g, u, v, P=None, jmax=6):
    if P is None:
        P = PairInfo(g, u, v)
    n = g.n
    full = (1 << n) - 1
    co = coreach(P)
    ga = gb = None
    for j in range(0, jmax + 1):
        if ga is None:
            for S in itertools.combinations(range(n), j):
                A = P.reach[u]
                for x in S:
                    A |= P.reach[x]
                if not (A >> v) & 1 and cut_has_path(g, A, u, v):
                    ga = j
                    break
        if gb is None:
            for S in itertools.combinations(range(n), j):
                B = co[v]
                for y in S:
                    B |= co[y]
                if not (B >> u) & 1 and cut_has_path(g, full ^ B, u, v):
                    gb = j
                    break
        if ga is not None and gb is not None:
            break
    return ga, gb


def gen_numbers_fast(g, u, v, P, paths):
    """gen_A, gen_B computed through the cut paths: a closed set A (u in A, v not in A) spans a minimum cut that
    contains a u-v path iff A contains the even and avoids the odd vertices of some cut path.  So gen_A is the
    minimum over cut paths p of the least number of vertices x (with reach[x] avoiding v and the odd vertices of
    p) whose closures, together with that of u, cover the even vertices of p.  Same for gen_B with co-closures.
    Equal to gen_numbers (checked in main on the variants of F(k))."""
    n = g.n
    co = coreach(P)
    best_a = best_b = None
    for p in paths:
        ev = 0
        od = 0
        for i, x in enumerate(p):
            if i % 2 == 0:
                ev |= 1 << x
            else:
                od |= 1 << x
        need_a = ev & ~P.reach[u]
        cand = [x for x in range(n) if not (P.reach[x] & (od | (1 << v))) and P.reach[x] & need_a]
        ja = _cover(need_a, [P.reach[x] & need_a for x in cand])
        need_b = od & ~co[v]
        cand = [y for y in range(n) if not (co[y] & (ev | (1 << u))) and co[y] & need_b]
        jb = _cover(need_b, [co[y] & need_b for y in cand])
        if ja is not None and (best_a is None or ja < best_a):
            best_a = ja
        if jb is not None and (best_b is None or jb < best_b):
            best_b = jb
    return best_a, best_b


def _cover(need, sets):
    if not need:
        return 0
    sets = sorted(set(sets), key=lambda s: -bin(s).count("1"))
    for j in range(1, len(sets) + 1):
        for S in itertools.combinations(sets, j):
            acc = 0
            for s in S:
                acc |= s
            if acc & need == need:
                return j
    return None


def variant(k, even_clique, odd_clique):
    g, u, v = family.family(k, False)
    es = list(g.edges)
    L = 2 * k + 1
    if even_clique:
        ev = list(range(0, L + 1, 2))
        es += [(a, b) for a, b in itertools.combinations(ev, 2)]
    if odd_clique:
        od = list(range(1, L + 1, 2))
        es += [(a, b) for a, b in itertools.combinations(od, 2)]
    return Gr(g.n, es), u, v


def main():
    lines = ["generators.py: gen_A, gen_B (see docstring) for variants of F(k)", ""]
    for k in range(1, 6):
        for ec, oc in ((True, True), (False, True), (True, False), (False, False)):
            g, u, v = variant(k, ec, oc)
            P = PairInfo(g, u, v)
            paths = P.cut_paths()
            lens = sorted(set(len(p) - 1 for p in paths))
            ga, gb = gen_numbers(g, u, v, P, jmax=k)
            fa, fb = gen_numbers_fast(g, u, v, P, paths)
            lines.append("k=%d even clique=%s odd clique=%s: n=%d m=%d DC=%s c=%d cut path lengths %s gen_A=%s gen_B=%s"
                         " (fast: %s %s)" % (k, ec, oc, g.n, g.m, cpz.in_dc(g), P.c, lens, ga, gb, fa, fb))
            print(lines[-1], flush=True)
    with open(os.path.join(HERE, "results-generators.txt"), "w") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
