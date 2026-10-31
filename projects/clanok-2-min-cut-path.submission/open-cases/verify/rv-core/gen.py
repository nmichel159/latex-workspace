"""Random general switch-form instances with P2 (rv-core's own generator).

A planted path of r members (random types) is laid out (s in X_1, y_i in X_i & X_{i+1}, t in X_r); extra switches;
random strict relations and ties that keep the planted path valid; random extra nodes; random middle edges; then P2 is
enforced for every incomparable pair without witness by one of: a common E-node, a common F-node, a lower middle witness
(middle edges w-a, w-b with private nodes) or an upper middle witness.  `style` biases where witness nodes go:
'flip' prefers non-path sides (keeps the planted path long), 'any' uses any side.
"""
import random
from sw import SW


def gen(rng, r, extra, p_rel=0.15, p_tie=0.03, n_extra_nodes=4, p_medge=0.1, style="flip", middle=True):
    m = r + extra
    perm = list(range(m))
    rng.shuffle(perm)
    members = perm[:r]
    types = [rng.choice("EF") for _ in range(r)]
    ptype = {members[i]: types[i] for i in range(r)}
    rel = []

    def closure(rel):
        le = [1 << i for i in range(m)]
        for a, b in rel:
            le[a] |= 1 << b
        ch = True
        while ch:
            ch = False
            for a in range(m):
                x = le[a]
                y = x
                for b in range(m):
                    if x >> b & 1:
                        y |= le[b]
                if y != x:
                    le[a] = y
                    ch = True
        return le

    def ok(le):
        for a, ta in ptype.items():
            for b, tb in ptype.items():
                if ta == "E" and tb == "F" and le[a] >> b & 1:
                    return False
        return True
    le = closure(rel)
    for a in range(m):
        for b in range(m):
            if a == b:
                continue
            pr = p_tie if a < b else 0
            if rng.random() < p_rel or rng.random() < pr:
                cand = rel + [(a, b)] + ([(b, a)] if rng.random() < pr else [])
                le2 = closure(cand)
                if ok(le2):
                    rel, le = cand, le2
    E = [0] * m
    F = [0] * m
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
    put(members[0], ptype[members[0]], s)
    put(members[-1], ptype[members[-1]], t)
    for i in range(r - 1):
        y = newnode()
        put(members[i], ptype[members[i]], y)
        put(members[i + 1], ptype[members[i + 1]], y)
    pathside = set((w, ptype[w]) for w in members)
    allsides = [(w, ty) for w in range(m) for ty in "EF"]
    nonpath = [x for x in allsides if x not in pathside]
    for _ in range(n_extra_nodes):
        x = newnode()
        pool = nonpath if style == "flip" else allsides
        for (w, ty) in rng.sample(pool, rng.randint(1, 3)):
            put(w, ty, x)
    medges = []
    strict = lambda a, b: (le[a] >> b & 1) and not (le[b] >> a & 1)
    if middle:
        for a in range(m):
            for b in range(m):
                if a != b and strict(a, b) and rng.random() < p_medge:
                    x = newnode()
                    put(a, "F", x)
                    put(b, "E", x)
                    medges.append((a, b, x))
    # P2
    for a in range(m):
        for b in range(a + 1, m):
            if le[a] >> b & 1 or le[b] >> a & 1:
                continue
            if E[a] & E[b] or F[a] & F[b]:
                continue
            low = {w for (w, x, _) in medges if x == a} & {w for (w, x, _) in medges if x == b}
            upp = {x for (w, x, _) in medges if w == a} & {x for (w, x, _) in medges if w == b}
            if any(strict(w, a) and strict(w, b) for w in low) or any(strict(a, w) and strict(b, w) for w in upp):
                continue
            opts = []
            for ty in "EF":
                inpath = ((a, ty) in pathside) + ((b, ty) in pathside)
                opts.append(("node", ty, inpath))
            if middle:
                for w in range(m):
                    if strict(w, a) and strict(w, b):
                        opts.append(("low", w, 0))
                    if strict(a, w) and strict(b, w):
                        opts.append(("up", w, 0))
            if style == "flip":
                mn = min(o[2] for o in opts)
                opts = [o for o in opts if o[2] == mn] if rng.random() < 0.8 else opts
            o = rng.choice(opts)
            if o[0] == "node":
                x = newnode()
                put(a, o[1], x)
                put(b, o[1], x)
            elif o[0] == "low":
                w = o[1]
                for z in (a, b):
                    x = newnode()
                    put(w, "F", x)
                    put(z, "E", x)
                    medges.append((w, z, x))
            else:
                w = o[1]
                for z in (a, b):
                    x = newnode()
                    put(z, "F", x)
                    put(w, "E", x)
                    medges.append((z, w, x))
    G = SW(nn[0], s, t, E, F, rel, medges)
    G.planted = [2 * w + (0 if ptype[w] == "E" else 1) for w in members]
    return G
