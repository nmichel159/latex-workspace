"""Side-set certificates (generalisation of Theorem H of dc-hardness.md), agent r4-switch.

Certificate: a set K of sides.  A walk Y_1..Y_m (sides, consecutive equal or meeting, s in Y_1, t in Y_m) is
K-admissible with bound B if
  (i)   every member's partner is empty or lies in K,
  (ii)  no two members lying in K are partners,
  (iii) at most B distinct members lie in K.
Soundness (proved in r4-switch.md): a K-admissible walk has no two partner sides, hence is a valid walk.
Search: BFS over (current side, set of members in K so far).

Basic sets: N[Z] = Z and the sides meeting Z (Z a side); S(x) = sides containing node x.
K ranges over unions of at most k basic sets.
"""
import itertools
from collections import deque

import sw


def basic_sets(inst, kinds=("N", "S")):
    adj = sw.side_graph(inst)
    S = list(adj)
    out = []
    seen = set()
    if "N" in kinds:
        for z in S:
            fs = frozenset(adj[z] | {z})
            if fs not in seen:
                seen.add(fs)
                out.append((("N", z), fs))
    if "S" in kinds:
        N = inst[0]
        for x in range(N):
            fs = frozenset(i for i in S if (sw.side_mask(inst, i) >> x) & 1)
            if fs and fs not in seen:
                seen.add(fs)
                out.append((("S", x), fs))
    return out


def partners_of(inst, path):
    allsides = set(sw.side_ids(inst))
    return set(i ^ 1 for i in path if (i ^ 1) in allsides)


def min_cert(inst, path, kmax=3, kinds=("N", "S")):
    """For k = 1..kmax: least |P ∩ K| over unions K of k basic sets with partners(P) ⊆ K (None if impossible).
    Also returns the best K labels."""
    Q = partners_of(inst, path)
    P = set(path)
    bs = basic_sets(inst, kinds)
    # keep only sets that meet Q
    bs = [(lab, fs) for lab, fs in bs if fs & Q]
    res = {}
    if not Q:
        return {k: (0, ()) for k in range(1, kmax + 1)}
    for k in range(1, kmax + 1):
        best = None
        for combo in itertools.combinations(range(len(bs)), k):
            U = frozenset().union(*(bs[c][1] for c in combo))
            if not Q <= U:
                continue
            cost = len(P & U)
            if best is None or cost < best[0]:
                best = (cost, tuple(bs[c][0] for c in combo))
        res[k] = best
    return res


def k_search(inst, k, B, kinds=("N", "S"), want_witness=False, Klist=None):
    """Sound search over unions of at most k basic sets (or the explicit list Klist of side sets)."""
    N, E, F, s, t = inst
    adj = sw.side_graph(inst)
    S = list(adj)
    allsides = set(S)
    m = {i: sw.side_mask(inst, i) for i in S}
    starts = [i for i in S if (m[i] >> s) & 1]
    if Klist is None:
        bs = [fs for lab, fs in basic_sets(inst, kinds)]
        Klist = [frozenset()]
        for kk in range(1, k + 1):
            for combo in itertools.combinations(range(len(bs)), kk):
                Klist.append(frozenset().union(*(bs[c] for c in combo)))
        Klist = list(dict.fromkeys(Klist))
    for K in Klist:
        def adm(i):
            p = i ^ 1
            return (p not in allsides) or (p in K)
        q = deque()
        seen = set()
        for i in starts:
            if not adm(i):
                continue
            st = (i, frozenset([i]) if i in K else frozenset())
            if len(st[1]) > B:
                continue
            if st not in seen:
                seen.add(st)
                q.append((st, (i,)))
        while q:
            (cur, stored), walk = q.popleft()
            if (m[cur] >> t) & 1:
                if want_witness:
                    return True, (K, walk)
                return True
            for j in adj[cur]:
                if not adm(j):
                    continue
                ns = stored
                if j in K and j not in stored:
                    if (j ^ 1) in stored:
                        continue
                    ns = stored | {j}
                    if len(ns) > B:
                        continue
                st = (j, ns)
                if st not in seen:
                    seen.add(st)
                    q.append((st, walk + (j,)))
    return (False, None) if want_witness else False
