"""Core of the review rv-classes-q of r5-classes.md: 2CH with classes + P2.

Written from the definitions of r5-classes.md sections 1-2c only (no import of r5-classes/).

Instance: nodes 0..N-1, terminals s != t, switches w with node sets E_w (type 0) and F_w (type 1), stored as int
bitmasks over the nodes, and a class cls[w] for every switch (normalised to 0..c-1).  A side is the pair (w, ty),
side id 2*w + ty; it *exists* iff its node set is non-empty (empty sides are "possibly empty" sides of the text and
meet nothing).  A mode vector is an int whose bit C is the mode of class C (0 = E, 1 = F); every switch picks the
side of the mode of its class.  Sets of sides are int bitmasks over side ids.
"""
import itertools
import math
from fractions import Fraction

import numpy as np


def _mask(S):
    if isinstance(S, int):
        return S
    m = 0
    for x in S:
        m |= 1 << x
    return m


def bits(m):
    """indices of the set bits of the int m, increasing"""
    out = []
    while m:
        low = m & -m
        out.append(low.bit_length() - 1)
        m ^= low
    return out


def popcount(m):
    return bin(m).count("1")


class Inst:
    def __init__(self, N, s, t, sw, cl):
        self.N, self.s, self.t = N, s, t
        self.sw = [[_mask(E), _mask(F)] for E, F in sw]
        self.n = len(self.sw)
        lab = {}
        self.cl = []
        for x in cl:
            if x not in lab:
                lab[x] = len(lab)
            self.cl.append(lab[x])
        self.c = len(lab)
        self.classes = [[] for _ in range(self.c)]
        for w, C in enumerate(self.cl):
            self.classes[C].append(w)
        self.D2 = 2 * self.n
        self.mask = [self.sw[x >> 1][x & 1] for x in range(self.D2)]
        self.sides = [x for x in range(self.D2) if self.mask[x]]
        self.sideset = 0
        for x in self.sides:
            self.sideset |= 1 << x
        self.meet = [0] * self.D2
        for x in self.sides:
            mx = self.mask[x]
            b = 0
            for y in self.sides:
                if self.mask[y] & mx:
                    b |= 1 << y
            self.meet[x] = b
        self.hasS = 0
        self.hasT = 0
        for x in self.sides:
            if (self.mask[x] >> s) & 1:
                self.hasS |= 1 << x
            if (self.mask[x] >> t) & 1:
                self.hasT |= 1 << x
        self.Omega = [[0, 0] for _ in range(self.c)]
        for x in self.sides:
            self.Omega[self.cl[x >> 1]][x & 1] |= 1 << x
        self.typmask = [0, 0]
        for x in self.sides:
            self.typmask[x & 1] |= 1 << x

    # ------------------------------------------------------------------ basic
    def cls_of(self, x):
        return self.cl[x >> 1]

    def other(self, x):
        """the other side of the switch of side x (side id; it may not exist)"""
        return x ^ 1

    def exists(self, x):
        return self.mask[x] != 0

    def p2(self):
        """P2 (classes): switches of different classes share a node in E or in F"""
        sw, cl = self.sw, self.cl
        for w in range(self.n):
            for v in range(w + 1, self.n):
                if cl[w] != cl[v] and not (sw[w][0] & sw[v][0]) and not (sw[w][1] & sw[v][1]):
                    return False
        return True

    def p2_violations(self):
        sw, cl = self.sw, self.cl
        out = []
        for w in range(self.n):
            for v in range(w + 1, self.n):
                if cl[w] != cl[v] and not (sw[w][0] & sw[v][0]) and not (sw[w][1] & sw[v][1]):
                    out.append((w, v))
        return out

    def to_json(self):
        return {"N": self.N, "s": self.s, "t": self.t, "sw": [[bits(E), bits(F)] for E, F in self.sw],
                "cl": list(self.cl)}

    @staticmethod
    def from_json(d):
        return Inst(d["N"], d["s"], d["t"], [(set(E), set(F)) for E, F in d["sw"]], d["cl"])

    # ------------------------------------------------------------- mode vectors
    def picked(self, modes):
        p = 0
        Om = self.Omega
        for C in range(self.c):
            p |= Om[C][(modes >> C) & 1]
        return p

    def connects_picked(self, picked):
        if self.s == self.t:
            return True
        start = picked & self.hasS
        if not start:
            return False
        if start & self.hasT:
            return True
        reached = start
        frontier = start
        meet = self.meet
        while frontier:
            nb = 0
            f = frontier
            while f:
                low = f & -f
                nb |= meet[low.bit_length() - 1]
                f ^= low
            new = nb & picked & ~reached
            if new & self.hasT:
                return True
            reached |= new
            frontier = new
        return False

    def connects(self, modes):
        return self.connects_picked(self.picked(modes))

    def dist_picked(self, picked):
        """least number of picked sides in a sequence from s to t (None if not connected)"""
        start = picked & self.hasS
        if not start:
            return None
        if start & self.hasT:
            return 1
        layer = 1
        reached = start
        frontier = start
        meet = self.meet
        while frontier:
            nb = 0
            f = frontier
            while f:
                low = f & -f
                nb |= meet[low.bit_length() - 1]
                f ^= low
            new = nb & picked & ~reached
            layer += 1
            if new & self.hasT:
                return layer
            reached |= new
            frontier = new
        return None

    def solutions(self):
        return [m for m in range(1 << self.c) if self.connects(m)]

    def brute(self):
        for m in range(1 << self.c):
            if self.connects(m):
                return True
        return False

    # ------------------------------------------------------------ valid paths
    def is_valid_path(self, P):
        if not P:
            return False
        for x in P:
            if not self.mask[x]:
                return False
        if not ((self.mask[P[0]] >> self.s) & 1) or not ((self.mask[P[-1]] >> self.t) & 1):
            return False
        for a in range(len(P) - 1):
            if not (self.mask[P[a]] & self.mask[P[a + 1]]):
                return False
        sws = [x >> 1 for x in P]
        if len(set(sws)) != len(sws):
            return False
        ty = {}
        for x in P:
            C = self.cl[x >> 1]
            if ty.setdefault(C, x & 1) != (x & 1):
                return False
        return True

    def dist_to_t(self):
        """unconstrained number of sides from each existing side to a side containing t (BFS on the side graph)"""
        INF = 10 ** 9
        d = [INF] * self.D2
        frontier = [x for x in self.sides if (self.hasT >> x) & 1]
        for x in frontier:
            d[x] = 1
        k = 1
        while frontier:
            k += 1
            nxt = []
            for x in frontier:
                for y in bits(self.meet[x]):
                    if d[y] == INF:
                        d[y] = k
                        nxt.append(y)
            frontier = nxt
        return d

    def shortest_paths_dfs(self, limit=None, maxlen=None):
        """(r, list of all shortest valid paths) by iterative deepening with exact pruning (A1, s/t only at the
        ends, unconstrained distance bound).  (None, []) for a no-instance.  `limit` caps the number of paths."""
        if self.s == self.t:
            raise ValueError("s = t")
        dt = self.dist_to_t()
        INF = 10 ** 9
        starts = [x for x in self.sides if (self.hasS >> x) & 1 and dt[x] < INF]
        if not starts:
            return None, []
        lo = min(dt[x] for x in starts)
        hi = maxlen if maxlen is not None else self.n
        mask, meet, cl, s, t = self.mask, self.meet, self.cl, self.s, self.t
        for L in range(lo, hi + 1):
            paths = []
            ctype = [-1] * self.c

            def rec(path, usedsw, prevunion):
                if limit is not None and len(paths) >= limit:
                    return
                d = len(path)
                last = path[-1]
                if d == L:
                    if (mask[last] >> t) & 1:
                        paths.append(tuple(path))
                    return
                if (mask[last] >> t) & 1:
                    return
                cand = meet[last]
                for y in bits(cand):
                    if y == last:
                        continue
                    w = y >> 1
                    if (usedsw >> w) & 1:
                        continue
                    C = cl[w]
                    ty = y & 1
                    if ctype[C] != -1 and ctype[C] != ty:
                        continue
                    my = mask[y]
                    if my & prevunion:
                        continue
                    if (my >> s) & 1:
                        continue
                    if dt[y] > L - d:
                        continue
                    old = ctype[C]
                    ctype[C] = ty
                    path.append(y)
                    rec(path, usedsw | (1 << w), prevunion | mask[last])
                    path.pop()
                    ctype[C] = old

            for x in starts:
                if dt[x] > L:
                    continue
                C = self.cl[x >> 1]
                ctype[C] = x & 1
                rec([x], 1 << (x >> 1), 0)
                ctype[C] = -1
            if paths:
                return L, paths
        return None, []

    def shortest_paths_modes(self, limit=None):
        """(r, sorted list of all shortest valid paths) through the mode vectors (exact, for small c)"""
        best = None
        sols = []
        for m in range(1 << self.c):
            p = self.picked(m)
            d = self.dist_picked(p)
            if d is None:
                continue
            sols.append((m, p, d))
            if best is None or d < best:
                best = d
        if best is None:
            return None, []
        out = set()
        mask, meet, s, t = self.mask, self.meet, self.s, self.t
        for m, p, d in sols:
            if d != best:
                continue
            # layers
            layer = {}
            start = p & self.hasS
            cur = start
            reached = start
            k = 1
            for x in bits(cur):
                layer[x] = 1
            while cur and k < best:
                nb = 0
                for x in bits(cur):
                    nb |= meet[x]
                new = nb & p & ~reached
                k += 1
                for x in bits(new):
                    layer[x] = k
                reached |= new
                cur = new

            def rec(path):
                last = path[-1]
                if len(path) == best:
                    if (mask[last] >> t) & 1:
                        out.add(tuple(path))
                    return
                for y in bits(meet[last] & p):
                    if layer.get(y) == len(path) + 1:
                        path.append(y)
                        rec(path)
                        path.pop()

            for x in bits(start):
                rec([x])
        res = sorted(out)
        if limit is not None:
            res = res[:limit]
        return best, res

    # ---------------------------------------------------- descriptions (§2a)
    def Nset(self, tau, Z):
        """N_tau[Z]: the existing tau-sides meeting the side Z (empty if Z is empty)"""
        if not self.mask[Z]:
            return 0
        return self.meet[Z] & self.typmask[tau]

    def sigma(self, U, tau):
        """sigma_U: class C gets mode 1 - tau iff Omega(C, tau) is contained in U, else tau"""
        m = 0
        for C in range(self.c):
            mode = (1 - tau) if (self.Omega[C][tau] & ~U) == 0 else tau
            m |= mode << C
        return m

    def path_types(self, P):
        """class -> type used on P"""
        pt = {}
        for x in P:
            pt[self.cl[x >> 1]] = x & 1
        return pt

    def misclassified(self, P, modes):
        """classes of P whose mode under `modes` differs from their type on P"""
        pt = self.path_types(P)
        return sorted(C for C, ty in pt.items() if ((modes >> C) & 1) != ty)

    def picks_path(self, P, modes):
        for x in P:
            if ((modes >> self.cl[x >> 1]) & 1) != (x & 1):
                return False
        return True


