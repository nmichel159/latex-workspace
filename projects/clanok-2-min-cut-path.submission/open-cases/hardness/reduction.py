"""The reduction from 3-SAT to PATH-IN-MIN-CUT (= deciding cp(u,v) = c(u,v)), theory-hardness.md Section 2.

A formula is a list of clauses; a clause is a list of non-zero integers (i = x_i, -i = not x_i); repeated
literals are allowed.  build(phi) returns (UG, u, v, info).

Construction (m clauses, L literal occurrences in total, c0 = (m + 1) + 2L, M = c0 + 2):
  K_A: a clique on M vertices containing u = h_0, h_1, ..., h_m, a_1, a_2 (and fillers);
  K_B: a clique on M vertices containing beta_0, ..., beta_m = v, b_1, b_2 (and fillers);
  F:   the edges h_k beta_k, k = 0..m;
  for the j-th literal of clause C_k an occurrence vertex o_{k,j}:
       literal x_i:     o adjacent to beta_{k-1}, beta_k (in K_B) and a_1, a_2 (in K_A);
       literal not x_i: o adjacent to h_{k-1},   h_k    (in K_A) and b_1, b_2 (in K_B);
  sync edges: the occurrence vertices of each variable form a path (in the order of occurrence).
"""

import itertools
import random

from exact import UG


def build(phi, filler=True):
    m = len(phi)
    L = sum(len(C) for C in phi)
    c0 = (m + 1) + 2 * L
    M = c0 + 2
    assert M >= m + 3
    h = list(range(0, m + 1))
    a1, a2 = m + 1, m + 2
    KA = list(range(0, M))
    beta = [M + k for k in range(m + 1)]
    b1, b2 = M + m + 1, M + m + 2
    KB = list(range(M, 2 * M))
    u, v = h[0], beta[m]
    nxt = 2 * M
    edges = []
    for grp in (KA, KB):
        for x, y in itertools.combinations(grp, 2):
            edges.append((x, y))
    for k in range(m + 1):
        edges.append((h[k], beta[k]))
    occ = {}            # (k, j) -> vertex, k = 1..m
    groups = {}         # variable -> list of vertices
    for k, C in enumerate(phi, start=1):
        for j, lit in enumerate(C):
            o = nxt
            nxt += 1
            occ[(k, j)] = o
            groups.setdefault(abs(lit), []).append(o)
            if lit > 0:
                edges += [(o, beta[k - 1]), (o, beta[k]), (o, a1), (o, a2)]
            else:
                edges += [(o, h[k - 1]), (o, h[k]), (o, b1), (o, b2)]
    for var, os_ in groups.items():
        for x, y in zip(os_, os_[1:]):
            edges.append((x, y))
    g = UG(nxt, edges)
    info = dict(m=m, L=L, c0=c0, M=M, KA=KA, KB=KB, h=h, beta=beta, occ=occ, groups=groups, a=(a1, a2), b=(b1, b2))
    return g, u, v, info


def intended_cuts(info):
    """{assignment (tuple of booleans over sorted variables): A_tau}."""
    vars_ = sorted(info["groups"])
    res = {}
    for bits in itertools.product((False, True), repeat=len(vars_)):
        A = set(info["KA"])
        for var, val in zip(vars_, bits):
            if val:
                A.update(info["groups"][var])
        res[bits] = frozenset(A)
    return vars_, res


def satisfies(phi, assign):
    return all(any(assign[abs(l)] == (l > 0) for l in C) for C in phi)


def satisfiable(phi):
    vars_ = sorted({abs(l) for C in phi for l in C})
    for bits in itertools.product((False, True), repeat=len(vars_)):
        if satisfies(phi, dict(zip(vars_, bits))):
            return True
    return False


def shortest_route(phi):
    """Shortest u-v path length in (V, delta(A_tau)) over all satisfying tau, computed from the formula alone:
    a route visits the levels 0..m; inside clause k it uses 2 edges (h-o-h for a true negative literal, beta-o-beta
    for a true positive literal); switching between h_k and beta_k costs the F-edge h_k beta_k; it starts at h_0 and
    ends at beta_m.  Returns None if phi is unsatisfiable."""
    vars_ = sorted({abs(l) for C in phi for l in C})
    best = None
    for bits in itertools.product((False, True), repeat=len(vars_)):
        tau = dict(zip(vars_, bits))
        if not satisfies(phi, tau):
            continue
        # dynamic programming over levels; state = side at level k ('h' or 'b')
        INF = 10 ** 9
        cost = {"h": 0, "b": 1}
        for C in phi:
            types = {("b" if l > 0 else "h") for l in C if tau[abs(l)] == (l > 0)}
            new = {}
            for s in ("h", "b"):
                best_s = INF
                for t in types:
                    # reach level k-1 on side t, cross clause on side t, arrive on side t, switch to s if needed
                    val = min(cost["h"] + (0 if t == "h" else 1), cost["b"] + (0 if t == "b" else 1)) + 2
                    val += 0 if s == t else 1
                    best_s = min(best_s, val)
                new[s] = best_s
            cost = new
        val = cost["b"]
        if best is None or val < best:
            best = val
    return best


def random_formula(rng, n, m, k=3):
    return [[rng.choice((1, -1)) * rng.randint(1, n) for _ in range(k)] for _ in range(m)]
