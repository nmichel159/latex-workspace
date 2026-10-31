"""The combinatorial core of Theorem Q (r5-classes §2b), on random 0/1 matrices.

Rows v (|V| = nr), columns w (|W*| = nc); M[v][w] = 1 iff v^O meets w^O; N[v][w] = 1 iff w^T meets v^T; Lemma D says
M | N = all ones.  Claim of the proof: with m >= nr + nc and k = floor(log2 m) + 1, if the game value of M is >= 1/2
then some k rows of M cover all columns; otherwise some k columns of N cover all rows (here V* = all rows).
usage: python test_minimax.py SEED COUNT NMAX
"""
import itertools
import json
import math
import random
import sys

import numpy as np
from scipy.optimize import linprog


def game_value(M):
    nr, ncol = M.shape
    c = np.zeros(nr + 1)
    c[-1] = -1.0
    A_ub = np.hstack([-M.T, np.ones((ncol, 1))])
    res = linprog(c, A_ub=A_ub, b_ub=np.zeros(ncol), A_eq=np.hstack([np.ones((1, nr)), np.zeros((1, 1))]),
                  b_eq=np.array([1.0]), bounds=[(0, None)] * nr + [(None, None)], method="highs")
    return -res.fun


def cover_size(rows_sets, universe, limit):
    """least number of sets (bit masks) whose union is `universe`, if <= limit (greedy first, then exact)"""
    if universe == 0:
        return 0
    # greedy upper bound
    left = universe
    g = 0
    while left:
        best = max(rows_sets, key=lambda s: bin(s & left).count("1"))
        if not best & left:
            return None
        left &= ~best
        g += 1
    if g <= 2:
        return g
    for j in range(1, min(g, limit + 1)):
        for comb in itertools.combinations(rows_sets, j):
            u = 0
            for s in comb:
                u |= s
            if u & universe == universe:
                return j
    return g if g <= limit else None


def main():
    seed, count, nmax = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    rng = random.Random(seed)
    stats = {"tested": 0, "lam>=1/2": 0, "lam<1/2": 0, "fail": 0, "max_needed": 0}
    worst = []
    for _ in range(count):
        nr, nc = rng.randint(2, nmax), rng.randint(2, nmax)
        m = nr + nc
        k = int(math.floor(math.log2(m))) + 1
        p = rng.choice([0.2, 0.35, 0.5, 0.65, 0.8])
        M = np.array([[1.0 if rng.random() < p else 0.0 for _ in range(nc)] for _ in range(nr)])
        q = rng.choice([0.0, 0.1, 0.3])
        N = np.array([[1.0 if (M[v][w] == 0 or rng.random() < q) else 0.0 for w in range(nc)] for v in range(nr)])
        lam = game_value(M)
        rowsets = [sum(1 << w for w in range(nc) if M[v][w]) for v in range(nr)]
        colsets = [sum(1 << v for v in range(nr) if N[v][w]) for w in range(nc)]
        stats["tested"] += 1
        if lam >= 0.5 - 1e-9:
            stats["lam>=1/2"] += 1
            j = cover_size(rowsets, (1 << nc) - 1, k)
        else:
            stats["lam<1/2"] += 1
            j = cover_size(colsets, (1 << nr) - 1, k)
        if j is None:
            stats["fail"] += 1
            worst.append({"M": M.tolist(), "N": N.tolist(), "lam": lam, "k": k})
        else:
            stats["max_needed"] = max(stats["max_needed"], j)
    print(json.dumps(stats))
    with open("runs/minimax-%d.json" % seed, "w") as fh:
        json.dump({"stats": stats, "fails": worst[:5]}, fh)


if __name__ == "__main__":
    main()
