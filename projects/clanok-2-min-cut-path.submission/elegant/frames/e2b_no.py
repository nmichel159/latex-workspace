"""E2b: tree size of the conflict-driven branching on no-instances: a planted instance with one edge of P removed (checked to be a no-instance by the exact solver when it finishes),
and the yes-instance with the opposite child order.

Usage: e2b_no.py SEED COUNT LIMIT LOG
"""
import random
import sys
import time

from common import BASES, Budget, Inst, StateGraph, WData, bits, conflicts, popcnt
from e2_branch import search


def strip_edge(I, a, b):
    return Inst(I.m, list(I.UP), set(I.edges) - {(a, b)}, I.u, I.v, I.names)


def main():
    sys.setrecursionlimit(100000)
    seed, count, limit, logf = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    rng = random.Random(seed)
    fams = ["small", "B", "A", "stair", "ties", "mix", "cross", "allstrict", "kappa", "two"]
    with open(logf, "w", encoding="utf-8") as f:
        print("fam m q removed-pos p2 exact | result nodes depth", file=f)
        for fam in fams:
            for _ in range(count):
                d = BASES[fam](rng)
                I, P = d.build()
                W = WData(I, P)
                P = W.P
                for trial in range(3):
                    i = rng.randrange(len(P) - 1)
                    a, b = (P[i], P[i + 1]) if i % 2 == 0 else (P[i + 1], P[i])
                    J = strip_edge(I, a, b)
                    t0 = time.time()
                    r, n, dep = search(J, limit, "min", None, "first")
                    t1 = time.time()
                    status = "V" if isinstance(r, list) else r
                    print(fam, I.m, len(P) - 1, i, J.p2(), "|", status, n, dep, round(t1 - t0, 1), file=f, flush=True)


if __name__ == "__main__":
    main()
