"""Referee qp-referee (round 6c): own library for spot checks of qp-proof.md.

Written from the definitions of qp-proof.md only; no code of other folders is imported here.
Sets of vertices / elements / switches / nodes are Python ints used as bit masks.

Contents
  graphs:  cut values by brute force, bridges, distances, cp from Definition 1.1 (independent of Lemma 1.3(c))
  Section 2: K, Q, ears, H, preorder of Definition 2.5, R, ZZ answer; checks of Lemmas 2.1-2.8, Theorem 2.9
  Section 3: Construction 3.1, checks of Lemma 3.2, Lemma 3.3 (per down-set), Lemma 3.4
  Section 4: objects of Definition 4.1, shortest valid paths, Lemmas 4.2(e), 4.3 (j = 1, 2), 4.4, 4.5
  Section 5: Lemma 5.2 by the proof's construction (LP for the game, derandomised by conditional expectations),
             Theorem 5.3 (levels), and an exact IDESC (Definition 6.1) for small m
"""
import math
from collections import deque
from itertools import combinations


def bits(x):
    out = []
    while x:
        b = x & -x
        out.append(b.bit_length() - 1)
        x ^= b
    return out


def pc(x):
    return bin(x).count("1")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


# =====================================================================================================================
# graphs
# =====================================================================================================================

class G:
    def __init__(self, n, edges, vmask=None):
        self.n = n
        self.edges = sorted({(min(a, b), max(a, b)) for a, b in edges if a != b})
        self.vmask = (1 << n) - 1 if vmask is None else vmask
        self.adj = [0] * n
        for a, b in self.edges:
            self.adj[a] |= 1 << b
            self.adj[b] |= 1 << a

    def delta(self, S):
        return sum(1 for a, b in self.edges if ((S >> a) & 1) != ((S >> b) & 1))

    def delta_edges(self, S):
        return [(a, b) for a, b in self.edges if ((S >> a) & 1) != ((S >> b) & 1)]

    def comp(self, x, emask_edges=None):
        """vertex mask of the component of x (in the subgraph of the given edge list, default all edges)"""
        if emask_edges is None:
            adj = self.adj
        else:
            adj = [0] * self.n
            for a, b in emask_edges:
                adj[a] |= 1 << b
                adj[b] |= 1 << a
        seen = 1 << x
        st = [x]
        while st:
            a = st.pop()
            nb = adj[a] & ~seen
            seen |= nb
            st.extend(bits(nb))
        return seen

    def dist(self, x):
        d = [-1] * self.n
        d[x] = 0
        dq = deque([x])
        while dq:
            a = dq.popleft()
            for b in bits(self.adj[a]):
                if d[b] < 0:
                    d[b] = d[a] + 1
                    dq.append(b)
        return d

    def cutvals(self):
        """|delta(S)| for every S within vmask (dict); brute force"""
        vs = bits(self.vmask)
        out = {}
        for r in range(1 << len(vs)):
            S = 0
            for i, x in enumerate(vs):
                if (r >> i) & 1:
                    S |= 1 << x
            out[S] = self.delta(S)
        return out


def cvals_all(g):
    """c(x, y) for all ordered pairs of vertices of g (within vmask), by brute force: least |delta(S)| over S with
    x in S, y not in S (every cut contains such a delta(S): elementary).  Vertices outside vmask are isolated in g,
    so subsets of all n vertices may be used."""
    import numpy as np
    n = g.n
    S = np.arange(1 << n, dtype=np.int64)
    dl = np.zeros(1 << n, dtype=np.int64)
    for a, b in g.edges:
        dl += ((S >> a) & 1) ^ ((S >> b) & 1)
    memb = [((S >> x) & 1).astype(bool) for x in range(n)]
    vs = bits(g.vmask)
    c = {}
    for x in vs:
        for y in vs:
            if x != y:
                c[(x, y)] = int(dl[memb[x] & ~memb[y]].min())
    cv = {}
    for Sv in range(1 << n):
        if Sv & ~g.vmask == 0:
            cv[Sv] = int(dl[Sv])
    return c, cv


def bridges(g):
    out = []
    for e in g.edges:
        rest = [f for f in g.edges if f != e]
        if not (g.comp(e[0], rest) >> e[1]) & 1:
            out.append(e)
    return out


def cp_bruteforce(g, u, v, cv=None):
    """cp(u, v) from Definition 1.1: least |E(P) u C| over u-v paths P and u-v cuts C.  A cut C contains delta(S)
    for S = component of u in G - C, so the least value is min over S (u in S, v not in S) of
    |delta(S)| + (least number of edges outside delta(S) on a u-v path), the latter by 0-1 BFS."""
    if cv is None:
        cv = g.cutvals()
    best = None
    n = g.n
    for S, val in cv.items():
        if not (S >> u) & 1 or (S >> v) & 1:
            continue
        # 0-1 BFS: weight 0 on edges of delta(S)
        INF = 10 ** 9
        d = [INF] * n
        d[u] = 0
        dq = deque([u])
        while dq:
            a = dq.popleft()
            for b in bits(g.adj[a]):
                w = 0 if ((S >> a) & 1) != ((S >> b) & 1) else 1
                if d[a] + w < d[b]:
                    d[b] = d[a] + w
                    if w == 0:
                        dq.appendleft(b)
                    else:
                        dq.append(b)
        tot = val + d[v]
        if best is None or tot < best:
            best = tot
    return best


# =====================================================================================================================
# Section 2: graph -> ZZ
# =====================================================================================================================