# ------------------------------------------------------------------ DESC
def desc_items(I, tau, f, g):
    """iterator over (U, description) for DESC(f, g, .) with type tau: unions of at most f sets N_tau[Z]
    (Z any existing side) and at most g class groups Omega(C, tau) or single tau-sides.  Distinct sets only."""
    Ns = {}
    for Z in I.sides:
        Ns.setdefault(I.Nset(tau, Z), Z)
    Nlist = sorted(Ns.items())
    items = {}
    for C in range(I.c):
        items.setdefault(I.Omega[C][tau], ("class", C))
    for x in I.sides:
        if (x & 1) == tau:
            items.setdefault(1 << x, ("side", x))
    ilist = sorted(items.items())
    seen = set()
    for i in range(f + 1):
        for combo in itertools.combinations(Nlist, i):
            U1 = 0
            for m, _ in combo:
                U1 |= m
            for j in range(g + 1):
                for combo2 in itertools.combinations(ilist, j):
                    U = U1
                    for m, _ in combo2:
                        U |= m
                    if U in seen:
                        continue
                    seen.add(U)
                    yield U, (tuple(z for _, z in combo), tuple(d for _, d in combo2))


def desc_literal(I, f, g, e):
    """DESC(f, g, e) exactly as defined in r5-classes.md §2a (enumerates U and Phi)."""
    for tau in (0, 1):
        for U, descr in desc_items(I, tau, f, g):
            base = I.sigma(U, tau)
            for l in range(min(e, I.c) + 1):
                for Phi in itertools.combinations(range(I.c), l):
                    m = base
                    for C in Phi:
                        m ^= 1 << C
                    if I.connects(m):
                        return True, (tau, U, descr, Phi, m)
    return False, None


