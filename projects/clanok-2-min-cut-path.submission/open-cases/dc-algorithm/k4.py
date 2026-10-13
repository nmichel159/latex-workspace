"""A two-choice hypergraph (2CH) encoding of 3-colouring K4, as a test case for path consistency (PC).

Gadget p (p = 0..3, the vertices of K4) has three parallel routes R(p,c) (c = colour) between the nodes n_p and
n_{p+1}; s = n_0, t = n_4.  For every edge {p, q} (p < q) and colour c there is a switch sigma(p,q,c) whose E-set lies
on route R(p,c) and whose F-set lies on route R(q,c): colouring p and q with the same c needs sigma in both modes.
A route is the chain n_p - X_1 - m_1 - X_2 - m_2 - X_3 - n_{p+1} of the three sets of its switches (private nodes
m_1, m_2), in the order given by `order` (a permutation of the three neighbours of p).  Without connectors this is a
no-instance (K4 is not 3-colourable) and has no P2.

Usage: python k4.py base            (exact, AC, PC of the base instance)
       python k4.py isolated        (single connector options per pair that keep the answer 'no')
"""
import os
import sys
import itertools
import time

sys.setrecursionlimit(100000)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import zz  # noqa: E402
import hunt2  # noqa: E402


def build(order=None, k=4, colours=3):
    """Returns (N, E, F, s, t, labels) with E, F lists of bit masks; labels[i] = (p, q, c)."""
    nodes = {}

    def node(name):
        if name not in nodes:
            nodes[name] = len(nodes)
        return nodes[name]

    s = node(("n", 0))
    t = node(("n", k))
    for p in range(1, k):
        node(("n", p))
    labels = [(p, q, c) for p in range(k) for q in range(p + 1, k) for c in range(colours)]
    idx = {lab: i for i, lab in enumerate(labels)}
    E = [0] * len(labels)
    F = [0] * len(labels)
    for p in range(k):
        nbrs = [q for q in range(k) if q != p]
        for c in range(colours):
            seq = order[(p, c)] if order and (p, c) in order else nbrs
            chain = [node(("n", p))] + [node(("m", p, c, i)) for i in range(len(seq) - 1)] + [node(("n", p + 1))]
            for i, q in enumerate(seq):
                a, b = min(p, q), max(p, q)
                sw = idx[(a, b, c)]
                mask = (1 << chain[i]) | (1 << chain[i + 1])
                if p == a:
                    E[sw] |= mask
                else:
                    F[sw] |= mask
    return len(nodes), E, F, s, t, labels


def answer(inst):
    N, E, F, s, t = inst[:5]
    return zz.exact_dfs(zz.from_sw(*hunt2.ch_to_sw((N, E, F, s, t))))[0]


def p2_pairs(E, F):
    n = len(E)
    return [(i, l) for i in range(n) for l in range(i + 1, n) if not (E[i] & E[l]) and not (F[i] & F[l])]


def options(inst, i, l):
    """single connectors for the pair (i, l) that keep the answer 'no'"""
    N, E, F, s, t = inst[:5]
    good = []
    for side in "EF":
        for x in list(range(N)) + [N]:
            E2, F2 = list(E), list(F)
            if side == "E":
                E2[i] |= 1 << x
                E2[l] |= 1 << x
            else:
                F2[i] |= 1 << x
                F2[l] |= 1 << x
            if not answer((max(N, x + 1), E2, F2, s, t)):
                good.append((side, x))
    return good


if __name__ == "__main__":
    mode = sys.argv[1]
    inst = build()
    N, E, F, s, t, labels = inst
    z = zz.from_sw(*hunt2.ch_to_sw((N, E, F, s, t)))
    if mode == "base":
        import pcfast
        t0 = time.time()
        print("nodes", N, "switches", len(E), "ZZ n", z.n, "|R|", len(z.R))
        print("exact", zz.exact_dfs(z)[0], "AC", zz.ac_answer(z), flush=True)
        L = 2 * 3 * 4 + 1   # every u-v zigzag of the base instance uses 4 x 3 switches: length 2*12+1
        print("PC with L = %d:" % L, pcfast.pc_answer(z, L), "%.0fs" % (time.time() - t0), flush=True)
    elif mode == "isolated":
        bad = p2_pairs(E, F)
        print(len(bad), "pairs without P2")
        none = 0
        for i, l in bad:
            opt = options(inst, i, l)
            if not opt:
                none += 1
                print("no harmless connector for", labels[i], labels[l])
        print(none, "pairs with no harmless single connector")
