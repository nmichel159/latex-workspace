"""Own implementation (reviewer r5-verify) of the general switch form of r4-general.md §5.1, the forced-exit
propagation and pruning of §7.3, the contraction of Theorem R (§8), and the search of Theorem 5' (§5.1), written
from the text of r4-general.md.  No code of other agents is imported here.

Switch form: nodes 0..N-1, terminals s, t; switches 0..m-1 with node bitmasks E[w], F[w]; a preorder le[w][w'] on
the switches; a mode vector is a dict/list w -> 0 (E-mode, outside D) or 1 (F-mode, inside D) that is a down-set
(w F-mode and w' <= w imply w' F-mode).  Sides: 2w (E_w), 2w + 1 (F_w), only non-empty ones.
"""
import itertools
import random
from collections import deque
from zzlib import Inst, bits


class SW:
    def __init__(self, N, E, F, le, s, t):
        self.N, self.E, self.F, self.le, self.s, self.t = N, list(E), list(F), le, s, t
        self.m = len(E)
        self.sides = [2 * w + ty for w in range(self.m) for ty in (0, 1) if (F[w] if ty else E[w])]
        self.sideset = set(self.sides)

    def mask(self, side):
        return self.F[side >> 1] if side & 1 else self.E[side >> 1]

    # ----------------------------------------------------------------------------------------------------------
    def conflict(self, X, Y):
        """{E_w, F_z} with w <= z."""
        if (X & 1) == (Y & 1):
            return False
        if X & 1:
            X, Y = Y, X
        return self.le[X >> 1][Y >> 1]

    def Pi(self, X):
        w = X >> 1
        if X & 1 == 0:
            return frozenset(2 * z + 1 for z in range(self.m) if self.le[w][z] and (2 * z + 1) in self.sideset)
        return frozenset(2 * z for z in range(self.m) if self.le[z][w] and (2 * z) in self.sideset)

    def is_valid_walk(self, walk):
        if self.s == self.t:
            return True
        if not walk or not (self.mask(walk[0]) >> self.s) & 1 or not (self.mask(walk[-1]) >> self.t) & 1:
            return False
        for a, b in zip(walk, walk[1:]):
            if a != b and not (self.mask(a) & self.mask(b)):
                return False
        S = set(walk)
        for X in S:
            for Y in S:
                if self.conflict(X, Y):
                    return False
        return True

    def walk_to_modes(self, walk):
        """Mode vector certified by a valid walk: F-mode exactly on the down-closure of its F-members."""
        Fm = [Y >> 1 for Y in walk if Y & 1]
        modes = [1 if any(self.le[w][z] for z in Fm) else 0 for w in range(self.m)]
        return modes

    # ----------------------------------------------------------------------------------------------------------
    def is_downset_modes(self, modes):
        for w in range(self.m):
            if modes[w] == 1:
                for z in range(self.m):
                    if self.le[z][w] and modes[z] == 0:
                        return False
        return True

    def connects(self, modes):
        par = list(range(self.N))

        def find(a):
            while par[a] != a:
                par[a] = par[par[a]]
                a = par[a]
            return a
        for w in range(self.m):
            side = self.F[w] if modes[w] else self.E[w]
            b = bits(side)
            for x in b[1:]:
                ra, rb = find(b[0]), find(x)
                if ra != rb:
                    par[ra] = rb
        return find(self.s) == find(self.t)

    def mode_vectors(self):
        """All order-consistent mode vectors (down-sets of the switch preorder)."""
        m = self.m
        order = sorted(range(m), key=lambda w: sum(self.le[z][w] for z in range(m)))
        out = []
        modes = [None] * m

        def rec(i):
            if i == m:
                out.append(list(modes))
                return
            w = order[i]
            if modes[w] is not None:
                rec(i + 1)
                return
            for mo in (0, 1):
                ch = []
                ok = True
                for z in range(m):
                    if (mo == 1 and self.le[z][w]) or (mo == 0 and self.le[w][z]):
                        if modes[z] is None:
                            modes[z] = mo
                            ch.append(z)
                        elif modes[z] != mo:
                            ok = False
                if ok:
                    rec(i + 1)
                for z in ch:
                    modes[z] = None
        rec(0)
        return out

    def solutions(self):
        if self.s == self.t:
            return self.mode_vectors()
        return [mv for mv in self.mode_vectors() if self.connects(mv)]

    # ----------------------------------------------------------------------------------------------------------
    # forced-exit propagation (r4-general.md §7.3), written from the text
    def closure(self, fixed):
        fx = dict(fixed)
        stack = list(fx.items())
        while stack:
            w, mo = stack.pop()
            for z in range(self.m):
                if (mo == 1 and self.le[z][w]) or (mo == 0 and self.le[w][z]):
                    if z in fx:
                        if fx[z] != mo:
                            return None
                    else:
                        fx[z] = mo
                        stack.append((z, mo))
        return fx

    def refutes(self, fixed):
        fx = self.closure(fixed)
        if fx is None:
            return True
        for start, goal in ((self.s, self.t), (self.t, self.s)):
            f2 = dict(fx)
            C = 1 << start
            while True:
                # grow C by the fixed picked sides (component of `start`)
                changed = True
                while changed:
                    changed = False
                    for w, mo in f2.items():
                        side = self.F[w] if mo else self.E[w]
                        if side & C and side & ~C:
                            C |= side
                            changed = True
                if (C >> goal) & 1:
                    break
                exits = []
                for w in range(self.m):
                    if w in f2:
                        continue
                    for mo in (0, 1):
                        side = self.F[w] if mo else self.E[w]
                        if side & C and side & ~C:
                            exits.append((w, mo))
                if not exits:
                    return True
                if len(exits) == 1:
                    f3 = dict(f2)
                    f3[exits[0][0]] = exits[0][1]
                    f3 = self.closure(f3)
                    if f3 is None:
                        return True
                    f2 = f3
                    continue
                break
        return False

    def prune(self):
        """Returns (fixed, status): status 'no' if some switch has both modes refuted."""
        fixed = {}
        while True:
            changed = False
            for w in range(self.m):
                if w in fixed:
                    continue
                r0 = self.refutes({**fixed, w: 0})
                r1 = self.refutes({**fixed, w: 1})
                if r0 and r1:
                    return fixed, "no"
                if r0 or r1:
                    f3 = self.closure({**fixed, w: 1 if r0 else 0})
                    if f3 is None:
                        return fixed, "no"
                    fixed = f3
                    changed = True
            if not changed:
                return fixed, "ok"

    # ----------------------------------------------------------------------------------------------------------
    # Theorem R contraction
    def contract(self, fixed):
        free = [w for w in range(self.m) if w not in fixed]
        par = list(range(self.N))

        def find(a):
            while par[a] != a:
                par[a] = par[par[a]]
                a = par[a]
            return a
        for w, mo in fixed.items():
            b = bits(self.F[w] if mo else self.E[w])
            for x in b[1:]:
                ra, rb = find(b[0]), find(x)
                if ra != rb:
                    par[ra] = rb
        roots = {}
        for x in range(self.N):
            roots.setdefault(find(x), len(roots))

        def remap(mk):
            o = 0
            for x in bits(mk):
                o |= 1 << roots[find(x)]
            return o
        E = [remap(self.E[w]) for w in free]
        F = [remap(self.F[w]) for w in free]
        k = len(free)
        le = [[self.le[a][b] for b in free] for a in free]
        return SW(len(roots), E, F, le, roots[find(self.s)], roots[find(self.t)]), free

    def p2_switch(self):
        """P2 of 2CH for all pairs of distinct switches (node form)."""
        bad = []
        for a in range(self.m):
            for b in range(a + 1, self.m):
                if not (self.E[a] & self.E[b]) and not (self.F[a] & self.F[b]):
                    bad.append((a, b))
        return bad

    # ----------------------------------------------------------------------------------------------------------
    # search of Theorem 5'
    def step5(self, Y, St, Dc, nd, K, B, s):
        if Y in Dc:
            return None
        P = self.Pi(Y)
        if P & St:
            return None
        miss = P - K - Dc
        if miss:
            if Y in K or nd >= s:
                return None
            Dc = Dc | miss
            nd += 1
        if Y in K and Y not in St:
            if len(St) >= B:
                return None
            St = St | {Y}
        return St, Dc, nd

    def search5(self, K, B, s):
        """BFS over (current side, St, Dc, nd); returns an accepted walk or None."""
        K = frozenset(K)
        if self.s == self.t:
            return []
        e0 = frozenset()
        q = deque()
        seen = set()
        for Y in self.sides:
            if (self.mask(Y) >> self.s) & 1:
                r = self.step5(Y, e0, e0, 0, K, B, s)
                if r is None:
                    continue
                st = (Y,) + r
                if st not in seen:
                    seen.add(st)
                    q.append((st, (Y,)))
        while q:
            (cur, St, Dc, nd), walk = q.popleft()
            if (self.mask(cur) >> self.t) & 1:
                return list(walk)
            for Y in self.sides:
                if Y == cur or not (self.mask(Y) & self.mask(cur)):
                    continue
                r = self.step5(Y, St, Dc, nd, K, B, s)
                if r is None:
                    continue
                st = (Y,) + r
                if st not in seen:
                    seen.add(st)
                    q.append((st, walk + (Y,)))
        return None

    def all_rule_walks(self, K, B, s, maxlen):
        """Every walk (no state merging) of length <= maxlen accepted step by step by the rules of Theorem 5', ending
        in a side that contains t.  Consecutive sides equal or meeting."""
        K = frozenset(K)
        out = []
        e0 = frozenset()

        def rec(walk, St, Dc, nd):
            cur = walk[-1]
            if (self.mask(cur) >> self.t) & 1:
                out.append(list(walk))
            if len(walk) >= maxlen:
                return
            for Y in self.sides:
                if Y != cur and not (self.mask(Y) & self.mask(cur)):
                    continue
                r = self.step5(Y, St, Dc, nd, K, B, s)
                if r is None:
                    continue
                walk.append(Y)
                rec(walk, *r)
                walk.pop()
        for Y in self.sides:
            if (self.mask(Y) >> self.s) & 1:
                r = self.step5(Y, e0, e0, 0, K, B, s)
                if r is not None:
                    rec([Y], *r)
        return out


