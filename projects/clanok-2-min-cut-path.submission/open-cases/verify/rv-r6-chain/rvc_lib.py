"""rv-r6-chain: own library for the end-to-end check of the chain
    graph of DC  ->  ZZ + P2 (theory-dc.md Theorem 13(a))  ->  general switch form (r4-general.md §5.1)
    ->  terms and intersections of terms (r5-core.md §6.1, §6.3, §8.2: Lemma 8.1, Theorem 8.2, IDESC).
Written from the definitions in those texts; no code of other agents is imported here.

Conventions: sets of vertices / elements / switches / nodes are Python ints used as bit masks.
"""
import math
from collections import deque


def bits(m):
    out = []
    while m:
        low = m & -m
        out.append(low.bit_length() - 1)
        m ^= low
    return out


def popcount(m):
    return bin(m).count("1")


# =====================================================================================================================
# graphs, flows, closures
# =====================================================================================================================

class Graph:
    def __init__(self, n, edges):
        self.n = n
        es = set()
        for a, b in edges:
            a, b = int(a), int(b)
            if a == b:
                raise ValueError("loop")
            es.add((min(a, b), max(a, b)))
        self.edges = sorted(es)
        self.adj = [[] for _ in range(n)]
        for a, b in self.edges:
            self.adj[a].append(b)
            self.adj[b].append(a)

    def dist_from(self, s):
        d = [-1] * self.n
        d[s] = 0
        dq = deque([s])
        while dq:
            a = dq.popleft()
            for b in self.adj[a]:
                if d[b] < 0:
                    d[b] = d[a] + 1
                    dq.append(b)
        return d

    def unit_cap(self, vertices=None):
        cap = [dict() for _ in range(self.n)]
        for a, b in self.edges:
            if vertices is not None and (a not in vertices or b not in vertices):
                continue
            cap[a][b] = cap[a].get(b, 0) + 1
            cap[b][a] = cap[b].get(a, 0) + 1
        return cap


def maxflow(n, cap, s, t, limit=None):
    """Integer maximum flow on an undirected (multi)graph given by symmetric capacities cap[a][b]; BFS augmenting
    paths. Returns (value, f) with f[a][b] the (skew-symmetric) flow."""
    f = [dict() for _ in range(n)]
    val = 0
    while limit is None or val < limit:
        par = {s: s}
        dq = deque([s])
        while dq and t not in par:
            a = dq.popleft()
            fa = f[a]
            for b, c in cap[a].items():
                if b not in par and c - fa.get(b, 0) > 0:
                    par[b] = a
                    dq.append(b)
        if t not in par:
            break
        bott = None
        b = t
        while b != s:
            a = par[b]
            r = cap[a][b] - f[a].get(b, 0)
            bott = r if bott is None else min(bott, r)
            b = a
        if limit is not None:
            bott = min(bott, limit - val)
        b = t
        while b != s:
            a = par[b]
            f[a][b] = f[a].get(b, 0) + bott
            f[b][a] = f[b].get(a, 0) - bott
            b = a
        val += bott
    return val, f


def residual_reach(n, cap, f):
    """reach[x] = bit mask of the vertices reachable from x by residual arcs (cap - f > 0)."""
    radj = [[b for b, c in cap[a].items() if c - f[a].get(b, 0) > 0] for a in range(n)]
    reach = [0] * n
    for x in range(n):
        seen = 1 << x
        st = [x]
        while st:
            a = st.pop()
            for b in radj[a]:
                if not (seen >> b) & 1:
                    seen |= 1 << b
                    st.append(b)
        reach[x] = seen
    return reach


def bridges(G):
    """Bridges of G (iterative lowlink)."""
    n = G.n
    disc = [-1] * n
    low = [0] * n
    out = set()
    timer = 0
    for r in range(n):
        if disc[r] >= 0:
            continue
        disc[r] = low[r] = timer
        timer += 1
        stack = [[r, -1, 0]]
        while stack:
            fr = stack[-1]
            x, p, i = fr
            if i < len(G.adj[x]):
                fr[2] += 1
                y = G.adj[x][i]
                if y == p:
                    continue          # simple graph: the parent edge is the only edge to p
                if disc[y] < 0:
                    disc[y] = low[y] = timer
                    timer += 1
                    stack.append([y, x, 0])
                else:
                    low[x] = min(low[x], disc[y])
            else:
                stack.pop()
                if p >= 0:
                    low[p] = min(low[p], low[x])
                    if low[x] > disc[p]:
                        out.add((min(p, x), max(p, x)))
    return out


def conn3(G, x, y, cap=None):
    """min(c(x, y), 3)."""
    if cap is None:
        cap = G.unit_cap()
    return maxflow(G.n, cap, x, y, limit=3)[0]


def dc_test(G):
    """G in DC: every pair has d <= 2 or c <= 2.  c >= 3 is an equivalence relation; vertices of degree <= 2 are
    singleton classes; pairs inside a class must be at distance <= 2.  Returns (ok, first bad pair or None)."""
    n = G.n
    cap = G.unit_cap()
    cls = [-1] * n
    reps = []
    for x in range(n):
        if len(G.adj[x]) < 3:
            cls[x] = len(reps)
            reps.append(x)
            continue
        found = False
        for ci, r in enumerate(reps):
            if len(G.adj[r]) >= 3 and maxflow(n, cap, r, x, limit=3)[0] >= 3:
                cls[x] = ci
                found = True
                break
        if not found:
            cls[x] = len(reps)
            reps.append(x)
    members = {}
    for x in range(n):
        members.setdefault(cls[x], []).append(x)
    for ci, mem in members.items():
        if len(mem) < 2:
            continue
        ms = set(mem)
        for x in mem:
            near = {x}
            for y in G.adj[x]:
                near.add(y)
                near.update(G.adj[y])
            bad = ms - near
            if bad:
                return False, (x, min(bad))
    return True, None


# =====================================================================================================================
# brute force for cp(u,v) = c(u,v) from the definition (two independent methods)
# =====================================================================================================================

