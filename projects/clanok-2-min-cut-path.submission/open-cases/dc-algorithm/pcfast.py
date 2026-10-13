"""Fast strong path consistency (PC) of the path-position CSP of zz.py, with float32 BLAS products.

Network: R[j][k] is a D x D 0/1 matrix (value a of position j, value b of position k allowed together), with
R[j][j] = diag(domain of j).  Strong PC fixpoint: R[j][k] &= R[j][l] o R[l][k] for all j, k, l (l = j or l = k
filters by the domains).  Returns False when some relation or domain becomes empty (PC refutes), else True.
Same answers as zz.pc_numpy (checked by test_pcfast.py), much faster: one sweep is L batched products per l.
"""
import numpy as np
import zz


def build(z, L=None, window=None):
    csp = zz.CSP(z, L)
    csp.window = window
    L, D = csp.L, len(csp.E)
    doms = csp.init_domains()
    doms = zz.arc_consistency(csp, doms)
    if doms is None or D == 0:
        return None, csp
    dm = np.array([[(doms[j] >> i) & 1 for i in range(D)] for j in range(L)], dtype=bool)
    R = np.zeros((L, L, D, D), dtype=bool)
    # base relations
    for j in range(L):
        R[j, j] = np.diag(dm[j])
        for k in range(L):
            if k == j:
                continue
            for i in range(D):
                if dm[j, i]:
                    m = csp.rel(j, k, i)
                    for b in zz.bits(m):
                        R[j, k, i, b] = dm[k, b]
    return R, csp


def pc_closure(R, max_sweeps=10000):
    """In place; returns True if the closure is non-empty everywhere."""
    L = R.shape[0]
    Rf = R.astype(np.float32)
    for sweep in range(max_sweeps):
        changed = False
        for l in range(L):
            A = Rf[:, l]          # (L, D, D): R[j, l]
            B = Rf[l, :]          # (L, D, D): R[l, k]
            C = np.matmul(A[:, None], B[None, :]) > 0.5   # (L, L, D, D)
            newR = R & C
            if not np.array_equal(newR, R):
                changed = True
                R[...] = newR
                Rf = R.astype(np.float32)
                # empty domain?
                diag = R[np.arange(L), np.arange(L)]          # (L, D, D)
                if not diag.any(axis=(1, 2)).all():
                    return False
        if not changed:
            break
    diag = R[np.arange(L), np.arange(L)]
    if not diag.any(axis=(1, 2)).all():
        return False
    # every relation non-empty
    return bool(R.any(axis=(2, 3)).all())


def pc_answer(z, L=None, window=None, return_R=False):
    R, csp = build(z, L, window)
    if R is None:
        return (False, None) if return_R else False
    ok = pc_closure(R)
    return (ok, R) if return_R else ok
