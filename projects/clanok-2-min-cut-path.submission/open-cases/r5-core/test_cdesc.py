"""CDESC (cdesc.py) on the known families and on random core instances.

For every yes-instance: guided flip cost (least over the shortest valid paths, at most LIMIT paths) with 0, 1, 2
centres, on the better side; and for small instances the exact enumeration decide(fmax, emax).
Families: Y_k, Y'_k (r4-general/yfam), Y^d_k, Y'^d_k (fool.py, both back variants), X_L (xfam), Z_k, Z^B_k (zfam),
the r4-search instances (json).  Random: generators of r4-general/test_core.py; only P2 yes-instances in the core
(propagation leaves comparable free switches) are reported separately.
Usage: python test_cdesc.py families [KMAX]
       python test_cdesc.py random SEED COUNT NMIN NMAX
"""
import os
import sys
import glob
import json
import random
import time
from collections import Counter
import gcore
from gcore import Gen, from_inst, to_inst
import cdesc
import gcert
import mixed
from common_r4 import from_zz, load_json
from gsw import GSW, prune, reduce_to_2ch

LIMIT = 60
HERE = os.path.dirname(os.path.abspath(__file__))
OC = os.path.dirname(HERE)


def analyse(G, name, decide_par=(1, 1), small=40, out=None):
    L, path = G.shortest()
    if L is None:
        r = cdesc.decide(G, 1, 1) if G.m <= small else None
        msg = "%s: no-instance (m=%d) decide=%s" % (name, G.m, r)
        print(msg, flush=True)
        if r:
            raise AssertionError("UNSOUND")
        return None
    paths = G.all_shortest(limit=LIMIT, length=L)
    cs = (cdesc.centre_sets(G, 0), cdesc.centre_sets(G, 1))
    best = {0: None, 1: None, 2: None}
    for P in paths:
        g = cdesc.guided(G, P, 2 if G.m <= 30 else 1, cs=cs)
        for f, v in g.items():
            if best[f] is None or v[0] < best[f][0]:
                best[f] = v
    dec = None
    if G.m <= small:
        dec = cdesc.decide(G, *decide_par, want=True)
        if dec[0]:
            side, cents, Phi, D = dec[1]
            assert G.connects(D)
            dec = ("ok", "EF"[side], cents, Phi)
        else:
            dec = ("fail",)
    msg = "%s: m=%d len=%d paths=%d guided f0=%s f1=%s f2=%s decide%s=%s" % (
        name, G.m, L, len(paths), best[0][:2] if best[0] else None, best[1][:2] if best[1] else None,
        best[2][:2] if best[2] else None, decide_par, dec)
    print(msg, flush=True)
    return best, dec


def families(kmax):
    sys.path.insert(0, os.path.join(OC, "r4-general"))
    import yfam
    import xfam
    import zfam
    from fool import yd
    for k in range(2, kmax + 1):
        for contact in (False, True):
            I, full, info = yfam.yfam(k, contact=contact)
            G, _ = from_inst(I)
            analyse(G, "Y%s_%d" % ("'" if contact else "", k))
            for back in (False, True):
                Gd, _ = yd(k, back=back, contact=contact)
                analyse(Gd, "Y%s^d_%d back=%s" % ("'" if contact else "", k, back))
    for L in range(2, 2 * kmax + 1):
        I, full, info = xfam.xfam(L)
        G, _ = from_inst(I)
        analyse(G, "X_%d" % L)
    for k in range(2, min(kmax, 4) + 1):
        for block in (False, True):
            I, full, info = zfam.zfam(k, block=block)
            G, _ = from_inst(I)
            analyse(G, "Z%s_%d" % ("^B" if block else "", k), small=0)
    for p in sorted(glob.glob(os.path.join(OC, "r4-search", "instances", "*.json"))):
        I, d = load_json(p)
        if not I.p2():
            print("%s: no P2, skipped" % os.path.basename(p))
            continue
        G, _ = from_inst(I)
        analyse(G, os.path.basename(p), small=24)


def gen_instance(rng, nmin, nmax, it):
    nm = rng.randint(nmin, nmax)
    if it % 2 == 0:
        I = gcert.random_inst(rng, nm=nm, p_order=rng.choice([0.2, 0.35, 0.5]), p_R=rng.choice([0.15, 0.25]))
    else:
        I = from_zz(mixed.random_instance(rng, rng.choice(["lower", "upper", "mixed"]), nm=nm,
                                          p_order=rng.choice([0.25, 0.4]), p_tie=rng.choice([0.0, 0.5])))
    return I


def random_run(seed, count, nmin, nmax):
    rng = random.Random(seed)
    st = Counter()
    worst = Counter()
    t0 = time.time()
    for it in range(count):
        I = gen_instance(rng, nmin, nmax, it)
        if not I.p2():
            continue
        st["P2"] += 1
        G, G0 = from_inst(I)
        L, path = G.shortest()
        if L is None:
            st["no"] += 1
            if G.m <= 14 and cdesc.decide(G, 1, 1):
                raise AssertionError("UNSOUND on a no-instance")
            continue
        st["yes"] += 1
        if L == 0:
            st["trivial s=t"] += 1
            continue
        fixed, dead = prune(G0)
        inst, free, reason = reduce_to_2ch(G0, fixed)
        core = inst is None
        if core:
            st["core"] += 1
        paths = G.all_shortest(limit=LIMIT, length=L)
        cs = (cdesc.centre_sets(G, 0), cdesc.centre_sets(G, 1))
        b1 = None
        b0 = None
        for P in paths:
            g = cdesc.guided(G, P, 1, cs=cs)
            if b0 is None or g[0][0] < b0:
                b0 = g[0][0]
            if b1 is None or g[1][0] < b1:
                b1 = g[1][0]
        worst["f1 cost %d" % b1] += 1
        if core:
            worst["core f1 cost %d" % b1] += 1
        if b1 > 1 and G.m <= 18:
            ok = cdesc.decide(G, 1, 2)
            st["decide(1,2) on guided>1: %s" % ok] += 1
    print("seed %d count %d n %d-%d: %s | %s | %.0fs" % (seed, count, nmin, nmax, dict(st), dict(sorted(worst.items())),
                                                       time.time() - t0), flush=True)


if __name__ == "__main__":
    if sys.argv[1] == "families":
        families(int(sys.argv[2]) if len(sys.argv) > 2 else 5)
    else:
        random_run(*(int(a) for a in sys.argv[2:6]))
