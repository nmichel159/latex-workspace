"""CROSS-CHECK (reviewer rv-core-65): the reviewer's own objects of r5-core.md Section 6 (thy.py) against the code of
r5-core (gcore.Gen, gstar.Stars/Skel/classify/tool_cover_*, gdesc.describe), imported READ-ONLY from ../../r5-core.
This is the only script of verify/rv-core-65 that imports code of another agent.

For random P2 instances of the reviewer's generators: stars E#, F# and their switch neighbourhoods, A, B, N_E, N_F of
every shortest valid path, E- and F-tool covers, the bad pairs, the minimum vertex cover size, and the descriptions
for random parameters (kind, T, flags, anchors, flips) must agree.

usage: python cross_r5core.py SEED COUNT MMIN MMAX
"""
import os
import sys
import random
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
R5 = os.path.normpath(os.path.join(HERE, "..", "..", "r5-core"))
sys.path.append(R5)                      # appended, so the reviewer's own modules take precedence

import gcore                             # noqa: E402  (r5-core, read only)
import gstar                             # noqa: E402
import gdesc                             # noqa: E402
from gsf import bits                     # noqa: E402
from thy import Stars, Skel, cov_E, cov_F, bad_pairs, min_vertex_cover, describe_E, describe_F   # noqa: E402
import test_thm65                        # noqa: E402


def to_gen(I):
    medge = {node: (z, v) for (z, v), node in I.medges.items()}
    return gcore.Gen(I.N, I.E, I.F, I.le, I.s, I.t, medge=medge)


def main():
    seed, count, mmin, mmax = (int(a) for a in sys.argv[1:5])
    rng = random.Random(seed)
    st = Counter()
    for it in range(count):
        I = test_thm65.gen(rng, mmin, mmax, "both", it)
        if not I.p2() or I.s == I.t:
            continue
        st["instances"] += 1
        G = to_gen(I)
        S1 = Stars(I)
        S2 = gstar.Stars(G)
        if S1.Estar != S2.Estar or S1.Fstar != S2.Fstar:
            st["STARS DIFFER"] += 1
        if S1.NEstar != S2.NEstar or S1.NFstar != S2.NFstar:
            st["STAR NEIGHBOURHOODS DIFFER"] += 1
        r, paths = I.shortest_paths(cap=10)
        if r is None:
            continue
        for P in paths:
            st["paths"] += 1
            K1 = Skel(I, P)
            P2 = [2 * w + typ for (w, typ) in P]
            K2 = gstar.Skel(G, P2)
            if (K1.A, K1.B, K1.NEi, K1.NFi, K1.Up, K1.L) != (K2.A, K2.B, K2.NE, K2.NF, K2.Up, K2.L):
                st["SKELETONS DIFFER"] += 1
            for x in bits(K1.NFi):
                if cov_E(I, S1, K1, x) != gstar.tool_cover_E(G, S2, K2, x):
                    st["E-TOOL COVERS DIFFER"] += 1
            for y in bits(K1.NEi):
                if cov_F(I, S1, K1, y) != gstar.tool_cover_F(G, S2, K2, y):
                    st["F-TOOL COVERS DIFFER"] += 1
            bp1 = sorted(bad_pairs(I, K1))
            _, cls = gstar.classify(G, P2, S2, K2)
            # gstar.classify calls a pair 'bad' only if it is bad by the order AND no star covers it
            narrow = sorted((x, y) for x, y in bp1
                            if not (S1.NEstar[x] >> y) & 1 and not (S1.NFstar[y] >> x) & 1)
            if sorted(cls["bad"]) != narrow:
                st["NARROW BAD PAIRS DIFFER"] += 1
            st["order-bad pairs covered by a star"] += len(bp1) - len(narrow)
            if cls["incomp_fail"]:
                st["LEMMA 6.4 FAILS (r5-core classify)"] += 1
            st["bad pairs"] += len(bp1)
            for bpl in (bp1, narrow):
                if bpl:
                    k1, _ = min_vertex_cover(bpl)
                    k2 = gstar.min_vertex_cover_bip(bpl)
                    if not isinstance(k2, int):
                        k2 = len(k2)
                    if k1 != k2:
                        st["VERTEX COVER SIZES DIFFER"] += 1
            for _ in range(5):
                kind = rng.randrange(2)
                T = rng.sample(range(I.m), rng.randint(0, min(3, I.m)))
                flags = [x for x in T if rng.random() < 0.5]
                Y0 = rng.sample(range(I.m), rng.randint(0, min(2, I.m)))
                Phi = sum(1 << w for w in range(I.m) if rng.random() < 0.2)
                if kind == 0:
                    D1, _, _ = describe_E(I, S1, T, flags, Y0, Phi)
                else:
                    D1, _, _ = describe_F(I, S1, T, flags, Y0, Phi)
                D2 = gdesc.describe(G, S2, kind, T, set(flags), Y0, Phi)
                st["descriptions compared"] += 1
                if D1 != D2:
                    st["DESCRIPTIONS DIFFER"] += 1
    print("cross_r5core seed %d count %d m %d-%d: %s" % (seed, count, mmin, mmax, dict(sorted(st.items()))))


if __name__ == "__main__":
    main()
