"""Generators of 2CH-with-classes instances whose planted path stays a shortest valid path (for stress tests)."""
import itertools
import random

from clib import CInst, shortest_len, p2_ok


def _inst(N, E, F, cls):
    return CInst(N, E, F, cls, 0, 1)


def planted_shortest(rng, r, nmates, ncls, ncontacts, multi=True, max_tries=6):
    """Planted path X_1..X_r (positions with classes, one type per class), mates in path classes and in new classes,
    random contacts (a node shared by a non-path side and a path side), P2 repaired; every addition is kept only if
    the shortest valid path length stays r.  Returns (inst, planted path) or None."""
    ctype = {}
    pos_cls = []
    for a in range(r):
        if multi and pos_cls and rng.random() < 0.35:
            c = rng.choice(pos_cls)
        else:
            c = rng.randrange(ncls)
        if c not in ctype:
            ctype[c] = rng.randrange(2)
        pos_cls.append(c)
    newc = ncls
    cls = list(pos_cls)
    for _ in range(nmates):
        if rng.random() < 0.7:
            cls.append(rng.choice(pos_cls))
        else:
            cls.append(newc + rng.randrange(2))
    m = len(cls)
    E = [0] * m
    F = [0] * m

    def add(w, ty, z):
        if ty == 0:
            E[w] |= 1 << z
        else:
            F[w] |= 1 << z

    def rem(w, ty, z):
        if ty == 0:
            E[w] &= ~(1 << z)
        else:
            F[w] &= ~(1 << z)

    N = 2
    add(0, ctype[pos_cls[0]], 0)
    add(r - 1, ctype[pos_cls[r - 1]], 1)
    for a in range(r - 1):
        add(a, ctype[pos_cls[a]], N)
        add(a + 1, ctype[pos_cls[a + 1]], N)
        N += 1
    P = [2 * a + ctype[pos_cls[a]] for a in range(r)]
    if shortest_len(_inst(N, E, F, cls)) != r:
        return None

    def ok():
        return shortest_len(_inst(N, E, F, cls)) == r

    # contacts: a fresh node in a non-path side and in a path side (or two non-path sides)
    for _ in range(ncontacts):
        w = rng.randrange(m)
        ty = rng.randrange(2)
        if w < r and ty == ctype[pos_cls[w]]:
            ty = 1 - ty
        if rng.random() < 0.7:
            a = rng.randrange(r)
            w2, ty2 = a, ctype[pos_cls[a]]
        else:
            w2, ty2 = rng.randrange(m), rng.randrange(2)
        if w2 == w and ty2 == ty:
            continue
        z = N
        add(w, ty, z)
        add(w2, ty2, z)
        N += 1
        if not ok():
            rem(w, ty, z)
            rem(w2, ty2, z)
            N -= 1
    # P2 repair
    pairs = [(w, v) for w, v in itertools.combinations(range(m), 2) if cls[w] != cls[v]]
    rng.shuffle(pairs)
    for w, v in pairs:
        if (E[w] & E[v]) or (F[w] & F[v]):
            continue
        done = False
        opts = [0, 1]
        rng.shuffle(opts)
        for ty in opts:
            # try an existing node of one of the two sides first (sometimes), else a fresh node
            cand = []
            if rng.random() < 0.5:
                mw = E[w] if ty == 0 else F[w]
                mv = E[v] if ty == 0 else F[v]
                cand = [(v, z) for z in range(2, N) if (mw >> z) & 1] + [(w, z) for z in range(2, N) if (mv >> z) & 1]
                rng.shuffle(cand)
                cand = cand[:3]
            for (x, z) in cand:
                had = ((E[x] if ty == 0 else F[x]) >> z) & 1
                add(x, ty, z)
                if ok():
                    done = True
                    break
                if not had:
                    rem(x, ty, z)
            if done:
                break
            z = N
            add(w, ty, z)
            add(v, ty, z)
            N += 1
            if ok():
                done = True
                break
            rem(w, ty, z)
            rem(v, ty, z)
            N -= 1
        if not done:
            return None
    I = _inst(N, E, F, cls)
    if not p2_ok(I) or shortest_len(I) != r:
        return None
    return I, tuple(P)
