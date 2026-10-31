"""Exhaustive check on all 2CH + P2 instances with N nodes (s = 0, t = 1) and n switches (every side any subset of
the nodes, including empty and equal sides): for every yes-instance and every shortest valid path, the proof's
certificate (prove.certificate, with and without preferring swaps) is accepted by the plain search; for every
no-instance, alg.decide(1, 1, 4, 8) answers no.  Usage: python exhaustive.py N n"""
import sys
import itertools
import time
import sw
import prove
import tsearch
import alg

N, n = int(sys.argv[1]), int(sys.argv[2])
st = dict(total=0, p2=0, yes=0, no=0, paths=0, ok=0, fail=0, unsound=0, swaps=0)
t0 = time.time()
for sides in itertools.product(range(1 << N), repeat=2 * n):
    E = list(sides[:n])
    F = list(sides[n:])
    # symmetry: switches sorted by (E, F)
    pairs = list(zip(E, F))
    if pairs != sorted(pairs):
        continue
    st["total"] += 1
    inst = (N, E, F, 0, 1)
    if not sw.p2_ok(inst):
        continue
    st["p2"] += 1
    ex = sw.brute(inst) is not None
    if not ex:
        st["no"] += 1
        if alg.decide(inst, 1, 1, 4, 8):
            st["unsound"] += 1
            print("UNSOUND", sw.fmt(inst), flush=True)
        continue
    st["yes"] += 1
    L, paths = sw.shortest_valid_paths(inst)
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
            K = set()
            for T in (0, 1):
                K |= prove.build_K(inst, certs[T][0], certs[T][1], 1 - T)
            ok, walk = tsearch.admissible_search(inst, frozenset(K), storage, True)
            if ok and sw.is_valid_walk(inst, walk):
                st["ok"] += 1
            else:
                st["fail"] += 1
                print("GUIDED FAILED", sw.fmt(inst), P, flush=True)
print("N", N, "n", n, st, "%.1fs" % (time.time() - t0), flush=True)
