"""Tiny random instances of ZZ with P2, not derived from graphs: solver against enumeration of down-sets, all shortest walks, proof on all four variants,
soundness of formula values (every value of a random formula is a down-set; on a no-instance no value connects u and v).

Usage: run_tiny.py SEED SECONDS LOG
"""
import os
import random
import sys
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from zz_core import ClaimFail, Inst, bits, chk  # noqa: E402
from zz_proof import Cfg, Walk, construct  # noqa: E402


def random_preorder(rng, m):
    """A random preorder on 0..m-1 with bottom 0 and top 1: closure of random relations."""
    up = [1 << i for i in range(m)]
    p = rng.uniform(0.05, 0.5)
    for i in range(2, m):
        up[0] |= 1 << i
        up[i] |= 1 << 1
    up[0] |= 1 << 1
    for i in range(2, m):
        for j in range(2, m):
            if i != j and rng.random() < p:
                up[i] |= 1 << j
    changed = True
    while changed:
        changed = False
        for i in range(m):
            for j in bits(up[i]):
                if up[j] & ~up[i]:
                    up[i] |= up[j]
                    changed = True
    return up


def random_instance(rng):
    m = rng.randint(4, 11)
    up = random_preorder(rng, m)
    I0 = Inst(m, up, [], 0, 1)
    if not I0.lt(0, 1):
        return None
    pairs = [(x, y) for x in range(m) for y in bits(I0.USTR[x])]
    q = rng.uniform(0.1, 0.8)
    edges = {e for e in pairs if rng.random() < q}
    I = Inst(m, up, edges, 0, 1)
    # P2 repair with existing elements only: add edges for the violating pairs
    for _ in range(40):
        viol = I.p2_violations()
        if not viol:
            return I
        x, y = rng.choice(viol)
        below = I.DSTR[x] & I.DSTR[y]
        above = I.USTR[x] & I.USTR[y]
        c = list(bits(below)) + list(bits(above))
        if not c:
            return None
        z = rng.choice(c)
        if I.lt(z, x):
            edges |= {(z, x), (z, y)}
        else:
            edges |= {(x, z), (y, z)}
        I = Inst(m, up, edges, 0, 1)
    return None


def random_formula_value(I, rng):
    Q = list(range(I.m))

    def s(k):
        r = 0
        for _ in range(rng.randint(0, k)):
            r |= 1 << rng.choice(Q)
        return r

    if rng.random() < 0.5:
        xs = [rng.choice(Q) for _ in range(6)]
        pairs = [(xs[0], xs[1]) if rng.random() < 0.7 else None, (xs[2], xs[3]) if rng.random() < 0.7 else None,
                 (xs[4], xs[5]) if rng.random() < 0.7 else None]
        return I.F_formula(pairs, s(4), s(3))
    xs = [rng.choice(Q) for _ in range(8)]
    pairs = [(xs[2 * i], xs[2 * i + 1]) if rng.random() < 0.7 else None for i in range(4)]
    return I.E_formula(pairs, s(4))


def main():
    seed, secs, logf = int(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
    rng = random.Random(seed)
    st = Counter()
    fails = []
    cfg = Cfg()
    t0 = time.time()
    while time.time() - t0 < secs:
        I = random_instance(rng)
        if I is None:
            st["generator gave up"] += 1
            continue
        try:
            I.validate()
            chk(I.p2(), "P2")
            st["instances"] += 1
            ds = I.downsets()
            best = None
            for D in ds:
                k = I.dist_in_GD(D)
                if k is not None and (best is None or k < best):
                    best = k
            w = I.shortest_walk()
            chk((w is None) == (best is None), "solver: yes or no against the down-sets")
            if w is None:
                st["no-instances"] += 1
            else:
                st["yes-instances"] += 1
                chk(len(w) - 1 == best, "solver: length against the down-sets")
                J = I.reversed_instance()
                for Q in I.all_shortest(best, cap=20):
                    st["shortest walks"] += 1
                    for K, Z in ((I, Q), (I, Q[::-1]), (J, Q), (J, Q[::-1])):
                        construct(Walk(K, Z), cfg, rng, st)
            for _ in range(10):
                D = random_formula_value(I, rng)
                chk(I.is_downset(D), "formula value is a down-set")
                st["formula values"] += 1
                if D >> I.u & 1 and not D >> I.v & 1 and I.connected_in_GD(D):
                    chk(best is not None, "a formula value connects on a no-instance")
                    st["formula values passing the test"] += 1
        except ClaimFail as e:
            fails.append((I.m, sorted(I.edges), [hex(x) for x in I.UP], str(e)))
    with open(logf, "w", encoding="utf-8") as f:
        print("seed", seed, "time", round(time.time() - t0, 1), file=f)
        for k in sorted(st):
            print(k, st[k], file=f)
        print("FAILURES:", fails[:4] if fails else "none", file=f)


if __name__ == "__main__":
    main()
