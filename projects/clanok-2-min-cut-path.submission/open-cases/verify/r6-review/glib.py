"""General switch form of ZZ + P2 (r4-general.md §5.1, r5-core.md), written from the definitions of the reports.

Instance: N nodes; terminals s, t (nodes); switches w = 0..m-1 with node masks E[w], F[w]; a preorder le on the
switches (closed here); middle edges (y, x, z): y < x and a private node z in F_y & E_x.
Modes: a down-set D of the preorder (D = F-mode); picked side F_w for w in D, E_w otherwise.
Yes iff s, t connected in the hypergraph of the picked sides.
Side id: 2w = E_w, 2w + 1 = F_w (exists iff non-empty).  Conflict pair {E_w, F_z} with w <= z.
P2: every incomparable pair has a common non-private node in E_x & E_y or F_x & F_y (bottom / top witness in the
realisation with one bottom-top pair per node), or a middle witness w < x, y with middle edges w-x, w-y, or
w > x, y with edges x-w, y-w.
"""
import itertools
import random
from collections import deque


def bits(x):
    i = 0
    while x:
        if x & 1:
            yield i
        x >>= 1
        i += 1


def popcount(x):
    return bin(x).count("1")


def close_preorder(m, rel):
    le = [[(i == j) or bool(rel[i][j]) for j in range(m)] for i in range(m)]
    for k in range(m):
        for i in range(m):
            if le[i][k]:
                for j in range(m):
                    if le[k][j]:
                        le[i][j] = True
    return le


class GInst:
    def __init__(self, N, E, F, le, s, t, medges=()):
        self.N, self.E, self.F, self.s, self.t = N, list(E), list(F), s, t
        self.m = m = len(E)
        self.le = close_preorder(m, le)
        self.medges = list(medges)
        self.private = 0
        for (y, x, z) in self.medges:
            self.private |= 1 << z
        self.up = [sum(1 << j for j in range(m) if self.le[i][j]) for i in range(m)]
        self.dn = [sum(1 << j for j in range(m) if self.le[j][i]) for i in range(m)]
        self.all = (1 << m) - 1
        self.sides = [i for w in range(m) for i in (2 * w, 2 * w + 1) if self.mask(i)]
        self.sideset = set(self.sides)
        self.adj = {i: [] for i in self.sides}
        for a, b in itertools.combinations(self.sides, 2):
            if self.mask(a) & self.mask(b):
                self.adj[a].append(b)
                self.adj[b].append(a)
        self.Pi = {}
        for i in self.sides:
            w = i >> 1
            if i & 1 == 0:
                fam = [2 * x + 1 for x in bits(self.up[w])]
            else:
                fam = [2 * x for x in bits(self.dn[w])]
            self.Pi[i] = frozenset(x for x in fam if x in self.sideset)
        self.Enon = sum(1 << w for w in range(m) if self.E[w])
        self.Fnon = sum(1 << w for w in range(m) if self.F[w])

    def mask(self, i):
        return self.F[i >> 1] if i & 1 else self.E[i >> 1]

    def lt(self, a, b):
        return self.le[a][b] and not self.le[b][a]

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

    def to_json(self):
        rel = [[1 if self.le[i][j] else 0 for j in range(self.m)] for i in range(self.m)]
        return {"N": self.N, "E": [sorted(bits(x)) for x in self.E], "F": [sorted(bits(x)) for x in self.F],
                "le": rel, "s": self.s, "t": self.t, "medges": self.medges}

    @staticmethod
    def from_json(d):
        E = [sum(1 << b for b in x) for x in d["E"]]
        F = [sum(1 << b for b in x) for x in d["F"]]
        return GInst(d["N"], E, F, d["le"], d["s"], d["t"], [tuple(e) for e in d.get("medges", [])])


# ----------------------------------------------------------------------------------------------------------------
def is_downset(G, D):
    for w in bits(D):
        if G.dn[w] & ~D:
            return False
    return True


