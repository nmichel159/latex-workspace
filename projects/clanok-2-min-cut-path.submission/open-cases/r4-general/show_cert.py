"""Print the side-set certificate and the walk found by gsw.decide for R(W) with mates.
Usage: python show_cert.py WORD [KD KS S B]"""
import sys
import common_r4  # noqa: F401  (sets the import path)
from yfam import rword
from gsw import GSW

W = sys.argv[1]
par = tuple(int(a) for a in sys.argv[2:6]) if len(sys.argv) > 5 else (1, 0, 2, 6)
I, names, info = rword(W, mates=True)
G = GSW(I)
sw = [names[x] for x in G.M]


def sname(i):
    return "%s%s.%s" % (sw[i >> 1][0], sw[i >> 1][1], "EF"[i & 1])


r = G.decide(*par, want_walk=True)
print("params", par, "accepted", r[0])
if r[0]:
    dE, dF, walk = r[1]
    print("K_E dominators", [sname(z) for z in dE[0]], "singles", [sname(z) for z in dE[1]])
    print("K_F dominators", [sname(z) for z in dF[0]], "singles", [sname(z) for z in dF[1]])
    print("walk", [sname(i) for i in walk])
    for i in walk:
        print("  ", sname(i), "Pi:", [sname(j) for j in sorted(G.Pi[i])])
