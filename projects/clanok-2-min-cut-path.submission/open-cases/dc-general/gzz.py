"""2CH with classes (2CHC): the switch model of theory-dc.md with ties (agent DC-general).

Instance (N, E, F, cls, s, t): nodes 0..N-1, terminals s != t; switches i = 0..n-1 with node sets E[i], F[i] (bit masks)
and a class label cls[i].  A mode vector assigns one mode (E or F) to every CLASS; switch i picks E[i] or F[i] by the mode
of its class.  Question: are s and t connected in the hypergraph of the picked sets?
P2 (classes): for switches i, l of different classes, E[i] & E[l] != 0 or F[i] & F[l] != 0.
With every class a singleton this is 2CH (dc-hardness/twoch.py).

As a ZZ instance (theory-dc.md Theorem 13): bottoms (equivalent to u), tops (equivalent to v), one element per switch,
switches of one class equivalent, switches of different classes incomparable.  A node x in some E-set gets a bottom b_x,
a node in some F-set a top t_x, both get the fixed edge b_x t_x; switch i is joined to the bottoms of E[i] and to the tops
of F[i].  A class in the down-set D is a class of valleys (F-mode), otherwise of peaks (E-mode).  P2 of 2CHC is P2 of ZZ.
"""
import os
import sys
import random

HERE = os.path.dirname(os.path.abspath(__file__))
ALG = os.path.join(HERE, "..", "dc-algorithm")
sys.path.insert(0, HERE)
sys.path.insert(0, ALG)
sys.setrecursionlimit(100000)
import zz  # noqa: E402  (read-only import of agent DC-algorithm's code)


def bits_of(m):
    out = []
    while m:
        low = m & -m
        out.append(low.bit_length() - 1)
        m ^= low
    return out


def connected(hyper, s, t):
    if s == t:
        return True
    comp = 1 << s
    rest = [h for h in hyper if h]
    changed = True
    while changed:
        changed = False
        keep = []
        for h in rest:
            if h & comp:
                comp |= h
                changed = True
            else:
                keep.append(h)
        rest = keep
        if (comp >> t) & 1:
            return True
    return bool((comp >> t) & 1)


def classes(inst):
    return sorted(set(inst[3]))


def picked(inst, modes):
    """modes: dict class -> 0 (E) / 1 (F)."""
    N, E, F, cls, s, t = inst
    return [F[i] if modes[cls[i]] else E[i] for i in range(len(E))]


def brute(inst):
    """A connecting class-mode dict, or None (brute force over 2^#classes)."""
    N, E, F, cls, s, t = inst
    K = classes(inst)
    for mask in range(1 << len(K)):
        modes = {c: (mask >> j) & 1 for j, c in enumerate(K)}
        if connected(picked(inst, modes), s, t):
            return modes
    return None


def all_solutions(inst):
    N, E, F, cls, s, t = inst
    K = classes(inst)
    out = []
    for mask in range(1 << len(K)):
        modes = {c: (mask >> j) & 1 for j, c in enumerate(K)}
        if connected(picked(inst, modes), s, t):
            out.append(modes)
    return out


def relaxed(inst):
    N, E, F, cls, s, t = inst
    return connected(list(E) + list(F), s, t)


def p2_missing(inst):
    N, E, F, cls, s, t = inst
    n = len(E)
    return [(i, l) for i in range(n) for l in range(i + 1, n)
            if cls[i] != cls[l] and not (E[i] & E[l]) and not (F[i] & F[l])]


def p2_ok(inst):
    return not p2_missing(inst)


def to_zz(inst):
    """2CHC -> zz.ZZ (preorder given by le) and the element names."""
    N, E, F, cls, s, t = inst
    n_sw = len(E)
    inE, inF = 0, 0
    for i in range(n_sw):
        inE |= E[i]
        inF |= F[i]
    names = ["u"]
    bottom, top = {s: 0}, {}
    for x in range(N):
        if x != s and (inE >> x) & 1:
            bottom[x] = len(names)
            names.append(("b", x))
    sw0 = len(names)
    for i in range(n_sw):
        names.append(("sw", i))
    for x in range(N):
        if x != t and (inF >> x) & 1:
            top[x] = len(names)
            names.append(("t", x))
    top[t] = len(names)
    names.append("v")
    # (a node t in an E-set got its bottom, and a node s in an F-set its top, in the loops above)
    n = len(names)
    u, v = 0, top[t]
    B = set(bottom.values())
    T = set(top.values())
    le = [[False] * n for _ in range(n)]
    for a in range(n):
        for b in range(n):
            if a == b or a in B or b in T:
                le[a][b] = True
    for i in range(n_sw):
        for l in range(n_sw):
            if cls[i] == cls[l]:
                le[sw0 + i][sw0 + l] = True
    R = []
    for x in range(N):
        if x in bottom and x in top and (bottom[x], top[x]) != (u, v):
            R.append((bottom[x], top[x]))
    for i in range(n_sw):
        for x in bits_of(E[i]):
            R.append((bottom[x], sw0 + i))
        for x in bits_of(F[i]):
            R.append((sw0 + i, top[x]))
    return zz.ZZ(n, None, R, u, v, le=le), names


def random_inst(rng, N, n, ncls, pe, pf, p2=True, newnode=0.5, maxN=40):
    """Random 2CHC instance; s = 0, t = 1; P2 repaired by shared nodes (new with probability newnode)."""
    E = [sum(1 << x for x in range(N) if rng.random() < pe) for _ in range(n)]
    F = [sum(1 << x for x in range(N) if rng.random() < pf) for _ in range(n)]
    cls = [rng.randrange(ncls) for _ in range(n)]
    inst = (N, E, F, cls, 0, 1)
    if p2:
        inst = repair(rng, inst, newnode, maxN)
    return inst


def repair(rng, inst, newnode=0.5, maxN=40):
    N, E, F, cls, s, t = inst
    E, F = list(E), list(F)
    n = len(E)
    order = [(i, l) for i in range(n) for l in range(i + 1, n)]
    rng.shuffle(order)
    for i, l in order:
        if cls[i] != cls[l] and not (E[i] & E[l]) and not (F[i] & F[l]):
            if rng.random() < newnode and N < maxN:
                z = N
                N += 1
            else:
                z = rng.randrange(N)
            if rng.random() < 0.5:
                E[i] |= 1 << z
                E[l] |= 1 << z
            else:
                F[i] |= 1 << z
                F[l] |= 1 << z
    return (N, E, F, cls, s, t)


def fmt(inst):
    N, E, F, cls, s, t = inst
    return "N=%d s=%d t=%d " % (N, s, t) + " ".join(
        "[%d c%d: E=%s F=%s]" % (i, cls[i], bits_of(E[i]), bits_of(F[i])) for i in range(len(E)))


if __name__ == "__main__":
    # self-check: brute force on 2CHC = exact ZZ answer on the conversion
    seed, count = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    stats = {}
    for it in range(count):
        inst = random_inst(rng, rng.randint(3, 7), rng.randint(2, 8), rng.randint(1, 5),
                           rng.uniform(0.1, 0.4), rng.uniform(0.1, 0.4), p2=rng.random() < 0.7)
        b = brute(inst) is not None
        z, _ = to_zz(inst)
        e = zz.exact_dfs(z)[0]
        e2 = zz.exact(z)[0]
        p2a = p2_ok(inst)
        p2b = not z.p2_bad()
        key = (b, e, e2, p2a, p2b)
        stats[key] = stats.get(key, 0) + 1
        if b != e or e != e2 or p2a != p2b:
            print("MISMATCH", fmt(inst), key)
    print(stats)
