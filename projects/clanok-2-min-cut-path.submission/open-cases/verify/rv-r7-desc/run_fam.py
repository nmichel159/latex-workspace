"""Referee rv-r7-desc: known families X_L, Y_k, Y'_k, Y^d_k.  Builders of r4-general, r5-core imported read-only; everything else is
the referee's own code.  Usage: run_fam.py KMAX LMAX LOG."""
import os
import random
import sys
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
OC = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
from swf import Inst, ClaimFail, Budget  # noqa: E402
from proof import run_all  # noqa: E402


def to_mask(x):
    if isinstance(x, int):
        return x
    return sum(1 << int(n) for n in x)


def from_info(info):
    E = [to_mask(e) for e in info["E"]]
    F = [to_mask(f) for f in info["F"]]
    nn = max(info["nodes"].values()) + 1
    return Inst(len(E), [[bool(b) for b in r] for r in info["mle"]], E, F, info["s"], info["t"], nn, [])


def from_gen(G):
    me = [(int(y), int(x), int(p)) for p, (y, x) in G.medge.items()]
    return Inst(G.m, [[bool(b) for b in r] for r in G.le], [int(x) for x in G.E], [int(x) for x in G.F], G.s, G.t,
                G.N, me)


def main():
    kmax, lmax = int(sys.argv[1]), int(sys.argv[2])
    log = open(sys.argv[3], "w", encoding="utf-8")
    for d in ("r5-core", "r4-general"):
        sys.path.append(os.path.join(OC, d))
    import gcore  # noqa: F401  (sets the import path of the builders)
    import common_r4  # noqa: F401
    import yfam
    import xfam
    from fool import yd
    rng = random.Random(7)
    insts = []
    for k in range(2, kmax + 1):
        for contact in (False, True):
            _, _, info = yfam.yfam(k, contact=contact)
            insts.append(("Y", "Y-%d-%d" % (k, contact), from_info(info)))
            for back in ((False, True) if k <= 5 else (False,)):
                Gd, _ = yd(k, back=back, contact=contact)
                insts.append(("Yd", "Yd-%d-%d-%d" % (k, back, contact), from_gen(Gd)))
    for L in range(2, lmax + 1):
        _, _, info = xfam.xfam(L)
        insts.append(("X", "X-%d" % L, from_info(info)))
    sts = {}
    fails = []
    for fam, name, I in insts:
        st = sts.setdefault(fam, Counter())
        t0 = time.time()
        I.validate()
        st["instances"] += 1
        if not I.p2():
            st["no P2"] += 1
            print(name, "no P2", file=log, flush=True)
            continue
        try:
            w = I.shortest(budget=150_000)
        except Budget:
            st["budget"] += 1
            print(name, "over budget", file=log, flush=True)
            continue
        if w is None:
            st["no-instances"] += 1
            continue
        paths = [w] if I.m > 30 else I.all_shortest(len(w), cap=50)
        st["max r"] = max(st["max r"], len(w))
        st["max m"] = max(st["max m"], I.m)
        for P in paths:
            try:
                run_all(I, P, rng, st, trials=2)
            except ClaimFail as e:
                fails.append((name, str(e)))
                print("FAIL", name, e, P, file=log, flush=True)
        print(name, "m", I.m, "r", len(w), "paths", len(paths), "t", round(time.time() - t0, 1), file=log, flush=True)
    for fam, st in sts.items():
        print("==", fam, file=log)
        for k in sorted(st):
            print("  ", k, st[k], file=log)
    print("FAILURES:", fails if fails else "none", file=log)
    log.close()


if __name__ == "__main__":
    main()
