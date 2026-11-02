"""Experiment E1: how many guessed elements does a walk-based algorithm need?

For a planted instance with its shortest valid walk P we test, for tuples drawn from P, the restricted state graph
    low states: x in ER(b1, b2) minus up(a1, a2) minus up(MA(b1) cap MA(b2))
    high states: x not in FR(a1, a2) and not in dn(b1, b2) and not in dn(MB(a1) cap MB(a2))
and report: the distance in the restricted graph, whether a BFS shortest walk is valid, and the number of conflicts.
All restrictions are consequences of a1, a2, b1, b2 being far pairs of A_P, B_P (lem:pa-one, lem:pa-atoms): P survives.

Usage: e1_guess.py SEED COUNT SAMPLES LOG
"""
import random
import sys
from collections import Counter

from common import BASES, Budget, StateGraph, WData, bits, conflicts, is_valid, popcnt


def restricted(I, A2=None, B2=None):
    LOK, HOK = I.ALL, I.ALL
    if A2 is not None:
        a1, a2 = A2
        HOK &= ~I.FR(a1, a2)
        forced_low = I.dn(I.MB[a1] & I.MB[a2])
        HOK &= ~forced_low
        LOK &= ~(I.UP[a1] | I.UP[a2])
    if B2 is not None:
        b1, b2 = B2
        LOK &= I.ER(b1, b2)
        forced_high = I.up(I.MA[b1] & I.MA[b2])
        LOK &= ~forced_high
        HOK &= ~(I.DN[b1] | I.DN[b2])
    return LOK, HOK


def main():
    seed, count, samples, logf = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    rng = random.Random(seed)
    fams = ["B", "A", "stair", "ties", "small", "mix", "cross", "allstrict", "kappa", "two"]
    with open(logf, "w", encoding="utf-8") as f:
        print("fam m q |A| |B| d0 | best d over samples (A,B far) | valid found | min conflicts | fraction valid", file=f)
        for fam in fams:
            for _ in range(count):
                d = BASES[fam](rng)
                I, P = d.build()
                W = WData(I, P)
                q = len(W.P) - 1
                d0 = StateGraph(I).dist()
                FA, FB = W.far_pairs_A(), W.far_pairs_B()
                # sanity: P survives
                nval, ntot, best, minc = 0, 0, None, None
                for _s in range(samples):
                    A2 = rng.choice(FA) if FA else None
                    B2 = rng.choice(FB) if FB else None
                    LOK, HOK = restricted(I, A2, B2)
                    for i, x in enumerate(W.P):
                        ok = (LOK if i % 2 == 0 else HOK) >> x & 1
                        assert ok, ("P must survive", fam, x)
                    G = StateGraph(I, LOK, HOK)
                    dd = G.dist()
                    best = dd if best is None else max(best, dd)
                    w = G.shortest(rng)
                    ntot += 1
                    c = len(conflicts(I, w))
                    minc = c if minc is None else min(minc, c)
                    if c == 0:
                        nval += 1
                print(fam, I.m, q, len(W.A), len(W.B), d0, best, nval > 0, minc, "%d/%d" % (nval, ntot), file=f, flush=True)


if __name__ == "__main__":
    main()
