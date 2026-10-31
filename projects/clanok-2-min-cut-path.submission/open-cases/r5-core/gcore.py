"""Core library of agent r5-core (round 5): the general switch form of ZZ + P2 and exact routines.

General switch form (r4-general.md Section 5.1): nodes 0..N-1, terminals s, t; switches 0..m-1 with a preorder `le`
(le[a][b] = a <= b); switch w has two node sets E[w] (lower neighbours) and F[w] (upper neighbours), as bit masks.
A mode vector is a down-set D of the preorder (D = switches in F-mode); it picks F[w] for w in D and E[w] otherwise.
Yes-instance iff s and t are connected in the hypergraph of the picked sides.
Side ids: 2w = E-side of w, 2w + 1 = F-side (only non-empty sides exist).
A set of sides is consistent iff it contains no conflict pair {E_w, F_z} with w <= z; a valid path is a walk of
pairwise distinct sides from s to t (consecutive sides meet) whose side set is consistent.

Exact routines written from these definitions (no import of other agents' solvers):
  brute(G)        all order-consistent mode vectors connecting s, t (enumeration of down-sets)
  shortest(G)     BFS over states (side, Up = up-closure of the E-members, Dn = down-closure of the F-members):
                  the length of a shortest valid path and one such path
  all_shortest(G) all shortest valid paths (DFS with a side-graph distance bound)
Conversion from a gcert.Inst (ZZ form) through gsw.GSW of r4-general (read-only import), with the private nodes
of the middle edges kept (G.medge[node] = (y, x), y < x).
"""
import os
import sys
import itertools
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
OC = os.path.dirname(HERE)
for _d in ("r4-general", "dc-hardness", "dc-general", "dc-algorithm", "r4-switch"):
    _p = os.path.join(OC, _d)
    if _p not in sys.path:
        sys.path.append(_p)
sys.setrecursionlimit(100000)


def bits(m):
    out = []
    while m:
        low = m & -m
        out.append(low.bit_length() - 1)
        m ^= low
    return out


def popcount(m):
    return bin(m).count("1")


