"""Pointwise checks of the lemmas of r4-switch.md on every shortest valid path of many instances, independent of
the case split of prove.py:
  Lemma 1 (one-sided contacts), Lemma 2 (q_b >= q_f - 1), Lemma 3 / Theorem 4 (domination);
  Lemma 7 on EVERY straddle of the path (any type, any r, p, nearest r_1 < r < r_2 and p_1 < p < p_2 with disjoint
  intervals): tightness, validity of P*, storage of the two certificates of P* <= 3;
  (3a) for every hole p of a forward critical row a != q_b - 1: a ∈ b(p); a not extreme in b(p) => straddle;
  (3b) for every triple of forward critical rows with pairwise disjoint spans, monotone positions and |f| >= 3 for
  the middle one: the middle-span row is between the others and a straddle exists.
Usage: python lemma_test.py SEED COUNT MODE   (MODE: saturated | random | planted | repair)"""
import sys
import random
import itertools
import time

import sw
import prove
import saturate
from test_prove import gen_instance

seed, count, mode = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
rng = random.Random(seed)
cnt = dict(paths=0, straddles=0, holes=0, triples=0, caseii=0, fail=0)


def fail(msg, inst, P):
    cnt["fail"] += 1
    print("FAIL", msg, sw.fmt(inst), "P=", P, flush=True)


def check_swap(inst, pp, a, p, r1, r2, p1, p2):
    cnt["straddles"] += 1
    P = pp.P
    if not (r2 - r1 == 2 and p2 - p1 == 2):
        Pn = P[:r1 + 1] + [pp.pid[p]] + P[r2:p1 + 1] + [pp.pid[a]] + P[p2:] if r2 < p1 else \
            P[:p1 + 1] + [pp.pid[a]] + P[p2:r1 + 1] + [pp.pid[p]] + P[r2:]
        if sw.is_valid_walk(inst, tuple(Pn)) and len(Pn) < len(P):
            fail("non-tight straddle gives shorter path (P not shortest?!)", inst, P)
        else:
            fail("non-tight straddle", inst, P)
        return
    Pn = list(P)
    Pn[a] = pp.pid[p]
    Pn[p] = pp.pid[a]
    if not sw.is_valid_walk(inst, tuple(Pn)):
        fail("swap invalid", inst, P)
        return
    q2 = prove.Path(inst, Pn)
    T = q2.typ[a]
    certs = {T: ([q2.pid[a]], [q2.pid[b] for b in range(q2.r) if q2.typ[b] == T and abs(b - a) == 1]),
             1 - T: ([q2.pid[p]], [q2.pid[b] for b in range(q2.r) if q2.typ[b] == 1 - T and abs(b - p) == 1])}
    try:
        st = prove.verify_cert(inst, Pn, certs)
        if st > 6:
            fail("swap storage > 6", inst, P)
    except AssertionError as ex:
        fail("swap certificate: " + repr(ex), inst, P)


def all_straddles(pp):
    r = pp.r
    for a in range(r):
        if pp.pid[a] is None:
            continue
        for p in range(r):
            if pp.typ[p] == pp.typ[a] or pp.pid[p] is None:
                continue
            T = pp.typ[a]
            bl = [x for x in range(a) if pp.typ[x] == T and (pp.Xp[p] & pp.X[x])]
            ab = [x for x in range(a + 1, r) if pp.typ[x] == T and (pp.Xp[p] & pp.X[x])]
            fl = [x for x in range(p) if pp.typ[x] != T and (pp.Xp[a] & pp.X[x])]
            fa = [x for x in range(p + 1, r) if pp.typ[x] != T and (pp.Xp[a] & pp.X[x])]
            if bl and ab and fl and fa:
                r1, r2, p1, p2 = max(bl), min(ab), max(fl), min(fa)
                if r2 < p1 or p2 < r1:
                    yield a, p, r1, r2, p1, p2


def analyse(inst, P):
    pp = prove.Path(inst, P)
    cnt["paths"] += 1
    r = pp.r
    try:
        kinds = [pp.kind(a) if pp.pid[a] is not None else "loc" for a in range(r)]
    except AssertionError as ex:
        fail(repr(ex), inst, P)
        return
    for st in all_straddles(pp):
        check_swap(inst, pp, *st)
    for T in (0, 1):
        O = 1 - T
        Om = [q for q in range(r) if pp.typ[q] == O]
        if not Om or any(kinds[q] == "loc" for q in Om):
            continue
        cnt["caseii"] += 1
        fw = [q for q in Om if kinds[q] == "fwd"]
        bw = [q for q in Om if kinds[q] == "bwd"]
        qf = max(fw) if fw else -10
        qb = min(bw) if bw else r + 10
        if qb < qf - 1:
            fail("Lemma 2 consequence", inst, P)
        for a in range(r):
            if pp.typ[a] != T or pp.pid[a] is None:
                continue
            if a <= qf - 2 and not (pp.Xp[a] & pp.X[qf]):
                fail("domination qf", inst, P)
            if a >= qb + 2 and not (pp.Xp[a] & pp.X[qb]):
                fail("domination qb", inst, P)
        R = [a for a in range(max(qf + 1, 0), min(qb, r))]
        if any(pp.typ[a] != T for a in R):
            fail("critical run not of one type", inst, P)
            continue
        rows = [a for a in R if kinds[a] == "fwd" and a != qb - 1 and pp.pid[a] is not None]
        cols = [q for q in Om if q >= qb]
        f = {a: set(pp.f(a)) for a in rows}
        for a in rows:
            if not f[a] <= set(cols):
                fail("f(a) not in C", inst, P)
        b = {p: set(x for x in R if (pp.Xp[p] & pp.X[x])) for p in cols if pp.pid[p] is not None}
        for a in rows:
            if len(f[a]) < 2:
                continue
            lo, hi = min(f[a]), max(f[a])
            for p in cols:
                if lo < p < hi and p not in f[a] and p in b:
                    cnt["holes"] += 1
                    if a not in b[p]:
                        fail("(3a): hole row not in b(p)", inst, P)
        spans = {a: (min(f[a]), max(f[a])) for a in rows if f[a]}
        for x, y, z in itertools.permutations(list(spans), 3):
            sx, sy, sz = spans[x], spans[y], spans[z]
            if not (sx[1] < sy[0] and sy[1] < sz[0]):
                continue
            if not (x < y < z or x > y > z):
                continue
            if len(f[y]) < 3:
                continue
            cnt["triples"] += 1
            pin = sorted(f[y])[1]
            if pin not in b or x not in b[pin] or z not in b[pin]:
                fail("(3b): outer rows not in b(p)", inst, P)


t0 = time.time()
for it in range(count):
    if mode == "saturated":
        L = rng.randint(7, 13)
        word = "".join(rng.choice("EF") for _ in range(L))
        inst, P0 = saturate.saturate(rng, word, 0.3)
        if inst is None:
            continue
    else:
        inst = gen_instance(rng, mode)
        if len(inst[1]) > 12:
            continue
    L, paths = sw.shortest_valid_paths(inst, limit=100)
    for P in paths:
        analyse(inst, list(P))
print("seed", seed, "mode", mode, cnt, "%.1fs" % (time.time() - t0), flush=True)
