"""Question 2 of the task: structural parameters of the planted families and of the walk.

For each family: m, q, |A_P|, |B_P|, classes, width of the preorder (Dilworth on classes), number of strict pairs of A x B, VC dimension of the set systems
{MA(a) cap B_P : a in A_P}, {MB(b) cap A_P : b in B_P}, {MA(x) : x in Q}, {MB(x) : x in Q}, Helly-type data on upper neighbourhoods of A_P, and states of the exact solver.

Usage: params.py SEED COUNT LOG
"""
import random
import sys
import time
from itertools import combinations

from common import BASES, Budget, WData, bits, popcnt


def width(I):
    """Largest antichain of the classes: |classes| - maximum matching in the strict order (Dilworth)."""
    reps = []
    seen = 0
    for x in range(I.m):
        if not seen >> x & 1:
            reps.append(x)
            seen |= I.CL[x]
    idx = {r: i for i, r in enumerate(reps)}
    adj = [[idx[y] for y in reps if I.lt(x, y)] for x in reps]
    match = [-1] * len(reps)

    def aug(i, vis):
        for j in adj[i]:
            if not vis[j]:
                vis[j] = True
                if match[j] < 0 or aug(match[j], vis):
                    match[j] = i
                    return True
        return False

    c = 0
    for i in range(len(reps)):
        if aug(i, [False] * len(reps)):
            c += 1
    return len(reps) - c, len(reps)


def vc_dim(sets, ground, cap=8, limit=3_000_000):
    """VC dimension of a family of masks on the listed ground elements, computed from below by extension of shattered sets."""
    fam = list({s & sum(1 << g for g in ground) for s in sets})
    if not fam:
        return -1
    shattered = [()]
    d = 0
    work = 0
    while d < cap:
        nxt = []
        for S in shattered:
            start = (ground.index(S[-1]) + 1) if S else 0
            for g in ground[start:]:
                T = S + (g,)
                mask = sum(1 << t for t in T)
                traces = {s & mask for s in fam}
                work += len(fam)
                if len(traces) == 1 << len(T):
                    nxt.append(T)
                if work > limit:
                    return ">=%d" % d
        if not nxt:
            return d
        shattered = nxt
        d += 1
    return ">=%d" % d


def helly(I, W):
    """Upper neighbourhoods of A_P: largest k such that all k-subsets of far elements intersect, tested for k = 2, 3, and whether they have a common element."""
    A = W.A
    far = [a for i, a in enumerate(A) if i % 3 == 0]
    all_int = I.ALL
    for a in far:
        all_int &= I.HI[a]
    p = all(I.HI[x] & I.HI[y] for x, y in combinations(far, 2))
    return p, bool(all_int)


def main():
    seed, count, logf = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    rng = random.Random(seed)
    fams = ["B", "A", "stair", "ties", "small", "mix", "cross", "allstrict", "kappa", "two"]
    with open(logf, "w", encoding="utf-8") as f:
        print("family m q |A| |B| classes width strictAB/|AxB| VC(MA cap B on B) VC(MB cap A on A) VC(MA on Q) VC(MB on Q) pairwise-common(hi(A)) global-common  solver-states", file=f)
        for fam in fams:
            for _ in range(count):
                d = BASES[fam](rng)
                I, P = d.build()
                W = WData(I, P)
                w, cl = width(I)
                st = sum(1 for a in W.A for b in W.B if I.lt(b, a))
                a1 = vc_dim([I.MA[a] for a in W.A], W.B)
                a2 = vc_dim([I.MB[b] for b in W.B], W.A)
                core = [x for x in range(I.m) if x not in (I.u, I.v)]
                core = core[:60]
                a3 = vc_dim([I.MA[x] for x in range(I.m)], core, limit=800_000)
                a4 = vc_dim([I.MB[x] for x in range(I.m)], core, limit=800_000)
                h = helly(I, W)
                print(fam, I.m, len(P) - 1, len(W.A), len(W.B), cl, w, "%d/%d" % (st, len(W.A) * len(W.B)), a1, a2, a3, a4, h[0], h[1], file=f, flush=True)


if __name__ == "__main__":
    main()
