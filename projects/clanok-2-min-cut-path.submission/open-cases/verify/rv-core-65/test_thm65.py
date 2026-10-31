"""Checks of Theorem 6.5 and Corollary 6.5' of r5-core.md on every shortest valid path and many bad-pair covers.
Reviewer's own code (gsf, thy, planted).

usage: python test_thm65.py SEED COUNT MMIN MMAX [GEN] [PATHCAP] [GDESC_MMAX]
GEN: random (gsf.random_inst, profile mix), planted (planted.planted_inst), both (alternating)
For every path P and cover (X0, Y0) of the bad pairs (all minimum covers, X0 = all bad x, Y0 = all bad y, random
supersets), with k = floor(log2 m) + 1, R = NF - X0, C = NE - Y0:
  * duality on R x C (no pair of R x C is bad);
  * exact fractional cover numbers tau_E (of C by the E-tools of R) and tau_F (of R by the F-tools of C);
    lambda >= 1/2 iff tau_E <= 2; the proof needs: tau_E <= 2 or tau_F < 2;
  * the proof's case split: lambda >= 1/2 => C has a cover by <= k E-tools, else R has a cover by <= k F-tools;
  * (E'): every inclusion-minimal cover T of C by E-tools of R gives an E-description (T' = T & A, F-anchors Y0,
    Phi = A & U) that picks every member of P, with |Phi| <= 9|T|; (F') dually;
  * the literal statement: (E) or (F) holds with at most k tools;
  * the empty cases (C or R empty);
  * Corollary 6.5': exact LP cover numbers of NE by the cheap E-tools and of NF by the cheap F-tools; integer cover
    numbers; integer <= ceil(tau ln m) + 1; min(tau_E*, tau_F*) <= 2 + max(|X0|, |Y0|).
Optionally (m <= GDESC_MMAX) the algorithm GDESC with k tools, kappa_min anchors, 9k flips against brute force.
"""
import sys
import math
import time
import random
import itertools
from fractions import Fraction
from collections import Counter
from gsf import bits, popcount, random_inst
from planted import planted_inst
from thy import (Stars, Skel, cov_E, cov_F, bad_pairs, min_vertex_cover, thm_desc_E, thm_desc_F, frac_cover,
                 min_cover, all_covers, gdesc)


def gen(rng, mmin, mmax, kind, it):
    if kind == "random" or (kind == "both" and it % 2 == 0):
        m = rng.randint(mmin, mmax)
        return random_inst(rng, m, p_order=rng.choice([0.3, 0.5, 0.7]), p_tie=rng.choice([0, 0, 0.5]),
                           p_side=rng.choice([0.1, 0.15, 0.25]), p_med=rng.choice([0.1, 0.3, 0.6]))
    m = rng.randint(mmin, mmax)
    r = rng.randint(3, max(3, m - 2))
    rest = m - r
    n_up = rng.randint(0, rest)
    n_down = rng.randint(0, rest - n_up)
    n_free = rest - n_up - n_down
    return planted_inst(rng, r=r, n_up=n_up, n_down=n_down, n_free=n_free, p_rel=rng.choice([0.2, 0.4, 0.6]),
                        p_bad=rng.choice([0.5, 0.8, 1.0]), p_tie=rng.choice([0, 0.05, 0.15]),
                        p_side=rng.choice([0.1, 0.2]), p_contact=rng.choice([0.1, 0.3]),
                        p_med=rng.choice([0.1, 0.3, 0.5]))


def cheap_tools(I, St, K, kind):
    """Cor. 6.5' cheap tools: kind E: stars Estar(w), w not in L (with strict anchor if w in A), F-anchors down(z),
    z not in Up; covered sets inside NE.  Returns list of (label, covered mask, is_star)."""
    out = []
    m = I.m
    if kind == 0:
        for w in range(m):
            if (K.L >> w) & 1:
                continue
            c = St.NEstar[w]
            if (K.A >> w) & 1:
                c |= I.strict_down(w)
            out.append((("star", w), c & K.NEi, True))
        for z in range(m):
            if (K.Up >> z) & 1:
                continue
            out.append((("anc", z), I.dn[z] & K.NEi, False))
    else:
        for w in range(m):
            if (K.Up >> w) & 1:
                continue
            c = St.NFstar[w]
            if (K.B >> w) & 1:
                c |= I.strict_up(w)
            out.append((("star", w), c & K.NFi, True))
        for z in range(m):
            if (K.L >> z) & 1:
                continue
            out.append((("anc", z), I.up[z] & K.NFi, False))
    return out


def cor65_desc(I, St, K, kind, chosen):
    """Description of Cor. 6.5' from a list of cheap tools."""
    stars = [lab[1] for lab, c, isstar in chosen if isstar]
    ancs = [lab[1] for lab, c, isstar in chosen if not isstar]
    if kind == 0:
        D, U, Phi = thm_desc_E(I, St, K, stars, ancs)
    else:
        D, U, Phi = thm_desc_F(I, St, K, stars, ancs)
    return D, Phi, len(stars)


