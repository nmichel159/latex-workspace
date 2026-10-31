"""Greedy shrinking of the rigid family R_L (dc-hardness/rigid.py, read-only import) under the property 'P2 and every
solution has at least K switches in each mode' (dc-algorithm.md Section 11.6).
Usage: python shrink_rigid.py L K SEEDS"""
import os
import sys
import json
import random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "dc-hardness"))
from rigid import rigid  # noqa: E402
import hunt_antichain as ha  # noqa: E402

L, K, seeds = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
inst = list(rigid(L))
print("R_%d: ok %s, mode counts %s, zz size %d, nodes %d" % (L, ha.ok(inst, K), ha.mode_counts(inst), ha.zz_size(inst),
                                                           inst[0]), flush=True)
best = None
for sd in range(seeds):
    rng = random.Random(sd)
    small, sz = ha.shrink(rng, inst, K)
    print("seed", sd, "size", sz, "switches", len(small[1]), "nodes", small[0], json.dumps(small), flush=True)
    if best is None or sz < best[0]:
        best = (sz, small)
print("best", best[0], json.dumps(best[1]), flush=True)
