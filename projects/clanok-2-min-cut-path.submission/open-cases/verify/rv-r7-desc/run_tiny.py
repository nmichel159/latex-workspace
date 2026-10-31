"""Referee rv-r7-desc: exhaustive tiny instances.  Usage: run_tiny.py PART NPARTS LOG.
All preorders on m <= 3 switches (m = 3: up to isomorphism), all sides over the nodes {s, t, n} for m <= 3 (and {s, t, n, n'} for m <= 2),
all sets of middle edges on strict pairs.  For each: own validity, P2 filter, solver against enumeration of down-sets, all shortest
paths, the checks of proof.run_all.  Also: every down-set is a mode vector and the connect test agrees with Lemma 3.4."""
import itertools
import os
import random
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from swf import Inst, ClaimFail  # noqa: E402
from proof import run_all  # noqa: E402


def preorders(m):
    out = []
    pairs = [(i, j) for i in range(m) for j in range(m) if i != j]
    for mask in range(1 << len(pairs)):
        le = [[i == j for j in range(m)] for i in range(m)]
        for k, (i, j) in enumerate(pairs):
            if mask >> k & 1:
                le[i][j] = True
        ok = all(not (le[i][j] and le[j][k]) or le[i][k] for i in range(m) for j in range(m) for k in range(m))
        if ok:
            out.append(le)
    return out


def canon(le):
    m = len(le)
    return min(tuple(tuple(le[p[i]][p[j]] for j in range(m)) for i in range(m)) for p in itertools.permutations(range(m)))


def main():
    part, nparts = int(sys.argv[1]), int(sys.argv[2])
    log = open(sys.argv[3], "w", encoding="utf-8")
    rng = random.Random(part)
    st = Counter()
    fails = []
    idx = 0
    for m, nbase in ((1, 4), (2, 4), (3, 3)):
        ps = preorders(m)
        seen = set()
        reps = []
        for le in ps:
            c = canon(le)
            if c not in seen:
                seen.add(c)
                reps.append(le)
        for le in reps:
            strict = [(i, j) for i in range(m) for j in range(m) if le[i][j] and not le[j][i]]
            for mesub in range(1 << len(strict)):
                me0 = [strict[k] for k in range(len(strict)) if mesub >> k & 1]
                if m == 3 and len(me0) > 2:
                    continue
                nn = nbase + len(me0)
                me = [(z, w, nbase + k) for k, (z, w) in enumerate(me0)]
                extraE = [0] * m
                extraF = [0] * m
                for z, w, p in me:
                    extraF[z] |= 1 << p
                    extraE[w] |= 1 << p
                # sides over base nodes: s = 0, t = 1, others
                for combo in itertools.product(range(1 << nbase), repeat=2 * m):
                    idx += 1
                    if idx % nparts != part:
                        continue
                    E = [combo[i] | extraE[i] for i in range(m)]
                    F = [combo[m + i] | extraF[i] for i in range(m)]
                    # quick P2 filter
                    bad = False
                    for x in range(m):
                        for y in range(x + 1, m):
                            if not le[x][y] and not le[y][x]:
                                if not (E[x] & E[y] or F[x] & F[y]):
                                    lmn = any(z == q and w1 == x for z, w1, _ in me for q, w2, _ in me if w2 == y)
                                    umn = any(w == q and z1 == x for z1, w, _ in me for z2, q, _ in me if z2 == y)
                                    if not lmn and not umn:
                                        bad = True
                    if bad:
                        st["P2 fails"] += 1
                        continue
                    I = Inst(m, le, E, F, 0, 1, nn, me)
                    st["instances"] += 1
                    assert I.p2()
                    yes, best = I.exact_downsets()
                    w = I.shortest()
                    assert (w is not None) == (best is not None), "solver disagrees on existence"
                    if w is None:
                        st["no"] += 1
                        continue
                    assert len(w) == best, "solver disagrees on length"
                    st["yes"] += 1
                    paths = I.all_shortest(len(w))
                    assert w in paths, "enumerator misses a path"
                    for P in paths:
                        try:
                            run_all(I, P, rng, st, trials=1)
                        except ClaimFail as e:
                            fails.append((m, le, E, F, me, P, str(e)))
                            print("FAIL", m, le, E, F, me, P, e, file=log, flush=True)
    for k in sorted(st):
        print(k, st[k], file=log)
    print("FAILURES:", len(fails) if fails else "none", file=log)
    log.close()


if __name__ == "__main__":
    main()
