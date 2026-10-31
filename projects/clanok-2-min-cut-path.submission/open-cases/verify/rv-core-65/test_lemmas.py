"""Checks of r5-core.md Section 6.1-6.4 (facts (a)-(c), Lemma 6.2, Lemma 6.3, Lemma 6.4, duality with strict
anchors) on every shortest valid path of random general ZZ + P2 instances.  Reviewer's own code (gsf, thy).

usage: python test_lemmas.py SEED COUNT MMIN MMAX [PATHCAP] [JMAX] [profile]
profile: mix (default), dense-med (many middle edges), dense-order, ties
"""
import sys
import time
import random
from collections import Counter
from gsf import bits, popcount, random_inst
from thy import Stars, Skel, cov_E, cov_F, bad_pairs


def gen(rng, mmin, mmax, profile):
    m = rng.randint(mmin, mmax)
    if profile == "dense-med":
        return random_inst(rng, m, p_order=rng.choice([0.3, 0.45]), p_tie=rng.choice([0, 0.3]),
                           p_side=rng.choice([0.12, 0.2]), p_med=rng.choice([0.5, 0.8]),
                           repair=["low", "up", "low", "up", "freshE", "freshF"])
    if profile == "dense-order":
        return random_inst(rng, m, p_order=rng.choice([0.5, 0.7]), p_tie=rng.choice([0, 0.5]),
                           p_side=rng.choice([0.15, 0.25]), p_med=rng.choice([0.1, 0.3]))
    if profile == "ties":
        return random_inst(rng, m, p_order=rng.choice([0.15, 0.3]), p_tie=rng.choice([1.0, 2.0]),
                           p_side=rng.choice([0.15, 0.25]), p_med=rng.choice([0.1, 0.3]))
    return random_inst(rng, m, p_order=rng.choice([0.2, 0.35, 0.5]), p_tie=rng.choice([0, 0, 0.5]),
                       p_side=rng.choice([0.12, 0.2, 0.3]), p_med=rng.choice([0.1, 0.3, 0.6]))


def chains(I, K, consistent_off, j):
    """All chains Z_1..Z_j of P-consistent nonempty sides of pairwise distinct switches not on P, no conflict pair,
    consecutive sides meeting."""
    out = []

    def rec(ch, used):
        if len(ch) == j:
            out.append(list(ch))
            return
        last = ch[-1]
        for sd in consistent_off:
            w = sd[0]
            if w in used:
                continue
            if not I.side_mask(sd) & I.side_mask(last):
                continue
            if any(I.conflict(sd, z) for z in ch):
                continue
            ch.append(sd)
            used.add(w)
            rec(ch, used)
            ch.pop()
            used.discard(w)
    for sd in consistent_off:
        rec([sd], {sd[0]})
    return out


