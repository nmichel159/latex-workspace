"""Problem ZZ (theory-dc.md, Theorem 13) on strict partial orders, P2 completion, exact solver and polynomial
relaxations (arc consistency, path consistency) of the path-position CSP.

An instance: n elements 0..n-1, lt[a][b] (strict order, transitive), u = 0 least, v = n-1 greatest, R a set of
pairs (a, b) with lt[a][b] (real edges), (u, v) not in R.  A zigzag is a u-v path of (Q, R) alternating up and down;
consistent iff no valley >= a peak, i.e. iff its edge set lies in one down-set cut (D1-D3 of literature.md).

CSP (path positions): variables 1..L (L odd), value of variable j = an R-edge (t, h), t < h; variable 1 has t = u,
variable L has h = v; consecutive edges j, j+1 share the head (j odd) or the tail (j even); every two edges are
compatible (neither h(e) <= t(e') nor h(e') <= t(e)).  A solution is a u-v walk of length L inside one down-set cut,
which contains a consistent zigzag; conversely a consistent zigzag of length l <= L pads to length L by going back
and forth on its last edge.  So the CSP with L = the largest odd number <= n decides ZZ.
"""
import random
from collections import deque


class ZZ:
    def __init__(self, n, lt, R, u=0, v=None, le=None):
        """lt: strict order (then le = lt plus equality); or le: a preorder (then lt is derived)."""
        if v is None:
            v = n - 1
        self.n, self.u, self.v = n, u, v
        if le is None:
            le = [[lt[a][b] or a == b for b in range(n)] for a in range(n)]
        else:
            lt = [[le[a][b] and not le[b][a] for b in range(n)] for a in range(n)]
        self.le, self.lt = le, lt
        self.R = sorted({(a, b) if lt[a][b] else (b, a) for a, b in R})
        for a, b in self.R:
            assert lt[a][b]

    def adj(self):
        A = [set() for _ in range(self.n)]
        for a, b in self.R:
            A[a].add(b)
            A[b].add(a)
        return A

    def p2_bad(self):
        A = self.adj()
        lt = self.lt
        bad = []
        le = self.le
        for x in range(self.n):
            for y in range(x + 1, self.n):
                if le[x][y] or le[y][x]:
                    continue
                if not any((lt[w][x] and lt[w][y]) or (lt[x][w] and lt[y][w]) for w in A[x] & A[y]):
                    bad.append((x, y))
        return bad


def closure(n, less):
    lt = [[False] * n for _ in range(n)]
    for a, b in less:
        lt[a][b] = True
    for k in range(n):
        for i in range(n):
            if lt[i][k]:
                row = lt[k]
                li = lt[i]
                for j in range(n):
                    if row[j]:
                        li[j] = True
    for i in range(n):
        assert not lt[i][i]
    return lt


def random_order(rng, n, p):
    """u = 0 < everything < v = n-1; random relations on a random linear extension of the middle."""
    perm = list(range(1, n - 1))
    rng.shuffle(perm)
    less = {(0, x) for x in range(1, n)} | {(x, n - 1) for x in range(n - 1)}
    for i in range(len(perm)):
        for j in range(i + 1, len(perm)):
            if rng.random() < p:
                less.add((perm[i], perm[j]))
    return closure(n, less)


def p2_complete(rng, n, lt, R, prefer_uv=0.0):
    """Add R-edges until P2 holds: for an incomparable pair x, y pick a random common bound w (above both or below
    both; u and v always qualify) and add the edges w-x and w-y.  prefer_uv: probability of using u or v."""
    R = set(R)
    while True:
        A = [set() for _ in range(n)]
        for a, b in R:
            A[a].add(b)
            A[b].add(a)
        bad = None
        pairs = [(x, y) for x in range(n) for y in range(x + 1, n) if not lt[x][y] and not lt[y][x]]
        rng.shuffle(pairs)
        for x, y in pairs:
            if not any((lt[w][x] and lt[w][y]) or (lt[x][w] and lt[y][w]) for w in A[x] & A[y]):
                bad = (x, y)
                break
        if bad is None:
            return R
        x, y = bad
        if rng.random() < prefer_uv:
            cands = [0, n - 1]
        else:
            cands = [w for w in range(n) if (lt[w][x] and lt[w][y]) or (lt[x][w] and lt[y][w])]
        w = rng.choice(cands)
        for z in (x, y):
            e = (w, z) if lt[w][z] else (z, w)
            if e != (0, n - 1):
                R.add(e)


