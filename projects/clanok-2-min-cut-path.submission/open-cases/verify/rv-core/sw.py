"""Reviewer's own implementation of the general switch form (rv-core, round 5).

Written from the definitions of r4-general.md Section 5.1 and r5-core.md Sections 2, 3, 5; no code of other agents.

Instance: nodes 0..N-1 (bitmasks), terminals s, t (nodes); switches 0..m-1 with node sets E[w], F[w] and a
preorder `le` (le[a] = bitmask of b with a <= b, reflexive and transitive).  Modes: a down-set D of switches
(F-mode = in D).  Picked side of w: F[w] if w in D else E[w].  Yes iff s, t connected in the hypergraph of the picked
sides.  Middle edges: triples (y, x, node) with y < x and a private node in F[y] & E[x].
Sides are numbered 2w (E-side of w) and 2w+1 (F-side of w).
Conflict pair: {E_w, F_z} with w <= z.  Valid walk: consecutive sides meet (or are equal), s in the first, t in the
last, no conflict pair among its sides.
"""
import itertools
from collections import deque


def bits(x):
    while x:
        b = x & -x
        yield b.bit_length() - 1
        x ^= b


def pc(x):
    return bin(x).count("1")


class SW:
    def __init__(self, N, s, t, E, F, rel=(), medges=(), names=None, nodenames=None):
        self.N, self.s, self.t = N, s, t
        self.E, self.F = list(E), list(F)
        self.m = m = len(self.E)
        le = [1 << i for i in range(m)]
        for a, b in rel:
            le[a] |= 1 << b
        # transitive closure
        changed = True
        while changed:
            changed = False
            for a in range(m):
                x = le[a]
                y = x
                for b in bits(x):
                    y |= le[b]
                if y != x:
                    le[a] = y
                    changed = True
        self.le = le                       # le[a]: all b >= a  (up-set of a)
        self.up = le
        self.dn = [0] * m
        for a in range(m):
            for b in bits(le[a]):
                self.dn[b] |= 1 << a
        self.medges = list(medges)
        self.names = names or ["w%d" % i for i in range(m)]
        self.nodenames = nodenames
        self.side = [self.E[i // 2] if i % 2 == 0 else self.F[i // 2] for i in range(2 * m)]

    # ---------------- order ----------------
    def leq(self, a, b):
        return bool(self.le[a] >> b & 1)

    def incomparable(self, a, b):
        return not self.leq(a, b) and not self.leq(b, a)

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

    def strict_lt(self, a, b):
        return self.leq(a, b) and not self.leq(b, a)

    # ---------------- P2 ----------------
    def p2_violations(self):
        bad = []
        low = {}
        upp = {}
        for (y, x, nd) in self.medges:
            upp.setdefault(y, set()).add(x)    # x is an upper R-neighbour of y
            low.setdefault(x, set()).add(y)    # y is a lower R-neighbour of x
        for a in range(self.m):
            for b in range(a + 1, self.m):
                if not self.incomparable(a, b):
                    continue
                if self.E[a] & self.E[b] or self.F[a] & self.F[b]:
                    continue
                ok = False
                for w in low.get(a, ()):       # lower middle witness w < a, b with edges w-a, w-b
                    if w in low.get(b, ()) and self.strict_lt(w, a) and self.strict_lt(w, b):
                        ok = True
                for w in upp.get(a, ()):
                    if w in upp.get(b, ()) and self.strict_lt(a, w) and self.strict_lt(b, w):
                        ok = True
                if not ok:
                    bad.append((a, b))
        return bad

    # ---------------- modes ----------------
    def downsets(self):
        m = self.m
        order = list(range(m))
        out = []

        def rec(i, D, X):
            if i == m:
                out.append(D)
                return
            w = order[i]
            if (D >> w) & 1 or (X >> w) & 1:
                rec(i + 1, D, X)
                return
            # w in D: needs dn[w] disjoint from X
            if not (self.dn[w] & X):
                rec(i + 1, D | self.dn[w], X)
            if not (self.up[w] & D):
                rec(i + 1, D, X | self.up[w])
        rec(0, 0, 0)
        return out

    def picked(self, D):
        return [self.F[w] if (D >> w) & 1 else self.E[w] for w in range(self.m)]

    def picked_sides(self, D):
        return [2 * w + ((D >> w) & 1) for w in range(self.m)]

    def connects(self, D):
        return self.connects_sides(self.picked(D))

    def connects_sides(self, sets):
        s, t = self.s, self.t
        if s == t:
            return True
        comp = 1 << s
        rest = [x for x in sets if x]
        changed = True
        while changed:
            changed = False
            nxt = []
            for x in rest:
                if x & comp:
                    comp |= x
                    changed = True
                else:
                    nxt.append(x)
            rest = nxt
            if comp >> t & 1:
                return True
        return bool(comp >> t & 1)

    def solutions(self):
        return [D for D in self.downsets() if self.connects(D)]

    # ---------------- walks and paths ----------------
    def conflict(self, i, j):
        """sides i, j form a conflict pair"""
        wi, ti = divmod(i, 2)
        wj, tj = divmod(j, 2)
        if ti == tj:
            return False
        if ti == 0:   # E_wi, F_wj
            return self.leq(wi, wj)
        return self.leq(wj, wi)

    def is_valid_walk(self, W):
        if not W or not (self.side[W[0]] >> self.s & 1) or not (self.side[W[-1]] >> self.t & 1):
            return False
        for a, b in zip(W, W[1:]):
            if a != b and not (self.side[a] & self.side[b]):
                return False
        S = sorted(set(W))
        for i in range(len(S)):
            for j in range(i + 1, len(S)):
                if self.conflict(S[i], S[j]):
                    return False
        return True

    def shortest_paths_for(self, D):
        """all shortest s-t side paths in the hypergraph of the picked sides of D (list of tuples), or []"""
        sides = [i for i in self.picked_sides(D) if self.side[i]]
        st = [i for i in sides if self.side[i] >> self.s & 1]
        if not st:
            return []
        dist = {i: 1 for i in st}
        q = deque(st)
        while q:
            a = q.popleft()
            for b in sides:
                if b not in dist and self.side[a] & self.side[b]:
                    dist[b] = dist[a] + 1
                    q.append(b)
        ends = [i for i in sides if i in dist and self.side[i] >> self.t & 1]
        if not ends:
            return []
        L = min(dist[i] for i in ends)
        res = []

        def back(path):
            a = path[-1]
            if dist[a] == 1:
                res.append(tuple(reversed(path)))
                return
            for b in sides:
                if dist.get(b) == dist[a] - 1 and self.side[a] & self.side[b]:
                    back(path + [b])
        for e in ends:
            if dist[e] == L:
                back([e])
        return res

    def shortest_valid_paths(self):
        best = None
        allp = set()
        for D in self.solutions():
            ps = self.shortest_paths_for(D)
            if not ps:
                continue
            L = len(ps[0])
            if best is None or L < best:
                best = L
                allp = set(ps)
            elif L == best:
                allp |= set(ps)
        return best, sorted(allp)


# ---------------- path data (r5-core 3.2, 5.1) ----------------
def path_data(G, P):
    WE = WF = 0
    pos = {}
    for i, sd in enumerate(P):
        w, ty = divmod(sd, 2)
        pos[w] = i + 1
        if ty == 0:
            WE |= 1 << w
        else:
            WF |= 1 << w
    Up = G.upc(WE)
    L = G.dnc(WF)
    A = 0
    for a in bits(WE):
        # no E-member strictly below a
        if not any(G.strict_lt(b, a) for b in bits(WE)):
            A |= 1 << a
    B = 0
    for b in bits(WF):
        if not any(G.strict_lt(b, c) for c in bits(WF)):
            B |= 1 << b
    return dict(WE=WE, WF=WF, Up=Up, L=L, A=A, B=B, pos=pos)


def enon(G):
    return sum(1 << w for w in range(G.m) if G.E[w])


def fnon(G):
    return sum(1 << w for w in range(G.m) if G.F[w])


def NE(G, Z, Esets=None):
    Es = Esets if Esets is not None else G.E
    return sum(1 << w for w in range(G.m) if Es[w] and Es[w] & Z)


def NF(G, Z, Fsets=None):
    Fs = Fsets if Fsets is not None else G.F
    return sum(1 << w for w in range(G.m) if Fs[w] and Fs[w] & Z)


def describe(G, kind, B0=0, A0=0, U=0, Phi=0):
    """anchored description of r5-core 5.1 (CDESC = no anchors). Returns the down-set D or None if skipped."""
    full = (1 << G.m) - 1
    dB, uA = G.dnc(B0), G.upc(A0)
    if dB & uA:
        return None
    if kind == "E":
        g = ((enon(G) & ~U) & ~dB) ^ Phi
        g |= A0
        if g & dB:
            return None
        return full & ~G.upc(g)
    g = ((fnon(G) & ~U) & ~uA) ^ Phi
    g |= B0
    if g & uA:
        return None
    return G.dnc(g)


def contracted_sets(G, merge_sides):
    """identify all nodes of each node set in merge_sides (union-find over nodes); return (E', F') as bitmasks over
    class representatives"""
    par = list(range(G.N))

    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a
    for S in merge_sides:
        el = list(bits(S))
        for x in el[1:]:
            ra, rb = find(el[0]), find(x)
            if ra != rb:
                par[rb] = ra

    def mp(S):
        r = 0
        for x in bits(S):
            r |= 1 << find(x)
        return r
    return [mp(x) for x in G.E], [mp(x) for x in G.F], mp


# ---------------- forced-exit propagation (r4-general 7.3, with the repair of verify/r5-review.md) -------------
def closure_fix(G, fixed):
    """fixed: dict w -> 'E'/'F'. Close under order; return None on contradiction."""
    fx = dict(fixed)
    changed = True
    while changed:
        changed = False
        for w, mo in list(fx.items()):
            S = G.dn[w] if mo == "F" else G.up[w]
            for v in bits(S):
                if v not in fx:
                    fx[v] = mo
                    changed = True
                elif fx[v] != mo:
                    return None
    return fx


def refutes(G, fixed, stop_at_other=True):
    fx = closure_fix(G, fixed)
    if fx is None:
        return True
    while True:
        progress = False
        for term, other in ((G.s, G.t), (G.t, G.s)):
            comp = 1 << term
            fsides = [G.F[w] if mo == "F" else G.E[w] for w, mo in fx.items()]
            ch = True
            while ch:
                ch = False
                for x in fsides:
                    if x & comp and x & ~comp:
                        comp |= x
                        ch = True
            if stop_at_other and comp >> other & 1:
                continue
            exits = []
            for w in range(G.m):
                if w in fx:
                    continue
                for mo, x in (("E", G.E[w]), ("F", G.F[w])):
                    if x & comp and x & ~comp:
                        exits.append((w, mo))
            if not exits:
                if comp >> other & 1:
                    continue
                return True
            if len(exits) == 1:
                w, mo = exits[0]
                fx2 = dict(fx)
                fx2[w] = mo
                fx2 = closure_fix(G, fx2)
                if fx2 is None:
                    return True
                fx = fx2
                progress = True
                break
        if not progress:
            return False


def prune(G, stop_at_other=True, rounds=50):
    fixed = {}
    for _ in range(rounds):
        changed = False
        for w in range(G.m):
            if w in fixed:
                continue
            for mo in ("E", "F"):
                if w in fixed:
                    break
                trial = dict(fixed)
                trial[w] = mo
                if refutes(G, trial, stop_at_other):
                    other = "F" if mo == "E" else "E"
                    f2 = dict(fixed)
                    f2[w] = other
                    f2 = closure_fix(G, f2)
                    if f2 is None:
                        return None     # no solution
                    fixed = f2
                    changed = True
        if not changed:
            break
    return fixed


# ---------------- search of Theorem 5' (r4-general 5.1) ----------------
def conflict_family(G, i, allowed=None):
    w, ty = divmod(i, 2)
    if ty == 0:
        fam = [2 * v + 1 for v in bits(G.up[w])]
    else:
        fam = [2 * v for v in bits(G.dn[w])]
    if allowed is not None:
        fam = [x for x in fam if x in allowed]
    return frozenset(fam)


def search5(G, K, B, s, alive=None, want=False):
    """Theorem 5' search. K: set of side ids; B: storage bound; s: declaration bound; alive: set of usable sides
    (default all non-empty sides).  Returns an accepted walk (want) or True/False."""
    if alive is None:
        alive = set(i for i in range(2 * G.m) if G.side[i])
    alive = set(alive)
    Pi = {i: conflict_family(G, i, alive) for i in alive}
    nb = {i: [j for j in alive if j == i or G.side[i] & G.side[j]] for i in alive}
    K = frozenset(K)

    def app(Y, St, Dc, nd):
        if Y in Dc:
            return None
        if Pi[Y] & St:
            return None
        if Pi[Y] <= (K | Dc):
            Dc2, nd2 = Dc, nd
        elif Y not in K and nd < s:
            Dc2, nd2 = Dc | (Pi[Y] - K - Dc), nd + 1
        else:
            return None
        St2 = St | {Y} if Y in K else St
        if len(St2) > B:
            return None
        return (Y, St2, Dc2, nd2)

    start = []
    for Y in alive:
        if G.side[Y] >> G.s & 1:
            st = app(Y, frozenset(), frozenset(), 0)
            if st:
                start.append(st)
    seen = set(start)
    par = {x: None for x in start}
    q = deque(start)
    while q:
        cur = q.popleft()
        Y, St, Dc, nd = cur
        if G.side[Y] >> G.t & 1:
            if not want:
                return True
            W = []
            x = cur
            while x is not None:
                W.append(x[0])
                x = par[x]
            return list(reversed(W))
        for Z in nb[Y]:
            nxt = app(Z, St, Dc, nd)
            if nxt and nxt not in seen:
                seen.add(nxt)
                par[nxt] = cur
                q.append(nxt)
    return None if want else False


def nbhd(G, Z, typ, alive):
    """N_typ[Z]: sides of type typ (0 = E, 1 = F) meeting the node set Z (among alive sides)"""
    return frozenset(i for i in alive if i % 2 == typ and G.side[i] & Z)


def cert_families(G, typ, kd, ks, alive):
    """all unions of <= kd sets N_typ[Z] (Z alive side) and <= ks single sides of type typ"""
    nbs = sorted(set(nbhd(G, G.side[z], typ, alive) for z in alive), key=lambda x: sorted(x))
    singles = sorted(i for i in alive if i % 2 == typ)
    out = set()
    for a in range(kd + 1):
        for cd in itertools.combinations(nbs, a):
            base = frozenset().union(*cd) if cd else frozenset()
            for b in range(ks + 1):
                for cs in itertools.combinations(singles, b):
                    out.add(base | frozenset(cs))
    return sorted(out, key=lambda x: (len(x), sorted(x)))


def hyb(G, kd, ks, s, B, refined=False, fixed=None, want=False):
    """HYB: prune, delete the wrong sides of fixed switches, run the search over all K = K_E | K_F.
    refined: the refined search of r4-general 6.2 (guess S <= K, |S| <= B; delete K - S; restrict to the sides
    reachable from s; search with K' = S)."""
    if fixed is None:
        fixed = prune(G)
    if fixed is None:
        return False
    alive = set()
    for i in range(2 * G.m):
        w, ty = divmod(i, 2)
        if not G.side[i]:
            continue
        if w in fixed and fixed[w] != "EF"[ty]:
            continue
        alive.add(i)
    KE = cert_families(G, 1, kd, ks, alive)
    KF = cert_families(G, 0, kd, ks, alive)
    for ke in KE:
        for kf in KF:
            K = ke | kf
            if not refined:
                r = search5(G, K, B, s, alive, want)
                if r:
                    return (K, r) if want else True
            else:
                for b in range(B + 1):
                    for S in itertools.combinations(sorted(K), b):
                        S = frozenset(S)
                        rem = alive - (K - S)
                        R = reachable(G, rem)
                        r = search5(G, S & R, B, s, R, want)
                        if r:
                            return (K, S, r) if want else True
    return False


def reachable(G, rem):
    st = [i for i in rem if G.side[i] >> G.s & 1]
    seen = set(st)
    q = deque(st)
    while q:
        a = q.popleft()
        for b in rem:
            if b not in seen and G.side[a] & G.side[b]:
                seen.add(b)
                q.append(b)
    return seen
