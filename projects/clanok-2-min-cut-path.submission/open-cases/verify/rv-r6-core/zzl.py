"""Own library of reviewer rv-r6-core (review of r5-core.md Section 8), written from the definitions.

ZZ (r4-brief.md Section 1): elements 0..q-1, u least, v greatest, preorder le[a][b] (a <= b), R = set of real edges
{a, b} with a < b strictly, {u, v} not in R.  For a down-set D with u in D and v not in D, G_D has the R-edges with
exactly one end in D; the question is whether G_D connects u and v.  P2: two incomparable elements have a common
R-neighbour strictly below both or strictly above both.

General switch form (r4-general.md Section 5.1, r5-core.md Section 6.1): bottoms = elements <= u, tops = elements
>= v, switches = the other elements.  Nodes: components of the R-edges between bottoms and tops, plus one private
node per R-edge between two switches.  E_w = nodes of the lower R-neighbours of w, F_w = nodes of the upper ones.
A down-set D of the switches picks F_w for w in D and E_w otherwise.

Sets of switches and of nodes are Python int bitmasks.
"""
import itertools


def bits(x):
    while x:
        b = x & -x
        yield b.bit_length() - 1
        x ^= b


def popcount(x):
    return bin(x).count("1")


class SW:
    """Instance in general switch form.

    m switches; le[i][j] (preorder on switches); E[w], F[w] node masks; s, t node ids; nn = number of nodes;
    me = list of middle edges (z, v, p) with z < v strictly and p the private node.
    """

    def __init__(self, m, le, E, F, s, t, nn, me):
        self.m = m
        self.le = le
        self.E = list(E)
        self.F = list(F)
        self.s = s
        self.t = t
        self.nn = nn
        self.me = list(me)
        self.full = (1 << m) - 1
        self.up = [sum(1 << j for j in range(m) if le[i][j]) for i in range(m)]
        self.dn = [sum(1 << j for j in range(m) if le[j][i]) for i in range(m)]
        self.tie = [self.up[i] & self.dn[i] for i in range(m)]
        self.sup = [self.up[i] & ~self.tie[i] for i in range(m)]   # strictly above
        self.sdn = [self.dn[i] & ~self.tie[i] for i in range(m)]   # strictly below
        self.enon = sum(1 << w for w in range(m) if self.E[w])
        self.fnon = sum(1 << w for w in range(m) if self.F[w])
        # stars (r5-core.md 6.3): E#_w = E_w + private nodes of middle edges z v with z in LMN(w)
        lmn = [[] for _ in range(m)]
        umn = [[] for _ in range(m)]
        for (z, v, p) in self.me:
            lmn[v].append(z)
            umn[z].append(v)
        priv_up = [0] * m   # priv_up[z] = private nodes of the edges z v (z the lower end)
        priv_dn = [0] * m   # priv_dn[v] = private nodes of the edges z v (v the upper end)
        for (z, v, p) in self.me:
            priv_up[z] |= 1 << p
            priv_dn[v] |= 1 << p
        # OR, not sum: a pair may carry several middle edges (several private nodes) in stored instances
        self.Es = []
        self.Fs = []
        for w in range(m):
            e = self.E[w]
            for z in set(lmn[w]):
                e |= priv_up[z]
            f = self.F[w]
            for z in set(umn[w]):
                f |= priv_dn[z]
            self.Es.append(e)
            self.Fs.append(f)
        self.NEs = [self.NE(self.Es[w]) for w in range(m)]
        self.NFs = [self.NF(self.Fs[w]) for w in range(m)]
        self.lmn = lmn
        self.umn = umn

    def NE(self, Z):
        return sum(1 << w for w in range(self.m) if self.E[w] & Z)

    def NF(self, Z):
        return sum(1 << w for w in range(self.m) if self.F[w] & Z)

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

    def is_down(self, D):
        return all((self.dn[w] & ~D) == 0 for w in bits(D))

    def connects(self, D):
        """s-t connectivity in the hypergraph of the sides picked by the down-set D."""
        sides = [self.F[w] if (D >> w) & 1 else self.E[w] for w in range(self.m)]
        reach = 1 << self.s
        changed = True
        used = 0
        while changed:
            changed = False
            for w in range(self.m):
                if not (used >> w) & 1 and sides[w] & reach:
                    reach |= sides[w]
                    used |= 1 << w
                    changed = True
        return bool((reach >> self.t) & 1)

    def downsets(self):
        """All down-sets of the switch preorder (as masks)."""
        out = []
        m = self.m
        # recursive over switches in an order compatible with <=; simple filter for small m
        if m <= 16:
            for D in range(1 << m):
                if self.is_down(D):
                    out.append(D)
            return out
        raise ValueError("too many switches for downsets()")

    def comparable(self, a, b):
        return self.le[a][b] or self.le[b][a]

    def p2_switch(self):
        """P2 in switch form: incomparable x, y have a common E-node, a common F-node, a lower middle witness
        z < x, y with middle edges z x, z y, or an upper middle witness z > x, y with edges x z, y z."""
        mset = {(z, v) for (z, v, p) in self.me}
        for x in range(self.m):
            for y in range(x + 1, self.m):
                if self.comparable(x, y):
                    continue
                if self.E[x] & self.E[y] or self.F[x] & self.F[y]:
                    continue
                ok = False
                for z in range(self.m):
                    if (z, x) in mset and (z, y) in mset:
                        ok = True
                        break
                    if (x, z) in mset and (y, z) in mset:
                        ok = True
                        break
                if not ok:
                    return False
        return True


