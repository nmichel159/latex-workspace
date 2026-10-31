"""Debug: print the pairs (x, y) of R x C (residue A' = A) that violate the duality claim on r5-core's stored
instances, with the order relation and the P2 witnesses of the pair."""
import sys
import os
import glob
from zzl import Skel, all_shortest_valid_paths, bits, popcount, kparam
from cross_r5data import load_r5, SRC

files = [os.path.join(SRC, "two-levels-example.json")] + sorted(glob.glob(os.path.join(SRC, "single", "*.json")))
shown = 0
for fp in files[: int(sys.argv[1]) if len(sys.argv) > 1 else 3]:
    I, P, d = load_r5(fp)
    r, paths = all_shortest_valid_paths(I, cap=3)
    for pp in paths:
        Sk = Skel(I, [tuple(x) for x in pp])
        Ap = Sk.A
        R = I.upc(Ap) & I.fnon
        C = Sk.NE_
        for x in bits(R):
            for y in bits(C):
                inE = (I.NEs[x] >> y) & 1
                inF = (I.NFs[y] >> x) & 1
                rel = "x<=y" if I.le[x][y] else ("y<x" if I.le[y][x] else "incomparable")
                yB = (Sk.B >> y) & 1
                if rel == "incomparable" and not inE and not inF:
                    ee = I.E[x] & I.E[y]
                    ff = I.F[x] & I.F[y]
                    lw = [z for (z, v, p) in I.me if v == x and any(zz == z and vv == y for (zz, vv, pp2) in I.me)]
                    uw = [z for (zz, z, p) in I.me if zz == x and any(a == y and b == z for (a, b, c) in I.me)]
                    print(os.path.basename(fp), "x", x, d["names"][x], "y", y, d["names"][y], rel,
                          "commonE", bin(ee).count("1"), "commonF", bin(ff).count("1"), "lowerW", lw, "upperW", uw,
                          "E_x", bin(I.E[x]).count("1"), "F_y", bin(I.F[y]).count("1"))
                    shown += 1
print("shown", shown)