def hyper_dist(c, sols):
    """for every mode vector (0..2^c-1) its Hamming distance to the nearest solution (255 if none)"""
    size = 1 << c
    INF = 255
    dist = np.full(size, INF, dtype=np.uint8)
    if not sols:
        return dist
    idx = np.arange(size, dtype=np.int64)
    frontier = np.zeros(size, dtype=bool)
    frontier[np.array(sols, dtype=np.int64)] = True
    dist[frontier] = 0
    d = 0
    while frontier.any():
        d += 1
        nb = np.zeros(size, dtype=bool)
        for b in range(c):
            nb |= frontier[idx ^ (1 << b)]
        new = nb & (dist == INF)
        dist[new] = d
        frontier = new
    return dist


def solutions_np(I, chunk=1 << 15):
    """boolean array over all 2^c mode vectors: does the vector connect s and t (vectorised BFS on sides)"""
    c = I.c
    sides = I.sides
    D = len(sides)
    size = 1 << c
    out = np.zeros(size, dtype=bool)
    if D == 0:
        return out
    pos = {x: i for i, x in enumerate(sides)}
    adj = np.zeros((D, D), dtype=np.float32)
    for x in sides:
        for y in bits(I.meet[x]):
            adj[pos[x], pos[y]] = 1.0
    scls = np.array([I.cl[x >> 1] for x in sides], dtype=np.int64)
    sty = np.array([x & 1 for x in sides], dtype=np.int64)
    hs = np.array([(I.hasS >> x) & 1 for x in sides], dtype=bool)
    ht = np.array([(I.hasT >> x) & 1 for x in sides], dtype=bool)
    for lo in range(0, size, chunk):
        M = np.arange(lo, min(size, lo + chunk), dtype=np.int64)
        picked = ((M[:, None] >> scls[None, :]) & 1) == sty[None, :]
        reached = picked & hs[None, :]
        while True:
            nb = (reached.astype(np.float32) @ adj) > 0
            new = reached | (nb & picked)
            if (new == reached).all():
                break
            reached = new
        out[lo:lo + len(M)] = (reached & ht[None, :]).any(axis=1)
    return out