def zz_to_sw(q, u, v, le, R):
    """Own converter ZZ -> general switch form.  Returns (SW, mid) with mid the list of ZZ elements that are
    switches (switch i = element mid[i])."""
    bottoms = [a for a in range(q) if le[a][u]]
    tops = [a for a in range(q) if le[v][a]]
    bset, tset = set(bottoms), set(tops)
    mid = [a for a in range(q) if a not in bset and a not in tset]
    idx = {a: i for i, a in enumerate(mid)}
    # union-find on bottoms and tops via R-edges between them
    par = {a: a for a in bottoms + tops}

    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a
    for (a, b) in R:
        if a in par and b in par:
            ra, rb = find(a), find(b)
            if ra != rb:
                par[ra] = rb
    comp = {}
    for a in bottoms + tops:
        r = find(a)
        if r not in comp:
            comp[r] = len(comp)
    node = {a: comp[find(a)] for a in bottoms + tops}
    nn = len(comp)
    m = len(mid)
    E = [0] * m
    F = [0] * m
    me = []
    for (a, b) in R:
        # a < b strictly
        if a in bset and b in idx:
            E[idx[b]] |= 1 << node[a]
        elif a in idx and b in tset:
            F[idx[a]] |= 1 << node[b]
        elif a in idx and b in idx:
            p = nn
            nn += 1
            me.append((idx[a], idx[b], p))
            F[idx[a]] |= 1 << p
            E[idx[b]] |= 1 << p
        elif a in bset and b in tset:
            pass
        else:
            raise ValueError("edge between two bottoms or two tops, or not strict: %r" % ((a, b),))
    lem = [[le[mid[i]][mid[j]] for j in range(m)] for i in range(m)]
    return SW(m, lem, E, F, node[u], node[v], nn, me), mid


def zz_connects(q, u, v, R, Dfull):
    """u-v connectivity of G_D (edges with exactly one end in D), from the definition."""
    adj = [[] for _ in range(q)]
    for (a, b) in R:
        if ((Dfull >> a) & 1) != ((Dfull >> b) & 1):
            adj[a].append(b)
            adj[b].append(a)
    seen = {u}
    st = [u]
    while st:
        a = st.pop()
        for b in adj[a]:
            if b not in seen:
                seen.add(b)
                st.append(b)
    return v in seen


