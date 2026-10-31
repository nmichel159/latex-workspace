"""Objects of r5-core.md Section 6, written by the reviewer from the text (no import of r5-core code).

For a shortest valid path P (list of sides (w, typ)):
  WE, WF (masks of E- and F-members), Up = up(WE), L = down(WF), A (minimal E-members), B (maximal F-members),
  NE = {y in L : E_y nonempty}, NF = {x in Up : F_x nonempty}, pos (switch -> position 1..r).
Stars (Section 6.3): Estar(w) = E_w + private nodes of all middle edges (z, v) with z in LMN(w);
                     Fstar(w) = F_w + private nodes of all middle edges (v, z) with z in UMN(w).
NE(nodes) = {w : E_w nonempty, E_w meets nodes};  NF(nodes) dually.
Tools (Section 6.4): cov_E(x) = (NE(Estar x) + (down(x) - [x] if x in A)) & NE;
                     cov_F(y) = (NF(Fstar y) + (up(y) - [y] if y in B)) & NF.
Bad pair: (x, y) in NF x NE with y < x, x not in A, y not in B.
GDESC E-description (Section 6.1): U = OR NE(Estar x), x in T; S = down(Y0) + OR (down(x) - [x]), x in T';
  G = (Enon - U - S) | Phi; D = Q - up(G).  F-description dually: D = down(G').
"""
from fractions import Fraction
import itertools
from gsf import bits, popcount


class Stars:
    def __init__(self, I):
        self.I = I
        m = I.m
        priv_from = [0] * m      # private nodes of edges (z, v), indexed by the lower end z
        priv_to = [0] * m        # private nodes of edges (v, z), indexed by the upper end z
        for (z, v), nd in I.medges.items():
            priv_from[z] |= 1 << nd
            priv_to[v] |= 1 << nd
        self.Estar = []
        self.Fstar = []
        for w in range(m):
            e = I.E[w]
            for z in I.lmn[w]:
                e |= priv_from[z]
            f = I.F[w]
            for z in I.umn[w]:
                f |= priv_to[z]
            self.Estar.append(e)
            self.Fstar.append(f)
        self.NEstar = [self.NE(self.Estar[w]) for w in range(m)]
        self.NFstar = [self.NF(self.Fstar[w]) for w in range(m)]

    def NE(self, nodes):
        I = self.I
        return sum(1 << w for w in range(I.m) if I.E[w] and I.E[w] & nodes)

    def NF(self, nodes):
        I = self.I
        return sum(1 << w for w in range(I.m) if I.F[w] and I.F[w] & nodes)


class Skel:
    def __init__(self, I, P):
        self.I = I
        self.P = list(P)
        self.r = len(P)
        self.pos = {}
        self.WE = self.WF = 0
        for i, (w, typ) in enumerate(P, start=1):
            assert w not in self.pos, "switch twice on P"
            self.pos[w] = i
            if typ:
                self.WF |= 1 << w
            else:
                self.WE |= 1 << w
        self.onP = self.WE | self.WF
        self.Up = I.upc(self.WE)
        self.L = I.dnc(self.WF)
        assert self.Up & self.L == 0, "Up meets L on a valid path"
        self.A = sum(1 << a for a in bits(self.WE)
                     if not any(I.lt(b, a) for b in bits(self.WE)))
        self.B = sum(1 << b for b in bits(self.WF)
                     if not any(I.lt(b, c) for c in bits(self.WF)))
        self.NEi = sum(1 << y for y in bits(self.L) if I.E[y])
        self.NFi = sum(1 << x for x in bits(self.Up) if I.F[x])

    def consistent_side(self, side):
        w, typ = side
        return not ((self.Up >> w) & 1) if typ else not ((self.L >> w) & 1)

    def picks(self, D):
        return (self.L & ~D) == 0 and (self.Up & D) == 0


def cov_E(I, St, K, x):
    c = St.NEstar[x]
    if (K.A >> x) & 1:
        c |= I.strict_down(x)
    return c & K.NEi


