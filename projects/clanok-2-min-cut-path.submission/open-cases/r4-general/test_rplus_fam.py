"""Theorem R+ on the instances where Theorem R does not apply directly (hubs, two-route families)."""
import os
import sys
import time
from common_r4 import OC, gcert, from_zz
from gsw import GSW, prune, free_comparability_cover, branches_R
from zfam import zfam
import hubimp
sys.path.insert(0, os.path.join(OC, "r4-switch"))
import sw as rsw     # noqa: E402

insts = [("H(1,1)cl", from_zz(hubimp.hubimp(1, 1)[0]), False), ("H(2,2)cl", from_zz(hubimp.hubimp(2, 2)[0]), False),
         ("H(2,2)po", from_zz(hubimp.hubimp(2, 2, strict=True)[0]), False),
         ("Z_2", zfam(2)[0], True), ("Z^B_2", zfam(2, block=True)[0], True), ("Z_3", zfam(3)[0], True),
         ("Z^B_3", zfam(3, block=True)[0], True)]
for name, I, ex in insts:
    t0 = time.time()
    G = GSW(I)
    fixed, dead = prune(G)
    cover = free_comparability_cover(G, fixed)
    nb = yes = nop2 = 0
    for f2, inst, reason in branches_R(G, fixed, cover):
        nb += 1
        if inst is None:
            nop2 += 1
            continue
        if rsw.brute(inst) is not None:
            yes += 1
    print("%-9s switches=%d fixed=%d cover=%d branches=%d (P2 fails in %d) yes-branches=%d -> %s exact=%s %.1fs"
          % (name, G.m, len(fixed), len(cover), nb, nop2, yes, yes > 0, ex, time.time() - t0), flush=True)
