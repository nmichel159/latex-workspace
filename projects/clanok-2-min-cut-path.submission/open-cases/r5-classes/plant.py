"""Link-based planted paths with classes (agent r5-classes, third run).

A planted instance consists of switches 0..n-1 with a class each; switches 0..r-1 are the *members* of the planted
path P (switch a sits at position a with member type typ[a]); switches r..n-1 are *mates* or other switches.
Every node is either s, t, or the private node of one *link*: a link (u, tu, v, tv) is a node lying in side tu of
switch u and side tv of switch v (type 0 = E, 1 = F).  Structural links: y-links between consecutive members
(X_a meets X_{a+1}).  Everything else is added by generators and hill climbing.

P2 for switches u, v of different classes holds iff some link joins E_u, E_v or F_u, F_v (same-type link).
realise() builds a ccore.Inst; the planted path is the tuple of member sides.
"""
import random
import ccore as C


class Planted:
    def __init__(self, typ, cls, extra_cls=()):
        self.r = len(typ)
        self.typ = list(typ)
        self.cls = list(cls) + list(extra_cls)
        self.n = len(self.cls)
        self.links = set()          # frozenset-free canonical tuples (u, tu, v, tv) with (u, tu) < (v, tv)
        for a in range(self.r - 1):
            self.add_link(a, self.typ[a], a + 1, self.typ[a + 1])
        self.struct = set(self.links)
        self.mtyp = {}              # mate switch -> intended type (type of its class on P)

    def copy(self):
        o = Planted.__new__(Planted)
        o.r, o.typ, o.cls, o.n = self.r, list(self.typ), list(self.cls), self.n
        o.links, o.struct, o.mtyp = set(self.links), set(self.struct), dict(self.mtyp)
        return o

    @staticmethod
    def canon(u, tu, v, tv):
        a, b = (u, tu), (v, tv)
        if a > b:
            a, b = b, a
        return (a[0], a[1], b[0], b[1])

    def add_link(self, u, tu, v, tv):
        if u == v:
            return False
        L = self.canon(u, tu, v, tv)
        if L in self.links:
            return False
        self.links.add(L)
        return True

    def remove_link(self, L):
        if L in self.struct or L not in self.links:
            return False
        self.links.discard(L)
        return True

    def add_switch(self, cl, mtyp=None):
        self.cls.append(cl)
        self.n += 1
        if mtyp is not None:
            self.mtyp[self.n - 1] = mtyp
        return self.n - 1

    # ----------------------------------------------------------------------------------------------- P2
    def p2_pairs_missing(self):
        have = set()
        for (u, tu, v, tv) in self.links:
            if tu == tv:
                have.add((min(u, v), max(u, v)))
        out = []
        for u in range(self.n):
            for v in range(u + 1, self.n):
                if self.cls[u] != self.cls[v] and (u, v) not in have:
                    out.append((u, v))
        return out

    def p2_count(self, u, v):
        """number of same-type links between switches u and v"""
        c = 0
        for (a, ta, b, tb) in self.links:
            if ta == tb and {a, b} == {u, v}:
                c += 1
        return c

    # --------------------------------------------------------------------------------------- realisation
    def realise(self):
        sides = [[set(), set()] for _ in range(self.n)]
        N = 0
        s, t = 0, 1
        N = 2
        sides[0][self.typ[0]].add(s)
        sides[self.r - 1][self.typ[self.r - 1]].add(t)
        for (u, tu, v, tv) in sorted(self.links):
            sides[u][tu].add(N)
            sides[v][tv].add(N)
            N += 1
        sw = [(C.orbits(E), C.orbits(F)) for E, F in sides]
        I = C.Inst(N, s, t, sw, self.cls)
        P = tuple(2 * a + self.typ[a] for a in range(self.r))
        return I, P

    def shortest_ok(self, I=None, P=None):
        if I is None:
            I, P = self.realise()
        L, paths = C.shortest_valid_paths(I, limit=1, maxlen=self.r)
        return L == self.r


def contacts(I, P):
    """for every position a: the set of positions c != a with X'_a meeting X_c (X'_a = other side of the switch)."""
    r = len(P)
    out = []
    for a in range(r):
        x = P[a]
        other = x ^ 1
        m = I.mask.get(other, 0)
        out.append({c for c in range(r) if c != a and m & I.mask[P[c]]})
    return out


def base_word(W, cls=None, forward=True):
    """planted path for the type word W (E/F) with classes cls (default: all distinct); P2 for opposite-type pairs
    of different classes by forward contacts (X'_a meets X_b, a < b) when forward, else backward; same-type pairs
    of different classes at distance >= 2 by partner-partner links."""
    typ = [0 if ch == "E" else 1 for ch in W]
    r = len(typ)
    if cls is None:
        cls = list(range(r))
    pl = Planted(typ, cls)
    for a in range(r):
        for b in range(a + 1, r):
            if cls[a] == cls[b]:
                continue
            if typ[a] == typ[b]:
                if b >= a + 2:
                    pl.add_link(a, 1 - typ[a], b, 1 - typ[b])
            else:
                if forward:
                    pl.add_link(a, 1 - typ[a], b, typ[b])
                else:
                    pl.add_link(b, 1 - typ[b], a, typ[a])
    return pl
