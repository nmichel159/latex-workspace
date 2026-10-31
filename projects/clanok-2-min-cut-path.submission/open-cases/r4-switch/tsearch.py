"""Typed side-set certificate search (agent r4-switch).

A certificate is a pair (K_E, K_F): K_E a set of F-sides, K_F a set of E-sides.  K = K_E ∪ K_F.
A walk is admissible (bound B) if
  (i)   every member's partner is empty or lies in K,
  (ii)  no member's partner is a stored member, where the stored members are the members lying in K,
  (iii) at most B distinct stored members.
Soundness: if X and X' are both members, then X' ∈ K and X ∈ K by (i), both are stored, and (ii) fails at the later
one.  So admissible walks are valid.  (This is Theorem H of dc-hardness.md with arbitrary side sets in place of
node stars.)

Basic sets of one type T (T = 'F' for K_E, 'E' for K_F):
  N_T[Z]  = sides of type T meeting Z (Z itself included if of type T), Z any side;
  S_T(x)  = sides of type T containing node x;
  {Z}     = a single side of type T.
K_T is a union of at most k basic sets of type T.
"""
import itertools
from collections import deque

import sw


def typed_basic(inst, T):
    adj = sw.side_graph(inst)
    S = list(adj)
    want = 0 if T == "E" else 1
    out = {}
    for z in S:
        fs = frozenset(i for i in (adj[z] | {z}) if (i & 1) == want)
        if fs:
            out.setdefault(fs, ("N", z))
    N = inst[0]
    for x in range(N):
        fs = frozenset(i for i in S if (i & 1) == want and (sw.side_mask(inst, i) >> x) & 1)
        if fs:
            out.setdefault(fs, ("S", x))
    for z in S:
        if (z & 1) == want:
            out.setdefault(frozenset([z]), ("1", z))
    return [(lab, fs) for fs, lab in out.items()]


def admissible_search(inst, K, B, want_witness=False):
    N, E, F, s, t = inst
    adj = sw.side_graph(inst)
    allsides = set(adj)
    m = {i: sw.side_mask(inst, i) for i in allsides}

    def adm(i):
        p = i ^ 1
        return (p not in allsides) or (p in K)
    q = deque()
    seen = set()
    for i in allsides:
        if (m[i] >> s) & 1 and adm(i):
            st = (i, frozenset([i]) if i in K else frozenset())
            if len(st[1]) <= B and st not in seen:
                seen.add(st)
                q.append((st, (i,)))
    while q:
        (cur, stored), walk = q.popleft()
        if (m[cur] >> t) & 1:
            return (True, walk) if want_witness else True
        for j in adj[cur]:
            if not adm(j):
                continue
            if (j ^ 1) in stored:
                continue
            ns = stored
            if j in K and j not in stored:
                ns = stored | {j}
                if len(ns) > B:
                    continue
            st = (j, ns)
            if st not in seen:
                seen.add(st)
                q.append((st, walk + (j,)))
    return (False, None) if want_witness else False


def unions(basic, k):
    out = [frozenset()]
    for kk in range(1, k + 1):
        for combo in itertools.combinations(basic, kk):
            out.append(frozenset().union(*(fs for lab, fs in combo)))
    return list(dict.fromkeys(out))


def t_search(inst, kE, kF, B, want_witness=False):
    """Try all K_E (union of <= kE F-type basic sets) and K_F (<= kF E-type basic sets)."""
    bF = typed_basic(inst, "F")
    bE = typed_basic(inst, "E")
    UE = unions(bF, kE)
    UF = unions(bE, kF)
    for KE in UE:
        for KF in UF:
            r = admissible_search(inst, KE | KF, B, want_witness)
            ok = r[0] if want_witness else r
            if ok:
                if want_witness:
                    assert sw.is_valid_walk(inst, r[1]), "UNSOUND"
                    return True, (KE, KF, r[1])
                return True
    return (False, None) if want_witness else False


def path_cost(inst, P, kE, kF):
    """Least storage |P ∩ (K_E ∪ K_F)| over typed certificates of the given sizes covering partners(P);
    returns (cost, labels) or None."""
    allsides = set(sw.side_ids(inst))
    Q = set(i ^ 1 for i in P if (i ^ 1) in allsides)
    QE = frozenset(x for x in Q if x & 1)        # partners of E-members: F-sides
    QF = frozenset(x for x in Q if not x & 1)    # partners of F-members: E-sides
    Pset = set(P)

    def best(basic, Qt, k):
        if not Qt:
            return (0, ())
        cand = [(lab, fs) for lab, fs in basic if fs & Qt]
        res = None
        for kk in range(1, k + 1):
            for combo in itertools.combinations(cand, kk):
                U = frozenset().union(*(fs for lab, fs in combo))
                if not Qt <= U:
                    continue
                c = len(U & Pset)
                if res is None or c < res[0]:
                    res = (c, tuple(lab for lab, fs in combo))
        return res
    bE = best(typed_basic(inst, "F"), QE, kE)
    bF = best(typed_basic(inst, "E"), QF, kF)
    if bE is None or bF is None:
        return None
    return (bE[0] + bF[0], bE[1], bF[1])
