"""Certificate check for "PC leaves every relation non-empty" (agent verify-round3).

The PC closure is the largest path-consistent network inside the base constraints. So a network N with
 (1) N inside the base constraints (unary: tail of position 1 is u, head of position L is v; binary: consecutive
     positions share the head (odd 1-based position) or the tail (even); every two positions compatible:
     not h <= t', not h' <= t),
 (2) N path consistent (for all positions i, j, k and (a, b) in N_ij some c with (a, c) in N_ik, (c, b) in N_kj;
     N_ii is a diagonal, so this includes arc consistency),
 (3) every N_ij non-empty,
proves that the PC closure is non-empty. (1) is checked here with explicit Python loops from the definitions,
(2) with int64 matrix products per triple (a code path different from r3core.pc).
Usage: python pc_cert.py m mp L version"""
import sys

import numpy as np

from hub3 import hub


def certify(inst, L, N, E):
    le = inst.le
    m = len(E)
    bad = 0
    # (1) base constraints
    for i in range(L):
        for a in range(m):
            for b in range(m):
                if not N[i, i, a, b]:
                    continue
                if a != b:
                    bad += 1
                if i == 0 and E[a][0] != inst.u:
                    bad += 1
                if i == L - 1 and E[a][1] != inst.v:
                    bad += 1
    for i in range(L):
        for j in range(L):
            if i == j:
                continue
            for a in range(m):
                ta, ha = E[a]
                for b in range(m):
                    if not N[i, j, a, b]:
                        continue
                    tb, hb = E[b]
                    if le[ha, tb] or le[hb, ta]:
                        bad += 1
                    if not N[i, i, a, a] or not N[j, j, b, b]:
                        bad += 1
                    if j == i + 1:
                        pos = i + 1  # 1-based position of i
                        if pos % 2 == 1 and ha != hb:
                            bad += 1
                        if pos % 2 == 0 and ta != tb:
                            bad += 1
                    if i == j + 1:
                        pos = j + 1
                        if pos % 2 == 1 and ha != hb:
                            bad += 1
                        if pos % 2 == 0 and ta != tb:
                            bad += 1
                    if N[j, i, b, a] != N[i, j, a, b]:
                        bad += 1
    # (2) path consistency
    Ni = N.astype(np.int64)
    for i in range(L):
        for j in range(L):
            for k in range(L):
                P = Ni[i, k] @ Ni[k, j]
                if np.any(N[i, j] & (P == 0)):
                    bad += 1
    # (3) non-empty
    empty = sum(1 for i in range(L) for j in range(L) if not N[i, j].any())
    return bad, empty


if __name__ == "__main__":
    m, mp, L = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    ver = sys.argv[4]
    H = hub(m, mp, ver)
    ok, N, E = H.pc(L, return_net=True)
    print("H(%d,%d) %s L=%d: r3core.pc says %s" % (m, mp, ver, L, ok))
    if ok:
        bad, empty = certify(H, L, N, E)
        sizes = [int(N[i, i].sum()) for i in range(L)]
        print("  certificate: violations %d, empty relations %d; domain sizes %s" % (bad, empty, sizes))
        print("  pairs kept in total: %d" % int(N.sum()))
