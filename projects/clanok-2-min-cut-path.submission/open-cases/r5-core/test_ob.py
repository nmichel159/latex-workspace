"""Family OB (obfam.py) against propagation, Theorem R, HYB, CDESC and ADESC.

Usage: python test_ob.py K M K2 k sz [back|noback] [mates|nomates] [nodecide]
"""
import sys
import time
from gcore import to_inst
import cdesc
import adesc
from gsw import GSW, prune, pruned_copy, reduce_to_2ch
from obfam import ob


def main():
    K, M, K2, k, sz = (int(a) for a in sys.argv[1:6])
    back = not (len(sys.argv) > 6 and sys.argv[6] == "noback")
    mates = not (len(sys.argv) > 7 and sys.argv[7] == "nomates")
    dodec = not (len(sys.argv) > 8 and sys.argv[8] == "nodecide")
    t0 = time.time()
    pl, info = ob(K, M, K2, k, sz, back=back, mates=mates)
    G, P = pl.realise()
    bad = G.p2_bad()
    valid = G.is_valid_walk(P)
    L, path = G.shortest()
    print("OB K=%d M=%d K2=%d k=%d sz=%d back=%s mates=%s: m=%d N=%d P2-bad=%d planted valid=%s len=%d shortest=%s"
          % (K, M, K2, k, sz, back, mates, G.m, G.N, len(bad), valid, len(P), L), flush=True)
    if bad:
        print("  P2 failures:", bad[:10])
    paths = G.all_shortest(limit=200, length=L) if L else []
    print("  #shortest (<=200): %d; planted among them: %s; a shortest: %s" %
          (len(paths), P in paths, path), flush=True)
    nsol = None
    if G.m <= 22:
        nsol = len(G.brute())
    I, _ = to_inst(G)
    G0 = GSW(I)
    fixed, dead = prune(G0)
    if dead is None:
        print("  propagation refutes (no solution)")
        return
    inst, free, reason = reduce_to_2ch(G0, fixed)
    print("  #solutions=%s; propagation fixes %d of %d; Theorem R: %s  (%.0fs)" %
          (nsol, len(fixed), G.m, reason, time.time() - t0), flush=True)
    H = pruned_copy(G0, dead)
    for par in [(1, 0, 1, 3), (1, 1, 2, 6)]:
        r = H.decide(*par)
        print("  HYB%s = %s (%.0fs)" % (par, r, time.time() - t0), flush=True)
        if r:
            break
    cs = (cdesc.centre_sets(G, 0), cdesc.centre_sets(G, 1))
    bestc = {}
    besta = None
    for Pp in paths[:60]:
        g = cdesc.guided(G, Pp, 1, cs=cs)
        for f, v in g.items():
            if f not in bestc or v[0] < bestc[f][0]:
                bestc[f] = v
        ga = adesc.guided(G, Pp, fmax=2, amax=2, cs=cs)
        if besta is None or ga[0] < besta[0]:
            besta = ga
    print("  CDESC guided (flips with f centres): %s" % {f: v[:2] for f, v in bestc.items()}, flush=True)
    print("  ADESC guided least total parameters: %s  (%.0fs)" % (besta[:2] if besta else None, time.time() - t0),
          flush=True)
    if dodec and G.m <= 40:
        r = cdesc.decide(G, 1, 1)
        print("  CDESC decide(1,1) = %s (%.0fs)" % (r, time.time() - t0), flush=True)
        r = adesc.decide(G, fmax=1, amax=1, emax=0)
        print("  ADESC decide(f=1,a=1,e=0) = %s (%.0fs)" % (r, time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
