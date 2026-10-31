"""Checks of gsw.py (side-set certificates with conflict families, r4-general.md §5).

Usage: python test_gsw.py random SEED COUNT        (random general instances: conversion, soundness, completeness)
       python test_gsw.py families KD KS S B        (known families and r4-search instances)
"""
import os
import sys
import glob
import time
import random
from common_r4 import OC, gcert, from_zz, load_json
from gsw import GSW
import mixed
import twoch
import swlib
import families
import ladder
import hubimp
from xfam import xfam


def gen(rng, kind):
    if kind == "gc":
        return gcert.random_inst(rng)
    if kind == "mx":
        return from_zz(mixed.random_instance(rng, rng.choice(["lower", "upper", "mixed", "mixed"])))
    N = rng.randint(3, 7)
    n = rng.randint(2, 8)
    inst = twoch.random_p2_instance(rng, N, n, rng.choice([0.2, 0.35, 0.5]), rng.choice([0.2, 0.35, 0.5]))
    z, names = swlib.to_zz(inst)
    return from_zz(z)


def run_random(seed, count):
    rng = random.Random(seed)
    stats = {}
    bad = 0
    t0 = time.time()
    for it in range(count):
        kind = ("gc", "mx", "sw")[it % 3]
        I = gen(rng, kind)
        if not I.p2():
            continue
        ex = gcert.exact(I)
        G = GSW(I)
        if G.m <= 14:
            bx = bool(G.brute())
            if bx != ex:
                print("CONVERSION MISMATCH", kind, gcert.describe(I))
                bad += 1
        key = (kind, ex)
        st = stats.setdefault(key, [0, 0, 0])
        st[0] += 1
        r1 = G.decide(1, 0, 2, 6)
        r2 = r1 or G.decide(1, 1, 4, 8)
        if (r1 or r2) and not ex:
            print("UNSOUND", kind, gcert.describe(I))
            bad += 1
        st[1] += r1
        st[2] += r2
    print("seed %d count %d: %.0fs, violations %d" % (seed, count, time.time() - t0, bad))
    for (kind, ex), st in sorted(stats.items()):
        print("  %-3s %-5s n=%5d  (1,0,2,6): %d  (1,1,4,8): %d" % (kind, ex, st[0], st[1], st[2]))


def run_families(kd, ks, s, B):
    insts = []
    for L in range(2, 9):
        insts.append(("X_%d" % L, xfam(L, "both")[0], True))
    for L in range(2, 8):
        for m in ("tie", "oneway"):
            insts.append(("T_%d^%s" % (L, m), families.tic_rigid(L, m)[0], True))
    for L in range(2, 8):
        for m in ("tie", "oneway"):
            insts.append(("RM_%d^%s" % (L, m), families.rigid(L, m, True)[0], True))
        insts.append(("R_%d 2CH" % L, families.rigid(L, None, False)[0], True))
    for k in range(2, 6):
        insts.append(("K(%d)" % k, from_zz(ladder.ladder(k)[0]), True))
        insts.append(("KW(%d)" % k, from_zz(ladder.ladder(k, True)[0]), True))
    for m, mp in [(1, 1), (2, 2), (2, 3)]:
        for strict in (False, True):
            insts.append(("H(%d,%d)%s" % (m, mp, "po" if strict else "cl"),
                          from_zz(hubimp.hubimp(m, mp, strict=strict)[0]), False))
    for f in sorted(glob.glob(os.path.join(OC, "r4-search", "instances", "*.json"))):
        I, d = load_json(f)
        insts.append((os.path.basename(f)[:-5], I, None))
    nfail = 0
    for name, I, known in insts:
        t0 = time.time()
        G = GSW(I)
        ex = known if known is not None else gcert.exact(I)
        st = {}
        r = G.decide(kd, ks, s, B, want_walk=True, stats=st)
        flag = ""
        if r[0] and not ex:
            flag = " <-- UNSOUND"
        if not r[0] and ex:
            flag = " (fails)"
            nfail += 1
        cert = "" if not r[0] else " KE dom %s singles %s | KF dom %s singles %s" % (
            r[1][0][0], r[1][0][1], r[1][1][0], r[1][1][1])
        print("%-22s q=%3d switches=%3d sides=%3d exact=%-5s side-set=%-5s tried=%6d %6.1fs%s%s"
              % (name, I.n, G.m, len(G.sides), ex, r[0], st.get("tried", 0), time.time() - t0, cert, flag),
              flush=True)
    print("failures:", nfail)


if __name__ == "__main__":
    if sys.argv[1] == "random":
        run_random(int(sys.argv[2]), int(sys.argv[3]))
    else:
        run_families(*(int(a) for a in sys.argv[2:6]))
