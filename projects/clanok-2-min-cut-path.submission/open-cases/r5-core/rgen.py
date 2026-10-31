"""Rigid-word designs with many bad pairs (r5-core.md Section 8.4).

rdesign(rng, W, S_sets, T_sets, ...) builds a gcore.Gen:
  * R(W) in 2CH form (r4-general.md Section 6, written from the text): members p = 1..L, path side h_p of type W_p,
    flip side Fl_p of the other type; s in h_1, t in h_L, link nodes in h_p and h_{p+1}; for p < q a node z_pq in
    Fl_p and h_q if W_p != W_q, a node w_pq in Fl_p and Fl_q if W_p == W_q (every member forward);
  * switches x_i above the E-members of S_sets[i] (positions, 1-based), switches y_j below the F-members of
    T_sets[j]; y_j < x_i for every pair with probability p_xy; a private F-node for every x_i and a private E-node for
    every y_j;
  * P2 for the new switches by nodes in sides that are dead on the planted path (hubs: one E-node in all E(x_i), one
    F-node in all F(y_j); x_i ∥ E-member a: a node of F(x_i) ∩ Fl_a; x_i ∥ F-member b: a node of E(x_i) ∩ Fl_b, or
    with probability p_low a lower middle witness y_j < x_i, b; y_j ∥ F-member b: a node of E(y_j) ∩ Fl_b, or with
    probability p_contact a node of F(y_j) ∩ h_b (a contact, allowed only next to the previous contact); y_j ∥
    E-member a: a node of F(y_j) ∩ Fl_a, or with probability p_up an upper middle witness x_i > y_j, a).
The planted path h_1 .. h_L is checked to be a shortest valid path by the callers.
"""
from gcore import Gen, closure_le


def rdesign(rng, W, S_sets, T_sets, p_xy=1.0, p_low=0.0, p_up=0.0, p_contact=0.0, hubs=True):
    L = len(W)
    nX, nY = len(S_sets), len(T_sets)
    m = L + nX + nY
    X = list(range(L, L + nX))
    Y = list(range(L + nX, m))
    E = [0] * m
    F = [0] * m
    medge = {}
    nn = [0]

    def newnode():
        nn[0] += 1
        return nn[0] - 1

    def put(w, ty, z):
        if ty == "E":
            E[w] |= 1 << z
        else:
            F[w] |= 1 << z

    def h(p):          # 1-based member p -> (switch, type) of its path side
        return (p - 1, W[p - 1])

    def fl(p):
        return (p - 1, "F" if W[p - 1] == "E" else "E")
    s = newnode()
    t = newnode()
    put(*h(1), s)
    put(*h(L), t)
    for p in range(1, L):
        z = newnode()
        put(*h(p), z)
        put(*h(p + 1), z)
    for p in range(1, L + 1):
        for q in range(p + 1, L + 1):
            z = newnode()
            if W[p - 1] != W[q - 1]:
                put(*fl(p), z)
                put(*h(q), z)
            else:
                put(*fl(p), z)
                put(*fl(q), z)
    rel = []
    for i, S in enumerate(S_sets):
        for p in S:
            assert W[p - 1] == "E"
            rel.append((p - 1, X[i]))
    for j, T in enumerate(T_sets):
        for p in T:
            assert W[p - 1] == "F"
            rel.append((Y[j], p - 1))
    for x in X:
        for y in Y:
            if rng.random() < p_xy:
                rel.append((y, x))
    le = [[a == b for b in range(m)] for a in range(m)]
    for a, b in rel:
        le[a][b] = True
    le = closure_le(le)
    for x in X:
        put(x, "F", newnode())
    for y in Y:
        put(y, "E", newnode())
    if hubs:
        hx, hy = newnode(), newnode()
        for x in X:
            put(x, "E", hx)
        for y in Y:
            put(y, "F", hy)
    strict = lambda a, b: le[a][b] and not le[b][a]
    lmn = {}
    umn = {}

    def mid(lo, hi):
        z = newnode()
        put(lo, "F", z)
        put(hi, "E", z)
        medge[z] = (lo, hi)
    contact_of = {}
    for x in X:
        for y in Y:
            if not (le[x][y] or le[y][x]):
                z = newnode()
                put(x, "F", z)
                put(y, "F", z)
    for x in X:
        for p in range(1, L + 1):
            w = p - 1
            if le[w][x] or le[x][w]:
                continue
            if W[p - 1] == "E":
                z = newnode()
                put(x, "F", z)
                put(*fl(p), z)
            else:
                lows = [y for y in Y if strict(y, x) and strict(y, w)]
                if lows and rng.random() < p_low:
                    y = rng.choice(lows)
                    mid(y, x)
                    mid(y, w)
                else:
                    z = newnode()
                    put(x, "E", z)
                    put(*fl(p), z)
    for y in Y:
        for p in range(1, L + 1):
            w = p - 1
            if le[w][y] or le[y][w]:
                continue
            if W[p - 1] == "F":
                prev = contact_of.get(y)
                if rng.random() < p_contact and (prev is None or abs(prev - p) <= 2):
                    z = newnode()
                    put(y, "F", z)
                    put(*h(p), z)
                    contact_of[y] = p if prev is None else min(prev, p)
                else:
                    z = newnode()
                    put(y, "E", z)
                    put(*fl(p), z)
            else:
                ups = [x for x in X if strict(y, x) and strict(w, x)]
                if ups and rng.random() < p_up:
                    x = rng.choice(ups)
                    mid(y, x)
                    mid(w, x)
                else:
                    z = newnode()
                    put(y, "F", z)
                    put(*fl(p), z)
    names = [("m", p, W[p - 1]) for p in range(1, L + 1)] + [("x", i) for i in range(nX)] + \
            [("y", j) for j in range(nY)]
    G = Gen(nn[0], E, F, le, s, t, medge=medge, names=names)
    G.planted = [2 * (p - 1) + (0 if W[p - 1] == "E" else 1) for p in range(1, L + 1)]
    return G