class Gen:
    """General switch form.  E, F: lists of node masks; le: m x m preorder (lists of bools)."""

    def __init__(self, N, E, F, le, s, t, medge=None, names=None):
        self.N, self.s, self.t = N, s, t
        self.m = len(E)
        self.E, self.F = list(E), list(F)
        self.le = [list(map(bool, r)) for r in le]
        m = self.m
        self.up = [sum(1 << b for b in range(m) if self.le[a][b]) for a in range(m)]
        self.dn = [sum(1 << a for a in range(m) if self.le[a][b]) for b in range(m)]
        self.medge = dict(medge or {})          # private node -> (y, x) with y < x
        self.names = names
        self.sides = [i for w in range(m) for i in (2 * w, 2 * w + 1) if self.mask(i)]
        self.sideset = set(self.sides)
        nb = {}
        for i in self.sides:
            nb[i] = [j for j in self.sides if j != i and self.mask(i) & self.mask(j)]
        self.nb = nb
        self.startsides = [i for i in self.sides if (self.mask(i) >> s) & 1]
        self.goalsides = set(i for i in self.sides if (self.mask(i) >> t) & 1)
        self._dist_t = None

    def mask(self, i):
        return self.F[i >> 1] if i & 1 else self.E[i >> 1]

    def comparable(self, a, b):
        return self.le[a][b] or self.le[b][a]

    # ---------------------------------------------------------------------------------------------------------
    def dist_to_t(self):
        """Side-graph distance (number of further sides) from each side to a side containing t, ignoring validity."""
        if self._dist_t is None:
            d = {i: 0 for i in self.goalsides}
            dq = deque(self.goalsides)
            while dq:
                x = dq.popleft()
                for y in self.nb[x]:
                    if y not in d:
                        d[y] = d[x] + 1
                        dq.append(y)
            self._dist_t = d
        return self._dist_t

    def step_ok(self, i, Up, Dn):
        """Can side i be added to a consistent set with closures Up, Dn?  Returns new (Up, Dn) or None."""
        w = i >> 1
        if i & 1:
            if (Up >> w) & 1:
                return None
            return Up, Dn | self.dn[w]
        if (Dn >> w) & 1:
            return None
        return Up | self.up[w], Dn

    def shortest(self):
        """(length, path) of a shortest valid path, or (None, None)."""
        if self.s == self.t:
            return 0, []
        par = {}
        dq = deque()
        for i in self.startsides:
            r = self.step_ok(i, 0, 0)
            if r is None:
                continue
            st = (i,) + r
            if st not in par:
                par[st] = None
                dq.append(st)
        while dq:
            st = dq.popleft()
            i, Up, Dn = st
            if i in self.goalsides:
                path = [st]
                while par[path[-1]] is not None:
                    path.append(par[path[-1]])
                return len(path), [p[0] for p in path[::-1]]
            for j in self.nb[i]:
                r = self.step_ok(j, Up, Dn)
                if r is None:
                    continue
                st2 = (j,) + r
                if st2 not in par:
                    par[st2] = st
                    dq.append(st2)
        return None, None

    def all_shortest(self, limit=None, length=None):
        """All shortest valid paths (lists of side ids).  `limit` caps the number returned."""
        if length is None:
            length, _ = self.shortest()
        if length is None:
            return []
        dt = self.dist_to_t()
        out = []

        def rec(path, Up, Dn, used):
            if limit is not None and len(out) >= limit:
                return
            i = path[-1]
            if len(path) == length:
                if i in self.goalsides:
                    out.append(list(path))
                return
            rem = length - len(path)
            for j in self.nb[i]:
                if (j >> 1) in used:
                    continue
                if dt.get(j, 10 ** 9) > rem - 1:
                    continue
                r = self.step_ok(j, Up, Dn)
                if r is None:
                    continue
                path.append(j)
                used.add(j >> 1)
                rec(path, r[0], r[1], used)
                used.discard(j >> 1)
                path.pop()
        for i in self.startsides:
            if dt.get(i, 10 ** 9) > length - 1:
                continue
            r = self.step_ok(i, 0, 0)
            if r is None:
                continue
            rec([i], r[0], r[1], {i >> 1})
        return out

    def is_valid_walk(self, walk):
        if not walk:
            return self.s == self.t
        if not (self.mask(walk[0]) >> self.s) & 1 or not (self.mask(walk[-1]) >> self.t) & 1:
            return False
        for a, b in zip(walk, walk[1:]):
            if a != b and not (self.mask(a) & self.mask(b)):
                return False
        Up = Dn = 0
        for i in walk:
            r = self.step_ok(i, Up, Dn)
            if r is None:
                return False
            Up, Dn = r
        return True

    def downsets(self):
        """All down-sets of the switch preorder (bit masks over switches)."""
        m = self.m
        out = []

        def rec(i, D, X):          # D: in, X: out (excluded); i: next switch to decide
            while i < m and ((D >> i) & 1 or (X >> i) & 1):
                i += 1
            if i == m:
                out.append(D)
                return
            # put i in D: its down-closure must avoid X
            if not (self.dn[i] & X):
                rec(i + 1, D | self.dn[i], X)
            # put i out: its up-closure must avoid D
            if not (self.up[i] & D):
                rec(i + 1, D, X | self.up[i])
        rec(0, 0, 0)
        return out

    def connects(self, D):
        hyper = [self.F[w] if (D >> w) & 1 else self.E[w] for w in range(self.m)]
        comp = 1 << self.s
        ch = True
        while ch:
            ch = False
            for h in hyper:
                if h & comp and h & ~comp:
                    comp |= h
                    ch = True
        return bool((comp >> self.t) & 1)

    def brute(self):
        return [D for D in self.downsets() if self.connects(D)]

    # ---------------------------------------------------------------------------------------------------------
    def p2_bad(self):
        """Incomparable switch pairs without a common same-type node and without a middle witness (through the
        private nodes of middle edges)."""
        m = self.m
        lowF = [set() for _ in range(m)]     # y with an edge y-x (y < x): lower middle neighbours of x
        upE = [set() for _ in range(m)]
        for z, (y, x) in self.medge.items():
            lowF[x].add(y)
            upE[y].add(x)
        bad = []
        for a in range(m):
            for b in range(a + 1, m):
                if self.comparable(a, b):
                    continue
                if self.E[a] & self.E[b] or self.F[a] & self.F[b]:
                    continue
                if lowF[a] & lowF[b] or upE[a] & upE[b]:
                    continue
                bad.append((a, b))
        return bad


def from_inst(I):
    """gcert.Inst -> Gen (through r4-general's GSW conversion; private nodes of middle edges recorded)."""
    from gsw import GSW
    G0 = GSW(I)
    medge = {z: (G0.idx[a], G0.idx[b]) for z, (a, b) in G0.private.items()}     # element ids -> switch ids
    return Gen(G0.N, G0.E, G0.F, G0.le, G0.s, G0.t, medge=medge), G0


