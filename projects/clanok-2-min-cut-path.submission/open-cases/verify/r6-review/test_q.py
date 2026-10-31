"""Checks of r5-classes.md: A1-A5, Lemma 2a.1, Lemma W, Lemma D, Theorem Q (every step), Lemma PP.

usage: python test_q.py MODE SEED COUNT [params]
  MODE rand  : rand_inst(m in 3..8, nodes 3..6, classes 1..5)
  MODE plant : planted paths (r in 4..10, mates 0..6, classes 2..6)
  MODE tiny  : all instances with 3 nodes (s, t, one more) and 2 switches, every class partition (exhaustive),
               then COUNT random instances with 3 switches over 3 nodes
Every assertion failure is printed with the instance (JSON) and counted.
"""
import itertools
import json
import math
import random
import sys

import numpy as np
from scipy.optimize import linprog

from clib import (CInst, brute, p2_ok, all_shortest, is_valid_path, is_valid_walk, omega, nbhd, sigma, picks_path,
                  connects, desc, a5_search, rand_inst, planted_inst, bits)

STATS = {}
FAIL = []


def bump(k, v=1):
    STATS[k] = STATS.get(k, 0) + v


def fail(name, I, extra=None):
    bump("FAIL " + name)
    if len(FAIL) < 20:
        FAIL.append({"check": name, "inst": I.to_json(), "extra": extra})


def game_value(M):
    """value of the zero-sum game, row player maximises, payoff matrix M (rows x cols)"""
    nr, ncol = M.shape
    # variables p_1..p_nr, lam ; maximise lam
    c = np.zeros(nr + 1)
    c[-1] = -1.0
    A_ub = np.hstack([-M.T, np.ones((ncol, 1))])   # lam - sum_v p_v M[v][w] <= 0
    b_ub = np.zeros(ncol)
    A_eq = np.hstack([np.ones((1, nr)), np.zeros((1, 1))])
    b_eq = np.array([1.0])
    bounds = [(0, None)] * nr + [(None, None)]
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method="highs")
    return -res.fun


def min_cover(rows, cols, hit, limit):
    """least j <= limit such that some j rows hit every column (hit(r, c) bool); returns (j, rows) or (None, None)"""
    if not cols:
        return 0, ()
    for j in range(1, limit + 1):
        for comb in itertools.combinations(rows, j):
            if all(any(hit(r, c) for r in comb) for c in cols):
                return j, comb
    return None, None


