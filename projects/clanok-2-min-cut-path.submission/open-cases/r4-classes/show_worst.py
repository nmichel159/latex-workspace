"""Regenerate the satc.py run (same seed and parameters) and print the structure (types, classes, kinds of the
partners, contacts, f-sets) of the first shortest path reaching hP >= THRESH.
Usage: python show_worst.py SEED COUNT LMIN LMAX KCLS THRESH [jsonout]"""
import os
import sys
import json
import random

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "r5-classes"))
import ccore as C  # noqa: E402
import satc  # noqa: E402

seed, count, lmin, lmax, kcls, thresh = (int(x) for x in sys.argv[1:7])
out = sys.argv[7] if len(sys.argv) > 7 else None
rng = random.Random(seed)
for it in range(count):
    L = rng.randint(lmin, lmax)
    word = "".join(rng.choice("EF") for _ in range(L))
    pl = satc.saturate(rng, word, kcls, 0.3)
    if pl is None:
        continue
    I, P0 = pl.realise()
    Ls, paths = C.shortest_valid_paths(I, limit=20)
    for P in paths:
        if satc.hP(I, P) >= thresh:
            f = satc.fsets(I, P)
            r = len(P)
            print("word", "".join("EF"[x & 1] for x in P), "hP", satc.hP(I, P), "planted" if tuple(P) == tuple(P0) else "")
            for a in range(r):
                x = P[a]
                m = I.mask.get(x ^ 1, 0)
                cont = [c for c in range(r) if c != a and m & I.mask[P[c]]]
                print("  pos %2d %s cls %-8s contacts %-40s f %s" % (a, "EF"[x & 1], I.cl[x >> 1], cont, sorted(f[a])))
            if out:
                json.dump({"inst": I.to_json(), "P": list(P)}, open(out, "w"))
            sys.exit(0)
print("not found")
