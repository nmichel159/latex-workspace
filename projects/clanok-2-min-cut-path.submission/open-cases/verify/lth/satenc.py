"""Theorem L(b) of dc-hardness.md rebuilt from the text (agent verify-LTH): the 3-SAT variant and the encoding
into two-choice interval cover (no P2)."""
import itertools
import random


def sat_brute(nvars, clauses):
    for code in range(1 << nvars):
        val = [(code >> i) & 1 for i in range(nvars)]
        if all(any((lit > 0) == bool(val[abs(lit) - 1]) for lit in c) for c in clauses):
            return True
    return False


def to_variant(nvars, clauses):
    """Replace a variable with q >= 2 occurrences by copies x^1..x^q, one per occurrence, and add the clauses
    (not x^a or x^{a+1}), indices mod q. Variables with one occurrence are kept. Returns (nvars', clauses')."""
    occ = {}
    for j, c in enumerate(clauses):
        for p, lit in enumerate(c):
            occ.setdefault(abs(lit), []).append((j, p))
    newc = [list(c) for c in clauses]
    extra = []
    nv = 0
    for x in range(1, nvars + 1):
        lst = occ.get(x, [])
        if not lst:
            continue
        if len(lst) == 1:
            nv += 1
            j, p = lst[0]
            newc[j][p] = nv if clauses[j][p] > 0 else -nv
            continue
        ids = []
        for (j, p) in lst:
            nv += 1
            ids.append(nv)
            newc[j][p] = nv if clauses[j][p] > 0 else -nv
        q = len(ids)
        for a in range(q):
            extra.append([-ids[a], ids[(a + 1) % q]])
    return nv, [list(c) for c in newc] + extra


def variant_ok(nvars, clauses):
    """Every variable occurs at most twice positively and at most once negatively, or vice versa."""
    pos = [0] * (nvars + 1)
    neg = [0] * (nvars + 1)
    for c in clauses:
        for lit in c:
            if lit > 0:
                pos[lit] += 1
            else:
                neg[-lit] += 1
    return all((pos[x] <= 2 and neg[x] <= 1) or (pos[x] <= 1 and neg[x] <= 2) for x in range(1, nvars + 1))


def encode_tic(nvars, clauses):
    """Line of edges: one clause edge per clause, then for each variable the conflict edges d_ac (and d_bc) next to
    each other, where c is the single occurrence of one sign and a (b) the occurrences of the other sign.
    Switch = literal occurrence; F-span = its clause edge; E-span = its conflict edges (None if it has none).
    Returns (K, sw, occurrence list)."""
    occs = []                      # (clause j, literal)
    for j, c in enumerate(clauses):
        for lit in c:
            occs.append((j, lit))
    edges = []                     # names of the edges in line order
    for j in range(len(clauses)):
        edges.append(("C", j))
    conflict = {}                  # occurrence index -> list of edge indices
    for x in range(1, nvars + 1):
        P = [i for i, (j, lit) in enumerate(occs) if lit == x]
        Nn = [i for i, (j, lit) in enumerate(occs) if lit == -x]
        if not P or not Nn:
            continue
        if len(P) == 1:
            single, others = P[0], Nn
        else:
            single, others = Nn[0], P
        assert len(others) <= 2 and (len(P) == 1 or len(Nn) == 1)
        for o in others:
            e = len(edges)
            edges.append(("D", o, single))
            conflict.setdefault(o, []).append(e)
            conflict.setdefault(single, []).append(e)
    K = len(edges)
    sw = []
    for i, (j, lit) in enumerate(occs):
        F = (j, j + 1)             # edge index e covers junctions e, e+1
        es = conflict.get(i)
        if es:
            lo, hi = min(es), max(es)
            assert hi - lo + 1 == len(es)
            E = (lo, hi + 1)
        else:
            E = None
        sw.append((E, F))
    return K, sw, occs


def rand_cnf(rng, nvars, nclauses, kmax=3):
    cl = []
    for _ in range(nclauses):
        k = rng.randint(1, kmax)
        vs = rng.sample(range(1, nvars + 1), min(k, nvars))
        cl.append([v if rng.random() < 0.5 else -v for v in vs])
    return cl
