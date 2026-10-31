"""Own implementation (reviewer rv-core-65) of the general switch form of ZZ + P2, written from the definitions of
r4-general.md Section 5.1 and r5-core.md Section 6.1.  No code of other agents is imported here.

Instance: nodes 0..N-1, terminals s, t; switches 0..m-1 with a preorder le (le[a][b] means a <= b); switch w has two
node sets E[w], F[w] (bit masks).  A middle edge (z, v), z < v strictly, has one private node that lies in F[z] and
E[v] and in no other side.  A mode vector is a down-set D (switches in F-mode); D picks F[w] for w in D and E[w]
otherwise; yes-instance iff s and t are connected in the hypergraph of the picked sides.
P2 (switch form): for incomparable x, y: a node of E[x] & E[y], or of F[x] & F[y], or a lower middle witness z
(edges (z, x), (z, y)), or an upper middle witness z (edges (x, z), (y, z)).
Sides are pairs (w, typ), typ 0 = E, 1 = F.  A conflict pair is {E_w, F_z} with w <= z.  A valid path is a sequence
of distinct sides X_1..X_r, s in X_1, t in X_r, consecutive sides meet, no conflict pair.
"""
import itertools
import random
from collections import deque


def bits(x):
    out = []
    while x:
        low = x & -x
        out.append(low.bit_length() - 1)
        x ^= low
    return out


def popcount(x):
    return bin(x).count("1")


