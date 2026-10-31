"""Tests of gcert.py.

Usage: python test_gcert.py SEED COUNT KMAX [flavour]
flavour: mixed (default) | ties (no order between middle classes) | poset (classes of size 1) | sw (2CH: middle
         antichain, no middle edges) | nomid (no R-edges between middle elements; any preorder)
Checks: own exact solver = enumeration of all down-sets (and = dc-algorithm/zz.exact_dfs); P2 by the definition;
every certificate 'yes' is re-checked by an independent walk check (soundness); completeness counted per k and per
mode; the first instance that each method misses is printed (smallest q first, via a running minimum).
"""
import os
import sys
import random
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "dc-algorithm"))
import gcert  # noqa: E402
import zz  # noqa: E402  (read-only import, cross-check only)


def gen(rng, flavour):
    while True:
        if flavour == "ties":
            I = gcert.random_inst(rng, p_order=0.0)
        elif flavour == "poset":
            nm = rng.randint(2, 7)
            I = gcert.random_inst(rng, nm=nm, p_order=rng.choice([0.15, 0.3, 0.5]), distinct=True)
        elif flavour == "sw":
            nm = rng.randint(2, 6)
            I = gcert.random_inst(rng, nb=rng.randint(2, 4), nm=nm, nt=rng.randint(2, 4), p_order=0.0,
                                  middle_edges=False, distinct=True)
        elif flavour == "nomid":
            I = gcert.random_inst(rng, middle_edges=False)
        else:
            I = gcert.random_inst(rng)
        if flavour in ("sw", "nomid", "ties"):
            # drop instances whose P2 completion used middle-middle edges
            mid = ~(I.B | I.T)
            if any((mid >> a) & 1 and (mid >> b) & 1 for a, b in I.R):
                continue
        if I.p2():
            return I


def main():
    seed, count, kmax = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    flavour = sys.argv[4] if len(sys.argv) > 4 else "mixed"
    rng = random.Random(seed)
    stats = {"yes": 0, "no": 0, "unsound": 0, "exact-mismatch": 0}
    found_at = {}
    missed_min = {}
    t0 = time.time()
    for it in range(count):
        I = gen(rng, flavour)
        ex, w = gcert.exact(I, want_walk=True)
        ex2 = gcert.exact_downsets(I)
        z = zz.ZZ(I.n, None, I.R, I.u, I.v, le=I.le)
        ex3 = zz.exact_dfs(z)[0]
        if not (ex == ex2 == ex3) or (ex and not gcert.check_walk(I, w)):
            stats["exact-mismatch"] += 1
            print("EXACT MISMATCH", ex, ex2, ex3, gcert.describe(I))
            continue
        stats["yes" if ex else "no"] += 1
        c = gcert.certificate(I, kmax)
        cH = gcert.certificate(I, kmax, modes=("gen",), piercers_only="H")
        for name, cc in (("GC", c), ("H-literal", cH)):
            if cc is not None and not ex:
                stats["unsound"] += 1
                print("UNSOUND", name, cc, gcert.describe(I))
        if ex:
            key = ("GC", None if c is None else c[0], None if c is None else c[1])
            found_at[key] = found_at.get(key, 0) + 1
            keyH = ("H", None if cH is None else cH[0])
            found_at[keyH] = found_at.get(keyH, 0) + 1
            for name, cc in (("GC", c), ("H-literal", cH)):
                if cc is None:
                    sz = (I.n, len(I.R))
                    if name not in missed_min or sz < missed_min[name][0]:
                        missed_min[name] = (sz, gcert.describe(I))
    print("flavour", flavour, "seed", seed, "count", count, "kmax", kmax)
    print(stats)
    for k in sorted(found_at, key=str):
        print("  ", k, found_at[k])
    for name, (sz, d) in missed_min.items():
        print("smallest missed by", name, "(n, |R|) =", sz, ":", d)
    print("%.0fs" % (time.time() - t0))


if __name__ == "__main__":
    main()