def hyper_dist_bool(c, solmask):
    """as hyper_dist, from a boolean solution array"""
    return hyper_dist(c, list(np.nonzero(solmask)[0]))


def desc_accepts(I, f, g, e, dist):
    """DESC(f, g, e) as an algorithm (early exit at the first accepted U), using the hypercube distance array:
    accepts iff some U of the enumerated shape has dist[sigma_U] <= e.  Returns (accepted, (tau, U, descr, d))."""
    for tau in (0, 1):
        for U, descr in desc_items(I, tau, f, g):
            d = int(dist[I.sigma(U, tau)])
            if d <= e:
                return True, (tau, U, descr, d)
    return False, None


def desc_emin(I, f, g, dist):
    """least e for which DESC(f, g, e) accepts (255 if never), from the hypercube distance array"""
    best = 255
    arg = None
    for tau in (0, 1):
        for U, descr in desc_items(I, tau, f, g):
            d = int(dist[I.sigma(U, tau)])
            if d < best:
                best = d
                arg = (tau, U, descr)
                if best == 0:
                    return 0, arg
    return best, arg


# ------------------------------------------------------------- games, covers
def solve_game(A):
    """Exact value of the zero-sum game with payoff matrix A (rows maximise), entries 0/1.
    Returns (lam, p, q) as Fractions with min_j (pA)_j = lam = max_i (Aq)_i (asserted)."""
    R = len(A)
    Cn = len(A[0])
    F1 = Fraction(1)
    F0 = Fraction(0)
    T = []
    for i in range(R):
        row = [Fraction(A[i][j] + 1) for j in range(Cn)] + [F1 if k == i else F0 for k in range(R)] + [F1]
        T.append(row)
    z = [Fraction(-1)] * Cn + [F0] * R + [F0]
    basis = [Cn + i for i in range(R)]
    while True:
        ent = None
        for j in range(Cn + R):
            if z[j] < 0:
                ent = j
                break
        if ent is None:
            break
        best = None
        for i in range(R):
            if T[i][ent] > 0:
                ratio = T[i][-1] / T[i][ent]
                if best is None or ratio < best[0] or (ratio == best[0] and basis[i] < basis[best[1]]):
                    best = (ratio, i)
        assert best is not None, "unbounded LP"
        piv = best[1]
        pv = T[piv][ent]
        T[piv] = [x / pv for x in T[piv]]
        prow = T[piv]
        for i in range(R):
            if i != piv:
                fct = T[i][ent]
                if fct != 0:
                    T[i] = [a - fct * b for a, b in zip(T[i], prow)]
        fct = z[ent]
        if fct != 0:
            z = [a - fct * b for a, b in zip(z, prow)]
        basis[piv] = ent
    Ystar = z[-1]
    y = [F0] * Cn
    for i, bv in enumerate(basis):
        if bv < Cn:
            y[bv] = T[i][-1]
    x = [z[Cn + i] for i in range(R)]
    vs = 1 / Ystar
    q = [yj * vs for yj in y]
    p = [xi * vs for xi in x]
    lam = vs - 1
    assert sum(p) == 1 and sum(q) == 1 and min(p) >= 0 and min(q) >= 0
    colpay = [sum(p[i] * A[i][j] for i in range(R)) for j in range(Cn)]
    rowpay = [sum(A[i][j] * q[j] for j in range(Cn)) for i in range(R)]
    assert min(colpay) == lam == max(rowpay), (min(colpay), lam, max(rowpay))
    return lam, p, q