def has_path_in(n, edge_list, u, v):
    adj = [[] for _ in range(n)]
    for a, b in edge_list:
        adj[a].append(b)
        adj[b].append(a)
    seen = {u}
    st = [u]
    while st:
        a = st.pop()
        if a == v:
            return True
        for b in adj[a]:
            if b not in seen:
                seen.add(b)
                st.append(b)
    return False


def brute_subsets(G, u, v):
    """All vertex sets A with u in A, v not in A (numpy table); returns (c, answer, number of minimum cuts)."""
    import numpy as np
    n = G.n
    others = [x for x in range(n) if x not in (u, v)]
    k = len(others)
    if k > 22:
        raise ValueError("too large")
    masks = np.arange(1 << k, dtype=np.int64)
    side = np.zeros((n, 1 << k), dtype=bool)
    side[u, :] = True
    for i, x in enumerate(others):
        side[x, :] = ((masks >> i) & 1).astype(bool)
    cut = np.zeros(1 << k, dtype=np.int32)
    for a, b in G.edges:
        cut += side[a] ^ side[b]
    c = int(cut.min())
    idx = np.nonzero(cut == c)[0]
    ans = False
    for mk in idx:
        A = {u} | {others[i] for i in range(k) if (int(mk) >> i) & 1}
        ce = [(a, b) for a, b in G.edges if (a in A) != (b in A)]
        if has_path_in(n, ce, u, v):
            ans = True
            break
    return c, ans, len(idx)


def brute_core(G, u, v, kmax=24, chunk=1 << 20):
    """Subset table over the core (vertices of degree >= 3, and u, v) for graphs whose other vertices have degree
    exactly 2, both neighbours in the core (the realised graphs of Theorem 13(b)).  Exact by elementary counting: the
    non-core vertices are pairwise non-adjacent, so each is placed independently and contributes min = 1 if its two
    neighbours are split, 0 otherwise; in a minimum cut each has at most one cut edge, so no u-v path inside a
    minimum cut passes through it.  Returns (c, answer, number of minimum core traces) or raises ValueError."""
    import numpy as np
    n = G.n
    core = [x for x in range(n) if len(G.adj[x]) >= 3 or x in (u, v)]
    cs = set(core)
    pairw = {}
    for x in range(n):
        if x in cs:
            continue
        if len(G.adj[x]) != 2 or any(y not in cs for y in G.adj[x]):
            raise ValueError("not core + independent degree-2 vertices")
        p, s = sorted(G.adj[x])
        pairw[(p, s)] = pairw.get((p, s), 0) + 1
    others = [x for x in core if x not in (u, v)]
    k = len(others)
    if k > kmax:
        raise ValueError("core too large")
    pos = {u: -1, v: -2}
    for i, x in enumerate(others):
        pos[x] = i
    cedges = [(a, b) for a, b in G.edges if a in cs and b in cs]
    terms = {}
    for a, b in cedges:
        key = (min(a, b), max(a, b))
        terms[key] = terms.get(key, 0) + 1
    for key, w in pairw.items():
        terms[key] = terms.get(key, 0) + w
    total = 1 << k
    best = None
    mins = []

    def side(arr, x):
        if x == u:
            return np.ones(arr.shape, dtype=np.int64)
        if x == v:
            return np.zeros(arr.shape, dtype=np.int64)
        return (arr >> pos[x]) & 1

    for start in range(0, total, chunk):
        arr = np.arange(start, min(total, start + chunk), dtype=np.int64)
        cut = np.zeros(arr.shape, dtype=np.int32)
        for (a, b), w in terms.items():
            cut += w * (side(arr, a) ^ side(arr, b)).astype(np.int32)
        mn = int(cut.min())
        if best is None or mn < best:
            best = mn
            mins = [arr[cut == mn]]
        elif mn == best:
            mins.append(arr[cut == mn])
    M = np.concatenate(mins)
    # vectorised reachability from u through crossing core edges
    reach = np.zeros(M.shape, dtype=np.int64)          # bit i: others[i]; bit k: u; bit k+1: v
    bitpos = dict(pos)
    bitpos[u] = k
    bitpos[v] = k + 1
    reach |= np.int64(1) << k
    cross = []
    for a, b in cedges:
        cr = (side(M, a) ^ side(M, b)).astype(bool)
        cross.append((bitpos[a], bitpos[b], cr))
    for _ in range(len(core) + 1):
        old = reach.copy()
        for ba, bb, cr in cross:
            ra = ((reach >> ba) & 1).astype(bool) & cr
            rb = ((reach >> bb) & 1).astype(bool) & cr
            reach |= ra.astype(np.int64) << bb
            reach |= rb.astype(np.int64) << ba
        if np.array_equal(old, reach):
            break
    ans = bool(((reach >> (k + 1)) & 1).any())
    return best, ans, int(M.shape[0])


def brute_paths(G, u, v, budget=2_000_000):
    """Lemma 6 (Picard-Queyranne) on every alternating u-v walk: a walk with even vertices X and odd vertices Y lies
    in a minimum cut iff cl(X) (residual closure of a maximum flow) misses Y and v.  Exhaustive search over the
    states (vertex, closure of the even vertices, set of odd vertices); a walk inside a minimum cut contains a path
    inside it, so this decides cp = c exactly.  Returns (c, answer, states) or raises RuntimeError on budget."""
    n = G.n
    cap = G.unit_cap()
    c, f = maxflow(n, cap, u, v)
    reach = residual_reach(n, cap, f)
    # rreach[y] = vertices from which y is reachable (they lie outside every closed set that misses y)
    rreach = [0] * n
    for x in range(n):
        for y in bits(reach[x]):
            rreach[y] |= 1 << x
    vb = 1 << v
    C0 = reach[u]
    Out0 = rreach[v]
    assert not C0 & Out0
    # state: (even vertex x, C = closure of the even vertices, Out = co-closure of the odd vertices and v);
    # an odd y is allowed iff y not in C; an even z iff z not in Out (then C | reach[z] misses Out automatically).
    seen = set()
    stack = [(u, C0, Out0)]
    states = 0
    while stack:
        x, C, Out = stack.pop()
        key = (x, C, Out)
        if key in seen:
            continue
        seen.add(key)
        states += 1
        if states > budget:
            raise RuntimeError("budget")
        for y in G.adj[x]:              # odd vertex
            if (C >> y) & 1:
                continue
            if y == v:
                return c, True, states
            Out2 = Out | rreach[y]
            for z in G.adj[y]:          # next even vertex
                if (Out2 >> z) & 1:
                    continue
                C2 = C | reach[z]
                if C2 & Out2:
                    continue
                stack.append((z, C2, Out2))
    return c, False, states


