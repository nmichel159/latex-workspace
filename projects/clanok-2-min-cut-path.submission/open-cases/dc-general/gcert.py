"""General certificate search (Theorem GC of dc-general.md) for ZZ instances with an arbitrary preorder.

Instance: class Inst(n, le, R, u, v); le[a][b] = a <= b (a preorder, u least, v greatest), R = set of pairs (a, b)
with a < b (strict).  Everything is stored as bit masks: down[x] = {a : a <= x}, up[x] = {b : x <= b},
lo[x] = R-neighbours strictly below x, hi[x] = R-neighbours strictly above x, B = class of u, T = class of v.

Pin set pi = (Gm, Pm, Gp, Pp) (generators and piercers below / above, bit masks).
  Dm = down-closure of Gm | Pm, Up = up-closure of Gp | Pp,
  Mm = {y : lo[y] & Pm != 0}  (peaks that are stored),  Mp = {x : hi[x] & Pp != 0}  (valleys that are stored).
A walk is pi-admissible (general mode) if
  (A1) no peak in Dm, no valley in Up;
  (A2) every valley x not in Dm: every peak-capable y <= x with y not in Dm lies in Mm;
  (A3) every peak y not in Up: every valley-capable x >= y with x not in Up lies in Mp;
  (A4) no stored valley >= stored peak;
  (A5) every pin of Pm is R-adjacent to at most 2 stored peaks, every pin of Pp to at most 2 stored valleys.
Peak-pinned mode: every peak in Up, no valley in Up (Theorem F); valley-pinned mode: dual.
Every admissible walk is conflict-free (Lemma 1), hence the search is sound for every pin set.
"""
import itertools
from collections import deque


def bits(m):
    out = []
    while m:
        low = m & -m
        out.append(low.bit_length() - 1)
        m ^= low
    return out


class Inst:
    def __init__(self, n, le, R, u=0, v=None):
        if v is None:
            v = n - 1
        self.n, self.u, self.v = n, u, v
        self.le = le
        lt = [[le[a][b] and not le[b][a] for b in range(n)] for a in range(n)]
        self.lt = lt
        R2 = set()
        for a, b in R:
            if lt[a][b]:
                R2.add((a, b))
            elif lt[b][a]:
                R2.add((b, a))
            else:
                raise ValueError("edge between non-comparable or equivalent elements: %r" % ((a, b),))
        assert (u, v) not in R2
        self.R = sorted(R2)
        self.down = [sum(1 << a for a in range(n) if le[a][x]) for x in range(n)]
        self.up = [sum(1 << b for b in range(n) if le[x][b]) for x in range(n)]
        self.lo = [0] * n
        self.hi = [0] * n
        for a, b in self.R:
            self.hi[a] |= 1 << b
            self.lo[b] |= 1 << a
        self.B = self.down[u] & self.up[u]
        self.T = self.down[v] & self.up[v]
        full = (1 << n) - 1
        self.peakcap = sum(1 << y for y in range(n) if self.lo[y] and not (self.B >> y) & 1)
        self.valcap = sum(1 << x for x in range(n) if self.hi[x] and not (self.T >> x) & 1)
        self.full = full

    def p2_bad(self):
        bad = []
        n = self.n
        for x in range(n):
            for y in range(x + 1, n):
                if self.le[x][y] or self.le[y][x]:
                    continue
                if not ((self.lo[x] & self.lo[y]) or (self.hi[x] & self.hi[y])):
                    bad.append((x, y))
        return bad

    def p2(self):
        return not self.p2_bad()

    def downclose(self, m):
        r = 0
        for x in bits(m):
            r |= self.down[x]
        return r

    def upclose(self, m):
        r = 0
        for x in bits(m):
            r |= self.up[x]
        return r


# ----------------------------------------------------------------------------------------------------------------
# exact solver (own code): depth-first search over walks with the down-closure of the valleys and the up-closure of
# the peaks (a walk is conflict-free iff the two closures are disjoint); memoised on (vertex, role, D, U)
# ----------------------------------------------------------------------------------------------------------------

def exact(I, want_walk=False):
    seen = set()
    u, v = I.u, I.v

    def rec(x, valley, D, U):
        key = (x, valley, D, U)
        if key in seen:
            return None
        seen.add(key)
        if valley:
            for y in bits(I.hi[x]):
                U2 = U | I.up[y]
                if U2 & D:
                    continue
                if y == v:
                    return [x, y]
                r = rec(y, False, D, U2)
                if r is not None:
                    return [x] + r
        else:
            for y in bits(I.lo[x]):
                D2 = D | I.down[y]
                if D2 & U:
                    continue
                r = rec(y, True, D2, U)
                if r is not None:
                    return [x] + r
        return None

    import sys
    old = sys.getrecursionlimit()
    sys.setrecursionlimit(max(old, 10000))
    w = rec(u, True, I.down[u], 0)
    return (w is not None, w) if want_walk else (w is not None)


