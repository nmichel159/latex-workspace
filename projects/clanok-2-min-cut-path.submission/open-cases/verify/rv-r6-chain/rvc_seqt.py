"""rv-r6-chain, L3 edge case: a yes-instance of the open case whose general switch form has s = t and no switch
at all, so it has no valid path X_1 .. X_r with r >= 1 (Theorem 8.2 is stated for instances "with a valid path"),
while IDESC accepts (its test of the empty intersection already connects).

ZZ instance: elements u = 0, b = 1, t = 2, v = 3; u ~ b (class of u), t ~ v (class of v), u, b < t, v;
R = {u t, b t, b v}.  Zigzag u < t > b < v (valleys u, b; peaks t, v) is consistent.
Realised by Theorem 13(b) (M = 1) and run through the whole chain (rvc_run.chain_pair).
"""
import os
import sys
import random

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rvc_lib as L     # noqa: E402
import rvc_run as R     # noqa: E402

le = [[1, 1, 1, 1], [1, 1, 1, 1], [0, 0, 1, 1], [0, 0, 1, 1]]
z = L.ZZ(4, le, [(0, 2), (1, 2), (1, 3)], 0, 3)
print("preorder ok", z.check_preorder(), "P2 bad", z.p2_bad(), "ZZ exact", z.exact())
sf = L.SF(z)
print("switches m =", sf.m, "nodes N =", sf.N, "s =", sf.s, "t =", sf.t, "sides", sf.sides())
print("IDESC (blind, Theorem 8.2 parameters):", L.idesc_full(sf))
n, edges = L.realise(z, M=1)
G = L.Graph(n, edges)
print("realised graph: n =", n, "edges =", len(edges), "DC", L.dc_test(G)[0], "d(u,v) =", G.dist_from(0)[3])
rec = R.chain_pair(G, 0, 3, "s=t example", random.Random(1), orig=z)
for k in ("c", "brute", "brute_methods", "zz", "sf_L", "s_eq_t", "idesc", "cert_graph", "roundtrip", "err"):
    print("  %s: %s" % (k, rec.get(k)))