# =====================================================================================================================
# Theorem 13(a): graph -> ZZ + P2, and the lift of a down-set back to a cut of G
# =====================================================================================================================

class ZZ:
    """(q, le, R, u, v): le[a][b] = a <= b (preorder), R = sorted list of (a, b) with a < b strictly."""

    def __init__(self, q, le, R, u, v):
        self.q, self.le, self.u, self.v = q, [list(map(bool, r)) for r in le], u, v
        RR = set()
        for a, b in R:
            a, b = int(a), int(b)
            if self.lt(a, b):
                RR.add((a, b))
            elif self.lt(b, a):
                RR.add((b, a))
            else:
                raise ValueError("R-edge between incomparable or equivalent elements %r" % ((a, b),))
        self.R = sorted(RR)
        self.down = [sum(1 << a for a in range(q) if self.le[a][x]) for x in range(q)]
        self.up = [sum(1 << b for b in range(q) if self.le[x][b]) for x in range(q)]
        self.lo = [0] * q
        self.hi = [0] * q
        for a, b in self.R:
            self.hi[a] |= 1 << b
            self.lo[b] |= 1 << a

    def lt(self, a, b):
        return self.le[a][b] and not self.le[b][a]

    def check_preorder(self):
        q, le = self.q, self.le
        for a in range(q):
            if not le[a][a]:
                return False
            for b in range(q):
                if le[a][b]:
                    for c in range(q):
                        if le[b][c] and not le[a][c]:
                            return False
        return all(le[self.u][x] and le[x][self.v] for x in range(q)) and (self.u, self.v) not in self.R

    def p2_bad(self):
        q, le = self.q, self.le
        bad = []
        for x in range(q):
            for y in range(x + 1, q):
                if le[x][y] or le[y][x]:
                    continue
                if not ((self.lo[x] & self.lo[y]) or (self.hi[x] & self.hi[y])):
                    bad.append((x, y))
        return bad

    def exact(self, budget=None):
        """Own exact solver: search over zigzags u = x0 < x1 > x2 < ... with the down-closure Dn of the valleys and
        the up-closure Up of the peaks; consistent iff Dn and Up are disjoint.  Memoised on (x, role, Dn, Up)."""
        u, v = self.u, self.v
        seen = set()
        stack = [(u, True, self.down[u], 0)]
        while stack:
            x, val, Dn, Up = stack.pop()
            key = (x, val, Dn, Up)
            if key in seen:
                continue
            seen.add(key)
            if budget is not None and len(seen) > budget:
                raise RuntimeError("budget")
            if val:
                for y in bits(self.hi[x]):
                    U2 = Up | self.up[y]
                    if U2 & Dn:
                        continue
                    if y == v:
                        return True
                    stack.append((y, False, Dn, U2))
            else:
                for y in bits(self.lo[x]):
                    D2 = Dn | self.down[y]
                    if D2 & Up:
                        continue
                    stack.append((y, True, D2, Up))
        return False


class GraphToZZ:
    """theory-dc.md Theorem 13(a) with Lemma 1, Lemma 4, Proposition 5, executed literally."""

    def __init__(self, G, u, v):
        self.G, self.u, self.v = G, u, v
        n = G.n
        br = bridges(G)
        # Lemma 1: component K of u in G minus the bridges
        adjK = [[b for b in G.adj[a] if (min(a, b), max(a, b)) not in br] for a in range(n)]
        K = {u}
        st = [u]
        while st:
            a = st.pop()
            for b in adjK[a]:
                if b not in K:
                    K.add(b)
                    st.append(b)
        if v not in K:
            raise ValueError("v not in the 2-edge-connected component of u (c(u,v) <= 1)")
        self.K = K
        capK = G.unit_cap(K)
        # Q = {u} + {x in K : c_K(u, x) >= 3}
        # (a vertex of degree <= 2 has c(u, x) <= 2)
        Q = [u] + [x for x in sorted(K) if x != u and len(adjK[x]) >= 3 and maxflow(n, capK, u, x, limit=3)[0] >= 3]
        Qs = set(Q)
        if v not in Qs:
            raise ValueError("c(u,v) < 3")
        # ears: components of K - Q, each with exactly two boundary edges
        ears = []
        rest = K - Qs
        seen = set()
        for x in sorted(rest):
            if x in seen:
                continue
            X = {x}
            seen.add(x)
            st = [x]
            while st:
                a = st.pop()
                for b in adjK[a]:
                    if b in rest and b not in X:
                        X.add(b)
                        seen.add(b)
                        st.append(b)
            bd = [(a, b) for a in X for b in adjK[a] if b not in X]
            if len(bd) != 2:
                raise AssertionError("ear with %d boundary edges" % len(bd))
            (a1, p), (a2, s) = bd
            if p not in Qs or s not in Qs:
                raise AssertionError("ear attached outside Q")
            ears.append((frozenset(X), p, s))
        self.ears = ears
        qi = {x: i for i, x in enumerate(Q)}
        self.Q, self.qi = Q, qi
        q = len(Q)
        # multigraph H on Q: real edges of K[Q] plus ear edges
        capH = [dict() for _ in range(q)]
        real = []
        for a, b in G.edges:
            if a in Qs and b in Qs:
                ia, ib = qi[a], qi[b]
                real.append((ia, ib))
                capH[ia][ib] = capH[ia].get(ib, 0) + 1
                capH[ib][ia] = capH[ib].get(ia, 0) + 1
        for X, p, s in ears:
            if p != s:
                ip, is_ = qi[p], qi[s]
                capH[ip][is_] = capH[ip].get(is_, 0) + 1
                capH[is_][ip] = capH[is_].get(ip, 0) + 1
        self.real = real
        iu, iv = qi[u], qi[v]
        cH, fH = maxflow(q, capH, iu, iv)
        self.c = cH
        reach = residual_reach(q, capH, fH)
        full = (1 << q) - 1
        Cy = []
        for y in range(q):
            cy = reach[iu] | reach[y]
            if (cy >> iv) & 1:
                cy = full
            Cy.append(cy)
        le = [[bool((Cy[y] >> x) & 1) for y in range(q)] for x in range(q)]
        R = []
        for ia, ib in real:
            if le[ia][ib] and le[ib][ia]:
                continue                      # equivalent: never cut by a minimum cut
            if not (le[ia][ib] or le[ib][ia]):
                raise AssertionError("Proposition 11 fails: real edge between incomparable elements")
            R.append((ia, ib))
        self.zz = ZZ(q, le, R, iu, iv)

    def lift(self, Dq):
        """A down-set Dq of the ZZ elements (bit mask over Q indices, containing u, not v) -> vertex set A of G:
        Q-part, ears on the side of an attachment in A, the parts outside K on the side of their bridge end."""
        G = self.G
        A = {self.Q[i] for i in bits(Dq)}
        for X, p, s in self.ears:
            if p in A or s in A:
                A |= X
        # outside K: attach through bridges
        outside = set(range(G.n)) - self.K
        if outside:
            side = {x: (x in A) for x in self.K}
            dq = deque(self.K)
            while dq:
                a = dq.popleft()
                for b in G.adj[a]:
                    if b not in side:
                        side[b] = side[a]
                        dq.append(b)
            A = {x for x, s_ in side.items() if s_}
        return A

    def cut_check(self, A):
        """(cut size of A in G, does the cut contain a u-v path)."""
        G = self.G
        ce = [(a, b) for a, b in G.edges if (a in A) != (b in A)]
        return len(ce), has_path_in(G.n, ce, self.u, self.v)


