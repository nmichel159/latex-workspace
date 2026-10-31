"""NG on random instances: soundness (every accepted down-set is re-checked; NG never accepts a no-instance) and the
completeness rate per budget.

Usage: python test_ng_random.py SEED COUNT
Families: 'gc'  = gcert.random_inst (general preorders, ties, middle edges, P2 completion);
          'mx'  = mixed.random_instance with lower / upper / mixed witness directions;
          'sw'  = twoch.random_p2_instance converted by swlib.to_zz (switch model).
Exact answer: gcert.exact (DFS) and, for q <= 20, the enumeration of all down-sets.
"""
import sys
import random
import time
from common_r4 import gcert, from_zz, check_solution
import mixed
import twoch
import swlib
from ng import ng

seed, count = int(sys.argv[1]), int(sys.argv[2])
rng = random.Random(seed)
BUDGETS = (0, 1, 2)


def gen(kind):
    if kind == "gc":
        return gcert.random_inst(rng)
    if kind == "mx":
        mode = rng.choice(["lower", "upper", "mixed", "mixed"])
        return from_zz(mixed.random_instance(rng, mode))
    N = rng.randint(3, 7)
    n = rng.randint(2, 8)
    inst = twoch.random_p2_instance(rng, N, n, rng.choice([0.2, 0.35, 0.5]), rng.choice([0.2, 0.35, 0.5]))
    z, names = swlib.to_zz(inst)
    return from_zz(z)


stats = {}
t0 = time.time()
bad = 0
for it in range(count):
    kind = ("gc", "mx", "sw")[it % 3]
    I = gen(kind)
    if not I.p2():
        continue
    ex = gcert.exact(I)
    if I.n <= 20:
        ex2 = gcert.exact_downsets(I)
        if ex2 != ex:
            print("EXACT MISMATCH", kind, gcert.describe(I))
            bad += 1
    key = (kind, ex)
    st = stats.setdefault(key, [0] + [0] * len(BUDGETS))
    st[0] += 1
    for j, b in enumerate(BUDGETS):
        r = ng(I, b, 0)
        if r is not None:
            if not ex or not check_solution(I, r[1]):
                print("UNSOUND", kind, b, gcert.describe(I))
                bad += 1
            st[1 + j] += 1
            # larger budgets succeed too (they include the smaller ones)
            for jj in range(j + 1, len(BUDGETS)):
                st[1 + jj] += 1
            break
print("seed %d, %d instances generated, %.0fs, violations %d" % (seed, count, time.time() - t0, bad))
for (kind, ex), st in sorted(stats.items()):
    print("  %-3s %-5s n=%5d  " % (kind, ex, st[0]) + "  ".join("NG(%d): %d" % (b, st[1 + j])
                                                            for j, b in enumerate(BUDGETS)))
