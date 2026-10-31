"""Certificate-guided check (as test_guided.py) on saturated planted instances of length LMIN..LMAX only, with the
swap preferred.  Usage: python guided_sat.py SEED COUNT LMIN LMAX"""
import sys
import random
import time
import sw
import prove
import tsearch
import saturate

seed, count, lmin, lmax = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
rng = random.Random(seed)
st = dict(inst=0, paths=0, ok=0, fail=0, swaps=0, bad=0, maxstore=0)
t0 = time.time()
for it in range(count):
    L = rng.randint(lmin, lmax)
    word = "".join(rng.choice("EF") for _ in range(L))
    inst, P0 = saturate.saturate(rng, word, 0.3)
    if inst is None:
        continue
    st["inst"] += 1
    Ls, paths = sw.shortest_valid_paths(inst, limit=40)
    for P in paths:
        st["paths"] += 1
        for pref in (False, True):
            try:
                Pu, certs, storage, info = prove.certificate(inst, list(P), prefer_swap=pref)
            except AssertionError as e:
                st["fail"] += 1
                print("PROOF STEP FAILED", repr(e), sw.fmt(inst), P, flush=True)
                continue
            if info.startswith("swap"):
                st["swaps"] += 1
            if "rows" in info:
                st["bad"] += 1
            K = set()
            for T in (0, 1):
                K |= prove.build_K(inst, certs[T][0], certs[T][1], 1 - T)
            ok, walk = tsearch.admissible_search(inst, frozenset(K), storage, True)
            if ok and sw.is_valid_walk(inst, walk):
                st["ok"] += 1
                st["maxstore"] = max(st["maxstore"], storage)
            else:
                st["fail"] += 1
                print("GUIDED SEARCH FAILED", sw.fmt(inst), P, flush=True)
print("seed", seed, "L", lmin, lmax, st, "%.1fs" % (time.time() - t0), flush=True)
