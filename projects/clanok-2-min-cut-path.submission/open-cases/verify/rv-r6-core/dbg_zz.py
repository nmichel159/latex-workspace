"""Debug: for saved failure instances, check (i) privacy of the private nodes (a private node of z v lies only in F_z
and E_v), (ii) switch form = ZZ realisation on every down-set (m <= 14)."""
import sys
from zzl import bits, sw_to_zz, zz_connects
from adv8 import load, zz_check_D

for fp in sys.argv[1:]:
    I, P = load(fp)
    priv = {p: (z, v) for (z, v, p) in I.me}
    viol = []
    for w in range(I.m):
        for ty, side in ((0, I.E[w]), (1, I.F[w])):
            for nd in bits(side):
                if nd in priv:
                    z, v = priv[nd]
                    if not ((ty == 1 and w == z) or (ty == 0 and w == v)):
                        viol.append((nd, (z, v), w, "EF"[ty]))
    zzc = sw_to_zz(I)
    mism = 0
    for D in I.downsets():
        if I.connects(D) != zz_check_D(I, D, zzc):
            mism += 1
    print(fp, "m", I.m, "privacy violations", viol[:4], "down-set mismatches", mism)
