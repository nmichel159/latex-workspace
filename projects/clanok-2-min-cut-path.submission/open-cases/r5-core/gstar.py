"""Sibling stars, strict anchors and the generalized duality of r5-core.md Section 6.

Setting: gcore.Gen (general switch form; G.medge[node] = (y, x) for a middle edge y - x with y < x, the node lying
in F_y and E_x).  For a valid path P (list of side ids):
  WE, WF, Up = up(WE), L = down(WF), A = minimal E-members, B = maximal F-members (switch masks),
  NF = switches of Up with non-empty F-side (needed F-sides), NE = switches of L with non-empty E-side.
Sibling stars (node masks):
  Estar(w) = E_w  united with the private nodes of all middle edges z - v with z a lower middle neighbour of w;
  Fstar(w) = F_w  united with the private nodes of all middle edges v - z with z an upper middle neighbour of w.
  NE(Estar(w)) = NE(E_w) + lower siblings of w + {w};  NF(Fstar(w)) = NF(F_w) + upper siblings + {w}.
E-tool of x: the centre Estar(x), plus the strict anchor at x (down(x) - [x] into F-mode) when x is in A.
F-tool of y: the centre Fstar(y), plus the strict anchor at y (up(y) - [y] into E-mode) when y is in B.
Pair classes for (x, y) in NF x NE:
  'E'  y in NE(Estar(x));  'F'  x in NF(Fstar(y));
  'Ea' y < x and x in A;   'Fa' y < x and y in B;
  'bad' otherwise (then y < x strictly, x not in A, y not in B; Lemma 6.4 excludes incomparable pairs).
"""
import itertools
from gcore import bits, popcount


def lt(G, a, b):
    return G.le[a][b] and not G.le[b][a]


class Stars:
    """Sibling stars of every switch (node masks) and their switch neighbourhoods."""

    def __init__(self, G):
        self.G = G
        m = G.m
        lmn = [set() for _ in range(m)]     # lower middle neighbours
        umn = [set() for _ in range(m)]
        priv_up = [0] * m                   # private nodes of edges z - v, indexed by the lower end z
        priv_dn = [0] * m                   # private nodes of edges v - z, indexed by the upper end z
        for node, (y, x) in G.medge.items():
            lmn[x].add(y)
            umn[y].add(x)
            priv_up[y] |= 1 << node
            priv_dn[x] |= 1 << node
        self.lmn, self.umn = lmn, umn
        self.Estar = []
        self.Fstar = []
        for w in range(m):
            e = G.E[w]
            for z in lmn[w]:
                e |= priv_up[z]
            f = G.F[w]
            for z in umn[w]:
                f |= priv_dn[z]
            self.Estar.append(e)
            self.Fstar.append(f)
        self.NEstar = [self.ne(self.Estar[w]) for w in range(m)]
        self.NFstar = [self.nf(self.Fstar[w]) for w in range(m)]

    def ne(self, nodes):
        G = self.G
        return sum(1 << v for v in range(G.m) if G.E[v] & nodes)

    def nf(self, nodes):
        G = self.G
        return sum(1 << v for v in range(G.m) if G.F[v] & nodes)


class Skel:
    """Skeleton data of a valid path P."""

    def __init__(self, G, P):
        self.G, self.P = G, P
        WE = sum(1 << (i >> 1) for i in P if not i & 1)
        WF = sum(1 << (i >> 1) for i in P if i & 1)
        Up = 0
        for w in bits(WE):
            Up |= G.up[w]
        L = 0
        for w in bits(WF):
            L |= G.dn[w]
        assert not (Up & L), "invalid path"
        self.WE, self.WF, self.Up, self.L = WE, WF, Up, L
        self.A = sum(1 << a for a in bits(WE) if not any(lt(G, b, a) for b in bits(WE)))
        self.B = sum(1 << b for b in bits(WF) if not any(lt(G, b, c) for c in bits(WF)))
        self.NF = sum(1 << x for x in bits(Up) if G.F[x])
        self.NE = sum(1 << y for y in bits(L) if G.E[y])
        self.pos = {i >> 1: a for a, i in enumerate(P)}


def classify(G, P, S=None, K=None):
    """Classes of all pairs (x, y) in NF x NE.  Returns (K, dict class -> list of pairs)."""
    if S is None:
        S = Stars(G)
    if K is None:
        K = Skel(G, P)
    out = {"E": [], "F": [], "Ea": [], "Fa": [], "bad": [], "incomp_fail": []}
    for x in bits(K.NF):
        for y in bits(K.NE):
            if (S.NEstar[x] >> y) & 1:
                out["E"].append((x, y))
            elif (S.NFstar[y] >> x) & 1:
                out["F"].append((x, y))
            elif lt(G, y, x) and (K.A >> x) & 1:
                out["Ea"].append((x, y))
            elif lt(G, y, x) and (K.B >> y) & 1:
                out["Fa"].append((x, y))
            elif lt(G, y, x):
                out["bad"].append((x, y))
            else:
                out["incomp_fail"].append((x, y))      # must never happen (Lemma 6.4)
    return K, out


def tool_cover_E(G, S, K, x):
    """Switches of NE covered by the E-tool of x (centre Estar(x), strict anchor at x if x in A)."""
    cov = S.NEstar[x]
    if (K.A >> x) & 1:
        cov |= G.dn[x] & ~sum(1 << w for w in range(G.m) if G.le[x][w] and G.le[w][x])
    return cov & K.NE


