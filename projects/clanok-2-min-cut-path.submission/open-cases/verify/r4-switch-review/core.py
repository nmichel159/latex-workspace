"""Core of the independent review of r4-switch.md: 2CH instances, P2, exact solvers, the search of Theorem 5.

Written from the definitions in r4-switch.md section 1 and 3 only (no import of r4-switch/).
An instance: N nodes 0..N-1, terminals s, t, switches w with node sets E_w (type 0) and F_w (type 1).
A side is a pair (switch, type) with a non-empty node set; sides are indexed 0..D-1.
"""
import itertools
from collections import deque


class Inst:
    def __init__(self, N, s, t, sw):
        self.N, self.s, self.t = N, s, t
        self.sw = [(frozenset(E), frozenset(F)) for E, F in sw]
        self.n = len(self.sw)
        self.sides = []      # (switch, type)
        self.sets = []       # node set of each side
        idx = {}
        for w, (E, F) in enumerate(self.sw):
            for typ, S in ((0, E), (1, F)):
                if S:
                    idx[(w, typ)] = len(self.sides)
                    self.sides.append((w, typ))
                    self.sets.append(S)
        self.idx = idx
        self.D = len(self.sides)
        self.partner = [idx.get((w, 1 - typ)) for (w, typ) in self.sides]
        self.typ = [typ for (_, typ) in self.sides]
        self.swof = [w for (w, _) in self.sides]
        D = self.D
        self.meet = [[bool(self.sets[i] & self.sets[j]) for j in range(D)] for i in range(D)]
        self.nbrs = [[j for j in range(D) if j != i and self.meet[i][j]] for i in range(D)]
        self.has_s = [s in S for S in self.sets]
        self.has_t = [t in S for S in self.sets]

    def to_json(self):
        return {"N": self.N, "s": self.s, "t": self.t,
                "sw": [[sorted(E), sorted(F)] for E, F in self.sw]}

    @staticmethod
    def from_json(d):
        return Inst(d["N"], d["s"], d["t"], [(set(E), set(F)) for E, F in d["sw"]])

    def N_of(self, typ, z):
        """N_typ[Z] for the side index z: all sides of type typ meeting Z (contains z if z has type typ)."""
        Z = self.sets[z]
        return frozenset(i for i in range(self.D) if self.typ[i] == typ and self.sets[i] & Z)


def p2(inst):
    sw = inst.sw
    for w in range(inst.n):
        for v in range(w + 1, inst.n):
            if not (sw[w][0] & sw[v][0]) and not (sw[w][1] & sw[v][1]):
                return False
    return True


def brute_force(inst):
    """Yes iff some mode vector connects s and t in the hypergraph of picked sides (union-find)."""
    if inst.s == inst.t:
        return True
    for modes in itertools.product((0, 1), repeat=inst.n):
        parent = list(range(inst.N))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x
        for w, m in enumerate(modes):
            S = inst.sw[w][m]
            it = iter(S)
            first = next(it, None)
            if first is None:
                continue
            rf = find(first)
            for x in it:
                rx = find(x)
                if rx != rf:
                    parent[rx] = rf
        if find(inst.s) == find(inst.t):
            return True
    return False


def dist_to_t(inst):
    """Number of further sides needed from side i to reach a side containing t, ignoring switch distinctness."""
    D = inst.D
    INF = 10 ** 9
    d = [INF] * D
    q = deque()
    for i in range(D):
        if inst.has_t[i]:
            d[i] = 0
            q.append(i)
    while q:
        i = q.popleft()
        for j in inst.nbrs[i]:
            if d[j] == INF:
                d[j] = d[i] + 1
                q.append(j)
    return d


