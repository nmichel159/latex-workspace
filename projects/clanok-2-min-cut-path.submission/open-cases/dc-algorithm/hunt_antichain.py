"""Smallest switch-model (2CH + P2) instances in which every solution has at least K switches in each mode
(dc-algorithm.md Section 11.6).  In the ZZ form (dc-hardness/swlib.to_zz: middle elements pairwise incomparable,
bottoms ~ u, tops ~ v) the generator numbers of a solution down-set are its numbers of E-mode and F-mode switches, so
on such an instance every guess of fewer than K generators, on either side, fails; since the middle elements form an
antichain, no guess defined from the order with fewer than K parameters helps either.

Method: random alternating skeleton s - X_1 - X_2 - ... - X_n - t (consecutive picked sides share a private node),
random P2 completion (each violating pair gets a shared node of a random type: an existing node or a new one), then
greedy shrinking (remove a node from a side, merge two nodes, delete a node, delete a switch) as long as P2 holds and
the property holds.  Size = number of elements of the ZZ form.
Usage: python hunt_antichain.py SEED TRIES K
"""
import os
import sys
import json
import random

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "dc-hardness"))
from twoch import connected, p2_ok  # noqa: E402  (read-only import)
import swlib  # noqa: E402  (read-only import)


def mode_counts(inst):
    """(min number of E-mode switches, min number of F-mode switches) over connecting mode vectors, or None."""
    N, E, F, s, t = inst
    n = len(E)
    mE = mF = None
    for mask in range(1 << n):
        hyper = [F[i] if (mask >> i) & 1 else E[i] for i in range(n)]
        if connected(N, hyper, s, t):
            f = bin(mask).count("1")
            e = n - f
            mE = e if mE is None else min(mE, e)
            mF = f if mF is None else min(mF, f)
    if mE is None:
        return None
    return mE, mF


def zz_size(inst):
    z, _ = swlib.to_zz(inst)
    return z.n


def ok(inst, K):
    N, E, F, s, t = inst
    if not p2_ok(E, F):
        return False
    mc = mode_counts(inst)
    return mc is not None and min(mc) >= K


def skeleton(rng, n):
    # nodes: s = 0, t = 1, y_1..y_{n-1} = 2..n
    N = n + 1
    E = [0] * n
    F = [0] * n
    first = rng.randint(0, 1)          # type of X_1: 0 = E, 1 = F
    for k in range(n):
        typ = (first + k) % 2
        nodes = []
        nodes.append(0 if k == 0 else 1 + k)     # y_k = 1 + k for k >= 1
        nodes.append(1 if k == n - 1 else 2 + k)
        m = sum(1 << x for x in nodes)
        if typ == 0:
            E[k] |= m
        else:
            F[k] |= m
    return [N, E, F, 0, 1]


def p2_repair(rng, inst, p_new):
    N, E, F, s, t = inst
    E, F = E[:], F[:]
    n = len(E)
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    rng.shuffle(pairs)
    for i, j in pairs:
        if (E[i] & E[j]) or (F[i] & F[j]):
            continue
        S = E if rng.random() < 0.5 else F
        if rng.random() < p_new:
            x = N
            N += 1
        else:
            x = rng.randrange(N)
        S[i] |= 1 << x
        S[j] |= 1 << x
    return [N, E, F, s, t]


def compact(inst):
    """drop nodes in no side (other than s, t) and renumber."""
    N, E, F, s, t = inst
    used = 0
    for m in E + F:
        used |= m
    used |= (1 << s) | (1 << t)
    keep = [x for x in range(N) if (used >> x) & 1]
    ren = {x: i for i, x in enumerate(keep)}

    def rm(m):
        return sum(1 << ren[x] for x in keep if (m >> x) & 1)
    return [len(keep), [rm(m) for m in E], [rm(m) for m in F], ren[s], ren[t]]


def shrink(rng, inst, K):
    inst = compact(inst)
    best = zz_size(inst)
    improved = True
    while improved:
        improved = False
        N, E, F, s, t = inst
        n = len(E)
        moves = []
        for i in range(n):
            for typ in (0, 1):
                S = E if typ == 0 else F
                for x in range(N):
                    if (S[i] >> x) & 1:
                        moves.append(("rm", i, typ, x))
        for x in range(N):
            for y in range(x + 1, N):
                if {x, y} != {s, t}:
                    moves.append(("merge", x, y))
        for x in range(N):
            if x not in (s, t):
                moves.append(("del", x))
        for i in range(n):
            moves.append(("delsw", i))
        rng.shuffle(moves)
        for mv in moves:
            E2, F2 = E[:], F[:]
            s2, t2 = s, t
            if mv[0] == "rm":
                _, i, typ, x = mv
                if typ == 0:
                    E2[i] &= ~(1 << x)
                else:
                    F2[i] &= ~(1 << x)
            elif mv[0] == "merge":
                _, x, y = mv

                def mg(m):
                    return (m & ~(1 << y)) | (1 << x) if (m >> y) & 1 else m
                E2 = [mg(m) for m in E2]
                F2 = [mg(m) for m in F2]
                if y == s:
                    s2 = x
                if y == t:
                    t2 = x
            elif mv[0] == "del":
                _, x = mv
                E2 = [m & ~(1 << x) for m in E2]
                F2 = [m & ~(1 << x) for m in F2]
            else:
                _, i = mv
                E2 = E2[:i] + E2[i + 1:]
                F2 = F2[:i] + F2[i + 1:]
            cand = compact([N, E2, F2, s2, t2])
            if ok(cand, K):
                sz = zz_size(cand)
                if sz < best or (sz == best and sum(bin(m).count("1") for m in cand[1] + cand[2]) <
                                 sum(bin(m).count("1") for m in E + F)):
                    inst, best = cand, sz
                    improved = True
                    break
    return inst, best


def main():
    seed, tries, K = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    rng = random.Random(seed)
    best = None
    found = 0
    for it in range(tries):
        n = rng.randint(2 * K, 2 * K + 2)
        inst = skeleton(rng, n)
        inst = p2_repair(rng, inst, rng.choice([0.2, 0.5, 0.8]))
        if not ok(inst, K):
            continue
        found += 1
        inst, sz = shrink(rng, inst, K)
        if best is None or sz < best[0]:
            best = (sz, inst)
            z, names = swlib.to_zz(inst)
            print("NEW BEST", it, "zz size", sz, "switches", len(inst[1]), "nodes", inst[0], "R", len(z.R),
                  json.dumps(inst), flush=True)
    print("done", seed, "tries", tries, "with property", found, "best size", best[0] if best else None,
          json.dumps(best[1]) if best else "", flush=True)


if __name__ == "__main__":
    main()
