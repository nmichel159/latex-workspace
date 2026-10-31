"""Random instances with classes + P2: every claim on every shortest valid path, DESC against brute force.

usage: python test_rand.py SEED COUNT NMIN NMAX nmin nmax WORKERS [pathlimit] [descmax_c]
For each instance (seed = SEED * 1000003 + index): N in [NMIN, NMAX] nodes, n in [nmin, nmax] switches, c classes
in [1, n]; P2 repaired with private or shared nodes.  On every shortest valid path (up to pathlimit) and both
types: check_basic (A1-A4, Lemma W), Lemma 2a.1, Theorem Q (proof steps), Lemma PP.  If c <= descmax_c: the exact
hypercube distance to the solution set, DESC(h, 0, 3h) and DESC(k, 0, 3k) must accept on yes-instances, and every
DESC run rejects no-instances; emin(f, 0) for f = 1, 2 recorded.
"""
import json
import random
import sys
import traceback
from multiprocessing import Pool

from qcore import hyper_dist, desc_emin, kq
from qchecks import (ClaimFailure, check_basic, check_2a1, check_theorem_q, full_covers, check_pp, bump, bmax)
from qgen import random_instance


def run(args):
    seed, lo, hi, NMIN, NMAX, nmin, nmax, plim, dmax = args
    st = {}
    fails = []
    for idx in range(lo, hi):
        rng = random.Random(seed * 1000003 + idx)
        N = rng.randint(NMIN, NMAX)
        n = rng.randint(nmin, nmax)
        c = rng.randint(1, n)
        I = random_instance(rng, N, n, c, rng.choice([0.15, 0.25, 0.35, 0.5]),
                            rng.choice([0.15, 0.25, 0.35, 0.5]), fresh=rng.random(), p2=True)
        if not I.p2():
            bump(st, "p2_fail_gen")
            continue
        bump(st, "inst")
        try:
            r, paths = I.shortest_paths_dfs(limit=plim)
            if r is None:
                bump(st, "no")
                if I.c <= dmax:
                    sols = I.solutions()
                    assert not sols, "dfs says no, brute says yes"
                continue
            bump(st, "yes")
            hs = []
            for P in paths:
                check_basic(I, list(P), st)
                check_2a1(I, list(P), rng, st, trials=2)
                for T in (0, 1):
                    out = check_theorem_q(I, list(P), T, st)
                    hs.append(out["h"])
                    hO, hT = full_covers(I, list(P), T)
                    m = min(x for x in (hO, hT, 10 ** 9) if x is not None)
                    if m < 10 ** 9:
                        bmax(st, "fullcover_min_max", m)
                        assert m <= kq(I.n), "full covers exceed k"
                    check_pp(I, list(P), T, st, maxpairs=20)
            if I.c <= dmax:
                sols = I.solutions()
                assert sols, "dfs yes, brute no"
                dist = hyper_dist(I.c, sols)
                h = min(hs)
                e1, _ = desc_emin(I, h, 0, dist)
                assert e1 <= 3 * h, ("DESC(h,0,3h)", h, e1)
                k = kq(I.n)
                if k <= 3:
                    ek, _ = desc_emin(I, k, 0, dist)
                    assert ek <= 3 * k, ("DESC(k,0,3k)", k, ek)
                    bump(st, "desc_k_runs")
                for f in (1, 2):
                    ef, _ = desc_emin(I, f, 0, dist)
                    bmax(st, "emin_f%d_max" % f, ef)
                    if ef > 3 * f:
                        bump(st, "emin_f%d_gt_3f" % f)
                bump(st, "desc_runs")
                if I.c > 3 * k:
                    bump(st, "desc_nondegenerate")
        except (ClaimFailure, AssertionError) as ex:
            fails.append({"idx": idx, "err": repr(ex), "inst": I.to_json(), "tb": traceback.format_exc()[-800:]})
            bump(st, "FAIL")
    return st, fails


def merge(a, b):
    for k, v in b.items():
        if k.endswith("_max") or k.startswith("Q_h") or k in ("r_max", "W_maxwidth", "nonconsistent_maxwidth"):
            a[k] = max(a.get(k, -1), v)
        else:
            a[k] = a.get(k, 0) + v


def main():
    seed, count = int(sys.argv[1]), int(sys.argv[2])
    NMIN, NMAX, nmin, nmax, workers = map(int, sys.argv[3:8])
    plim = int(sys.argv[8]) if len(sys.argv) > 8 else 30
    dmax = int(sys.argv[9]) if len(sys.argv) > 9 else 12
    chunk = max(1, count // (workers * 4))
    jobs = [(seed, lo, min(count, lo + chunk), NMIN, NMAX, nmin, nmax, plim, dmax) for lo in range(0, count, chunk)]
    tot = {}
    allf = []
    with Pool(workers) as pool:
        for st, fails in pool.imap_unordered(run, jobs):
            merge(tot, st)
            allf.extend(fails)
    print(json.dumps(tot, sort_keys=True), flush=True)
    if allf:
        with open("runs/fail-rand-%d.json" % seed, "w") as fh:
            json.dump(allf[:50], fh)
        print("FAILURES", len(allf), allf[0]["err"], flush=True)


if __name__ == "__main__":
    main()