class ZZ:
    """(Q, <=, R, u, v) on elements 0..q-1; le[a] = mask of b with a <= b; R = set of pairs (a, b) with a < b."""

    def __init__(self, q, le, R, u, v):
        self.q, self.le, self.R, self.u, self.v = q, list(le), set(R), u, v
        self.ge = [sum(1 << b for b in range(q) if (le[b] >> a) & 1) for a in range(q)]   # ge[a] = {b : b <= a}

    def leq(self, a, b):
        return (self.le[a] >> b) & 1 == 1

    def lt(self, a, b):
        return self.leq(a, b) and not self.leq(b, a)

    def downsets(self):
        """down-sets D with u in D, v not in D (brute force over subsets; q small)"""
        out = []
        for D in range(1 << self.q):
            if not (D >> self.u) & 1 or (D >> self.v) & 1:
                continue
            ok = True
            for y in bits(D):
                if self.ge[y] & ~D:
                    ok = False
                    break
            if ok:
                out.append(D)
        return out

    def connected_in_GD(self, D):
        adj = [0] * self.q
        for a, b in self.R:
            if ((D >> a) & 1) != ((D >> b) & 1):
                adj[a] |= 1 << b
                adj[b] |= 1 << a
        seen = 1 << self.u
        st = [self.u]
        while st:
            a = st.pop()
            nb = adj[a] & ~seen
            seen |= nb
            st.extend(bits(nb))
        return (seen >> self.v) & 1 == 1

    def answer(self):
        return any(self.connected_in_GD(D) for D in self.downsets())

    def check_def16(self):
        for x in range(self.q):
            need(self.leq(self.u, x) and self.leq(x, self.v), "Def1.6: u <= x <= v")
        for a, b in self.R:
            need(self.lt(a, b), "Def1.6: R pair not strict")
        need((self.u, self.v) not in self.R, "Def1.6: {u,v} in R")

    def p2(self):
        nb = [0] * self.q
        for a, b in self.R:
            nb[a] |= 1 << b
            nb[b] |= 1 << a
        for x in range(self.q):
            for y in range(x + 1, self.q):
                if self.leq(x, y) or self.leq(y, x):
                    continue
                ok = False
                for z in bits(nb[x] & nb[y]):
                    if (self.lt(z, x) and self.lt(z, y)) or (self.lt(x, z) and self.lt(y, z)):
                        ok = True
                        break
                if not ok:
                    return False
        return True


