"""Smoke test: zipper design; four transforms; stages reached."""
import random
import sys
import time
from collections import Counter

from swf import ClaimFail
from design import zipper
from proof import run_all
from swf import path_rev, path_op


def go(d, st, rng, trials=3):
    I, P = d.build()
    I.validate()
    assert I.p2(), "P2"
    t0 = time.time()
    w = I.shortest()
    t1 = time.time()
    print("m", I.m, "r", len(P), "shortest", len(w), "t", round(t1 - t0, 3))
    assert len(w) == len(P), "not shortest"
    for name, J, Q in (("id", I, P), ("rev", I.reversed_st(), path_rev(P)), ("op", I.op(), path_op(P)),
                       ("oprev", I.op().reversed_st(), path_rev(path_op(P)))):
        t0 = time.time()
        run_all(J, Q, rng, st, trials=trials)
        print(name, "t", round(time.time() - t0, 2))


if __name__ == "__main__":
    rng = random.Random(1)
    st = Counter()
    go(zipper(45, 45), st, rng)
    for k, v in sorted(st.items()):
        print(k, v)
