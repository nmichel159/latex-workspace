"""Planted instances of the general switch form with many bad pairs (reviewer rv-core-65, own code).

A planted path X_1..X_r (members 0..r-1, word of types), contact nodes c_i in X_i & X_{i+1}, s in X_1, t in X_r.
Order: every switch gets a chain type, 'E' (members of type E and up-mates) or 'F' (members of type F and down-mates),
and strict relations a < b are drawn only for (F, F), (F, E), (E, E); the transitive closure keeps every E-typed
switch out of the down-closure of the F-typed ones, so the planted path stays valid.  Bad pairs come from relations
down-mate < up-mate, non-maximal F-member < non-minimal E-member, and so on.  P2 is enforced by fresh witness nodes
or middle witnesses.  The planted path need not stay shortest: the tests recompute all shortest valid paths.
"""
import random
from gsf import Inst, closure, bits


def planted_inst(rng, r=6, n_up=3, n_down=3, n_free=0, word=None, p_rel=0.35, p_bad=0.6, p_tie=0.05,
                 p_side=0.15, p_contact=0.3, p_med=0.25, pool=None, witness=None, name="planted"):
    if word is None:
        word = [rng.choice("EF") for _ in range(r)]
    r = len(word)
    m = r + n_up + n_down + n_free
    ctype = list(word) + ["E"] * n_up + ["F"] * n_down + ["X"] * n_free
    ups = list(range(r, r + n_up))
    downs = list(range(r + n_up, r + n_up + n_down))
    frees = list(range(r + n_up + n_down, m))
    le = [[i == j for j in range(m)] for i in range(m)]
    Em = [i for i in range(r) if word[i] == "E"]
    Fm = [i for i in range(r) if word[i] == "F"]
    # mates: up-mate above a random E-member, down-mate below a random F-member
    for x in ups:
        if Em:
            le[rng.choice(Em)][x] = True
    for y in downs:
        if Fm:
            le[y][rng.choice(Fm)] = True
    # random relations of allowed shape (a < b with (type a, type b) in (F,F), (F,E), (E,E))
    order = list(range(m))
    rng.shuffle(order)
    rank = {w: i for i, w in enumerate(order)}
    for a in range(m):
        for b in range(m):
            if a == b or rank[a] > rank[b]:
                continue
            ta, tb = ctype[a], ctype[b]
            if ta == "X" or tb == "X":
                if ta == tb == "X" and rng.random() < p_rel:
                    le[a][b] = True
                continue
            if (ta, tb) == ("E", "F"):
                continue
            pr = p_rel
            if a in downs and b in ups:
                pr = p_bad
            if rng.random() < pr:
                le[a][b] = True
    # ties inside one chain type
    for a in range(m):
        for b in range(a + 1, m):
            if ctype[a] == ctype[b] != "X" and rng.random() < p_tie:
                le[a][b] = le[b][a] = True
    le = closure(le)
    for a in range(m):
        for b in range(m):
            if le[a][b] and ctype[a] == "E" and ctype[b] == "F":
                raise AssertionError("closure created E <= F")
    N = 0

    def fresh():
        nonlocal N
        N += 1
        return N - 1
    s = fresh()
    t = fresh()
    E = [0] * m
    F = [0] * m
    side = lambda w, typ: (F if typ else E)
    # member sides
    c = [fresh() for _ in range(r - 1)]
    for i in range(r):
        typ = 1 if word[i] == "F" else 0
        msk = 0
        if i == 0:
            msk |= 1 << s
        if i == r - 1:
            msk |= 1 << t
        if i > 0:
            msk |= 1 << c[i - 1]
        if i < r - 1:
            msk |= 1 << c[i]
        side(i, typ)[i] |= msk
    # node pool for partners and mates
    if pool is None:
        pool = max(3, r // 2 + 1)
    poolnodes = [fresh() for _ in range(pool)]
    for w in range(m):
        for typ in (0, 1):
            if w < r and typ == (1 if word[w] == "F" else 0):
                continue          # member side already set
            for nd in poolnodes:
                if rng.random() < p_side:
                    side(w, typ)[w] |= 1 << nd
            # occasional contacts with member sides (a contact node c_i lies in X_i and X_{i+1})
            if w >= r and rng.random() < p_contact and c:
                side(w, typ)[w] |= 1 << rng.choice(c)
    medges = {}

    def lt(a, b):
        return le[a][b] and not le[b][a]

    def add_med(z, v):
        if (z, v) in medges:
            return
        nd = fresh()
        medges[(z, v)] = nd
        F[z] |= 1 << nd
        E[v] |= 1 << nd
    for z in range(m):
        for v in range(m):
            if lt(z, v) and rng.random() < p_med:
                add_med(z, v)
    modes = witness or ["freshE", "freshF", "low", "up", "freshE", "freshF"]

    def ok(x, y):
        if E[x] & E[y] or F[x] & F[y]:
            return True
        for (z, v) in medges:
            if v == x and (z, y) in medges:
                return True
            if z == x and (y, v) in medges:
                return True
        return False
    for x in range(m):
        for y in range(x + 1, m):
            if le[x][y] or le[y][x] or ok(x, y):
                continue
            tries = 0
            while not ok(x, y) and tries < 30:
                tries += 1
                mode = rng.choice(modes)
                if mode == "freshE":
                    # avoid joining two member E-sides directly when possible
                    if x < r and y < r and word[x] == word[y] == "E":
                        continue
                    nd = fresh()
                    E[x] |= 1 << nd
                    E[y] |= 1 << nd
                elif mode == "freshF":
                    if x < r and y < r and word[x] == word[y] == "F":
                        continue
                    nd = fresh()
                    F[x] |= 1 << nd
                    F[y] |= 1 << nd
                elif mode == "low":
                    zs = [z for z in range(m) if lt(z, x) and lt(z, y)]
                    if zs:
                        z = rng.choice(zs)
                        add_med(z, x)
                        add_med(z, y)
                elif mode == "up":
                    zs = [z for z in range(m) if lt(x, z) and lt(y, z)]
                    if zs:
                        z = rng.choice(zs)
                        add_med(x, z)
                        add_med(y, z)
            if not ok(x, y):
                nd = fresh()
                if x < r and y < r and word[x] == word[y] == "E":
                    F[x] |= 1 << nd
                    F[y] |= 1 << nd
                else:
                    E[x] |= 1 << nd
                    E[y] |= 1 << nd
    I = Inst(N, s, t, le, E, F, medges, name)
    I.planted = [(i, 1 if word[i] == "F" else 0) for i in range(r)]
    return I
