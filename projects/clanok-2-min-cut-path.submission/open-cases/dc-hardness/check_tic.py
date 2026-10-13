"""Checks for tic.py.
 (1) Theorem L(b): local_sat_instance(phi) is coverable iff phi is satisfiable (random small formulas with every
     variable having at most one occurrence of one sign); reach <= 2 when each variable occurs at most 3 times.
 (2) R_L as TIC: P2 holds and the only solution is the alternating one.
 (3) Theorem L(a) on random TIC + P2 instances: the window algorithm restricted to sets S of size <= |W| + 1
     (W = junction range of the concentrated type, which exists by the lemma) agrees with brute force; the lemma
     itself (one type concentrated in 5*reach+1 junctions) is checked.
Usage: python check_tic.py SEED COUNT"""
import sys
import random
import itertools
import tic


def check_local(rng, count):
    st = {}
    maxreach = 0
    for it in range(count):
        nv = rng.randint(1, 4)
        m = rng.randint(1, 6)
        # every variable: at most one occurrence of one sign
        clauses = [[] for _ in range(m)]
        for z in range(1, nv + 1):
            sgn = rng.choice([1, -1])
            k = rng.randint(0, 3)
            for _ in range(k):
                clauses[rng.randrange(m)].append(sgn * z)
            if rng.random() < 0.8:
                clauses[rng.randrange(m)].append(-sgn * z)
        clauses = [sorted(set(c)) for c in clauses if c]
        if not clauses:
            continue
        # remove clauses containing x and -x
        clauses = [c for c in clauses if not any(-l in c for l in c)]
        if not clauses:
            continue
        try:
            K, E, F, occ = tic.local_sat_instance(nv, clauses)
        except ValueError:
            continue
        a = tic.exact(K, E, F) is not None
        s = tic.satisfiable(nv, clauses)
        st[(s, a)] = st.get((s, a), 0) + 1
        for sp in E + F:
            if sp is not None:
                maxreach = max(maxreach, sp[1] - sp[0])
    return st, maxreach


def check_rigid(LMAX):
    out = []
    for L in range(1, LMAX + 1):
        K, E, F = tic.rigid(L)
        sols = []
        n = len(E)
        for mask in range(1 << n):
            sp = [F[i] if (mask >> i) & 1 else E[i] for i in range(n)]
            if tic.covers(K, sp):
                sols.append(mask)
        alt = sum(1 << (k - 1) for k in range(1, L + 1) if k % 2 == 0)
        out.append((L, tic.p2_ok(E, F), sols == [alt]))
    return out


def concentrated(E, F, reach):
    """Return (T, lo, hi): a type whose spans all lie in junctions lo..hi with hi - lo <= 5*reach (the lemma)."""
    res = []
    for T, S in (("E", E), ("F", F)):
        sp = [x for x in S if x is not None]
        if not sp:
            res.append((T, 0, -1))
            continue
        lo = min(x[0] for x in sp)
        hi = max(x[1] for x in sp)
        res.append((T, lo, hi))
    res.sort(key=lambda r: r[2] - r[1])
    return res[0]


def window_check(K, E, F, T, lo, hi):
    n = len(E)
    maxS = hi - lo + 2
    for r in range(0, min(n, maxS) + 1):
        for S in itertools.combinations(range(n), r):
            Ss = set(S)
            sp = []
            for i in range(n):
                inT = i in Ss
                if T == "F":
                    sp.append(F[i] if inT else E[i])
                else:
                    sp.append(E[i] if inT else F[i])
            if tic.covers(K, sp):
                return True
    return False


def check_window(rng, count):
    st = {"agree": 0, "disagree": 0, "lemma_fail": 0}
    for it in range(count):
        K = rng.randint(2, 14)
        n = rng.randint(2, 9)
        K, E, F = tic.random_tic(rng, K, n, longp=rng.choice([0.0, 0.1, 0.3]))
        reach = max(x[1] - x[0] for x in E + F if x is not None)
        T, lo, hi = concentrated(E, F, reach)
        if hi - lo > 5 * reach:
            st["lemma_fail"] += 1
        ex = tic.exact(K, E, F) is not None
        w = window_check(K, E, F, T, lo, hi)
        st["agree" if ex == w else "disagree"] += 1
    return st


if __name__ == "__main__":
    seed, count = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    print("(1) local SAT family (satisfiable, coverable):", check_local(rng, count))
    print("(2) rigid TIC (L, P2, only alternating):", check_rigid(12))
    print("(3) window algorithm vs brute force:", check_window(rng, count))
