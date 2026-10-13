"""Shared helpers of agent DC-hardness: 2CH instances (contracted switch model, see twoch.py), conversion to ZZ
(the zigzag problem of theory-dc.md, Theorem 13) and the AC / PC relaxations of dc-algorithm/zz.py (imported
read-only).

2CH instance: (N, E, F, s, t) with E[i], F[i] bit masks of nodes; a mode vector picks E[i] or F[i]; question: are
s and t connected in the hypergraph of the picked sets.  P2: E[i] & E[l] or F[i] & F[l] for i != l.

Conversion to ZZ (switch model SW of theory-dc.md Section 5): bottoms (all equivalent to u) and tops (all equivalent
to v), one element per switch, pairwise incomparable.  A node x lying in some E-set gets a bottom b_x, a node lying
in some F-set gets a top t_x, and a node with both gets the fixed real edge b_x t_x.  Switch i (as a peak) is joined
to the bottoms of E[i], (as a valley) to the tops of F[i].  s is the bottom u (and gets a top t_s with the fixed edge
u t_s if it lies in an F-set); t is the top v (and gets a bottom b_t with the fixed edge b_t v if it lies in an
E-set).  The cut graph of a mode vector contains a u-v path iff s ~ t in the hypergraph, and P2 of 2CH is P2 of ZZ.
"""
import os
import sys
import itertools

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "dc-algorithm"))
sys.setrecursionlimit(100000)
import zz  # noqa: E402  (read-only import)
from twoch import connected, p2_ok  # noqa: E402


def bits_of(m):
    out = []
    while m:
        low = m & -m
        out.append(low.bit_length() - 1)
        m ^= low
    return out


def to_zz(inst):
    """2CH -> ZZ instance (zz.ZZ) and the element map."""
    N, E, F, s, t = inst
    n_sw = len(E)
    inE = 0
    inF = 0
    for i in range(n_sw):
        inE |= E[i]
        inF |= F[i]
    bottom, top = {}, {}
    # element numbering: u = 0, then other bottoms, switches, other tops, v last
    names = ["u"]
    bottom[s] = 0
    for x in range(N):
        if x != s and (inE >> x) & 1:
            bottom[x] = len(names)
            names.append(("b", x))
    if t not in bottom and False:
        pass
    if t != s and ((inE >> t) & 1) and t not in bottom:
        bottom[t] = len(names)
        names.append(("b", t))
    sw0 = len(names)
    for i in range(n_sw):
        names.append(("sw", i))
    for x in range(N):
        if x != t and ((inF >> x) & 1 or x == s and (inF >> s) & 1):
            top[x] = len(names)
            names.append(("t", x))
    top[t] = len(names)
    names.append("v")
    n = len(names)
    u, v = 0, n - 1
    le = [[False] * n for _ in range(n)]
    B = set(bottom.values())
    T = set(top.values())
    for a in range(n):
        for b in range(n):
            if a == b or a in B or b in T:
                le[a][b] = True
    R = []
    for x in range(N):
        if x in bottom and x in top:
            if (bottom[x], top[x]) != (u, v):
                R.append((bottom[x], top[x]))
    for i in range(n_sw):
        for x in bits_of(E[i]):
            R.append((bottom[x], sw0 + i))
        for x in bits_of(F[i]):
            R.append((sw0 + i, top[x]))
    return zz.ZZ(n, None, R, u, v, le=le), names


def exact_2ch(inst):
    """Brute force over mode vectors (fine up to about 20 switches)."""
    N, E, F, s, t = inst
    n = len(E)
    for mask in range(1 << n):
        hyper = [F[i] if (mask >> i) & 1 else E[i] for i in range(n)]
        if connected(N, hyper, s, t):
            return mask
    return None


def all_solutions_2ch(inst):
    N, E, F, s, t = inst
    n = len(E)
    out = []
    for mask in range(1 << n):
        hyper = [F[i] if (mask >> i) & 1 else E[i] for i in range(n)]
        if connected(N, hyper, s, t):
            out.append(mask)
    return out


def relaxed_2ch(inst):
    N, E, F, s, t = inst
    return connected(N, list(E) + list(F), s, t)


def relaxations(inst, do_pc=True):
    """(exact zz answer, AC answer, PC answer) on the ZZ conversion."""
    z, _ = to_zz(inst)
    ex = zz.exact_dfs(z)[0]
    ac = zz.ac_answer(z)
    pc = zz.pc_numpy(z) if (ac and do_pc) else (False if not ac else None)
    return ex, ac, pc, z


class Builder:
    """Incremental construction of 2CH instances with named nodes and switches."""

    def __init__(self):
        self.nodes = {}
        self.E = []
        self.F = []
        self.swname = []

    def node(self, name):
        if name not in self.nodes:
            self.nodes[name] = len(self.nodes)
        return self.nodes[name]

    def switch(self, name):
        self.E.append(0)
        self.F.append(0)
        self.swname.append(name)
        return len(self.E) - 1

    def add(self, i, side, *names):
        for nm in names:
            b = 1 << self.node(nm)
            if side == "E":
                self.E[i] |= b
            else:
                self.F[i] |= b

    def inst(self, s="s", t="t"):
        return (len(self.nodes), list(self.E), list(self.F), self.node(s), self.node(t))

    def p2_missing(self):
        n = len(self.E)
        return [(i, l) for i in range(n) for l in range(i + 1, n)
                if not (self.E[i] & self.E[l]) and not (self.F[i] & self.F[l])]
