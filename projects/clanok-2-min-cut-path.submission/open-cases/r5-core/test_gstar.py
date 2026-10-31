"""Checks of r5-core.md Section 6 (Lemmas 6.2-6.4, Theorem 6.5) on random general ZZ + P2 instances.

usage: python test_gstar.py SEED COUNT NMIN NMAX [LIMIT] [decide]
For every P2 yes-instance and every shortest valid path (at most LIMIT per instance):
  * Lemma 6.3: |A & NE(Estar(x))| <= 9 for every x not in L, |B & NF(Fstar(y))| <= 9 for every y not in Up;
  * Lemma 6.4: no incomparable pair (x, y) in NF x NE is covered by neither Estar(x) nor Fstar(y);
  * pair classes, bad pairs, the vertex cover number kappa of the bad pairs;
  * LP cover numbers (cheap tools with anchors) and the ILP guided cost of GDESC, verified on the description;
  * optionally GDESC.decide(1, 1, 2) as an exact decision (sound) compared with brute force.
"""
import sys
import random
import time
from collections import Counter
import gcore
from gcore import from_inst
import gcert
import mixed
from common_r4 import from_zz
import gstar
import gdesc


def gen_instance(rng, nmin, nmax, it):
    nm = rng.randint(nmin, nmax)
    if it % 2 == 0:
        return gcert.random_inst(rng, nm=nm, p_order=rng.choice([0.2, 0.35, 0.5]), p_R=rng.choice([0.15, 0.25]))
    return from_zz(mixed.random_instance(rng, rng.choice(["lower", "upper", "mixed"]), nm=nm,
                                         p_order=rng.choice([0.25, 0.4]), p_tie=rng.choice([0.0, 0.5])))


def analyse_instance(G, st, limit, worst, name):
    L, _ = G.shortest()
    if L is None:
        st["no"] += 1
        return
    st["yes"] += 1
    if L == 0:
        return
    St = gstar.Stars(G)
    paths = G.all_shortest(limit=limit, length=L)
    best_inst = None
    for P in paths:
        K = gstar.Skel(G, P)
        st["paths"] += 1
        ce, cf = gstar.star_cost(G, St, K)
        st["max star cost"] = max(st["max star cost"], ce, cf)
        if ce > 9 or cf > 9:
            st["LEMMA 6.3 VIOLATED"] += 1
        K, cl = gstar.classify(G, P, St, K)
        if cl["incomp_fail"]:
            st["LEMMA 6.4 VIOLATED"] += 1
        for key in ("E", "F", "Ea", "Fa", "bad"):
            st["pairs " + key] += len(cl[key])
        kap = gstar.min_vertex_cover_bip(cl["bad"]) if cl["bad"] else 0
        if cl["bad"]:
            st["paths with bad pairs"] += 1
        st["max kappa"] = max(st["max kappa"], kap)
        g = gdesc.guided(G, P, St, K)
        if not g["verified"]:
            st["GUIDED NOT VERIFIED"] += 1
        st["max guided cost"] = max(st["max guided cost"], g["cost"])
        key = (kap, g["cost"])
        if best_inst is None or key < best_inst:
            best_inst = key
    if best_inst is not None:
        st["inst: least kappa over paths > 0"] += best_inst[0] > 0
        st["inst max least guided"] = max(st["inst max least guided"], best_inst[1])
        worst.append((best_inst, name))


def main():
    seed, count, nmin, nmax = (int(a) for a in sys.argv[1:5])
    limit = int(sys.argv[5]) if len(sys.argv) > 5 else 20
    do_decide = len(sys.argv) > 6 and sys.argv[6] == "decide"
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
        analyse_instance(G, st, limit, worst, "r%d" % it)
        if do_decide and G.m <= 12:
            ex = bool(G.brute())
            dec = gdesc.decide(G, 1, 1, 2)
            if dec and not ex:
                st["DECIDE UNSOUND"] += 1
            if ex and not dec:
                st["decide(1,1,2) misses"] += 1
            st["decided"] += 1
        if (it + 1) % 100 == 0:
            print("  %d instances (%.0fs) %s" % (it + 1, time.time() - t0, dict(st)), flush=True)
    worst.sort(reverse=True)
    print("seed %d count %d n %d-%d limit %d (%.0fs)" % (seed, count, nmin, nmax, limit, time.time() - t0))
    for k in sorted(st):
        print("  %-40s %s" % (k, st[k]))
    print("  worst (least kappa, least guided) per instance:", worst[:8])


if __name__ == "__main__":
    main()