def graph_to_zz(n, edges, u, v, stats):
    """Section 2 with checks of Lemmas 2.1-2.8 and Theorem 2.9.  Returns (zz, info)."""
    g = G(n, edges)
    cG, cvG = cvals_all(g)
    dG = [g.dist(x) for x in range(n)]
    # ---- Lemma 2.1
    br = bridges(g)
    rest = [e for e in g.edges if e not in br]
    Kv = g.comp(u, rest)
    need((Kv >> v) & 1, "L2.1(a)")
    Kedges = [e for e in rest if (Kv >> e[0]) & 1 and (Kv >> e[1]) & 1]
    K = G(n, Kedges, vmask=Kv)
    need(not bridges(K), "L2.1(d): K has a bridge")
    cK, cvK = cvals_all(K)
    for x in bits(Kv):
        dK = K.dist(x)
        for y in bits(Kv):
            if x != y:
                need(dK[y] == dG[x][y], "L2.1(b): distance")
                need(cK[(x, y)] == cG[(x, y)], "L2.1(b): c")
                need(dK[y] <= 2 or cK[(x, y)] <= 2, "L2.1(d): K in DC")
    c = cK[(u, v)]
    need(c == cG[(u, v)] and c >= 3, "L2.1(d): c")
    # minimum cuts of G and of K as edge sets (Lemma 2.1(b)): every minimum cut of G is delta_G(S) (Lemma 1.3(a))
    mincutsG = {tuple(g.delta_edges(S)) for S, val in cvG.items() if (S >> u) & 1 and not (S >> v) & 1 and val == c}
    mincutsK = {tuple(K.delta_edges(S)) for S, val in cvK.items() if (S >> u) & 1 and not (S >> v) & 1 and val == c}
    need(mincutsG == mincutsK, "L2.1(b): minimum cuts of G and K differ")
    # ---- Q
    Q = [x for x in bits(Kv) if x == u or cK[(u, x)] >= 3]
    Qm = sum(1 << x for x in Q)
    need((Qm >> v) & 1, "v in Q")
    # ---- Lemma 2.2(c)
    for x in Q:
        dK = K.dist(x)
        for y in Q:
            if x != y:
                need(cK[(x, y)] >= 3 and dK[y] <= 2, "L2.2(c)")
    # ---- Lemma 2.2(b): every vertex of a u-v path inside a minimum cut lies in Q (paths enumerated)
    # (checked through Lemma 2.4(d) below: real-edge paths)
    # ---- Lemma 2.3: ears = components of K - Q
    nonQ = Kv & ~Qm
    ears = []
    seen = 0
    for x in bits(nonQ):
        if (seen >> x) & 1:
            continue
        sub = [e for e in Kedges if (nonQ >> e[0]) & 1 and (nonQ >> e[1]) & 1]
        Y = K.comp(x, sub) & nonQ
        seen |= Y
        bd = K.delta_edges(Y)
        need(len(bd) == 2, "L2.3(c): |delta(Y)| != 2")
        att = []
        for a, b in bd:
            p = a if not (Y >> a) & 1 else b
            need((Qm >> p) & 1, "L2.3(c): attachment outside Q")
            att.append(p)
        ears.append((Y, att[0], att[1]))
    # maximality: every ear set (non-empty, misses Q, |delta| = 2) lies inside one component
    for S, val in cvK.items():
        if S and not S & Qm and val == 2:
            need(any(S & ~Y == 0 for (Y, p, pp) in ears), "L2.3(c): ear set not inside a component")
    # ---- Lemma 2.4: H
    real = [e for e in Kedges if (Qm >> e[0]) & 1 and (Qm >> e[1]) & 1]
    earedges = [(min(p, pp), max(p, pp)) for (Y, p, pp) in ears if p != pp]

    def dH(B):
        return (sum(1 for a, b in real if ((B >> a) & 1) != ((B >> b) & 1))
                + sum(1 for a, b in earedges if ((B >> a) & 1) != ((B >> b) & 1)))

    def AofB(B):
        A = B
        for (Y, p, pp) in ears:
            if (B >> p) & 1:
                A |= Y
        return A

    Qsubs = []
    for r in range(1 << len(Q)):
        B = 0
        for i, x in enumerate(Q):
            if (r >> i) & 1:
                B |= 1 << x
        Qsubs.append(B)
    for B in Qsubs:
        A = AofB(B)
        need(A & Qm == B and K.delta(A) == dH(B), "L2.4(a)")
    for S in cvK:
        need(cvK[S] >= dH(S & Qm), "L2.4(b)")
    cuts = [B for B in Qsubs if (B >> u) & 1 and not (B >> v) & 1]
    cH = min(dH(B) for B in cuts)
    need(cH == c, "L2.4(c): c_H != c")
    minH = [B for B in cuts if dH(B) == c]
    for S, val in cvK.items():
        if (S >> u) & 1 and not (S >> v) & 1 and val == c:
            need((S & Qm) in minH, "L2.4(c): S cap Q not minimum in H")
    for B in minH:
        need(K.delta(AofB(B)) == c, "L2.4(c): A(B) not minimum in K")
    # Lemma 2.4(e)
    realadj = [0] * n
    for a, b in real:
        realadj[a] |= 1 << b
        realadj[b] |= 1 << a
    ears_set = set(earedges)
    for x in Q:
        for y in Q:
            if x < y:
                ok = ((realadj[x] >> y) & 1) or (x, y) in ears_set or (realadj[x] & realadj[y] & Qm)
                need(ok, "L2.4(e)")
    # ---- Definition 2.5: preorder by brute force over minimum cuts of H
    idx = {x: i for i, x in enumerate(Q)}
    q = len(Q)
    le = [0] * q
    for x in Q:
        for y in Q:
            if all((B >> x) & 1 for B in minH if (B >> y) & 1):
                le[idx[x]] |= 1 << idx[y]
    # flow formula of Theorem 2.9 (Time): x <= y iff x = y, x = u, y = v, or least |delta_H(S)| over
    # {u, y} <= S <= Q - {x, v} exceeds c
    for x in Q:
        for y in Q:
            if x == y or x == u or y == v:
                f = True
            else:
                f = min(dH(B) for B in Qsubs if (B >> u) & 1 and (B >> y) & 1 and not (B >> x) & 1
                        and not (B >> v) & 1) > c
            need(f == bool((le[idx[x]] >> idx[y]) & 1), "Thm2.9 time: flow formula for <=")
    def leqQ(x, y):
        return (le[idx[x]] >> idx[y]) & 1 == 1
    # ---- Lemma 2.6
    for x in Q:
        need(leqQ(u, x) and leqQ(x, v), "L2.6: u <= x <= v")
    need(not leqQ(v, u), "L2.6: u < v")
    for (a, b) in real + earedges:
        need(leqQ(a, b) or leqQ(b, a), "L2.6: edge of H joins incomparable elements")
    Rq = set()
    for (a, b) in real:
        if leqQ(a, b) and leqQ(b, a):
            continue
        lo, hi = (a, b) if leqQ(a, b) else (b, a)
        Rq.add((idx[lo], idx[hi]))
    zz = ZZ(q, le, Rq, idx[u], idx[v])
    zz.check_def16()
    # ---- Lemma 2.7: minimum cuts of H = down-sets with u in, v out
    ds = set()
    for D in zz.downsets():
        ds.add(sum(1 << Q[i] for i in bits(D)))
    need(ds == set(minH), "L2.7")
    # ---- Lemma 2.8
    need(zz.p2(), "L2.8: P2 fails")
    # ---- Theorem 2.9: answer
    cp = cp_bruteforce(g, u, v, cvG)
    need(c <= cp <= c + 1, "cp outside [c, c+1] (A2 Prop. 5)")
    zans = zz.answer()
    need(zans == (cp == c), "Thm2.9: answer")
    need(len(Rq) <= len(g.edges) and q <= n, "Thm2.9: sizes")
    stats["pairs"] = stats.get("pairs", 0) + 1
    stats["yes" if zans else "no"] = stats.get("yes" if zans else "no", 0) + 1
    stats["ears"] = stats.get("ears", 0) + len(ears)
    stats["ears p=p'"] = stats.get("ears p=p'", 0) + sum(1 for e in ears if e[1] == e[2])
    stats["ear edges"] = stats.get("ear edges", 0) + len(earedges)
    stats["bridges>0"] = stats.get("bridges>0", 0) + (1 if br else 0)
    return zz, {"c": c, "cp": cp, "q": q, "ears": len(ears)}


# =====================================================================================================================
# Section 3: switch form
# =====================================================================================================================