def downsets(I):
    """All down-sets D with u in D, v not in D (as bit masks)."""
    n = I.n
    cand = [x for x in range(n) if not (I.B >> x) & 1 and not (I.T >> x) & 1]
    res = set()
    stack = [(0, I.B)]
    while stack:
        i, A = stack.pop()
        while i < len(cand) and (A >> cand[i]) & 1:
            i += 1
        if i == len(cand):
            res.add(A)
            continue
        x = cand[i]
        stack.append((i + 1, A))
        stack.append((i + 1, A | I.down[x]))
    # the skip branch can produce sets that are not down-sets only if a later element's down-closure re-adds x,
    # which keeps them down-sets; filter anyway
    out = []
    for A in res:
        if all(((A >> x) & 1) == 0 or (I.down[x] & ~A) == 0 for x in range(n)) and not (A >> I.v) & 1:
            out.append(A)
    return sorted(set(out))


def cut_path(I, D):
    """Shortest u-v path in G_D (BFS) or None."""
    par = {I.u: None}
    dq = deque([I.u])
    while dq:
        x = dq.popleft()
        nb = (I.hi[x] & ~D) if (D >> x) & 1 else (I.lo[x] & D)
        for y in bits(nb):
            if y not in par:
                par[y] = x
                if y == I.v:
                    p = [y]
                    while par[p[-1]] is not None:
                        p.append(par[p[-1]])
                    return p[::-1]
                dq.append(y)
    return None


def exact_downsets(I):
    for D in downsets(I):
        if cut_path(I, D) is not None:
            return True
    return False


# ----------------------------------------------------------------------------------------------------------------
# certificate search
# ----------------------------------------------------------------------------------------------------------------

def pinned_search(I, Dm, Up, peak_pinned):
    """Peak-pinned: peaks in Up and not in Dm, valleys not in Up.  Valley-pinned: valleys in Dm and not in Up, peaks
    not in Dm.  BFS on (vertex, role)."""
    n = I.n
    if peak_pinned:
        okv = I.full & ~Up
        okp = Up & ~Dm
    else:
        okv = Dm & ~Up
        okp = I.full & ~Dm
    if not (okv >> I.u) & 1 or not (okp >> I.v) & 1:
        return None
    start = (I.u, 1)
    par = {start: None}
    dq = deque([start])
    while dq:
        x, val = dq.popleft()
        nb = (I.hi[x] & okp) if val else (I.lo[x] & okv)
        for y in bits(nb):
            st = (y, 1 - val)
            if st in par:
                continue
            par[st] = (x, val)
            if y == I.v and val:
                w = [st]
                while par[w[-1]] is not None:
                    w.append(par[w[-1]])
                return [a for a, _ in w[::-1]]
            dq.append(st)
    return None


def general_search(I, Gm, Pm, Gp, Pp, cap=2, return_walk=False):
    """BFS over (vertex, role, stored set) for a pi-admissible walk in general mode."""
    n = I.n
    Dm = I.downclose(Gm | Pm)
    Up = I.upclose(Gp | Pp)
    Mm = sum(1 << y for y in range(n) if I.lo[y] & Pm)
    Mp = sum(1 << x for x in range(n) if I.hi[x] & Pp)
    # allowed valleys and peaks
    okv = 0
    okp = 0
    for x in range(n):
        if not (Up >> x) & 1:
            if (Dm >> x) & 1:
                okv |= 1 << x
            else:
                need = I.down[x] & I.peakcap & ~Dm
                if need & ~Mm == 0:
                    okv |= 1 << x
        if not (Dm >> x) & 1:
            if (Up >> x) & 1:
                okp |= 1 << x
            else:
                need = I.up[x] & I.valcap & ~Up
                if need & ~Mp == 0:
                    okp |= 1 << x
    if not (okv >> I.u) & 1 or not (okp >> I.v) & 1:
        return None
    pinsm = bits(Pm)
    pinsp = bits(Pp)

    def add(S, y, as_peak):
        """S = (stored peaks mask, stored valleys mask)."""
        sp, sv = S
        if as_peak:
            if not (Mm >> y) & 1 or (sp >> y) & 1:
                return S
            # conflict: stored valley x with y <= x
            if sv & I.up[y]:
                return None
            sp2 = sp | (1 << y)
            for phi in pinsm:
                if (I.lo[y] >> phi) & 1:
                    if bin(sp2 & I.hi[phi]).count("1") > cap:
                        return None
            return (sp2, sv)
        else:
            if not (Mp >> y) & 1 or (sv >> y) & 1:
                return S
            if sp & I.down[y]:
                return None
            sv2 = sv | (1 << y)
            for phi in pinsp:
                if (I.hi[y] >> phi) & 1:
                    if bin(sv2 & I.lo[phi]).count("1") > cap:
                        return None
            return (sp, sv2)

    S0 = add((0, 0), I.u, False)
    if S0 is None:
        return None
    start = (I.u, 1, S0)
    par = {start: None}
    dq = deque([start])
    while dq:
        st = dq.popleft()
        x, val, S = st
        nb = (I.hi[x] & okp) if val else (I.lo[x] & okv)
        for y in bits(nb):
            S2 = add(S, y, bool(val))
            if S2 is None:
                continue
            nst = (y, 1 - val, S2)
            if nst in par:
                continue
            par[nst] = st
            if y == I.v and val:
                if not return_walk:
                    return True
                w = [nst]
                while par[w[-1]] is not None:
                    w.append(par[w[-1]])
                return [a for a, _, _ in w[::-1]]
            dq.append(nst)
    return None


