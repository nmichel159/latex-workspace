"""Theorem 6.5 with kappa = 0 against Theorem Q of r5-classes.md (2CH with classes + P2), reviewer's own code.

usage: python test_classes.py SEED COUNT MMIN MMAX [PATHCAP] [DESC_MMAX]
Instances: switches partitioned into classes (ties of the preorder, no strict relations, no middle edges), random
sides, P2 between switches of different classes enforced by fresh nodes.  Checks:
  * no shortest valid path has a bad pair (kappa = 0);
  * the checks of test_thm65.check_cover with X0 = Y0 = empty, plus |A & U| <= 3|T| (Lemma W instead of 6.3);
  * every Theorem 6.5 E-description (F-description) equals sigma_U^Phi' of r5-classes.md Section 2a with
    tau = E (F), U = union of N_tau[E_x] (N_tau[F_y]) and Phi' = the classes meeting A & U (B & U') that sigma_U puts
    into the wrong mode, |Phi'| <= 3k;
  * DESC(k, 0, 3k) of Theorem Q (own implementation of sigma_U^Phi) and GDESC(k, 0, 3k) against brute force
    for m <= DESC_MMAX.
"""
import sys
import math
import time
import random
import itertools
from collections import Counter
from gsf import Inst, bits, popcount
from thy import Stars, Skel, bad_pairs, thm_desc_E, thm_desc_F, cov_E, cov_F, all_covers, gdesc
import test_thm65


def classes_inst(rng, m, ncls, p_side, extra_nodes):
    cls = [rng.randrange(ncls) for _ in range(m)]
    le = [[cls[a] == cls[b] for b in range(m)] for a in range(m)]
    N = 2 + extra_nodes
    E = [0] * m
    F = [0] * m
    for w in range(m):
        for nd in range(N):
            if rng.random() < p_side:
                E[w] |= 1 << nd
            if rng.random() < p_side:
                F[w] |= 1 << nd
    for x in range(m):
        for y in range(x + 1, m):
            if cls[x] == cls[y]:
                continue
            if E[x] & E[y] or F[x] & F[y]:
                continue
            nd = N
            N += 1
            if rng.random() < 0.5:
                E[x] |= 1 << nd
                E[y] |= 1 << nd
            else:
                F[x] |= 1 << nd
                F[y] |= 1 << nd
    return Inst(N, 0, 1, le, E, F, {}, "classes")


def sigma(I, tau, Ysides, Phi_classes):
    """sigma_U^Phi of r5-classes.md 2a: U = tau-sides meeting some Y in Ysides (node masks); a class goes to mode
    1 - tau iff all its nonempty tau-sides lie in U; then the classes in Phi_classes (class masks) are flipped.
    Returns the down-set D (switches in F-mode)."""
    m = I.m
    side = I.F if tau == 1 else I.E
    U = set(w for w in range(m) if side[w] and any(side[w] & Y for Y in Ysides))
    D = 0
    seen = 0
    for w in range(m):
        if (seen >> w) & 1:
            continue
        C = I.cls[w]
        seen |= C
        allin = all((w2 in U) for w2 in bits(C) if side[w2])
        mode = (1 - tau) if allin else tau            # 1 = F-mode
        if C in Phi_classes:
            mode = 1 - mode
        if mode == 1:
            D |= C
    return D


def desc_Q(I, k, e):
    """DESC(k, 0, e): both tau, every union of <= k sets N_tau[Z] (Z any nonempty side), every set of <= e classes."""
    sides = [I.E[w] for w in range(I.m) if I.E[w]] + [I.F[w] for w in range(I.m) if I.F[w]]
    sides = sorted(set(sides))
    classes = sorted(set(I.cls))
    cache = {}
    for tau in (0, 1):
        for kk in range(k + 1):
            for Ys in itertools.combinations(sides, kk):
                for ne in range(min(e, len(classes)) + 1):
                    for Ph in itertools.combinations(classes, ne):
                        D = sigma(I, tau, list(Ys), set(Ph))
                        if D not in cache:
                            cache[D] = I.connects(D)
                        if cache[D]:
                            return True
    return False