def check_path(I, St, P, st, jmax):
    K = Skel(I, P)
    assert I.is_valid_path(P)
    members = list(P)
    m = I.m
    allsides = [(w, typ) for w in range(m) for typ in (0, 1) if I.side_mask((w, typ))]
    cons = [sd for sd in allsides if K.consistent_side(sd)]
    # (a)
    for sd in cons:
        for M in members:
            if I.conflict(sd, M):
                st["FACT (a) FAILS"] += 1
    # (b)
    for sd in cons:
        if (K.onP >> sd[0]) & 1 and sd not in members:
            st["FACT (b) FAILS"] += 1
    # (c)
    for i, s1 in enumerate(cons):
        for s2 in cons[i + 1:]:
            if I.conflict(s1, s2):
                e, f = (s1, s2) if s1[1] == 0 else (s2, s1)
                w, z = e[0], f[0]
                if not (e[1] == 0 and f[1] == 1 and I.le[w][z]):
                    st["FACT (c) FAILS (shape)"] += 1
                if ((K.Up | K.L) >> w) & 1 or ((K.Up | K.L) >> z) & 1:
                    st["FACT (c) FAILS (outside Up, L)"] += 1
                st["(c) conflicting consistent pairs"] += 1
    # picks iff L <= D <= Q - Up, for every down-set
    for D in I.downsets():
        pk = all((((D >> w) & 1) == typ) for (w, typ) in members)
        if pk != K.picks(D):
            st["PICK CRITERION FAILS"] += 1
    # Lemma 6.2
    cons_off = [sd for sd in cons if not (K.onP >> sd[0]) & 1]
    contacts = {sd: [c for c in range(1, K.r + 1) if I.side_mask(P[c - 1]) & I.side_mask(sd)] for sd in cons_off}
    for j in range(1, jmax + 1):
        for ch in chains(I, K, cons_off, j):
            c1 = contacts[ch[0]]
            c2 = contacts[ch[-1]]
            if not c1 or not c2:
                continue
            gap = max(max(c2) - min(c1), max(c1) - min(c2))
            st["6.2 chains with contacts j=%d" % j] += 1
            st["6.2 max(|c-d| - j)"] = max(st["6.2 max(|c-d| - j)"], gap - j)
            if gap > j + 1:
                st["LEMMA 6.2 FAILS"] += 1
    # Lemma 6.3 (and its dual)
    for x in range(m):
        if (K.L >> x) & 1:
            continue
        Sx = St.NEstar[x] & K.A
        if Sx:
            ps = [K.pos[a] for a in bits(Sx)]
            span = max(ps) - min(ps)
            st["6.3 max span E"] = max(st["6.3 max span E"], span)
            st["6.3 max |S_x|"] = max(st["6.3 max |S_x|"], popcount(Sx))
            if span > 8:
                st["LEMMA 6.3 FAILS"] += 1
            if not I.medges and span > 2:
                st["LEMMA W (no middle edges) FAILS"] += 1
    for y in range(m):
        if (K.Up >> y) & 1:
            continue
        Sy = St.NFstar[y] & K.B
        if Sy:
            ps = [K.pos[b] for b in bits(Sy)]
            span = max(ps) - min(ps)
            st["6.3 max span F"] = max(st["6.3 max span F"], span)
            st["6.3 max |S_y| dual"] = max(st["6.3 max |S_y| dual"], popcount(Sy))
            if span > 8:
                st["LEMMA 6.3 DUAL FAILS"] += 1
    # Lemma 6.4 and duality with strict anchors
    for x in bits(K.NFi):
        for y in bits(K.NEi):
            if I.le[x][y]:
                st["PAIR WITH x <= y"] += 1
                continue
            ce = (cov_E(I, St, K, x) >> y) & 1
            cf = (cov_F(I, St, K, y) >> x) & 1
            if not I.le[y][x]:
                st["6.4 incomparable pairs"] += 1
                if not ((St.NEstar[x] >> y) & 1 or (St.NFstar[y] >> x) & 1):
                    st["LEMMA 6.4 FAILS"] += 1
            else:
                bad = not ((K.A >> x) & 1) and not ((K.B >> y) & 1)
                st["comparable pairs (bad)" if bad else "comparable pairs (anchored)"] += 1
                if not bad and not (ce or cf):
                    st["DUALITY (STRICT ANCHORS) FAILS"] += 1
    # strict anchors contain no element of Up / A (dually L / B)
    for a in bits(K.A):
        sd = I.strict_down(a)
        if sd & K.Up or sd & K.A:
            st["STRICT ANCHOR MEETS Up OR A"] += 1
    for b in bits(K.B):
        su = I.strict_up(b)
        if su & K.L or su & K.B:
            st["STRICT ANCHOR MEETS L OR B"] += 1
    # remark of 6.3: NE(Estar w) = NE(E_w) + Sib(w) (+ w)
    for w in range(m):
        sib = 0
        for z in I.lmn[w]:
            for v in I.umn[z]:
                sib |= 1 << v
        lhs = St.NEstar[w]
        rhs = St.NE(I.E[w]) | sib
        if lhs != rhs:
            st["REMARK NE(E#) IDENTITY FAILS"] += 1
    nb = len(bad_pairs(I, K))
    st["bad pairs"] += nb
    st["max bad pairs on a path"] = max(st["max bad pairs on a path"], nb)


def main():
    seed, count, mmin, mmax = (int(a) for a in sys.argv[1:5])
    cap = int(sys.argv[5]) if len(sys.argv) > 5 else 30
    jmax = int(sys.argv[6]) if len(sys.argv) > 6 else 3
    profile = sys.argv[7] if len(sys.argv) > 7 else "mix"
    rng = random.Random(seed)
    st = Counter()
    t0 = time.time()
    for it in range(count):
        I = gen(rng, mmin, mmax, profile)
        I.validate()
        if not I.p2():
            st["P2 FAILS (generator)"] += 1
            continue
        st["instances"] += 1
        if I.s == I.t:
            st["s = t"] += 1
            continue
        r, paths = I.shortest_paths(cap=cap)
        if r is None:
            st["no-instances"] += 1
            continue
        st["yes-instances"] += 1
        St = Stars(I)
        for P in paths:
            st["paths"] += 1
            check_path(I, St, P, st, jmax)
        if (it + 1) % 100 == 0:
            print("  %d (%.0fs) %s" % (it + 1, time.time() - t0, dict(st)), flush=True)
    print("test_lemmas seed %d count %d m %d-%d cap %d jmax %d profile %s (%.0fs)"
          % (seed, count, mmin, mmax, cap, jmax, profile, time.time() - t0))
    for k in sorted(st):
        print("  %-45s %s" % (k, st[k]))


if __name__ == "__main__":
    main()