def random_zz(rng, n, p_order, p_R, prefer_uv=0.0, p2=True):
    lt = random_order(rng, n, p_order)
    comp = [(a, b) for a in range(n) for b in range(n) if lt[a][b] and (a, b) != (0, n - 1)]
    R = [e for e in comp if rng.random() < p_R]
    if p2:
        R = p2_complete(rng, n, lt, R, prefer_uv)
    return ZZ(n, lt, R)


# ------------------------------------------------------------------------------------------------------------
# exact solver: all down-sets
# ------------------------------------------------------------------------------------------------------------

def downsets(z):
    n, le = z.n, z.le
    below = [0] * n
    for b in range(n):
        m = 1 << b
        for a in range(n):
            if le[a][b]:
                m |= 1 << a
        below[b] = m
    u, v = z.u, z.v
    cand = [x for x in range(n) if x != u and x != v]
    res = set()
    stack = [(0, below[u])]
    while stack:
        i, A = stack.pop()
        while i < len(cand) and (A >> cand[i]) & 1:
            i += 1
        if i == len(cand):
            res.add(A)
            continue
        x = cand[i]
        stack.append((i + 1, A))
        if not (below[x] >> v) & 1:
            stack.append((i + 1, A | below[x]))
    # keep only down-sets: A | below[x] unions are down-sets; the 'skip' branch may later include x via another
    # element's down-closure, which is still a down-set.
    return sorted(res)


def zigzag_in(z, A, adj=None):
    if adj is None:
        adj = z.adj()
    par = {z.u: None}
    dq = deque([z.u])
    while dq:
        x = dq.popleft()
        for y in adj[x]:
            if y not in par and ((A >> x) & 1) != ((A >> y) & 1):
                par[y] = x
                dq.append(y)
    if z.v not in par:
        return None
    p = [z.v]
    while par[p[-1]] is not None:
        p.append(par[p[-1]])
    return p[::-1]


def exact(z):
    adj = z.adj()
    wits = []
    for A in downsets(z):
        p = zigzag_in(z, A, adj)
        if p is not None:
            return True, (A, p)
    return False, None


def all_witness_cuts(z):
    adj = z.adj()
    return [A for A in downsets(z) if zigzag_in(z, A, adj) is not None]


# ------------------------------------------------------------------------------------------------------------
# path-position CSP and its relaxations
# ------------------------------------------------------------------------------------------------------------

class CSP:
    def __init__(self, z, L=None):
        self.z = z
        n = z.n
        if L is None:
            L = n if n % 2 == 1 else n - 1
        self.L = L
        E = z.R
        self.E = E
        D = len(E)
        le = z.le
        self.compat = [0] * D
        for i, (t, h) in enumerate(E):
            m = 0
            for j, (t2, h2) in enumerate(E):
                if not le[h][t2] and not le[h2][t]:
                    m |= 1 << j
            self.compat[i] = m
        self.same_head = [0] * D
        self.same_tail = [0] * D
        for i, (t, h) in enumerate(E):
            for j, (t2, h2) in enumerate(E):
                if h == h2:
                    self.same_head[i] |= 1 << j
                if t == t2:
                    self.same_tail[i] |= 1 << j
        self.first = sum(1 << i for i, (t, h) in enumerate(E) if t == z.u)
        self.last = sum(1 << i for i, (t, h) in enumerate(E) if h == z.v)

    window = None

    def rel(self, j, k, i):
        """bit mask of values of variable k allowed with value i of variable j (j != k, 0-based).
        With self.window = w, compatibility is required only for |j - k| <= w (a weaker CSP)."""
        if self.window is not None and abs(j - k) > self.window:
            return (1 << len(self.E)) - 1
        m = self.compat[i]
        if k == j + 1:
            m &= self.same_head[i] if (j + 1) % 2 == 1 else self.same_tail[i]
        elif k == j - 1:
            m &= self.same_head[i] if (k + 1) % 2 == 1 else self.same_tail[i]
        return m

    def init_domains(self):
        full = (1 << len(self.E)) - 1
        doms = [full] * self.L
        doms[0] &= self.first
        doms[-1] &= self.last
        return doms


def bits(m):
    while m:
        low = m & -m
        yield low.bit_length() - 1
        m ^= low


def arc_consistency(csp, doms):
    L = csp.L
    doms = list(doms)
    if not all(doms):
        return None
    changed = True
    while changed:
        changed = False
        for j in range(L):
            for k in range(L):
                if j == k:
                    continue
                keep = 0
                dk = doms[k]
                for i in bits(doms[j]):
                    if csp.rel(j, k, i) & dk:
                        keep |= 1 << i
                if keep != doms[j]:
                    doms[j] = keep
                    changed = True
                    if not keep:
                        return None
    return doms


