"""Print the shortest locally valid walks of a small planted instance, with names, after all far-pair atoms."""
import random
import sys

from wd import Budget, WS, best_atoms, conflicts, window_search, bits, popcnt
from zz_design import BASES

fam = sys.argv[1]
seed = int(sys.argv[2])
rng = random.Random(seed)
d = BASES[fam](rng)
I, P = d.build()
print("P2", I.p2(), "m", I.m, "q", len(P) - 1)
print("short", I.shortest_walk(bound=len(P) - 1, budget=60000))
W = WS(I, P)
print("P:", " ".join(I.name(x) for x in P))
print("A_P:", " ".join(I.name(x) for x in W.A))
print("B_P:", " ".join(I.name(x) for x in W.B))
F, E = best_atoms(I, W)
print("Z:", " ".join(I.name(x) for x in bits(E & ~F)))
print("not allowed low on P?", [I.name(x) for x in bits(W.lows & ~E)], "not allowed high on P?", [I.name(x) for x in bits(W.highs & F)])
for k in (1, 2, 4, 6):
    try:
        w = window_search(I, E, I.ALL & ~F, k)
    except Budget:
        print("k", k, "budget")
        continue
    if w is None:
        print("k", k, None)
        continue
    print("k", k, "len", len(w) - 1, " ".join(I.name(x) for x in w))
    print("   conflicts", [(I.name(w[i]), i, I.name(w[j]), j) for i, j in conflicts(I, w)])
