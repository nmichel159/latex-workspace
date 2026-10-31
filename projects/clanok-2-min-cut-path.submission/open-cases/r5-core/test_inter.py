"""Checks of r5-core.md Section 8 (Lemma 8.1, Theorem 8.2) with inter.levels on random instances and families.

usage: python test_inter.py random SEED COUNT NMIN NMAX [LIMIT]
       python test_inter.py families KMAX
For every P2 yes-instance and every shortest valid path (at most LIMIT per instance) the proof of Theorem 8.2 is run
(inter.levels): every claim of the proof is checked (duality for light rows, cover sizes <= k, anchors <= N, flips
<= 9 per tool, damage <= |A'|/2, each term contains L, the residue property, final D picks P and connects, levels
<= k).  Also: bad pairs, their vertex cover kappa (gstar), and whether one term suffices (inter.min_single).
"""
import os
import sys
import random
import time
from collections import Counter
import gcore
from gcore import from_inst
import gstar
import inter

HERE = os.path.dirname(os.path.abspath(__file__))
OC = os.path.dirname(HERE)


def gen_instance(rng, nmin, nmax, it):
    import gcert
    import mixed
    from common_r4 import from_zz
    nm = rng.randint(nmin, nmax)
    if it % 2 == 0:
        return gcert.random_inst(rng, nm=nm, p_order=rng.choice([0.2, 0.35, 0.5]), p_R=rng.choice([0.15, 0.25]))
    return from_zz(mixed.random_instance(rng, rng.choice(["lower", "upper", "mixed"]), nm=nm,
                                         p_order=rng.choice([0.25, 0.4]), p_tie=rng.choice([0.0, 0.5])))


def analyse(G, st, limit, name, worst, verbose=False):
    L, _ = G.shortest()
    if L is None:
        st["no"] += 1
        return
    st["yes"] += 1
    if L == 0:
        return
    St = gstar.Stars(G)
    paths = G.all_shortest(limit=limit, length=L)
    inst_best = None
    for P in paths:
        K = gstar.Skel(G, P)
        st["paths"] += 1
        r = inter.levels(G, P, St, K)
        if r["errors"]:
            st["ERRORS"] += 1
            print("ERROR %s P=%s: %s" % (name, P, r["errors"][:5]), flush=True)
        st["levels=%d" % r["nlev"]] += 1
        for lv in r["levels"]:
            st["case " + lv.get("case", "?")] += 1
            st["max tools"] = max(st["max tools"], lv.get("tools", 0))
            st["max anchors"] = max(st["max anchors"], lv.get("anchors", 0))
            st["max flips"] = max(st["max flips"], lv.get("flips", 0))
            st["max heavy"] = max(st["max heavy"], lv.get("heavy", 0))
            st["max damage"] = max(st["max damage"], lv.get("damage", 0))
        K2, cl = gstar.classify(G, P, St, K)
        kap = gstar.min_vertex_cover_bip(cl["bad"]) if cl["bad"] else 0
        st["max kappa"] = max(st["max kappa"], kap)
        if cl["bad"]:
            st["paths with bad pairs"] += 1
        ms = inter.min_single(G, P, St, K)
        one = (ms["edmg"] == 0) or ms["fone"]
        if not one:
            st["paths needing >= 2 terms (proof tools)"] += 1
        key = (r["nlev"], 0 if one else 1, kap)
        if inst_best is None or key < inst_best:
            inst_best = key
    if inst_best is not None:
        worst.append((inst_best, name))
        if inst_best[1]:
            st["inst: every path needs >= 2 terms"] += 1


def run_random(seed, count, nmin, nmax, limit):
    rng = random.Random(seed)
    st = Counter()
    worst = []
    t0 = time.time()
    for it in range(count):
        I = gen_instance(rng, nmin, nmax, it)
        if not I.p2():
            continue
        st["P2"] += 1
        G, _ = from_inst(I)
        analyse(G, st, limit, "r%d" % it, worst)
        if (it + 1) % 100 == 0:
            print("  %d instances (%.0fs) %s" % (it + 1, time.time() - t0, dict(st)), flush=True)
    worst.sort(reverse=True)
    print("random seed %d count %d n %d-%d limit %d (%.0fs)" % (seed, count, nmin, nmax, limit, time.time() - t0))
    for kk in sorted(st):
        print("  %-45s %s" % (kk, st[kk]))
    print("  worst (levels, needs>=2 terms, kappa) per instance:", worst[:8])


def run_families(kmax, limit=40):
    sys.path.insert(0, os.path.join(OC, "r4-general"))
    import yfam
    import xfam
    import zfam
    from fool import yd
    from wfam import wfam
    from obfam import ob
    st = Counter()
    worst = []
    t0 = time.time()
    insts = []
    for k in range(2, kmax + 1):
        for contact in (False, True):
            I, full, info = yfam.yfam(k, contact=contact)
            insts.append(("Y%s_%d" % ("'" if contact else "", k), from_inst(I)[0]))
            for back in (False, True):
                Gd, _ = yd(k, back=back, contact=contact)
                insts.append(("Y%s^d_%d back=%s" % ("'" if contact else "", k, back), Gd))
    for L in range(2, 2 * kmax + 1):
        I, full, info = xfam.xfam(L)
        insts.append(("X_%d" % L, from_inst(I)[0]))
    for k in range(2, kmax + 1):
        for B in (False, True):
            try:
                I = zfam.zfam(k, B) if B else zfam.zfam(k)
                if isinstance(I, tuple):
                    I = I[0]
                insts.append(("Z%s_%d" % ("^B" if B else "", k), from_inst(I)[0]))
            except Exception as e:          # noqa: BLE001
                print("zfam", k, B, "skipped:", e)
    for n in (1, 2, 3):
        for pairing in ("F", "E"):
            try:
                G = wfam(n, pairing=pairing)
                if isinstance(G, tuple):
                    G = G[0]
                insts.append(("W_%d %s" % (n, pairing), G))
            except Exception as e:          # noqa: BLE001
                print("wfam", n, pairing, "skipped:", e)
    for args in ((2, 2, 2, 1, 1), (3, 3, 3, 2, 1)):
        try:
            G = ob(*args)
            if isinstance(G, tuple):
                G = G[0]
            if hasattr(G, "realise"):
                G = G.realise()[0]
            insts.append(("OB%s" % (args,), G))
        except Exception as e:              # noqa: BLE001
            print("ob", args, "skipped:", e)
    for name, G in insts:
        before = st["ERRORS"]
        analyse(G, st, limit, name, worst)
        print("  %s: m=%d errors=%d" % (name, G.m, st["ERRORS"] - before), flush=True)
    print("families kmax %d (%.0fs)" % (kmax, time.time() - t0))
    for kk in sorted(st):
        print("  %-45s %s" % (kk, st[kk]))
    worst.sort(reverse=True)
    print("  worst:", worst[:8])


def main():
    mode = sys.argv[1]
    if mode == "random":
        seed, count, nmin, nmax = (int(a) for a in sys.argv[2:6])
        limit = int(sys.argv[6]) if len(sys.argv) > 6 else 20
        run_random(seed, count, nmin, nmax, limit)
    else:
        run_families(int(sys.argv[2]))


if __name__ == "__main__":
    main()