def realise(z, M=1):
    """theory-dc.md Theorem 13(b): ZZ instance -> simple graph G(Pi) (ear vertices of degree two).  Returns (n,
    edges)."""
    q, le, u, v = z.q, z.le, z.u, z.v
    Rset = set(z.R)
    edges = []
    nxt = [q]

    def ear(x, y):
        w = nxt[0]
        nxt[0] += 1
        edges.append((x, w))
        edges.append((y, w))

    for a in range(q):
        for b in range(q):
            if a != b and le[a][b] and not le[b][a]:
                if (a, b) in Rset:
                    edges.append((a, b))
                else:
                    ear(a, b)
                if a != u:
                    ear(u, a)
                if b != v:
                    ear(b, v)
    for a in range(q):
        for b in range(a + 1, q):
            if le[a][b] and le[b][a]:
                for _ in range(M):
                    ear(a, b)
    return nxt[0], edges


# =====================================================================================================================
# general switch form (r4-general.md §5.1), own conversion
# =====================================================================================================================

class SF:
    def __init__(self, z):
        q, le, u, v = z.q, z.le, z.u, z.v
        self.z = z
        Bc = [x for x in range(q) if le[x][u] and le[u][x]]
        Tc = [x for x in range(q) if le[x][v] and le[v][x]]
        if set(Bc) & set(Tc):
            raise ValueError("u equivalent to v")
        Bs, Ts = set(Bc), set(Tc)
        mid = [x for x in range(q) if x not in Bs and x not in Ts]
        self.mid = mid
        idx = {x: i for i, x in enumerate(mid)}
        self.idx = idx
        m = len(mid)
        self.m = m
        par = {x: x for x in Bc + Tc}

        def find(a):
            while par[a] != a:
                par[a] = par[par[a]]
                a = par[a]
            return a
        for a, b in z.R:
            if a in Bs and b in Ts:
                ra, rb = find(a), find(b)
                if ra != rb:
                    par[ra] = rb
        node = {}
        roots = {}
        for x in Bc + Tc:
            r = find(x)
            if r not in roots:
                roots[r] = len(roots)
            node[x] = roots[r]
        self.node = node
        N = len(roots)
        E = [0] * m
        F = [0] * m
        priv = {}
        for a, b in z.R:
            if a in idx and b in idx:
                priv[(idx[a], idx[b])] = N
                F[idx[a]] |= 1 << N
                E[idx[b]] |= 1 << N
                N += 1
            elif a in idx:
                if b not in Ts:
                    raise AssertionError("upper neighbour of a middle element neither middle nor top")
                F[idx[a]] |= 1 << node[b]
            elif b in idx:
                if a not in Bs:
                    raise AssertionError("lower neighbour of a middle element neither middle nor bottom")
                E[idx[b]] |= 1 << node[a]
            else:
                if not (a in Bs and b in Ts):
                    raise AssertionError("edge between bottoms or between tops")
        self.N, self.E, self.F, self.priv = N, E, F, priv
        self.s, self.t = node[u], node[v]
        self.le = [[le[mid[i]][mid[j]] for j in range(m)] for i in range(m)]
        self.up = [sum(1 << j for j in range(m) if self.le[i][j]) for i in range(m)]
        self.down = [sum(1 << j for j in range(m) if self.le[j][i]) for i in range(m)]
        self.cls = [self.up[i] & self.down[i] for i in range(m)]
        self.sdown = [self.down[i] & ~self.cls[i] for i in range(m)]
        self.sup = [self.up[i] & ~self.cls[i] for i in range(m)]
        self.full = (1 << m) - 1
        self.LMN = [0] * m
        self.UMN = [0] * m
        for (i, j) in priv:
            self.UMN[i] |= 1 << j
            self.LMN[j] |= 1 << i
        self.Enon = sum(1 << i for i in range(m) if E[i])
        self.Fnon = sum(1 << i for i in range(m) if F[i])
        # stars (r5-core.md §6.3)
        self.Esh = []
        self.Fsh = []
        for w in range(m):
            e = E[w]
            for zz_ in bits(self.LMN[w]):
                for v2 in bits(self.UMN[zz_]):
                    e |= 1 << priv[(zz_, v2)]
            self.Esh.append(e)
            f = F[w]
            for zz_ in bits(self.UMN[w]):
                for v2 in bits(self.LMN[zz_]):
                    f |= 1 << priv[(v2, zz_)]
            self.Fsh.append(f)
        self._NE = {}
        self._NF = {}

    # ------------------------------------------------------------------ basic operations
    def upclose(self, S):
        r = 0
        for x in bits(S):
            r |= self.up[x]
        return r

    def downclose(self, S):
        r = 0
        for x in bits(S):
            r |= self.down[x]
        return r

    def is_down(self, D):
        return all((self.down[x] & ~D) == 0 for x in bits(D))

    def NE(self, Z):
        r = self._NE.get(Z)
        if r is None:
            r = sum(1 << w for w in range(self.m) if self.E[w] & Z)
            self._NE[Z] = r
        return r

    def NF(self, Z):
        r = self._NF.get(Z)
        if r is None:
            r = sum(1 << w for w in range(self.m) if self.F[w] & Z)
            self._NF[Z] = r
        return r

    def connects(self, D):
        if self.s == self.t:
            return True
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

    def p2_bad(self):
        """P2 in switch form: incomparable x, y need a common node (E or F) or a lower / upper middle witness."""
        bad = []
        for x in range(self.m):
            for y in range(x + 1, self.m):
                if self.le[x][y] or self.le[y][x]:
                    continue
                if self.E[x] & self.E[y] or self.F[x] & self.F[y]:
                    continue
                if self.LMN[x] & self.LMN[y] or self.UMN[x] & self.UMN[y]:
                    continue
                bad.append((x, y))
        return bad

    def lift_down(self, D):
        """Down-set of switches -> down-set of the ZZ elements (bit mask over Q indices): D plus the class of u."""
        z = self.z
        r = 0
        for x in range(z.q):
            if z.le[x][z.u] and z.le[z.u][x]:
                r |= 1 << x
        for i in bits(D):
            r |= 1 << self.mid[i]
        return r

    # ------------------------------------------------------------------ exact answers
    def sides(self):
        out = []
        for w in range(self.m):
            if self.E[w]:
                out.append((w, 0))
            if self.F[w]:
                out.append((w, 1))
        return out

    def smask(self, X):
        return self.F[X[0]] if X[1] else self.E[X[0]]

    def brute(self, cap=1 << 22):
        """Enumerate all down-sets of the switch preorder (tie classes in a linear extension: a class may join D
        iff everything strictly below it is in D); True iff one connects s and t."""
        m = self.m
        classes = []
        seen = 0
        for i in sorted(range(m), key=lambda i: popcount(self.down[i])):
            if (seen >> i) & 1:
                continue
            classes.append((self.cls[i], self.sdown[i]))
            seen |= self.cls[i]
        cnt = [0]

        def rec(k, D):
            if k == len(classes):
                cnt[0] += 1
                if cnt[0] > cap:
                    raise RuntimeError("cap")
                return self.connects(D)
            c, sd = classes[k]
            if rec(k + 1, D):
                return True
            if (sd & ~D) == 0 and rec(k + 1, D | c):
                return True
            return False

        return rec(0, 0)

    def count_downsets(self, cap=1 << 22):
        m = self.m
        classes = []
        seen = 0
        for i in sorted(range(m), key=lambda i: popcount(self.down[i])):
            if (seen >> i) & 1:
                continue
            classes.append((self.cls[i], self.sdown[i]))
            seen |= self.cls[i]
        out = []

        def rec(k, D):
            if len(out) > cap:
                raise RuntimeError("cap")
            if k == len(classes):
                out.append(D)
                return
            c, sd = classes[k]
            rec(k + 1, D)
            if (sd & ~D) == 0:
                rec(k + 1, D | c)

        rec(0, 0)
        return out

    def shortest(self):
        """BFS over (side, Up, Dn): Up = up-closure of the E-members, Dn = down-closure of the F-members.  Returns the
        least number of sides of a valid path, 0 if s = t, None if there is none."""
        if self.s == self.t:
            return 0
        sides = self.sides()
        start = []
        for X in sides:
            if (self.smask(X) >> self.s) & 1:
                w, ty = X
                st = (X, self.up[w], 0) if ty == 0 else (X, 0, self.down[w])
                start.append(st)
        seen = set(start)
        layer = start
        r = 1
        adjs = {X: [Y for Y in sides if Y != X and self.smask(X) & self.smask(Y)] for X in sides}
        while layer:
            for (X, Up, Dn) in layer:
                if (self.smask(X) >> self.t) & 1:
                    return r
            nxt = []
            for (X, Up, Dn) in layer:
                for Y in adjs[X]:
                    w, ty = Y
                    if ty == 0:
                        if (Dn >> w) & 1:
                            continue
                        st = (Y, Up | self.up[w], Dn)
                    else:
                        if (Up >> w) & 1:
                            continue
                        st = (Y, Up, Dn | self.down[w])
                    if st not in seen:
                        seen.add(st)
                        nxt.append(st)
            layer = nxt
            r += 1
        return None

    def all_shortest(self, L, limit=50):
        """All valid paths with exactly L sides (at most `limit`), by DFS with the side-graph distance to t."""
        sides = self.sides()
        adjs = {X: [Y for Y in sides if Y != X and self.smask(X) & self.smask(Y)] for X in sides}
        dist = {X: None for X in sides}
        dq = deque()
        for X in sides:
            if (self.smask(X) >> self.t) & 1:
                dist[X] = 1
                dq.append(X)
        while dq:
            X = dq.popleft()
            for Y in adjs[X]:
                if dist[Y] is None:
                    dist[Y] = dist[X] + 1
                    dq.append(Y)
        out = []

        def rec(path, Up, Dn):
            if len(out) >= limit:
                return
            X = path[-1]
            if len(path) == L:
                if (self.smask(X) >> self.t) & 1:
                    out.append(list(path))
                return
            for Y in adjs[X]:
                if Y in path or dist[Y] is None or dist[Y] > L - len(path):
                    continue
                w, ty = Y
                if ty == 0:
                    if (Dn >> w) & 1:
                        continue
                    rec(path + [Y], Up | self.up[w], Dn)
                else:
                    if (Up >> w) & 1:
                        continue
                    rec(path + [Y], Up, Dn | self.down[w])

        for X in sides:
            if (self.smask(X) >> self.s) & 1 and dist[X] is not None and dist[X] <= L:
                w, ty = X
                if ty == 0:
                    rec([X], self.up[w], 0)
                else:
                    rec([X], 0, self.down[w])
        return out

    # ------------------------------------------------------------------ terms (r5-core.md §8.2)
    def eterm(self, T, Tflag, Y0, Phi):
        U = 0
        for x in bits(T):
            U |= self.NE(self.Esh[x])
        S = self.downclose(Y0)
        for x in bits(Tflag):
            S |= self.sdown[x]
        Gm = (self.Enon & ~U & ~S) | Phi
        return self.full & ~self.upclose(Gm), U, Gm

    def fterm(self, T, Tflag, X0, Phi):
        U = 0
        for y in bits(T):
            U |= self.NF(self.Fsh[y])
        S = self.upclose(X0)
        for y in bits(Tflag):
            S |= self.sup[y]
        Gm = (self.Fnon & ~U & ~S) | Phi
        return self.downclose(Gm), U, Gm