def class_reps(I):
    """One element per equivalence class (generators depend only on the class)."""
    seen = 0
    reps = []
    for x in range(I.n):
        if not (seen >> x) & 1:
            reps.append(x)
            seen |= I.down[x] & I.up[x]
    return reps


def certificate(I, k, modes=("pp", "vp", "gen"), cap=2, piercers_only=None):
    """Smallest certificate of size <= k found, as (size, mode, pins) or None.
    piercers_only: None (all pin kinds) or 'H' (only piercers in B / T: the literal Theorem H translation)."""
    n = I.n
    reps = class_reps(I)
    middle = [x for x in reps if not (I.B >> x) & 1 and not (I.T >> x) & 1]
    for size in range(0, k + 1):
        if "pp" in modes and piercers_only is None:
            # peak-pinned: G+ = A (generators above), size |A|; A must give v in Up
            cands = middle + [I.v]
            for A in itertools.combinations(cands, size):
                if not A:
                    continue
                m = sum(1 << a for a in A)
                if pinned_search(I, 0, I.upclose(m), True) is not None:
                    return (size, "pp", A)
        if "vp" in modes and piercers_only is None:
            cands = middle + [I.u]
            for A in itertools.combinations(cands, size):
                if not A:
                    continue
                m = sum(1 << a for a in A)
                if pinned_search(I, I.downclose(m), 0, False) is not None:
                    return (size, "vp", A)
        if "gen" in modes:
            if piercers_only == "H":
                roles = [("Pm", x) for x in bits(I.B)] + [("Pp", x) for x in bits(I.T)]
            else:
                roles = ([("Gm", x) for x in middle] + [("Pm", x) for x in range(n) if I.hi[x]] +
                         [("Gp", x) for x in middle] + [("Pp", x) for x in range(n) if I.lo[x]])
            for combo in itertools.combinations(roles, size):
                masks = {"Gm": 0, "Pm": 0, "Gp": 0, "Pp": 0}
                for r, x in combo:
                    masks[r] |= 1 << x
                if general_search(I, masks["Gm"], masks["Pm"], masks["Gp"], masks["Pp"], cap) is not None:
                    return (size, "gen", combo)
    return None


def check_walk(I, w):
    """Independent check that w is a consistent zigzag walk (alternating, R-edges, no valley >= peak)."""
    if w[0] != I.u or w[-1] != I.v or len(w) % 2 != 0:
        return False
    Rs = set(I.R)
    for i in range(len(w) - 1):
        a, b = w[i], w[i + 1]
        if i % 2 == 0:
            if (a, b) not in Rs:
                return False
        else:
            if (b, a) not in Rs:
                return False
    vals = w[0::2]
    peaks = w[1::2]
    for x in vals:
        for y in peaks:
            if I.le[y][x]:
                return False
    return True


# ----------------------------------------------------------------------------------------------------------------
# random instances (general preorders with ties, one-way comparabilities, middle edges), P2 completion
# ----------------------------------------------------------------------------------------------------------------