def zz_p2(q, le, R):
    nb = [set() for _ in range(q)]
    for (a, b) in R:
        nb[a].add(b)
        nb[b].add(a)
    for x in range(q):
        for y in range(x + 1, q):
            if le[x][y] or le[y][x]:
                continue
            ok = False
            for z in nb[x] & nb[y]:
                below = le[z][x] and not le[x][z] and le[z][y] and not le[y][z]
                above = le[x][z] and not le[z][x] and le[y][z] and not le[z][y]
                if below or above:
                    ok = True
                    break
            if not ok:
                return False
    return True


def sw_to_zz(I):
    """Realise a switch-form instance as ZZ: u, v; per non-terminal node n a bottom b_n (tied with u) and a top t_n
    (tied with v) with the edge b_n t_n; extra top for s and extra bottom for t when needed; a private node of a middle
    edge z v becomes the R-edge (z, v).  Returns (q, u, v, le, R, sw_index) with sw_index[i] = element of switch i."""
    m = I.m
    priv = {p: (z, v) for (z, v, p) in I.me}
    # elements: 0 = u, 1 = v, then switches, then bottoms/tops per node
    q = 2
    sw_index = list(range(2, 2 + m))
    q += m
    bot = {}
    top = {}
    for n in range(I.nn):
        if n in priv:
            continue
        if n == I.s:
            bot[n] = 0
        if n == I.t:
            top[n] = 1
    # nodes used in E-sides need a bottom, in F-sides a top
    usedE = 0
    usedF = 0
    for w in range(m):
        usedE |= I.E[w]
        usedF |= I.F[w]
    for n in range(I.nn):
        if n in priv:
            continue
        if (usedE >> n) & 1 and n not in bot:
            bot[n] = q
            q += 1
        if (usedF >> n) & 1 and n not in top:
            top[n] = q
            q += 1
    R = []
    for n in range(I.nn):
        if n in bot and n in top and not (bot[n] == 0 and top[n] == 1):
            R.append((bot[n], top[n]))
    if I.s == I.t:
        raise ValueError("s = t")
    for w in range(m):
        for n in bits(I.E[w]):
            if n in priv:
                continue
            R.append((bot[n], sw_index[w]))
        for n in bits(I.F[w]):
            if n in priv:
                continue
            R.append((sw_index[w], top[n]))
    for (z, v, p) in I.me:
        R.append((sw_index[z], sw_index[v]))
    bots = {0} | set(bot.values())
    tops = {1} | set(top.values())
    botmask = 0
    for a in bots:
        botmask |= 1 << a
    if q > 3000:
        # the order matrix of the realisation would be too large (q^2 entries); connectivity needs only R and the
        # bottoms (every down-set of the realisation is bottoms + a down-set of the switches)
        return q, 0, 1, None, R, sw_index, botmask
    le = [[False] * q for _ in range(q)]
    for a in range(q):
        for b in range(q):
            if a in bots or b in tops:
                le[a][b] = True
            elif a in tops or b in bots:
                le[a][b] = (a in tops and b in tops) or (a in bots and b in bots)
    for i in range(m):
        for j in range(m):
            le[sw_index[i]][sw_index[j]] = I.le[i][j]
    for a in range(q):
        le[a][a] = True
    return q, 0, 1, le, R, sw_index, botmask


# ---------------------------------------------------------------- valid paths

def side_nodes(I, side):
    w, typ = side
    return I.E[w] if typ == 0 else I.F[w]


class Budget(Exception):
    pass


