"""Exhaustive checks on tiny abstract switch forms: all side sets on N nodes for m switches, all preorders on the
switches (m <= 3), terminals s = 0, t = N - 1.  For each instance: pruning soundness, Theorem R (a) for the own
fixing and the maximal sound fixing, and Theorem 5' soundness for every certificate set K, B in 0..3, s in 0..2.
Usage: python exhaustive_small.py N M [SAMPLE SEED]"""
import itertools
import random
import sys
from collections import Counter
from gswlib import SW


def preorders(m):
    out = []
    pairs = [(i, j) for i in range(m) for j in range(m) if i != j]
    for sub in itertools.product((False, True), repeat=len(pairs)):
        le = [[i == j for j in range(m)] for i in range(m)]
        for (i, j), b in zip(pairs, sub):
            le[i][j] = b
        ok = all(not (le[i][k] and le[k][j]) or le[i][j] for i in range(m) for j in range(m) for k in range(m))
        if ok:
            out.append(le)
    return out


def main():
    N, m = int(sys.argv[1]), int(sys.argv[2])
    sample = int(sys.argv[3]) if len(sys.argv) > 3 else None
    rng = random.Random(int(sys.argv[4]) if len(sys.argv) > 4 else 0)
    pos = preorders(m)
    st = Counter()
    full = 1 << N

    def instances():
        if sample is None:
            for sides in itertools.product(range(full), repeat=2 * m):
                for le in pos:
                    yield sides, le
        else:
            for _ in range(sample):
                yield [rng.randrange(full) for _ in range(2 * m)], rng.choice(pos)
    for sides, le in instances():
        E, F = list(sides[0::2]), list(sides[1::2])
        G = SW(N, E, F, le, 0, N - 1)
        sols = G.solutions()
        yes = bool(sols)
        st["inst"] += 1
        st["yes" if yes else "no"] += 1
        fixed, status = G.prune()
        if status == "no" and yes:
            st["prune_unsound"] += 1
        if status == "ok":
            if any(sol[z] != mo for sol in sols for z, mo in fixed.items()):
                st["prune_unsound"] += 1
        fixings = []
        if status == "ok":
            fixings.append(fixed)
        if yes:
            fmax = {z: sols[0][z] for z in range(m) if all(s[z] == sols[0][z] for s in sols)}
            fixings.append(fmax)
        for fx in fixings:
            free = [w for w in range(m) if w not in fx]
            if all(not le[a][b] and not le[b][a] for i, a in enumerate(free) for b in free[i + 1:]):
                H, _ = G.contract(fx)
                st["R_checked"] += 1
                if bool(H.solutions()) != yes:
                    st["R_mismatch"] += 1
                    print("R MISMATCH", E, F, le, fx)
        sidelist = G.sides
        for r in range(len(sidelist) + 1):
            for K in itertools.combinations(sidelist, r):
                for B in range(4):
                    for s in range(3):
                        w = G.search5(K, B, s)
                        st["t5"] += 1
                        if w is not None:
                            st["t5_acc"] += 1
                            if not yes or not G.is_valid_walk(w):
                                st["t5_unsound"] += 1
                                print("5' UNSOUND", E, F, le, K, B, s, w)
    print("N=%d m=%d sample=%s:" % (N, m, sample), dict(sorted(st.items())))


if __name__ == "__main__":
    main()