def downsets(G):
    """all down-sets (bit masks)"""
    m = G.m
    out = []

    def rec(i, D, notD):
        if i == m:
            out.append(D)
            return
        # put i into D: all below must not be in notD
        if not (G.dn[i] & notD):
            rec(i + 1, D | (1 << i), notD)
        if not (G.up[i] & D):
            rec(i + 1, D, notD | (1 << i))

    rec(0, 0, 0)
    return out


def picked_masks(G, D):
    return [G.F[w] if (D >> w) & 1 else G.E[w] for w in range(G.m)]


def comp_from(G, start, sidemasks):
    C = 1 << start
    rest = [p for p in sidemasks if p]
    changed = True
    while changed:
        changed = False
        nr = []
        for p in rest:
            if p & C:
                if p & ~C:
                    C |= p
                    changed = True
            else:
                nr.append(p)
        rest = nr
    return C


def connects(G, D):
    if G.s == G.t:
        return True
    return bool((comp_from(G, G.s, picked_masks(G, D)) >> G.t) & 1)


def brute(G):
    return [D for D in downsets(G) if connects(G, D)]


def p2_violations(G):
    out = []
    npriv = ~G.private
    lowers = {}
    uppers = {}
    for (y, x, z) in G.medges:
        uppers.setdefault(y, set()).add(x)   # x is an upper middle neighbour of y
        lowers.setdefault(x, set()).add(y)
    for x, y in itertools.combinations(range(G.m), 2):
        if G.le[x][y] or G.le[y][x]:
            continue
        if (G.E[x] & G.E[y] & npriv) or (G.F[x] & G.F[y] & npriv):
            continue
        if lowers.get(x, set()) & lowers.get(y, set()):
            continue
        if uppers.get(x, set()) & uppers.get(y, set()):
            continue
        out.append((x, y))
    return out


def p2_ok(G):
    return not p2_violations(G)


def is_valid_walk(G, W):
    if G.s == G.t and not W:
        return True
    if not W or not (G.mask(W[0]) >> G.s) & 1 or not (G.mask(W[-1]) >> G.t) & 1:
        return False
    for a, b in zip(W, W[1:]):
        if a != b and not (G.mask(a) & G.mask(b)):
            return False
    used = set(W)
    for x in used:
        if G.Pi[x] & used:
            return False
    return True


def walk_state_ok(G, i, Up, Dn):
    """may side i be appended to a walk with up-closure Up of its E-members and down-closure Dn of its F-members?"""
    w = i >> 1
    if i & 1:
        return not ((Up >> w) & 1)       # F_w conflicts with E_z, z <= w  <=>  w in Up
    return not ((Dn >> w) & 1)           # E_w conflicts with F_z, w <= z  <=>  w in Dn


def add_state(G, i, Up, Dn):
    w = i >> 1
    if i & 1:
        return Up, Dn | G.dn[w]
    return Up | G.up[w], Dn


def shortest_len(G):
    if G.s == G.t:
        return 0
    q = deque()
    seen = set()
    for i in G.sides:
        if (G.mask(i) >> G.s) & 1 and walk_state_ok(G, i, 0, 0):
            Up, Dn = add_state(G, i, 0, 0)
            if Up & Dn:
                continue
            st = (i, Up, Dn)
            if st not in seen:
                seen.add(st)
                q.append((st, 1))
    while q:
        (i, Up, Dn), d = q.popleft()
        if (G.mask(i) >> G.t) & 1:
            return d
        for j in G.adj[i]:
            if not walk_state_ok(G, j, Up, Dn):
                continue
            U2, D2 = add_state(G, j, Up, Dn)
            if U2 & D2:
                continue
            st = (j, U2, D2)
            if st not in seen:
                seen.add(st)
                q.append((st, d + 1))
    return None