# --------------------------------------------------------------------------------------------------------------
def from_zz(I):
    """General switch form of a ZZ instance (r4-general.md §5.1)."""
    n = I.n
    Bc = [x for x in range(n) if I.le(x, I.u)]
    Tc = [x for x in range(n) if I.le(I.v, x)]
    Bs, Ts = set(Bc), set(Tc)
    M = [x for x in range(n) if x not in Bs and x not in Ts]
    idx = {x: i for i, x in enumerate(M)}
    par = {x: x for x in Bc + Tc}

    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a
    for a, b in I.R:
        if (a in Bs and b in Ts) or (b in Bs and a in Ts):
            ra, rb = find(a), find(b)
            if ra != rb:
                par[ra] = rb
    roots = {}
    node = {}
    for x in Bc + Tc:
        node[x] = roots.setdefault(find(x), len(roots))
    N = len(roots)
    m = len(M)
    E = [0] * m
    F = [0] * m
    for a, b in I.R:
        if not I.lt(a, b):
            a, b = b, a
        if a in idx and b in idx:
            z = N
            N += 1
            F[idx[a]] |= 1 << z
            E[idx[b]] |= 1 << z
        elif a in idx:
            assert b in Ts, "upper neighbour of a middle element must be middle or top"
            F[idx[a]] |= 1 << node[b]
        elif b in idx:
            assert a in Bs
            E[idx[b]] |= 1 << node[a]
    le = [[I.le(M[i], M[j]) for j in range(m)] for i in range(m)]
    G = SW(N, E, F, le, node[I.u], node[I.v])
    G.M = M
    return G


