"""General switch form of ZZ and the side-set certificate search extended by conflict families (r4-general.md §5).

General switch form (from a ZZ instance, gcert.Inst):
  nodes  = components of the graph of the R-edges between the class B of u and the class T of v (every element of
           B or T lies in exactly one node), plus one private node for every R-edge between two middle elements;
  s, t   = the nodes of u and v;
  switch = middle element w; E_w = nodes of its lower R-neighbours (bottoms; private nodes of middle edges y-w),
           F_w = nodes of its upper R-neighbours (tops; private nodes of middle edges w-x);
  order  = the preorder restricted to the middle elements; a mode vector must be a down-set (w in F-mode, w' <= w
           imply w' in F-mode).
  u, v connected in G_D  <=>  s, t connected in the hypergraph of the sides picked by D (F_w for w in D, else E_w).
Side ids: 2w = E-side of switch w, 2w + 1 = F-side (as in r4-switch/sw.py).
Conflict family Pi(X): X = E_w: the F-sides of all w' >= w; X = F_w: the E-sides of all w' <= w (non-empty sides).
A walk of sides is *valid* if it contains no conflict pair; valid walks from s to t <=> solutions.

search(inst, K, B, s): BFS over states (current side, St = members in K so far, Dc = declared sides, number of
declarations).  Append Y iff Y not in Dc, Pi(Y) has no stored member, and either Pi(Y) is contained in K | Dc, or
(Y not in K, declarations < s, and then Pi(Y) - K - Dc is added to Dc); Y in K is stored (|St| <= B).
Sound for every K, B, s (proof in r4-general.md §5).
"""
import itertools
from collections import deque
from common_r4 import bits


