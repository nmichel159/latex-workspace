"""Y^d_k and Y'^d_k (fool.py) against HYB with parameters below the bound of Theorem Y(ii), and against the refined
search of r4-general.md Section 6.2 after the same pruning.

For each k and variant: P2, exact answer, number of solutions (k <= 6), switches fixed by gsw.prune, which ones,
then for every parameter set (kd, ks, s, B) in PARS the plain search (gsw.decide) on the pruned copy and, if
`refined` is given, gsw.decide_refined on the pruned copy.
Usage: python test_fool2.py KMIN KMAX [refined]
"""
import sys
import time
from gcore import to_inst
from fool import yd
import gcert
from gsw import GSW, prune, pruned_copy, decide_refined


def main():
    kmin, kmax = int(sys.argv[1]), int(sys.argv[2])
    refined = len(sys.argv) > 3 and sys.argv[3] == "refined"
    for k in range(kmin, kmax + 1):
        # parameter sets strictly below the bound kd + ks + s < k, B < k (and the r4 defaults where they fit)
        pars = [p for p in [(1, 0, 1, 3), (1, 1, 2, 6), (1, 1, 4, 8), (2, 1, 4, 8), (1, 0, 2, 6)]
                if p[0] + p[1] + p[2] < k and p[3] < k]
        for contact in (False, True):
            for back in (False, True):
                t0 = time.time()
                G, nodes = yd(k, back=back, contact=contact)
                I, _ = to_inst(G)
                p2 = I.p2()
                ex = gcert.exact(I)
                nsol = len(G.brute()) if G.m <= 19 else None
                G0 = GSW(I)
                fixed, dead = prune(G0)
                H = pruned_copy(G0, dead)
                res = {}
                for par in pars:
                    res[par] = H.decide(*par)
                    if refined:
                        kd, ks, s, B = par
                        if B <= 3:
                            res[("ref",) + par] = decide_refined(H, kd, ks, s, B)
                fx = sorted(G0.M[w] for w in fixed)
                print("k=%d contact=%s back=%s: q=%d sw=%d P2=%s exact=%s sols=%s fixed=%d %s results=%s %.0fs"
                      % (k, contact, back, I.n, G.m, p2, ex, nsol, len(fixed), fx, res, time.time() - t0),
                      flush=True)


if __name__ == "__main__":
    main()