def random_zz_p2(rng, nmid, nb, nt, p_order, p_tie, p_edge, p_mid_wit=0.4, max_new=6):
    """Random ZZ instance with P2: u = 0, v = 1, bottoms 2..nb+1 (tied to u), tops, middle elements with a random
    preorder (random DAG plus ties), random real edges, then P2 repaired by witnesses (existing or new bottoms/tops,
    or middle witnesses below or above both when available)."""
    u, v = 0, 1
    bots = list(range(2, 2 + nb))
    tops = list(range(2 + nb, 2 + nb + nt))
    mid = list(range(2 + nb + nt, 2 + nb + nt + nmid))
    n = 2 + nb + nt + nmid
    rel = []
    for b in bots:
        rel += [(b, u), (u, b)]
    for t in tops:
        rel += [(t, v), (v, t)]
    perm = list(mid)
    rng.shuffle(perm)
    for i in range(nmid):
        for j in range(i + 1, nmid):
            if rng.random() < p_order:
                rel.append((perm[i], perm[j]))
                if rng.random() < p_tie:
                    rel.append((perm[j], perm[i]))
    base_rel = rel

    def build(n, rel, R):
        r2 = list(rel) + [(u, x) for x in range(n)] + [(x, v) for x in range(n)]
        return Inst(n, r2, R, u, v)
    I = build(n, rel, [])
    R = set()
    for a in range(n):
        for b in range(n):
            if a != b and I.lt(a, b) and frozenset((a, b)) != frozenset((u, v)) and rng.random() < p_edge:
                R.add((a, b))
    I = build(n, rel, sorted(R))
    newc = 0
    for _ in range(200):
        bad = I.p2_failures()
        if not bad:
            break
        x, y = rng.choice(bad)
        lowers = [w for w in range(n) if I.lt(w, x) and I.lt(w, y) and w not in bots + [u]]
        uppers = [w for w in range(n) if I.lt(x, w) and I.lt(y, w) and w not in tops + [v]]
        r = rng.random()
        if r < p_mid_wit and (lowers or uppers):
            w = rng.choice(lowers + uppers)
            if I.lt(w, x):
                R |= {(w, x), (w, y)}
            else:
                R |= {(x, w), (y, w)}
        elif r < 0.75 or newc >= max_new:
            if rng.random() < 0.5 and bots:
                b = rng.choice(bots)
                R |= {(b, x), (b, y)}
            elif tops:
                t = rng.choice(tops)
                R |= {(x, t), (y, t)}
            else:
                b = rng.choice(bots + [u])
                R |= {(b, x), (b, y)}
        else:
            newc += 1
            nn = n
            n += 1
            if rng.random() < 0.5:
                bots.append(nn)
                rel = rel + [(nn, u), (u, nn)]
                R |= {(nn, x), (nn, y)}
            else:
                tops.append(nn)
                rel = rel + [(nn, v), (v, nn)]
                R |= {(x, nn), (y, nn)}
        I = build(n, rel, sorted(R))
    if I.p2_failures():
        return None
    return I


def random_abstract(rng, N, m, p_side, p_order, p_tie):
    """Random abstract switch form (no P2, any hypergraph) with a random preorder on the switches."""
    E = [sum(1 << x for x in range(N) if rng.random() < p_side) for _ in range(m)]
    F = [sum(1 << x for x in range(N) if rng.random() < p_side) for _ in range(m)]
    le = [[i == j for j in range(m)] for i in range(m)]
    perm = list(range(m))
    rng.shuffle(perm)
    for i in range(m):
        for j in range(i + 1, m):
            if rng.random() < p_order:
                le[perm[i]][perm[j]] = True
                if rng.random() < p_tie:
                    le[perm[j]][perm[i]] = True
    for k in range(m):
        for i in range(m):
            if le[i][k]:
                for j in range(m):
                    if le[k][j]:
                        le[i][j] = True
    s, t = 0, N - 1
    return SW(N, E, F, le, s, t)