def random_preorder(rng, nb, nm, nt, ncls, p_order, distinct=False):
    """Elements: 0..nb-1 equivalent to u = 0; middle nb..nb+nm-1 in ncls classes; last nt equivalent to v = n-1.
    Classes ordered by a random partial order (relation probability p_order on a random linear order of classes)."""
    n = nb + nm + nt
    M = list(range(nb, nb + nm))
    T = list(range(nb + nm, n))
    if distinct:
        ncls = nm
        cls = {x: i for i, x in enumerate(M)}
    else:
        cls = {x: rng.randrange(ncls) for x in M}
    perm = list(range(ncls))
    rng.shuffle(perm)
    cl_lt = set()
    for i in range(ncls):
        for j in range(i + 1, ncls):
            if rng.random() < p_order:
                cl_lt.add((perm[i], perm[j]))
    le = [[False] * n for _ in range(n)]
    for a in range(n):
        le[a][a] = True
        for b in range(n):
            if a < nb or b in T:
                le[a][b] = True
    for x in M:
        for y in M:
            if cls[x] == cls[y] or (cls[x], cls[y]) in cl_lt:
                le[x][y] = True
    for k in range(n):
        for i in range(n):
            if le[i][k]:
                for j in range(n):
                    if le[k][j]:
                        le[i][j] = True
    return le


def p2_complete(rng, n, le, R, u=0, v=None, prefer=None):
    """Add R-edges until P2 holds: for an incomparable pair pick a random common bound w (strictly above both or
    strictly below both, comparable and non-equivalent) and add w-x, w-y.  prefer: optional list of preferred w."""
    if v is None:
        v = n - 1
    lt = [[le[a][b] and not le[b][a] for b in range(n)] for a in range(n)]
    R = set(R)
    lo = [0] * n
    hi = [0] * n
    for a, b in R:
        hi[a] |= 1 << b
        lo[b] |= 1 << a
    pairs = [(x, y) for x in range(n) for y in range(x + 1, n) if not le[x][y] and not le[y][x]]
    rng.shuffle(pairs)
    for x, y in pairs:
        if (lo[x] & lo[y]) or (hi[x] & hi[y]):
            continue
        cands = [w for w in range(n) if (lt[w][x] and lt[w][y]) or (lt[x][w] and lt[y][w])]
        if prefer:
            pc = [w for w in cands if w in prefer]
            if pc and rng.random() < 0.7:
                cands = pc
        w = rng.choice(cands)
        for z in (x, y):
            e = (w, z) if lt[w][z] else (z, w)
            if e == (u, v):
                continue
            R.add(e)
            hi[e[0]] |= 1 << e[1]
            lo[e[1]] |= 1 << e[0]
    return R


def random_inst(rng, nb=None, nm=None, nt=None, ncls=None, p_order=None, p_R=None, middle_edges=True,
                distinct=False):
    nb = nb or rng.randint(1, 3)
    nm = nm or rng.randint(2, 7)
    nt = nt or rng.randint(1, 3)
    ncls = ncls or rng.randint(max(1, nm // 2), nm)
    p_order = rng.choice([0.0, 0.15, 0.3]) if p_order is None else p_order
    p_R = rng.choice([0.15, 0.3, 0.45]) if p_R is None else p_R
    n = nb + nm + nt
    le = random_preorder(rng, nb, nm, nt, ncls, p_order, distinct)
    lt = [[le[a][b] and not le[b][a] for b in range(n)] for a in range(n)]
    u, v = 0, n - 1
    R = set()
    for a in range(n):
        for b in range(n):
            if lt[a][b] and (a, b) != (u, v) and rng.random() < p_R:
                if not middle_edges and nb <= a < nb + nm and nb <= b < nb + nm:
                    continue
                R.add((a, b))
    R = p2_complete(rng, n, le, R, u, v)
    if not middle_edges:
        # P2 completion may have used middle common bounds; that is allowed only through B / T
        pass
    return Inst(n, le, R, u, v)


def describe(I):
    """Compact text: classes, strict order between middle classes, edges."""
    n = I.n
    reps = class_reps(I)
    cl = {}
    for r in reps:
        cl[r] = bits(I.down[r] & I.up[r])
    lines = ["n=%d u=%d v=%d" % (n, I.u, I.v)]
    lines.append("classes: " + " ".join("{%s}" % ",".join(map(str, c)) for c in cl.values()))
    rel = []
    for a in reps:
        for b in reps:
            if a != b and I.lt[a][b] and not (I.B >> a) & 1 and not (I.T >> b) & 1:
                # covering relations only
                if not any(I.lt[a][c] and I.lt[c][b] for c in reps if c not in (a, b)):
                    rel.append("%d<%d" % (a, b))
    lines.append("middle order (covers): " + " ".join(rel))
    lines.append("R: " + " ".join("%d-%d" % e for e in I.R))
    return "; ".join(lines)
