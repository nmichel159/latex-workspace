"""Referee rv-r7-desc: soundness of the enumeration of Corollary B1.  Random choices of switches in the roles of all four shapes and of the exit
formulas, on random P2 instances and on planted instances with the path destroyed: every value must be a down-set, and if it connects s, t the exact
solver must say yes.  Usage: run_sound.py SEED COUNT LOG."""
import os
import random
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from swf import ClaimFail  # noqa: E402
import run_random as rr  # noqa: E402


def formulas(I, rng):
    M = list(range(I.m))
    pick = lambda k: [rng.choice(M) for _ in range(k)]
    ALL = I.ALL

    def dn(S):
        r = 0
        for b in S:
            r |= I.DN[b]
        return r

    def nu(S):
        r = ALL
        for a in S:
            r &= ~I.UP[a]
        return r

    x = pick(4)
    Fs = I.FR(x[0], x[1]) | I.FR(x[2], x[3]) | dn(pick(rng.randint(0, 28)))
    y = pick(4)
    Es = I.ER(y[0], y[1]) & I.ER(y[2], y[3]) & nu(pick(rng.randint(0, 28)))
    Ek = nu(pick(rng.randint(0, 20)))
    Fk = dn(pick(rng.randint(0, 20)))
    a1, a2 = pick(2)
    F1 = Fs | Fk | I.FR(a1, a2) | (nu(pick(rng.randint(0, 18))) & (I.EP(a1) | I.EP(a2)))
    yield "shape A", F1 | dn(pick(rng.randint(0, 19)))
    h = pick(4)
    yield "shape B", Es & Ek & I.ER(h[0], h[1]) & I.ER(h[2], h[3])
    h1, h2 = pick(2)
    E1 = Es & Ek & I.ER(h1, h2) & (dn(pick(rng.randint(0, 18))) | (I.FP(h1) & I.FP(h2)))
    yield "shape A'", E1 & nu(pick(rng.randint(0, 19)))
    z = pick(4)
    yield "shape B'", Fs | Fk | I.FR(z[0], z[1]) | I.FR(z[2], z[3])
    yield "exit nu", nu(pick(rng.randint(0, 9)))
    yield "exit dn", dn(pick(rng.randint(0, 9)))


def main():
    seed, count = int(sys.argv[1]), int(sys.argv[2])
    log = open(sys.argv[3], "w", encoding="utf-8")
    rng = random.Random(seed)
    st = Counter()
    for it in range(count):
        I = rr.flat(rng)
        w = I.shortest(budget=500_000)
        st["instances"] += 1
        st["no-instances" if w is None else "yes-instances"] += 1
        for _ in range(30):
            for name, D in formulas(I, rng):
                assert I.is_downset(D), name + ": not a down-set"
                st["formula values"] += 1
                if I.connects(D):
                    st["connecting values"] += 1
                    assert w is not None or I.s == I.t, name + ": connects on a no-instance"
    for k in sorted(st):
        print(k, st[k], file=log)
    print("FAILURES: none", file=log)
    log.close()


if __name__ == "__main__":
    main()
