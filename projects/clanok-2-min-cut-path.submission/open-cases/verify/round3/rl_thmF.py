"""The rigid family R_L of dc-hardness.md Section 2 in ZZ form (own 2CH -> ZZ conversion as in verify/lth.md §1):
P2, answer, and the Theorem F search with at most k peaks (bottom version) or valleys (dual): shows that the bound
"at most two" of Theorem F needs its witness hypothesis (agent verify-round3). Usage: python rl_thmF.py Lmax"""
import sys
import numpy as np
from r3core import Inst


def rigid_2ch(L):
    nodes = ['s', 't'] + [('y', k) for k in range(1, L)]
    for p in range(1, L + 1):
        for q in range(p + 1, L + 1):
            nodes.append(('z', p, q) if (q - p) % 2 == 1 else ('w', p, q))
    idx = {x: i for i, x in enumerate(nodes)}
    h = {k: set() for k in range(1, L + 1)}
    fl = {k: set() for k in range(1, L + 1)}
    h[1].add(idx['s']); h[L].add(idx['t'])
    for k in range(1, L):
        h[k].add(idx[('y', k)]); h[k + 1].add(idx[('y', k)])
    for p in range(1, L + 1):
        for q in range(p + 1, L + 1):
            if (q - p) % 2 == 1:
                x = idx[('z', p, q)]; fl[p].add(x); h[q].add(x)
            else:
                x = idx[('w', p, q)]; fl[p].add(x); fl[q].add(x)
    sw = []
    for k in range(1, L + 1):
        sw.append((h[k], fl[k]) if k % 2 == 1 else (fl[k], h[k]))   # (E, F)
    return len(nodes), idx['s'], idx['t'], sw


def twoch_to_zz(N, s, t, sw):
    n = len(sw)
    q = 2 * N + n
    b = lambda x: x
    tp = lambda x: N + x
    e = lambda w: 2 * N + w
    le = np.eye(q, dtype=bool)
    for x in range(N):
        for y in range(N):
            le[b(x), b(y)] = True; le[tp(x), tp(y)] = True
            le[b(x), tp(y)] = True
        for w in range(n):
            le[b(x), e(w)] = True; le[e(w), tp(x)] = True
    R = [(b(x), tp(x)) for x in range(N)]
    for w, (E, F) in enumerate(sw):
        R += [(b(x), e(w)) for x in E] + [(e(w), tp(x)) for x in F]
    return Inst(q, le, R, b(s), tp(t))


if __name__ == "__main__":
    for L in range(2, int(sys.argv[1]) + 1):
        I = twoch_to_zz(*rigid_2ch(L))
        I.check()
        ans = I.solve_dfs()
        ks = []
        for k in range(0, L + 1):
            if I.thmF(maxA=k)[0] or I.thmF(dual=True, maxA=k)[0]:
                ks.append(k)
                break
        print("R_%d: q=%d P2=%s answer=%s zigzag length=%s bottom/top witnesses=%s/%s; smallest k with a "
              "Theorem-F-type search (k peaks or k valleys) succeeding: %s"
              % (L, I.q, I.p2(), ans is not None, len(ans) - 1 if ans else None, I.bottom_witness_ok(),
                 I.top_witness_ok(), ks[0] if ks else None), flush=True)
