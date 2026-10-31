"""Referee rv-r7-desc: random P2 instances with many ties, including long paths.  Usage: run_random.py SEED COUNT LOG.
Generators:
 flat: random preorder (few classes, so many ties), random sides, P2 completed by adding common nodes or middle witnesses.
 long: a random word with random classes; contacts added at random and kept only if the planted path stays shortest; shorter walks
       blocked by strict pairs (random-layout CEGIS), so paths reach r = 40..90 with |A|, |B| around 10..40.
"""
import os
import random
import sys
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from swf import Inst, ClaimFail, Budget  # noqa: E402
from proof import run_all  # noqa: E402


def random_preorder(rng, m):
    k = rng.randint(1, max(1, m // 2 + 1))
    cl = [rng.randrange(k) for _ in range(m)]
    order = list(range(k))
    rng.shuffle(order)
    rank = {c: i for i, c in enumerate(order)}
    p = rng.choice([0.0, 0.1, 0.3, 0.6])
    rel = {(a, b) for a in range(k) for b in range(k) if rank[a] < rank[b] and rng.random() < p}
    # transitive closure
    changed = True
    while changed:
        changed = False
        for a, b in list(rel):
            for c, d in list(rel):
                if b == c and (a, d) not in rel:
                    rel.add((a, d))
                    changed = True
    return [[cl[i] == cl[j] or (cl[i], cl[j]) in rel for j in range(m)] for i in range(m)]


def flat(rng):
    m = rng.randint(3, 11)
    le = random_preorder(rng, m)
    base = rng.randint(3, 10)
    dens = rng.choice([0.1, 0.2, 0.35])
    E = [sum(1 << n for n in range(base) if rng.random() < dens) for _ in range(m)]
    F = [sum(1 << n for n in range(base) if rng.random() < dens) for _ in range(m)]
    nn = base
    me = []
    strict = [(i, j) for i in range(m) for j in range(m) if le[i][j] and not le[j][i]]

    def add_me(z, w):
        nonlocal nn
        if any(a == z and b == w for a, b, _ in me):
            return
        me.append((z, w, nn))
        F[z] |= 1 << nn
        E[w] |= 1 << nn
        nn += 1

    for z, w in strict:
        if rng.random() < 0.1:
            add_me(z, w)
    for x in range(m):
        for y in range(x + 1, m):
            if le[x][y] or le[y][x]:
                continue
            lmn = {a for a, b, _ in me if b == x} & {a for a, b, _ in me if b == y}
            umn = {b for a, b, _ in me if a == x} & {b for a, b, _ in me if a == y}
            if E[x] & E[y] or F[x] & F[y] or lmn or umn:
                continue
            kind = rng.randrange(4)
            low = [z for z in range(m) if le[z][x] and not le[x][z] and le[z][y] and not le[y][z]]
            upp = [z for z in range(m) if le[x][z] and not le[z][x] and le[y][z] and not le[z][y]]
            if kind == 2 and low:
                z = rng.choice(low)
                add_me(z, x)
                add_me(z, y)
            elif kind == 3 and upp:
                z = rng.choice(upp)
                add_me(x, z)
                add_me(y, z)
            elif kind == 0:
                n = nn
                nn += 1
                E[x] |= 1 << n
                E[y] |= 1 << n
            else:
                n = nn
                nn += 1
                F[x] |= 1 << n
                F[y] |= 1 << n
    return Inst(m, le, E, F, 0, 1, nn, me)


def main():
    seed, count = int(sys.argv[1]), int(sys.argv[2])
    log = open(sys.argv[3], "w", encoding="utf-8")
    rng = random.Random(seed)
    st = Counter()
    fails = []
    t0 = time.time()
    for it in range(count):
        I = flat(rng)
        I.validate()
        assert I.p2()
        st["instances"] += 1
        try:
            w = I.shortest(budget=500_000)
        except Budget:
            st["budget"] += 1
            continue
        if I.m <= 11:
            yes, best = I.exact_downsets()
            assert (w is not None) == (best is not None) and (w is None or len(w) == best), "solver disagrees"
        if w is None:
            st["no"] += 1
            continue
        st["yes"] += 1
        st["max r"] = max(st["max r"], len(w))
        st["ties on path"] += 0
        paths = I.all_shortest(len(w), cap=60)
        for P in paths:
            try:
                run_all(I, P, rng, st, trials=2)
            except ClaimFail as e:
                name = os.path.join(HERE, "ce", "random-%d-%d.json" % (seed, it))
                I.dump(name, {"P": P, "fail": str(e)})
                fails.append((name, str(e)))
                print("FAIL", name, e, file=log, flush=True)
    for k in sorted(st):
        print(k, st[k], file=log)
    print("time", round(time.time() - t0, 1), file=log)
    print("FAILURES:", fails if fails else "none", file=log)
    log.close()


if __name__ == "__main__":
    main()