class Inst:
    def __init__(self, N, s, t, le, E, F, medges, name=""):
        self.N, self.s, self.t = N, s, t
        self.m = len(E)
        self.le = [[bool(v) for v in row] for row in le]
        self.E, self.F = list(E), list(F)
        self.medges = dict(medges)            # (z, v) -> private node
        self.name = name
        m = self.m
        self.up = [sum(1 << b for b in range(m) if self.le[a][b]) for a in range(m)]
        self.dn = [sum(1 << a for a in range(m) if self.le[a][b]) for b in range(m)]
        self.cls = [self.up[a] & self.dn[a] for a in range(m)]
        self.full = (1 << m) - 1
        self.lmn = [set() for _ in range(m)]
        self.umn = [set() for _ in range(m)]
        self.private = 0
        for (z, v), node in self.medges.items():
            self.lmn[v].add(z)
            self.umn[z].add(v)
            self.private |= 1 << node
        self.enon = sum(1 << w for w in range(m) if self.E[w])
        self.fnon = sum(1 << w for w in range(m) if self.F[w])
        self._downsets = None

    # ---- order ------------------------------------------------------------------------------------------------
    def lt(self, a, b):
        return self.le[a][b] and not self.le[b][a]

    def comparable(self, a, b):
        return self.le[a][b] or self.le[b][a]

    def upc(self, S):
        r = 0
        for w in bits(S):
            r |= self.up[w]
        return r

    def dnc(self, S):
        r = 0
        for w in bits(S):
            r |= self.dn[w]
        return r

    def strict_down(self, x):
        return self.dn[x] & ~self.cls[x]

    def strict_up(self, y):
        return self.up[y] & ~self.cls[y]

    def is_downset(self, D):
        for w in bits(D):
            if self.dn[w] & ~D:
                return False
        return True

    def side_mask(self, side):
        w, typ = side
        return self.F[w] if typ else self.E[w]

    def conflict(self, s1, s2):
        (w1, t1), (w2, t2) = s1, s2
        if t1 == 0 and t2 == 1:
            return self.le[w1][w2]
        if t1 == 1 and t2 == 0:
            return self.le[w2][w1]
        return False

    # ---- validation and P2 -------------------------------------------------------------------------------------
    def validate(self):
        m = self.m
        for a in range(m):
            assert self.le[a][a], "not reflexive"
            for b in range(m):
                if self.le[a][b]:
                    for c in range(m):
                        if self.le[b][c]:
                            assert self.le[a][c], "not transitive"
        for (z, v), node in self.medges.items():
            assert self.lt(z, v), "middle edge not strict"
            assert node not in (self.s, self.t)
            for w in range(m):
                inE = (self.E[w] >> node) & 1
                inF = (self.F[w] >> node) & 1
                assert inE == (w == v), "private node in a wrong E-side"
                assert inF == (w == z), "private node in a wrong F-side"
        return True

    def p2_witness(self, x, y):
        if self.E[x] & self.E[y]:
            return "E"
        if self.F[x] & self.F[y]:
            return "F"
        for z in self.lmn[x] & self.lmn[y]:
            return "low"
        for z in self.umn[x] & self.umn[y]:
            return "up"
        return None

    def p2(self):
        m = self.m
        for x in range(m):
            for y in range(x + 1, m):
                if not self.comparable(x, y) and self.p2_witness(x, y) is None:
                    return False
        return True

    # ---- down-sets, connectivity, brute force -----------------------------------------------------------------------
    def downsets(self):
        """All down-sets of the preorder (as switch masks)."""
        if self._downsets is not None:
            return self._downsets
        m = self.m
        # tie classes and a linear extension of the quotient
        classes = []
        seen = 0
        for w in range(m):
            if not (seen >> w) & 1:
                classes.append(self.cls[w])
                seen |= self.cls[w]
        # sort classes by size of down-closure (a linear extension)
        classes.sort(key=lambda c: popcount(self.dn[bits(c)[0]]))
        below = [self.dn[bits(c)[0]] & ~c for c in classes]
        out = []

        def rec(i, D):
            if i == len(classes):
                out.append(D)
                return
            rec(i + 1, D)
            if below[i] & ~D == 0:
                rec(i + 1, D | classes[i])
        rec(0, 0)
        self._downsets = out
        return out

    def picked_masks(self, D):
        return [self.F[w] if (D >> w) & 1 else self.E[w] for w in range(self.m)]

    def connects(self, D):
        if self.s == self.t:
            return True
        masks = [x for x in self.picked_masks(D) if x]
        reach = 1 << self.s
        changed = True
        while changed:
            changed = False
            rest = []
            for x in masks:
                if x & reach:
                    if x & ~reach:
                        reach |= x
                    changed = True
                else:
                    rest.append(x)
            masks = rest
            if (reach >> self.t) & 1:
                return True
        return bool((reach >> self.t) & 1)

    def solutions(self):
        return [D for D in self.downsets() if self.connects(D)]

    def yes(self):
        for D in self.downsets():
            if self.connects(D):
                return True
        return False

    # ---- shortest valid paths -------------------------------------------------------------------------------------
    def picked_sides(self, D):
        out = []
        for w in range(self.m):
            typ = 1 if (D >> w) & 1 else 0
            if self.side_mask((w, typ)):
                out.append((w, typ))
        return out

    def _bfs_paths(self, D, want_len=None, cap=None):
        """Shortest s-t paths of sides in the picked side graph of D: (length, list of paths)."""
        sides = self.picked_sides(D)
        msk = {sd: self.side_mask(sd) for sd in sides}
        dist = {}
        dq = deque()
        for sd in sides:
            if (msk[sd] >> self.s) & 1:
                dist[sd] = 1
                dq.append(sd)
        while dq:
            a = dq.popleft()
            for b in sides:
                if b not in dist and msk[a] & msk[b]:
                    dist[b] = dist[a] + 1
                    dq.append(b)
        ends = [sd for sd in sides if sd in dist and (msk[sd] >> self.t) & 1]
        if not ends:
            return None, []
        L = min(dist[sd] for sd in ends)
        if want_len is not None and L != want_len:
            return L, []
        paths = []

        def back(sd, suffix):
            if cap is not None and len(paths) >= cap:
                return
            if dist[sd] == 1:
                paths.append([sd] + suffix)
                return
            for a in sides:
                if dist.get(a) == dist[sd] - 1 and msk[a] & msk[sd]:
                    back(a, [sd] + suffix)
        for sd in ends:
            if dist[sd] == L:
                back(sd, [])
        return L, paths

    def shortest_length(self):
        if self.s == self.t:
            return 0
        best = None
        for D in self.downsets():
            if not self.connects(D):
                continue
            L, _ = self._bfs_paths(D, cap=0)
            if L is not None and (best is None or L < best):
                best = L
        return best

    def all_shortest_paths(self, cap=None):
        """All shortest valid paths (tuples of sides); every valid path of the least length r is a shortest s-t path
        of the picked side graph of D = down(W_F), and conversely."""
        r = self.shortest_length()
        if r is None or r == 0:
            return r, []
        out = set()
        for D in self.downsets():
            if not self.connects(D):
                continue
            L, paths = self._bfs_paths(D, want_len=r, cap=None)
            if L != r:
                continue
            for p in paths:
                out.add(tuple(p))
                if cap is not None and len(out) >= cap:
                    return r, sorted(out)
        return r, sorted(out)

    # ---- second method for larger instances: BFS over states (side, Up, Dn), then DFS with a distance bound ----------
    def _sides(self):
        return [(w, typ) for w in range(self.m) for typ in (0, 1) if self.side_mask((w, typ))]

    def _add(self, side, Up, Dn):
        w, typ = side
        if typ:
            if (Up >> w) & 1:
                return None
            return Up, Dn | self.dn[w]
        if (Dn >> w) & 1:
            return None
        return Up | self.up[w], Dn

    def shortest_length_states(self):
        if self.s == self.t:
            return 0
        sides = self._sides()
        msk = {sd: self.side_mask(sd) for sd in sides}
        nb = {a: [b for b in sides if b != a and msk[a] & msk[b]] for a in sides}
        seen = set()
        frontier = []
        for sd in sides:
            if (msk[sd] >> self.s) & 1:
                r = self._add(sd, 0, 0)
                if r is not None:
                    st = (sd,) + r
                    if st not in seen:
                        seen.add(st)
                        frontier.append(st)
        L = 1
        while frontier:
            for st in frontier:
                if (msk[st[0]] >> self.t) & 1:
                    return L
            nxt = []
            for sd, Up, Dn in frontier:
                for b in nb[sd]:
                    r = self._add(b, Up, Dn)
                    if r is None:
                        continue
                    st = (b,) + r
                    if st not in seen:
                        seen.add(st)
                        nxt.append(st)
            frontier = nxt
            L += 1
        return None

    def all_shortest_paths_dfs(self, cap=None):
        r = self.shortest_length_states()
        if r is None or r == 0:
            return r, []
        sides = self._sides()
        msk = {sd: self.side_mask(sd) for sd in sides}
        nb = {a: [b for b in sides if b != a and msk[a] & msk[b]] for a in sides}
        dist = {sd: 1 for sd in sides if (msk[sd] >> self.t) & 1}
        dq = deque(dist)
        while dq:
            a = dq.popleft()
            for b in nb[a]:
                if b not in dist:
                    dist[b] = dist[a] + 1
                    dq.append(b)
        out = []

        def rec(path, Up, Dn):
            if cap is not None and len(out) >= cap:
                return
            last = path[-1]
            if len(path) == r:
                if (msk[last] >> self.t) & 1:
                    out.append(tuple(path))
                return
            for b in nb[last]:
                if b in path or len(path) + dist.get(b, 10 ** 9) > r:
                    continue
                res = self._add(b, Up, Dn)
                if res is None:
                    continue
                path.append(b)
                rec(path, res[0], res[1])
                path.pop()
        for sd in sides:
            if (msk[sd] >> self.s) & 1 and dist.get(sd, 10 ** 9) <= r:
                res = self._add(sd, 0, 0)
                if res is not None:
                    rec([sd], res[0], res[1])
        return r, sorted(set(out))

    def shortest_paths(self, cap=None):
        """All shortest valid paths: down-set method for m <= 13, state BFS + DFS above (the two agree, see
        test_methods.py)."""
        if self.m <= 13:
            return self.all_shortest_paths(cap=cap)
        return self.all_shortest_paths_dfs(cap=cap)

    def is_valid_path(self, P):
        if not P:
            return self.s == self.t
        if not (self.side_mask(P[0]) >> self.s) & 1:
            return False
        if not (self.side_mask(P[-1]) >> self.t) & 1:
            return False
        if len(set(P)) != len(P):
            return False
        for i in range(len(P) - 1):
            if not self.side_mask(P[i]) & self.side_mask(P[i + 1]):
                return False
        for i in range(len(P)):
            for j in range(len(P)):
                if i != j and self.conflict(P[i], P[j]):
                    return False
        return True

    def to_json(self):
        return dict(N=self.N, s=self.s, t=self.t, le=[[int(v) for v in r] for r in self.le], E=self.E, F=self.F,
                    medges=[[z, v, n] for (z, v), n in self.medges.items()], name=self.name)

    @staticmethod
    def from_json(d):
        return Inst(d["N"], d["s"], d["t"], d["le"], d["E"], d["F"],
                    {(z, v): n for z, v, n in d["medges"]}, d.get("name", ""))


