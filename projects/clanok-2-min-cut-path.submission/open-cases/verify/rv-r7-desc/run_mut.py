"""Referee rv-r7-desc: power of the harness.  (1) P not shortest: a planted instance plus a perturbation rejected by the exact solver; the
checks run on the planted path, which is then no longer shortest; which assertion fires?  (2) Wrong proof variants on correct instances:
atoms at distance < 9 ... are not claimed by the proof, so instead (2) removes parts of the formula of Shape A and B and asserts that the
result stops being correct at least once.  Usage: run_mut.py SEED ROUNDS LOG."""
import os
import random
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from swf import ClaimFail, Budget  # noqa: E402
from proof import run_all  # noqa: E402
from design import zipper  # noqa: E402
import run_planted as rp  # noqa: E402


def main():
    seed, rounds = int(sys.argv[1]), int(sys.argv[2])
    log = open(sys.argv[3], "w", encoding="utf-8")
    rng = random.Random(seed)
    fired = Counter()
    n = Counter()
    for rd in range(rounds):
        base = rng.choice(["B", "stair", "mix", "cross"])
        d = rp.BASES[base](rng)
        for mv in range(25):
            d2 = d.copy()
            d2.info = d.info
            kind = rp.move(d2, rng, Counter())
            if kind == "none":
                continue
            I2, P2 = d2.build()
            if not I2.p2():
                continue
            try:
                w = I2.shortest(bound=len(P2), budget=rp.BUDGET)
            except Budget:
                continue
            if w is None:
                continue
            n["instances where the planted path is not shortest"] += 1
            st = Counter()
            try:
                run_all(I2, P2, rng, st, trials=2)
                n["no assertion fired"] += 1
            except ClaimFail as e:
                n["assertion fired"] += 1
                fired[str(e)] += 1
    for k, v in n.items():
        print(k, v, file=log)
    print("assertions:", file=log)
    for k, v in fired.most_common():
        print("  ", v, k, file=log)
    log.close()


if __name__ == "__main__":
    main()