class GSW:
    def __init__(self, I):
        n = I.n
        self.I = I
        B = [x for x in range(n) if (I.B >> x) & 1]
        T = [x for x in range(n) if (I.T >> x) & 1]
        M = [x for x in range(n) if not (I.B >> x) & 1 and not (I.T >> x) & 1]
        self.M = M
        idx = {x: i for i, x in enumerate(M)}
        self.idx = idx
        # union-find on B + T over the B-T edges
        par = {x: x for x in B + T}

        def find(a):
            while par[a] != a:
                par[a] = par[par[a]]
                a = par[a]
            return a
        Bs, Ts = set(B), set(T)
        for a, b in I.R:
            if a in Bs and b in Ts:
                ra, rb = find(a), find(b)
                if ra != rb:
                    par[ra] = rb
        roots = {}
        nodeof = {}
        for x in B + T:
            r = find(x)
            if r not in roots:
                roots[r] = len(roots)
            nodeof[x] = roots[r]
        N = len(roots)
        m = len(M)
        E = [0] * m
        F = [0] * m
        self.private = {}
        for a, b in I.R:      # a < b
            if a in idx and b in idx:
                z = N
                N += 1
                self.private[z] = (a, b)
                F[idx[a]] |= 1 << z
                E[idx[b]] |= 1 << z
            elif a in idx:    # a middle, b top
                F[idx[a]] |= 1 << nodeof[b]
            elif b in idx:    # a bottom, b middle
                E[idx[b]] |= 1 << nodeof[a]
        self.N, self.E, self.F = N, E, F
        self.s, self.t = nodeof[I.u], nodeof[I.v]
        self.le = [[I.le[M[i]][M[j]] for j in range(m)] for i in range(m)]
        self.m = m
        self.sides = [i for w in range(m) for i in (2 * w, 2 * w + 1) if self.mask(i)]
        self.sideset = set(self.sides)
        self.adj = {i: set() for i in self.sides}
        for a in range(len(self.sides)):
            for b in range(a + 1, len(self.sides)):
                x, y = self.sides[a], self.sides[b]
                if self.mask(x) & self.mask(y):
                    self.adj[x].add(y)
                    self.adj[y].add(x)
        self.Pi = {}
        for i in self.sides:
            w, ty = i >> 1, i & 1
            if ty == 0:     # E_w: F-sides of w' >= w
                fam = [2 * w2 + 1 for w2 in range(m) if self.le[w][w2]]
            else:           # F_w: E-sides of w' <= w
                fam = [2 * w2 for w2 in range(m) if self.le[w2][w]]
            self.Pi[i] = frozenset(x for x in fam if x in self.sideset)

    def mask(self, i):
        return self.F[i >> 1] if i & 1 else self.E[i >> 1]

    # ------------------------------------------------------------------------------------------------------------
    def is_valid_walk(self, walk):
        if not walk and self.s == self.t:
            return True
        if not walk or not (self.mask(walk[0]) >> self.s) & 1 or not (self.mask(walk[-1]) >> self.t) & 1:
            return False
        for a, b in zip(walk, walk[1:]):
            if a != b and not (self.mask(a) & self.mask(b)):
                return False
        used = set(walk)
        for x in used:
            if self.Pi[x] & used:
                return False
        return True

    def search(self, K, B, s, want_walk=False):
        Pi, adj, K = self.Pi, self.adj, frozenset(K)

        def step(Y, St, Dc, nd):
            if Y in Dc:
                return None
            if Pi[Y] & St:
                return None
            miss = Pi[Y] - K - Dc
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

        if self.s == self.t:
            return (True, ()) if want_walk else True
        q = deque()
        seen = set()
        e0 = frozenset()
        for i in self.sides:
            if (self.mask(i) >> self.s) & 1:
                r = step(i, e0, e0, 0)
                if r is None:
                    continue
                st = (i,) + r
                if st not in seen:
                    seen.add(st)
                    q.append((st, (i,)))
        while q:
            (cur, St, Dc, nd), walk = q.popleft()
            if (self.mask(cur) >> self.t) & 1:
                return (True, walk) if want_walk else True
            for j in adj[cur]:
                r = step(j, St, Dc, nd)
                if r is None:
                    continue
                st = (j,) + r
                if st not in seen:
                    seen.add(st)
                    q.append((st, walk + (j,) if want_walk else None))
        return (False, None) if want_walk else False

    def dom_sets(self, O):
        """Distinct sets N_O[Z] = sides of type O meeting Z or equal to Z (Z any side)."""
        out = {}
        for z in self.sides:
            fs = frozenset(i for i in self.sides if (i & 1) == O and (i == z or (self.mask(i) & self.mask(z))))
            if fs:
                out.setdefault(fs, z)
        return list(out.items())

    def decide(self, kd=1, ks=1, s=4, B=8, want_walk=False, stats=None):
        """K_E = union of <= kd sets N_F[Z] and <= ks single F-sides (it must contain the conflict families of the
        E-members), K_F likewise with E.  Sound for all parameters."""
        def unions(O):
            sets = self.dom_sets(O)
            singles = [i for i in self.sides if (i & 1) == O]
            out = {}
            for kk in range(0, kd + 1):
                for combo in itertools.combinations(sets, kk):
                    base = frozenset().union(*[c[0] for c in combo]) if combo else frozenset()
                    for j in range(0, ks + 1):
                        for sc in itertools.combinations(singles, j):
                            key = base | frozenset(sc)
                            out.setdefault(key, (tuple(c[1] for c in combo), sc))
            return list(out.items())
        UE = unions(1)
        UF = unions(0)
        tried = 0
        for KE, dE in UE:
            for KF, dF in UF:
                tried += 1
                r = self.search(KE | KF, B, s, True)
                if r[0]:
                    assert self.is_valid_walk(r[1]), "UNSOUND walk %s" % (r[1],)
                    if stats is not None:
                        stats["tried"] = tried
                    return (True, (dE, dF, r[1])) if want_walk else True
        if stats is not None:
            stats["tried"] = tried
        return (False, None) if want_walk else False

    def brute(self):
        """Order-consistent mode vectors connecting s and t (exponential)."""
        m = self.m
        out = []
        for mask in range(1 << m):
            ok = True
            for a in range(m):
                if (mask >> a) & 1:
                    for b in range(m):
                        if self.le[b][a] and not (mask >> b) & 1:
                            ok = False
                            break
                if not ok:
                    break
            if not ok:
                continue
            comp = 1 << self.s
            hyper = [self.F[w] if (mask >> w) & 1 else self.E[w] for w in range(m)]
            ch = True
            while ch:
                ch = False
                for h in hyper:
                    if h & comp and (h & ~comp):
                        comp |= h
                        ch = True
            if (comp >> self.t) & 1:
                out.append(mask)
        return out


# ----------------------------------------------------------------------------------------------------------------
# refined search (r4-general.md §6.2): forbid K - S, restrict to the sides reachable from s, watch only S
# ----------------------------------------------------------------------------------------------------------------

def reachable(G, allowed):
    """Sides of `allowed` reachable from the sides containing s in the side graph restricted to `allowed`."""
    start = [i for i in allowed if (G.mask(i) >> G.s) & 1]
    seen = set(start)
    stack = list(start)
    while stack:
        x = stack.pop()
        for y in G.adj[x]:
            if y in allowed and y not in seen:
                seen.add(y)
                stack.append(y)
    return seen