# ---- conversion from ZZ form (n elements, u, v, le, R) ------------------------------------------------------------
def from_zz(n, u, v, le, R, name=""):
    """General switch form of a ZZ instance, from the definitions of r4-general.md Section 5.1."""
    le = [[bool(x) for x in row] for row in le]
    Bc = [x for x in range(n) if le[x][u] and le[u][x]]
    Tc = [x for x in range(n) if le[x][v] and le[v][x]]
    Bs, Ts = set(Bc), set(Tc)
    mid = [x for x in range(n) if x not in Bs and x not in Ts]
    idx = {x: i for i, x in enumerate(mid)}
    # components of the R-edges between B and T
    par = {x: x for x in Bc + Tc}

    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a
    for a, b in R:
        if (a in Bs and b in Ts) or (a in Ts and b in Bs):
            ra, rb = find(a), find(b)
            if ra != rb:
                par[ra] = rb
    roots = sorted(set(find(x) for x in Bc + Tc))
    node = {r: i for i, r in enumerate(roots)}
    N = len(roots)
    m = len(mid)
    E = [0] * m
    F = [0] * m
    medges = {}
    for a, b in R:
        if le[b][a] and not le[a][b]:
            a, b = b, a
        # now a < b
        if a in idx and b in idx:
            medges[(idx[a], idx[b])] = N
            F[idx[a]] |= 1 << N
            E[idx[b]] |= 1 << N
            N += 1
        elif a in idx and b in Ts:
            F[idx[a]] |= 1 << node[find(b)]
        elif b in idx and a in Bs:
            E[idx[b]] |= 1 << node[find(a)]
        # edges inside B, inside T, or B-T: no side
    lem = [[le[x][y] for y in mid] for x in mid]
    return Inst(N, node[find(u)], node[find(v)], lem, E, F, medges, name)


