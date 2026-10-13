"""The construction of theory-hardness.md, Section 2.1, re-implemented from the text alone.

A formula is a list of clauses; a clause is a non-empty list of non-zero integers (DIMACS literals:
i means x_i, -i means not x_i). Repeated literals and a variable twice in a clause are allowed.

Text of Section 2.1, as implemented:
  c0 = (m + 1) + 2L, M = c0 + 2 (L = number of literal occurrences).
  K_A: clique on M vertices containing u = h_0, ..., h_m and a_1, a_2 (the rest fillers).
  K_B: clique on M vertices containing beta_0, ..., beta_m (beta_m = v) and b_1, b_2 (the rest fillers).
  F = {h_k beta_k : k = 0..m}.
  occurrence vertex o_{k,j} for the j-th literal of C_k:
     positive literal: o ~ beta_{k-1}, beta_k, a_1, a_2;   negative literal: o ~ h_{k-1}, h_k, b_1, b_2.
  sync edges: the occurrence vertices of each variable joined into a path.
The text does not fix the order of the vertices on a sync path; `sync_order` is "natural" (order of occurrence),
"reverse" or "random" (seeded shuffle) so that the claims can be tested for several orders.
"""

import itertools
import random

from vlib import Gr


def build(clauses, sync_order="natural", seed=0):
    m = len(clauses)
    assert m >= 1 and all(len(C) >= 1 for C in clauses) and all(l != 0 for C in clauses for l in C)
    L = sum(len(C) for C in clauses)
    c0 = (m + 1) + 2 * L
    M = c0 + 2
    h = list(range(0, m + 1))
    a1, a2 = m + 1, m + 2
    KA = list(range(0, M))
    beta = [M + k for k in range(m + 1)]
    b1, b2 = M + m + 1, M + m + 2
    KB = list(range(M, 2 * M))
    u, v = h[0], beta[m]
    edges = []
    for K in (KA, KB):
        edges += list(itertools.combinations(K, 2))
    F = [(h[k], beta[k]) for k in range(m + 1)]
    edges += F
    occ = []          # (vertex, k, j, literal)
    O = {}            # variable -> list of occurrence vertices
    nxt = 2 * M
    for k in range(1, m + 1):
        for j, lit in enumerate(clauses[k - 1]):
            o = nxt
            nxt += 1
            occ.append((o, k, j, lit))
            if lit > 0:
                edges += [(o, beta[k - 1]), (o, beta[k]), (o, a1), (o, a2)]
            else:
                edges += [(o, h[k - 1]), (o, h[k]), (o, b1), (o, b2)]
            O.setdefault(abs(lit), []).append(o)
    rng = random.Random(seed)
    sync = []
    for var in sorted(O):
        seq = list(O[var])
        if sync_order == "reverse":
            seq.reverse()
        elif sync_order == "random":
            rng.shuffle(seq)
        sync += list(zip(seq, seq[1:]))
    edges += sync
    g = Gr(nxt, edges)          # raises on a duplicate edge or a loop
    return dict(g=g, n=nxt, u=u, v=v, m=m, L=L, c0=c0, M=M, h=h, beta=beta, a1=a1, a2=a2, b1=b1, b2=b2,
                KA=KA, KB=KB, F=F, occ=occ, O=O, sync=sync, clauses=clauses)


def variables(R):
    return sorted(R["O"])


def A_tau(R, tau):
    """tau: dict variable -> bool. A_tau = K_A plus the occurrence vertices of the true variables."""
    A = set(R["KA"])
    for var, os_ in R["O"].items():
        if tau[var]:
            A |= set(os_)
    return frozenset(A)


def assignments(R):
    vs = variables(R)
    for bits in itertools.product([False, True], repeat=len(vs)):
        yield dict(zip(vs, bits))


def satisfies(clauses, tau):
    return all(any((l > 0) == tau[abs(l)] for l in C) for C in clauses)


def is_sat(clauses):
    vs = sorted({abs(l) for C in clauses for l in C})
    for bits in itertools.product([False, True], repeat=len(vs)):
        tau = dict(zip(vs, bits))
        if satisfies(clauses, tau):
            return True
    return False


def claimed_edge_count(R):
    M, m, L = R["M"], R["m"], R["L"]
    return M * (M - 1) + (m + 1) + 4 * L + sum(len(os_) - 1 for os_ in R["O"].values())
