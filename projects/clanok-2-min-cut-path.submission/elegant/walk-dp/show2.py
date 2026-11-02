"""Trace of the closure on one planted instance: alive conflict pairs after SAC, the walk found, the branches."""
import random
import sys
from collections import Counter

from wd import WS, bits, conflicts
from closure import Graph, Refuted, alive_conflicts, bfs_walk, closure, sac
from zz_design import zipper, BASES


def nm(I, S):
    return " ".join(I.name(x) for x in bits(S))


fam = sys.argv[1]
seed = int(sys.argv[2])
rng = random.Random(seed)
if fam == "z":
    d = zipper(int(sys.argv[3]), int(sys.argv[4]))
else:
    d = BASES[fam](rng)
I, P = d.build()
print("P2", I.p2(), "m", I.m, "q", len(P) - 1, "short", I.shortest_walk(bound=len(P) - 1, budget=100000))
print("P:", " ".join(I.name(x) for x in P))
G = Graph(I)
AL, AH, forced = closure(G, I.ALL, I.ALL)
print("closure forced:", " ".join(I.name(n >> 1) + ("^" if n & 1 else "_") for n in forced[::-1]))
print("dead lows on P?", nm(I, I.dn(1 << 0) & 0), "alive lows:", nm(I, AL))
print("alive highs:", nm(I, AH))
AL, AH = sac(G, AL, AH)
print("SAC alive lows:", nm(I, AL))
print("SAC alive highs:", nm(I, AH))
step = 0
while True:
    w = bfs_walk(G, AL, AH)
    print("walk len", len(w) - 1, " ".join(I.name(x) for x in w))
    c = conflicts(I, w)
    if not c:
        print("VALID", I.is_valid_walk(w))
        break
    i, j = c[0]
    h, l = w[i], w[j]
    print("conflict", I.name(h), i, I.name(l), j, "of", len(c))
    # try kill h as high
    try:
        AL2, AH2 = sac(G, AL, AH & ~(1 << h))
        print("  kill", I.name(h), "high: passes; killed further: lows", nm(I, AL & ~AL2), "highs", nm(I, AH & ~AH2 & ~(1 << h)))
        AL, AH = AL2, AH2
        continue
    except Refuted:
        print("  kill", I.name(h), "high: refuted")
    AL2, AH2 = sac(G, AL & ~(1 << l), AH)
    print("  kill", I.name(l), "low: passes; killed further: lows", nm(I, AL & ~AL2 & ~(1 << l)), "highs", nm(I, AH & ~AH2))
    AL, AH = AL2, AH2
