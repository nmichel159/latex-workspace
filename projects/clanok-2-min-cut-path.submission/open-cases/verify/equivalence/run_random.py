"""Random DC graphs (k = 2) or DC' graphs (k = 3) with 9..16 vertices: checks.check_graph on every unordered
pair (and the planted pair in both orders).
Usage: python run_random.py K SEED COUNT [workers] > results-random-K-SEED.txt"""
import sys, time, random
from collections import Counter
from multiprocessing import Pool
from checks import check_graph
from randgraphs import gen_core_ears, gen_planted


def work(args):
    k, seed = args
    rng = random.Random(seed)
    for _ in range(50):
        if rng.random() < 0.5:
            g = gen_core_ears(rng, k=k)
            if g is None:
                continue
            n, edges = g
            pairs = None
        else:
            g = gen_planted(rng, k=k)
            if g is None:
                continue
            n, edges, u, v = g
            pairs = [(x, y) for x in range(n) for y in range(x + 1, n)] + [(v, u)]
        st, vi = check_graph(n, edges, ordered=False, do_cp=(n <= 10), pairs=pairs)
        st["n=%d" % n] += 1
        return st, vi, seed
    return Counter(), [], seed


if __name__ == "__main__":
    k = int(sys.argv[1])
    seed = int(sys.argv[2])
    count = int(sys.argv[3])
    workers = int(sys.argv[4]) if len(sys.argv) > 4 else 30
    t0 = time.time()
    total = Counter()
    viol = []
    with Pool(workers) as pool:
        for st, vi, s in pool.imap_unordered(work, [(k, seed * 10 ** 7 + i) for i in range(count)], chunksize=4):
            total.update(st)
            for x in vi:
                viol.append((s,) + tuple(x))
    print("class k =", k, "seed", seed, "count", count)
    for key in sorted(total):
        print("%-55s %d" % (key, total[key]))
    print("violations:", len(viol))
    for x in viol[:40]:
        print("  ", x)
    print("time %.1fs" % (time.time() - t0))