class SF:
    """General switch form (Definition 1.7).  Switches 0..m-1, le[w] = mask of switches >= w, sides E[w], F[w] node
    masks, mid = dict (z, w) -> private node."""

    def __init__(self, m, le, E, F, s, t, mid, nn):
        self.m, self.le, self.E, self.F, self.s, self.t, self.mid, self.nn = m, list(le), list(E), list(F), s, t, dict(mid), nn
        self.full = (1 << m) - 1
        self.up = list(le)
        self.dn = [sum(1 << j for j in range(m) if (le[j] >> i) & 1) for i in range(m)]
        self.tie = [self.up[i] & self.dn[i] for i in range(m)]
        self.sup = [self.up[i] & ~self.tie[i] for i in range(m)]
        self.sdn = [self.dn[i] & ~self.tie[i] for i in range(m)]
        self.enon = sum(1 << w for w in range(m) if E[w])
        self.fnon = sum(1 << w for w in range(m) if F[w])
        self.lmn = [0] * m
        self.umn = [0] * m
        for (z, w) in self.mid:
            self.lmn[w] |= 1 << z
            self.umn[z] |= 1 << w
        # stars (Definition 4.1)
        self.Estar = []
        self.Fstar = []
        for w in range(m):
            es = E[w]
            for (z, w2), p in self.mid.items():
                if (self.lmn[w] >> z) & 1:
                    es |= 1 << p
            self.Estar.append(es)
            fs = F[w]
            for (w2, z), p in self.mid.items():
                if (self.umn[w] >> z) & 1:
                    fs |= 1 << p
            self.Fstar.append(fs)
        self.NEstar = [self.NE(self.Estar[x]) for x in range(m)]
        self.NFstar = [self.NF(self.Fstar[y]) for y in range(m)]

    def leq(self, a, b):
        return (self.le[a] >> b) & 1 == 1

    def lt(self, a, b):
        return self.leq(a, b) and not self.leq(b, a)

    def NE(self, Z):
        return sum(1 << w for w in range(self.m) if self.E[w] & Z)

    def NF(self, Z):
        return sum(1 << w for w in range(self.m) if self.F[w] & Z)

    def upc(self, S):
        r = 0
        for x in bits(S):
            r |= self.up[x]
        return r

    def dnc(self, S):
        r = 0
        for x in bits(S):
            r |= self.dn[x]
        return r

    def is_down(self, D):
        return self.dnc(D) == D

    def check_def17(self):
        for (z, w), p in self.mid.items():
            need(self.lt(z, w), "Def1.7: middle edge not strict")
            for x in range(self.m):
                inE = (self.E[x] >> p) & 1
                inF = (self.F[x] >> p) & 1
                need(inE == (1 if x == w else 0), "Def1.7: private node in a wrong E-side")
                need(inF == (1 if x == z else 0), "Def1.7: private node in a wrong F-side")

    def p2(self):
        for x in range(self.m):
            for y in range(x + 1, self.m):
                if self.leq(x, y) or self.leq(y, x):
                    continue
                if self.E[x] & self.E[y] or self.F[x] & self.F[y] or self.lmn[x] & self.lmn[y] or self.umn[x] & self.umn[y]:
                    continue
                return False
        return True

    def downsets(self):
        out = []
        for D in range(1 << self.m):
            if self.is_down(D):
                out.append(D)
        return out

    def connects(self, D):
        if self.s == self.t:
            return True
        picked = [self.F[w] if (D >> w) & 1 else self.E[w] for w in range(self.m)]
        reach = 1 << self.s
        used = 0
        changed = True
        while changed:
            changed = False
            for w in range(self.m):
                if not (used >> w) & 1 and picked[w] & reach:
                    used |= 1 << w
                    reach |= picked[w]
                    changed = True
        return (reach >> self.t) & 1 == 1

    def answer(self):
        return any(self.connects(D) for D in self.downsets())


