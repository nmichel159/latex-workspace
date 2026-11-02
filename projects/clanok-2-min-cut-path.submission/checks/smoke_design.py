"""Smoke test of the planted designs: P2, P shortest, stages reached on the four variants of each base."""
import os
import random
import sys
import time
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from zz_core import ClaimFail  # noqa: E402
from zz_design import BASES  # noqa: E402
from zz_proof import Cfg, Walk, construct, general_claim  # noqa: E402

rng = random.Random(1)
cfg = Cfg()
for name, fn in BASES.items():
    st = Counter()
    d = fn(rng)
    I, P = d.build()
    I.validate()
    print(name, "m", I.m, "q", len(P) - 1, "P2", I.p2(), "violations", I.p2_violations()[:5], flush=True)
    t0 = time.time()
    w = I.shortest_walk(bound=len(P) - 1, budget=400000)
    print("  shorter walk:", None if w is None else (len(w) - 1, [I.name(x) for x in w][:60]), "t", round(time.time() - t0, 2), flush=True)
    if w is not None:
        continue
    for tag, J, Q in (("id", I, P), ("rev", I, P[::-1]), ("op", I.reversed_instance(), P), ("oprev", I.reversed_instance(), P[::-1])):
        try:
            t0 = time.time()
            ex = construct(Walk(J, Q), cfg, rng, st)
            general_claim(Walk(J, Q), cfg, rng, st)
            print("  ", tag, ex, "t", round(time.time() - t0, 2), flush=True)
        except ClaimFail as e:
            print("  ", tag, "FAIL", e, flush=True)
    for k in sorted(st):
        if k.startswith("final") or k.startswith("orient") or k.startswith("Shape") or k.startswith("(star)") or k.startswith("two") or k.startswith("general") or k == "C_1 max":
            print("    ", k, st[k])
