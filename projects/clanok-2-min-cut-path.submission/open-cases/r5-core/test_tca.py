"""Two-cheap-anchors statistic (tca.py) on 2CH and general instances and on the families.

usage: python test_tca.py sw SEED COUNT            (random, planted and critical-run 2CH + P2 instances)
       python test_tca.py gen SEED COUNT NMIN NMAX  (random general ZZ + P2 instances, generators of test_cdesc)
       python test_tca.py fam KMAX                  (families)
For every yes-instance: tca over at most LIMIT shortest valid paths (minimum over paths), the exact cost of the
corresponding anchored description (checkE / checkF), histograms.
"""
import os
import sys
import random
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
OC = os.path.dirname(HERE)
VR = os.path.join(OC, "verify", "r4-switch-review")

import gcore
from gcore import from_inst
import tca

LIMIT = 40


def inst_value(G, maxpaths=LIMIT):
    L, _ = G.shortest()
    if L is None or L == 0:
        return None
    paths = G.all_shortest(limit=maxpaths, length=L)
    best = None
    worst_check = 0
    for P in paths:
        r = tca.tca_path(G, P)
        ce = r["checkE"][0]
        cf = r["checkF"][0]
        act = min(ce, cf)
        if best is None or (r["tca"], act) < (best["tca"], best["act"]):
            best = dict(r)
            best["act"] = act
            best["P"] = P
    return best


def sw_instances(rng, count):
    sys.path.insert(0, VR)
    import core as vcore
    import planted as vplanted
    import gen_run as vgen
    out = []
    for it in range(count):
        kind = it % 3
        try:
            if kind == 0:
                N = rng.randint(4, 9)
                n = rng.randint(3, 9)
                inst = vcore.random_instance(rng, N, n, rng.choice([0.2, 0.3, 0.4]))
                inst = vcore.p2_repair(inst, rng, fresh=rng.random() < 0.5)
                tag = "random"
            elif kind == 1:
                res = vplanted.gen_planted(rng, rng.randint(2, 5), rng.randint(2, 5), rng.randint(2, 5),
                                           rng.randint(0, 3))
                inst = res[0] if isinstance(res, tuple) else res
                tag = "planted"
            else:
                kw = [rng.choice("TO") for _ in range(rng.randint(2, 5))]
                lw = [rng.choice("TO") for _ in range(rng.randint(3, 7))]
                res = vgen.gen_run(rng, kw, rng.randint(2, 6), lw, pM=rng.choice([0.4, 0.6, 0.8]),
                                   pB=rng.choice([0.0, 0.2, 0.4]), reverse=rng.random() < 0.5)
                if res is None:
                    continue
                inst = res[0] if isinstance(res, tuple) else res
                tag = "run"
        except Exception as ex:          # generator rejected the draw
            continue
        if inst is None or not vcore.p2(inst):
            continue
        out.append((tag, tca.from_core(inst)))
    return out


def run_sw(seed, count):
    rng = random.Random(seed)
    t0 = time.time()
    hist = Counter()
    mism = Counter()
    top = []
    for tag, G in sw_instances(rng, count):
        if G.m > 16:
            continue
        v = inst_value(G)
        if v is None:
            continue
        hist[(tag, v["tca"])] += 1
        if v["act"] > v["tca"]:
            mism[tag] += 1
        top.append((v["tca"], v["act"], tag, G.m, len(v["P"])))
    top.sort(reverse=True)
    print("sw seed %d count %d: tca histogram %s; actual>bound %s; top %s (%.0fs)" %
          (seed, count, dict(sorted(hist.items())), dict(mism), top[:8], time.time() - t0), flush=True)


def gen_instance(rng, nmin, nmax, it):
    import gcert
    import mixed
    from common_r4 import from_zz
    nm = rng.randint(nmin, nmax)
    if it % 2 == 0:
        return gcert.random_inst(rng, nm=nm, p_order=rng.choice([0.2, 0.35, 0.5]), p_R=rng.choice([0.15, 0.25]))
    return from_zz(mixed.random_instance(rng, rng.choice(["lower", "upper", "mixed"]), nm=nm,
                                         p_order=rng.choice([0.25, 0.4]), p_tie=rng.choice([0.0, 0.5])))


def run_gen(seed, count, nmin, nmax):
    rng = random.Random(seed)
    t0 = time.time()
    hist = Counter()
    act = Counter()
    top = []
    for it in range(count):
        I = gen_instance(rng, nmin, nmax, it)
        if not I.p2():
            continue
        G, _ = from_inst(I)
        v = inst_value(G)
        if v is None:
            continue
        hist[v["tca"]] += 1
        act[v["act"]] += 1
        top.append((v["act"], v["tca"], G.m, len(v["P"]), it))
    top.sort(reverse=True)
    print("gen seed %d count %d n %d-%d: tca bound histogram %s; actual description cost %s; top %s (%.0fs)" %
          (seed, count, nmin, nmax, dict(sorted(hist.items())), dict(sorted(act.items())), top[:8],
           time.time() - t0), flush=True)


def run_fam(kmax):
    sys.path.insert(0, os.path.join(OC, "r4-general"))
    import yfam
    import xfam
    import zfam
    from fool import yd
    from obfam import ob
    from wfam import wfam

    def show(name, G):
        v = inst_value(G, maxpaths=20)
        if v is None:
            print("%s: no / trivial" % name)
            return
        print("%s: m=%d len=%d |A|=%d |B|=%d tca=%d actual=%d costE=%s costF=%s checkE=%s checkF=%s" %
              (name, G.m, len(v["P"]), v["A"], v["B"], v["tca"], v["act"], v["costE"][0], v["costF"][0],
               v["checkE"], v["checkF"]), flush=True)
    for k in range(2, kmax + 1):
        for contact in (False, True):
            I, full, info = yfam.yfam(k, contact=contact)
            show("Y%s_%d" % ("'" if contact else "", k), from_inst(I)[0])
            for back in (False, True):
                Gd, _ = yd(k, back=back, contact=contact)
                show("Y%s^d_%d back=%s" % ("'" if contact else "", k, back), Gd)
    for L in range(2, 2 * kmax + 1):
        I, full, info = xfam.xfam(L)
        show("X_%d" % L, from_inst(I)[0])
    for k in range(2, min(kmax, 3) + 1):
        for block in (False, True):
            I, full, info = zfam.zfam(k, block=block)
            show("Z%s_%d" % ("^B" if block else "", k), from_inst(I)[0])
    for n in (1, 2):
        show("W_%d" % n, wfam(n)[0])
    for par in ((3, 3, 3, 2, 1), (4, 4, 4, 2, 2)):
        pl, info = ob(*par)
        show("OB%s" % (par,), pl.realise()[0])


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "sw":
        run_sw(int(sys.argv[2]), int(sys.argv[3]))
    elif mode == "gen":
        run_gen(*(int(a) for a in sys.argv[2:6]))
    else:
        run_fam(int(sys.argv[2]))
