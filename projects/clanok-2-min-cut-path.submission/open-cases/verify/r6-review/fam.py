"""Families of r4-general.md §4, §6 and r5-core.md §2.1, rebuilt from the text of the reports.

yfam(k, contact, dvar): Y_k (contact=False) / Y'_k (contact=True); dvar None (no d), 'plain' (Y^d_k) or 'back'.
xfam(L): X_L.
Switch ids: Y: x_j -> j - 1 (j = 1..2k), m_c -> 2k + c - 1 (c = 1..k), d -> 3k.  X: x_k -> k - 1, m_k -> L + k - 1.
Returns (GInst, info) with info holding names of sides and nodes.
"""
from glib import GInst


class Builder:
    def __init__(self, m):
        self.m = m
        self.E = [0] * m
        self.F = [0] * m
        self.names = {}
        self.N = 0
        self.rel = [[0] * m for _ in range(m)]

    def node(self, name):
        z = self.N
        self.N += 1
        self.names[name] = z
        return z

    def put(self, z, w, ty):
        if ty == 0:
            self.E[w] |= 1 << z
        else:
            self.F[w] |= 1 << z

    def build(self, s, t):
        return GInst(self.N, self.E, self.F, self.rel, self.names[s], self.names[t])


def yfam(k, contact=False, dvar=None):
    m = 3 * k + (1 if dvar else 0)
    bd = Builder(m)
    x = lambda j: j - 1
    mt = lambda c: 2 * k + c - 1
    d = 3 * k
    hty = lambda j: 0 if j <= k else 1          # type of path side h_j
    fty = lambda j: 1 - hty(j)                   # type of flip side Fl_j
    s = bd.node("s")
    t = bd.node("t")
    bd.put(s, x(1), hty(1))
    bd.put(t, x(2 * k), hty(2 * k))
    for j in range(1, 2 * k):
        z = bd.node("y%d" % j)
        bd.put(z, x(j), hty(j))
        bd.put(z, x(j + 1), hty(j + 1))
    for p in range(1, 2 * k + 1):
        for q in range(p + 1, 2 * k + 1):
            if hty(p) != hty(q):
                z = bd.node("z%d_%d" % (p, q))
                bd.put(z, x(p), fty(p))
                bd.put(z, x(q), hty(q))
            else:
                z = bd.node("w%d_%d" % (p, q))
                bd.put(z, x(p), fty(p))
                bd.put(z, x(q), fty(q))
    for c in range(1, k + 1):
        bd.rel[x(c)][mt(c)] = 1           # x_c < m_c
        for b in range(1, k + 1):
            if b != c:
                z = bd.node("f%d_%d" % (c, b))
                bd.put(z, mt(c), 1)
                bd.put(z, x(b), fty(b))
        for q in range(k + 1, 2 * k + 1):
            z = bd.node("e%d_%d" % (c, q))
            bd.put(z, mt(c), 0)
            bd.put(z, x(q), fty(q))
        for c2 in range(c + 1, k + 1):
            z = bd.node("g%d_%d" % (c, c2))
            bd.put(z, mt(c), 0)
            bd.put(z, mt(c2), 0)
        if contact:
            z = bd.node("fc%d" % c)
            bd.put(z, mt(c), 1)
            bd.put(z, x(k + c), hty(k + c))
    if dvar:
        bd.put(s, d, 0)
        for c in range(1, k + 1):
            z = bd.node("gamma%d" % c)
            bd.put(z, d, 0)
            bd.put(z, mt(c), 0)
        for q in range(k + 1, 2 * k + 1):
            z = bd.node("delta%d" % q)
            bd.put(z, d, 0)
            bd.put(z, x(q), fty(q))       # Fl_q = E(x_q)
        for b in range(1, k + 1):
            z = bd.node("eps%d" % b)
            bd.put(z, d, 1)
            bd.put(z, x(b), fty(b))       # Fl_b = F(x_b)
        if dvar == "back":
            bd.put(t, d, 1)
            z = bd.node("kappa")
            bd.put(z, d, 1)
            bd.put(z, mt(1), 0)
    G = bd.build("s", "t")
    info = {"x": x, "m": mt, "d": d if dvar else None, "h": lambda j: 2 * x(j) + hty(j),
            "Fl": lambda j: 2 * x(j) + fty(j), "names": bd.names, "k": k}
    return G, info