def path_consistency(csp, doms):
    """Strong path consistency (PC-1 style) on the binary CSP; returns None if a domain or relation empties."""
    doms = arc_consistency(csp, doms)
    if doms is None:
        return None
    L, D = csp.L, len(csp.E)
    rel = {}
    for j in range(L):
        for k in range(L):
            if j != k:
                rel[(j, k)] = [csp.rel(j, k, i) & doms[k] if (doms[j] >> i) & 1 else 0 for i in range(D)]
    changed = True
    while changed:
        changed = False
        for j in range(L):
            for k in range(L):
                if j == k:
                    continue
                rjk = rel[(j, k)]
                for l in range(L):
                    if l == j or l == k:
                        continue
                    rjl = rel[(j, l)]
                    rlk = rel[(l, k)]
                    for i in bits(doms[j]):
                        cur = rjk[i]
                        if not cur:
                            continue
                        reach = 0
                        for c in bits(rjl[i]):
                            reach |= rlk[c]
                        new = cur & reach
                        if new != cur:
                            rjk[i] = new
                            rel[(k, j)] = rel[(k, j)]  # symmetric update below
                            for b in bits(cur & ~new):
                                rel[(k, j)][b] &= ~(1 << i)
                            changed = True
                # domains: value i of j needs support in every k
                for i in bits(doms[j]):
                    if not rjk[i]:
                        doms[j] &= ~(1 << i)
                        for k2 in range(L):
                            if k2 != j:
                                rel[(j, k2)][i] = 0
                                for b in range(D):
                                    rel[(k2, j)][b] &= ~(1 << i)
                        changed = True
                if not doms[j]:
                    return None
    return doms


def ac_answer(z, L=None):
    csp = CSP(z, L)
    return arc_consistency(csp, csp.init_domains()) is not None


def pc_answer(z, L=None):
    csp = CSP(z, L)
    return path_consistency(csp, csp.init_domains()) is not None


# ------------------------------------------------------------------------------------------------------------
# converters
# ------------------------------------------------------------------------------------------------------------

def from_pi(inst):
    """ZZ instance of a Pi-instance (theory-dc.md Theorem 13(a)): x <= y iff every minimum cut containing y contains
    x; elements in no minimum cut are equivalent to v; real edges between non-equivalent elements."""
    import pi
    c, F = pi.maxflow(inst.W, inst.u, inst.v)
    reach = pi.residual_reach(inst.W, F)
    q, u, v = inst.q, inst.u, inst.v
    C = [reach[u] | reach[y] for y in range(q)]
    top = [bool((C[y] >> v) & 1) for y in range(q)]
    le = [[False] * q for _ in range(q)]
    for x in range(q):
        for y in range(q):
            if top[y]:
                le[x][y] = True
            elif top[x]:
                le[x][y] = False
            else:
                le[x][y] = bool((C[y] >> x) & 1)
    R = [(a, b) for a, b in inst.real_edges() if not (le[a][b] and le[b][a])]
    for a, b in R:
        assert le[a][b] or le[b][a], "real edge between incomparable elements"
    return ZZ(q, None, R, u, v, le=le)


def from_sw(nb, nt, F, Nb, Nt):
    """Switch model (sw2.py) as a ZZ instance: u = element 0 and bottoms 1..nb-1 equivalent to u, switches,
    tops equivalent to v = last element."""
    k = len(Nb)
    B = list(range(nb))
    S = list(range(nb, nb + k))
    T = list(range(nb + k, nb + k + nt))
    n = nb + k + nt
    u, v = B[0], T[0]
    le = [[False] * n for _ in range(n)]
    for x in range(n):
        for y in range(n):
            if x in B or y in T or x == y:
                le[x][y] = True
    R = [(B[b], T[t]) for b, t in F]
    for s in range(k):
        R += [(B[b], S[s]) for b in Nb[s]]
        R += [(S[s], T[t]) for t in Nt[s]]
    return ZZ(n, None, R, u, v, le=le)


