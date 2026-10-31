"""Acceptance rate of the incremental generator for structured words (development helper).
usage: python try_inc.py SEED COUNT r nTc nOc mates offc wordkind"""
import random
import sys
import time

from qcore import kq
from qgen2 import incremental


def word_of(rng, r, kind, T=0):
    O = 1 - T
    if kind == "rand":
        return [rng.randrange(2) for _ in range(r)]
    if kind == "zones":
        k = rng.randint(1, max(1, r // 3))
        m = rng.randint(1, max(1, r // 3))
        w = [O if rng.random() < 0.75 else T for _ in range(k)] + [T] * m
        w += [O if rng.random() < 0.75 else T for _ in range(r - len(w))]
        return w[:r]
    if kind == "blocks":
        w = []
        while len(w) < r:
            w += [rng.randrange(2)] * rng.randint(2, 4)
        return w[:r]
    raise ValueError(kind)


def main():
    seed, count, r, nTc, nOc, mates, offc = map(int, sys.argv[1:8])
    kind = sys.argv[8]
    rng = random.Random(seed)
    acc = 0
    t0 = time.time()
    cs = []
    for it in range(count):
        w = word_of(rng, r, kind)
        out = incremental(rng, r, nTc, nOc, mates=mates, offc=offc, word=w)
        if out:
            acc += 1
            I, P = out
            cs.append((I.c, I.n, kq(I.n)))
    print("accepted", acc, "of", count, "time %.1f" % (time.time() - t0), cs[:10])


if __name__ == "__main__":
    main()
