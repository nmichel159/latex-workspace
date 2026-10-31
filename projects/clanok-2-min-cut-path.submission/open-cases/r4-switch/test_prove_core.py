"""Constructive proof check on 'core' instances designed to reach the bad case: word F^A E^M F^B (and the mirror
E^A F^M E^B), cross pairs between the run and the later block oriented at random (forward contact of the run
partner with probability PF, else backward contact of the later partner), optional extra forward contacts.
All shortest valid paths are tested.
Usage: python test_prove_core.py SEED COUNT A M B PF PX"""
import sys
import random
import time

import sw
import gen
import prove
from test_prove import run_one

seed, count = int(sys.argv[1]), int(sys.argv[2])
A, M, B = int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
PF, PX = float(sys.argv[6]), float(sys.argv[7])
rng = random.Random(seed)
stats = dict(yes=0, no=0, paths=0, fail=0, maxdom=0, maxsing=0, maxstore=0)
t0 = time.time()
for it in range(count):
    x, y = ("F", "E") if it % 2 == 0 else ("E", "F")
    word = x * A + y * M + x * B

    def orient(p, q):
        if word[p - 1] == x and word[q - 1] == y:
            return "f"
        if word[p - 1] == y and word[q - 1] == x:
            return "f" if rng.random() < PF else "b"
        return "f"
    inst, P = gen.planted(word, rng, orient, PX, 0.0)
    assert sw.p2_ok(inst)
    run_one(inst, stats, word)
print("seed", seed, "A M B", A, M, B, "PF", PF, "PX", PX, stats, "%.1fs" % (time.time() - t0), flush=True)