def cov_F(I, St, K, y):
    c = St.NFstar[y]
    if (K.B >> y) & 1:
        c |= I.strict_up(y)
    return c & K.NFi


def bad_pairs(I, K):
    out = []
    for x in bits(K.NFi):
        if (K.A >> x) & 1:
            continue
        for y in bits(K.NEi):
            if (K.B >> y) & 1:
                continue
            if I.lt(y, x):
                out.append((x, y))
    return out


def min_vertex_cover(pairs):
    """Minimum vertex cover of a bipartite graph given by pairs (x, y): (size, list of all minimum covers
    (X0, Y0) as frozensets) by enumeration of X0 over the left vertices (small graphs only)."""
    if not pairs:
        return 0, [(frozenset(), frozenset())]
    left = sorted(set(x for x, _ in pairs))
    best = None
    covers = []
    for k in range(len(left) + 1):
        for X0 in itertools.combinations(left, k):
            Xs = set(X0)
            Y0 = frozenset(y for x, y in pairs if x not in Xs)
            size = len(Xs) + len(Y0)
            if best is None or size < best:
                best = size
                covers = [(frozenset(Xs), Y0)]
            elif size == best:
                covers.append((frozenset(Xs), Y0))
    return best, covers


def describe_E(I, St, T, Tflag, Y0, Phi):
    U = 0
    for x in T:
        U |= St.NEstar[x]
    S = 0
    for y in Y0:
        S |= I.dn[y]
    for x in Tflag:
        S |= I.strict_down(x)
    G = (I.enon & ~U & ~S) | Phi
    return I.full & ~I.upc(G), U, G


def describe_F(I, St, T, Tflag, X0, Phi):
    U = 0
    for y in T:
        U |= St.NFstar[y]
    S = 0
    for x in X0:
        S |= I.up[x]
    for y in Tflag:
        S |= I.strict_up(y)
    G = (I.fnon & ~U & ~S) | Phi
    return I.dnc(G), U, G


def thm_desc_E(I, St, K, T, Y0):
    """The E-description of Theorem 6.5 (E): T' = T & A, F-anchors Y0, Phi = A & U."""
    U = 0
    for x in T:
        U |= St.NEstar[x]
    Tflag = [x for x in T if (K.A >> x) & 1]
    D, U2, G = describe_E(I, St, T, Tflag, Y0, K.A & U)
    return D, U, K.A & U


def thm_desc_F(I, St, K, T, X0):
    U = 0
    for y in T:
        U |= St.NFstar[y]
    Tflag = [y for y in T if (K.B >> y) & 1]
    D, U2, G = describe_F(I, St, T, Tflag, X0, K.B & U)
    return D, U, K.B & U


# ---- exact LP: fractional cover number (rational simplex, Bland's rule) -----------------------------------------
def frac_cover(rows_cover, universe):
    """Fractional cover number of `universe` (list of items) by the sets rows_cover (list of sets).
    Solves the packing LP max sum v_j, sum_{j in row i} v_j <= 1, v >= 0 exactly; returns a Fraction
    (None if some item is in no set)."""
    items = list(universe)
    if not items:
        return Fraction(0)
    for it in items:
        if not any(it in S for S in rows_cover):
            return None
    nr = len(rows_cover)
    nv = len(items)
    # tableau: constraints i: sum_j a_ij v_j + s_i = 1
    A = [[Fraction(1 if items[j] in rows_cover[i] else 0) for j in range(nv)] for i in range(nr)]
    # variables 0..nv-1 original, nv..nv+nr-1 slacks
    T = []
    for i in range(nr):
        row = A[i] + [Fraction(1 if k == i else 0) for k in range(nr)] + [Fraction(1)]
        T.append(row)
    basis = [nv + i for i in range(nr)]
    c = [Fraction(1)] * nv + [Fraction(0)] * nr     # maximise c.x
    ncol = nv + nr
    while True:
        # reduced costs: c_j - c_B B^-1 A_j ; tableau rows are already B^-1 A
        red = []
        for j in range(ncol):
            z = sum(c[basis[i]] * T[i][j] for i in range(nr))
            red.append(c[j] - z)
        enter = None
        for j in range(ncol):
            if red[j] > 0:
                enter = j
                break
        if enter is None:
            break
        best = None
        leave = None
        for i in range(nr):
            if T[i][enter] > 0:
                ratio = T[i][-1] / T[i][enter]
                if best is None or ratio < best or (ratio == best and basis[i] < basis[leave]):
                    best = ratio
                    leave = i
        if leave is None:
            raise ValueError("unbounded")
        piv = T[leave][enter]
        T[leave] = [v / piv for v in T[leave]]
        for i in range(nr):
            if i != leave and T[i][enter] != 0:
                f = T[i][enter]
                T[i] = [a - f * b for a, b in zip(T[i], T[leave])]
        basis[leave] = enter
    val = sum(c[basis[i]] * T[i][-1] for i in range(nr))
    return val


