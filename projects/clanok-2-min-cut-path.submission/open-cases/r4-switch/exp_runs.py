"""Experiment: planted instances with word E^a F^b (or a given word pattern), random orientations and random extra
forward/backward contacts; keep instances whose planted path is the unique solution; report the least certificate
storage for k = 1..KMAX basic sets.
Usage: python exp_runs.py SEED COUNT WORD PFWD PBWD KMAX"""
import sys
import random
import time

import sw
import gen
import certcost

seed, count, word = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
pfwd, pbwd, kmax = float(sys.argv[4]), float(sys.argv[5]), int(sys.argv[6])
rng = random.Random(seed)
t0 = time.time()
worst = {}
nuniq = 0
for it in range(count):
    po = rng.random()
    orient = lambda p, q: "f" if rng.random() < po else "b"
    inst, P = gen.planted(word, rng, orient, pfwd, pbwd)
    assert sw.p2_ok(inst)
    sols = sw.all_solutions(inst)
    if len(sols) != 1:
        continue
    nuniq += 1
    c = certcost.cost(inst, P, kmax)
    for k in range(1, kmax + 1):
        v = c[k][0] if c[k] else 999
        if v > worst.get(k, (-1,))[0]:
            worst[k] = (v, it, po, c[k])
print("seed", seed, "word", word, "pfwd", pfwd, "pbwd", pbwd, "unique", nuniq, "of", count)
for k in sorted(worst):
    print("  k=%d worst storage %s (it %d, po %.2f) %s" % (k, worst[k][0], worst[k][1], worst[k][2], worst[k][3]))
print("%.1fs" % (time.time() - t0))
