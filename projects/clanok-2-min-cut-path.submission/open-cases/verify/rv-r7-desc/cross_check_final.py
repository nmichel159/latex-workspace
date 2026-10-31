"""Referee rv-r7-desc: the one separated final cross-check with the author's code (r7-desc/check_b.py, reviewed zzl.py), on the referee's planted instances.
Nothing else of the referee's code imports this file.  Usage: cross_check_final.py SEED ROUNDS LOG."""
import os
import random
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
OC = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
sys.path.append(os.path.join(OC, "verify", "rv-r6-core"))
sys.path.append(os.path.join(OC, "r7-desc"))
import run_planted as rp  # noqa: E402
from proof import run_all  # noqa: E402
from zzl import SW  # noqa: E402
from check_b import run_path, shortest_len  # noqa: E402


def to_sw(I):
    return SW(I.m, I.le, I.E, I.F, I.s, I.t, I.nn, I.me)


def main():
    seed, rounds = int(sys.argv[1]), int(sys.argv[2])
    log = open(sys.argv[3], "w", encoding="utf-8")
    rng = random.Random(seed)
    theirs = Counter()
    mine = Counter()
    for rd in range(rounds):
        for base in ("B", "A", "stair", "ties", "mix", "small", "cross", "allstrict"):
            d = rp.BASES[base](rng)
            I, P = d.build()
            assert I.p2()
            w = I.shortest(bound=len(P) + 1, budget=rp.BUDGET)
            assert w is not None and len(w) == len(P), "planted path not shortest (own solver): " + base
            J = to_sw(I)
            Q = [(x >> 1, x & 1) for x in P]
            L2 = shortest_len(J, len(P) + 1, cap=rp.BUDGET)
            print(base, "m", I.m, "r", len(P), "author's shortest_len:", L2, file=log, flush=True)
            run_path(J, Q, theirs)
            run_all(I, P, rng, mine, trials=1, extended=False)
    print("author's counters:", file=log)
    for k in sorted(theirs):
        print("  ", k, theirs[k], file=log)
    print("referee's counters:", file=log)
    for k in sorted(mine):
        if k[:2] in ("S0", "S1", "Ca", "Sh", "Or", "pa"):
            print("  ", k, mine[k], file=log)
    log.close()


if __name__ == "__main__":
    main()