def all_shortest(G, cap=10 ** 5):
    L = shortest_len(G)
    if not L:
        return []
    dist = {i: None for i in G.sides}
    q = deque()
    for i in G.sides:
        if (G.mask(i) >> G.t) & 1:
            dist[i] = 1
            q.append(i)
    while q:
        i = q.popleft()
        for j in G.adj[i]:
            if dist[j] is None:
                dist[j] = dist[i] + 1
                q.append(j)
    out = []

    def rec(path, Up, Dn):
        if len(out) >= cap:
            return
        i = path[-1]
        if len(path) == L:
            if (G.mask(i) >> G.t) & 1:
                out.append(tuple(path))
            return
        for j in G.adj[i]:
            if dist[j] is None or len(path) + dist[j] > L or j in path:
                continue
            if not walk_state_ok(G, j, Up, Dn):
                continue
            U2, D2 = add_state(G, j, Up, Dn)
            if U2 & D2:
                continue
            path.append(j)
            rec(path, U2, D2)
            path.pop()

    for i in G.sides:
        if (G.mask(i) >> G.s) & 1 and dist[i] is not None and dist[i] <= L and walk_state_ok(G, i, 0, 0):
            Up, Dn = add_state(G, i, 0, 0)
            if not (Up & Dn):
                rec([i], Up, Dn)
    return out


# ----------------------------------------------------------------------------------------------------------------
# forced-exit propagation and pruning (r4-general §7.3, with the stopping repair of verify/r5-review.md §3.3)
def closure(G, fixed):
    """fixed: dict w -> 0 (E) / 1 (F); order closure or None on contradiction"""
    fx = dict(fixed)
    stack = list(fx.items())
    while stack:
        w, mo = stack.pop()
        S = G.dn[w] if mo == 1 else G.up[w]
        for w2 in bits(S):
            if w2 in fx:
                if fx[w2] != mo:
                    return None
            else:
                fx[w2] = mo
                stack.append((w2, mo))
    return fx


def refutes(G, fixed, alive=None):
    """forced-exit propagation from s and (separately) from t; True = no solution extends `fixed`.
    alive: optional set of side ids that may be used (default: all)."""
    fx = closure(G, fixed)
    if fx is None:
        return True
    for start, goal in ((G.s, G.t), (G.t, G.s)):
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
                    if alive is not None and (2 * w + mo) not in alive:
                        continue
                    if w in f2:
                        if f2[w] == mo:
                            C |= side
                            grew = True
                    else:
                        exits.append((w, mo))
            if grew:
                continue
            if not exits:
                return True
            if len(exits) == 1:
                w, mo = exits[0]
                f2[w] = mo
                f3 = closure(G, f2)
                if f3 is None:
                    return True
                f2 = f3
                continue
            break
    return False


def prune(G, rounds=50):
    """returns (fixed dict, dead side set) or (fixed, None) if both modes of a switch are refuted"""
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
                    trial2 = dict(fixed)
                    trial2[w] = 1 - mo
                    f3 = closure(G, trial2)
                    if f3 is None:
                        return fixed, None
                    fixed = f3
                    changed = True
                    break
        if not changed:
            break
    dead = {2 * w + (1 - mo) for w, mo in fixed.items()} & G.sideset
    return fixed, dead


# ----------------------------------------------------------------------------------------------------------------
# Theorem 5' search with conflict families and declarations; refined search (r4-general §5.1, §6.2)
def search5(G, K, B, s, allowed=None, KS=None, want_walk=False):
    """allowed: set of usable sides (default all); conflict families restricted to `allowed`.
    KS: the set used as K in the rules (default K).  Storage bound B applies to members in KS."""
    if allowed is None:
        allowed = G.sideset
    Kp = frozenset(KS if KS is not None else K)
    Pi = {i: G.Pi[i] & allowed for i in allowed}

    def step(Y, St, Dc, nd):
        if Y in Dc or (Pi[Y] & St):
            return None
        miss = Pi[Y] - Kp - Dc
        if miss:
            if Y in Kp or nd >= s:
                return None
            Dc = Dc | miss
            nd += 1
        if Y in Kp and Y not in St:
            if len(St) >= B:
                return None
            St = St | {Y}
        return St, Dc, nd

    if G.s == G.t:
        return (True, ()) if want_walk else True
    q = deque()
    seen = set()
    e0 = frozenset()
    for i in allowed:
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
            if j not in allowed:
                continue
            r = step(j, St, Dc, nd)
            if r is None:
                continue
            st = (j,) + r
            if st not in seen:
                seen.add(st)
                q.append((st, walk + (j,) if want_walk else None))
    return (False, None) if want_walk else False