def min_cover(rows_cover, universe, kmax):
    """Least number (<= kmax) of sets covering universe, and one such choice of row indices; (None, None) if none."""
    U = set(universe)
    if not U:
        return 0, []
    idx = [i for i, S in enumerate(rows_cover) if S & U]
    for k in range(1, kmax + 1):
        for comb in itertools.combinations(idx, k):
            cov = set()
            for i in comb:
                cov |= rows_cover[i]
            if U <= cov:
                return k, list(comb)
    return None, None


def all_covers(rows_cover, universe, kmax, cap=200):
    """All inclusion-minimal covers with at most kmax sets (up to cap)."""
    U = set(universe)
    out = []
    if not U:
        return [[]]
    idx = [i for i, S in enumerate(rows_cover) if S & U]
    for k in range(1, kmax + 1):
        for comb in itertools.combinations(idx, k):
            cov = set()
            for i in comb:
                cov |= rows_cover[i]
            if U <= cov:
                # minimal?
                minimal = True
                for j in comb:
                    c2 = set()
                    for i in comb:
                        if i != j:
                            c2 |= rows_cover[i]
                    if U <= c2:
                        minimal = False
                        break
                if minimal:
                    out.append(list(comb))
                    if len(out) >= cap:
                        return out
    return out


# ---- GDESC as an algorithm ---------------------------------------------------------------------------------------
def gdesc(I, St, k, a, e, want=False, kinds=(0, 1), cache=None):
    """Exhaustive GDESC: both kinds, every set of <= k tool switches with every flag pattern, every anchor set of
    size <= a, every flip set of size <= e inside U; test connectivity.  Returns True/False (or the witness)."""
    if I.s == I.t:
        return (True, None) if want else True
    if cache is None:
        cache = {}
    m = I.m

    def conn(D):
        v = cache.get(D)
        if v is None:
            v = I.connects(D)
            cache[D] = v
        return v
    for kind in kinds:
        for kk in range(k + 1):
            for T in itertools.combinations(range(m), kk):
                U = 0
                for x in T:
                    U |= St.NEstar[x] if kind == 0 else St.NFstar[x]
                Ub = bits(U)
                for nf in range(kk + 1):
                    for Tf in itertools.combinations(T, nf):
                        for na in range(a + 1):
                            for Y0 in itertools.combinations(range(m), na):
                                for ne in range(min(e, len(Ub)) + 1):
                                    for Ph in itertools.combinations(Ub, ne):
                                        ph = sum(1 << w for w in Ph)
                                        if kind == 0:
                                            D, _, _ = describe_E(I, St, T, Tf, Y0, ph)
                                        else:
                                            D, _, _ = describe_F(I, St, T, Tf, Y0, ph)
                                        if conn(D):
                                            assert I.is_downset(D)
                                            if want:
                                                return True, (kind, T, Tf, Y0, Ph, D)
                                            return True
    return (False, None) if want else False
