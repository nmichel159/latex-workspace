"""Family Y^d_k: the family Y_k of r4-general.md Section 6 plus one 'dead-end' switch d that gives s a second exit.

Y_k (switch form, built by r4-general/yfam.rword read-only): base R(E^k F^k) with path sides h_j, flip sides Fl_j,
mates m_c > x_c (c <= k) with F(m_c) = {f_cb : b != c} (f_cb in Fl_b) and E(m_c) = {e_cq} (e_cq in Fl_q) + g-nodes.
New switch d (incomparable with every switch):
  E(d) = {s} + {gamma_c : c <= k} + {delta_q : q F-member},  gamma_c added to E(m_c), delta_q added to Fl_q = E(x_q);
  F(d) = {eps_b : b E-member} (+ {t} and a node kappa shared with E(m_1) if back=True),  eps_b added to Fl_b = F(x_b).
P2 of d: with E-members through eps_b (F-sides), with F-members through delta_q (E-sides), with mates through gamma_c.
Purpose: the forced-exit propagation of r4-general (gsw.prune) starts from s and needs a single exit; with d the
node s has two exits (h_1 and E(d)), so the first-flip induction that makes Y_k rigid is never started.
"""
import os
import sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gcore                     # noqa: E402  (sets the import path)
from gcore import Gen, bits      # noqa: E402
import yfam                      # noqa: E402  (r4-general, read-only)


def yd(k, back=False, contact=False, gadget=True):
    I0, full, info = yfam.yfam(k, contact=contact)
    E = [set(e) for e in info["E"]]
    F = [set(f) for f in info["F"]]
    mle = [list(r) for r in info["mle"]]
    nodes = dict(info["nodes"])
    s, t = info["s"], info["t"]
    names = list(info["swnames"])

    def node(name):
        if name not in nodes:
            nodes[name] = len(nodes)
        return nodes[name]

    L = 2 * k
    # switch indices: x_j -> j - 1 (j = 1..2k); m_c -> names.index(("m", c))
    if gadget:
        Ed, Fd = {s}, set()
        for c in range(1, k + 1):
            mi = names.index(("m", c))
            g = node(("gamma", c))
            Ed.add(g)
            E[mi].add(g)
        for q in range(k + 1, L + 1):
            dq = node(("delta", q))
            Ed.add(dq)
            E[q - 1].add(dq)              # Fl_q = E(x_q) for an F-member
        for b in range(1, k + 1):
            eb = node(("eps", b))
            Fd.add(eb)
            F[b - 1].add(eb)              # Fl_b = F(x_b) for an E-member
        if back:
            Fd.add(t)
            kap = node("kappa")
            Fd.add(kap)
            E[names.index(("m", 1))].add(kap)
        E.append(Ed)
        F.append(Fd)
        names.append(("d",))
        nm = len(names)
        mle2 = [[a == b for b in range(nm)] for a in range(nm)]
        for a in range(nm - 1):
            for b in range(nm - 1):
                mle2[a][b] = mle[a][b]
        mle = mle2
    N = len(nodes)
    Em = [sum(1 << x for x in e) for e in E]
    Fm = [sum(1 << x for x in f) for f in F]
    G = Gen(N, Em, Fm, mle, s, t, names=names)
    return G, nodes