def main():
    seed, count, mmin, mmax = (int(a) for a in sys.argv[1:5])
    cap = int(sys.argv[5]) if len(sys.argv) > 5 else 20
    dmax = int(sys.argv[6]) if len(sys.argv) > 6 else 0
    rng = random.Random(seed)
    st = Counter()
    t0 = time.time()
    for it in range(count):
        m = rng.randint(mmin, mmax)
        I = classes_inst(rng, m, rng.randint(2, max(2, m - 1)), rng.choice([0.08, 0.12, 0.2]),
                         rng.randint(m // 2, m + 2))
        I.validate()
        assert I.p2()
        st["instances"] += 1
        k = int(math.floor(math.log2(m))) + 1
        r, paths = I.all_shortest_paths(cap=cap)
        yes = r is not None
        st["yes" if yes else "no"] += 1
        if m <= dmax:
            dq = desc_Q(I, k, 3 * k)
            St0 = Stars(I)
            dg = gdesc(I, St0, k, 0, 3 * k)
            if dq != yes:
                st["DESC(k,0,3k) WRONG" + (" (UNSOUND)" if dq else " (MISSES)")] += 1
            if dg != yes:
                st["GDESC(k,0,3k) WRONG" + (" (UNSOUND)" if dg else " (MISSES)")] += 1
            st["DESC/GDESC runs"] += 1
        if not yes:
            continue
        st["sum r"] += r
        St = Stars(I)
        for P in paths:
            K = Skel(I, P)
            st["paths"] += 1
            if bad_pairs(I, K):
                st["BAD PAIR IN CLASSES MODEL"] += 1
            test_thm65.check_cover(I, St, K, set(), set(), k, st, rng)
            R, C = bits(K.NFi), bits(K.NEi)
            # E-descriptions from covers of C by E-tools, compared with sigma (tau = E)
            if C and R:
                rowsets = [set(bits(cov_E(I, St, K, x))) & set(C) for x in R]
                for comb in all_covers(rowsets, C, min(len(R), k), cap=30):
                    T = [R[i] for i in comb]
                    D, U, Phi = thm_desc_E(I, St, K, T, [])
                    if popcount(Phi) > 3 * len(T):
                        st["|A & U| > 3|T| WITHOUT MIDDLE EDGES"] += 1
                    # Phi' = classes meeting Phi that sigma_U puts into F-mode
                    Ys = [I.E[x] for x in T if I.E[x]]
                    D0 = sigma(I, 0, Ys, set())
                    Php = set(I.cls[a] for a in bits(Phi) if (D0 >> a) & 1)
                    D1 = sigma(I, 0, Ys, Php)
                    st["sigma comparisons"] += 1
                    if D1 != D:
                        st["GDESC E-DESCRIPTION != sigma_U^Phi'"] += 1
                    if len(Php) > 3 * k:
                        st["|Phi'| > 3k"] += 1
                colsets = [set(bits(cov_F(I, St, K, y))) & set(R) for y in C]
                for comb in all_covers(colsets, R, min(len(C), k), cap=30):
                    T = [C[i] for i in comb]
                    D, U, Phi = thm_desc_F(I, St, K, T, [])
                    if popcount(Phi) > 3 * len(T):
                        st["|B & U'| > 3|T| WITHOUT MIDDLE EDGES"] += 1
                    Ys = [I.F[y] for y in T if I.F[y]]
                    D0 = sigma(I, 1, Ys, set())
                    Php = set(I.cls[b] for b in bits(Phi) if not (D0 >> b) & 1)
                    D1 = sigma(I, 1, Ys, Php)
                    st["sigma comparisons"] += 1
                    if D1 != D:
                        st["GDESC F-DESCRIPTION != sigma_U^Phi'"] += 1
        if (it + 1) % 100 == 0:
            print("  %d (%.0fs) %s" % (it + 1, time.time() - t0, dict(st)), flush=True)
    print("test_classes seed %d count %d m %d-%d cap %d desc<=%d (%.0fs)"
          % (seed, count, mmin, mmax, cap, dmax, time.time() - t0))
    for key in sorted(st):
        print("  %-55s %s" % (key, st[key]))


if __name__ == "__main__":
    main()
