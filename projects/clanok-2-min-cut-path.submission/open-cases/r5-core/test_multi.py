"""Multi-level runs of the proof of Theorem 8.2 (r5-core.md Section 8.4).

usage: python test_multi.py SEED COUNT NMIN NMAX [LIMIT]
Designs (badgen.design) with a long alternating planted path of 2n members (n E-members, so that |A| >= 2k and
pivots of damage 1 are light), x_i above 1-2 random E-members, y_j below 1-3 random F-members, every y below every
x, random P2 completion.  On every shortest valid path (at most LIMIT) the proof is run three times:
  ilp      least covers (inter.levels),
  sample   covers drawn as in the proof from the optimal strategies, light tools pivoted (rng),
  kth=1    sample mode with the light threshold |A'|/2 instead of |A'|/(2k) (exercises the recursion; the bounds of
           the proof are not claimed then, only the logic: every term contains L, residue property, final D picks P).
"""
import sys
import random
import time
from collections import Counter
import gstar
import inter
from badgen import design


def main():
    seed, count, nmin, nmax = (int(a) for a in sys.argv[1:5])
    limit = int(sys.argv[5]) if len(sys.argv) > 5 else 4
    rng = random.Random(seed)
    st = Counter()
    t0 = time.time()
    for it in range(count):
        n = rng.randint(nmin, nmax)
        types = "EF" * n
        G = design(rng, types, rng.randint(3, 6), rng.randint(3, 6), rng.randint(1, 2), rng.randint(1, 3),
                   p_xy=1.0, n_extra=rng.randint(0, 3), style="flip", middle=rng.random() < 0.7,
                   p_node=rng.choice([0.3, 0.6]))
        if G.p2_bad():
            st["P2 FAILS"] += 1
            continue
        L, _ = G.shortest()
        if L is None:
            st["no"] += 1
            continue
        st["yes"] += 1
        St = gstar.Stars(G)
        for P in G.all_shortest(limit=limit, length=L):
            K = gstar.Skel(G, P)
            st["paths"] += 1
            st["max |A|"] = max(st["max |A|"], bin(K.A).count("1"))
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
                                                    or e.startswith("anchors"))]
                    st["kth=1 no progress"] += sum(1 for e in errs if e.startswith("no progress"))
                    errs = [e for e in errs if not e.startswith("no progress")]
                if errs:
                    st["ERRORS " + mode] += 1
                    print("ERROR %s it=%d %s" % (mode, it, errs[:4]), flush=True)
                st["%s levels=%d" % (mode, res["nlev"])] += 1
                st[mode + " sample failures"] += res.get("sample failures", 0)
                for lv in res["levels"]:
                    st["%s max damage" % mode] = max(st["%s max damage" % mode], lv.get("damage", 0))
        if (it + 1) % 10 == 0:
            print("  %d (%.0fs) %s" % (it + 1, time.time() - t0, dict(st)), flush=True)
    print("test_multi seed %d count %d n %d-%d limit %d (%.0fs)" % (seed, count, nmin, nmax, limit, time.time() - t0))
    for kk in sorted(st):
        print("  %-40s %s" % (kk, st[kk]))


if __name__ == "__main__":
    main()
