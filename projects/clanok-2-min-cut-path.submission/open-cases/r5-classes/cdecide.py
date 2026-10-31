"""Certificate shapes, the decision procedure with class conflict families, guided certificate costs.

A T-certificate of a valid path P is a set K_T of O-sides (O = 1 - T) containing Pi(X) for every T-member X of
P (all O-sides of every class used with type T); its storage is the number of classes of O-members of P lying in
K_T.  Shapes: unions of at most kd sets N_O[Z] (Z any side), at most kc class groups Omega(c, O) and at most ks
single O-sides.  decide(...) enumerates K_E, K_F of a shape and runs ccore.csearch with K = K_E | K_F; it is
sound for all parameters (ccore.csearch is sound for every K, B).

csearch_decl: the search with class declarations (sound; proof in r5-classes.md): Y of (C, T) may be appended iff
(C, O) is neither stored nor declared and either Pi(Y) <= K, or (C, T) is already declared, or Y is not in K and
fewer than s declarations were made (then (C, T) is declared); members in K store (C, T).
"""
import itertools
from collections import deque
import ccore as C


def dominator_sets(inst, O):
    """distinct sets N_O[Z] over all sides Z (as frozensets), with one representative Z each"""
    seen = {}
    for z in inst.sides:
        S = inst.N_of(O, z)
        if S and S not in seen:
            seen[S] = z
    return seen


def class_groups(inst, O):
    out = {}
    for c in inst.classes:
        S = inst.Omega[(c, O)]
        if S and S not in out:
            out[S] = c
    return out


def shapes(inst, O, kd, kc, ks, cap=None):
    """all distinct K_T sets of the given shape"""
    doms = list(dominator_sets(inst, O))
    grps = list(class_groups(inst, O))
    singles = [frozenset([i]) for i in inst.sides if (i & 1) == O]
    out = set()
    for a in range(kd + 1):
        for D in itertools.combinations(doms, a):
            base = frozenset().union(*D) if D else frozenset()
            for b in range(kc + 1):
                for G in itertools.combinations(grps, b):
                    base2 = base.union(*G) if G else base
                    for c in range(ks + 1):
                        for S in itertools.combinations(singles, c):
                            out.add(base2.union(*S) if S else base2)
                            if cap is not None and len(out) > cap:
                                return out
    return out


def decide(inst, kd, kc, ks, B, want_walk=False):
    if inst.s == inst.t:
        return True
    KE = shapes(inst, 1, kd, kc, ks)
    KF = shapes(inst, 0, kd, kc, ks)
    # a side y can be used only if Pi(y) <= K; quick filter: s-t connectivity through usable sides
    for ke in KE:
        for kf in KF:
            K = ke | kf
            W = C.csearch(inst, K, B, want_walk=True)
            if W is not None:
                assert C.is_valid_walk(inst, W)
                return W if want_walk else True
    return None if want_walk else False


def guided_cost(inst, P, kd, kc, ks):
    """min storage over T-certificates of P of the shape, per type; None if no certificate of the shape covers"""
    res = {}
    for T in (0, 1):
        O = 1 - T
        need = set()
        for x in P:
            if (x & 1) == T:
                need |= inst.Pi[x]
        need = frozenset(need)
        best = None
        if not need:
            res[T] = 0
            continue
        for K in shapes(inst, O, kd, kc, ks):
            if need <= K:
                st = len({(inst.scls[x], x & 1) for x in P if x in K})
                if best is None or st < best:
                    best = st
        res[T] = best
    return res


def csearch_decl(inst, K, B, s, want_walk=True):
    K = frozenset(K)
    okside = {i: inst.Pi[i] <= K for i in inst.sides}

    def step(y, St, Dc):
        c, ty = inst.scls[y], y & 1
        if (c, 1 - ty) in St or (c, 1 - ty) in Dc:
            return None
        nDc = Dc
        if not okside[y] and (c, ty) not in Dc:
            if y in K or len(Dc) >= s:
                return None
            nDc = Dc | {(c, ty)}
        nSt = St
        if y in K and (c, ty) not in St:
            nSt = St | {(c, ty)}
            if len(nSt) > B:
                return None
        return nSt, nDc

    par = {}
    q = deque()
    for y in inst.sides:
        if inst.has_s[y]:
            r = step(y, frozenset(), frozenset())
            if r is None:
                continue
            st = (y,) + r
            if st not in par:
                par[st] = None
                q.append(st)
    while q:
        st = q.popleft()
        y, St, Dc = st
        if inst.has_t[y]:
            if not want_walk:
                return True
            walk = []
            cur = st
            while cur is not None:
                walk.append(cur[0])
                cur = par[cur]
            return walk[::-1]
        for z in inst.adj[y]:
            r = step(z, St, Dc)
            if r is None:
                continue
            nst = (z,) + r
            if nst not in par:
                par[nst] = st
                q.append(nst)
    return None


def decide_decl(inst, kd, kc, ks, B, s):
    KE = shapes(inst, 1, kd, kc, ks)
    KF = shapes(inst, 0, kd, kc, ks)
    for ke in KE:
        for kf in KF:
            W = csearch_decl(inst, ke | kf, B, s)
            if W is not None:
                assert C.is_valid_walk(inst, W)
                return True
    return False


if __name__ == "__main__":
    import sys
    import cfam
    for k in range(2, 6):
        for contact in (0, 1, 2):
            I = cfam.ytie(k, contact)
            L, paths = C.shortest_valid_paths(I)
            P = paths[0]
            g = guided_cost(I, P, 2, 1, 1)
            print("k=%d contact=%d |P|=%d guided(2,1,1)=%s" % (k, contact, L, g), flush=True)
