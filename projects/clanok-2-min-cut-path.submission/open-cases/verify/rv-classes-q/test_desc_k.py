"""DESC(k, 0, 3k) with the parameters of Theorem Q on instances where it is not a brute force (more than 3k
classes), against the exact answer (all 2^c mode vectors, vectorised).

usage: python test_desc_k.py KIND SEED COUNT WORKERS [args]
KIND = rand   : random P2 instances with m switches in c classes (args: m c N)
       inc    : planted incremental instances (args: r nTc nOc mates offc)
       band   : band instances (args: r nTc nOc mT mO offc)
Per instance: k = floor(log2 m) + 1; asserted c > 3k is recorded; DESC(k, 0, 3k) run as an algorithm (early
exit) must accept iff the instance is a yes-instance; emin(1, 0) and emin(1, 1) (least number of flips with one
centre, with one centre and one class group or single side) are recorded; on yes-instances the proof
construction of Theorem Q is checked on up to 10 shortest valid paths for both types.
"""
import json
import random
import sys
import traceback
from collections import Counter
from multiprocessing import Pool

from qcore import solutions_np, hyper_dist_bool, desc_accepts, desc_emin, kq
from qchecks import ClaimFailure, check_basic, check_theorem_q, bump, bmax
from qgen import random_instance
from qgen2 import incremental, band, word_of


def make(kind, rng, a):
    if kind == "rand":
        m, c, N = a
        I = random_instance(rng, N, m, c, rng.choice([0.15, 0.25, 0.35]), rng.choice([0.15, 0.25, 0.35]),
                            fresh=rng.random(), p2=True)
        return I
    if kind == "inc":
        r, nTc, nOc, mates, offc = a
        w = word_of(rng, r, rng.choice(["zones", "blocks", "blocks"]))
        out = incremental(rng, r, nTc, nOc, mates=mates, offc=offc, offn=1, p_extra=0.5, word=w)
        return out[0] if out else None
    if kind == "band":
        r, nTc, nOc, mT, mO, offc = a
        lam = max(1, r // 2 - 1)
        I, P, _ = band(rng, r, lam, nTc, nOc, mT, mO, offc=offc)
        return I
    raise ValueError(kind)


def delete_nodes(I, rng, cnt):
    """the instance with `cnt` random nodes (not s, t) removed from every side; None if impossible"""
    from qcore import Inst
    cand = [x for x in range(2, I.N)]
    if len(cand) < cnt:
        return None
    dele = 0
    for x in rng.sample(cand, cnt):
        dele |= 1 << x
    sw = [[E & ~dele, F & ~dele] for E, F in I.sw]
    return Inst(I.N, I.s, I.t, sw, list(I.cl))


def run(job):
    kind, seed, lo, hi, a = job
    st = {}
    hist = Counter()
    fails = []
    for idx in range(lo, hi):
        rng = random.Random(seed * 1000003 + idx)
        I = make(kind, rng, a)
        if I is None:
            bump(st, "gen_reject")
            continue
        try:
            assert I.p2()
            k = kq(I.n)
            bump(st, "inst")
            if I.c > 3 * k:
                bump(st, "nondegenerate")
            else:
                bump(st, "degenerate")
            sol = solutions_np(I)
            yes = bool(sol.any())
            dist = hyper_dist_bool(I.c, sol)
            acc, info = desc_accepts(I, k, 0, 3 * k, dist)
            assert acc == yes, ("DESC(k,0,3k) vs exact", acc, yes)
            bump(st, "yes" if yes else "no")
            if not yes:
                continue
            e1, _ = desc_emin(I, 1, 0, dist)
            e11, _ = desc_emin(I, 1, 1, dist)
            hist[("emin(1,0)", e1)] += 1
            hist[("emin(1,1)", e11)] += 1
            bmax(st, "emin10_max", e1)
            bmax(st, "emin11_max", e11)
            r, paths = I.shortest_paths_dfs(limit=10)
            assert r is not None
            for Q in paths:
                Q = list(Q)
                check_basic(I, Q, st)
                for T in (0, 1):
                    out = check_theorem_q(I, Q, T, st)
                    hist[("h", out["h"])] += 1
            bmax(st, "c_max", I.c)
            bmax(st, "n_max", I.n)
            # no-variant: delete one or two random non-terminal nodes of the planted path's junctions
            for rep in range(2):
                J = delete_nodes(I, rng, 1 + rep)
                if J is None or not J.p2():
                    continue
                solJ = solutions_np(J)
                yesJ = bool(solJ.any())
                distJ = hyper_dist_bool(J.c, solJ)
                accJ, _ = desc_accepts(J, kq(J.n), 0, 3 * kq(J.n), distJ)
                assert accJ == yesJ, ("DESC(k,0,3k) vs exact on a variant", accJ, yesJ)
                bump(st, "variant_yes" if yesJ else "variant_no")
                if J.c > 3 * kq(J.n):
                    bump(st, "variant_nondegenerate")
        except (ClaimFailure, AssertionError) as ex:
            fails.append({"idx": idx, "err": repr(ex), "inst": I.to_json(), "tb": traceback.format_exc()[-800:]})
            bump(st, "FAIL")
    return st, hist, fails


def main():
    kind, seed, count, workers = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    a = tuple(int(x) for x in sys.argv[5:])
    chunk = max(1, count // (workers * 3))
    jobs = [(kind, seed, lo, min(count, lo + chunk), a) for lo in range(0, count, chunk)]
    tot = {}
    hist = Counter()
    allf = []
    with Pool(workers) as pool:
        for st, h, fails in pool.imap_unordered(run, jobs):
            for key, v in st.items():
                if key.endswith("_max") or key in ("r_max", "W_maxwidth", "nonconsistent_maxwidth"):
                    tot[key] = max(tot.get(key, -1), v)
                else:
                    tot[key] = tot.get(key, 0) + v
            hist.update(h)
            allf.extend(fails)
    print(kind, a, json.dumps(tot, sort_keys=True), flush=True)
    print("histogram:", sorted(hist.items()), flush=True)
    if allf:
        with open("runs/fail-desck-%s-%d.json" % (kind, seed), "w") as fh:
            json.dump(allf[:20], fh)
        print("FAILURES", len(allf), allf[0]["err"], flush=True)


if __name__ == "__main__":
    main()
