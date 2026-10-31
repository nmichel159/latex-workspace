"""Remark (2) of r5-classes.md §2b, abstract part: for random bipartite tournaments (rows R, columns C, each pair
oriented at random: B[r][c] = 1 means 'r covers c', else 'c covers r'), the least number hR of rows covering all
columns and hC of columns covering all rows; also the game value and the bound floor(log2 n) + 1.

usage: python tourn_abstract.py SEED TRIALS n [n ...]
"""
import random
import sys

from qcore import min_cover, kq


def main():
    seed, trials = int(sys.argv[1]), int(sys.argv[2])
    sizes = [int(x) for x in sys.argv[3:]]
    rng = random.Random(seed)
    for n in sizes:
        res = []
        for _ in range(trials):
            B = [[rng.randrange(2) for _ in range(n)] for _ in range(n)]
            rows = [sum(B[i][j] << j for j in range(n)) for i in range(n)]
            cols = [sum((1 - B[i][j]) << i for i in range(n)) for j in range(n)]
            hR, _ = min_cover((1 << n) - 1, rows)
            hC, _ = min_cover((1 << n) - 1, cols)
            res.append(min(x for x in (hR, hC) if x is not None))
        res.sort()
        print("n=%d: min(hR, hC) over %d trials: min %d, median %d, max %d; floor(log2 n)+1 = %d" % (
            n, trials, res[0], res[len(res) // 2], res[-1], kq(n)), flush=True)


if __name__ == "__main__":
    main()
