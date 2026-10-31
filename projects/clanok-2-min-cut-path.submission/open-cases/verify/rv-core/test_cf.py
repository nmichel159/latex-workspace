"""Proposition CF of r5-core.md 3.3 with the reviewer's own code.

(i), (ii): Y_k, Y'_k, Y^d_k, Y'^d_k (both variants): E-description with the single centre Fl_2k = E(x_2k), no flip:
     D computed, compared with the claimed set, connectivity tested.
(iii): X_L: centre E(m_1), no flip (L even) or flip {x_L} (L odd).
(iv) (cross-check, author's generator r4-general/zfam.py imported read-only, converted to the reviewer's SW):
     minimal Lemma-G cost with one centre (any side or node), E- and F-side, over all shortest valid paths.
usage: python test_cf.py KMAX LMAX ZMAX
"""
import os
import sys
from fams import yfam, xfam
from sw import SW, describe, NE, NF, bits, path_data, enon, fnon

HERE = os.path.dirname(os.path.abspath(__file__))
OC = os.path.dirname(os.path.dirname(HERE))


def names(G, S):
    return sorted(G.names[w] for w in bits(S))


def lemma_g_cost(G, P, U, kind):
    pd = path_data(G, P)
    if kind == "E":
        En = enon(G)
        out = pd["L"] & En & ~U
        G1 = (En & ~U) & ~pd["L"]
        inn = [a for a in bits(pd["A"]) if not (G.dnc(1 << a) & G1)]
    else:
        Fn = fnon(G)
        out = pd["Up"] & Fn & ~U
        G1 = (Fn & ~U) & ~pd["Up"]
        inn = [b for b in bits(pd["B"]) if not (G.upc(1 << b) & G1)]
    return bin(out).count("1") + len(inn)


def min_one_centre(G):
    L, paths = G.shortest_valid_paths()
    cands = [G.side[i] for i in range(2 * G.m) if G.side[i]] + [1 << v for v in range(G.N)]
    best = None
    for P in paths:
        for kind in "EF":
            c0 = lemma_g_cost(G, P, 0, kind)
            if best is None or (c0, 0) < best[:2]:
                best = (c0, 0, kind)
            for Z in cands:
                U = NE(G, Z) if kind == "E" else NF(G, Z)
                c = lemma_g_cost(G, P, U, kind)
                if (c, 1) < best[:2]:
                    best = (c, 1, kind)
    return L, len(paths), best


def main(KMAX, LMAX, ZMAX):
    for k in range(2, KMAX + 1):
        for (c, d, bk) in [(False, False, False), (True, False, False), (False, True, False), (False, True, True),
                           (True, True, False), (True, True, True)]:
            G = yfam(k, contact=c, d=d, back=bk)
            Z = G.E[G.x[2 * k]]
            U = NE(G, Z)
            D = describe(G, "E", 0, 0, U, 0)
            claim = sum(1 << G.x[q] for q in range(k + 1, 2 * k + 1)) | ((1 << G.d) if d else 0)
            print("Y%s%s_%d%s: U = %s; D = %s; claim holds: %s; connects: %s" % (
                "'" if c else "", "^d" if d else "", k, "/back" if bk else "", names(G, U), names(G, D),
                D == claim, G.connects(D)), flush=True)
    for L in range(2, LMAX + 1):
        G = xfam(L)
        assert not G.p2_violations()
        sols = G.solutions()
        Z = G.E[G.mate[1]]
        U = NE(G, Z)
        Phi = (1 << G.x[L]) if L % 2 else 0
        D = describe(G, "E", 0, 0, U, Phi)
        print("X_%d: P2 ok, solutions %d; D = %s; equals the unique solution: %s; connects: %s" % (
            L, len(sols), names(G, D), len(sols) == 1 and D == sols[0], G.connects(D)), flush=True)
    if ZMAX >= 2:
        sys.path.append(os.path.join(OC, "r4-general"))
        sys.path.append(os.path.join(OC, "r5-core"))
        from gcore import from_inst     # author, read-only (sets the import path of the other folders)
        import zfam                     # author, read-only
        for k in range(2, ZMAX + 1):
            for block in (False, True):
                I, full, info = zfam.zfam(k, block=block)
                A, _ = from_inst(I)
                rel = [(a, b) for a in range(A.m) for b in range(A.m) if a != b and A.le[a][b]] \
                    if isinstance(A.le[0], list) else [(a, b) for a in range(A.m) for b in range(A.m)
                                                       if a != b and (A.le[a] >> b & 1)]
                G = SW(A.N, A.s, A.t, A.E, A.F, rel)
                L, npaths, best = min_one_centre(G)
                print("Z%s_%d (cross-check, author's generator): switches %d, shortest length %s, %d shortest paths; "
                      "least Lemma-G cost: %d flips with %d centre (%s-description)" % (
                          "^B" if block else "", k, G.m, L, npaths, best[0], best[1], best[2]), flush=True)


if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
