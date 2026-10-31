"""Instance generators of reviewer rv-r6-core (own code).

rigid_design: the rigid word R(W) of r4-general.md Section 6 (base switches 1..n, path side h_j of the type W_j, flip
side Fl_j of the other type; nodes s in h_1, t in h_n, y_j in h_j and h_{j+1}, z_pq in Fl_p and h_q for p < q of
different types, w_pq in Fl_p and Fl_q for p < q of equal types), plus extra switches:
  X-switches x_i strictly above a set S_i of E-members (they are rows; damage = |S_i & A'|),
  Y-switches y_j strictly below a set T_j of F-members (columns),
  relations y_j < x_i ("bad" relations), optional chains x_i < x_i', ties (copies) among extras and with members,
  ties among members of equal type, middle edges between comparable switches whose private node lies in no path side,
  P2 completion by fresh nodes in a flip side of the base switch (never in a path side) or in extra sides.
Extra sides never contain a node of a path side, so (proof in the report, Section 3.3) every solution has the base
switches in their path modes and h_1 .. h_n is the unique valid path; `rigid_certificate` checks the node incidences
that this argument uses.

random_sw: random general switch-form instances (random preorder from a random DAG plus ties, random sides over a
small node set, random middle edges), P2 repaired by fresh nodes in random same-type side pairs.
"""
import random
from zzl import SW, bits


def closure(n, rel):
    le = [[i == j for j in range(n)] for i in range(n)]
    for (a, b) in rel:
        le[a][b] = True
    for k in range(n):
        for i in range(n):
            if le[i][k]:
                rowk = le[k]
                rowi = le[i]
                for j in range(n):
                    if rowk[j]:
                        rowi[j] = True
    return le


class Builder:
    def __init__(self):
        self.nn = 0

    def node(self):
        self.nn += 1
        return self.nn - 1


