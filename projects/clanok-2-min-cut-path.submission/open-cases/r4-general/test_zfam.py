"""Checks of the two-route family Z_k (zfam.py): P2, solutions, pruning, side-set searches.
Usage: python test_zfam.py KMIN KMAX [nocontact]"""
import sys
import time
from common_r4 import gcert
from zfam import zfam
from xfam import brute
from gsw import GSW, prune, pruned_copy, decide_refined
from ng import ng

kmin, kmax = int(sys.argv[1]), int(sys.argv[2])
contact = "nocontact" not in sys.argv[3:]
block = "block" in sys.argv[3:]
LADDER = [(1, 0, 1, 3), (1, 0, 2, 6), (1, 1, 2, 6), (2, 0, 2, 6), (2, 1, 4, 8)]
for k in range(kmin, kmax + 1):
    t0 = time.time()
    I, names, info = zfam(k, contact=contact, block=block)
    G = GSW(I)
    nsw = len(info["E"])
    nsol = len(brute(info)) if nsw <= 18 else None
    ex = gcert.exact(I)
    fixed, dead = prune(G)
    H = pruned_copy(G, dead) if dead is not None else None
    line = "Z%s_%d%s q=%d switches=%d P2=%s solutions=%s exact=%s fixed=%d" % (
        "^B" if block else "", k, "" if contact else " nocontact", I.n, nsw, I.p2(), nsol, ex, len(fixed))
    found = None
    for par in LADDER:
        if H is not None and H.decide(*par):
            found = par
            break
    line += " | pruned side-set: %s" % (found,)
    line += " | NG(2)=%s" % (ng(I, 2, 0) is not None)
    line += " | %.1fs" % (time.time() - t0)
    print(line, flush=True)
