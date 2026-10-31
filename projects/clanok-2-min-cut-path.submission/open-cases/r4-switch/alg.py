"""The certificate algorithm of r4-switch.md (Theorem 10, with the declaration variant of Theorem 11).

decide(inst, kd, ks, s, B):
  for every K_E = union of <= kd sets N_F[Z] and <= ks single F-sides, and K_F likewise with E,
  run search_v(inst, K_E | K_F, B, s); answer True (with a valid walk) iff some search accepts.
search_v: breadth-first search over states (current side, St = members in K so far, Dc = declared sides):
  a side Y may be appended iff Y not in Dc, partner(Y) not in St, and
     partner(Y) empty, or partner(Y) in K, or partner(Y) in Dc (Y used before), or
     (Y not in K and |Dc| < s: declare partner(Y), i.e. forbid it from now on);
  Y in K is added to St (|St| <= B).
Sound for every K, B, s (Theorem 11); complete for kd = 10, ks = 20, s = 0, B = 60 (Theorem 10).
"""
import itertools
from collections import deque

import sw


def dom_sets(inst, O):
    """All distinct sets N_O[Z] (Z any side): sides of type O meeting Z or equal to Z."""
    S = sw.side_ids(inst)
    m = {i: sw.side_mask(inst, i) for i in S}
    out = {}
    for z in S:
        fs = frozenset(i for i in S if (i & 1) == O and (m[i] & m[z]))
        if fs:
            out.setdefault(fs, z)
    return list(out.keys())


def search_v(inst, K, B, s, want_walk=False, adj=None):
    N, E, F, s_, t = inst
    if adj is None:
        adj = sw.side_graph(inst)
    allsides = adj.keys()
    m = {i: sw.side_mask(inst, i) for i in allsides}

    def step(Y, St, Dc):
        if Y in Dc:
            return None
        p = Y ^ 1
        if p in St:
            return None
        if p in allsides and p not in K and p not in Dc:
            if Y in K or len(Dc) >= s:
                return None
            Dc = Dc | {p}
        if Y in K and Y not in St:
            if len(St) >= B:
                return None
            St = St | {Y}
        return St, Dc

    q = deque()
    seen = set()
    for i in allsides:
        if (m[i] >> s_) & 1:
            r = step(i, frozenset(), frozenset())
            if r is None:
                continue
            st = (i,) + r
            if st not in seen:
                seen.add(st)
                q.append((st, (i,)))
    while q:
        (cur, St, Dc), walk = q.popleft()
        if (m[cur] >> t) & 1:
            return (True, walk) if want_walk else True
        for j in adj[cur]:
            r = step(j, St, Dc)
            if r is None:
                continue
            st = (j,) + r
            if st not in seen:
                seen.add(st)
                q.append((st, walk + (j,) if want_walk else None))
    return (False, None) if want_walk else False


def k_unions(sets, k, singles, ks):
    out = []
    for kk in range(0, k + 1):
        for combo in itertools.combinations(sets, kk):
            base = frozenset().union(*combo) if combo else frozenset()
            for j in range(0, ks + 1):
                for sc in itertools.combinations(singles, j):
                    out.append(base | frozenset(sc))
    return list(dict.fromkeys(out))


def decide(inst, kd=1, ks=0, s=4, B=8, want_walk=False):
    N, E, F, s_, t = inst
    if s_ == t:
        return (True, ()) if want_walk else True
    adj = sw.side_graph(inst)
    S = list(adj)
    if not S:
        return (False, None) if want_walk else False
    UE = k_unions(dom_sets(inst, 1), kd, [i for i in S if i & 1], ks)
    UF = k_unions(dom_sets(inst, 0), kd, [i for i in S if not i & 1], ks)
    for KE in UE:
        for KF in UF:
            r = search_v(inst, KE | KF, B, s, True, adj)
            if r[0]:
                assert sw.is_valid_walk(inst, r[1]), "UNSOUND walk %s" % (r[1],)
                return (True, (KE, KF, r[1])) if want_walk else True
    return (False, None) if want_walk else False


def decide_full(inst, want_walk=False):
    """The algorithm of Theorem 10 with the parameters of the proof (10 dominator sets and 20 single sides per type,
    storage 60, no declarations).  Polynomial, but the exponent makes it usable only on very small instances; the
    tests use decide() with small parameters and the certificate-guided check of test_guided.py."""
    return decide(inst, kd=10, ks=20, s=0, B=60, want_walk=want_walk)