def check_cover(I, St, K, X0, Y0, k, st, rng):
    m = I.m
    R = [x for x in bits(K.NFi) if x not in X0]
    C = [y for y in bits(K.NEi) if y not in Y0]
    st["covers tested"] += 1
    # empty cases
    if not C:
        D, U, Phi = thm_desc_E(I, St, K, [], sorted(Y0))
        st["case C empty"] += 1
        if not K.picks(D):
            st["EMPTY CASE (E) FAILS"] += 1
        return
    if not R:
        D, U, Phi = thm_desc_F(I, St, K, [], sorted(X0))
        st["case R empty"] += 1
        if not K.picks(D):
            st["EMPTY CASE (F) FAILS"] += 1
        return
    Cs, Rs = set(C), set(R)
    rowsets = [set(bits(cov_E(I, St, K, x))) & Cs for x in R]
    colsets = [set(bits(cov_F(I, St, K, y))) & Rs for y in C]
    # duality on R x C
    for i, x in enumerate(R):
        for j, y in enumerate(C):
            if y not in rowsets[i] and x not in colsets[j]:
                st["DUALITY FAILS ON R x C"] += 1
    tauE = frac_cover(rowsets, C)
    tauF = frac_cover(colsets, R)
    lam_half = tauE is not None and tauE <= 2
    st["lambda >= 1/2" if lam_half else "lambda < 1/2"] += 1
    if not lam_half and not (tauF is not None and tauF < 2):
        st["MINIMAX STEP FAILS (tau_F >= 2 although lambda < 1/2)"] += 1
    if tauE is not None and tauE == 2:
        st["lambda exactly 1/2"] += 1
    kE, TE = min_cover(rowsets, C, len(R))
    kF, TF = min_cover(colsets, R, len(C))
    if lam_half and (kE is None or kE > k):
        st["CASE lambda>=1/2: NO COVER BY k E-TOOLS"] += 1
    if not lam_half and (kF is None or kF > k):
        st["CASE lambda<1/2: NO COVER BY k F-TOOLS"] += 1
    best = min(x for x in (kE, kF) if x is not None) if (kE is not None or kF is not None) else None
    if best is None:
        st["NEITHER SIDE COVERABLE"] += 1
    else:
        st["max min(kE,kF)"] = max(st["max min(kE,kF)"], best)
    # (E'): every minimal cover by E-tools gives a picking description
    for comb in all_covers(rowsets, C, min(len(R), k + 1), cap=60):
        T = [R[i] for i in comb]
        D, U, Phi = thm_desc_E(I, St, K, T, sorted(Y0))
        st["(E') descriptions"] += 1
        if not I.is_downset(D):
            st["E-DESCRIPTION NOT A DOWN-SET"] += 1
        if not K.picks(D):
            st["(E') FAILS"] += 1
        elif not I.connects(D):
            st["(E') PICKS BUT DOES NOT CONNECT"] += 1
        if popcount(Phi) > 9 * len(T):
            st["(E') |Phi| > 9|T|"] += 1
        st["max |Phi|/|T| (E)"] = max(st["max |Phi|/|T| (E)"], Fraction(popcount(Phi), max(1, len(T))))
    for comb in all_covers(colsets, R, min(len(C), k + 1), cap=60):
        T = [C[i] for i in comb]
        D, U, Phi = thm_desc_F(I, St, K, T, sorted(X0))
        st["(F') descriptions"] += 1
        if not I.is_downset(D):
            st["F-DESCRIPTION NOT A DOWN-SET"] += 1
        if not K.picks(D):
            st["(F') FAILS"] += 1
        elif not I.connects(D):
            st["(F') PICKS BUT DOES NOT CONNECT"] += 1
        if popcount(Phi) > 9 * len(T):
            st["(F') |Phi| > 9|T|"] += 1
        st["max |Phi|/|T| (F)"] = max(st["max |Phi|/|T| (F)"], Fraction(popcount(Phi), max(1, len(T))))
    # literal statement: (E) or (F) with <= k tools from NF (resp. NE)
    lit = False
    NF, NE = bits(K.NFi), bits(K.NEi)
    for kk in range(0, k + 1):
        if lit:
            break
        for T in itertools.combinations(NF, kk):
            D, U, Phi = thm_desc_E(I, St, K, list(T), sorted(Y0))
            if K.picks(D) and popcount(Phi) <= 9 * k:
                lit = True
                break
        if lit:
            break
        for T in itertools.combinations(NE, kk):
            D, U, Phi = thm_desc_F(I, St, K, list(T), sorted(X0))
            if K.picks(D) and popcount(Phi) <= 9 * k:
                lit = True
                break
    if not lit:
        st["LITERAL (E) OR (F) FAILS"] += 1