# =====================================================================================================================
# Lemma 8.1 / Theorem 8.2 executed on a shortest valid path (own implementation)
# =====================================================================================================================

PREFER_DAMAGE = False
HALF = False     # True: light threshold |A'|/2 (exercises the recursion on small instances; damage bound not checked)


def game_value(rows, cols, M):
    """Value of the zero-sum game (row player maximises) with 0/1 payoff M[i][j]; LP by scipy."""
    import numpy as np
    from scipy.optimize import linprog
    nr, nc = len(rows), len(cols)
    # variables p_1..p_nr, v ; maximise v: minimise -v
    c = np.zeros(nr + 1)
    c[-1] = -1.0
    A_ub = np.zeros((nc, nr + 1))
    for j in range(nc):
        for i in range(nr):
            A_ub[j, i] = -M[i][j]
        A_ub[j, -1] = 1.0
    b_ub = np.zeros(nc)
    A_eq = np.zeros((1, nr + 1))
    A_eq[0, :nr] = 1.0
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=[1.0], bounds=[(0, None)] * nr + [(None, None)],
                  method="highs")
    if res.status != 0:
        raise RuntimeError("LP failed: %s" % res.message)
    return float(res.x[-1]), [float(x) for x in res.x[:nr]]


def min_cover(universe, sets, cap=None, weights=None):
    """Least number of the given sets (list of bit masks) covering `universe` (bit mask); exact by ILP (scipy milp).
    Returns (size, list of indices) or (None, None) if impossible."""
    import numpy as np
    from scipy.optimize import milp, LinearConstraint, Bounds
    els = bits(universe)
    if not els:
        return 0, []
    nS = len(sets)
    if nS == 0:
        return None, None
    U = 0
    for s_ in sets:
        U |= s_
    if universe & ~U:
        return None, None
    A = np.zeros((len(els), nS))
    for i, e in enumerate(els):
        for j, s_ in enumerate(sets):
            if (s_ >> e) & 1:
                A[i, j] = 1.0
    cvec = np.ones(nS) if weights is None else np.array(weights, dtype=float)
    res = milp(c=cvec, constraints=LinearConstraint(A, lb=np.ones(len(els)), ub=np.full(len(els), np.inf)),
               integrality=np.ones(nS), bounds=Bounds(0, 1))
    if res.status != 0:
        raise RuntimeError("milp failed: %s" % res.message)
    chosen = [j for j in range(nS) if res.x[j] > 0.5]
    # verify
    cov = 0
    for j in chosen:
        cov |= sets[j]
    assert not universe & ~cov
    return len(chosen), chosen