def all_shortest_valid_paths(I, cap=None, maxlen=None, budget=None):
    """All shortest valid paths (sequences of sides (w, type), type 0 = E, 1 = F): s in the first side, t in the
    last, consecutive sides meet, pairwise distinct switches, no conflict pair {E_w, F_z} with w <= z.
    Returns (r, paths) with r the length, or (None, []) if there is none.  Iterative deepening DFS with the
    side-graph distance to t as admissible bound."""
    m = I.m
    sides = [(w, ty) for w in range(m) for ty in (0, 1) if side_nodes(I, (w, ty))]
    sn = {sd: side_nodes(I, sd) for sd in sides}
    # side-graph distance to t (ignoring validity)
    INF = 10 ** 9
    dist = {sd: INF for sd in sides}
    frontier = [sd for sd in sides if (sn[sd] >> I.t) & 1]
    for sd in frontier:
        dist[sd] = 1
    d = 1
    while frontier:
        nxt = []
        for sd in sides:
            if dist[sd] == INF and any(sn[sd] & sn[f] for f in frontier):
                dist[sd] = d + 1
                nxt.append(sd)
        frontier = nxt
        d += 1
    nbr = {sd: [o for o in sides if o[0] != sd[0] and sn[sd] & sn[o]] for sd in sides}
    starts = [sd for sd in sides if (sn[sd] >> I.s) & 1]
    if not starts:
        return None, []
    lb = min(dist[sd] for sd in starts)
    if lb >= INF:
        return None, []
    limit = maxlen if maxlen is not None else 2 * m + 1
    visits = [0]
    for r in range(lb, min(m, limit) + 1):
        out = []

        def dfs(path, used, upm, dnm):
            if cap is not None and len(out) >= cap:
                return
            visits[0] += 1
            if budget is not None and visits[0] > budget:
                raise Budget()
            cur = path[-1]
            if (sn[cur] >> I.t) & 1 and len(path) == r:
                out.append(list(path))
                return
            if len(path) >= r:
                return
            for o in nbr[cur]:
                w, ty = o
                if (used >> w) & 1:
                    continue
                if len(path) + dist[o] > r:
                    continue
                if ty == 0:
                    if (dnm >> w) & 1:
                        continue
                    path.append(o)
                    dfs(path, used | (1 << w), upm | I.up[w], dnm)
                    path.pop()
                else:
                    if (upm >> w) & 1:
                        continue
                    path.append(o)
                    dfs(path, used | (1 << w), upm, dnm | I.dn[w])
                    path.pop()
        for st in starts:
            if dist[st] > r:
                continue
            w, ty = st
            if ty == 0:
                dfs([st], 1 << w, I.up[w], 0)
            else:
                dfs([st], 1 << w, 0, I.dn[w])
        # a path of length r whose t-contact is earlier would be shorter; dfs only accepts at length r,
        # and shorter lengths were tried before
        if out:
            return r, out
    return None, []


class Skel:
    """Objects of a valid path P (r5-core.md 6.1, 8.2)."""

    def __init__(self, I, P):
        self.P = P
        self.WE = sum(1 << w for (w, ty) in P if ty == 0)
        self.WF = sum(1 << w for (w, ty) in P if ty == 1)
        self.Up = I.upc(self.WE)
        self.L = I.dnc(self.WF)
        self.A = sum(1 << a for a in bits(self.WE) if not (I.sdn[a] & self.WE))
        self.B = sum(1 << b for b in bits(self.WF) if not (I.sup[b] & self.WF))
        self.NE_ = self.L & I.enon
        self.NF_ = self.Up & I.fnon
        self.pos = {w: i for i, (w, ty) in enumerate(P)}


# ---------------------------------------------------------------- terms (r5-core.md 8.2)

def term_D(I, kind, T, Tp, anchors, Phi):
    """kind 'E': U = union NE(E#_x), S = down(Y0) + union over Tp of strict-down, G = (Enon - U - S) | Phi,
    D = Q - up(G).  kind 'F': U' = union NF(F#_y), S' = up(X0) + union over Tp of strict-up, G' = (Fnon - U' - S')
    | Phi, D = down(G').  Returns (D, U, S, G)."""
    if kind == "E":
        U = 0
        for x in T:
            U |= I.NEs[x]
        S = I.dnc(anchors)
        for x in Tp:
            S |= I.sdn[x]
        G = (I.enon & ~U & ~S) | Phi
        D = I.full & ~I.upc(G)
        return D, U, S, G
    U = 0
    for y in T:
        U |= I.NFs[y]
    S = I.upc(anchors)
    for y in Tp:
        S |= I.sup[y]
    G = (I.fnon & ~U & ~S) | Phi
    D = I.dnc(G)
    return D, U, S, G


def kparam(m):
    import math
    k = m.bit_length()          # = floor(log2 m) + 1 for m >= 1
    N = math.ceil(2 * k * math.log(m)) if m >= 1 else 0
    return k, N