def check_cor65(I, St, K, kappa, st):
    m = I.m
    taus = []
    for kind in (0, 1):
        items = bits(K.NEi if kind == 0 else K.NFi)
        tools = cheap_tools(I, St, K, kind)
        if not items:
            taus.append(Fraction(0))
            continue
        sets = [set(bits(c)) for lab, c, s in tools]
        tau = frac_cover(sets, items)
        if tau is None:
            st["COR 6.5': ITEMS NOT COVERABLE BY CHEAP TOOLS"] += 1
            taus.append(None)
            continue
        taus.append(tau)
        kint, comb = min_cover(sets, items, len(items))
        bound = math.ceil(float(tau) * math.log(m)) + 1 if m > 1 else 1
        if kint is None or kint > bound:
            st["COR 6.5' ROUNDING BOUND FAILS"] += 1
        greedy_bound = sum(Fraction(1, i) for i in range(1, len(items) + 1)) * tau
        st["max integer/tau"] = max(st["max integer/tau"], Fraction(kint, 1) / tau if tau else 0)
        chosen = [tools[i] for i in comb]
        D, Phi, nstars = cor65_desc(I, St, K, kind, chosen)
        st["cor 6.5' descriptions"] += 1
        if not K.picks(D):
            st["COR 6.5' DESCRIPTION FAILS"] += 1
        if popcount(Phi) > 9 * nstars:
            st["COR 6.5' FLIPS > 9 PER STAR"] += 1
    if taus[0] is not None and taus[1] is not None:
        mn = min(taus)
        if mn > 2 + kappa:
            st["COR 6.5': min LP cover > 2 + kappa"] += 1
        st["max min LP cover - kappa"] = max(st["max min LP cover - kappa"], mn - kappa)


def analyse(I, st, cap, rng, gd_mmax):
    m = I.m
    k = int(math.floor(math.log2(m))) + 1 if m >= 1 else 1
    if I.s == I.t:
        st["s = t"] += 1
        return
    r, paths = I.shortest_paths(cap=cap)
    if r is None:
        st["no-instances"] += 1
        if m <= gd_mmax - 1:
            St = Stars(I)
            if gdesc(I, St, min(k, 2), 1, 9 * k):
                st["GDESC ACCEPTS A NO-INSTANCE"] += 1
            st["GDESC no-instances run"] += 1
        return
    st["yes-instances"] += 1
    st["sum r"] += r
    St = Stars(I)
    kappa_min = None
    for P in paths:
        K = Skel(I, P)
        st["paths"] += 1
        bp = bad_pairs(I, K)
        kap, covers = min_vertex_cover(bp)
        st["paths with bad pairs"] += bool(bp)
        st["max bad pairs"] = max(st["max bad pairs"], len(bp))
        st["max kappa"] = max(st["max kappa"], kap)
        kappa_min = kap if kappa_min is None else min(kappa_min, kap)
        tested = set()
        cl = list(covers[:6])
        if bp:
            cl.append((frozenset(x for x, _ in bp), frozenset()))
            cl.append((frozenset(), frozenset(y for _, y in bp)))
            for _ in range(2):
                X0, Y0 = rng.choice(covers)
                X0 = set(X0) | set(x for x in bits(K.NFi) if rng.random() < 0.3)
                Y0 = set(Y0) | set(y for y in bits(K.NEi) if rng.random() < 0.3)
                cl.append((frozenset(X0), frozenset(Y0)))
        for X0, Y0 in cl:
            if (X0, Y0) in tested:
                continue
            tested.add((X0, Y0))
            check_cover(I, St, K, set(X0), set(Y0), k, st, rng)
        check_cor65(I, St, K, kap, st)
    st["inst with kappa_min > 0"] += kappa_min > 0
    st["max kappa_min"] = max(st["max kappa_min"], kappa_min)
    if m <= gd_mmax:
        acc = gdesc(I, St, k, kappa_min, 9 * k)
        st["GDESC(k, kappa_min, 9k) runs"] += 1
        if not acc:
            st["GDESC(k, kappa_min, 9k) REJECTS A YES-INSTANCE"] += 1
        acc0 = gdesc(I, St, k, 0, 9 * k)
        if not acc0:
            st["yes-instances needing anchors (GDESC(k,0,9k) rejects)"] += 1


def main():
    seed, count, mmin, mmax = (int(a) for a in sys.argv[1:5])
    kind = sys.argv[5] if len(sys.argv) > 5 else "both"
    cap = int(sys.argv[6]) if len(sys.argv) > 6 else 20
    gd_mmax = int(sys.argv[7]) if len(sys.argv) > 7 else 0
    rng = random.Random(seed)
    st = Counter()
    t0 = time.time()
    for it in range(count):
        I = gen(rng, mmin, mmax, kind, it)
        I.validate()
        if not I.p2():
            st["P2 FAILS (generator)"] += 1
            continue
        st["instances"] += 1
        analyse(I, st, cap, rng, gd_mmax)
        if (it + 1) % 50 == 0:
            print("  %d (%.0fs) %s" % (it + 1, time.time() - t0, dict(st)), flush=True)
    print("test_thm65 seed %d count %d m %d-%d gen %s cap %d gdesc<=%d (%.0fs)"
          % (seed, count, mmin, mmax, kind, cap, gd_mmax, time.time() - t0))
    for key in sorted(st):
        print("  %-55s %s" % (key, st[key]))


if __name__ == "__main__":
    main()