def tool_cover_F(G, S, K, y):
    cov = S.NFstar[y]
    if (K.B >> y) & 1:
        cov |= G.up[y] & ~sum(1 << w for w in range(G.m) if G.le[y][w] and G.le[w][y])
    return cov & K.NF


def star_cost(G, S, K):
    """max over x not in L of |A & NE(Estar(x))| and over y not in Up of |B & NF(Fstar(y))| (Lemma 6.3)."""
    ce = max((popcount(S.NEstar[x] & K.A) for x in range(G.m) if not (K.L >> x) & 1), default=0)
    cf = max((popcount(S.NFstar[y] & K.B) for y in range(G.m) if not (K.Up >> y) & 1), default=0)
    return ce, cf


def min_vertex_cover_bip(pairs):
    """Minimum vertex cover of a bipartite graph given by pairs (x, y) (Koenig via augmenting paths)."""
    xs = sorted(set(p[0] for p in pairs))
    adj = {x: [] for x in xs}
    for x, y in pairs:
        adj[x].append(y)
    match_y = {}

    def aug(x, seen):
        for y in adj[x]:
            if y in seen:
                continue
            seen.add(y)
            if y not in match_y or aug(match_y[y], seen):
                match_y[y] = x
                return True
        return False
    size = 0
    for x in xs:
        if aug(x, set()):
            size += 1
    return size


def strict_down(G, x):
    return G.dn[x] & ~sum(1 << w for w in range(G.m) if G.le[x][w] and G.le[w][x])


def strict_up(G, y):
    return G.up[y] & ~sum(1 << w for w in range(G.m) if G.le[y][w] and G.le[w][y])


def cheap_tools(G, S, K, kind, anchors=True, pivot_cost=None):
    """Cheap tools of one kind as switch masks of covered needed items.
    kind 0 (E): for every w not in L the centre Estar(w) (cost <= 9 flips, Lemma 6.3), with the strict anchor at w
    when w in A (free); if `anchors`, the F-anchor down(z) for every z not in Up (free); if pivot_cost is given,
    the pivot down(x) - [x] for x in Up with at most pivot_cost minimal E-members strictly below x.
    kind 1 (F): dually.  Returns a list of (mask, label)."""
    tools = []
    if kind == 0:
        for w in range(G.m):
            if (K.L >> w) & 1:
                continue
            cov = S.NEstar[w]
            if (K.A >> w) & 1:
                cov |= strict_down(G, w)
            tools.append((cov & K.NE, ("E", w)))
        if anchors:
            for z in range(G.m):
                if not (K.Up >> z) & 1:
                    tools.append((G.dn[z] & K.NE, ("anc", z)))
        if pivot_cost is not None:
            for x in bits(K.Up):
                c = popcount(K.A & strict_down(G, x))
                if c <= pivot_cost:
                    tools.append((strict_down(G, x) & K.NE, ("piv", x, c)))
    else:
        for w in range(G.m):
            if (K.Up >> w) & 1:
                continue
            cov = S.NFstar[w]
            if (K.B >> w) & 1:
                cov |= strict_up(G, w)
            tools.append((cov & K.NF, ("F", w)))
        if anchors:
            for z in range(G.m):
                if not (K.L >> z) & 1:
                    tools.append((G.up[z] & K.NF, ("anc", z)))
        if pivot_cost is not None:
            for y in bits(K.L):
                c = popcount(K.B & strict_up(G, y))
                if c <= pivot_cost:
                    tools.append((strict_up(G, y) & K.NF, ("piv", y, c)))
    return [(t, lab) for (t, lab) in tools if t]


def cover_numbers(G, P, S=None, K=None, anchors=True, integral=False, pivot_cost=None):
    """LP (or integral) cover numbers of NE by cheap E-tools and of NF by cheap F-tools (cheap_tools).
    Returns (tauE, tauF); inf if some item is covered by no tool."""
    from scipy.optimize import linprog, milp, LinearConstraint, Bounds
    import numpy as np
    if S is None:
        S = Stars(G)
    if K is None:
        K = Skel(G, P)
    res = []
    for kind in (0, 1):
        items = bits(K.NE if kind == 0 else K.NF)
        if not items:
            res.append(0.0)
            continue
        tools = [t for (t, lab) in cheap_tools(G, S, K, kind, anchors=anchors, pivot_cost=pivot_cost)]
        tools = [t for t in tools if t]
        A_ = np.zeros((len(items), len(tools)))
        for j, t in enumerate(tools):
            for i, it in enumerate(items):
                if (t >> it) & 1:
                    A_[i, j] = 1.0
        if (A_.sum(axis=1) == 0).any():
            res.append(float("inf"))
            continue
        c = np.ones(len(tools))
        if integral:
            r = milp(c, constraints=LinearConstraint(A_, lb=np.ones(len(items)), ub=np.inf),
                     integrality=np.ones(len(tools)), bounds=Bounds(0, 1))
            res.append(float(r.fun) if r.success else None)
        else:
            r = linprog(c, A_ub=-A_, b_ub=-np.ones(len(items)), bounds=(0, None), method="highs")
            res.append(float(r.fun) if r.success else None)
    return tuple(res)
