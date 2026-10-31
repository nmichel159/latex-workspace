"""T3 (r4-hard.md section 6), ZZ level: random CNF formulas; checks of I0 and I (axioms, order on old elements
unchanged, P3, P2 status), and the answer by three methods: satisfiability (truth tables), zz_search on I and on I0,
and enumeration of all down-sets of I0 (small I0 only).  Usage: python t3_zz.py SEED COUNT MAXVARS MAXCLAUSES"""
import random
import sys
from zzlib import Inst
from t3lib import from_sat, add_pendants, satisfiable


def rand_formula(rng, maxv, maxc):
    nv = rng.randint(1, maxv)
    m = rng.randint(1, maxc)
    clauses = []
    for _ in range(m):
        k = rng.randint(1, 3)
        cl = [rng.choice((1, -1)) * rng.randint(1, nv) for _ in range(k)]
        clauses.append(cl)
    return nv, clauses


def main():
    seed, count, maxv, maxc = map(int, sys.argv[1:5])
    rng = random.Random(seed)
    stats = dict(total=0, sat=0, unsat=0, p2fail=0, brute=0, mismatch=0, p3fail=0, axiom=0)
    for it in range(count):
        nv, clauses = rand_formula(rng, maxv, maxc)
        I0 = from_sat(nv, clauses)
        I = add_pendants(I0)
        bad = I0.check() + I.check()
        if bad:
            stats["axiom"] += 1
            print("AXIOM", nv, clauses, bad[:5])
        # order among old elements unchanged, no ties
        for x in range(I0.n):
            for y in range(I0.n):
                if I0.le(x, y) != I.le(x, y):
                    stats["axiom"] += 1
                    print("ORDER CHANGED", nv, clauses, x, y)
        if I.has_ties():
            print("TIES", nv, clauses)
            stats["axiom"] += 1
        # pendants: only u below, comparable with every old element, pairwise incomparable
        for x, b in I.pendants.items():
            assert bin(I.down[b]).count("1") == 2, (clauses, x)
            for y in range(I0.n):
                assert I.comparable(b, y)
        p3 = I.p3_failures()
        if p3:
            stats["p3fail"] += 1
            print("P3 FAIL", nv, clauses, p3[:3])
        if not I.p2_failures():
            stats["p2fail"] += 0
        else:
            stats["p2fail"] += 1
        sat = satisfiable(nv, clauses)
        a_I = I.zz_search()
        a_I0 = I0.zz_search()
        res = [sat, a_I, a_I0]
        if I0.n <= 26:
            try:
                res.append(I0.zz_brute(limit=200000))
                stats["brute"] += 1
            except OverflowError:
                pass
        if len(set(res)) != 1:
            stats["mismatch"] += 1
            print("MISMATCH", nv, clauses, res)
        # the zigzag found in I is consistent and uses no pendant
        if a_I:
            ok, path, D = I.zz_search(want=True)
            assert all(x < I0.n for x in path)
            assert I.is_downset(D) and I.connected_in_GD(D)
        stats["total"] += 1
        stats["sat" if sat else "unsat"] += 1
    print("seed %d count %d maxv %d maxc %d:" % (seed, count, maxv, maxc), stats)


if __name__ == "__main__":
    main()
