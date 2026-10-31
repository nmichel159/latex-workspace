"""Random general switch-form instances with many bad pairs (r5-core.md Section 8.4).

design(rng, ...) builds a gcore.Gen:
  * a planted path of r members with types `types` (string over 'EF'), s in the first, t in the last member side,
    a link node in every pair of consecutive member sides;
  * nX switches x_i above random sets S_i of E-members (|S_i| = sizeS), nY switches y_j below random sets T_j of
    F-members (|T_j| = sizeT), y_j < x_i with probability p_xy (so (x_i, y_j) are bad pairs of the planted path
    when x_i is not a minimal E-member and y_j not a maximal F-member); every x_i gets a private F-node and every y_j
    a private E-node (so they are needed items);
  * n_extra random extra nodes in 1-3 random non-path sides;
  * P2 enforced for every incomparable pair without witness by a common E-node, a common F-node (non-path sides
    preferred with probability 0.8), a lower or an upper middle witness among the existing switches (private nodes of
    middle edges recorded in G.medge).
The planted path need not stay shortest; the checks use the shortest valid paths of the result.
"""
from gcore import Gen, closure_le


def projective_lines(q):
    """Lines of the projective plane of prime order q (points 0..q^2+q)."""
    pts = []
    for x in range(q):
        for y in range(q):
            pts.append((x, y, 1))
    for x in range(q):
        pts.append((x, 1, 0))
    pts.append((1, 0, 0))
    idx = {p: i for i, p in enumerate(pts)}

    def norm(v):
        v = [c % q for c in v]
        for c in reversed(v):
            if c:
                inv = pow(c, q - 2, q)
                return tuple((d * inv) % q for d in v)
        return None
    lines = []
    seen = set()
    for a in range(q):
        for b in range(q):
            for c in range(q):
                L = norm((a, b, c))
                if L is None or L in seen:
                    continue
                seen.add(L)
                lines.append(sorted(idx[norm(p)] for p in pts
                                    if (L[0] * p[0] + L[1] * p[1] + L[2] * p[2]) % q == 0))
    return lines


def design(rng, types, nX, nY, sizeS, sizeT, p_xy=1.0, n_extra=0, style="flip", middle=True, S_sets=None,
           T_sets=None, p_node=0.5):
    r = len(types)
    m = r + nX + nY
    Apos = [i for i in range(r) if types[i] == "E"]
    Bpos = [i for i in range(r) if types[i] == "F"]
    X = list(range(r, r + nX))
    Y = list(range(r + nX, m))
    rel = []
    for i, x in enumerate(X):
        S = S_sets[i] if S_sets is not None else rng.sample(Apos, min(sizeS, len(Apos)))
        for a in S:
            rel.append((Apos[a] if S_sets is not None else a, x))
    for j, y in enumerate(Y):
        T = T_sets[j] if T_sets is not None else rng.sample(Bpos, min(sizeT, len(Bpos)))
        for b in T:
            rel.append((y, Bpos[b] if T_sets is not None else b))
    for x in X:
        for y in Y:
            if rng.random() < p_xy:
                rel.append((y, x))
    le = [[a == b for b in range(m)] for a in range(m)]
    for a, b in rel:
        le[a][b] = True
    le = closure_le(le)
    E = [0] * m
    F = [0] * m
    medge = {}
    nn = [0]

    def newnode():
        nn[0] += 1
        return nn[0] - 1

    def put(w, ty, x):
        if ty == "E":
            E[w] |= 1 << x
        else:
            F[w] |= 1 << x
    s = newnode()
    t = newnode()
    put(0, types[0], s)
    put(r - 1, types[r - 1], t)
    for i in range(r - 1):
        z = newnode()
        put(i, types[i], z)
        put(i + 1, types[i + 1], z)
    for x in X:
        put(x, "F", newnode())
    for y in Y:
        put(y, "E", newnode())
    pathside = set((i, types[i]) for i in range(r))
    allsides = [(w, ty) for w in range(m) for ty in "EF"]
    nonpath = [x for x in allsides if x not in pathside]
    for _ in range(n_extra):
        z = newnode()
        for (w, ty) in rng.sample(nonpath, rng.randint(1, 3)):
            put(w, ty, z)
    strict = lambda a, b: le[a][b] and not le[b][a]
    medges = []
    for a in range(m):
        for b in range(a + 1, m):
            if le[a][b] or le[b][a]:
                continue
            if E[a] & E[b] or F[a] & F[b]:
                continue
            low = {w for (w, x) in medges if x == a} & {w for (w, x) in medges if x == b}
            upp = {x for (w, x) in medges if w == a} & {x for (w, x) in medges if w == b}
            if low or upp:
                continue
            opts = []
            if rng.random() < p_node or not middle:
                for ty in "EF":
                    inpath = ((a, ty) in pathside) + ((b, ty) in pathside)
                    opts.append(("node", ty, inpath))
            if middle:
                for w in range(m):
                    if strict(w, a) and strict(w, b):
                        opts.append(("low", w, 0))
                    if strict(a, w) and strict(b, w):
                        opts.append(("up", w, 0))
            if not opts:
                for ty in "EF":
                    inpath = ((a, ty) in pathside) + ((b, ty) in pathside)
                    opts.append(("node", ty, inpath))
            if style == "flip":
                mn = min(o[2] for o in opts)
                opts = [o for o in opts if o[2] == mn] if rng.random() < 0.8 else opts
            o = rng.choice(opts)
            if o[0] == "node":
                z = newnode()
                put(a, o[1], z)
                put(b, o[1], z)
            elif o[0] == "low":
                w = o[1]
                for v in (a, b):
                    z = newnode()
                    put(w, "F", z)
                    put(v, "E", z)
                    medge[z] = (w, v)
                    medges.append((w, v))
            else:
                w = o[1]
                for v in (a, b):
                    z = newnode()
                    put(v, "F", z)
                    put(w, "E", z)
                    medge[z] = (v, w)
                    medges.append((v, w))
    names = [("p", i, types[i]) for i in range(r)] + [("x", i) for i in range(nX)] + [("y", j) for j in range(nY)]
    G = Gen(nn[0], E, F, le, s, t, medge=medge, names=names)
    G.planted = [2 * i + (0 if types[i] == "E" else 1) for i in range(r)]
    return G
