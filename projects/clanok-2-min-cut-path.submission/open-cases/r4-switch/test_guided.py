"""Certificate-guided check of Theorem 10: for every yes-instance and every shortest valid path P, build the
certificate of the proof (prove.certificate: Lemma 7 or Theorem 8), and run the plain search of Theorem 5
(tsearch.admissible_search) with exactly that K and B = its storage: it must accept, with a valid walk.
For every no-instance, the generic algorithm alg.decide(kd=1, ks=1, s=4, B=8) must answer no (soundness).
Families as in test_alg.py plus saturated instances.  Usage: python test_guided.py SEED COUNT"""
import sys
import random
import time

import sw
import prove
import tsearch
import alg
import saturate
import gen
from test_prove import A14, A18, gen_instance

seed, count = int(sys.argv[1]), int(sys.argv[2])
PREFER = len(sys.argv) > 3 and sys.argv[3] == 'swap'
rng = random.Random(seed)
st = dict(yes=0, no=0, paths=0, guided_ok=0, guided_fail=0, unsound=0, maxstore=0, swaps=0)
t0 = time.time()


def check(inst, label):
    ex = (sw.brute(inst) is not None) if len(inst[1]) <= 16 else sw.exact(inst)
    if not ex:
        st["no"] += 1
        if alg.decide(inst, 1, 1, 4, 8):
            st["unsound"] += 1
            print("UNSOUND", label, sw.fmt(inst), flush=True)
        return
    st["yes"] += 1
    L, paths = sw.shortest_valid_paths(inst, limit=60)
    for P in paths:
        st["paths"] += 1
        try:
            Pu, certs, storage, info = prove.certificate(inst, list(P), prefer_swap=PREFER)
        except AssertionError as e:
            st["guided_fail"] += 1
            print("PROOF STEP FAILED", label, repr(e), sw.fmt(inst), P, flush=True)
            continue
        if info.startswith("swap"):
            st["swaps"] += 1
        K = set()
        for T in (0, 1):
            K |= prove.build_K(inst, certs[T][0], certs[T][1], 1 - T)
        ok, walk = tsearch.admissible_search(inst, frozenset(K), storage, True)
        if ok and sw.is_valid_walk(inst, walk):
            st["guided_ok"] += 1
            st["maxstore"] = max(st["maxstore"], storage)
        else:
            st["guided_fail"] += 1
            print("GUIDED SEARCH FAILED", label, sw.fmt(inst), P, certs, flush=True)


for L in range(2, 10):
    for lab, inst in gen.rigid_variants(L):
        check(inst, lab + str(L))
for base in (A14, A18):
    check(tuple(base), "A")
for it in range(count):
    m = ["random", "repair", "planted", "saturated"][it % 4]
    if m == "saturated":
        Lw = rng.randint(6, 12)
        word = "".join(rng.choice("EF") for _ in range(Lw))
        inst, P = saturate.saturate(rng, word, 0.3)
        if inst is None:
            continue
    else:
        inst = gen_instance(rng, m)
        if len(inst[1]) > 12:
            continue
    check(inst, m)
print("seed", seed, "count", count, st, "%.1fs" % (time.time() - t0), flush=True)
