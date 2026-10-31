"""alg.decide (kd=1, ks=1, s=4, B=8) and the certificate of the proof on R_L for larger L, plus all one-node
no-variants and t-flip variants keeping P2 (exact answers by sw.exact).  Usage: python rigid_big.py LMIN LMAX"""
import sys
import time
import sw
import gen
import alg
import prove
import tsearch

lmin, lmax = int(sys.argv[1]), int(sys.argv[2])
for L in range(lmin, lmax + 1):
    t0 = time.time()
    cnt = {}
    for lab, inst in gen.rigid_variants(L):
        ex = sw.exact(inst)
        a = alg.decide(inst, 1, 1, 4, 8)
        g = None
        if ex:
            Ls, paths = sw.shortest_valid_paths(inst, limit=5)
            Pu, certs, storage, info = prove.certificate(inst, list(paths[0]))
            K = set()
            for T in (0, 1):
                K |= prove.build_K(inst, certs[T][0], certs[T][1], 1 - T)
            g = tsearch.admissible_search(inst, frozenset(K), storage)
        key = (lab, ex, a, g)
        cnt[key] = cnt.get(key, 0) + 1
    print("L=%d" % L, cnt, "%.1fs" % (time.time() - t0), flush=True)
