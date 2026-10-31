"""Planted paths in the general switch form (r5-core.md Section 4).

A planted instance: switches 0..n-1; switches 0..r-1 are the members of the planted path P (switch a at position a
with member type typ[a], 0 = E, 1 = F); further switches are mates or decoys.  Nodes: s, t and *links*: a link is a
node lying in the given sides (a tuple of (switch, type) pairs, usually two).  Order: pairs (a, b) meaning a <= b,
closed transitively.  P2 is checked on the realised instance (common node of same-type sides for every incomparable
pair; no middle edges are used here).
"""
from gcore import Gen, closure_le


class GPlanted:
    def __init__(self, typ, nextra=0):
        self.typ = list(typ)
        self.r = len(typ)
        self.n = self.r + nextra
        self.links = []          # list of tuples of (switch, type)
        self.rel = []            # (a, b): a <= b
        self.names = [("x", a) for a in range(self.r)] + [("extra", i) for i in range(nextra)]
        self.s_sides = [(0, self.typ[0])]
        self.t_sides = [(self.r - 1, self.typ[self.r - 1])]
        for a in range(self.r - 1):
            self.link((a, self.typ[a]), (a + 1, self.typ[a + 1]))

    def add_switch(self, name):
        self.names.append(name)
        self.n += 1
        return self.n - 1

    def link(self, *sides):
        self.links.append(tuple(sides))

    def le(self, a, b):
        self.rel.append((a, b))

    def mem(self, a):          # member side of position a
        return (a, self.typ[a])

    def par(self, a):          # partner side of position a
        return (a, 1 - self.typ[a])

    def realise(self):
        n = self.n
        E = [0] * n
        F = [0] * n
        nid = 2

        def put(sides, x):
            for (w, ty) in sides:
                if ty == 0:
                    E[w] |= 1 << x
                else:
                    F[w] |= 1 << x
        put(self.s_sides, 0)
        put(self.t_sides, 1)
        for L in self.links:
            put(L, nid)
            nid += 1
        le = [[a == b for b in range(n)] for a in range(n)]
        for a, b in self.rel:
            le[a][b] = True
        le = closure_le(le)
        G = Gen(nid, E, F, le, 0, 1, names=list(self.names))
        P = [2 * a + self.typ[a] for a in range(self.r)]
        return G, P


def p2_ok(G):
    return not G.p2_bad()
