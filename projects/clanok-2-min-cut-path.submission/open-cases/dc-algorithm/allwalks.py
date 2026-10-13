"""Does the 'all walks' Duplicator strategy certify that PC does not refute an instance?

Family W = all u-v walks of length L in the path-position sense (unary and adjacency constraints only).  Network
N_jk = {(W_j, W_k) : W in W, W_j compatible with W_k}.  N is path consistent iff for every walk W, positions j, k
with W_j ~ W_k and every l there is a walk W' with W'_j = W_j, W'_k = W_k and W'_l compatible with both.
Then the PC closure contains N, so PC does not refute.  This script tests the condition exactly by reachability.
Usage: python allwalks.py L   (on hubimp.hubimp(2, 2), both versions)"""
import sys
import numpy as np
import zz
import hubimp


def check(z, L):
    csp = zz.CSP(z, L)
    E = csp.E
    D = len(E)
    doms = csp.init_domains()
    # step[j][a, b]: value a at position j, value b at position j+1 adjacent
    step = []
    for j in range(L - 1):
        M = np.zeros((D, D), dtype=bool)
        for a in range(D):
            m = csp.same_head[a] if j % 2 == 0 else csp.same_tail[a]
            for b in zz.bits(m):
                M[a, b] = True
        step.append(M)
    dom = np.array([[(doms[j] >> a) & 1 for a in range(D)] for j in range(L)], dtype=bool)
    # forward reachability from position 0, backward from position L-1
    fwd = np.zeros((L, D), dtype=bool)
    fwd[0] = dom[0]
    for j in range(1, L):
        fwd[j] = (fwd[j - 1].astype(int) @ step[j - 1].astype(int) > 0) & dom[j]
    bwd = np.zeros((L, D), dtype=bool)
    bwd[L - 1] = dom[L - 1]
    for j in range(L - 2, -1, -1):
        bwd[j] = (step[j].astype(int) @ bwd[j + 1].astype(int) > 0) & dom[j]
    alive = fwd & bwd
    # reach[j][k][a, b]: walk from (j, a) to (k, b), j < k, inside alive values
    reach = {}
    for j in range(L):
        M = np.diag(alive[j])
        reach[(j, j)] = M
        for k in range(j + 1, L):
            M = (M.astype(int) @ step[k - 1].astype(int) > 0) & alive[k][None, :]
            reach[(j, k)] = M
    compat = np.array([[(csp.compat[a] >> b) & 1 for b in range(D)] for a in range(D)], dtype=bool)
    bad = 0
    for j in range(L):
        for k in range(j + 1, L):
            pairs = reach[(j, k)] & compat
            for a, b in zip(*np.nonzero(pairs)):
                for l in range(L):
                    if l == j or l == k:
                        continue
                    ok_c = compat[a] & compat[b] & alive[l]
                    if l < j:
                        ok_c &= reach[(l, j)][:, a]
                    elif l < k:
                        ok_c &= reach[(j, l)][a, :] & reach[(l, k)][:, b]
                    else:
                        ok_c &= reach[(k, l)][b, :]
                    if not ok_c.any():
                        bad += 1
                        if bad <= 5:
                            print("  fails: j=%d a=%s k=%d b=%s l=%d" % (j, E[a], k, E[b], l))
    return bad


if __name__ == "__main__":
    L = int(sys.argv[1])
    for strict in (False, True):
        z, names = hubimp.hubimp(2, 2, strict=strict)
        print("H(2,2) %s, L = %d: failures of the all-walks condition: %d"
              % ("partial order" if strict else "classes", L, check(z, L)), flush=True)
