"""Simulated annealing for small portfolio-hard switch-model (2CH + P2) yes-instances (agent r4-search).

State: a 2CH instance with the property P (P2, yes-instance, portfolio-hard at level K: G_K, LAT2, H1, GC_K fail;
level 3 adds H2 when h2 is requested).  Moves: remove a node from a side, add an existing node to a side, add a new
node to two sides of the same type (a connector), merge two nodes, delete a node, delete a switch.  Every move must
keep P; a move that changes the size q (elements of the ZZ form) by d is accepted with probability
min(1, exp(-d / T)), T decreasing geometrically.  The best (smallest q, then |R|) instance is saved.
Usage: python anneal_sw.py START.json SEED STEPS K OUT.json"""
import sys
import math
import random
import time
from common import load, sw_to_zz, to_json, save, bits
import twoch
import swlib
from portfolio import portfolio
from shrink import compact


def prop(inst, K):
    N, E, F, s, t = inst
    if s == t or not twoch.p2_ok(E, F):
        return None
    if swlib.exact_2ch(inst) is None:
        return None
    z, names = sw_to_zz(inst)
    r = portfolio(z, level=K, sw=inst, exact_ans=True)
    if not r["hard"]:
        return None
    return (z.n, len(z.R))


def random_move(rng, inst):
    N, E, F, s, t = inst
    E, F = list(E), list(F)
    n = len(E)
    k = rng.random()
    if k < 0.3:
        i = rng.randrange(n)
        S = E if rng.random() < 0.5 else F
        if S[i]:
            x = rng.choice(bits(S[i]))
            S[i] &= ~(1 << x)
    elif k < 0.5:
        i = rng.randrange(n)
        S = E if rng.random() < 0.5 else F
        x = rng.randrange(N)
        S[i] |= 1 << x
    elif k < 0.6:
        i, j = rng.sample(range(n), 2)
        S = E if rng.random() < 0.5 else F
        x = N
        N += 1
        S[i] |= 1 << x
        S[j] |= 1 << x
    elif k < 0.8:
        x, y = rng.sample(range(N), 2)
        if {x, y} == {s, t}:
            return None
        for S in (E, F):
            for i in range(n):
                if (S[i] >> y) & 1:
                    S[i] = (S[i] & ~(1 << y)) | (1 << x)
        if y == s:
            s = x
        if y == t:
            t = x
    elif k < 0.92:
        x = rng.randrange(N)
        if x in (s, t):
            return None
        E = [e & ~(1 << x) for e in E]
        F = [f & ~(1 << x) for f in F]
    else:
        if n <= 2:
            return None
        i = rng.randrange(n)
        del E[i]
        del F[i]
    return compact((N, E, F, s, t))


def main():
    start, seed, steps, K, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    rng = random.Random(seed)
    z, inst, names = load(start)
    cur = tuple(inst)
    cs = prop(cur, K)
    assert cs is not None, "start lacks the property"
    best, bs = cur, cs
    T0, T1 = 2.0, 0.05
    t0 = time.time()
    acc = 0
    for step in range(steps):
        T = T0 * (T1 / T0) ** (step / max(1, steps - 1))
        nxt = random_move(rng, cur)
        if nxt is None:
            continue
        ns = prop(nxt, K)
        if ns is None:
            continue
        d = (ns[0] - cs[0]) + 0.1 * (ns[1] - cs[1])
        if d <= 0 or rng.random() < math.exp(-d / T):
            cur, cs = nxt, ns
            acc += 1
            if cs < bs:
                best, bs = cur, cs
                print("[%.0fs] step %d new best %s" % (time.time() - t0, step, bs), flush=True)
                zb, nb = sw_to_zz(best)
                save(out, to_json(zb, name="anneal-%d" % seed, names=nb, sw=best,
                                  notes="anneal_sw.py from %s seed %d level %d" % (start, seed, K)))
        if step % 2000 == 0:
            print("[%.0fs] step %d cur %s best %s accepted %d" % (time.time() - t0, step, cs, bs, acc), flush=True)
    zb, nb = sw_to_zz(best)
    save(out, to_json(zb, name="anneal-%d" % seed, names=nb, sw=best,
                      notes="anneal_sw.py from %s seed %d level %d" % (start, seed, K)))
    print("final best", bs, flush=True)


if __name__ == "__main__":
    main()
