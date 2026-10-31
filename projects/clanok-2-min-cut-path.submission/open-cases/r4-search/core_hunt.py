"""Random core instances (r4-general.md §8 'the core': yes-instances on which Theorem R does not apply after
propagation) on which HYB with the smallest parameters (1, 0, 1, 3) fails.  The generator is that of
r4-general/test_core.py (same random stream for the same seed and arguments), so seeds 2, 3, 4 with
COUNT 3000, NMIN 10, NMAX 16 reproduce the six instances of r4-general/runs/core-*.log that needed (1, 1, 2, 6).
Every instance with HYB(1, 0, 1, 3) failing is stored (runs/core-hunt-SEED.jsonl) with the first parameter set of
the ladder that succeeds.
Usage: python core_hunt.py SEED COUNT NMIN NMAX"""
import sys
import json
import random
import time
from collections import Counter
from common import gcert, zz, HERE, to_json
import mixed
from hyb import analyse

seed, count, nmin, nmax = (int(a) for a in sys.argv[1:5])
rng = random.Random(seed)
stats = Counter()
out = open("%s/runs/core-hunt-%d-%d-%d.jsonl" % (HERE, seed, nmin, nmax), "w")
t0 = time.time()
for it in range(count):
    nm = rng.randint(nmin, nmax)
    if it % 2 == 0:
        I = gcert.random_inst(rng, nm=nm, p_order=rng.choice([0.2, 0.35, 0.5]), p_R=rng.choice([0.15, 0.25]))
    else:
        zi = mixed.random_instance(rng, rng.choice(["lower", "upper", "mixed"]), nm=nm,
                                   p_order=rng.choice([0.25, 0.4]), p_tie=rng.choice([0.0, 0.5]))
        I = gcert.Inst(zi.n, zi.le, zi.R, zi.u, zi.v)
    if not I.p2():
        continue
    stats["P2"] += 1
    if not gcert.exact(I):
        continue
    stats["yes"] += 1
    z = zz.ZZ(I.n, None, I.R, I.u, I.v, le=I.le)
    a = analyse(z, with_thr=False)
    if not a["core"]:
        stats["R applies"] += 1
        continue
    stats["core"] += 1
    stats["HYB %s" % (a["hyb"],)] += 1
    if a["hyb"] != [1, 0, 1, 3]:
        d = to_json(z, name="core-%d-%d" % (seed, it), verdict=a,
                    notes="core_hunt.py seed %d it %d nm %d" % (seed, it, nm))
        out.write(json.dumps(d) + "\n")
        out.flush()
print("seed %d, %d generated, %.0fs: %s" % (seed, count, time.time() - t0, dict(stats)), flush=True)
