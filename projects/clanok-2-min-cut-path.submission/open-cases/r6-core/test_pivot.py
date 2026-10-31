"""Statistics of the pivot duality (pivot.py) on random general ZZ + P2 instances and on the families.

Usage: python test_pivot.py random SEED COUNT NMIN NMAX C
       python test_pivot.py families C
For every yes-instance and every shortest valid path (up to 20 per instance): number of (x, y) pairs, how they are
dominated, and the failing pairs (comparable: both pivots expensive; incomparable: P2 only through middle witnesses).
"""
import sys
import random
import time
from collections import Counter
import pivot  # noqa: F401  (sets the path)
import gcore
from gcore import from_inst
import gcert
import mixed
from common_r4 import from_zz
from pivot import pair_classes


def gen_instance(rng, nmin, nmax, it):
    nm = rng.randint(nmin, nmax)
    if it % 2 == 0:
        return gcert.random_inst(rng, nm=nm, p_order=rng.choice([0.2, 0.35, 0.5]), p_R=rng.choice([0.15, 0.25]))
    return from_zz(mixed.random_instance(rng, rng.choice(["lower", "upper", "mixed"]), nm=nm,
                                         p_order=rng.choice([0.25, 0.4]), p_tie=rng.choice([0.0, 0.5])))


def analyse(name, G, c, st, verbose=False):
    L, P0 = G.shortest()
    if L is None:
        st["no"] += 1
        return
    st["yes"] += 1
    paths = G.all_shortest(limit=20, length=L)
    best = None
    for P in paths:
        S, o = pair_classes(G, P, c)
        nf = len(o["fail_comp"]) + len(o["fail_incomp"])
        st["paths"] += 1
        st["pairs"] += o["pairs"]
        st["fail_comp"] += len(o["fail_comp"])
        st["fail_incomp"] += len(o["fail_incomp"])
        if nf:
            st["paths with failures"] += 1
        if best is None or nf < best:
            best = nf
    if best:
        st["instances: every shortest path has failures"] += 1
    if verbose:
        print("%-20s m=%d len=%d paths=%d least failures=%s" % (name, G.m, L, len(paths), best), flush=True)


def main():
    mode = sys.argv[1]
    st = Counter()
    t0 = time.time()
    if mode == "random":
        seed, count, nmin, nmax, c = (int(a) for a in sys.argv[2:7])
        rng = random.Random(seed)
        for it in range(count):
            I = gen_instance(rng, nmin, nmax, it)
            if not I.p2():
                continue
            G, _ = from_inst(I)
            analyse("r%d" % it, G, c, st)
        print("random seed %d count %d n %d-%d c=%d (%.0fs): %s" % (seed, count, nmin, nmax, c, time.time() - t0,
                                                                  dict(st)))
    else:
        c = int(sys.argv[2])
        import fool
        import xfam
        import yfam
        import zfam
        fams = []
        for k in range(2, 5):
            fams.append(("Y_%d" % k, yfam.yfam(k)[0]))
            fams.append(("Y'_%d" % k, yfam.yfam(k, contact=True)[0]))
        for L in range(2, 7):
            fams.append(("X_%d" % L, xfam.xfam(L, "both")[0]))
        for k in range(2, 4):
            fams.append(("Z_%d" % k, zfam.zfam(k)[0]))
            fams.append(("ZB_%d" % k, zfam.zfam(k, block=True)[0]))
        for name, I in fams:
            G, _ = from_inst(I)
            analyse(name, G, c, st, verbose=True)
        try:
            for k in range(2, 5):
                for back in (False, True):
                    for contact in (False, True):
                        Gd = fool.ydk(k, contact=contact, back=back)
                        G = Gd[0] if isinstance(Gd, tuple) else Gd
                        analyse("Yd_%d c%d b%d" % (k, contact, back), G, c, st, verbose=True)
        except Exception as e:      # the fool module's interface is checked separately
            print("fool families skipped:", repr(e))
        print("families c=%d (%.0fs): %s" % (c, time.time() - t0, dict(st)))


if __name__ == "__main__":
    main()
