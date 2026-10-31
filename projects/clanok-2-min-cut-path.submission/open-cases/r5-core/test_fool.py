"""Y^d_k (fool.py) against the hybrid algorithm HYB of r4-general (gsw.prune + gsw.decide, read-only).

For k = KMIN..KMAX and both variants (back = False / True): P2 of the ZZ form (gcert.Inst.p2), exact answer
(gcert.exact), number of solutions (Gen.brute, if at most 22 switches), switches fixed by gsw.prune, and the plain
search of Theorem 5' on the pruned copy with a ladder of parameters.
Usage: python test_fool.py KMIN KMAX
"""
import sys
import time
import gcore
from gcore import to_inst
from fool import yd
import gcert
from gsw import GSW, prune, pruned_copy

LADDER = [(1, 0, 1, 3), (1, 1, 2, 6), (1, 1, 4, 8), (2, 1, 4, 8)]


def main():
    kmin, kmax = int(sys.argv[1]), int(sys.argv[2])
    for k in range(kmin, kmax + 1):
        for back in (False, True):
            for gadget in (False, True):
                t0 = time.time()
                G, nodes = yd(k, back=back, gadget=gadget)
                I, _ = to_inst(G)
                p2 = I.p2()
                ex = gcert.exact(I)
                nsol = len(G.brute()) if G.m <= 22 else None
                G0 = GSW(I)
                fixed, dead = prune(G0)
                res = {}
                if dead is not None:
                    H = pruned_copy(G0, dead)
                    for par in LADDER:
                        if k >= 6 and par[3] > 6:
                            res[par] = "skip"
                            continue
                        res[par] = H.decide(*par)
                        if res[par]:
                            break
                print("k=%d back=%s gadget=%s: q=%d switches=%d P2=%s exact=%s solutions=%s fixed=%d/%d HYB=%s %.0fs"
                      % (k, back, gadget, I.n, G.m, p2, ex, nsol, len(fixed), G0.m, res, time.time() - t0),
                      flush=True)


if __name__ == "__main__":
    main()
