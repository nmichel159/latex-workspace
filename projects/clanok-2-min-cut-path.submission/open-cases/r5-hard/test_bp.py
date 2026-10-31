"""Checks of the family BP_n (route R1): P2, solutions, shortest valid paths, bad pairs, cheap-tool cover numbers,
Proposition M costs, and GDESC (r5-core/gdesc.decide) with small parameters.
Usage: python test_bp.py NMIN NMAX [k a e]"""
import sys
import time
import hlib
from hlib import bits, popcount
import gdesc
from gstar import Stars, Skel
from bpfam import bp


def main():
    nmin, nmax = int(sys.argv[1]), int(sys.argv[2])
    k, a, e = (int(x) for x in sys.argv[3:6]) if len(sys.argv) > 5 else (1, 1, 1)
    for n in range(nmin, nmax + 1):
        G = bp(n)
        print("== BP_%d" % n)
        t0 = time.time()
        rep = hlib.analyse(G, maxpaths=20)
        # Proposition M description, explicit, on the first shortest path
        length, P = G.shortest()
        S, K = Stars(G), Skel(G, P)
        best = None
        for kind in (1, 0):
            mem = bits(K.A) if kind == 1 else bits(K.B)
            for i, a1 in enumerate(mem):
                for a2 in mem[i + 1:]:
                    if abs(K.pos[a1] - K.pos[a2]) < 9:
                        continue
                    D = hlib.describe_M(G, S, K, a1, a2, kind)
                    ok = gdesc.picks(G, K, D) and G.connects(D)
                    fl = popcount((S.NFstar[a1] | S.NFstar[a2]) & K.B) if kind == 1 else \
                        popcount((S.NEstar[a1] | S.NEstar[a2]) & K.A)
                    if not ok:
                        print("  PROP-M FAILURE kind %d pair %s %s" % (kind, G.names[a1], G.names[a2]))
                    if best is None or fl < best[0]:
                        best = (fl, kind, G.names[a1], G.names[a2], ok)
        print("  Prop. M best (flips, kind, members, picks P): %s" % (best,))
        r = gdesc.decide(G, k=k, a=a, e=e, St=S, want=True)
        if r[0]:
            kind, T, flags, Y0, Phi, D = r[1]
            print("  GDESC(k=%d,a=%d,e=%d) accepts: kind %d tools %s flags %s anchors %s flips %s" %
                  (k, a, e, kind, [G.names[x] for x in T], [G.names[x] for x in flags],
                   [G.names[x] for x in Y0], [G.names[x] for x in Phi]))
        else:
            print("  GDESC(k=%d,a=%d,e=%d) rejects" % (k, a, e))
        print("  time %.1fs" % (time.time() - t0))
        sys.stdout.flush()


if __name__ == "__main__":
    main()
