"""Find and print a rigid-word design on which the proof of Theorem 8.2 uses two levels (r5-core.md Section 8.4).

usage: python show_levels.py SEED COUNT NMIN NMAX OUT.json
Generates designs with test_rgen.make; for the first instance and shortest valid path on which inter.levels (ILP
covers) uses at least two levels, prints the levels (case, game value, tools with pivots, damage, residue sizes) and
the names of the switches involved, saves the instance (hunt_single.save), and checks the final intersection.
"""
import sys
import random
from gcore import bits
import gstar
import inter
from test_rgen import make
from hunt_single import save


def main():
    seed, count, nmin, nmax = (int(a) for a in sys.argv[1:5])
    out = sys.argv[5]
    rng = random.Random(seed)
    for it in range(count):
        G, W, pp = make(rng, rng.randint(nmin, nmax))
        if G.p2_bad():
            continue
        Lsh, _ = G.shortest()
        if not Lsh:
            continue
        St = gstar.Stars(G)
        for P in G.all_shortest(limit=5, length=Lsh):
            K = gstar.Skel(G, P)
            res = inter.levels(G, P, St, K)
            if res["nlev"] < 2:
                continue
            nm = lambda mask: [G.names[w] for w in bits(mask)]
            print("it=%d W=%s m=%d k=%d N=%d |P|=%d |A|=%d |B|=%d errors=%s" % (
                it, W, G.m, res["k"], res["N"], len(P), bin(K.A).count("1"), bin(K.B).count("1"), res["errors"]))
            _, cl = gstar.classify(G, P, St, K)
            print("bad pairs %d, kappa %d" % (len(cl["bad"]), gstar.min_vertex_cover_bip(cl["bad"])))
            for i, lv in enumerate(res["levels"]):
                print("level %d: %s" % (i + 1, lv))
            print("final D picks P: %s, connects: %s" % (res["picks"], res["connects"]))
            save(G, out, dict(W=W, P=P, seed=seed, it=it))
            return
    print("none found")


if __name__ == "__main__":
    main()
