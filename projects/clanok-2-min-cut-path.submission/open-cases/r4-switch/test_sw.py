"""Self-test of sw.py: exact solvers agree with twoch brute force; PC of the side CSP never refutes a yes-instance;
compare the side-CSP PC with pcfast on the ZZ conversion (dc-algorithm/pcfast.py, read-only import).
Usage: python test_sw.py SEED COUNT"""
import os
import sys
import random
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "dc-hardness"))
sys.path.insert(0, os.path.join(HERE, "..", "dc-algorithm"))
import sw  # noqa: E402
import twoch  # noqa: E402
import swlib  # noqa: E402
import pcfast  # noqa: E402

seed, count = int(sys.argv[1]), int(sys.argv[2])
rng = random.Random(seed)
stats = {}
t0 = time.time()
for it in range(count):
    inst = sw.random_p2_instance(rng, rng.randint(3, 6), rng.randint(2, 7), rng.uniform(0.1, 0.4), rng.uniform(0.1, 0.4))
    b = twoch.solve(inst) is not None
    e = sw.exact(inst)
    L, paths = sw.shortest_valid_paths(inst)
    assert b == e == (L is not None), (b, e, L, sw.fmt(inst))
    for p in paths:
        assert sw.is_valid_walk(inst, p)
    pcs = sw.pc_side(inst)
    if b:
        assert pcs
    z, _ = swlib.to_zz(inst)
    pcz = pcfast.pc_answer(z)
    key = (b, pcs, pcz)
    stats[key] = stats.get(key, 0) + 1
print("seed", seed, "count", count, "(exact, PC side CSP, PC zz):", stats, "%.1fs" % (time.time() - t0))
