"""Print the shortest walks of the (restricted) state graph of a small planted instance, with names and conflicts."""
import random
import sys

from common import BASES, StateGraph, WData, bits, conflicts, popcnt
from e1_guess import restricted

fam = sys.argv[1]
seed = int(sys.argv[2])
rng = random.Random(seed)
d = BASES[fam](rng)
I, P = d.build()
W = WData(I, P)
print("m", I.m, "q", len(W.P) - 1, "|A|", len(W.A), "|B|", len(W.B))
print("P:", " ".join(I.name(x) for x in W.P))
print("A:", " ".join(I.name(x) for x in W.A))
print("B:", " ".join(I.name(x) for x in W.B))
G = StateGraph(I)
w = G.shortest(rng)
print("BFS unrestricted d=", len(w) - 1, ":", " ".join(I.name(x) for x in w))
print(" conflicts:", [(I.name(h), I.name(l)) for h, l in conflicts(I, w)])
FA, FB = W.far_pairs_A(), W.far_pairs_B()
for s in range(4):
    A2 = rng.choice(FA)
    B2 = rng.choice(FB)
    LOK, HOK = restricted(I, A2, B2)
    G = StateGraph(I, LOK, HOK)
    w = G.shortest(rng)
    print("far", I.name(A2[0]), I.name(A2[1]), I.name(B2[0]), I.name(B2[1]), "d=", len(w) - 1, "lows allowed", popcnt(LOK), "highs allowed", popcnt(HOK), "both", popcnt(LOK & HOK))
    print("  ", " ".join(I.name(x) for x in w))
    print("  conflicts:", [(I.name(h), I.name(l)) for h, l in conflicts(I, w)])
