#!/usr/bin/env python3
"""The harness with the final constants of the text: margin 6, Shape A up to 4 classes, Shape B with five classes.

Usage: run_final.py SEED ROUNDS LOG. The referee's runs used margin 4 with five classes; this one runs exactly what main.tex states.
"""
import os
import random
import sys
import time
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run_mut import get_inst  # noqa: E402
from zz_proof import ClaimFail, Cfg, Walk, construct  # noqa: E402

FAMILIES = ["kappay", "A", "cross", "stair", "B", "mix", "ties", "two", "margin2", "far2x"]


def main():
    seed, rounds, logf = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    rng = random.Random(seed)
    cfg = Cfg(margin=6, shape_a_max=4)
    exits, fired, st = Counter(), Counter(), Counter()
    runs = dropped = 0
    t0 = time.time()
    for fam in FAMILIES:
        for _ in range(rounds):
            I, P = get_inst(fam, rng)
            I.validate()
            if not I.p2() or I.shortest_walk(bound=len(P) - 1, budget=200000) is not None:
                dropped += 1
                continue
            J = I.reversed_instance()
            for K, Q in ((I, P), (I, P[::-1]), (J, P), (J, P[::-1])):
                for _ in range(3):
                    runs += 1
                    try:
                        exits[construct(Walk(K, Q), cfg, rng, st)] += 1
                    except ClaimFail as e:
                        fired[str(e)] += 1
    with open(logf, "w", encoding="utf-8") as f:
        f.write("final constants: margin 6, Shape A up to 4 classes, Shape B five classes\n")
        f.write("runs %d, instances dropped %d, time %.1f\n" % (runs, dropped, time.time() - t0))
        f.write("exits %s\n" % dict(exits))
        f.write("FAILURES: %s\n" % (dict(fired) if fired else "none"))


if __name__ == "__main__":
    main()
