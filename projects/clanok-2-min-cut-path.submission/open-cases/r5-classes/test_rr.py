"""DESC costs on round-robin families (rrfam.build) of growing size (agent r5-classes).

usage: python test_rr.py WORD R SEEDS MODE PBOTH [solve]
prints P2, shortest, number of solutions (brute force, if solve and at most 18 classes), h2, guided DESC costs
(1,0), (1,1), (2,0) with side centres only, and the exact least DESC(1,1) cost over all solutions when solved.
"""
import sys
import itertools
import ccore as C
import costs
import rrfam
import cdesc2


def main():
    W = sys.argv[1]
    R = int(sys.argv[2])
    seeds = int(sys.argv[3])
    mode = sys.argv[4]
    pboth = float(sys.argv[5])
    solve = len(sys.argv) > 6 and sys.argv[6] == "solve"
    for sd in range(1, seeds + 1):
        pl = rrfam.build(W, R, sd, pboth=pboth, mode=mode)
        I, P = pl.realise()
        p2 = C.p2_ok(I)
        sh = pl.shortest_ok(I, P)
        g10 = costs.desc_guided(I, P, 1, 0, nodes=False)
        g11 = costs.desc_guided(I, P, 1, 1, nodes=False)
        g20 = costs.desc_guided(I, P, 2, 0, nodes=False)
        line = "W=%s R=%d seed=%d mode=%s P2=%s shortest=%s classes=%d sides=%d h2=%d g(1,0)=%s g(1,1)=%s g(2,0)=%s" % (
            W, R, sd, mode, p2, sh, I.k, len(I.sides), costs.h2(I, P), g10, g11, g20)
        if solve and I.k <= 18:
            sols = cdesc2.solutions_masks(I)
            line += " nsol=%d exact(1,1)=%s" % (len(sols), cdesc2.desc_cost(I, 1, 1, sols))
        print(line, flush=True)


if __name__ == "__main__":
    main()
