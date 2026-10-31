"""Checks of the family LB(K, R, M): P2, planted path shortest, number of solutions (brute force over class modes),
guided DESC costs of r5-classes (fastdesc.Prep.guided: least misclassification over tau and U = union of <= f
neighbourhood sets and <= g class groups / single sides), and the exact DESC cost over all solutions (cdesc2).
Usage: python lbtest.py K R M SEED [FGLIST]   FGLIST like 1,0;1,1;2,0"""
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "r5-classes"))
import ccore as C  # noqa: E402
import fastdesc  # noqa: E402
import lbfam  # noqa: E402

K, R, M, seed = (int(x) for x in sys.argv[1:5])
fgl = [(1, 0), (1, 1), (2, 0)]
if len(sys.argv) > 5:
    fgl = [tuple(int(v) for v in p.split(",")) for p in sys.argv[5].split(";")]
t0 = time.time()
pl = lbfam.build(K, R, M, seed)
I, P = pl.realise()
print("LB K=%d R=%d M=%d seed=%d: switches %d classes %d sides %d nodes %d" % (K, R, M, seed, I.n, I.k, len(I.sides), I.N),
      flush=True)
print(" P2", C.p2_ok(I), "planted path valid", C.is_valid_path(I, P), flush=True)
L, paths = C.shortest_valid_paths(I, limit=3, maxlen=len(P))
print(" shortest length", L, "planted length", len(P), flush=True)
if I.k <= 18:
    sols = C.all_solutions(I)
    print(" solutions", len(sols), flush=True)
pr = fastdesc.Prep(I, P)
for f, g in fgl:
    print(" guided (f=%d, g=%d):" % (f, g), pr.guided(f, g, want=True), "%.1fs" % (time.time() - t0), flush=True)
