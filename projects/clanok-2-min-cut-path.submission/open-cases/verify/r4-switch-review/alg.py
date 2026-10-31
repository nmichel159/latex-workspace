"""Algorithm of Theorem 10 of r4-switch.md with parameters (kd sets N_O[Z], ks single sides per type, storage B).

decide(inst, 10, 20, 60) is the algorithm of Theorem 10; smaller parameters give the same algorithm restricted to
certificates of a smaller shape (sound for every parameter by Theorem 5(1)).
"""
from itertools import combinations
from core import search5, is_valid_walk


def families(inst, T, kd, ks):
    O = 1 - T
    Ns = sorted({inst.N_of(O, z) for z in range(inst.D)}, key=sorted)
    singles = [y for y in range(inst.D) if inst.typ[y] == O]
    res = set()
    for i in range(min(kd, len(Ns)) + 1):
        for combo in combinations(Ns, i):
            U = frozenset().union(*combo) if combo else frozenset()
            for j in range(min(ks, len(singles)) + 1):
                for sc in combinations(singles, j):
                    res.add(U | frozenset(sc))
    return res


def decide(inst, kd, ks, B, want_walk=False):
    if inst.s == inst.t:
        return (True, None) if want_walk else True
    FE = families(inst, 0, kd, ks)
    FF = families(inst, 1, kd, ks)
    seen = set()
    for KE in FE:
        for KF in FF:
            K = KE | KF
            if K in seen:
                continue
            seen.add(K)
            W = search5(inst, K, B)
            if W is not None:
                assert is_valid_walk(inst, W), "search returned an invalid walk"
                return (True, W) if want_walk else True
    return (False, None) if want_walk else False
