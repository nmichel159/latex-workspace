"""Generators of general switch forms with P2 (random, and planted shortest valid paths)."""
import itertools
import random

from glib import GInst, close_preorder, shortest_len, p2_violations, bits


def _mk(N, E, F, rel, medges):
    return GInst(N, E, F, rel, 0, 1, medges)


def rand_order(rng, m, p_rel, p_tie):
    rel = [[0] * m for _ in range(m)]
    perm = list(range(m))
    rng.shuffle(perm)
    for a in range(m):
        for b in range(a + 1, m):
            if rng.random() < p_rel:
                rel[perm[a]][perm[b]] = 1
                if rng.random() < p_tie:
                    rel[perm[b]][perm[a]] = 1
    return rel


def repair_p2_g(rng, G_args, keep=None, p_mid=0.4, max_rounds=400):
    """G_args = [N, E, F, rel, medges] (mutated).  keep(): predicate on the instance that must stay true.
    Returns True if P2 holds at the end."""
    N, E, F, rel, medges = G_args
    for _ in range(max_rounds):
        G = _mk(N, E, F, rel, medges)
        viol = p2_violations(G)
        if not viol:
            G_args[0] = N
            return True
        x, y = rng.choice(viol)
        opts = ["E", "F"]
        below = [w for w in range(G.m) if G.lt(w, x) and G.lt(w, y)]
        above = [w for w in range(G.m) if G.lt(x, w) and G.lt(y, w)]
        if below and rng.random() < p_mid:
            opts.append("lo")
        if above and rng.random() < p_mid:
            opts.append("hi")
        rng.shuffle(opts)
        done = False
        for o in opts:
            saveN = N
            saveE, saveF, saveM = list(E), list(F), list(medges)
            if o == "E":
                E[x] |= 1 << N
                E[y] |= 1 << N
                N += 1
            elif o == "F":
                F[x] |= 1 << N
                F[y] |= 1 << N
                N += 1
            elif o == "lo":
                w = rng.choice(below)
                for v in (x, y):
                    if not any(e[0] == w and e[1] == v for e in medges):
                        F[w] |= 1 << N
                        E[v] |= 1 << N
                        medges.append((w, v, N))
                        N += 1
            else:
                w = rng.choice(above)
                for v in (x, y):
                    if not any(e[0] == v and e[1] == w for e in medges):
                        F[v] |= 1 << N
                        E[w] |= 1 << N
                        medges.append((v, w, N))
                        N += 1
            if keep is None or keep(_mk(N, E, F, rel, medges)):
                done = True
                break
            N = saveN
            E[:], F[:], medges[:] = saveE, saveF, saveM
        if not done:
            G_args[0] = N
            return False
    G_args[0] = N
    return not p2_violations(_mk(N, E, F, rel, medges))


def rand_general(rng, m, nn, dens=0.3, p_rel=0.25, p_tie=0.2, p_med=0.15):
    rel = rand_order(rng, m, p_rel, p_tie)
    le = close_preorder(m, rel)
    E = [0] * m
    F = [0] * m
    for w in range(m):
        for z in range(nn):
            if rng.random() < dens:
                E[w] |= 1 << z
            if rng.random() < dens:
                F[w] |= 1 << z
    N = nn
    medges = []
    for y in range(m):
        for x in range(m):
            if le[y][x] and not le[x][y] and rng.random() < p_med:
                F[y] |= 1 << N
                E[x] |= 1 << N
                medges.append((y, x, N))
                N += 1
    args = [N, E, F, rel, medges]
    if not repair_p2_g(rng, args):
        return None
    return _mk(*args)


def planted_general(rng, r, nmates, ncontacts, nmed, p_rel=0.3, p_tie=0.15):
    """planted path of r members (random types), order relations that keep the path valid, mates, contacts and
    middle edges that keep the shortest valid path length r, P2 repaired under the same condition."""
    types = [rng.randrange(2) for _ in range(r)]
    m = r + nmates
    # order: random relations, reject those creating E-member <= F-member
    rel = [[0] * m for _ in range(m)]
    pairs = [(a, b) for a in range(m) for b in range(m) if a != b]
    rng.shuffle(pairs)
    for (a, b) in pairs[: int(p_rel * len(pairs) / 2)]:
        rel[a][b] = 1
        le = close_preorder(m, rel)
        bad = any(le[i][j] for i in range(r) for j in range(r) if types[i] == 0 and types[j] == 1)
        if bad:
            rel[a][b] = 0
        elif rng.random() < p_tie:
            rel[b][a] = 1
            le = close_preorder(m, rel)
            if any(le[i][j] for i in range(r) for j in range(r) if types[i] == 0 and types[j] == 1):
                rel[b][a] = 0
    E = [0] * m
    F = [0] * m

    def put(w, ty, z):
        if ty == 0:
            E[w] |= 1 << z
        else:
            F[w] |= 1 << z

    def unput(w, ty, z):
        if ty == 0:
            E[w] &= ~(1 << z)
        else:
            F[w] &= ~(1 << z)
    N = 2
    put(0, types[0], 0)
    put(r - 1, types[r - 1], 1)
    for a in range(r - 1):
        put(a, types[a], N)
        put(a + 1, types[a + 1], N)
        N += 1
    medges = []
    P = tuple(2 * a + types[a] for a in range(r))

    def ok(G=None):
        G = G or _mk(N, E, F, rel, medges)
        return shortest_len(G) == r

    if not ok():
        return None
    for _ in range(ncontacts):
        w, ty = rng.randrange(m), rng.randrange(2)
        if rng.random() < 0.7:
            a = rng.randrange(r)
            w2, ty2 = a, types[a]
        else:
            w2, ty2 = rng.randrange(m), rng.randrange(2)
        if (w, ty) == (w2, ty2):
            continue
        put(w, ty, N)
        put(w2, ty2, N)
        N += 1
        if not ok():
            N -= 1
            unput(w, ty, N)
            unput(w2, ty2, N)
    le = close_preorder(m, rel)
    strict = [(y, x) for y in range(m) for x in range(m) if le[y][x] and not le[x][y]]
    rng.shuffle(strict)
    for (y, x) in strict[:nmed]:
        F[y] |= 1 << N
        E[x] |= 1 << N
        medges.append((y, x, N))
        N += 1
        if not ok():
            N -= 1
            medges.pop()
            F[y] &= ~(1 << N)
            E[x] &= ~(1 << N)
    args = [N, E, F, rel, medges]
    if not repair_p2_g(rng, args, keep=lambda G: shortest_len(G) == r):
        return None
    G = _mk(*args)
    if p2_violations(G) or shortest_len(G) != r:
        return None
    return G, P
