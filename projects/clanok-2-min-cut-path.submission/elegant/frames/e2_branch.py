"""Experiment E2: conflict-driven branching on elements (CEGAR).

Node = pair (Lf, Uf) of forced sets (down-set, up-set, disjoint).  Compute a shortest walk W of the state graph with low states outside Uf and high states outside Lf.
No walk: dead end.  W valid: accept.  Otherwise take a conflict h <= l of W and branch on a pivot z in [h, l]: z in D (Lf |= dn z) or z not in D (Uf |= up z).
Every valid D stays consistent with one child, so the search is exact; the question is the size of the tree.

A no-instance is produced by deleting one edge of the walk that disconnects all valid walks, when possible (checked by the exact solver), or by random tiny instances.

Usage: e2_branch.py SEED COUNT LIMIT LOG
"""
import random
import sys
import time

from common import BASES, Budget, Inst, StateGraph, WData, bits, conflicts, popcnt, random_p2_instance


def search(I, limit, pivot="min", rng=None, order="first"):
    nodes = [0]
    seen = set()
    maxdepth = [0]

    def rec(Lf, Uf, depth):
        if (Lf, Uf) in seen:
            return None
        seen.add((Lf, Uf))
        nodes[0] += 1
        maxdepth[0] = max(maxdepth[0], depth)
        if nodes[0] > limit:
            raise Budget()
        G = StateGraph(I, I.ALL & ~Uf, I.ALL & ~Lf)
        W = G.shortest(rng)
        if W is None:
            return None
        c = conflicts(I, W)
        if not c:
            return W
        # choose the conflict: closest in position or first
        pos = {}
        for i, x in enumerate(W):
            pos.setdefault(x, []).append(i)
        if order == "near":
            c.sort(key=lambda hl: min(abs(i - j) for i in pos[hl[0]] for j in pos[hl[1]]))
        elif order == "far":
            c.sort(key=lambda hl: -min(abs(i - j) for i in pos[hl[0]] for j in pos[hl[1]]))
        h, l = c[0]
        z = h if pivot == "min" else l
        L1 = Lf | I.DN[z]
        U2 = Uf | I.UP[z]
        for Lc, Uc in ((L1, Uf), (Lf, U2)):
            if Lc & Uc:
                continue
            r = rec(Lc, Uc, depth + 1)
            if r is not None:
                return r
        return None

    try:
        r = rec(I.DN[I.u], I.UP[I.v], 0)
    except Budget:
        return "budget", nodes[0], maxdepth[0]
    return r, nodes[0], maxdepth[0]


def main():
    sys.setrecursionlimit(100000)
    seed, count, limit, logf = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    rng = random.Random(seed)
    fams = ["small", "B", "A", "stair", "ties", "mix", "cross", "allstrict", "kappa", "two"]
    with open(logf, "w", encoding="utf-8") as f:
        print("fam m q result nodes depth (pivot, order) ...", file=f)
        for fam in fams:
            for _ in range(count):
                d = BASES[fam](rng)
                I, P = d.build()
                row = [fam, I.m, len(P) - 1]
                for pivot in ("min", "max"):
                    for order in ("first", "near", "far"):
                        t = time.time()
                        r, n, dep = search(I, limit, pivot, None, order)
                        row.append("%s:%s:%s/%d/%d" % (pivot, order, "V" if isinstance(r, list) else r, n, dep))
                print(*row, file=f, flush=True)


if __name__ == "__main__":
    main()