def reach_from_s(G, allowed):
    start = [i for i in allowed if (G.mask(i) >> G.s) & 1]
    seen = set(start)
    st = list(start)
    while st:
        x = st.pop()
        for y in G.adj[x]:
            if y in allowed and y not in seen:
                seen.add(y)
                st.append(y)
    return seen


def search_refined(G, K, S, s, base_allowed=None, want_walk=False):
    K, S = frozenset(K), frozenset(S)
    allowed = set(base_allowed if base_allowed is not None else G.sideset) - (K - S)
    R = reach_from_s(G, allowed)
    return search5(G, S & R, len(S), s, allowed=R, KS=S & R, want_walk=want_walk)


def dom_sets(G, O, allowed=None):
    """distinct sets N_O[Z] = sides of type O meeting Z (Z any side), restricted to allowed"""
    allowed = G.sideset if allowed is None else allowed
    out = {}
    for z in allowed:
        fs = frozenset(i for i in allowed if (i & 1) == O and (G.mask(i) & G.mask(z)))
        if fs:
            out.setdefault(fs, z)
    return list(out.items())


def unions(G, O, kd, ks, allowed=None):
    allowed = G.sideset if allowed is None else allowed
    sets = dom_sets(G, O, allowed)
    singles = sorted(i for i in allowed if (i & 1) == O)
    out = {}
    for kk in range(kd + 1):
        for combo in itertools.combinations(sets, kk):
            base = frozenset().union(*[c[0] for c in combo]) if combo else frozenset()
            for j in range(ks + 1):
                for sc in itertools.combinations(singles, j):
                    out.setdefault(base | frozenset(sc), (tuple(c[1] for c in combo), sc))
    return list(out.items())


def hyb(G, kd, ks, s, B, refined=False, want=False):
    """HYB: prune, delete dead sides, run the search of Theorem 5' (or the refined search) for every K_E, K_F"""
    fixed, dead = prune(G)
    if dead is None:
        return False
    allowed = G.sideset - dead
    UE = unions(G, 1, kd, ks, allowed)
    UF = unions(G, 0, kd, ks, allowed)
    for KE, dE in UE:
        for KF, dF in UF:
            K = KE | KF
            if not refined:
                r = search5(G, K, B, s, allowed=allowed, want_walk=True)
                if r[0]:
                    assert is_valid_walk(G, r[1])
                    return (True, (dE, dF, r[1])) if want else True
            else:
                Kl = sorted(K)
                for b in range(B + 1):
                    for S in itertools.combinations(Kl, b):
                        r = search_refined(G, K, S, s, base_allowed=allowed, want_walk=True)
                        if r[0]:
                            assert is_valid_walk(G, r[1])
                            return (True, (dE, dF, S, r[1])) if want else True
    return (False, None) if want else False


# ----------------------------------------------------------------------------------------------------------------
# CDESC (r5-core §3.1) and ADESC (§5.1)
def NE(G, Zmask):
    return sum(1 << w for w in range(G.m) if G.E[w] and (G.E[w] & Zmask))


def NF(G, Zmask):
    return sum(1 << w for w in range(G.m) if G.F[w] and (G.F[w] & Zmask))


def e_desc(G, U, Phi):
    Gen = (G.Enon & ~U) ^ Phi
    return G.all & ~G.upc(Gen)


def f_desc(G, U, Phi):
    Gen = (G.Fnon & ~U) ^ Phi
    return G.dnc(Gen)