def from_sat(nvars, clauses):
    """The 3-SAT reduction of theory-dc.md Theorem 13(c) (no P2).  clauses: lists of non-zero ints (+i = x_i,
    -i = not x_i), variables 1..nvars.  Returns (ZZ, names)."""
    names = ["u", "d", "e0"] + ["a%d" % i for i in range(1, nvars + 2)]
    names += ["T%d" % i for i in range(1, nvars + 1)] + ["F%d" % i for i in range(1, nvars + 1)]
    m = len(clauses)
    names += ["c%d" % j for j in range(1, m + 2)]
    for j, cl in enumerate(clauses, 1):
        for k in range(len(cl)):
            names.append("P%d_%d" % (j, k))
    names.append("v")
    idx = {s: i for i, s in enumerate(names)}
    n = len(names)
    less = set()
    for s in names:
        if s != "u":
            less.add((idx["u"], idx[s]))
        if s != "v":
            less.add((idx[s], idx["v"]))
    less |= {(idx["e0"], idx["d"]), (idx["e0"], idx["a1"]), (idx["c1"], idx["a%d" % (nvars + 1)])}
    R = [("u", "d"), ("e0", "d"), ("e0", "a1"), ("c1", "a%d" % (nvars + 1)), ("c%d" % (m + 1), "v")]
    for i in range(1, nvars + 1):
        for X in ("T", "F"):
            for a in (i, i + 1):
                less.add((idx["%s%d" % (X, i)], idx["a%d" % a]))
                R.append(("%s%d" % (X, i), "a%d" % a))
    for j, cl in enumerate(clauses, 1):
        for k, lit in enumerate(cl):
            P = "P%d_%d" % (j, k)
            for c in (j, j + 1):
                less.add((idx["c%d" % c], idx[P]))
                R.append(("c%d" % c, P))
            conflict = ("F%d" % lit) if lit > 0 else ("T%d" % -lit)
            less.add((idx[P], idx[conflict]))
    lt = closure(n, less)
    return ZZ(n, lt, [(idx[a], idx[b]) for a, b in R], idx["u"], idx["v"]), names


def exact_dfs(z, limit=None):
    """Exact answer by depth-first search over alternating walks with pruning: keep the down-closure D of the
    valleys and the up-closure U of the peaks; a prefix is extendable only if D and U are disjoint.  A walk whose
    edges lie in one down-set cut contains a zigzag, so walks suffice, and the future of a prefix depends only on
    (last vertex, its role, D, U), which is memoised."""
    n, le = z.n, z.le
    down = [sum(1 << a for a in range(n) if le[a][b]) for b in range(n)]
    up = [sum(1 << b for b in range(n) if le[a][b]) for a in range(n)]
    adj = z.adj()
    lt = z.lt
    seen = set()
    count = [0]

    def rec(x, is_valley, D, U):
        count[0] += 1
        if limit is not None and count[0] > limit:
            raise RuntimeError("limit")
        key = (x, is_valley, D, U)
        if key in seen:
            return None
        seen.add(key)
        for y in adj[x]:
            if is_valley and lt[x][y]:
                U2 = U | up[y]
                if U2 & D:
                    continue
                if y == z.v:
                    return [x, y]
                r = rec(y, False, D, U2)
                if r is not None:
                    return [x] + r
            elif not is_valley and lt[y][x]:
                D2 = D | down[y]
                if D2 & U:
                    continue
                r = rec(y, True, D2, U)
                if r is not None:
                    return [x] + r
        return None

    p = rec(z.u, True, down[z.u], 0)
    return p is not None, p


def pc_numpy(z, L=None, return_state=False):
    """Strong path consistency with boolean matrices: R[j][k] &= R[j][l] o R[l][k] until a fixpoint.
    Returns True if no relation/domain empties (the PC relaxation says 'yes')."""
    import numpy as np
    csp = CSP(z, L)
    L = csp.L
    D = len(csp.E)
    if D == 0:
        return False
    doms0 = csp.init_domains()
    doms = arc_consistency(csp, doms0)
    if doms is None:
        return (False, None) if return_state else False
    dm = np.array([[(doms[j] >> i) & 1 for i in range(D)] for j in range(L)], dtype=bool)
    rel = {}
    for j in range(L):
        for k in range(L):
            if j == k:
                continue
            M = np.zeros((D, D), dtype=bool)
            for i in range(D):
                if dm[j, i]:
                    m = csp.rel(j, k, i)
                    for b in bits(m):
                        M[i, b] = dm[k, b]
            rel[(j, k)] = M
    changed = True
    while changed:
        changed = False
        for j in range(L):
            for k in range(j + 1, L):
                M = rel[(j, k)]
                for l in range(L):
                    if l == j or l == k:
                        continue
                    P = (rel[(j, l)].astype(np.int32) @ rel[(l, k)].astype(np.int32)) > 0
                    N = M & P
                    if (N != M).any():
                        M = N
                        changed = True
                rel[(j, k)] = M
                rel[(k, j)] = M.T.copy()
        # domains
        for j in range(L):
            alive = np.ones(D, dtype=bool)
            for k in range(L):
                if k != j:
                    alive &= rel[(j, k)].any(axis=1)
            if not alive.any():
                return (False, None) if return_state else False
            if (alive != dm[j]).any():
                dm[j] = alive
                changed = True
                for k in range(L):
                    if k != j:
                        rel[(j, k)] = rel[(j, k)] & alive[:, None]
                        rel[(k, j)] = rel[(k, j)] & alive[None, :]
    return (True, (dm, rel)) if return_state else True
