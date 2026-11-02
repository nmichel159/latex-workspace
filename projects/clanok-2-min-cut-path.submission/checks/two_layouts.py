"""Which gadget layouts of zz_design.two_gadget keep P shortest, with the sum of lem:pa-two for each.  Every layout is tried alone on an all-strict alternating word."""
import os
import random
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from zz_design import Design, two_gadget  # noqa: E402
from zz_proof import Cfg, Walk, check_lemmas  # noqa: E402

LAY = ["aL_hR", "hL_aR", "both_L", "both_R", "back_hL_aR", "back_aL_hR", "back_aL_hR8", "small_hL_aR", "short"]
rng = random.Random(1)
for lay in LAY:
    for below in (True, False):
        kept = Counter()
        st = Counter()
        for n in (31, 40):
            d = Design()
            E, F = [], []
            for i in range(n):
                if i % 2 == 0:
                    E.append(d.add("E"))
                else:
                    F.append(d.add("F"))
            for a in E:
                for b in F:
                    d.set_strict(b, a)
            d.info = {"Apos": E, "H": [(b, b) for b in F], "Vs": []}
            p1, a, al, be, h, p4 = two_gadget(d, 9, lay, below)
            s = (min(al, be) - p1) + (p4 - max(al, be))
            I, P = d.build()
            ok = I.p2() and I.shortest_walk(bound=len(P) - 1) is None
            kept["kept" if ok else "rejected"] += 1
            if ok:
                check_lemmas(Walk(I, P), Cfg(), rng, st)
        print("%-12s contact %-5s sum %2d  %s  two tested %d max %d" % (lay, "below" if below else "above", s, dict(kept), st["two tested"], st["two max sum"]))