def min_cover(universe, sets, cap=None):
    """minimum number of the int bitmasks in `sets` whose union contains `universe`.
    Returns (size, indices) or (None, None) if impossible (or if no cover of size <= cap exists)."""
    if universe == 0:
        return 0, []
    allu = 0
    for m in sets:
        allu |= m
    if universe & ~allu:
        return None, None
    # keep distinct, non-dominated sets (restricted to the universe)
    cand = {}
    for i, m in enumerate(sets):
        mm = m & universe
        if mm and mm not in cand:
            cand[mm] = i
    items = sorted(cand.items(), key=lambda kv: -popcount(kv[0]))
    keep = []
    for m, i in items:
        if not any((m | m2) == m2 for m2, _ in keep):
            keep.append((m, i))
    elems = bits(universe)
    cover_of = {e: [k for k, (m, _) in enumerate(keep) if (m >> e) & 1] for e in elems}
    best = [len(keep) + 1 if cap is None else cap + 1, None]
    maxsz = max(popcount(m) for m, _ in keep)

    def rec(unc, chosen):
        if unc == 0:
            if len(chosen) < best[0]:
                best[0] = len(chosen)
                best[1] = list(chosen)
            return
        need = -(-popcount(unc) // maxsz)
        if len(chosen) + need >= best[0]:
            return
        e = min(bits(unc), key=lambda x: len(cover_of[x]))
        opts = sorted(cover_of[e], key=lambda k: -popcount(keep[k][0] & unc))
        for k in opts:
            chosen.append(k)
            rec(unc & ~keep[k][0], chosen)
            chosen.pop()

    rec(universe, [])
    if best[1] is None:
        return None, None
    return best[0], [keep[k][1] for k in best[1]]


def kq(m):
    """k = floor(log2 m) + 1 of Theorem Q"""
    return int(math.floor(math.log2(m))) + 1 if m >= 1 else 1