def shortest_valid_paths(inst, limit=None, maxlen=None):
    """Return (L, list of all shortest valid paths as tuples of side indices), or (None, []) for a no-instance.

    Level L searches only for paths whose non-consecutive members are disjoint, with s only in the first and t only
    in the last member.  Every valid path of the minimum length L* has these properties (any violation gives a
    shorter valid path), and every path found at a level L is a valid path, so the first level with a path is L*
    and it lists all shortest valid paths.  Requires s != t.
    """
    assert inst.s != inst.t
    dt = dist_to_t(inst)
    D = inst.D
    starts = [i for i in range(D) if inst.has_s[i]]
    INF = 10 ** 9
    if not starts or min(dt[i] for i in starts) >= INF:
        return None, []
    top = maxlen if maxlen is not None else inst.n
    for L in range(1, top + 1):
        found = []
        path = []
        used = set()

        def rec(last):
            k = len(path)
            if k == L:
                if inst.has_t[last]:
                    found.append(tuple(path))
                return limit is not None and len(found) >= limit
            if inst.has_t[last]:
                return False
            for y in inst.nbrs[last]:
                if inst.swof[y] in used or inst.has_s[y]:
                    continue
                if k + 1 + dt[y] > L:
                    continue
                if inst.has_t[y] and k + 1 < L:
                    continue
                ok = True
                for z in path[:-1]:
                    if inst.meet[z][y]:
                        ok = False
                        break
                if not ok:
                    continue
                path.append(y)
                used.add(inst.swof[y])
                stop = rec(y)
                used.discard(inst.swof[y])
                path.pop()
                if stop:
                    return True
            return False

        for x in starts:
            if 1 + dt[x] > L:
                continue
            path.append(x)
            used.add(inst.swof[x])
            stop = rec(x)
            used.discard(inst.swof[x])
            path.pop()
            if stop:
                break
        if found:
            return L, found
    return None, []


def is_valid_path(inst, P):
    if not P:
        return False
    if not inst.has_s[P[0]] or not inst.has_t[P[-1]]:
        return False
    for a in range(len(P) - 1):
        if not inst.meet[P[a]][P[a + 1]]:
            return False
    sws = [inst.swof[x] for x in P]
    return len(set(sws)) == len(sws)


def is_valid_walk(inst, W):
    if not W:
        return False
    if not inst.has_s[W[0]] or not inst.has_t[W[-1]]:
        return False
    for a in range(len(W) - 1):
        if W[a] != W[a + 1] and not inst.meet[W[a]][W[a + 1]]:
            return False
    S = set(W)
    for x in S:
        if inst.partner[x] is not None and inst.partner[x] in S:
            return False
    return True


def search5(inst, K, B):
    """Breadth-first search of Theorem 5 over states (current side, members so far that lie in K).

    Returns a K-admissible walk (list of side indices) or None.  Conditions at each appended side Y:
    (i) partner of Y empty or in K; (ii) partner of Y not among the stored sides; (iii) at most B stored sides.
    """
    K = frozenset(K)
    D = inst.D
    par = {}
    q = deque()

    def allowed(y, stored):
        p = inst.partner[y]
        if p is not None and p not in K:
            return None
        if p is not None and p in stored:
            return None
        ns = stored | {y} if y in K else stored
        if len(ns) > B:
            return None
        return ns

    for y in range(D):
        if not inst.has_s[y]:
            continue
        ns = allowed(y, frozenset())
        if ns is None:
            continue
        st = (y, ns)
        if st not in par:
            par[st] = None
            q.append(st)
    while q:
        st = q.popleft()
        y, stored = st
        if inst.has_t[y]:
            walk = []
            cur = st
            while cur is not None:
                walk.append(cur[0])
                cur = par[cur]
            return walk[::-1]
        for z in [y] + inst.nbrs[y]:
            ns = allowed(z, stored)
            if ns is None:
                continue
            nst = (z, ns)
            if nst not in par:
                par[nst] = st
                q.append(nst)
    return None


def random_instance(rng, N, n, dens, s=0, t=1):
    sw = []
    for _ in range(n):
        E = {x for x in range(N) if rng.random() < dens}
        F = {x for x in range(N) if rng.random() < dens}
        sw.append((E, F))
    return Inst(N, s, t, sw)


def p2_repair(inst, rng, fresh=False):
    """Make P2 hold by adding, for each violating pair, a node to E_w, E_v or F_w, F_v.

    With fresh=True a new private node is created for each repair, otherwise a random existing node is used.
    """
    sw = [(set(E), set(F)) for E, F in inst.sw]
    N = inst.N
    for w in range(len(sw)):
        for v in range(w + 1, len(sw)):
            if not (sw[w][0] & sw[v][0]) and not (sw[w][1] & sw[v][1]):
                typ = rng.randrange(2)
                if fresh:
                    x = N
                    N += 1
                else:
                    x = rng.randrange(N)
                sw[w][typ].add(x)
                sw[v][typ].add(x)
    return Inst(N, inst.s, inst.t, sw)