def cdesc(G, f, e, want=False):
    """CDESC(f, e): both kinds, every choice of <= f centres (sides and single nodes), every Phi of <= e switches"""
    cents = sorted({G.mask(i) for i in G.sides} | {1 << z for z in range(G.N)})
    for kind in (0, 1):
        Us = set()
        for a in range(f + 1):
            for comb in itertools.combinations(cents, a):
                Z = 0
                for c in comb:
                    Z |= c
                U = NE(G, Z) if kind == 0 else NF(G, Z)
                if U in Us:
                    continue
                Us.add(U)
                for ee in range(e + 1):
                    for Ph in itertools.combinations(range(G.m), ee):
                        Phi = sum(1 << w for w in Ph)
                        D = e_desc(G, U, Phi) if kind == 0 else f_desc(G, U, Phi)
                        if connects(G, D):
                            return (True, (kind, comb, Ph, D)) if want else True
    return (False, None) if want else False


def contract_map(G, sidemasks):
    """union-find on nodes: the nodes of each mask in sidemasks are identified (transitively).  Returns root map."""
    par = list(range(G.N))

    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a
    for msk in sidemasks:
        bl = list(bits(msk))
        for z in bl[1:]:
            ra, rb = find(bl[0]), find(z)
            if ra != rb:
                par[ra] = rb
    return [find(z) for z in range(G.N)]


def cmask(G, root, msk):
    r = 0
    for z in bits(msk):
        r |= 1 << root[z]
    return r


def anchored_e(G, B0, A0, U, Phi):
    """anchored E-description: G = ((Enon - U) - dn(B0)) ^ Phi, G |= A0, D = Q - up(G); None if skipped"""
    dB = G.dnc(B0)
    Gen = ((G.Enon & ~U) & ~dB) ^ Phi
    Gen |= A0
    if (Gen & dB) or (dB & G.upc(A0)):
        return None
    return G.all & ~G.upc(Gen)


def anchored_f(G, A0, B0, U, Phi):
    """anchored F-description (dual): G' = ((Fnon - U') - up(A0)) ^ Phi, G' |= B0, D = dn(G')"""
    uA = G.upc(A0)
    Gen = ((G.Fnon & ~U) & ~uA) ^ Phi
    Gen |= B0
    if (Gen & uA) or (uA & G.dnc(B0)):
        return None
    return G.dnc(Gen)


# ----------------------------------------------------------------------------------------------------------------
def to_zz(G):
    """realisation as a ZZ instance: u = bottom of node s, v = top of node t; one bottom-top pair per non-private
    node.  Returns dict with elements, order (list of pairs a <= b generating), R edges."""
    els = []
    idx = {}
    for z in range(G.N):
        if (G.private >> z) & 1:
            continue
        idx[("b", z)] = len(els)
        els.append(("b", z))
        idx[("t", z)] = len(els)
        els.append(("t", z))
    for w in range(G.m):
        idx[("m", w)] = len(els)
        els.append(("m", w))
    R = []
    for z in range(G.N):
        if (G.private >> z) & 1:
            continue
        R.append((idx[("b", z)], idx[("t", z)]))
    for w in range(G.m):
        for z in bits(G.E[w] & ~G.private):
            R.append((idx[("b", z)], idx[("m", w)]))
        for z in bits(G.F[w] & ~G.private):
            R.append((idx[("m", w)], idx[("t", z)]))
    for (y, x, z) in G.medges:
        R.append((idx[("m", y)], idx[("m", x)]))
    order = [[idx[("m", i)], idx[("m", j)]] for i in range(G.m) for j in range(G.m) if i != j and G.le[i][j]]
    return {"elements": ["%s%d" % e for e in els], "bottoms": [idx[("b", z)] for z in range(G.N) if ("b", z) in idx],
            "tops": [idx[("t", z)] for z in range(G.N) if ("t", z) in idx], "middle_order_le": order,
            "R": R, "u": idx[("b", G.s)], "v": idx[("t", G.t)],
            "note": "bottoms are all tied with u, tops with v, bottoms < middle < tops; R edges (a, b) have a < b"}
