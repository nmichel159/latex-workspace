"""Exercise the swap branch (Lemma 7) and the bad case of Theorem 8: saturated planted instances (saturate.py) into
which straddle configurations are inserted (new nodes in X'_p & X_{r-1}, X'_p & X_{r+1}, X'_r & X_{p-1},
X'_r & X_{p+1} for a T-member r and an O-member p), kept only if the planted path stays a shortest valid path; then
prove.certificate is run on every shortest valid path, and alg.decide (kd=1, ks=0, s=4, B=8) is compared with the
exact answer.  Usage: python straddle_hunt.py SEED COUNT LMIN LMAX"""
import sys
import random
import time

import sw
import alg
import saturate
from test_prove import run_one

seed, count, lmin, lmax = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
rng = random.Random(seed)
stats = dict(yes=0, no=0, paths=0, fail=0, maxdom=0, maxsing=0, maxstore=0)
algstat = {}
t0 = time.time()
for it in range(count):
    L = rng.randint(lmin, lmax)
    word = "".join(rng.choice("EF") for _ in range(L))
    inst, P = saturate.saturate(rng, word, 0.3)
    if inst is None:
        continue
    r = len(P)
    for attempt in range(6):
        a = rng.randrange(1, r - 1)
        p = rng.randrange(1, r - 1)
        if abs(a - p) < 4 or (P[a] & 1) == (P[p] & 1):
            continue
        inst2 = inst
        for (x, y) in ((P[p] ^ 1, P[a - 1]), (P[p] ^ 1, P[a + 1]), (P[a] ^ 1, P[p - 1]), (P[a] ^ 1, P[p + 1])):
            if not (sw.side_mask(inst2, x) & sw.side_mask(inst2, y)):
                inst2 = saturate.add_node(inst2, x, y)
        Ls = saturate.shortest_len(inst2, r)
        if Ls is not None and Ls < r:
            continue
        inst = inst2
    run_one(inst, stats, word)
    ex = sw.brute(inst) is not None if len(inst[1]) <= 16 else sw.exact(inst)
    an = alg.decide(inst, 1, 0, 4, 8)
    algstat[(ex, an)] = algstat.get((ex, an), 0) + 1
    if ex != an:
        print("ALG MISMATCH", ex, an, sw.fmt(inst), flush=True)
print("seed", seed, stats, "alg (exact, decide):", algstat, "%.1fs" % (time.time() - t0), flush=True)