def search_refined(G, K, S, s, want_walk=False):
    """Walks inside R = reachable(all sides - (K - S)); conflict families restricted to R; K' = S stored.
    Sound for every K, S, s: every accepted walk is valid (Theorem 5' applied to the instance restricted to R)."""
    K, S = frozenset(K), frozenset(S)
    allowed = set(G.sides) - (K - S)
    R = reachable(G, allowed)
    Pi = {i: G.Pi[i] & R for i in R}
    Kp = S & R

    def step(Y, St, Dc, nd):
        if Y in Dc or Pi[Y] & St:
            return None
        miss = Pi[Y] - Kp - Dc
        if miss:
            if Y in Kp or nd >= s:
                return None
            Dc = Dc | miss
            nd += 1
        if Y in Kp and Y not in St:
            St = St | {Y}
        return St, Dc, nd

    if G.s == G.t:
        return (True, ()) if want_walk else True
    q = deque()
    seen = set()
    e0 = frozenset()
    for i in R:
        if (G.mask(i) >> G.s) & 1:
            r = step(i, e0, e0, 0)
            if r is not None:
                st = (i,) + r
                if st not in seen:
                    seen.add(st)
                    q.append((st, (i,)))
    while q:
        (cur, St, Dc, nd), walk = q.popleft()
        if (G.mask(cur) >> G.t) & 1:
            return (True, walk) if want_walk else True
        for j in G.adj[cur]:
            if j not in R:
                continue
            r = step(j, St, Dc, nd)
            if r is None:
                continue
            st = (j,) + r
            if st not in seen:
                seen.add(st)
                q.append((st, walk + (j,) if want_walk else None))
    return (False, None) if want_walk else False


def decide_refined(G, kd=1, ks=0, s=1, B=3, want_walk=False, stats=None):
    """K = K_E | K_F as in GSW.decide; S = any set of at most B sides of K (the members lying in K)."""
    def unions(O):
        sets = G.dom_sets(O)
        singles = [i for i in G.sides if (i & 1) == O]
        out = {}
        for kk in range(0, kd + 1):
            for combo in itertools.combinations(sets, kk):
                base = frozenset().union(*[c[0] for c in combo]) if combo else frozenset()
                for j in range(0, ks + 1):
                    for sc in itertools.combinations(singles, j):
                        out.setdefault(base | frozenset(sc), (tuple(c[1] for c in combo), sc))
        return list(out.items())
    UE, UF = unions(1), unions(0)
    tried = 0
    for KE, dE in UE:
        for KF, dF in UF:
            K = KE | KF
            Kl = sorted(K)
            for b in range(0, B + 1):
                for S in itertools.combinations(Kl, b):
                    tried += 1
                    r = search_refined(G, K, S, s, True)
                    if r[0]:
                        assert G.is_valid_walk(r[1]), "UNSOUND refined walk"
                        if stats is not None:
                            stats["tried"] = tried
                        return (True, (dE, dF, S, r[1])) if want_walk else True
    if stats is not None:
        stats["tried"] = tried
    return (False, None) if want_walk else False


# ----------------------------------------------------------------------------------------------------------------
# pruning by forced-exit propagation (r4-general.md §7.3): removes sides that no solution can pick.  Soundness of the
# search never depends on it (validity is checked on the walk's own sides); completeness needs only that every
# removed side is really unusable, which the refutation guarantees.
# ----------------------------------------------------------------------------------------------------------------

def _closure(G, fixed):
    """Order closure of a partial mode assignment (dict w -> 0 E / 1 F); None on contradiction."""
    fx = dict(fixed)
    stack = list(fx.items())
    while stack:
        w, mo = stack.pop()
        for w2 in range(G.m):
            if mo == 1 and G.le[w2][w] or mo == 0 and G.le[w][w2]:
                if w2 in fx:
                    if fx[w2] != mo:
                        return None
                else:
                    fx[w2] = mo
                    stack.append((w2, mo))
    return fx


def refutes(G, fixed, both_ends=True):
    """True if forced-exit propagation shows that no solution extends the partial assignment `fixed`."""
    fx = _closure(G, fixed)
    if fx is None:
        return True
    for start, goal in ((G.s, G.t), (G.t, G.s)) if both_ends else ((G.s, G.t),):
        f2 = dict(fx)
        C = 1 << start
        while True:
            if (C >> goal) & 1:
                break
            grew = False
            exits = []
            for w in range(G.m):
                for mo in (0, 1):
                    side = G.F[w] if mo else G.E[w]
                    if not side or not (side & C) or not (side & ~C):
                        continue
                    if w in f2:
                        if f2[w] == mo:
                            C |= side
                            grew = True
                    else:
                        exits.append((w, mo, side))
            if grew:
                continue
            if not exits:
                return True
            ws = {w for w, mo, side in exits}
            if len(exits) == 1 or (len(ws) == 1 and len(exits) == 1):
                w, mo, side = exits[0]
                f2[w] = mo
                f3 = _closure(G, f2)
                if f3 is None:
                    return True
                f2 = f3
                continue
            break
    return False