def to_inst(G):
    """Gen -> gcert.Inst (nodes become bottom-top pairs; middle edges kept as real middle-middle edges)."""
    import gcert
    m, N = G.m, G.N
    priv = G.medge
    inE, inF = set(), set()
    for w in range(m):
        for x in bits(G.E[w]):
            if x not in priv:
                inE.add(x)
        for x in bits(G.F[w]):
            if x not in priv:
                inF.add(x)
    inE.add(G.s)
    inF.add(G.t)
    names = []
    bot = {G.s: 0}
    names.append(("b", G.s))
    for x in range(N):
        if x in inE and x != G.s:
            bot[x] = len(names)
            names.append(("b", x))
    mem0 = len(names)
    for w in range(m):
        names.append(("m", w))
    top = {}
    for x in range(N):
        if x in inF and x != G.t:
            top[x] = len(names)
            names.append(("t", x))
    extra = []
    if G.s == G.t:
        # u and v in one node: realise it by a fresh bottom-top pair u - tau - beta - v (ZZ forbids the edge u v)
        extra = [len(names), len(names) + 1]          # tau (top), beta (bottom)
        names.append(("tau",))
        names.append(("beta",))
    top[G.t] = len(names)
    names.append(("t", G.t))
    n = len(names)
    Bs, Ts = set(bot.values()), set(top.values())
    if extra:
        Ts.add(extra[0])
        Bs.add(extra[1])
    le = [[a == b or a in Bs or b in Ts for b in range(n)] for a in range(n)]
    for a in range(m):
        for b in range(m):
            if G.le[a][b]:
                le[mem0 + a][mem0 + b] = True
    R = set()
    for x in range(N):
        if x in bot and x in top:
            R.add((bot[x], top[x]))
    for w in range(m):
        for x in bits(G.E[w]):
            if x in priv:
                continue
            R.add((bot[x], mem0 + w))
        for x in bits(G.F[w]):
            if x in priv:
                continue
            R.add((mem0 + w, top[x]))
    for z, (y, x) in priv.items():
        R.add((mem0 + y, mem0 + x))
    R.discard((0, n - 1))
    if extra:
        tau, beta = extra
        R |= {(0, tau), (beta, tau), (beta, n - 1)}
    return gcert.Inst(n, le, sorted(R), 0, n - 1), names


def closure_le(le):
    n = len(le)
    le = [list(r) for r in le]
    for i in range(n):
        le[i][i] = True
    for k in range(n):
        for i in range(n):
            if le[i][k]:
                rk = le[k]
                ri = le[i]
                for j in range(n):
                    if rk[j]:
                        ri[j] = True
    return le


# -------------------------------------------------------------------------------------------------------------
# structure of a valid path
# -------------------------------------------------------------------------------------------------------------

class PathInfo:
    """Data of a valid path P (list of side ids): members, types, closures, allowed and conflict sides."""

    def __init__(self, G, P):
        self.G, self.P = G, P
        self.r = len(P)
        self.sw = [i >> 1 for i in P]
        self.ty = [i & 1 for i in P]               # 0 = E-member, 1 = F-member
        self.pos = {i: a for a, i in enumerate(P)}
        WE = sum(1 << (i >> 1) for i in P if not i & 1)
        WF = sum(1 << (i >> 1) for i in P if i & 1)
        Up = 0
        for w in bits(WE):
            Up |= G.up[w]
        Dn = 0
        for w in bits(WF):
            Dn |= G.dn[w]
        self.WE, self.WF, self.Up, self.Dn = WE, WF, Up, Dn
        assert not (Up & Dn), "invalid path"
        # conflict sides (forbidden for every walk through P): F_z, z in Up; E_z, z in Dn
        self.conflict = set(i for i in G.sides if (i & 1 and (Up >> (i >> 1)) & 1) or
                            (not i & 1 and (Dn >> (i >> 1)) & 1))
        self.allowed = set(G.sides) - self.conflict

    def contacts(self, i):
        """Positions of members meeting side i (other than i itself)."""
        mk = self.G.mask(i)
        return [a for a, j in enumerate(self.P) if j != i and self.G.mask(j) & mk]

    def window(self, i):
        c = self.contacts(i)
        return (max(c) - min(c)) if c else -1

    def minimal_E(self):
        """E-member positions a such that no other E-member is <= w_a."""
        G = self.G
        out = []
        for a in range(self.r):
            if self.ty[a]:
                continue
            w = self.sw[a]
            if any(not self.ty[b] and b != a and G.le[self.sw[b]][w] for b in range(self.r)):
                continue
            out.append(a)
        return out

    def maximal_F(self):
        G = self.G
        out = []
        for a in range(self.r):
            if not self.ty[a]:
                continue
            w = self.sw[a]
            if any(self.ty[b] and b != a and G.le[w][self.sw[b]] for b in range(self.r)):
                continue
            out.append(a)
        return out
