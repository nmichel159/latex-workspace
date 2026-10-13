"""Theorem H with t = 2 (agent verify-LTH): on yes-instances where the t = 1 search fails, compute need (min over
solutions and shortest sequences of the largest group piercing number); the t = 2 search must succeed when
need <= 2. Soundness of t = 2 on a sample of no-instances. Small node counts (the guesses are N^8).
Usage: python test_H2.py <tag> <base seed> <instances per job> <jobs> [procs]"""
import sys
import random
import time
from multiprocessing import Pool

sys.path.insert(0, __file__.rsplit("/", 1)[0] if "/" in __file__ else ".")
from core import *
from test_H import need_value


def job(args):
    seed, count = args
    rng = random.Random(seed)
    st = {"n": 0, "yes": 0, "t1_miss": 0, "need2": 0, "need_gt2": 0, "t2_found": 0, "t2_incomplete": 0,
          "t2_sound_runs": 0, "t2_unsound": 0}
    bad = []
    for _ in range(count):
        N = rng.randint(4, 5); n = rng.randint(4, 8)
        inst = rand_2ch(rng, N, n, dens=rng.choice([0.2, 0.3]), p_empty=0.1, p2=True)
        ok, sols = brute_2ch(inst, all_solutions=True)
        st["n"] += 1; st["yes"] += ok
        if not ok:
            if rng.random() < 0.15:
                st["t2_sound_runs"] += 1
                if h_search(inst, 2):
                    st["t2_unsound"] += 1; bad.append(("unsound-t2", inst))
            continue
        if h_search(inst, 1):
            continue
        st["t1_miss"] += 1
        nv = need_value(inst, sols)
        H2, wit = h_search(inst, 2, want_witness=True)
        if H2:
            st["t2_found"] += 1
            if not walk_is_consistent(inst, wit[1]):
                bad.append(("badcert", inst, wit))
        if nv <= 2:
            st["need2"] += 1
            if not H2:
                st["t2_incomplete"] += 1; bad.append(("incomplete-t2", inst, nv))
        else:
            st["need_gt2"] += 1
    return seed, st, bad


if __name__ == "__main__":
    tag, base, count, jobs = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    procs = int(sys.argv[5]) if len(sys.argv) > 5 else 8
    t0 = time.time()
    tot = {}
    out = open("results-H2-%s.txt" % tag, "w")
    with Pool(min(procs, 8)) as pool:
        for seed, st, bad in pool.imap_unordered(job, [(base + j, count) for j in range(jobs)]):
            for k, x in st.items():
                tot[k] = tot.get(k, 0) + x
            out.write("seed %d: %s\n" % (seed, st))
            for b in bad:
                out.write("  BAD %r\n" % (b,))
            out.flush()
            print(seed, st, flush=True)
    viol = tot.get("t2_incomplete", 0) + tot.get("t2_unsound", 0)
    out.write("\nTOTALS (%.0fs): %s\nviolations: %d\n" % (time.time() - t0, tot, viol))
    out.close()
    print(tot, "violations:", viol)
