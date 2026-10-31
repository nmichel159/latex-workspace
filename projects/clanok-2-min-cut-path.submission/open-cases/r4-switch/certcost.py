"""Least storage of side-set certificates for a given valid path (bitmask implementation of cert.min_cert).
cost(inst, P, kmax): for k = 1..kmax, least |P ∩ K| over unions K of k basic sets (N[Z], S(x)) containing all
partners of P; None if no union of k basic sets contains them."""
import itertools
import sw
import cert


def cost(inst, P, kmax=3, kinds=("N", "S")):
    Q = cert.partners_of(inst, P)
    Pset = set(P)
    S = sorted(set(sw.side_ids(inst)))
    idx = {x: i for i, x in enumerate(S)}

    def tomask(fs):
        r = 0
        for x in fs:
            r |= 1 << idx[x]
        return r
    Qm, Pm = tomask(Q), tomask(Pset)
    if not Qm:
        return {k: (0, []) for k in range(1, kmax + 1)}
    bm = {}
    for lab, fs in cert.basic_sets(inst, kinds):
        mk = tomask(fs)
        if mk & Qm:
            # keep the cheapest set for each trace on Q (dominance pruning)
            key = mk & Qm
            c = bin(mk & Pm).count("1")
            if key not in bm or c < bm[key][0]:
                bm[key] = (c, lab, mk)
    items = list(bm.values())
    # remove dominated: trace subset of another trace with cost >=
    keep = []
    for a in items:
        dom = False
        for b in items:
            if b is a:
                continue
            if (a[2] & Qm) | (b[2] & Qm) == (b[2] & Qm) and b[0] <= a[0] and ((a[2] & Qm) != (b[2] & Qm) or id(b) < id(a)):
                dom = True
                break
        if not dom:
            keep.append(a)
    out = {}
    for k in range(1, kmax + 1):
        best = None
        for combo in itertools.combinations(keep, k):
            U = 0
            for c in combo:
                U |= c[2]
            if Qm & ~U:
                continue
            cst = bin(U & Pm).count("1")
            if best is None or cst < best[0]:
                best = (cst, [c[1] for c in combo])
        out[k] = best
    return out