def check_path(I, P, k):
    """all checks for one shortest valid path P"""
    r = len(P)
    pos_of_w = {i >> 1: a for a, i in enumerate(P)}
    ptype = {}
    for i in P:
        ptype[I.side_cls(i)] = i & 1
    onP = set(P)
    # (A1)
    for a, b in itertools.combinations(range(r), 2):
        if b - a >= 2 and I.mask(P[a]) & I.mask(P[b]):
            fail("A1", I, [P, a, b])
    # Lemma W (and A4 window): P-consistent sides not on P
    for Y in I.sides:
        if Y in onP:
            continue
        c = I.side_cls(Y)
        if c in ptype and ptype[c] != (Y & 1):
            continue
        hits = [a for a in range(r) if I.mask(Y) & I.mask(P[a])]
        bump("W sides")
        if hits and max(hits) - min(hits) > 2:
            fail("LemmaW", I, [P, Y, hits])
    # (A3): O-sides of classes used with T
    for c, T in ptype.items():
        O = 1 - T
        poss = [a for a in range(r) if I.side_cls(P[a]) == c]
        lo, hi = min(poss), max(poss)
        for Z in omega(I, c, O):
            hits = [a for a in range(r) if I.mask(Z) & I.mask(P[a])]
            left = [d for d in hits if d < lo]
            right = [d for d in hits if d > hi]
            if left and right:
                bump("A3 both sides")
                if len(poss) >= 2 or min(right) - max(left) > 2:
                    fail("A3", I, [P, Z, hits, poss])
    # (A4) domination part: Z of type T of class used with T, not on P, b a T-member of another class
    for c, T in ptype.items():
        for Z in omega(I, c, T):
            if Z in onP:
                continue
            Zp = I.mask(Z ^ 1)
            for b in range(r):
                Xb = P[b]
                if (Xb & 1) != T or I.side_cls(Xb) == c:
                    continue
                if not (I.mask(Z) & I.mask(Xb)):
                    bump("A4 dom")
                    if not (Zp & I.mask(Xb ^ 1)):
                        fail("A4dom", I, [P, Z, b])
    # (A2)
    for a, b in itertools.combinations(range(r), 2):
        if b - a < 2 or I.side_cls(P[a]) == I.side_cls(P[b]):
            continue
        Xa, Xb = P[a], P[b]
        if (Xa & 1) == (Xb & 1):
            if not (I.mask(Xa ^ 1) & I.mask(Xb ^ 1)):
                fail("A2same", I, [P, a, b])
        else:
            if not (I.mask(Xa ^ 1) & I.mask(Xb)) and not (I.mask(Xa) & I.mask(Xb ^ 1)):
                fail("A2opp", I, [P, a, b])
    res = {}
    for T in (0, 1):
        O = 1 - T
        cT = [c for c, ty in ptype.items() if ty == T]
        cO = [c for c, ty in ptype.items() if ty == O]
        # Lemma 2a.1 with random U
        allO = [i for i in I.sides if (i & 1) == O]
        for _ in range(3):
            U = frozenset(x for x in allO if random.random() < 0.5)
            Phi = [c for c in cT if not omega(I, c, O) <= U] + [c for c in cO if omega(I, c, O) <= U]
            mo = sigma(I, O, U, Phi)
            if not picks_path(I, mo, P):
                fail("Lemma2a.1", I, [P, T, sorted(U)])
        # Theorem Q
        Wst = [w for c in cT for w in I.members[c] if I.mask(2 * w + O)]
        V = [w for c in cO for w in I.members[c]]
        Vst = [v for v in V if I.mask(2 * v + T)]
        # Lemma D for all pairs
        for w in [w for c in cT for w in I.members[c]]:
            for v in V:
                if not (I.mask(2 * w + O) & I.mask(2 * v + O)) and not (I.mask(2 * w + T) & I.mask(2 * v + T)):
                    fail("LemmaD", I, [P, T, w, v])
        if not Wst:
            mo = sigma(I, O, frozenset())
            bump("Q W* empty")
            if not picks_path(I, mo, P):
                fail("Q-Wempty", I, [P, T])
            res[T] = 0
            continue
        if not Vst:
            mo = sigma(I, T, frozenset())
            bump("Q V* empty")
            if not picks_path(I, mo, P):
                fail("Q-Vempty", I, [P, T])
            res[T] = 0
            continue
        M = np.array([[1.0 if I.mask(2 * v + O) & I.mask(2 * w + O) else 0.0 for w in Wst] for v in V])
        lam = game_value(M)
        rho, rows = min_cover(V, Wst, lambda v, w: bool(I.mask(2 * v + O) & I.mask(2 * w + O)), k)
        kap, cols = min_cover(Wst, Vst, lambda w, v: bool(I.mask(2 * w + T) & I.mask(2 * v + T)), k)
        bump("Q game")
        if lam >= 0.5 - 1e-9:
            bump("Q lam>=1/2")
            if rho is None:
                fail("Q-rowcover", I, [P, T, lam])
        else:
            bump("Q lam<1/2")
            if kap is None:
                fail("Q-colcover", I, [P, T, lam])
        best = None
        for kind, j, cen in (("row", rho, rows), ("col", kap, cols)):
            if j is None:
                continue
            if kind == "row":
                tau = O
                Ys = [I.mask(2 * v + O) for v in cen]
                good, other = cT, cO
            else:
                tau = T
                Ys = [I.mask(2 * w + T) for w in cen]
                good, other = cO, cT
            U = frozenset().union(*[nbhd(I, tau, y) for y in Ys]) if Ys else frozenset()
            mo = sigma(I, tau, U)
            for c in good:
                if mo[c] != ptype[c]:
                    fail("Q-goodclass", I, [P, T, kind])
            nmem = sum(1 for i in P if i in U)
            if nmem > 3 * j:
                fail("Q-members", I, [P, T, kind, nmem, j])
            for y in Ys:
                cnt = sum(1 for i in P if (i & 1) == tau and I.mask(i) & y)
                if cnt > 3:
                    fail("Q-3members", I, [P, T, kind])
            Phi = [c for c in other if mo[c] != ptype[c]]
            bump("Q misclassified total", len(Phi))
            if len(Phi) > 3 * j:
                fail("Q-mis", I, [P, T, kind, len(Phi), j])
            mo2 = dict(mo)
            for c in Phi:
                mo2[c] = 1 - mo2[c]
            if not picks_path(I, mo2, P) or not connects(I, mo2):
                fail("Q-picks", I, [P, T, kind])
            if best is None or j < best:
                best = j
        res[T] = best
        # Lemma PP
        Tm = [a for a in range(r) if (P[a] & 1) == T]
        for u, b in itertools.combinations(Tm, 2):
            if abs(u - b) < 3 or I.side_cls(P[u]) == I.side_cls(P[b]):
                continue
            bump("PP pairs")
            Xu, Xb = P[u] ^ 1, P[b] ^ 1
            U = set(nbhd(I, O, I.mask(Xu))) | set(nbhd(I, O, I.mask(Xb)))
            U |= omega(I, I.side_cls(P[u]), O) | omega(I, I.side_cls(P[b]), O)
            for a in (u - 1, u + 1, b - 1, b + 1):
                if 0 <= a < r and (P[a] & 1) == T and I.mask(P[a] ^ 1):
                    U.add(P[a] ^ 1)
            U = frozenset(U)
            for c in cT:
                if not omega(I, c, O) <= U:
                    fail("PP-cover", I, [P, T, u, b, c])
            err = [c for c in cO if all(I.mask(Z) & (I.mask(Xu) | I.mask(Xb)) for Z in omega(I, c, O))]
            mo = sigma(I, O, U)
            mis = [c for c in ptype if mo[c] != ptype[c]]
            if sorted(mis) != sorted(err):
                fail("PP-err", I, [P, T, u, b, mis, err])
    return res


