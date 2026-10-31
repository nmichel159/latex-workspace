"""Exhaustive check on all small instances of 2CH with classes + P2.

usage: python test_exh.py N n WORKERS [descevery]
All instances with nodes 0..N-1 (s = 0, t = 1), n switches whose sides are arbitrary subsets of the nodes (empty
allowed), and every class partition of the switches (one representative per partition shape; switches of one class
as a multiset, classes of equal size as a multiset of classes).  On every P2 instance: brute force over the class
mode vectors = path search; every shortest valid path: check_basic (A1-A4, Lemma W), Lemma 2a.1, Theorem Q proof
steps for both types, full covers <= k, Lemma PP; every `descevery`-th instance: DESC(h, 0, 3h) accepts on yes,
emin(f, 0) for f <= 2 recorded, DESC rejects on no.
"""
import itertools
import json
import random
import sys
import traceback
from multiprocessing import Pool

from qcore import Inst, hyper_dist, desc_emin, kq
from qchecks import (ClaimFailure, check_basic, check_2a1, check_theorem_q, full_covers, check_pp, bump, bmax)


def int_partitions(n, maxpart=None):
    if maxpart is None:
        maxpart = n
    if n == 0:
        yield ()
        return
    for p in range(min(n, maxpart), 0, -1):
        for rest in int_partitions(n - p, p):
            yield (p,) + rest


def instances(N, n, shape, part, nparts):
    """yield (sw, cl) for the given shape; the outermost loop is split into nparts parts, this is part `part`"""
    full = (1 << N) - 1
    options = [(E, F) for E in range(full + 1) for F in range(full + 1)]
    groups = []
    for size in sorted(set(shape), reverse=True):
        mult = shape.count(size)
        groups.append((size, mult))
    msets = {size: list(itertools.combinations_with_replacement(range(len(options)), size)) for size, _ in groups}

    def group_iter(gi):
        size, mult = groups[gi]
        return itertools.combinations_with_replacement(range(len(msets[size])), mult)

    first = groups[0]
    idx0 = 0
    for g0 in group_iter(0):
        idx0 += 1
        if idx0 % nparts != part:
            continue
        rest_iters = [list(group_iter(gi)) for gi in range(1, len(groups))]
        for rest in itertools.product(*rest_iters):
            sw = []
            cl = []
            cid = 0
            for gi, combo in enumerate((g0,) + tuple(rest)):
                size, _ = groups[gi]
                for ms in combo:
                    for oi in msets[size][ms]:
                        sw.append(list(options[oi]))
                        cl.append(cid)
                    cid += 1
            yield sw, cl


def run(args):
    N, n, shape, part, nparts, descevery = args
    st = {}
    fails = []
    rng = random.Random(hash((N, n, shape, part)) & 0xffffffff)
    cnt = 0
    for sw, cl in instances(N, n, shape, part, nparts):
        bump(st, "all")
        I = Inst(N, 0, 1, sw, cl)
        if not I.p2():
            continue
        bump(st, "p2")
        cnt += 1
        try:
            sols = I.solutions()
            r, paths = I.shortest_paths_dfs()
            assert (r is not None) == bool(sols), "brute vs path search"
            if r is None:
                bump(st, "no")
                if cnt % descevery == 0:
                    dist = hyper_dist(I.c, sols)
                    e1, _ = desc_emin(I, 2, 1, dist)
                    assert e1 == 255, "DESC accepted a no-instance"
                    bump(st, "desc_no_runs")
                continue
            bump(st, "yes")
            hs = []
            for P in paths:
                P = list(P)
                check_basic(I, P, st)
                check_2a1(I, P, rng, st, trials=1)
                for T in (0, 1):
                    out = check_theorem_q(I, P, T, st)
                    hs.append(out["h"])
                    hO, hT = full_covers(I, P, T)
                    m = min(x for x in (hO, hT, 10 ** 9) if x is not None)
                    if m < 10 ** 9:
                        assert m <= kq(I.n), "full covers exceed k"
                        bmax(st, "fullcover_min_max", m)
                    check_pp(I, P, T, st)
            if cnt % descevery == 0:
                dist = hyper_dist(I.c, sols)
                h = min(hs)
                e1, _ = desc_emin(I, h, 0, dist)
                assert e1 <= 3 * h, ("DESC(h,0,3h)", h, e1)
                for f in (0, 1, 2):
                    ef, _ = desc_emin(I, f, 0, dist)
                    bmax(st, "emin_f%d_max" % f, ef)
                bump(st, "desc_yes_runs")
        except (ClaimFailure, AssertionError) as ex:
            fails.append({"err": repr(ex), "inst": I.to_json(), "tb": traceback.format_exc()[-600:]})
            bump(st, "FAIL")
    return st, fails


def merge(a, b):
    for k, v in b.items():
        if k.endswith("_max") or k in ("r_max", "W_maxwidth", "nonconsistent_maxwidth"):
            a[k] = max(a.get(k, -1), v)
        else:
            a[k] = a.get(k, 0) + v


def main():
    N, n, workers = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    descevery = int(sys.argv[4]) if len(sys.argv) > 4 else 25
    jobs = []
    for shape in int_partitions(n):
        nparts = workers * 2
        for part in range(nparts):
            jobs.append((N, n, shape, part, nparts, descevery))
    tot = {}
    allf = []
    with Pool(workers) as pool:
        for st, fails in pool.imap_unordered(run, jobs):
            merge(tot, st)
            allf.extend(fails)
    print("N=%d n=%d" % (N, n), json.dumps(tot, sort_keys=True), flush=True)
    if allf:
        with open("runs/fail-exh-%d-%d.json" % (N, n), "w") as fh:
            json.dump(allf[:50], fh)
        print("FAILURES", len(allf), allf[0]["err"], flush=True)


if __name__ == "__main__":
    main()