def xfam(L):
    m = 2 * L
    bd = Builder(m)
    x = lambda k: k - 1
    mt = lambda k: L + k - 1
    hty = lambda k: 0 if k % 2 == 1 else 1
    fty = lambda k: 1 - hty(k)
    s = bd.node("s")
    t = bd.node("t")
    bd.put(s, x(1), hty(1))
    bd.put(t, x(L), hty(L))
    for k in range(1, L):
        z = bd.node("y%d" % k)
        bd.put(z, x(k), hty(k))
        bd.put(z, x(k + 1), hty(k + 1))
    for p in range(1, L + 1):
        for q in range(p + 1, L + 1):
            if (q - p) % 2 == 1:
                z = bd.node("z%d_%d" % (p, q))
                bd.put(z, x(p), fty(p))
                bd.put(z, x(q), hty(q))
    for k in range(1, L + 1):
        bd.put(t, x(k), fty(k))
    cnode = {}
    for i in range(1, L + 1, 2):
        for k in range(2, L + 1, 2):
            cnode[(i, k)] = bd.node("c%d_%d" % (i, k))
    for k in range(1, L + 1):
        if k % 2 == 0:
            bd.rel[mt(k)][x(k)] = 1        # m_k < x_k
            for nm in ("n%d" % k, "nn%d" % k):
                z = bd.node(nm)
                bd.put(z, mt(k), 0)
                bd.put(z, x(k), hty(k))     # h_k = F(x_k)
            for j in range(2, L + 1, 2):
                if j != k:
                    z = bd.node("n%d_%d" % (k, j))
                    bd.put(z, mt(k), 0)
                    bd.put(z, x(j), fty(j))     # Fl_j = E(x_j)
            for i in range(1, L + 1, 2):
                bd.put(cnode[(i, k)], mt(k), 0)
            bd.put(t, mt(k), 1)
        else:
            bd.rel[x(k)][mt(k)] = 1        # x_k < m_k
            bd.put(t, mt(k), 0)
            for j in range(2, L + 1, 2):
                bd.put(cnode[(k, j)], mt(k), 0)
            for nm in ("e%d" % k, "ee%d" % k):
                z = bd.node(nm)
                bd.put(z, mt(k), 1)
                bd.put(z, x(k), hty(k))     # h_k = E(x_k)
            for j in range(1, L + 1, 2):
                if j != k:
                    z = bd.node("nn%d_%d" % (k, j))
                    bd.put(z, mt(k), 1)
                    bd.put(z, x(j), fty(j))     # Fl_j = F(x_j)
    G = bd.build("s", "t")
    info = {"x": x, "m": mt, "h": lambda k: 2 * x(k) + hty(k), "Fl": lambda k: 2 * x(k) + fty(k),
            "names": bd.names, "L": L}
    return G, info


def zfam(k, contact=True, block=False):
    """Z_k / Z^B_k of r4-general §7.4, rebuilt from the description in r4-general/zfam.py (two routes, cross P2
    nodes, one mate above every E-member of both routes).  Switch ids: route r, index j -> r * 2k + j - 1;
    mate (r, c) -> 4k + r * k + c - 1."""
    m = 4 * k + 2 * k
    bd = Builder(m)
    X = lambda r, j: r * 2 * k + j - 1
    M = lambda r, c: 4 * k + r * k + c - 1
    hty = lambda j: 0 if j <= k else 1
    fty = lambda j: 1 - hty(j)
    s = bd.node("s")
    t = bd.node("t")
    for r in (0, 1):
        bd.put(s, X(r, 1), hty(1))
        bd.put(t, X(r, 2 * k), hty(2 * k))
        for j in range(1, 2 * k):
            z = bd.node("y%d_%d" % (r, j))
            bd.put(z, X(r, j), hty(j))
            bd.put(z, X(r, j + 1), hty(j + 1))
        for p in range(1, 2 * k + 1):
            for q in range(p + 1, 2 * k + 1):
                z = bd.node("zw%d_%d_%d" % (r, p, q))
                bd.put(z, X(r, p), fty(p))
                bd.put(z, X(r, q), hty(q) if hty(p) != hty(q) else fty(q))
    for a in range(1, 2 * k + 1):
        for b in range(1, 2 * k + 1):
            z = bd.node("x%d_%d" % (a, b))
            if hty(a) == hty(b):
                bd.put(z, X(0, a), fty(a))
                bd.put(z, X(1, b), fty(b))
            elif hty(a) == 0:
                bd.put(z, X(0, a), hty(a))
                bd.put(z, X(1, b), fty(b))
            else:
                bd.put(z, X(0, a), fty(a))
                bd.put(z, X(1, b), hty(b))
    mates = [(r, c) for r in (0, 1) for c in range(1, k + 1)]
    for (r, c) in mates:
        bd.rel[X(r, c)][M(r, c)] = 1
        for r2 in (0, 1):
            for b in range(1, k + 1):
                if (r2, b) != (r, c):
                    z = bd.node("f%d_%d_%d_%d" % (r, c, r2, b))
                    bd.put(z, M(r, c), 1)
                    bd.put(z, X(r2, b), fty(b))
            for q in range(k + 1, 2 * k + 1):
                z = bd.node("e%d_%d_%d_%d" % (r, c, r2, q))
                bd.put(z, M(r, c), 0)
                bd.put(z, X(r2, q), fty(q))
        if contact:
            z = bd.node("fc%d_%d" % (r, c))
            bd.put(z, M(r, c), 1)
            bd.put(z, X(1 - r, k + c), hty(k + c))
    for i, a in enumerate(mates):
        for b in mates[i + 1:]:
            z = bd.node("g%d_%d_%d_%d" % (a + b))
            bd.put(z, M(*a), 0)
            bd.put(z, M(*b), 0)
    if block:
        for r in (0, 1):
            for q in range(k + 1, 2 * k + 1):
                bd.rel[X(r, q)][X(1 - r, 2 * k)] = 1
    G = bd.build("s", "t")
    return G, {"X": X, "M": M, "names": bd.names, "k": k}
