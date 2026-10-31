"""Theorem 8.2 on instances with many bad pairs (badgen.design), r5-core.md Section 8.4.

usage: python test_bad.py SEED COUNT [LIMIT] [decide]
For each random design (path of 6-12 members, 2-6 x's above sets of E-members, 2-6 y's below sets of F-members,
y < x with probability 0.6-1, random P2 completion with node and middle witnesses): P2 is verified (gcore.p2_bad), the
shortest valid paths are computed exactly (gcore BFS), and on each (at most LIMIT) the proof of Theorem 8.2 is run
(inter.levels, every claim checked) together with the bad-pair statistics and inter.min_single.  With 'decide' the
exhaustive single-term GDESC (gdesc.decide(G, 1, 1, 2)) is run as well (sound; reports how often one small term fails).
"""
import sys
import random
import time
from collections import Counter
import gstar
import gdesc
import inter
from badgen import design


def one(rng, it):
    r = rng.choice([6, 8, 10, 12])
    types = "".join("EF"[i % 2] for i in range(r)) if rng.random() < 0.7 else "".join(rng.choice("EF") for _ in range(r))
    nA = types.count("E")
    nB = types.count("F")
    nX = rng.randint(2, 6)
    nY = rng.randint(2, 6)
    G = design(rng, types, nX, nY, rng.randint(1, max(1, nA)), rng.randint(1, max(1, nB)),
               p_xy=rng.choice([0.6, 0.8, 1.0]), n_extra=rng.randint(0, 4), style=rng.choice(["flip", "any"]),
               middle=rng.random() < 0.8, p_node=rng.choice([0.2, 0.5, 0.8]))
    return G


def main():
    seed, count = int(sys.argv[1]), int(sys.argv[2])
    limit = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    do_dec = len(sys.argv) > 4 and sys.argv[4] == "decide"
    rng = random.Random(seed)
    st = Counter()
    t0 = time.time()
    worst = []
    for it in range(count):
        G = one(rng, it)
        if G.p2_bad():
            st["P2 FAILS (generator bug)"] += 1
            continue
        st["inst"] += 1
        L, _ = G.shortest()
        if L is None:
            st["no"] += 1
            continue
        st["yes"] += 1
        if L == 0:
            continue
        St = gstar.Stars(G)
        paths = G.all_shortest(limit=limit, length=L)
        best = None
        for P in paths:
            K = gstar.Skel(G, P)
            st["paths"] += 1
            res = inter.levels(G, P, St, K)
            if res["errors"]:
                st["ERRORS"] += 1
                print("ERROR it=%d P=%s %s" % (it, P, res["errors"][:4]), flush=True)
            st["levels=%d" % res["nlev"]] += 1
            res2 = inter.levels(G, P, St, K, rng=random.Random(1000 * seed + it))
            if res2["errors"]:
                st["ERRORS (sampled)"] += 1
                print("ERROR (sampled) it=%d P=%s %s" % (it, P, res2["errors"][:4]), flush=True)
            st["sampled levels=%d" % res2["nlev"]] += 1
            st["sample failures"] += res2.get("sample failures", 0)
            for lv in res2["levels"]:
                st["sampled max damage"] = max(st["sampled max damage"], lv.get("damage", 0))
                st["sampled max anchors"] = max(st["sampled max anchors"], lv.get("anchors", 0))
            for lv in res["levels"]:
                st["case " + lv.get("case", "?")] += 1
                st["max damage"] = max(st["max damage"], lv.get("damage", 0))
                st["max anchors"] = max(st["max anchors"], lv.get("anchors", 0))
                st["max tools"] = max(st["max tools"], lv.get("tools", 0))
                st["max heavy"] = max(st["max heavy"], lv.get("heavy", 0))
            _, cl = gstar.classify(G, P, St, K)
            kap = gstar.min_vertex_cover_bip(cl["bad"]) if cl["bad"] else 0
            st["bad pairs"] += len(cl["bad"])
            st["max kappa"] = max(st["max kappa"], kap)
            ms = inter.min_single(G, P, St, K)
            one_ok = ms["edmg"] == 0 or ms["fone"]
            if not one_ok:
                st["paths: no single proof-term"] += 1
            key = (0 if one_ok else 1, res["nlev"], kap)
            if best is None or key < best:
                best = key
        if best is not None:
            worst.append((best, it, G.m))
            if best[0]:
                st["inst: no path with a single proof-term"] += 1
        if do_dec and G.m <= 30:
            d = gdesc.decide(G, 1, 1, 2)
            st["decide(1,1,2) accepts"] += bool(d)
            st["decide(1,1,2) rejects"] += not d
        if (it + 1) % 50 == 0:
            print("  %d (%.0fs) %s" % (it + 1, time.time() - t0, dict(st)), flush=True)
    worst.sort(reverse=True)
    print("test_bad seed %d count %d limit %d (%.0fs)" % (seed, count, limit, time.time() - t0))
    for kk in sorted(st):
        print("  %-45s %s" % (kk, st[kk]))
    print("  worst (no single term, levels, kappa), it, m:", worst[:10])


if __name__ == "__main__":
    main()
