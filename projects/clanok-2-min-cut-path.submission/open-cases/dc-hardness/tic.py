"""TIC (two-choice interval cover with P2), a special case of 2CH + P2 (hence of the open case of DC).

Instance: K >= 1 and switches w = 0..n-1, each with two spans E[w] = (a, b), F[w] = (c, d) of junctions
(0 <= a <= b <= K; a span (a, b) is the junction set {a, ..., b}; an empty side is None).
A mode vector picks one span per switch; question: do the picked spans cover every edge (j-1, j), j = 1..K
(equivalently: are junctions 0 and K connected in the hypergraph of picked spans)?
P2: for w != v the E-spans share a junction or the F-spans share a junction.

Routines: exact (brute force), coverage test, P2 test, conversion to 2CH (swlib), random instances with P2,
the rigid family R_L as a TIC instance, the NP-hard 'local' family without P2 (two-choice interval cover from
3-SAT, Theorem L(b) of dc-hardness.md), and the window algorithm of Theorem L(a).
"""
import random
import itertools


def covers(K, spans):
    """spans: list of (a, b) or None; True iff every edge 1..K is covered (edge j = (j-1, j) inside [a, b])."""
    reach = [0] * (K + 2)
    for sp in spans:
        if sp is None:
            continue
        a, b = sp
        if b > a:
            reach[a + 1] += 1
            reach[b + 1] -= 1
    c = 0
    for j in range(1, K + 1):
        c += reach[j]
        if c <= 0:
            return False
    return True


def meet(x, y):
    return x is not None and y is not None and max(x[0], y[0]) <= min(x[1], y[1])


def p2_ok(E, F):
    n = len(E)
    return all(meet(E[i], E[l]) or meet(F[i], F[l]) for i in range(n) for l in range(i + 1, n))


def p2_missing(E, F):
    n = len(E)
    return [(i, l) for i in range(n) for l in range(i + 1, n) if not (meet(E[i], E[l]) or meet(F[i], F[l]))]


def exact(K, E, F):
    n = len(E)
    for mask in range(1 << n):
        sp = [F[i] if (mask >> i) & 1 else E[i] for i in range(n)]
        if covers(K, sp):
            return mask
    return None


def relaxed(K, E, F):
    return covers(K, list(E) + list(F))


def to_2ch(K, E, F):
    """Nodes = junctions 0..K; s = 0, t = K."""
    def mask(sp):
        if sp is None:
            return 0
        a, b = sp
        return sum(1 << j for j in range(a, b + 1))
    return (K + 1, [mask(x) for x in E], [mask(x) for x in F], 0, K)


def rigid(L):
    """R_L as TIC: switch k (1..L): path span h_k = (k-1, k), flip span Fl_k = (k, L); h_k is E for odd k."""
    E, F = [], []
    for k in range(1, L + 1):
        h, fl = (k - 1, k), (k, L)
        if k % 2 == 1:
            E.append(h); F.append(fl)
        else:
            E.append(fl); F.append(h)
    return L, E, F


def random_span(rng, K, longp):
    if rng.random() < longp:
        a = rng.randint(0, K)
        b = rng.randint(a, K)
    else:
        a = rng.randint(0, K - 1)
        b = min(K, a + rng.randint(1, 2))
    return (a, b)


def repair_p2(rng, K, E, F):
    """Extend spans until P2 holds: for a bad pair extend one of the two E-spans or F-spans to meet the other."""
    E, F = list(E), list(F)
    while True:
        bad = p2_missing(E, F)
        if not bad:
            return E, F
        i, l = rng.choice(bad)
        S = E if rng.random() < 0.5 else F
        if S[i] is None or S[l] is None:
            S = F if S is E else E
            if S[i] is None or S[l] is None:
                continue
        x, y = S[i], S[l]
        if x[1] < y[0]:
            # extend x right or y left
            if rng.random() < 0.5:
                S[i] = (x[0], y[0])
            else:
                S[l] = (x[1], y[1])
        else:  # y left of x
            if rng.random() < 0.5:
                S[l] = (y[0], x[0])
            else:
                S[i] = (y[1], x[1])


def random_tic(rng, K, n, longp=0.2):
    E = [random_span(rng, K, longp) for _ in range(n)]
    F = [random_span(rng, K, longp) for _ in range(n)]
    E, F = repair_p2(rng, K, E, F)
    return K, E, F


def window_algorithm(K, E, F, maxS=None):
    """Theorem L(a) specialised to TIC: if all F-spans (or all E-spans) lie in a window W, try all sets S of at most
    |W| switches in the concentrated mode.  Here simply: for each type T and each S of size <= maxS, put S in T and
    the rest in the other type.  Exact when maxS >= number of junctions spanned by the concentrated type."""
    n = len(E)
    if maxS is None:
        maxS = n
    for T in ("F", "E"):
        for r in range(0, maxS + 1):
            for S in itertools.combinations(range(n), r):
                Ss = set(S)
                sp = []
                for i in range(n):
                    if (i in Ss) == (T == "F"):
                        sp.append(F[i])
                    else:
                        sp.append(E[i])
                if covers(K, sp):
                    return True
    return False


def local_sat_instance(nvars, clauses):
    """Theorem L(b): two-choice interval cover with spans of at most 2 edges (no P2) from a CNF in which every
    variable has at most one occurrence of one sign (any number of the other sign is allowed here: the block of the
    single occurrence covers all its conflict edges).  Switch = occurrence; F-span = its clause edge; E-span = its
    conflict edges.  Returns (K, E, F, info)."""
    occ = []
    for j, cl in enumerate(clauses):
        for lit in cl:
            occ.append((j, lit))
    E = [None] * len(occ)
    F = [None] * len(occ)
    pos = 0
    edges = []  # list of ('clause', j) or ('conf', w1, w2)
    for j in range(len(clauses)):
        edges.append(("clause", j))
    for z in range(1, nvars + 1):
        P = [w for w, (j, l) in enumerate(occ) if l == z]
        N = [w for w, (j, l) in enumerate(occ) if l == -z]
        if not P or not N:
            continue
        if len(N) == 1:
            single, many = N[0], P
        elif len(P) == 1:
            single, many = P[0], N
        else:
            raise ValueError("variable %d has two occurrences of each sign" % z)
        for w in many:
            edges.append(("conf", single, w))
    K = len(edges)
    # edge index e (1-based) is the edge (e-1, e)
    for e, ed in enumerate(edges, 1):
        if ed[0] == "clause":
            for w, (j, l) in enumerate(occ):
                if j == ed[1]:
                    F[w] = (e - 1, e)
        else:
            _, single, w = ed
            E[w] = (e - 1, e)
            if E[single] is None:
                E[single] = (e - 1, e)
            else:
                E[single] = (min(E[single][0], e - 1), max(E[single][1], e))
    return K, E, F, occ


def satisfiable(nvars, clauses):
    return any(all(any((l > 0) == a[abs(l) - 1] for l in c) for c in clauses)
               for a in itertools.product([False, True], repeat=nvars))
