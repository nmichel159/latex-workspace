"""Planted instances (band and incremental generators of qgen2.py): every claim on every shortest valid path.

usage: python test_planted.py GEN SEED COUNT WORKERS [params as key=value ...]
GEN = band | inc.  Each instance i uses random.Random(SEED * 1000003 + i).  Parameters (defaults in DEF):
band: r, lam (default r // 2 - 1), nTc, nOc, mT, mO, offc, ptour; inc: r, nTc, nOc, mates, offc, offn, pextra.
Per instance: P2; the planted path is a shortest valid path (exact search); all shortest valid paths (limit
`plim`): check_basic, Lemma 2a.1, Theorem Q for both types (case, lam, centres h, |Phi|), full covers <= k,
Lemma PP; if the number of classes is <= dmax: exact DESC (hypercube distances): emin(h, 0) <= 3h, emin(k,0) if
k <= 3, emin(1, 0), emin(2, 0).  Prints totals and the distribution of (h, |Phi|) and writes failures.
"""
import json
import random
import sys
import traceback
from collections import Counter
from multiprocessing import Pool

from qcore import hyper_dist, desc_emin, kq
from qchecks import (ClaimFailure, check_basic, check_2a1, check_theorem_q, full_covers, check_pp, bump, bmax)
from qgen2 import band, incremental, word_of

DEF = {"r": 9, "nTc": 3, "nOc": 2, "mT": 4, "mO": 4, "offc": 0, "ptour": 0.5, "mates": 1, "offn": 1,
       "pextra": 0.5, "plim": 40, "dmax": 13, "lam": None, "word": 0}


def make(gen, rng, P):
    if gen == "band":
        r = P["r"]
        lam = P["lam"] if P["lam"] is not None else max(1, r // 2 - 1)
        I, Pp, info = band(rng, r, lam, P["nTc"], P["nOc"], P["mT"], P["mO"], offc=P["offc"], p_tour=P["ptour"])
        return I, Pp
    wk = ["rand", "zones", "blocks"][P["word"]] if P["word"] < 3 else rng.choice(["rand", "zones", "blocks"])
    w = word_of(rng, P["r"], wk)
    out = incremental(rng, P["r"], P["nTc"], P["nOc"], mates=P["mates"], offc=P["offc"], offn=P["offn"],
                      p_extra=P["pextra"], word=w)
    return out if out is not None else (None, None)


def run(args):
    gen, seed, lo, hi, P = args
    st = {}
    hist = Counter()
    fails = []
    for idx in range(lo, hi):
        rng = random.Random(seed * 1000003 + idx)
        I, Pp = make(gen, rng, P)
        if I is None:
            bump(st, "gen_reject")
            continue
        bump(st, "inst")
        try:
            assert I.p2(), "P2"
            r, paths = I.shortest_paths_dfs(limit=P["plim"])
            assert r == len(Pp), ("planted path not shortest", r, len(Pp))
            assert Pp in paths or len(paths) >= P["plim"], "planted path not found among shortest"
            k = kq(I.n)
            bmax(st, "n_max", I.n)
            bmax(st, "c_max", I.c)
            if I.c > 3 * k:
                bump(st, "nondegenerate_c_gt_3k")
            hs = []
            for Q in paths:
                Q = list(Q)
                check_basic(I, Q, st)
                check_2a1(I, Q, rng, st, trials=1)
                for T in (0, 1):
                    out = check_theorem_q(I, Q, T, st)
                    hs.append(out["h"])
                    hist[(str(out["case"]), out["h"], out["phi"])] += 1
                    hO, hT = full_covers(I, Q, T)
                    m = min(x for x in (hO, hT, 10 ** 9) if x is not None)
                    if m < 10 ** 9:
                        assert m <= k, "full covers exceed k"
                        bmax(st, "fullcover_min_max", m)
                    check_pp(I, Q, T, st, maxpairs=30)
            if I.c <= P["dmax"]:
                sols = I.solutions()
                dist = hyper_dist(I.c, sols)
                h = min(hs)
                e1, _ = desc_emin(I, h, 0, dist)
                assert e1 <= 3 * h, ("DESC(h,0,3h)", h, e1)
                if k <= 3:
                    ek, _ = desc_emin(I, k, 0, dist)
                    assert ek <= 3 * k
                for f in (1, 2):
                    ef, _ = desc_emin(I, f, 0, dist)
                    bmax(st, "emin_f%d_max" % f, ef)
                bump(st, "desc_runs")
        except (ClaimFailure, AssertionError) as ex:
            fails.append({"idx": idx, "err": repr(ex), "inst": I.to_json(), "P": list(Pp),
                          "tb": traceback.format_exc()[-800:]})
            bump(st, "FAIL")
    return st, hist, fails


def merge(a, b):
    for k, v in b.items():
        if k.endswith("_max") or k in ("r_max", "W_maxwidth", "nonconsistent_maxwidth"):
            a[k] = max(a.get(k, -1), v)
        else:
            a[k] = a.get(k, 0) + v


def main():
    gen, seed, count, workers = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    P = dict(DEF)
    for kv in sys.argv[5:]:
        key, val = kv.split("=")
        P[key] = float(val) if "." in val else int(val)
    chunk = max(1, count // (workers * 3))
    jobs = [(gen, seed, lo, min(count, lo + chunk), P) for lo in range(0, count, chunk)]
    tot = {}
    hist = Counter()
    allf = []
    with Pool(workers) as pool:
        for st, h, fails in pool.imap_unordered(run, jobs):
            merge(tot, st)
            hist.update(h)
            allf.extend(fails)
    print(gen, json.dumps(P, sort_keys=True), flush=True)
    print(json.dumps(tot, sort_keys=True), flush=True)
    print("(case, h, |Phi|) histogram:", sorted(hist.items()), flush=True)
    if allf:
        with open("runs/fail-planted-%s-%d.json" % (gen, seed), "w") as fh:
            json.dump(allf[:30], fh)
        print("FAILURES", len(allf), allf[0]["err"], flush=True)


if __name__ == "__main__":
    main()