def check_inst(I, full_desc=True, max_paths=200):
    if not p2_ok(I):
        bump("skip noP2")
        return
    bump("instances")
    sols = brute(I)
    yes = bool(sols)
    bump("yes" if yes else "no")
    m = I.m
    k = int(math.floor(math.log2(m))) + 1 if m >= 1 else 1
    # A5 search soundness with random K
    for _ in range(4):
        K = [i for i in I.sides if random.random() < 0.6]
        Bb = random.randrange(0, 5)
        w = a5_search(I, K, Bb, want_walk=True)
        if w:
            bump("A5 accepts")
            if not yes or not is_valid_walk(I, w):
                fail("A5-sound", I, [K, Bb, w])
    # A5 completeness remark: with K = all sides and B = all pairs it is exact
    w = a5_search(I, list(I.sides), 2 * I.nc, want_walk=True)
    if bool(w) != yes:
        fail("A5-exact", I, None)
    if not yes:
        # DESC soundness (it only accepts connecting vectors; checked through connects)
        if desc(I, 1, 1, 1):
            fail("DESC-sound", I, None)
        return
    paths = all_shortest(I, cap=max_paths)
    if not paths:
        fail("no shortest path on yes", I, None)
        return
    for P in paths:
        if not is_valid_path(I, P):
            fail("path invalid", I, P)
    bump("paths", len(paths))
    bestj = None
    for P in paths:
        res = check_path(I, P, k)
        for T, j in res.items():
            if j is not None and (bestj is None or j < bestj):
                bestj = j
    if bestj is None:
        fail("Q no certificate", I, None)
        return
    bump("Q best j=%d" % bestj)
    if full_desc:
        ok = desc(I, bestj, 0, 3 * bestj)
        if not ok:
            fail("DESC(j,0,3j)", I, bestj)
        # Theorem Q parameters
        if bestj > k:
            fail("Q j>k", I, [bestj, k])


def main():
    mode = sys.argv[1]
    seed = int(sys.argv[2])
    count = int(sys.argv[3])
    random.seed(seed)
    rng = random.Random(seed)
    if mode == "rand":
        for _ in range(count):
            m = rng.randint(3, 8)
            I = rand_inst(rng, m, rng.randint(3, 6), rng.randint(1, 5), dens=rng.choice([0.2, 0.3, 0.4]))
            check_inst(I, full_desc=(m <= 7))
    elif mode == "plant":
        for _ in range(count):
            r = rng.randint(4, 10)
            I = planted_inst(rng, r, rng.randint(0, 6), rng.randint(2, 6), extra=rng.randint(0, 4),
                             dens=rng.choice([0.1, 0.2]))
            check_inst(I, full_desc=(I.m <= 9 and I.nc <= 7))
    elif mode == "plant2":
        from gen_c import planted_shortest
        rmin = int(sys.argv[4]) if len(sys.argv) > 4 else 5
        rmax = int(sys.argv[5]) if len(sys.argv) > 5 else 10
        made = 0
        while made < count:
            r = rng.randint(rmin, rmax)
            g = planted_shortest(rng, r, rng.randint(0, 5), rng.randint(2, 5), rng.randint(0, 3 * r))
            if g is None:
                bump("gen fail")
                continue
            made += 1
            I, P = g
            check_inst(I, full_desc=(I.m <= 10 and I.nc <= 6), max_paths=60)
    elif mode == "tiny":
        # exhaustive: 2 switches over 3 nodes, s = 0, t = 1, both class partitions
        for masks in itertools.product(range(8), repeat=4):
            for cls in ([0, 0], [0, 1]):
                I = CInst(3, [masks[0], masks[2]], [masks[1], masks[3]], cls, 0, 1)
                check_inst(I)
        # exhaustive: 3 switches over 3 nodes for the 5 partitions, sampled
        parts = [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], [0, 1, 2]]
        for _ in range(count):
            masks = [rng.randrange(8) for _ in range(6)]
            I = CInst(3, masks[0::2], masks[1::2], rng.choice(parts), 0, 1)
            check_inst(I)
    out = {"mode": mode, "seed": seed, "count": count, "stats": STATS, "fails": FAIL}
    print(json.dumps(STATS, indent=1, sort_keys=True))
    if FAIL:
        print("FAILURES:")
        for f in FAIL[:5]:
            print(json.dumps(f))
    with open("runs/q-%s-%d.json" % (mode, seed), "w") as fh:
        json.dump(out, fh, indent=1)


if __name__ == "__main__":
    main()
