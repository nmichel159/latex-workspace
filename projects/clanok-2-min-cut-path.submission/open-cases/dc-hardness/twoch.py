"""Two-choice hypergraph connectivity (2CH), the contracted form of the switch model SW of theory-dc.md.

Instance: nodes 0..N-1 with terminals s, t; switches i = 0..n-1, each with two node sets E[i], F[i] (bit masks).
A mode vector picks E[i] or F[i] for every switch; the picked sets are hyperedges.  Question: is s connected to t?
P2: for i != l, E[i] & E[l] != 0 or F[i] & F[l] != 0.

SW + P2 and 2CH + P2 are the same problem: contract the components of the fixed bottom-top edges into nodes; conversely
give every node x a bottom vertex b_x, a top vertex t_x and the fixed edge b_x t_x, and put Nb(i) = {b_x : x in E[i]},
Nt(i) = {t_x : x in F[i]}.

Exact routines only (brute force over modes for small n).
"""
import random


def connected(N, hyper, s, t):
    """s ~ t in the hypergraph with the given hyperedges (masks)."""
    if s == t:
        return True
    comp = 1 << s
    changed = True
    rest = [h for h in hyper if h]
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


def solve(inst):
    """Return a mode vector (bit i = 1 means F-mode) that connects s and t, or None.  Brute force."""
    N, E, F, s, t = inst
    n = len(E)
    for mask in range(1 << n):
        hyper = [F[i] if (mask >> i) & 1 else E[i] for i in range(n)]
        if connected(N, hyper, s, t):
            return mask
    return None


def p2_ok(E, F):
    n = len(E)
    return all((E[i] & E[l]) or (F[i] & F[l]) for i in range(n) for l in range(i + 1, n))


def exceptional_solve(inst, K):
    """Least k <= K such that some configuration 'all switches in mode M except a set X of size k' connects s, t;
    returns (k, M, X) or None."""
    import itertools
    N, E, F, s, t = inst
    n = len(E)
    for k in range(K + 1):
        for X in itertools.combinations(range(n), k):
            Xs = set(X)
            for M in (0, 1):
                hyper = []
                for i in range(n):
                    m = M ^ (1 if i in Xs else 0)
                    hyper.append(F[i] if m else E[i])
                if connected(N, hyper, s, t):
                    return k, M, X
    return None


def random_p2_instance(rng, N, n, pe, pf):
    """Random sets, then every pair violating P2 gets a new shared node in E or in F (coin flip)."""
    E = [sum(1 << x for x in range(N) if rng.random() < pe) for _ in range(n)]
    F = [sum(1 << x for x in range(N) if rng.random() < pf) for _ in range(n)]
    NN = N
    for i in range(n):
        for l in range(i + 1, n):
            if not ((E[i] & E[l]) or (F[i] & F[l])):
                z = NN
                NN += 1
                if rng.random() < 0.5:
                    E[i] |= 1 << z
                    E[l] |= 1 << z
                else:
                    F[i] |= 1 << z
                    F[l] |= 1 << z
    return (NN, E, F, 0, 1)


def fmt_inst(inst):
    N, E, F, s, t = inst
    def bits(m):
        return [x for x in range(N) if (m >> x) & 1]
    return "N=%d s=%d t=%d " % (N, s, t) + " ".join("[%d: E=%s F=%s]" % (i, bits(E[i]), bits(F[i])) for i in range(len(E)))