def rigid_design(rng, word, nx, ny, smax, tmax, pbad, pchain=0.0, ptie_ex=0.0, ptie_mem=0.0, pme=0.0,
                 pyx_all=False, hub=False, sfix=None):
    """Returns (I, P, info).  word: string over 'EF' (the base).  sfix: optional list of S_i (lists of indices into
    the E-members) to use instead of random ones."""
    n = len(word)
    bd = Builder()
    s = bd.node()
    t = bd.node()
    nodesE = {}
    nodesF = {}
    # base switches 0..n-1; extras after
    m = n + nx + ny
    E = [0] * m
    F = [0] * m
    path = [0] * n   # path side mask
    flip = [0] * n
    path[0] |= 1 << s
    path[n - 1] |= 1 << t
    pathnodes = (1 << s) | (1 << t)
    for j in range(n - 1):
        y = bd.node()
        path[j] |= 1 << y
        path[j + 1] |= 1 << y
        pathnodes |= 1 << y
    for p in range(n):
        for q in range(p + 1, n):
            if word[p] != word[q]:
                z = bd.node()
                flip[p] |= 1 << z
                path[q] |= 1 << z
                pathnodes |= 1 << z
            else:
                w = bd.node()
                flip[p] |= 1 << w
                flip[q] |= 1 << w
    for j in range(n):
        if word[j] == "E":
            E[j] |= path[j]
            F[j] |= flip[j]
        else:
            F[j] |= path[j]
            E[j] |= flip[j]
    Emem = [j for j in range(n) if word[j] == "E"]
    Fmem = [j for j in range(n) if word[j] == "F"]
    X = list(range(n, n + nx))
    Y = list(range(n + nx, n + nx + ny))
    rel = []
    S = {}
    T = {}
    for i, x in enumerate(X):
        if sfix is not None and i < len(sfix):
            Si = [Emem[a] for a in sfix[i] if a < len(Emem)]
        else:
            Si = rng.sample(Emem, rng.randint(1, min(smax, len(Emem))))
        S[x] = Si
        for a in Si:
            rel.append((a, x))
    for y in Y:
        Tj = rng.sample(Fmem, rng.randint(1, min(tmax, len(Fmem))))
        T[y] = Tj
        for b in Tj:
            rel.append((y, b))
    for y in Y:
        for x in X:
            if pyx_all or rng.random() < pbad:
                rel.append((y, x))
    for x in X:
        for x2 in X:
            if x != x2 and rng.random() < pchain:
                rel.append((x, x2))
    # ties: an extra tied with another extra of the same kind, or an X tied with an E-member, a Y with an F-member
    for x in X:
        if rng.random() < ptie_ex:
            other = rng.choice(X + Emem)
            if other != x:
                rel.append((x, other))
                rel.append((other, x))
    for y in Y:
        if rng.random() < ptie_ex:
            other = rng.choice(Y + Fmem)
            if other != y:
                rel.append((y, other))
                rel.append((other, y))
    for grp in (Emem, Fmem):
        for a in grp:
            if rng.random() < ptie_mem:
                b = rng.choice(grp)
                if b != a:
                    rel.append((a, b))
                    rel.append((b, a))
    le = closure(m, rel)
    # validity of the planted path: no E-member <= F-member
    for a in Emem:
        for b in Fmem:
            if le[a][b]:
                return None
    # middle edges between comparable switches (strict), private node not in a path side:
    # allowed when the lower end's F-side and the upper end's E-side are not path sides
    me = []

    def pathF(w):
        return w < n and word[w] == "F"

    def pathE(w):
        return w < n and word[w] == "E"
    if pme > 0:
        for a in range(m):
            for b in range(m):
                if a != b and le[a][b] and not le[b][a] and not pathF(a) and not pathE(b):
                    if rng.random() < pme:
                        p = bd.node()
                        me.append((a, b, p))
                        F[a] |= 1 << p
                        E[b] |= 1 << p
    # P2 completion
    mset = {(z, v) for (z, v, p) in me}
    hubE = bd.node() if hub else None
    hubF = bd.node() if hub else None

    def has_p2(x, y):
        if E[x] & E[y] or F[x] & F[y]:
            return True
        for z in range(m):
            if (z, x) in mset and (z, y) in mset:
                return True
            if (x, z) in mset and (y, z) in mset:
                return True
        return False
    for x in range(m):
        for y in range(x + 1, m):
            if le[x][y] or le[y][x]:
                continue
            if has_p2(x, y):
                continue
            if x >= n and y >= n:
                if hub:
                    if rng.random() < 0.5:
                        E[x] |= 1 << hubE
                        E[y] |= 1 << hubE
                    else:
                        F[x] |= 1 << hubF
                        F[y] |= 1 << hubF
                else:
                    c = bd.node()
                    if rng.random() < 0.5:
                        E[x] |= 1 << c
                        E[y] |= 1 << c
                    else:
                        F[x] |= 1 << c
                        F[y] |= 1 << c
                continue
            b, e = (x, y) if x < n else (y, x)
            if e < n:
                raise RuntimeError("two base switches without P2")
            c = bd.node()
            if word[b] == "E":   # flip side is F
                F[b] |= 1 << c
                F[e] |= 1 << c
            else:
                E[b] |= 1 << c
                E[e] |= 1 << c
    # make sure every X has an F-side and every Y an E-side (dangling own node otherwise)
    for x in X:
        if not F[x]:
            F[x] |= 1 << bd.node()
    for y in Y:
        if not E[y]:
            E[y] |= 1 << bd.node()
    I = SW(m, le, E, F, s, t, bd.nn, me)
    P = [(j, 0 if word[j] == "E" else 1) for j in range(n)]
    info = {"n": n, "word": word, "X": X, "Y": Y, "S": S, "T": T, "pathnodes": pathnodes, "path": path,
            "flip": flip}
    return I, P, info


def rigid_certificate(I, P, info):
    """Node-incidence facts used by the rigidity argument: path nodes lie only in base sides (path sides h_j, and
    for z-nodes the flip side Fl_p with p < q); h_i and h_j are disjoint for |i - j| >= 2; s only in h_1, t only in
    h_n; the planted path is valid.  Returns a list of violated facts (empty = certificate holds)."""
    bad = []
    n = info["n"]
    pn = info["pathnodes"]
    path = info["path"]
    flip = info["flip"]
    for w in range(I.m):
        for ty, side in ((0, I.E[w]), (1, I.F[w])):
            hit = side & pn
            if not hit:
                continue
            if w >= n:
                bad.append("extra side meets a path node")
                continue
            if (w, ty) in P:
                continue
            # flip side of base switch w: its path nodes must be z_{w q} with q > w (they lie in h_q)
            for nd in bits(hit):
                qs = [q for q in range(n) if (path[q] >> nd) & 1]
                if not qs or min(qs) <= w:
                    bad.append("flip side meets a path node of h_q with q <= p")
    for i in range(n):
        for j in range(i + 2, n):
            if path[i] & path[j]:
                bad.append("h_i meets h_j, |i-j| >= 2")
    for (w, ty) in P:
        side = I.E[w] if ty == 0 else I.F[w]
        if side != (side | path[w]) or (side & pn) != path[w]:
            bad.append("path side differs from h_j on path nodes")
    # validity
    WE = [w for (w, ty) in P if ty == 0]
    WF = [w for (w, ty) in P if ty == 1]
    for a in WE:
        for b in WF:
            if I.le[a][b]:
                bad.append("planted path not valid")
    return bad