def prune(G, rounds=10):
    """Fixed modes implied by single-switch refutations, iterated; returns (fixed, dead sides)."""
    fixed = {}
    for _ in range(rounds):
        changed = False
        for w in range(G.m):
            if w in fixed:
                continue
            for mo in (0, 1):
                trial = dict(fixed)
                trial[w] = mo
                if refutes(G, trial):
                    other = 1 - mo
                    trial2 = dict(fixed)
                    trial2[w] = other
                    f3 = _closure(G, trial2)
                    if f3 is None:
                        return fixed, None          # no solution at all
                    fixed = f3
                    changed = True
                    break
        if not changed:
            break
    dead = set()
    for w, mo in fixed.items():
        dead.add(2 * w + (1 - mo))
    return fixed, dead & set(G.sides)


def pruned_copy(G, dead):
    """A shallow copy of G in which the dead sides are removed from the side set, the side graph and the conflict
    families (the walk can never use them)."""
    import copy
    H = copy.copy(G)
    H.sides = [i for i in G.sides if i not in dead]
    H.sideset = set(H.sides)
    H.adj = {i: {j for j in G.adj[i] if j not in dead} for i in H.sides}
    H.Pi = {i: frozenset(j for j in G.Pi[i] if j not in dead) for i in H.sides}
    return H


# ----------------------------------------------------------------------------------------------------------------
# Theorem R (r4-general.md §8): reduction to 2CH + P2 when the free switches are pairwise incomparable
# ----------------------------------------------------------------------------------------------------------------

def reduce_to_2ch(G, fixed):
    """Contract the picked sides of the fixed switches.  Returns (inst, free, reason): inst = (N, E, F, s, t) with bit
    masks over the contracted nodes (r4-switch/sw.py format) for the free switches, or None with the reason why
    the hypothesis of Theorem R fails ('comparable free switches' or 'P2 fails after contraction')."""
    free = [w for w in range(G.m) if w not in fixed]
    for i, a in enumerate(free):
        for b in free[i + 1:]:
            if G.le[a][b] or G.le[b][a]:
                return None, free, "comparable free switches %d, %d" % (a, b)
    par = list(range(G.N))

    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a
    for w, mo in fixed.items():
        side = G.F[w] if mo else G.E[w]
        bl = bits(side)
        for x in bl[1:]:
            ra, rb = find(bl[0]), find(x)
            if ra != rb:
                par[ra] = rb
    roots = {}
    for x in range(G.N):
        r = find(x)
        if r not in roots:
            roots[r] = len(roots)

    def remap(m):
        out = 0
        for x in bits(m):
            out |= 1 << roots[find(x)]
        return out
    E = [remap(G.E[w]) for w in free]
    F = [remap(G.F[w]) for w in free]
    inst = (len(roots), E, F, roots[find(G.s)], roots[find(G.t)])
    for i in range(len(free)):
        for j in range(i + 1, len(free)):
            if not (E[i] & E[j]) and not (F[i] & F[j]):
                return None, free, "P2 fails after contraction for %d, %d" % (free[i], free[j])
    return inst, free, "ok"


def free_comparability_cover(G, fixed):
    """A vertex cover (greedy, maximal matching based) of the comparability graph on the free switches."""
    free = [w for w in range(G.m) if w not in fixed]
    cover = []
    covered = set()
    for i, a in enumerate(free):
        for b in free[i + 1:]:
            if (G.le[a][b] or G.le[b][a]) and a not in covered and b not in covered:
                cover += [a, b]
                covered |= {a, b}
    return cover


def branches_R(G, fixed, cover):
    """Theorem R+: all order-consistent extensions of `fixed` by modes of the switches in `cover`; for each, the
    closure and the contraction of Theorem R.  Yields (fixing, inst or None, reason)."""
    import itertools as _it
    for modes in _it.product((0, 1), repeat=len(cover)):
        trial = dict(fixed)
        for w, mo in zip(cover, modes):
            trial[w] = mo
        f2 = _closure(G, trial)
        if f2 is None:
            continue
        inst, free, reason = reduce_to_2ch(G, f2)
        yield f2, inst, reason
