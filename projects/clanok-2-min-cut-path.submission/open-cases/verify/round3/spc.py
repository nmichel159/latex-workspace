"""Singleton path consistency on the hub family (dc-algorithm.md §6.6), own code (agent verify-round3).
SPC: for every position j and every value a left in its domain, run strong PC with the domain of j fixed to {a};
delete a if PC refutes; repeat until nothing changes. Refuted iff some domain becomes empty.
Usage: python spc.py m mp version [L]"""
import sys
import time

import numpy as np

from hub3 import hub


def pc_from(inst, L, unary):
    E, unary0, base = inst.csp(L)
    m = len(E)
    T = np.zeros((L, L, m, m), dtype=bool)
    for i in range(L):
        T[i, i] = np.diag(unary[i] & unary0[i])
    for (i, j), M in base.items():
        T[i, j] = M & (unary[i][:, None] & unary[j][None, :])
        T[j, i] = T[i, j].T
    while True:
        Tf = T.astype(np.float32)
        newT = T.copy()
        for k in range(L):
            newT &= np.matmul(Tf[:, k][:, None, :, :], Tf[k, :][None, :, :, :]) > 0.5
        if not newT.any(axis=(2, 3)).all():
            return False, None
        if (newT == T).all():
            return True, np.array([np.diag(T[i, i]) for i in range(L)])
        T = newT


if __name__ == "__main__":
    m, mp, ver = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    H = hub(m, mp, ver)
    L = int(sys.argv[4]) if len(sys.argv) > 4 else (H.q if H.q % 2 == 1 else H.q - 1)
    t0 = time.time()
    E, unary0, base = H.csp(L)
    ok, dom = pc_from(H, L, unary0)
    print("H(%d,%d) %s L=%d: PC %s, domain sizes %s" % (m, mp, ver, L, ok, dom.sum(axis=1).tolist() if ok else None),
          flush=True)
    rounds = 0
    while ok:
        rounds += 1
        changed = False
        for j in range(L):
            for a in np.nonzero(dom[j])[0]:
                if not dom[j][a]:
                    continue
                un = dom.copy()
                un[j] = False
                un[j][a] = True
                r, _ = pc_from(H, L, un)
                if not r:
                    dom[j][a] = False
                    changed = True
            if not dom[j].any():
                ok = False
                break
        if ok:
            ok, dom2 = pc_from(H, L, dom)
            if ok:
                dom = dom2
        print("  round %d: %s, domain sizes %s (%.0fs)" % (rounds, "alive" if ok else "refuted",
                                                          dom.sum(axis=1).tolist(), time.time() - t0), flush=True)
        if not changed:
            break
    print("singleton PC:", "passes" if ok else "refutes")
