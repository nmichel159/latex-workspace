"""Print the side-set certificate found on Z_k.  Usage: python show_cert_z.py K KD KS S B"""
import sys
import common_r4  # noqa: F401
from zfam import zfam
from gsw import GSW

k = int(sys.argv[1])
par = tuple(int(a) for a in sys.argv[2:6])
I, names, info = zfam(k)
G = GSW(I)
sw = [names[x] for x in G.M]


def sname(i):
    return "%s.%s" % ("".join(str(p) for p in sw[i >> 1]), "EF"[i & 1])


r = G.decide(*par, want_walk=True)
print("accepted", r[0])
if r[0]:
    dE, dF, walk = r[1]
    print("K_E dominators", [sname(z) for z in dE[0]], "singles", [sname(z) for z in dE[1]])
    print("K_F dominators", [sname(z) for z in dF[0]], "singles", [sname(z) for z in dF[1]])
    print("walk", [sname(i) for i in walk])
    for i in walk:
        print("  ", sname(i), "Pi:", [sname(j) for j in sorted(G.Pi[i])])
