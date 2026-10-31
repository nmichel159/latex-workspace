"""Theorem R check: prune, contract the fixed sides, solve the resulting 2CH + P2 instance with r4-switch's algorithm
(alg.decide, read-only import) and by brute force (r4-switch/sw.py), compare with the exact answer of the ZZ instance.
Usage: python test_reduce.py families | random SEED COUNT"""
import os
import sys
import glob
import random
from common_r4 import OC, gcert, from_zz, load_json
sys.path.insert(0, os.path.join(OC, "r4-switch"))
import sw as rsw      # noqa: E402  (r4-switch, read-only)
import alg as ralg    # noqa: E402  (r4-switch, read-only)
from gsw import GSW, prune, reduce_to_2ch   # noqa: E402
from xfam import xfam   # noqa: E402
from yfam import yfam   # noqa: E402
from zfam import zfam   # noqa: E402
import families         # noqa: E402
import ladder           # noqa: E402
import hubimp           # noqa: E402
import test_gsw         # noqa: E402


def check(name, I, known=None, verbose=True):
    G = GSW(I)
    fixed, dead = prune(G)
    ex = known if known is not None else gcert.exact(I)
    if dead is None:
        line = "%-18s pruning refutes the instance; exact=%s" % (name, ex)
        bad = ex
    else:
        inst, free, reason = reduce_to_2ch(G, fixed)
        if inst is None:
            line = "%-18s fixed %d/%d: Theorem R does not apply (%s); exact=%s" % (name, len(fixed), G.m, reason, ex)
            bad = False
        else:
            a = ralg.decide(inst, 1, 1, 4, 8)
            b = (rsw.brute(inst) is not None) if len(free) <= 16 else None
            bad = (a != ex) or (b is not None and b != ex)
            line = ("%-18s fixed %d/%d, 2CH instance: %d switches, %d nodes, P2 ok; r4-switch alg=%s brute=%s exact=%s%s"
                    % (name, len(fixed), G.m, len(free), inst[0], a, b, ex, "  <-- MISMATCH" if bad else ""))
    if verbose:
        print(line, flush=True)
    return bad


def families_run():
    insts = []
    for L in range(2, 9):
        insts.append(("X_%d" % L, xfam(L, "both")[0], True))
    for k in range(2, 7):
        insts.append(("Y_%d" % k, yfam(k)[0], True))
        insts.append(("Y'_%d" % k, yfam(k, contact=True)[0], True))
    for k in range(2, 4):
        insts.append(("Z_%d" % k, zfam(k)[0], True))
    for L in range(2, 8):
        for m in ("tie", "oneway"):
            insts.append(("T_%d^%s" % (L, m), families.tic_rigid(L, m)[0], True))
            insts.append(("RM_%d^%s" % (L, m), families.rigid(L, m, True)[0], True))
    for k in range(2, 6):
        insts.append(("K(%d)" % k, from_zz(ladder.ladder(k)[0]), True))
    for m, mp in [(1, 1), (2, 2)]:
        for strict in (False, True):
            insts.append(("H(%d,%d)%s" % (m, mp, "po" if strict else "cl"),
                          from_zz(hubimp.hubimp(m, mp, strict=strict)[0]), False))
    for f in sorted(glob.glob(os.path.join(OC, "r4-search", "instances", "*.json"))):
        I, d = load_json(f)
        insts.append((os.path.basename(f)[:-5], I, None))
    nbad = sum(1 for name, I, known in insts if check(name, I, known))
    print("instances %d, mismatches %d" % (len(insts), nbad))


def random_run(seed, count):
    rng = random.Random(seed)
    applies = n = bad = 0
    for it in range(count):
        I = test_gsw.gen(rng, ("gc", "mx", "sw")[it % 3])
        if not I.p2():
            continue
        n += 1
        G = GSW(I)
        fixed, dead = prune(G)
        if dead is not None and reduce_to_2ch(G, fixed)[0] is not None:
            applies += 1
        if check("random", I, verbose=False):
            bad += 1
            print("MISMATCH", gcert.describe(I))
    print("random seed %d: %d P2 instances, Theorem R applies to %d, mismatches %d" % (seed, n, applies, bad))


if __name__ == "__main__":
    if sys.argv[1] == "families":
        families_run()
    else:
        random_run(int(sys.argv[2]), int(sys.argv[3]))
