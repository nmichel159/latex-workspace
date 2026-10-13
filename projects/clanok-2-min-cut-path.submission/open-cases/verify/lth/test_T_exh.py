"""Exhaustive check of Theorem T (and of the t = 1 search of Theorem H) on all small TIC + P2 instances
(agent verify-LTH). All multisets of n switches over the line 0..K, every side a span (l <= r, length 0 allowed) or
empty, not both empty; only P2 instances are compared (algorithm answer = brute force).
Usage: python test_T_exh.py <K> <n> [procs]"""
import sys
import itertools
import time
from multiprocessing import Pool

sys.path.insert(0, __file__.rsplit("/", 1)[0] if "/" in __file__ else ".")
from core import *


def options(K):
    spans = [(l, r) for l in range(K + 1) for r in range(l, K + 1)] + [None]
    return [(E, F) for E in spans for F in spans if not (E is None and F is None)]


def job(args):
    K, n, first = args
    opts = options(K)
    st = {"inst": 0, "yes": 0, "relax_yes_no": 0, "viol": 0}
    bad = []
    for rest in itertools.combinations_with_replacement(range(first, len(opts)), n - 1):
        sw = [opts[first]] + [opts[i] for i in rest]
        if not p2_tic(sw):
            continue
        st["inst"] += 1
        ans, _ = brute_tic(K, sw)
        st["yes"] += ans
        if not ans and relaxation_2ch(tic_to_2ch(K, sw)):
            st["relax_yes_no"] += 1
        T = tic_T(K, sw)
        H = h_search(tic_to_2ch(K, sw), 1)
        if T != ans or H != ans:
            st["viol"] += 1
            bad.append((K, sw, ans, T, H))
    return st, bad


if __name__ == "__main__":
    K, n = int(sys.argv[1]), int(sys.argv[2])
    procs = int(sys.argv[3]) if len(sys.argv) > 3 else 8
    opts = options(K)
    t0 = time.time()
    tot = {}
    allbad = []
    with Pool(min(procs, 8)) as pool:
        for st, bad in pool.imap_unordered(job, [(K, n, f) for f in range(len(opts))]):
            for k, x in st.items():
                tot[k] = tot.get(k, 0) + x
            allbad += bad
    with open("results-T-exh-K%d-n%d.txt" % (K, n), "w") as out:
        out.write("K=%d n=%d switch options %d: %s (%.0fs)\n" % (K, n, len(opts), tot, time.time() - t0))
        for b in allbad[:50]:
            out.write("BAD %r\n" % (b,))
        out.write("violations: %d\n" % tot.get("viol", 0))
    print("K=%d n=%d" % (K, n), tot, "%.0fs" % (time.time() - t0))
