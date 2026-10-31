"""Own construction of the instances of r4-hard.md Theorem T3, written from theory-dc.md Theorem 13(c) and
r4-hard.md section 6.  Clauses: lists of non-zero ints (+i = x_i, -i = not x_i), variables 1..nv."""
import itertools
from zzlib import Inst


def from_sat(nv, clauses):
    """Instance I0 of theory-dc.md Theorem 13(c)."""
    names = []
    idx = {}

    def el(name):
        idx[name] = len(names)
        names.append(name)
        return idx[name]
    m = len(clauses)
    u = el("u")
    d = el("d")
    e0 = el("e0")
    a = [None] + [el("a%d" % i) for i in range(1, nv + 2)]
    T = [None] + [el("T%d" % i) for i in range(1, nv + 1)]
    F = [None] + [el("F%d" % i) for i in range(1, nv + 1)]
    c = [None] + [el("c%d" % j) for j in range(1, m + 2)]
    P = {}
    for j, cl in enumerate(clauses, start=1):
        for k, lit in enumerate(cl, start=1):
            P[j, k] = el("P%d_%d" % (j, k))
    v = el("v")
    n = len(names)
    rel = [(u, x) for x in range(n)] + [(x, v) for x in range(n)]
    rel += [(e0, d), (e0, a[1])]
    for i in range(1, nv + 1):
        for X in (T[i], F[i]):
            rel += [(X, a[i]), (X, a[i + 1])]
    rel.append((c[1], a[nv + 1]))
    for j, cl in enumerate(clauses, start=1):
        for k, lit in enumerate(cl, start=1):
            rel += [(c[j], P[j, k]), (c[j + 1], P[j, k])]
            i = abs(lit)
            rel.append((P[j, k], F[i] if lit > 0 else T[i]))     # conflict relations
    R = [(u, d), (e0, d), (e0, a[1])]
    for i in range(1, nv + 1):
        R += [(T[i], a[i]), (T[i], a[i + 1]), (F[i], a[i]), (F[i], a[i + 1])]
    R.append((c[1], a[nv + 1]))
    for j, cl in enumerate(clauses, start=1):
        for k, lit in enumerate(cl, start=1):
            R += [(c[j], P[j, k]), (c[j + 1], P[j, k])]
    R.append((c[m + 1], v))
    return Inst(n, rel, R, u, v, names)


def add_pendants(I0):
    """Theorem T3: a pendant b_x for every x in Q0 - {u, v}, u < b_x < y for every y in Q0 - {u}, edge b_x x."""
    n0 = I0.n
    names = list(I0.names)
    rel = []
    for x in range(n0):
        for y in range(n0):
            if I0.le(x, y):
                rel.append((x, y))
    R = list(I0.R)
    pend = {}
    for x in range(n0):
        if x in (I0.u, I0.v):
            continue
        b = len(names)
        names.append("b_" + I0.names[x])
        pend[x] = b
    n = len(names)
    for x, b in pend.items():
        rel.append((I0.u, b))
        for y in range(n0):
            if y != I0.u:
                rel.append((b, y))
        R.append((b, x))
    I = Inst(n, rel, R, I0.u, I0.v, names)
    I.pendants = pend
    I.n0 = n0
    return I


def satisfiable(nv, clauses):
    for vals in itertools.product((False, True), repeat=nv):
        if all(any((vals[abs(l) - 1] if l > 0 else not vals[abs(l) - 1]) for l in cl) for cl in clauses):
            return True
    return False
