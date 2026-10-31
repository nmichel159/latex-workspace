"""W_n (wfam.py) against propagation, Theorem R, HYB and CDESC.

Usage: python test_wfam.py NMIN NMAX [mates|nomates] [F|E|random] [SEED]
"""
import sys
import time
from gcore import to_inst
import cdesc
import gcert
from gsw import GSW, prune, pruned_copy, reduce_to_2ch
from wfam import wfam

HYB = [(1, 0, 1, 3), (1, 1, 2, 6)]


def main():
    nmin, nmax = int(sys.argv[1]), int(sys.argv[2])
    mates = not (len(sys.argv) > 3 and sys.argv[3] == "nomates")
    pairing = sys.argv[4] if len(sys.argv) > 4 else "F"
    seed = int(sys.argv[5]) if len(sys.argv) > 5 else 0
    for n in range(nmin, nmax + 1):
        t0 = time.time()
        G, nodes = wfam(n, mates=mates, pairing=pairing, seed=seed)
        I, _ = to_inst(G)
        p2 = I.p2()
        L, path = G.shortest()
        nsol = len(G.brute()) if G.m <= 20 else None
        paths = G.all_shortest(limit=400, length=L) if L else []
        G0 = GSW(I)
        fixed, dead = prune(G0)
        inst, free, reason = reduce_to_2ch(G0, fixed) if dead is not None else (None, None, "refuted")
        hyb = {}
        if dead is not None:
            H = pruned_copy(G0, dead)
            for par in HYB:
                hyb[par] = H.decide(*par)
                if hyb[par]:
                    break
        cs = (cdesc.centre_sets(G, 0), cdesc.centre_sets(G, 1))
        best = {}
        for P in paths:
            g = cdesc.guided(G, P, 2 if G.m <= 40 else 1, cs=cs)
            for f, v in g.items():
                if f not in best or v[0] < best[f][0]:
                    best[f] = v
        dec = None
        if G.m <= 34:
            dec = cdesc.decide(G, 1, 1)
        print("n=%d mates=%s: m=%d N=%d P2=%s shortest=%s #shortest=%d #sol=%s fixed=%d R=%s HYB=%s "
              "CDESC guided=%s decide(1,1)=%s %.0fs"
              % (n, mates, G.m, G.N, p2, L, len(paths), nsol, len(fixed), reason, hyb,
                 {f: v[:2] for f, v in best.items()}, dec, time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