class PathData:
    def __init__(self, sf, P):
        self.sf, self.P = sf, P
        WE = sum(1 << w for w, ty in P if ty == 0)
        WF = sum(1 << w for w, ty in P if ty == 1)
        self.WE, self.WF = WE, WF
        self.Up = sf.upclose(WE)
        self.L = sf.downclose(WF)
        if self.Up & self.L:
            raise AssertionError("path not valid")
        self.A = sum(1 << a for a in bits(WE) if not (sf.sdown[a] & WE))
        self.B = sum(1 << b for b in bits(WF) if not (sf.sup[b] & WF))
        self.NEset = self.L & sf.Enon
        self.NFset = self.Up & sf.Fnon
        self.pos = {w: i for i, (w, ty) in enumerate(P)}


def level(sf, pd, Ap, k, N, errs, info):
    """One application of Lemma 8.1 to the residue Ap.  Returns (term description, D, final flag, A'')."""
    m = sf.m
    nA = popcount(Ap)
    theta = nA / 2 if HALF else nA / (2 * k)
    Rr = sf.upclose(Ap) & sf.Fnon
    Cc = pd.NEset
    rows, cols = bits(Rr), bits(Cc)
    dam = {x: Ap & sf.sdown[x] for x in rows}
    light = {x: popcount(dam[x]) <= theta for x in rows}
    covE = {x: (sf.NE(sf.Esh[x]) | (sf.sdown[x] if light[x] else 0)) & Cc for x in rows}
    covF = {y: (sf.NF(sf.Fsh[y]) | (sf.sup[y] if (pd.B >> y) & 1 else 0)) & Rr for y in cols}
    info["rows"] = max(info.get("rows", 0), len(rows))
    info["heavy"] = max(info.get("heavy", 0), sum(1 for x in rows if not light[x]))
    # duality claim
    for x in rows:
        if not light[x]:
            continue
        for y in cols:
            if not ((covE[x] >> y) & 1 or (covF[y] >> x) & 1):
                errs.append("duality fails x=%d y=%d" % (x, y))
    # trivial cases
    if not Cc:
        D, U, Gm = sf.eterm(0, 0, 0, 0)
        if pd.L & ~D or D & sf.upclose(Ap):
            errs.append("trivial E-term (C empty) fails")
        return ("E0",), D, True, 0, 0
    if not Rr:
        D, U, Gm = sf.fterm(0, 0, 0, 0)
        if pd.L & ~D or D & sf.upclose(Ap):
            errs.append("trivial F-term (R empty) fails")
        return ("F0",), D, True, 0, 0
    M = [[1 if (covE[x] >> y) & 1 else 0 for y in cols] for x in rows]
    val, p = game_value(rows, cols, M)
    info.setdefault("values", []).append(round(val, 6))
    # E-side: least cover of the columns by cov_E of rows
    wE = None
    if PREFER_DAMAGE:
        # among least covers prefer light rows with non-zero damage (stress test of the recursion; any cover of
        # size <= k is allowed by the proof)
        wE = [0.99 if (light[x] and dam[x]) else 1.0 for x in rows]
    sE, chE = min_cover(Cc, [covE[x] for x in rows], weights=wE)
    # F-side: least cover of the light rows by cov_F of columns; least anchor set for the heavy rows
    lightmask = sum(1 << x for x in rows if light[x])
    heavymask = Rr & ~lightmask
    sF, chF = min_cover(lightmask, [covF[y] for y in cols])
    anc_sets = [sum(1 << x for x in bits(heavymask) if (sf.sdown[x] >> a) & 1) for a in bits(Ap)]
    sA, chA = min_cover(heavymask, anc_sets)
    eps = 1e-7
    okE = sE is not None and sE <= k
    okF = sF is not None and sF <= k and sA is not None and sA <= N
    if val >= 0.5 + eps and not okE:
        errs.append("value %.4f >= 1/2 but least E-cover %s > k = %d" % (val, sE, k))
    if val <= 0.5 - eps and not okF:
        errs.append("value %.4f < 1/2 but least F-cover %s / anchors %s exceed k = %d / N = %d" % (val, sF, sA, k, N))
    if not okE and not okF:
        errs.append("Lemma 8.1 fails: no term (E-cover %s, F-cover %s, anchors %s; k %d, N %d)" % (sE, sF, sA, k, N))
        return None, None, None, None, None
    useE = okE if (val >= 0.5 - eps) else (not okF)
    if useE:
        T = sum(1 << rows[j] for j in chE)
        Tflag = sum(1 << x for x in bits(T) if light[x])
        U = 0
        for x in bits(T):
            U |= sf.NE(sf.Esh[x])
        Phi = Ap & U
        D, U2, Gm = sf.eterm(T, Tflag, 0, Phi)
        if popcount(Phi) > 9 * popcount(T):
            errs.append("flips %d > 9 * tools %d" % (popcount(Phi), popcount(T)))
        App = Ap & ~Gm
        if 2 * popcount(App) > nA and not HALF:
            errs.append("damage %d > |A'|/2 = %.1f" % (popcount(App), nA / 2))
        if D & sf.upclose(Ap) & ~sf.upclose(App):
            errs.append("D(tau) meets up(A') outside up(A'')")
        if pd.L & ~D:
            errs.append("E-term misses L")
        info["tools"] = max(info.get("tools", 0), popcount(T))
        info["flips"] = max(info.get("flips", 0), popcount(Phi))
        info["damage"] = max(info.get("damage", 0), popcount(App))
        return ("E", T, Tflag, 0, Phi), D, App == 0, App, 0
    T = sum(1 << cols[j] for j in chF)
    Tflag = T & pd.B
    X0 = sum(1 << bits(Ap)[j] for j in chA)
    U = 0
    for y in bits(T):
        U |= sf.NF(sf.Fsh[y])
    Phi = pd.B & U
    D, U2, Gm = sf.fterm(T, Tflag, X0, Phi)
    if popcount(Phi) > 9 * popcount(T):
        errs.append("F flips %d > 9 * tools %d" % (popcount(Phi), popcount(T)))
    if D & sf.upclose(Ap):
        errs.append("F-term meets up(A')")
    if pd.L & ~D:
        errs.append("F-term misses L")
    info["tools"] = max(info.get("tools", 0), popcount(T))
    info["flips"] = max(info.get("flips", 0), popcount(Phi))
    info["anchors"] = max(info.get("anchors", 0), popcount(X0))
    return ("F", T, Tflag, X0, Phi), D, True, 0, popcount(X0)