def random_preorder(rng, m, pedge, ptie):
    rel = []
    perm = list(range(m))
    rng.shuffle(perm)
    for i in range(m):
        for j in range(i + 1, m):
            if rng.random() < pedge:
                rel.append((perm[i], perm[j]))
    for i in range(m):
        if rng.random() < ptie:
            j = rng.randrange(m)
            if j != i:
                rel.append((i, j))
                rel.append((j, i))
    return closure(m, rel)


def random_sw(rng, m, nnodes, pside, pedge, ptie, pme):
    le = random_preorder(rng, m, pedge, ptie)
    bd = Builder()
    s = bd.node()
    t = bd.node()
    base = [bd.node() for _ in range(nnodes)]
    pool = [s, t] + base
    E = [0] * m
    F = [0] * m
    for w in range(m):
        for nd in pool:
            if nd == t:
                pE = pside * 0.5
            else:
                pE = pside
            if rng.random() < pE:
                E[w] |= 1 << nd
            if rng.random() < (pside * 0.5 if nd == s else pside):
                F[w] |= 1 << nd
    me = []
    for a in range(m):
        for b in range(m):
            if a != b and le[a][b] and not le[b][a] and rng.random() < pme:
                p = bd.node()
                me.append((a, b, p))
                F[a] |= 1 << p
                E[b] |= 1 << p
    mset = {(z, v) for (z, v, p) in me}
    privmask = 0
    for (z, v, p) in me:
        privmask |= 1 << p
    for x in range(m):
        for y in range(x + 1, m):
            if le[x][y] or le[y][x]:
                continue
            if E[x] & E[y] or F[x] & F[y]:
                continue
            if any(((z, x) in mset and (z, y) in mset) or ((x, z) in mset and (y, z) in mset) for z in range(m)):
                continue
            r = rng.random()
            if r < 0.4:
                c = bd.node()
                E[x] |= 1 << c
                E[y] |= 1 << c
            elif r < 0.8:
                c = bd.node()
                F[x] |= 1 << c
                F[y] |= 1 << c
            else:
                # an existing NON-private node of the same type, chosen from x's side (private nodes of middle
                # edges must stay private: version 1 of this generator broke that, see the report)
                ex = E[x] & ~privmask
                fx = F[x] & ~privmask
                if ex and rng.random() < 0.5:
                    nd = rng.choice(list(bits(ex)))
                    E[y] |= 1 << nd
                elif fx:
                    nd = rng.choice(list(bits(fx)))
                    F[y] |= 1 << nd
                else:
                    c = bd.node()
                    E[x] |= 1 << c
                    E[y] |= 1 << c
    return SW(m, le, E, F, s, t, bd.nn, me)


def deep_design(rng, L, k, ny=None, ptie_ex=0.0, ptie_mem=0.0, pme=0.0, hub=False, extra_x=0, shuffle=True):
    """Design meant to make the proof of Theorem 8.2 (with adversarial covers) use L levels: nE = 2k 2^(L-2)
    E-members (word (EF)^nE), for every level i = 1 .. L-1 a family of k X-switches with disjoint sets S of size
    2^(L-1-i), nested in the union of the previous family, every Y below every X.  k must equal floor(log2 m) + 1
    for the resulting m (checked by the caller)."""
    nE = 2 * k * 2 ** (L - 2)
    word = "EF" * nE
    idx = list(range(nE))
    if shuffle:
        rng.shuffle(idx)
    sfix = []
    pool = idx
    for i in range(1, L):
        sz = 2 ** (L - 1 - i)
        fam = [pool[j * sz:(j + 1) * sz] for j in range(k)]
        sfix.extend(fam)
        pool = [a for f in fam for a in f[: max(1, sz // 2)]] if sz > 1 else pool
        # next family lives inside the union of this one (first halves)
        pool = [a for f in fam for a in f]
        if shuffle:
            rng.shuffle(pool)
    for _ in range(extra_x):
        sfix.append(rng.sample(range(nE), rng.randint(1, 2 ** (L - 2))))
    if ny is None:
        ny = k
    return rigid_design(rng, word, len(sfix), ny, 1, 2, pbad=1.0, ptie_ex=ptie_ex, ptie_mem=ptie_mem, pme=pme,
                        pyx_all=True, hub=hub, sfix=sfix)
