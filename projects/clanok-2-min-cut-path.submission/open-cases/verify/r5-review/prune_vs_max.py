"""Observation: how often the own pruning (r4-general §7.3) reaches the maximal sound fixing (the modes common to all
solutions), on random abstract switch forms and random ZZ + P2 instances.  Usage: python prune_vs_max.py SEED COUNT"""
import random
import sys
from gswlib import random_abstract, random_zz_p2, from_zz


def main():
    seed, count = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    for mode in ("abs", "zz"):
        eq = neq = 0
        for it in range(count):
            if mode == "abs":
                G = random_abstract(rng, rng.randint(3, 7), rng.randint(3, 9), rng.choice((0.2, 0.35, 0.5)),
                                    rng.choice((0.1, 0.3, 0.5)), rng.choice((0.0, 0.3)))
            else:
                I = random_zz_p2(rng, rng.randint(4, 10), rng.randint(0, 3), rng.randint(0, 3),
                                 rng.choice((0.1, 0.25, 0.4)), rng.choice((0.0, 0.2, 0.5)), rng.choice((0.15, 0.3)))
                if I is None:
                    continue
                G = from_zz(I)
            sols = G.solutions()
            if not sols:
                continue
            fmax = {z: sols[0][z] for z in range(G.m) if all(s[z] == sols[0][z] for s in sols)}
            f, st = G.prune()
            if f == fmax:
                eq += 1
            else:
                neq += 1
        print("%s seed %d: yes-instances %d, pruning = maximal sound fixing in %d, smaller in %d" % (
            mode, seed, eq + neq, eq, neq))


if __name__ == "__main__":
    main()
