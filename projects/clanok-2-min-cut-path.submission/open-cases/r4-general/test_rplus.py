"""Theorem R+ check: branch on a vertex cover of the comparability graph of the free switches (after propagation),
contract each branch (Theorem R), solve the 2CH instances by brute force (r4-switch sw.brute) and by r4-switch's
alg.decide(1, 1, 4, 8); the instance is yes iff some branch is.  Compared with the exact answer.
Usage: python test_rplus.py SEED COUNT NMIN NMAX"""
import os
import sys
import random
from collections import Counter
from common_r4 import OC, gcert, from_zz
from gsw import GSW, prune, free_comparability_cover, branches_R
import mixed
sys.path.insert(0, os.path.join(OC, "r4-switch"))
import sw as rsw     # noqa: E402
import alg as ralg   # noqa: E402

seed, count, nmin, nmax = (int(a) for a in sys.argv[1:5])
rng = random.Random(seed)
st = Counter()
cov = Counter()
for it in range(count):
    nm = rng.randint(nmin, nmax)
    if it % 2 == 0:
        I = gcert.random_inst(rng, nm=nm, p_order=rng.choice([0.2, 0.35, 0.5]), p_R=rng.choice([0.15, 0.25]))
    else:
        I = from_zz(mixed.random_instance(rng, rng.choice(["lower", "upper", "mixed"]), nm=nm,
                                          p_order=rng.choice([0.25, 0.4]), p_tie=rng.choice([0.0, 0.5])))
    if not I.p2():
        continue
    ex = gcert.exact(I)
    G = GSW(I)
    fixed, dead = prune(G)
    if dead is None:
        st["refuted by propagation", ex] += 1
        continue
    cover = free_comparability_cover(G, fixed)
    cov[len(cover)] += 1
    if len(cover) > 12:
        st["cover too large"] += 1
        continue
    ans_b = ans_a = False
    p2fail = 0
    for f2, inst, reason in branches_R(G, fixed, cover):
        if inst is None:
            p2fail += 1
            continue
        if rsw.brute(inst) is not None if len(inst[1]) <= 16 else ralg.decide(inst, 1, 1, 4, 8):
            ans_b = True
        if ralg.decide(inst, 1, 1, 4, 8):
            ans_a = True
        if ans_b and ans_a:
            break
    if p2fail:
        st["branch without P2 (should not happen)"] += 1
    st["agree" if ans_b == ex else "DISAGREE (brute)"] += 1
    st["alg agrees" if ans_a == ex else "alg disagrees"] += 1
print("seed %d: %s" % (seed, dict(st)))
print("  cover sizes:", dict(sorted(cov.items())))
