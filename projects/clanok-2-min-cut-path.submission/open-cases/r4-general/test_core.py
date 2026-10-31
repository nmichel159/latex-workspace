"""The open core: yes-instances on which propagation leaves comparable free switches (Theorem R does not apply).
Random general instances (larger than in the other tests); for each such yes-instance HYB is run with a ladder of
parameters; the first parameter set that succeeds is recorded.
Usage: python test_core.py SEED COUNT NMIN NMAX"""
import sys
import random
import time
import json
from collections import Counter
from common_r4 import gcert, from_zz, dump
from gsw import GSW, prune, pruned_copy, reduce_to_2ch
import mixed

seed, count, nmin, nmax = (int(a) for a in sys.argv[1:5])
rng = random.Random(seed)
LADDER = [(1, 0, 1, 3), (1, 1, 2, 6), (2, 1, 4, 8)]
stats = Counter()
hard = []
t0 = time.time()
for it in range(count):
    nm = rng.randint(nmin, nmax)
    if it % 2 == 0:
        I = gcert.random_inst(rng, nm=nm, p_order=rng.choice([0.2, 0.35, 0.5]), p_R=rng.choice([0.15, 0.25]))
    else:
        I = from_zz(mixed.random_instance(rng, rng.choice(["lower", "upper", "mixed"]), nm=nm,
                                          p_order=rng.choice([0.25, 0.4]), p_tie=rng.choice([0.0, 0.5])))
    if not I.p2():
        continue
    ex = gcert.exact(I)
    stats["P2"] += 1
    if not ex:
        continue
    stats["yes"] += 1
    G = GSW(I)
    fixed, dead = prune(G)
    inst, free, reason = reduce_to_2ch(G, fixed)
    if inst is not None:
        stats["R applies"] += 1
        continue
    stats["core"] += 1
    H = pruned_copy(G, dead)
    for i, par in enumerate(LADDER):
        if H.decide(*par):
            stats["HYB %s" % (par,)] += 1
            break
    else:
        stats["HYB fails"] += 1
        hard.append(dump(I))
print("seed %d, %d generated, %.0fs: %s" % (seed, count, time.time() - t0, dict(stats)))
if hard:
    with open("runs/core-hard-%d.jsonl" % seed, "w") as f:
        for d in hard:
            f.write(json.dumps(d) + "\n")