def theorem82(sf, P, errs, info):
    """Run the proof of Theorem 8.2 on the valid path P; returns the final down-set D (or None)."""
    m = sf.m
    pd = PathData(sf, P)
    k = int(math.floor(math.log2(m))) + 1 if m >= 1 else 1
    N = int(math.ceil(2 * k * math.log(m))) if m > 1 else 0
    info["k"], info["N"] = k, N
    # Lemma 6.3 (F1) on this path: stars meet at most 9 (even 5 consecutive) minimal members
    for x in range(m):
        if not (pd.L >> x) & 1:
            Sx = pd.A & sf.NE(sf.Esh[x])
            if popcount(Sx) > 9:
                errs.append("F1: |A cap NE(E#_%d)| = %d > 9" % (x, popcount(Sx)))
            if Sx:
                ps = [pd.pos[a] for a in bits(Sx)]
                sp = max(ps) - min(ps) + 1
                info["span"] = max(info.get("span", 0), sp)
                if sp > 9:
                    errs.append("Lemma 6.3: span %d > 9 (E#_%d)" % (sp, x))
        if not (pd.Up >> x) & 1:
            Sy = pd.B & sf.NF(sf.Fsh[x])
            if popcount(Sy) > 9:
                errs.append("F1 dual: |B cap NF(F#_%d)| = %d > 9" % (x, popcount(Sy)))
            if Sy:
                ps = [pd.pos[b] for b in bits(Sy)]
                sp = max(ps) - min(ps) + 1
                info["span"] = max(info.get("span", 0), sp)
                if sp > 9:
                    errs.append("Lemma 6.3 dual: span %d > 9 (F#_%d)" % (sp, x))
    if pd.A == 0:
        D, _, _ = sf.fterm(0, 0, 0, 0)
        terms = [("F0",)]
        Dall = D
    else:
        Ap = pd.A
        Dall = sf.full
        terms = []
        anchors_total = 0
        while True:
            r = level(sf, pd, Ap, k, N, errs, info)
            if r[0] is None:
                return None, terms, pd
            term, D, final, App, na = r
            if HALF and not final and popcount(App) >= popcount(Ap):
                # no progress with the threshold |A'|/2: this level with the threshold of the proof
                globals()["HALF"] = False
                try:
                    r = level(sf, pd, Ap, k, N, errs, info)
                finally:
                    globals()["HALF"] = True
                if r[0] is None:
                    return None, terms, pd
                term, D, final, App, na = r
                info["fallback"] = info.get("fallback", 0) + 1
            if not sf.is_down(D):
                errs.append("term is not a down-set")
            terms.append(term)
            Dall &= D
            if na and not final:
                errs.append("anchors in a non-final term")
            if final:
                break
            if popcount(App) < 1:
                errs.append("continue case with empty residue")
                break
            Ap = App
            if len(terms) > k and not HALF:
                errs.append("more than k levels")
                break
            if len(terms) > 3 * m + 3:
                errs.append("no termination")
                break
    info["levels"] = max(info.get("levels", 0), len(terms))
    if not sf.is_down(Dall):
        errs.append("intersection not a down-set")
    if pd.L & ~Dall:
        errs.append("final D misses L")
    if Dall & pd.Up:
        errs.append("final D meets Up")
    if not sf.connects(Dall):
        errs.append("final D does not connect s, t")
    return Dall, terms, pd


