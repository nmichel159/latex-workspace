"""Stronger or different relaxations on the PC counterexamples of the hub family.

1. SPC (singleton path consistency): for every position j and value a, restrict the domain of j to {a} and run PC;
   delete a if PC refutes; repeat until nothing changes.  'yes' iff all domains stay non-empty.
2. Simple-path CSP: the path-position CSP with walks replaced by simple paths (edges at non-adjacent positions are
   vertex-disjoint, edges at adjacent positions are different); a consistent zigzag of length exactly L is a
   solution.  Decision: 'yes' iff PC of the simple-path CSP is non-empty for some odd L <= n.
3. Hub family with longer routes (route rB of gadget p has length 4 through a private middle node), which gives
   simple paths of several lengths.
Usage: python variants.py"""
import time
import numpy as np
import zz
import pcfast
import hubimp


def build_simple(z, L):
    csp = zz.CSP(z, L)
    E = csp.E
    D = len(E)
    doms = csp.init_domains()
    full = (1 << D) - 1
    R = np.zeros((L, L, D, D), dtype=bool)
    dm = np.zeros((L, D), dtype=bool)
    for j in range(L):
        for i in zz.bits(doms[j]):
            dm[j, i] = True
    for j in range(L):
        R[j, j] = np.diag(dm[j])
        for k in range(L):
            if k == j:
                continue
            for a in range(D):
                if not dm[j, a]:
                    continue
                m = csp.rel(j, k, a)
                for b in zz.bits(m & full):
                    if not dm[k, b]:
                        continue
                    sa, sb = set(E[a]), set(E[b])
                    if abs(j - k) == 1:
                        if a == b:
                            continue
                    elif sa & sb:
                        continue
                    R[j, k, a, b] = True
    return R


def pc_simple(z, L):
    R = build_simple(z, L)
    return pcfast.pc_closure(R)


def spc(z, L=None):
    R0, csp = pcfast.build(z, L)
    if R0 is None:
        return False
    if not pcfast.pc_closure(R0):
        return False
    L = R0.shape[0]
    changed = True
    while changed:
        changed = False
        for j in range(L):
            for a in np.nonzero(R0[j, j].diagonal())[0]:
                R = R0.copy()
                keep = np.zeros(R.shape[2], dtype=bool)
                keep[a] = True
                R[j, :] &= keep[None, :, None]
                R[:, j] &= keep[None, None, :]
                if not pcfast.pc_closure(R):
                    R0[j, :, a, :] = False
                    R0[:, j, :, a] = False
                    changed = True
                    if not pcfast.pc_closure(R0):
                        return False
    return True


if __name__ == "__main__":
    for strict in (False, True):
        for m, mp in ((2, 2), (2, 3)):
            z, names = hubimp.hubimp(m, mp, strict=strict)
            t0 = time.time()
            ex = zz.exact_dfs(z)[0]
            s = spc(z)
            print("hubimp(%d,%d,%s): n=%d exact=%s SPC=%s %.0fs" % (m, mp, "strict" if strict else "classes",
                                                                  z.n, ex, s, time.time() - t0), flush=True)
            t0 = time.time()
            ys = [L for L in range(1, z.n + 1, 2) if pc_simple(z, L)]
            print("   simple-path CSP: PC non-empty for L in", ys, "%.0fs" % (time.time() - t0), flush=True)
