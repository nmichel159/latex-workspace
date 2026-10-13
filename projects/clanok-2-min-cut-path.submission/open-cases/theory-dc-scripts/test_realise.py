"""Tests of the realisation lemma (absreal.py): on random posets with random real pairs,
 (1) the minimum cuts of the realised weighted graph are exactly the down-sets containing u and not v;
 (2) the value is the number of comparable pairs;
 (3) if every incomparable pair has a common real neighbour that is a bound (P2), the realised simple graph
     (ears as degree-two vertices) is in DC, d(u,v) = 2, and cp = c iff a valid zigzag path exists.
Usage: python test_realise.py SEED COUNT"""
import sys, os, random, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dctools as T
import pi
from dctools import mcp
from absreal import closure, realise, p2_ok, downsets
import dctools as T

seed, count = int(sys.argv[1]), int(sys.argv[2])
rng = random.Random(seed)
st = {"posets": 0, "cuts_ok": 0, "cuts_bad": 0, "p2": 0, "dc_ok": 0, "dc_bad": 0, "cp_ok": 0, "cp_bad": 0}
for it in range(count):
    n = rng.randint(3, 7)
    u, v = 0, n - 1
    less = set((u, x) for x in range(1, n)) | set((x, v) for x in range(n - 1))
    perm = list(range(1, n - 1)); rng.shuffle(perm)
    for i in range(len(perm)):
        for j in range(i + 1, len(perm)):
            if rng.random() < 0.3:
                less.add((perm[i], perm[j]))
    lt = closure(n, less)
    comp = [(a, b) for a in range(n) for b in range(n) if lt[a][b] and (a, b) != (u, v)]
    R = [p for p in comp if rng.random() < 0.6]
    st["posets"] += 1
    inst = realise(n, lt, R, u, v)
    res = pi.answer(inst)
    ds = sorted(sum(1 << x for x in A) for A in downsets(n, lt, u, v))
    npairs = sum(1 for a in range(n) for b in range(n) if lt[a][b])
    if res["cuts"] == ds and res["c"] == npairs:
        st["cuts_ok"] += 1
    else:
        st["cuts_bad"] += 1
    if not p2_ok(n, lt, R):
        st["p2"] += 1
        nn, E = inst.realise()
        if nn <= 16:
            g = T.gr(nn, E)
            ok = mcp.in_dc(g)[0] and mcp.dist_matrix(g)[u][v] == 2
            st["dc_ok" if ok else "dc_bad"] += 1
            cp = mcp.cp_brute(g, u, v)[0]
            st["cp_ok" if ((cp == res["c"]) == res["yes"]) else "cp_bad"] += 1
print(st)
