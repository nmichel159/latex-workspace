"""decide_full (Theorem 10 parameters) against brute force on small random P2 instances (k_unions deduplicates, so
the enumeration is over distinct side sets and stays small for few switches).  Usage: python test_full.py SEED COUNT NMAX"""
import sys
import random
import time
import sw
import alg

seed, count, nmax = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
rng = random.Random(seed)
st = {}
t0 = time.time()
for it in range(count):
    inst = sw.random_p2_instance(rng, rng.randint(3, 6), rng.randint(2, nmax), rng.uniform(0.1, 0.45), rng.uniform(0.1, 0.45))
    ex = sw.brute(inst) is not None
    a = alg.decide_full(inst)
    st[(ex, a)] = st.get((ex, a), 0) + 1
    if ex != a:
        print("MISMATCH", sw.fmt(inst), flush=True)
print("seed", seed, "count", count, "nmax", nmax, "(exact, decide_full):", st, "%.1fs" % (time.time() - t0))
