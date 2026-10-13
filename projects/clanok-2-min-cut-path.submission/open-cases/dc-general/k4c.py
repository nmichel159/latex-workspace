"""3-colouring of K4 encoded in 2CH with classes (2CHC), as a test case for path consistency (PC) under P2.

Segment p (p = 0..3, the vertices of K4) has three parallel routes (p, c) (c = colour) from n_p to n_{p+1}; s = n_0,
t = n_4.  For every edge {p, q} (p < q) and colour c there is a class sigma(p,q,c) with two members: the e-member, whose
E-side is a piece of route (p, c) and whose F-side is empty, and the f-member, whose F-side is a piece of route (q, c)
and whose E-side is empty.  Route (p, c) is the chain n_p - X_1 - m_1 - X_2 - m_2 - X_3 - n_{p+1} of the pieces of
its three classes (private nodes m_1, m_2).  Colouring p and q with c needs sigma(p,q,c) in both modes, so the base
instance is a no-instance; it is the 2CH instance of dc-algorithm/k4.py with every switch split into two tied
members, which leaves the empty sides free for P2 connectors.

Usage: python k4c.py base          exact, AC, PC (L = shortest relaxed walk) of the base instance
"""
import os
import sys
import time

for _v in ("OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "OMP_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gzz  # noqa: E402
import tools  # noqa: E402


def build(k=4, colours=3, order=None):
    """Returns (inst, info): inst = (N, E, F, cls, s, t); info: names of nodes, member labels, route pieces."""
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
    E, F, cls, mlab = [], [], [], []
    idx = {}
    for j, lab in enumerate(labels):
        idx[(lab, "e")] = len(E)
        E.append(0); F.append(0); cls.append(j); mlab.append((lab, "e"))
        idx[(lab, "f")] = len(E)
        E.append(0); F.append(0); cls.append(j); mlab.append((lab, "f"))
    route = {}
    for p in range(k):
        nbrs = [q for q in range(k) if q != p]
        for c in range(colours):
            seq = order[(p, c)] if order and (p, c) in order else nbrs
            chain = [node(("n", p))] + [node(("m", p, c, i)) for i in range(len(seq) - 1)] + [node(("n", p + 1))]
            route[(p, c)] = []
            for i, q in enumerate(seq):
                a, b = min(p, q), max(p, q)
                mask = (1 << chain[i]) | (1 << chain[i + 1])
                if p == a:
                    m = idx[((a, b, c), "e")]
                    E[m] |= mask
                else:
                    m = idx[((a, b, c), "f")]
                    F[m] |= mask
                route[(p, c)].append(m)
    inst = (len(nodes), E, F, cls, s, t)
    return inst, {"nodes": nodes, "mlab": mlab, "route": route, "idx": idx}


if __name__ == "__main__":
    inst, info = build()
    z, names = gzz.to_zz(inst)
    print("nodes", inst[0], "members", len(inst[1]), "classes", len(set(inst[3])), "ZZ n", z.n, "|R|", len(z.R))
    print("P2 missing pairs:", len(gzz.p2_missing(inst)))
    t0 = time.time()
    print("exact (branch and bound):", tools.bb_solve(inst) is not None, "%.1fs" % (time.time() - t0))
    L0 = tools.shortest_relaxed_L(z)
    print("shortest relaxed walk length:", L0)
    t0 = time.time()
    print("AC_L0:", tools.ac_L(z, L0), "%.1fs" % (time.time() - t0), flush=True)
    t0 = time.time()
    print("PC_L0:", tools.pc_L(z, L0), "%.1fs" % (time.time() - t0), flush=True)
