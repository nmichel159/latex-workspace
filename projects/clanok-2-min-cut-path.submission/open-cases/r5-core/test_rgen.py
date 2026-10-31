"""Theorem 8.2 on rigid-word designs with many bad pairs (rgen.rdesign), r5-core.md Section 8.4.

usage: python test_rgen.py SEED COUNT NMIN NMAX [decide]
Word W = (EF)^n (or a random word), x_i above random sets of E-members (sizes 1..3, or lines of a projective plane
when n = 7 or 13), y_j below random sets of F-members, y < x with probability p_xy, random witness options.
Checked: P2 (gcore.p2_bad); whether the planted path is a shortest valid path; on the planted path and on up to 3
other shortest valid paths: inter.levels in modes ilp / sample / kth=1 (claims of the proof), inter.min_single, bad
pairs and kappa; with 'decide' also the exhaustive single-term GDESC decide(G, 1, 1, 2).
"""
import sys
import random
import time
from collections import Counter
import gstar
import gdesc
import inter
from rgen import rdesign
from badgen import projective_lines


def make(rng, n):
    if rng.random() < 0.8:
        W = "EF" * n
    else:
        W = "".join(rng.choice("EF") for _ in range(2 * n))
        if "E" not in W or "F" not in W:
            W = "EF" * n
    Epos = [p for p in range(1, len(W) + 1) if W[p - 1] == "E"]
    Fpos = [p for p in range(1, len(W) + 1) if W[p - 1] == "F"]
    nX = rng.randint(2, 7)
    nY = rng.randint(2, 7)
    pp = len(Epos) in (7, 13) and len(Fpos) == len(Epos) and rng.random() < 0.5
    if pp:
        lines = projective_lines(2 if len(Epos) == 7 else 3)
        S_sets = [[Epos[i] for i in ln] for ln in rng.sample(lines, min(nX, len(lines)))]
        T_sets = [[Fpos[i] for i in ln] for ln in rng.sample(lines, min(nY, len(lines)))]
    else:
        S_sets = [rng.sample(Epos, rng.randint(1, min(3, len(Epos)))) for _ in range(nX)]
        T_sets = [rng.sample(Fpos, rng.randint(1, min(3, len(Fpos)))) for _ in range(nY)]
    G = rdesign(rng, W, S_sets, T_sets, p_xy=rng.choice([0.7, 1.0]), p_low=rng.choice([0, 0.5]),
                p_up=rng.choice([0, 0.5]), p_contact=rng.choice([0, 0.3]))
    return G, W, pp


def main():
    seed, count, nmin, nmax = (int(a) for a in sys.argv[1:5])
    do_dec = len(sys.argv) > 5 and sys.argv[5] == "decide"
    rng = random.Random(seed)
    st = Counter()
    t0 = time.time()
    worst = []
    for it in range(count):
        G, W, pp = make(rng, rng.randint(nmin, nmax))
        if G.p2_bad():
            st["P2 FAILS"] += 1
            print("P2 fails it=%d: %s" % (it, G.p2_bad()[:3]), flush=True)
            continue
        Lsh, _ = G.shortest()
        if Lsh is None:
            st["no"] += 1
            continue
        st["yes"] += 1
        st["projective"] += pp
        planted_ok = G.is_valid_walk(G.planted) and len(G.planted) == Lsh
        st["planted path shortest"] += planted_ok
        paths = ([G.planted] if planted_ok else []) + [P for P in G.all_shortest(limit=3, length=Lsh)
                                                         if P != G.planted]
        St = gstar.Stars(G)
        best = None
        for P in paths:
            K = gstar.Skel(G, P)
            st["paths"] += 1
            st["max |A|"] = max(st["max |A|"], bin(K.A).count("1"))
            nlev = {}
            for mode in ("ilp", "sample", "kth=1"):
                if mode == "ilp":
                    res = inter.levels(G, P, St, K)
                elif mode == "sample":
                    res = inter.levels(G, P, St, K, rng=random.Random(rng.random()))
                else:
                    res = inter.levels(G, P, St, K, rng=random.Random(rng.random()), kth=1)
                errs = res["errors"]
                if mode == "kth=1" and any(e.startswith("no progress") for e in errs):
                    st["kth=1 stopped without progress"] += 1
                    errs = []
                if mode == "kth=1":
                    errs = [e for e in errs if not (e.startswith("damage") or e.startswith("levels")
                                                    or e.startswith("E-cover") or e.startswith("F-cover")
                                                    or e.startswith("anchors") or e.startswith("no progress"))]
                if errs:
                    st["ERRORS " + mode] += 1
                    print("ERROR %s it=%d W=%s %s" % (mode, it, W, errs[:4]), flush=True)
                st["%s levels=%d" % (mode, res["nlev"])] += 1
                st[mode + " sample failures"] += res.get("sample failures", 0)
                nlev[mode] = res["nlev"]
                for lv in res["levels"]:
                    st["%s max damage" % mode] = max(st["%s max damage" % mode], lv.get("damage", 0))
                    st["%s max anchors" % mode] = max(st["%s max anchors" % mode], lv.get("anchors", 0))
            _, cl = gstar.classify(G, P, St, K)
            kap = gstar.min_vertex_cover_bip(cl["bad"]) if cl["bad"] else 0
            st["max kappa"] = max(st["max kappa"], kap)
            ms = inter.min_single(G, P, St, K)
            one_ok = ms["edmg"] == 0 or ms["fone"]
            st["paths: single proof-term"] += one_ok
            key = (0 if one_ok else 1, kap)
            if best is None or key < best:
                best = key
        if best is not None:
            worst.append((best, it, W, G.m))
        if do_dec and G.m <= 40:
            d = gdesc.decide(G, 1, 1, 2)
            st["decide(1,1,2) accepts"] += bool(d)
        if (it + 1) % 20 == 0:
            print("  %d (%.0fs) %s" % (it + 1, time.time() - t0, dict(st)), flush=True)
    worst.sort(reverse=True)
    print("test_rgen seed %d count %d n %d-%d (%.0fs)" % (seed, count, nmin, nmax, time.time() - t0))
    for kk in sorted(st):
        print("  %-40s %s" % (kk, st[kk]))
    print("  worst (no single term, kappa), it, W, m:", worst[:8])


if __name__ == "__main__":
    main()
