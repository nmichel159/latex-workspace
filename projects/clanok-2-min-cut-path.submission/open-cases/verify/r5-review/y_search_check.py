"""Theorem Y (ii) of r4-general.md, partial computational check with own code (families.yfam, gswlib.SW.search5):
for K_E = (union of kd sets N_F[Z]) + (ks single F-sides) with kd, ks <= 1, K_F = union of at most `kf` sets N_E[Z]
(a sub-family of 'any K_F'), and kd + ks + s < k, B < k: the search of Theorem 5' must reject Y_k.  Also records
whether some certificate of this family is accepted with B = k (sharpness).
Usage: python y_search_check.py K KF"""
import itertools
import sys
from families import yfam


def nbhd(G, Z, O):
    return frozenset(i for i in G.sides if (i & 1) == O and (i == Z or (G.mask(i) & G.mask(Z))))


def main():
    k, kf = int(sys.argv[1]), int(sys.argv[2])
    G, it = yfam(k)
    Fs = [i for i in G.sides if i & 1]
    Es = [i for i in G.sides if not i & 1]
    NF = sorted({nbhd(G, Z, 1) for Z in G.sides}, key=sorted)
    NE = sorted({nbhd(G, Z, 0) for Z in G.sides}, key=sorted)
    KFs = [frozenset()]
    for r in range(1, kf + 1):
        for comb in itertools.combinations(NE, r):
            KFs.append(frozenset().union(*comb))
    KFs = sorted(set(KFs), key=sorted)
    accepted_below = 0
    tried = 0
    accepted_at_k = 0
    for kd in (0, 1):
        for ks in (0, 1):
            s = k - 1 - kd - ks
            if s < 0:
                continue
            KEs = set()
            for dom in ([frozenset()] if kd == 0 else NF):
                for single in ([None] if ks == 0 else Fs):
                    KEs.add(dom | ({single} if single is not None else frozenset()))
            for KE in KEs:
                for KF in KFs:
                    K = KE | KF
                    tried += 1
                    if G.search5(K, k - 1, s) is not None:
                        accepted_below += 1
                        print("ACCEPTED below the bound: kd=%d ks=%d s=%d B=%d" % (kd, ks, s, k - 1))
                    if kd == 1 and G.search5(K, k, s) is not None:
                        accepted_at_k += 1
    print("Y_%d: %d certificate sets tried with kd + ks + s = k - 1, B = k - 1: %d accepted (claim: 0); "
          "with B = k (kd = 1): %d accepted" % (k, tried, accepted_below, accepted_at_k))


if __name__ == "__main__":
    main()
