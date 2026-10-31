"""Own ZZ library of the reviewer r5-verify (written from the definitions of theory-dc.md, r4-brief.md).

ZZ instance: elements 0..n-1, a preorder given by bitmasks up[x] = {y : x <= y}, down[x] = {y : y <= x},
R = list of pairs (a, b) with a < b strictly, terminals u (least), v (greatest), {u, v} not in R.
For a down-set D (u in D, v not in D) G_D = the R-edges with exactly one end in D.
Question: is there D with u, v connected in G_D (equivalently a consistent zigzag)?
No code of other agents is imported here.
"""
from collections import deque
import itertools
import random


def bits(m):
    out = []
    while m:
        low = m & -m
        out.append(low.bit_length() - 1)
        m ^= low
    return out


class Inst:
    def __init__(self, n, rel, R, u, v, names=None):
        """rel: iterable of pairs (a, b) meaning a <= b (generators); the reflexive-transitive closure is taken."""
        self.n = n
        up = [1 << x for x in range(n)]
        for a, b in rel:
            up[a] |= 1 << b
        # transitive closure (Warshall on bitsets)
        for k in range(n):
            mk = up[k]
            for x in range(n):
                if (up[x] >> k) & 1:
                    up[x] |= mk
        self.up = up
        down = [0] * n
        for x in range(n):
            for y in bits(up[x]):
                down[y] |= 1 << x
        self.down = down
        self.R = [tuple(e) for e in R]
        self.u, self.v = u, v
        self.names = names
        self.adj = [[] for _ in range(n)]
        for a, b in self.R:
            self.adj[a].append(b)
            self.adj[b].append(a)

    def le(self, a, b):
        return (self.up[a] >> b) & 1 == 1

    def lt(self, a, b):
        return self.le(a, b) and not self.le(b, a)

    def comparable(self, a, b):
        return self.le(a, b) or self.le(b, a)

    def name(self, x):
        return self.names[x] if self.names else str(x)

    # --------------------------------------------------------------------------------------------------------------
    def check(self):
        """ZZ axioms; returns a list of violations (empty if fine)."""
        bad = []
        n, u, v = self.n, self.u, self.v
        for x in range(n):
            if not self.le(x, x):
                bad.append("not reflexive %d" % x)
            if not self.le(u, x):
                bad.append("u not <= %s" % self.name(x))
            if not self.le(x, v):
                bad.append("%s not <= v" % self.name(x))
            for y in bits(self.up[x]):
                if (self.up[y] | self.up[x]) != self.up[x]:
                    bad.append("not transitive at %d %d" % (x, y))
        if self.le(v, u):
            bad.append("u ~ v")
        seen = set()
        for a, b in self.R:
            if not self.lt(a, b):
                bad.append("R-edge not strict %s %s" % (self.name(a), self.name(b)))
            if frozenset((a, b)) in seen:
                bad.append("duplicate edge")
            seen.add(frozenset((a, b)))
        if frozenset((u, v)) in seen:
            bad.append("uv in R")
        return bad

    def has_ties(self):
        return any(self.le(a, b) and self.le(b, a) for a in range(self.n) for b in range(a + 1, self.n))

    # --------------------------------------------------------------------------------------------------------------
    def incomparable_pairs(self):
        return [(a, b) for a in range(self.n) for b in range(a + 1, self.n) if not self.comparable(a, b)]

    def has_witness(self, x, y, forbid_edge=None):
        """Common R-neighbour strictly below both or strictly above both (P2 witness)."""
        nx = set(self.adj[x])
        for w in self.adj[y]:
            if w in nx:
                if forbid_edge is not None and (frozenset((w, x)) == forbid_edge or frozenset((w, y)) == forbid_edge):
                    continue
                if (self.lt(w, x) and self.lt(w, y)) or (self.lt(x, w) and self.lt(y, w)):
                    return True
        return False

    def p2_failures(self):
        return [(x, y) for x, y in self.incomparable_pairs() if not self.has_witness(x, y)]

    def p3_failures(self):
        out = []
        for x, y in self.incomparable_pairs():
            ok = any(self.comparable(z, y) for z in self.adj[x]) or any(self.comparable(z, x) for z in self.adj[y])
            if not ok:
                out.append((x, y))
        return out

    # --------------------------------------------------------------------------------------------------------------
    def zz_search(self, want=False):
        """Exact: BFS over states (current element, D = down-closure of valleys, U = up-closure of peaks, parity).
        A walk found this way has every valley in D, every peak in U, D cap U empty, so it lies in G_D."""
        u, v = self.u, self.v
        start = (u, self.down[u], 0, 0)
        seen = {start}
        q = deque([(start, None)])
        parent = {start: None}
        while q:
            st, _ = q.popleft()
            x, D, U, par = st
            if par == 1 and x == v:
                if want:
                    path = []
                    s = st
                    while s is not None:
                        path.append(s[0])
                        s = parent[s]
                    return True, path[::-1], D
                return True
            for y in self.adj[x]:
                if par == 0:      # x valley, y must be a peak above x, not in D
                    if not self.lt(x, y) or (D >> y) & 1:
                        continue
                    ns = (y, D, U | self.up[y], 1)
                else:             # x peak, y valley below x, not in U
                    if not self.lt(y, x) or (U >> y) & 1:
                        continue
                    ns = (y, D | self.down[y], U, 0)
                if ns not in seen:
                    seen.add(ns)
                    parent[ns] = st
                    q.append((ns, None))
        return (False, None, None) if want else False

    def is_downset(self, D):
        for x in bits(D):
            if self.down[x] & ~D:
                return False
        return True

    def connected_in_GD(self, D):
        par = list(range(self.n))

        def find(a):
            while par[a] != a:
                par[a] = par[par[a]]
                a = par[a]
            return a
        for a, b in self.R:
            if ((D >> a) & 1) != ((D >> b) & 1):
                ra, rb = find(a), find(b)
                if ra != rb:
                    par[ra] = rb
        return find(self.u) == find(self.v)

    def downsets(self, limit=None):
        """All down-sets D with u in D, v not in D (exponential; for small instances)."""
        n = self.n
        # order elements by size of down-set (a linear extension of classes)
        order = sorted(range(n), key=lambda x: bin(self.down[x]).count("1"))
        out = []

        def rec(i, D, excluded):
            if limit is not None and len(out) > limit:
                raise OverflowError
            if i == n:
                out.append(D)
                return
            x = order[i]
            if (D >> x) & 1 or (excluded >> x) & 1:
                rec(i + 1, D, excluded)
                return
            # include x: needs all of down[x] includable (not excluded)
            if not (self.down[x] & excluded) and not (self.down[x] >> self.v) & 1:
                rec(i + 1, D | self.down[x], excluded)
            # exclude x: then everything above x excluded; u cannot be excluded
            if not (self.up[x] & D) and not (self.up[x] >> self.u) & 1:
                rec(i + 1, D, excluded | self.up[x])
        rec(0, 1 << self.u | self.down[self.u], 1 << self.v | self.up[self.v])
        return out

    def zz_brute(self, limit=None):
        for D in self.downsets(limit):
            if self.connected_in_GD(D):
                return True
        return False
