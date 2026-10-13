"""Two-choice hypergraphs with ties (classes of switches forced into one mode) and their ZZ form.

Instance: (N, E, F, cls, s, t): E[i], F[i] node bit masks of switch i, cls[i] its class.  A mode vector picks one
mode per CLASS; mode 0 picks the E-sides of all members, mode 1 their F-sides.  Question: are s, t connected.
ZZ form (theory-dc.md Theorem 13): bottoms (nodes in an E-side, and s) are equivalent to u, tops (nodes in an F-side,
and t) to v, members of one class are equivalent, different classes are incomparable; real edges bottom-switch
(E-side), switch-top (F-side), and bottom-top for a node with both (the fixed edge of the node).
E-mode = switch on the v-side (peak, joins its bottoms); F-mode = switch on the u-side (valley, joins its tops)."""
import itertools
import zz


def to_zz(inst):
    N, E, F, cls, s, t = inst
    k = len(E)
    inE = [any((m >> x) & 1 for m in E) or x == s for x in range(N)]
    inF = [any((m >> x) & 1 for m in F) or x == t for x in range(N)]
    border = [s] + [x for x in range(N) if x != s and inE[x]]
    torder = [t] + [x for x in range(N) if x != t and inF[x]]
    nb, nt = len(border), len(torder)
    bi = {x: i for i, x in enumerate(border)}
    ti = {x: nb + k + i for i, x in enumerate(torder)}
    n = nb + k + nt
    le = [[False] * n for _ in range(n)]
    for x in range(n):
        for y in range(n):
            if x < nb or y >= nb + k or x == y:
                le[x][y] = True
            elif nb <= x < nb + k and nb <= y < nb + k and cls[x - nb] == cls[y - nb]:
                le[x][y] = True
    R = [(bi[x], ti[x]) for x in range(N) if inE[x] and inF[x]]
    for i in range(k):
        R += [(bi[x], nb + i) for x in range(N) if (E[i] >> x) & 1]
        R += [(nb + i, ti[x]) for x in range(N) if (F[i] >> x) & 1]
    return zz.ZZ(n, None, R, 0, nb + k, le=le)


def connected(inst, cmode):
    N, E, F, cls, s, t = inst
    comp = 1 << s
    sides = [E[i] if cmode[cls[i]] == 0 else F[i] for i in range(len(E))]
    changed = True
    while changed:
        changed = False
        for X in sides:
            if X & comp and X & ~comp:
                comp |= X
                changed = True
    return bool((comp >> t) & 1)


def brute(inst):
    cls = inst[3]
    C = sorted(set(cls))
    idx = {c: i for i, c in enumerate(C)}
    for modes in itertools.product((0, 1), repeat=len(C)):
        cm = {c: modes[idx[c]] for c in C}
        if connected(inst, cm):
            return cm
    return None


class Builder:
    def __init__(self):
        self.nodes = {}
        self.E, self.F, self.cls, self.labels = [], [], [], []

    def node(self, name):
        if name not in self.nodes:
            self.nodes[name] = len(self.nodes)
        return self.nodes[name]

    def switch(self, label, c, Eset, Fset):
        self.E.append(sum(1 << self.node(x) for x in Eset))
        self.F.append(sum(1 << self.node(x) for x in Fset))
        self.cls.append(c)
        self.labels.append(label)
        return len(self.E) - 1

    def inst(self, s, t):
        return (len(self.nodes), list(self.E), list(self.F), list(self.cls), self.node(s), self.node(t))
