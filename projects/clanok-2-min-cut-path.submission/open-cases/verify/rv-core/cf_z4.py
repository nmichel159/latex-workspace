"""Cross-check (author's generator r4-general/zfam.py, read-only): do CDESC descriptions with one centre and no flip
(resp. at most one flip) connect on Z_k, Z^B_k?  Direct test of every description (no path enumeration).
usage: python cf_z4.py KMIN KMAX
"""
import os
import sys
from sw import SW, describe, NE, NF
HERE = os.path.dirname(os.path.abspath(__file__))
OC = os.path.dirname(os.path.dirname(HERE))
sys.path.append(os.path.join(OC, "r4-general"))
sys.path.append(os.path.join(OC, "r5-core"))
from gcore import from_inst   # noqa: E402  author, read-only
import zfam                   # noqa: E402  author, read-only


def main(kmin, kmax):
    for k in range(kmin, kmax + 1):
        for block in (False, True):
            I, full, info = zfam.zfam(k, block=block)
            A, _ = from_inst(I)
            rel = [(a, b) for a in range(A.m) for b in range(A.m) if a != b and A.le[a][b]]
            G = SW(A.N, A.s, A.t, A.E, A.F, rel)
            cands = sorted(set([G.side[i] for i in range(2 * G.m) if G.side[i]] + [1 << v for v in range(G.N)]))
            res = {}
            for e in (0, 1):
                found = None
                for kind in "EF":
                    for Z in cands:
                        U = NE(G, Z) if kind == "E" else NF(G, Z)
                        for Phi in ([0] if e == 0 else [1 << w for w in range(G.m)]):
                            D = describe(G, kind, 0, 0, U, Phi)
                            if D is not None and G.connects(D):
                                found = kind
                                break
                        if found:
                            break
                    if found:
                        break
                res[e] = found
            print("Z%s_%d: switches %d; one centre, no flip: %s; one centre, <= 1 flip: %s" % (
                "^B" if block else "", k, G.m, res[0] or "none", res[1] or "none"), flush=True)


if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]))