def zz_to_sf(zz):
    """Construction 3.1 (own implementation from the text)."""
    q, u, v = zz.q, zz.u, zz.v
    cu = [x for x in range(q) if zz.leq(x, u) and zz.leq(u, x)]
    cv = [x for x in range(q) if zz.leq(x, v) and zz.leq(v, x)]
    need(not set(cu) & set(cv), "C3.1: [u] and [v] meet")
    Ms = [x for x in range(q) if x not in cu and x not in cv]
    mi = {x: i for i, x in enumerate(Ms)}
    m = len(Ms)
    uv = set(cu) | set(cv)
    kinds = {1: [], 2: [], 3: [], 4: []}
    for (a, b) in zz.R:
        if a in cu and b in cv:
            kinds[1].append((a, b))
        elif a in cu and b in mi:
            kinds[2].append((a, b))
        elif a in mi and b in cv:
            kinds[3].append((a, b))
        elif a in mi and b in mi:
            kinds[4].append((a, b))
        else:
            raise Fail("C3.1: real edge of no kind")
    # nodes: components of the first-kind graph on [u] u [v]
    par = {x: x for x in uv}

    def f(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x
    for a, b in kinds[1]:
        ra, rb = f(a), f(b)
        if ra != rb:
            par[ra] = rb
    roots = sorted({f(x) for x in uv})
    nid = {r: i for i, r in enumerate(roots)}
    node = {x: nid[f(x)] for x in uv}
    nn = len(roots)
    mid = {}
    for a, b in kinds[4]:
        mid[(mi[a], mi[b])] = nn
        nn += 1
    E = [0] * m
    F = [0] * m
    for a, w in kinds[2]:
        E[mi[w]] |= 1 << node[a]
    for w, b in kinds[3]:
        F[mi[w]] |= 1 << node[b]
    for (a, b), p in mid.items():
        F[a] |= 1 << p
        E[b] |= 1 << p
    le = [0] * m
    for x in Ms:
        for y in Ms:
            if zz.leq(x, y):
                le[mi[x]] |= 1 << mi[y]
    sf = SF(m, le, E, F, node[u], node[v], mid, nn)
    return sf, {"Ms": Ms, "cu": cu, "cv": cv, "kinds": kinds}


def check_lemma32_33(zz, sf, info):
    sf.check_def17()
    if zz.p2():
        need(sf.p2(), "L3.2: P2 not inherited")
    need(sf.m <= zz.q - 2, "L3.2: m")
    need(sf.nn <= zz.q + len(zz.R), "L3.2: nodes")
    need(sum(pc(sf.E[w]) + pc(sf.F[w]) for w in range(sf.m)) <= 2 * len(zz.R), "L3.2: sigma")
    # Lemma 3.3 per down-set: (i) bijection, (ii)-(iv) G_{D'} connects u,v iff D' cap M connects s,t
    Ms, cu = info["Ms"], info["cu"]
    mi = {x: i for i, x in enumerate(Ms)}
    dz = zz.downsets()
    dsw = set(sf.downsets())
    images = set()
    for Dp in dz:
        D = sum(1 << mi[x] for x in bits(Dp) if x in mi)
        need(D in dsw, "L3.3(i): D' cap M not a down-set")
        back = D and 0
        back = sum(1 << x for x in cu) | sum(1 << Ms[i] for i in bits(D))
        need(back == Dp, "L3.3(i): maps not inverse")
        images.add(D)
        need(zz.connected_in_GD(Dp) == sf.connects(D), "L3.3: per down-set answers differ")
    need(images == dsw, "L3.3(i): not onto")
    return zz.answer() == sf.answer()


# =====================================================================================================================
# Section 3.4 / 4: valid paths and their objects
# =====================================================================================================================

def side_set(sf, w, k):
    return sf.E[w] if k == "E" else sf.F[w]


def conflict(sf, a, b):
    """a, b = (switch, kind); conflict pair {E_w, F_z} with w <= z"""
    (w1, k1), (w2, k2) = a, b
    if k1 == k2:
        return False
    if k1 == "E":
        return sf.leq(w1, w2)
    return sf.leq(w2, w1)


def is_valid(sf, P):
    if not P:
        return False
    ws = [w for w, k in P]
    if len(set(ws)) != len(ws):
        return False
    if not (side_set(sf, *P[0]) >> sf.s) & 1 or not (side_set(sf, *P[-1]) >> sf.t) & 1:
        return False
    for i in range(len(P) - 1):
        if not side_set(sf, *P[i]) & side_set(sf, *P[i + 1]):
            return False
    for i in range(len(P)):
        for j in range(i + 1, len(P)):
            if conflict(sf, P[i], P[j]):
                return False
    return True


def shortest_valid_paths(sf, cap=20000, rmax=None):
    """all shortest valid paths (iterative deepening), or [] if none; None if the budget is exceeded"""
    sides = [(w, k) for w in range(sf.m) for k in "EF" if side_set(sf, w, k)]
    rmax = sf.m if rmax is None else rmax
    budget = [cap * 50]
    for r in range(1, rmax + 1):
        out = []

        def dfs(P, used):
            budget[0] -= 1
            if budget[0] < 0:
                raise Fail("budget")
            if len(P) == r:
                if (side_set(sf, *P[-1]) >> sf.t) & 1:
                    out.append(list(P))
                return
            last = side_set(sf, *P[-1])
            for sd in sides:
                if (used >> sd[0]) & 1:
                    continue
                if not side_set(sf, *sd) & last:
                    continue
                if any(conflict(sf, sd, x) for x in P):
                    continue
                P.append(sd)
                dfs(P, used | (1 << sd[0]))
                P.pop()
                if len(out) > cap:
                    return
        try:
            for sd in sides:
                if (side_set(sf, *sd) >> sf.s) & 1:
                    dfs([sd], 1 << sd[0])
        except Fail:
            return None
        if out:
            return out
    return []


class PathObj:
    """objects of Definitions 1.8 and 4.1 for a valid path P"""

    def __init__(self, sf, P):
        self.P = P
        self.pos = {w: i + 1 for i, (w, k) in enumerate(P)}
        self.WE = sum(1 << w for w, k in P if k == "E")
        self.WF = sum(1 << w for w, k in P if k == "F")
        self.on = self.WE | self.WF
        self.Up = sf.upc(self.WE)
        self.L = sf.dnc(self.WF)
        self.A = sum(1 << w for w in bits(self.WE) if not (sf.sdn[w] & self.WE))
        self.B = sum(1 << w for w in bits(self.WF) if not (sf.sup[w] & self.WF))
        self.NEn = self.L & sf.enon
        self.NFn = self.Up & sf.fnon

    def X(self, sf, c):
        w, k = self.P[c - 1]
        return side_set(sf, w, k)


def check_lemma34(sf, P, po, allD):
    need(not (po.Up & po.L), "L3.4(a): Up cap L")
    for D in allD:
        picks = all(((D >> w) & 1) == (1 if k == "F" else 0) for w, k in P)
        need(picks == (po.L & ~D == 0 and D & po.Up == 0), "L3.4(a): pick criterion")
        if picks:
            need(sf.connects(D), "L3.4(a): picks every member but does not connect")


def check_section4(sf, P, po, stats):
    """Lemma 4.2, 4.2(e) (P shortest), 4.3 (j = 1, 2), 4.4, 4.5.  Returns max spans."""
    m = sf.m
    r = len(P)
    need(not (po.Up & po.L), "L4.2(a)")
    need(sf.upc(po.A) == po.Up and sf.dnc(po.B) == po.L, "L4.2(a): Up = upA, L = dnB")
    need(po.WE & ~sf.enon == 0 and po.WF & ~sf.fnon == 0, "L4.2(a): members non-empty")
    for a in bits(po.A):
        need(not (sf.up[a] & po.L), "L4.2(b)")
    for b in bits(po.B):
        need(not (sf.sup[b] & po.L), "L4.2(b): L strictly above B")
    # 4.2(e)
    for c in range(1, r + 1):
        for d in range(c + 2, r + 1):
            need(not (po.X(sf, c) & po.X(sf, d)), "L4.2(e)")
    # P-consistent sides of switches not on P
    pcs = []
    for w in range(m):
        if (po.on >> w) & 1:
            continue
        if not (po.L >> w) & 1 and sf.E[w]:
            pcs.append((w, "E"))
        if not (po.Up >> w) & 1 and sf.F[w]:
            pcs.append((w, "F"))
    # 4.2(d)
    for z in pcs:
        for x in P:
            need(not conflict(sf, z, x), "L4.2(d)")
    # 4.3 with j = 1 and j = 2
    def meet(Z):
        return [c for c in range(1, r + 1) if po.X(sf, c) & side_set(sf, *Z)]
    mt = {z: meet(z) for z in pcs}
    for z in pcs:
        if mt[z]:
            need(max(mt[z]) - min(mt[z]) <= 2, "L4.3 j=1")
    for z1 in pcs:
        for z2 in pcs:
            if z1[0] == z2[0] or conflict(sf, z1, z2) or not (side_set(sf, *z1) & side_set(sf, *z2)):
                continue
            for c in mt[z1]:
                for d in mt[z2]:
                    need(abs(c - d) <= 3, "L4.3 j=2")
    # 4.4
    span = 0
    for x in range(m):
        if (po.L >> x) & 1:
            continue
        Ax = po.A & sf.NEstar[x]
        if Ax:
            ps = [po.pos[a] for a in bits(Ax)]
            span = max(span, max(ps) - min(ps) + 1)
    for y in range(m):
        if (po.Up >> y) & 1:
            continue
        By = po.B & sf.NFstar[y]
        if By:
            ps = [po.pos[b] for b in bits(By)]
            span = max(span, max(ps) - min(ps) + 1)
    need(span <= 9, "L4.4: span > 9")
    stats["max span L4.4"] = max(stats.get("max span L4.4", 0), span)
    if span > 5:
        stats["span > 5"] = stats.get("span > 5", 0) + 1
    return span


def check_lemma45(sf, stats):
    for x in range(sf.m):
        for y in range(sf.m):
            if x == y or sf.leq(x, y) or sf.leq(y, x):
                continue
            ok = (sf.NEstar[x] >> y) & 1 or (sf.NFstar[y] >> x) & 1
            need(ok, "L4.5")   # checked without the hypothesis F_x, E_y non-empty


# =====================================================================================================================
# Section 5: terms, Lemma 5.2 by the proof's construction, Theorem 5.3
# =====================================================================================================================

def kN(m):
    k = int(math.floor(math.log2(m))) + 1
    N = int(math.ceil(2 * k * math.log(m))) if m > 1 else 0
    return k, N


def D_of_term(sf, kind, T, Tf, Phi, Psi=0):
    if kind == "E":
        U = 0
        for x in bits(T):
            U |= sf.NEstar[x]
        Pi = 0
        for x in bits(Tf):
            Pi |= sf.sdn[x]
        Gam = (sf.enon & ~U & ~Pi) | Phi
        return sf.full & ~sf.upc(Gam), U, Gam
    U = 0
    for y in bits(T):
        U |= sf.NFstar[y]
    Pi = sf.upc(Psi)
    for y in bits(Tf):
        Pi |= sf.sup[y]
    Gam = (sf.fnon & ~U & ~Pi) | Phi
    return sf.dnc(Gam), U, Gam


def game(rows, cols, mu):
    """value, p (on rows), q (on cols) of the zero-sum game, row player maximises mu"""
    import numpy as np
    from scipy.optimize import linprog
    R, C = len(rows), len(cols)
    A = np.array([[mu[(x, y)] for y in cols] for x in rows], dtype=float)
    # max lam s.t. A^T p >= lam, sum p = 1
    c = np.zeros(R + 1)
    c[-1] = -1
    Aub = np.hstack([-A.T, np.ones((C, 1))])
    bub = np.zeros(C)
    Aeq = np.hstack([np.ones((1, R)), np.zeros((1, 1))])
    res = linprog(c, A_ub=Aub, b_ub=bub, A_eq=Aeq, b_eq=[1.0], bounds=[(0, None)] * R + [(None, None)],
                  method="highs")
    p = res.x[:R]
    lam = res.x[-1]
    # min lam' s.t. A q <= lam', sum q = 1
    c2 = np.zeros(C + 1)
    c2[-1] = 1
    Aub2 = np.hstack([A, -np.ones((R, 1))])
    res2 = linprog(c2, A_ub=Aub2, b_ub=np.zeros(R), A_eq=np.hstack([np.ones((1, C)), np.zeros((1, 1))]), b_eq=[1.0],
                   bounds=[(0, None)] * C + [(None, None)], method="highs")
    qv = res2.x[:C]
    lam2 = res2.x[-1]
    need(abs(lam - lam2) < 1e-7, "minimax values differ (LP)")
    return lam, {x: p[i] for i, x in enumerate(rows)}, {y: qv[i] for i, y in enumerate(cols)}


ALLCOV = [False, 4000]
ADV = [False, 20000]


def lemma52(sf, po, Ap, stats, force=None):
    """One level by the construction of the proof of Lemma 5.2; every claimed property is checked exactly.
    Returns (kind, term, D, Asecond or None)."""
    m = sf.m
    k, N = kN(m)
    rows = [x for x in bits(sf.upc(Ap) & sf.fnon)]
    cols = [y for y in bits(po.NEn)]
    nA = pc(Ap)
    theta = nA / (2 * k)
    dam = {x: sf.sdn[x] & Ap for x in range(m)}
    light = {x: pc(dam[x]) <= theta for x in range(m)}
    for a in bits(Ap):
        need(light[a], "L5.2: element of A' not light")
    for x in rows:
        need((po.Up >> x) & 1 and not (po.L >> x) & 1, "L5.2: row not in Up - L")
    covE = {}
    for x in rows:
        cm = sf.NEstar[x] | (sf.sdn[x] if light[x] else 0)
        covE[x] = cm & po.NEn
    rowmask = sum(1 << x for x in rows)
    covF = {}
    for y in cols:
        cm = sf.NFstar[y] | (sf.sup[y] if (po.B >> y) & 1 else 0)
        covF[y] = cm & rowmask
    # Claim (duality)
    for x in rows:
        if not light[x]:
            continue
        for y in cols:
            need((covE[x] >> y) & 1 or (covF[y] >> x) & 1, "L5.2 Claim (duality)")

    def finish_E(T):
        Tf = sum(1 << x for x in bits(T) if light[x])
        D0, U, _ = D_of_term(sf, "E", T, Tf, 0)
        Phi = Ap & U
        D, U2, Gam = D_of_term(sf, "E", T, Tf, Phi)
        need(pc(T) <= k, "L5.2: tools")
        need(pc(Phi) <= 9 * k and Phi & ~U == 0, "L5.2: flips (E)")
        need(po.L & ~D == 0, "L5.2: L not in D (E)")
        A2 = Ap & ~Gam
        need(pc(A2) <= nA / 2, "L5.2: damage > |A'|/2")
        need(D & sf.upc(Ap) & ~sf.upc(A2) == 0, "L5.2: D cap upA' not in upA''")
        stats["max flips"] = max(stats.get("max flips", 0), pc(Phi))
        return ("E", (T, Tf, Phi, 0), D, A2 if A2 else None)

    def finish_F(T, Psi):
        Tf = T & po.B
        D0, U, _ = D_of_term(sf, "F", T, Tf, 0, Psi)
        Phi = po.B & U
        D, U2, Gam = D_of_term(sf, "F", T, Tf, Phi, Psi)
        need(pc(T) <= k and pc(Psi) <= N, "L5.2: tools/anchors (F)")
        need(pc(Phi) <= 9 * k and Phi & ~U == 0, "L5.2: flips (F)")
        need(D & sf.upc(Ap) == 0, "L5.2: D meets upA' (F)")
        need(po.L & ~D == 0, "L5.2: L not in D (F)")
        stats["max flips"] = max(stats.get("max flips", 0), pc(Phi))
        stats["max anchors"] = max(stats.get("max anchors", 0), pc(Psi))
        return ("F", (T, Tf, Phi, Psi), D, None)

    if not cols:
        D, U, Gam = D_of_term(sf, "E", 0, 0, 0)
        need(po.L & ~D == 0 and D & sf.upc(Ap) == 0, "L5.2 trivial C empty")
        stats["trivial C=0"] = stats.get("trivial C=0", 0) + 1
        return ("E", (0, 0, 0, 0), D, None)
    if not rows:
        D, U, Gam = D_of_term(sf, "F", 0, 0, 0, 0)
        need(po.L & ~D == 0 and D & sf.upc(Ap) == 0, "L5.2 trivial R empty")
        stats["trivial R=0"] = stats.get("trivial R=0", 0) + 1
        return ("F", (0, 0, 0, 0), D, None)
    if ALLCOV[0]:
        # the deductions of both cases use only the covering properties of the fixed outcome: check them for EVERY
        # tool set of size <= k that covers (E: all columns; F: all light rows), as long as there are few of them
        cnt = 0
        for r_ in range(1, k + 1):
            for c_ in combinations(rows, r_):
                cnt += 1
                if cnt > ALLCOV[1]:
                    break
                cm = 0
                for x in c_:
                    cm |= covE[x]
                if cm & po.NEn == po.NEn:
                    finish_E(sum(1 << x for x in c_))
                    stats["allcov E-terms checked"] = stats.get("allcov E-terms checked", 0) + 1
        heavy0 = [x for x in rows if not light[x]]
        # anchors: one element of A' strictly below each heavy row (at most N needed; checked)
        Psi0 = 0
        for x in heavy0:
            if not (dam[x] & Psi0):
                Psi0 |= dam[x] & -dam[x]
        lightmask = sum(1 << x for x in rows if light[x])
        if pc(Psi0) <= N:
            cnt = 0
            for r_ in range(1, k + 1):
                for c_ in combinations(cols, r_):
                    cnt += 1
                    if cnt > ALLCOV[1]:
                        break
                    cm = 0
                    for y in c_:
                        cm |= covF[y]
                    if cm & lightmask == lightmask:
                        finish_F(sum(1 << y for y in c_), Psi0)
                        stats["allcov F-terms checked"] = stats.get("allcov F-terms checked", 0) + 1
    if ADV[0]:
        # adversarial outcome (stress of Theorem 5.3): among covering tool sets of size <= k, the one with the
        # largest damaged set A'' (the deduction of the case lambda >= 1/2 holds for every covering outcome)
        best = None
        # greedy candidate first: up to k light rows, each adding the most damage outside the stars chosen so far
        Tg = 0
        for _ in range(k):
            cand = None
            for x in rows:
                if (Tg >> x) & 1 or not light[x]:
                    continue
                Tx = Tg | (1 << x)
                Tfx = sum(1 << z for z in bits(Tx) if light[z])
                _, U_, _ = D_of_term(sf, "E", Tx, Tfx, 0)
                _, _, G_ = D_of_term(sf, "E", Tx, Tfx, Ap & U_)
                dmg = pc(Ap & ~G_)
                if cand is None or dmg > cand[0]:
                    cand = (dmg, Tx)
            if cand is None:
                break
            Tg = cand[1]
        cm = 0
        for x in bits(Tg):
            cm |= covE[x]
        if Tg and cm & po.NEn == po.NEn:
            Tfg = sum(1 << z for z in bits(Tg) if light[z])
            _, U_, _ = D_of_term(sf, "E", Tg, Tfg, 0)
            _, _, G_ = D_of_term(sf, "E", Tg, Tfg, Ap & U_)
            best = (pc(Ap & ~G_), Tg)
        cnt = 0
        for r_ in range(1, k + 1):
            for c_ in combinations(rows, r_):
                cnt += 1
                if cnt > ADV[1]:
                    break
                cm = 0
                for x in c_:
                    cm |= covE[x]
                if cm & po.NEn != po.NEn:
                    continue
                T_ = sum(1 << x for x in c_)
                Tf_ = sum(1 << x for x in c_ if light[x])
                _, U_, _ = D_of_term(sf, "E", T_, Tf_, 0)
                _, _, G_ = D_of_term(sf, "E", T_, Tf_, Ap & U_)
                dmg = pc(Ap & ~G_)
                if best is None or dmg > best[0]:
                    best = (dmg, T_)
        if best is not None:
            stats["adversarial E-terms"] = stats.get("adversarial E-terms", 0) + 1
            return finish_E(best[1])
    mu = {(x, y): (covE[x] >> y) & 1 for x in rows for y in cols}
    lam, p, q = game(rows, cols, mu)
    branch = force or ("E" if lam >= 0.5 - 1e-9 else "F")
    eps = 1e-12
    if branch == "E":
        pi = {y: sum(p[x] * mu[(x, y)] for x in rows) for y in cols}
        E0 = sum((1 - pi[y]) ** k for y in cols)
        need(E0 < 1 + 1e-9, "L5.2 (E): expectation >= 1")
        supp = [x for x in rows if p[x] > eps]
        unc = set(cols)
        T = 0
        for i in range(k):
            best = None
            for x in supp:
                rest = [y for y in unc if not (covE[x] >> y) & 1]
                val = sum((1 - pi[y]) ** (k - i - 1) for y in rest)
                if best is None or val < best[0]:
                    best = (val, x, rest)
            T |= 1 << best[1]
            unc = set(best[2])
        need(not unc, "L5.2 (E): derandomisation left a column uncovered")
        stats["branch E"] = stats.get("branch E", 0) + 1
        return finish_E(T)
    # branch F
    lightrows = [x for x in rows if light[x]]
    heavy = [x for x in rows if not light[x]]
    if m == 1:
        need(not heavy, "L5.2: heavy row with m = 1")
    pf = {x: sum(q[y] for y in cols if (covF[y] >> x) & 1) for x in lightrows}
    h = {x: pc(dam[x]) / nA for x in heavy}
    for x in lightrows:
        need(pf[x] >= 1 - lam - 1e-9, "L5.2 (F): light row covered with probability < 1 - lambda")
    E0 = sum((1 - pf[x]) ** k for x in lightrows) + sum((1 - h[x]) ** N for x in heavy)
    need(E0 < 1 + 1e-9, "L5.2 (F): expectation >= 1")
    suppq = [y for y in cols if q[y] > eps]
    uncl = set(lightrows)
    unch = set(heavy)
    T = 0
    for i in range(k):
        best = None
        for y in suppq:
            rest = [x for x in uncl if not (covF[y] >> x) & 1]
            val = sum((1 - pf[x]) ** (k - i - 1) for x in rest) + sum((1 - h[x]) ** N for x in unch)
            if best is None or val < best[0]:
                best = (val, y, rest)
        T |= 1 << best[1]
        uncl = set(best[2])
    need(not uncl, "L5.2 (F): a light row stays uncovered")
    Psi = 0
    Alist = bits(Ap)
    for j in range(N):
        if not unch:
            break
        best = None
        for a in Alist:
            rest = [x for x in unch if not (dam[x] >> a) & 1]
            val = sum((1 - h[x]) ** (N - j - 1) for x in rest)
            if best is None or val < best[0]:
                best = (val, a, rest)
        Psi |= 1 << best[1]
        unch = set(best[2])
    need(not unch, "L5.2 (F): a heavy row is above no anchor")
    stats["branch F"] = stats.get("branch F", 0) + 1
    if heavy:
        stats["F with heavy rows"] = stats.get("F with heavy rows", 0) + 1
    return finish_F(T, Psi)


def theorem53(sf, P, stats):
    po = PathObj(sf, P)
    m = sf.m
    need(m >= 1, "T5.3: m >= 1")
    k, N = kN(m)
    if not po.A:
        D, U, Gam = D_of_term(sf, "F", 0, 0, 0, 0)
        need(po.L & ~D == 0 and not (D & po.Up), "T5.3: A empty")
        need(sf.connects(D), "T5.3: A empty, D does not connect")
        stats["levels hist"] = stats.get("levels hist", {})
        stats["levels hist"][1] = stats["levels hist"].get(1, 0) + 1
        return 1
    Ai = po.A
    Dcap = sf.full
    j = 0
    while True:
        j += 1
        need(j <= k, "T5.3: more than k levels")
        kind, term, D, A2 = lemma52(sf, po, Ai, stats)
        Dcap &= D
        need(po.L & ~Dcap == 0, "T5.3: L not in intersection")
        if A2 is None:
            need(not (Dcap & po.Up), "T5.3: D meets Up")
            break
        need(kind == "E", "T5.3: continue term not an E-term")
        need(Dcap & po.Up & ~sf.upc(A2) == 0, "T5.3: induction claim")
        Ai = A2
    need(sf.is_down(Dcap), "T5.3: not a mode vector")
    need(sf.connects(Dcap), "T5.3: intersection does not connect")
    for w, kk in P:
        need(((Dcap >> w) & 1) == (1 if kk == "F" else 0), "T5.3: member not picked")
    h = stats.setdefault("levels hist", {})
    h[j] = h.get(j, 0) + 1
    return j


# =====================================================================================================================
# exact IDESC (Definition 6.1) for small m, by de-duplicating the term values
# =====================================================================================================================

def submasks(U):
    s = U
    while True:
        yield s
        if s == 0:
            break
        s = (s - 1) & U


def idesc_exact(sf, maxm=7):
    if sf.s == sf.t:
        return True
    if sf.m == 0:
        return False
    m = sf.m
    if m > maxm:
        return None
    k, N = kN(m)
    full = sf.full
    toolsets = [sum(1 << x for x in c) for r in range(0, k + 1) for c in combinations(range(m), r)]
    # anchor sets: subsets of size <= N; their up-closures
    if N >= m:
        anc_up = {sf.upc(S) for S in range(1 << m)}
    else:
        anc_up = {sf.upc(sum(1 << x for x in c)) for r in range(0, N + 1) for c in combinations(range(m), r)}
    S_af = set()
    S_last = set()
    for kind in "EF":
        pairs = set()
        for T in toolsets:
            for Tf in submasks(T):
                if kind == "E":
                    U = 0
                    for x in bits(T):
                        U |= sf.NEstar[x]
                    Pi = 0
                    for x in bits(Tf):
                        Pi |= sf.sdn[x]
                    pairs.add((U, Pi))
                else:
                    U = 0
                    for y in bits(T):
                        U |= sf.NFstar[y]
                    Pi = 0
                    for y in bits(Tf):
                        Pi |= sf.sup[y]
                    pairs.add((U, Pi))
        for (U, Pi) in pairs:
            if kind == "E":
                base = sf.enon & ~U & ~Pi
                for Phi in submasks(U):
                    if pc(Phi) <= 9 * k:
                        S_af.add(full & ~sf.upc(base | Phi))
            else:
                bases_af = {sf.fnon & ~U & ~Pi}
                bases_all = {sf.fnon & ~U & ~(Pi | au) for au in anc_up}
                for base in bases_all:
                    for Phi in submasks(U):
                        if pc(Phi) <= 9 * k:
                            S_last.add(sf.dnc(base | Phi))
                for base in bases_af:
                    for Phi in submasks(U):
                        if pc(Phi) <= 9 * k:
                            S_af.add(sf.dnc(base | Phi))
    S_last |= S_af
    Y = {full}
    for _ in range(k - 1):
        Y = Y | {y & d for y in Y for d in S_af}
    for y in Y:
        for d in S_last:
            if sf.connects(y & d):
                return True
    return False
