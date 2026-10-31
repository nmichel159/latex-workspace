"""Certificate costs of a planted shortest valid path (agent r5-classes, third run).

All functions take a realised instance I (ccore.Inst) and a valid path P (tuple of sides, position a = P[a]).

f(a): O-members c (type != type of a) with X'_a meeting X_c.
err(a): O-classes D of P (classes used on P with the type opposite to a) all of whose O-sides meet X'_a.
h2_cost(T): min over pairs u, b of T-members of different classes with |u - b| >= 3 of |err(u) | err(b)|
            (0 if no such pair exists: then P has at most 3 T-classes, covered by class groups).
desc_guided(I, P, tau, U): misclassification of sigma_U on the classes of P (r5-classes.md Lemma 2a.1).
"""
import itertools
import ccore as C


def ptypes(I, P):
    """class -> type used on P"""
    out = {}
    for x in P:
        out[I.scls[x]] = x & 1
    return out


def f_sets(I, P):
    r = len(P)
    out = []
    for a in range(r):
        x = P[a]
        m = I.mask.get(x ^ 1, 0)
        out.append({c for c in range(r) if (P[c] & 1) != (x & 1) and m & I.mask[P[c]]})
    return out


def err_sets(I, P):
    pt = ptypes(I, P)
    r = len(P)
    out = []
    for a in range(r):
        x = P[a]
        T = x & 1
        O = 1 - T
        m = I.mask.get(x ^ 1, 0)
        e = set()
        if m:
            for D, ty in pt.items():
                if ty != O:
                    continue
                om = I.Omega[(D, O)]
                if om and all(I.mask[z] & m for z in om):
                    e.add(D)
        out.append(e)
    return out


def h2_cost(I, P, T, errs=None):
    if errs is None:
        errs = err_sets(I, P)
    r = len(P)
    mem = [a for a in range(r) if (P[a] & 1) == T]
    best = None
    for i in range(len(mem)):
        for j in range(i + 1, len(mem)):
            u, b = mem[i], mem[j]
            if b - u < 3 or I.scls[P[u]] == I.scls[P[b]]:
                continue
            if not (I.mask.get(P[u] ^ 1, 0) and I.mask.get(P[b] ^ 1, 0)):
                continue
            c = len(errs[u] | errs[b])
            if best is None or c < best:
                best = c
    if best is None:
        # no far pair of different classes: either at most 3 T-classes (class groups), or a far pair with an
        # empty partner exists (then F2 confines the T-members, again few classes)
        return 0
    return best


def h2(I, P):
    errs = err_sets(I, P)
    return min(h2_cost(I, P, 0, errs), h2_cost(I, P, 1, errs))


def mis(I, P, tau, U, pt=None):
    """misclassification of sigma_U (U a set of tau-sides) on the classes of P"""
    if pt is None:
        pt = ptypes(I, P)
    c = 0
    for D, ty in pt.items():
        covered = I.Omega[(D, tau)] <= U
        # sigma_U puts D into mode 1 - tau iff covered
        if ty == 1 - tau and not covered:
            c += 1
        elif ty == tau and covered:
            c += 1
    return c


def centres(I, nodes=True):
    """candidate centres: every side and (if nodes) every node (as ('s', side) or ('n', node))"""
    out = [("s", z) for z in I.sides]
    if nodes:
        out += [("n", x) for x in range(I.N)]
    return out


def nb(I, tau, cen):
    kind, z = cen
    M = I.mask[z] if kind == "s" else (1 << z)
    return frozenset(i for i in I.sides if (i & 1) == tau and I.mask[i] & M)


def desc_guided(I, P, f=1, g=0, want=False, nodes=True):
    """least misclassification on P over tau and U = union of <= f sets N_tau[centre] and <= g class groups or
    single sides"""
    pt = ptypes(I, P)
    best = None
    arg = None
    for tau in (0, 1):
        sets = {}
        for cen in centres(I, nodes):
            S = nb(I, tau, cen)
            if S not in sets:
                sets[S] = cen
        sl = list(sets.items())
        extra = {}
        for D in I.classes:
            om = I.Omega[(D, tau)]
            if om and om not in extra:
                extra[om] = ("g", D)
        for i in I.sides:
            if (i & 1) == tau:
                S = frozenset([i])
                if S not in extra:
                    extra[S] = ("1", i)
        el = list(extra.items())
        for a in range(f + 1):
            for combo in itertools.combinations(sl, a):
                U0 = frozenset().union(*[S for S, _ in combo]) if combo else frozenset()
                for b in range(g + 1):
                    for gc in itertools.combinations(el, b):
                        U = U0.union(*[S for S, _ in gc]) if gc else U0
                        m = mis(I, P, tau, U, pt)
                        if best is None or m < best:
                            best = m
                            arg = (tau, [c for _, c in combo], [c for _, c in gc])
                            if m == 0 and not want:
                                return 0
    return (best, arg) if want else best
