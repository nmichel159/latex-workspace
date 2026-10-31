"""Experiment: planted-path instances (gen.planted) with random words, random orientations and random extra
contacts.  For each instance: P2, number of solutions (brute force), whether the planted path is a shortest valid
path, least certificate cost (cert.min_cert, k = 1, 2), and the k-search answer.
Usage: python exp_planted.py SEED COUNT LMIN LMAX PFWD PBWD"""
import sys
import random
import time

import sw
import gen
import cert

seed, count, lmin, lmax = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
pfwd, pbwd = float(sys.argv[5]), float(sys.argv[6])
rng = random.Random(seed)
t0 = time.time()
agg = {}
for it in range(count):
    L = rng.randint(lmin, lmax)
    word = "".join(rng.choice("EF") for _ in range(L))
    po = rng.random()
    orient = lambda p, q: "f" if rng.random() < po else "b"
    inst, P = gen.planted(word, rng, orient, pfwd, pbwd)
    assert sw.p2_ok(inst)
    sols = sw.all_solutions(inst)
    Ls, paths = sw.shortest_valid_paths(inst, limit=50)
    planted_shortest = P in paths
    mc = cert.min_cert(inst, paths[0], kmax=2) if paths else None
    c1 = mc[1][0] if mc and mc[1] else None
    c2 = mc[2][0] if mc and mc[2] else None
    key = (len(sols) == 1, planted_shortest, c1, c2)
    agg[key] = agg.get(key, 0) + 1
    if len(sols) == 1 and (c1 is None or c1 > 3):
        print("word", word, "po %.2f" % po, "sols", len(sols), "len", Ls, "cert", mc, flush=True)
print("seed", seed, "(unique, planted shortest, cost k=1, cost k=2): count")
for k in sorted(agg, key=str):
    print("  ", k, agg[k])
print("%.1fs" % (time.time() - t0))