# ---- random generators -------------------------------------------------------------------------------------------
def closure(le):
    m = len(le)
    for k in range(m):
        for i in range(m):
            if le[i][k]:
                for j in range(m):
                    if le[k][j]:
                        le[i][j] = True
    return le


def random_preorder(rng, m, p_order, p_tie):
    perm = list(range(m))
    rng.shuffle(perm)
    rank = {w: i for i, w in enumerate(perm)}
    le = [[i == j for j in range(m)] for i in range(m)]
    for a in range(m):
        for b in range(m):
            if rank[a] < rank[b] and rng.random() < p_order:
                le[a][b] = True
    if p_tie > 0:
        for a in range(m):
            for b in range(a + 1, m):
                if rng.random() < p_tie / m:
                    le[a][b] = le[b][a] = True
    return closure(le)


def random_inst(rng, m, n_nodes=None, p_order=0.3, p_tie=0.0, p_side=0.25, p_med=0.2, repair=None, name=""):
    """Random general switch form instance with P2 enforced by adding witnesses."""
    le = random_preorder(rng, m, p_order, p_tie)
    if n_nodes is None:
        n_nodes = rng.randint(m // 2 + 2, m + 3)
    N = n_nodes
    s, t = 0, 1
    E = [0] * m
    F = [0] * m
    for w in range(m):
        for nd in range(N):
            if rng.random() < p_side:
                E[w] |= 1 << nd
            if rng.random() < p_side:
                F[w] |= 1 << nd
    medges = {}

    def lt(a, b):
        return le[a][b] and not le[b][a]

    def add_med(z, v):
        nonlocal N
        if (z, v) in medges:
            return
        medges[(z, v)] = N
        F[z] |= 1 << N
        E[v] |= 1 << N
        N += 1
    for z in range(m):
        for v in range(m):
            if lt(z, v) and rng.random() < p_med:
                add_med(z, v)
    regular = [nd for nd in range(n_nodes)]
    modes = repair or ["freshE", "freshF", "oldE", "oldF", "low", "up"]
    for x in range(m):
        for y in range(x + 1, m):
            if le[x][y] or le[y][x]:
                continue

            def ok():
                if E[x] & E[y] or F[x] & F[y]:
                    return True
                for (z, v) in medges:
                    if v == x and (z, y) in medges:
                        return True
                    if z == x and (y, v) in medges:
                        return True
                return False
            if ok():
                continue
            tries = 0
            while not ok() and tries < 50:
                tries += 1
                mode = rng.choice(modes)
                if mode == "freshE":
                    E[x] |= 1 << N
                    E[y] |= 1 << N
                    N += 1
                elif mode == "freshF":
                    F[x] |= 1 << N
                    F[y] |= 1 << N
                    N += 1
                elif mode == "oldE":
                    nd = rng.choice(regular)
                    E[x] |= 1 << nd
                    E[y] |= 1 << nd
                elif mode == "oldF":
                    nd = rng.choice(regular)
                    F[x] |= 1 << nd
                    F[y] |= 1 << nd
                elif mode == "low":
                    zs = [z for z in range(m) if lt(z, x) and lt(z, y)]
                    if zs:
                        z = rng.choice(zs)
                        add_med(z, x)
                        add_med(z, y)
                elif mode == "up":
                    zs = [z for z in range(m) if lt(x, z) and lt(y, z)]
                    if zs:
                        z = rng.choice(zs)
                        add_med(x, z)
                        add_med(y, z)
            if not ok():
                E[x] |= 1 << N
                E[y] |= 1 << N
                N += 1
    I = Inst(N, s, t, le, E, F, medges, name)
    return I
