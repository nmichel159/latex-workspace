"""Pruning by forced-exit propagation followed by the side-set search (r4-general.md §7.3).

Usage: python test_pruned.py families KD KS S B
       python test_pruned.py random SEED COUNT KD KS S B
For each instance: number of switches fixed by the pruning, number of dead sides, and the search on the pruned copy.
Completeness check of the pruning: the dead sides must not be used by any solution (checked by brute force over the
order-consistent mode vectors when there are at most 14 switches).
"""
import os
import sys
import glob
import time
import random
from common_r4 import OC, gcert, from_zz, load_json
from gsw import GSW, prune, pruned_copy
from xfam import xfam
from yfam import yfam
import families
import ladder
import hubimp
import test_gsw


def check_dead(G, dead):
    if G.m > 14:
        return None
    for mask in G.brute():
        for w in range(G.m):
            side = 2 * w + ((mask >> w) & 1)
            if side in dead:
                return False
    return True


def one(name, I, known, kd, ks, s, B):
    t0 = time.time()
    G = GSW(I)
    fixed, dead = prune(G)
    ex = known if known is not None else gcert.exact(I)
    if dead is None:
        res, ok = False, None
    else:
        ok = check_dead(G, dead)
        H = pruned_copy(G, dead)
        res = H.decide(kd, ks, s, B)
    flag = ""
    if res and not ex:
        flag = " <-- UNSOUND"
    if ok is False:
        flag += " <-- PRUNING WRONG"
    if not res and ex:
        flag += " (fails)"
    print("%-18s q=%4d switches=%3d fixed=%3d dead=%3s exact=%-5s pruned-search=%-5s dead-ok=%s %.1fs%s"
          % (name, I.n, G.m, len(fixed), "-" if dead is None else len(dead), ex, res, ok, time.time() - t0, flag),
          flush=True)
    return flag


def families_run(kd, ks, s, B):
    insts = []
    for L in range(2, 11):
        insts.append(("X_%d" % L, xfam(L, "both")[0], True))
    for k in range(2, 9):
        insts.append(("Y_%d" % k, yfam(k)[0], True))
        insts.append(("Y'_%d" % k, yfam(k, contact=True)[0], True))
    for L in range(2, 9):
        for m in ("tie", "oneway"):
            insts.append(("T_%d^%s" % (L, m), families.tic_rigid(L, m)[0], True))
            insts.append(("RM_%d^%s" % (L, m), families.rigid(L, m, True)[0], True))
        insts.append(("R_%d 2CH" % L, families.rigid(L, None, False)[0], True))
    for k in range(2, 6):
        insts.append(("K(%d)" % k, from_zz(ladder.ladder(k)[0]), True))
    for m, mp in [(1, 1), (2, 2), (2, 3)]:
        for strict in (False, True):
            insts.append(("H(%d,%d)%s" % (m, mp, "po" if strict else "cl"),
                          from_zz(hubimp.hubimp(m, mp, strict=strict)[0]), False))
    for f in sorted(glob.glob(os.path.join(OC, "r4-search", "instances", "*.json"))):
        I, d = load_json(f)
        insts.append((os.path.basename(f)[:-5], I, None))
    bad = 0
    for name, I, known in insts:
        if one(name, I, known, kd, ks, s, B):
            bad += 1
    print("instances %d, flagged %d" % (len(insts), bad))


def random_run(seed, count, kd, ks, s, B):
    rng = random.Random(seed)
    n = bad = 0
    for it in range(count):
        kind = ("gc", "mx", "sw")[it % 3]
        I = test_gsw.gen(rng, kind)
        if not I.p2():
            continue
        n += 1
        G = GSW(I)
        fixed, dead = prune(G)
        ex = gcert.exact(I)
        if dead is None:
            if ex:
                print("PRUNING REFUTED A YES-INSTANCE", gcert.describe(I))
                bad += 1
            continue
        ok = check_dead(G, dead)
        H = pruned_copy(G, dead)
        res = H.decide(kd, ks, s, B)
        if ok is False or (res and not ex) or (ex and not res):
            print("FLAG kind=%s exact=%s res=%s dead-ok=%s: %s" % (kind, ex, res, ok, gcert.describe(I)))
            bad += 1
    print("random seed %d: %d P2 instances, flagged %d" % (seed, n, bad))


if __name__ == "__main__":
    if sys.argv[1] == "families":
        families_run(*(int(a) for a in sys.argv[2:6]))
    else:
        random_run(*(int(a) for a in sys.argv[2:8]))