def idesc_full(sf, k=None, N=None, e=None, want=False):
    """IDESC(k, k, N, e) of r5-core.md §8.3 executed exactly and blindly (no path, no oracle), for small m:
    every term (both kinds, at most k tools, every flag pattern, anchors of any kind counted by the least number of
    generators of the anchored down-set / up-set, at most e flips among the caught switches), deduplicated by its
    down-set D with the least number of anchors; then every intersection of at most k terms with at most N anchors in
    total.  Default parameters: those of Theorem 8.2 (k = floor(log2 m) + 1, N = ceil(2k ln m), e = 9k).
    Returns True iff some intersection connects s and t (and, with want, the number of distinct term down-sets)."""
    import itertools
    m = sf.m
    if m == 0:
        return (sf.connects(0), 0) if want else sf.connects(0)
    if k is None:
        k = int(math.floor(math.log2(m))) + 1
    if N is None:
        N = int(math.ceil(2 * k * math.log(m))) if m > 1 else 0
    if e is None:
        e = 9 * k
    if sf.s == sf.t:
        return (True, 0) if want else True
    # anchored down-sets W = down(Y0) with the least |Y0|; anchored up-sets W' = up(X0) likewise
    downs = sf.count_downsets()
    def maxcls(W):
        return len({min(bits(sf.cls[x])) for x in bits(W) if not (sf.sup[x] & W)})
    def mincls(W):
        return len({min(bits(sf.cls[x])) for x in bits(W) if not (sf.sdown[x] & W)})
    Wd = {}
    for W in downs:
        c_ = maxcls(W)
        if c_ <= N:
            Wd[W] = c_
    Wu = {}
    for W in downs:
        Up = sf.full & ~W              # complements of down-sets are the up-sets
        c_ = mincls(Up)
        if c_ <= N:
            Wu[Up] = c_
    terms = {}                          # D -> least anchors
    sw = list(range(m))

    def add(D, a):
        if a < terms.get(D, N + 1):
            terms[D] = a

    for kind in (0, 1):
        for nt in range(0, min(k, m) + 1):
            for T in itertools.combinations(sw, nt):
                U = 0
                for x in T:
                    U |= sf.NE(sf.Esh[x]) if kind == 0 else sf.NF(sf.Fsh[x])
                Ul = bits(U)
                flipsets = []
                for nf in range(0, min(e, len(Ul)) + 1):
                    for ph in itertools.combinations(Ul, nf):
                        flipsets.append(sum(1 << x for x in ph))
                pivs = set()
                for fl in range(1 << nt):
                    P = 0
                    for i in range(nt):
                        if (fl >> i) & 1:
                            P |= sf.sdown[T[i]] if kind == 0 else sf.sup[T[i]]
                    pivs.add(P)
                seenb = {}
                for P in pivs:
                    for W, a in (Wd.items() if kind == 0 else Wu.items()):
                        S = W | P
                        base = ((sf.Enon if kind == 0 else sf.Fnon) & ~U & ~S)
                        if a < seenb.get(base, N + 1):
                            seenb[base] = a
                for base, a in seenb.items():
                    for Ph in flipsets:
                        Gm = base | Ph
                        D = (sf.full & ~sf.upclose(Gm)) if kind == 0 else sf.downclose(Gm)
                        add(D, a)
    # intersections of at most k terms, at most N anchors in total
    best = dict(terms)
    frontier = dict(terms)
    for D in best:
        if sf.connects(D):
            return (True, len(terms)) if want else True
    for _ in range(k - 1):
        new = {}
        for D1, a1 in frontier.items():
            for D2, a2 in terms.items():
                a = a1 + a2
                if a > N:
                    continue
                D = D1 & D2
                if a < best.get(D, N + 1):
                    best[D] = a
                    new[D] = a
        if not new:
            break
        for D in new:
            if sf.connects(D):
                return (True, len(terms)) if want else True
        frontier = new
    return (False, len(terms)) if want else False


def idesc_small(sf, max_tools=1, max_flips=2, max_anchors=1):
    """Blind exhaustive search over SINGLE terms with reduced parameters (no oracle): sound for every parameter."""
    import itertools
    m = sf.m
    sw = list(range(m))
    for kind in ("E", "F"):
        for nt in range(0, max_tools + 1):
            for T in itertools.combinations(sw, nt):
                Tm = sum(1 << x for x in T)
                U = 0
                for x in T:
                    U |= sf.NE(sf.Esh[x]) if kind == "E" else sf.NF(sf.Fsh[x])
                Ul = bits(U)
                for fl in range(1 << nt):
                    Tflag = sum(1 << T[i] for i in range(nt) if (fl >> i) & 1)
                    for na in range(0, max_anchors + 1):
                        for anc in itertools.combinations(sw, na):
                            Am = sum(1 << x for x in anc)
                            for nf in range(0, max_flips + 1):
                                for ph in itertools.combinations(Ul, nf):
                                    Ph = sum(1 << x for x in ph)
                                    if kind == "E":
                                        D, _, _ = sf.eterm(Tm, Tflag, Am, Ph)
                                    else:
                                        D, _, _ = sf.fterm(Tm, Tflag, Am, Ph)
                                    if sf.connects(D):
                                        return True, (kind, T, Tflag, anc, ph)
    return False, None
