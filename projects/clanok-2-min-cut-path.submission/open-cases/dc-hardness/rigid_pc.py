"""AC / PC of the path-position CSP (dc-algorithm/zz.py) on the rigid family R_L and on 'broken' variants.

Variants (all keep P2):
  R_L         the rigid family (rigid.py): yes, unique solution.
  cut(L, k)   R_L without the node y_k in h_k & h_{k+1}: the h-path is cut; no solution (first-flip argument).
  tflip(L, k) R_L with t moved from h_L into Fl_k: no solution (Fl_k is reachable from s only through h_q, q > k).
Each line: exact 2CH answer (brute force), exact ZZ answer (zz.exact_dfs on the conversion), AC, PC, sizes.
Usage: python rigid_pc.py LMAX"""
import sys
import time
from swlib import to_zz, exact_2ch, relaxed_2ch, zz, p2_ok


def rigid_named(L, drop_y=None, t_in_flip=None):
    nodes = {}

    def node(name):
        if name not in nodes:
            nodes[name] = len(nodes)
        return nodes[name]

    path = [0] * (L + 1)
    flip = [0] * (L + 1)
    s = node("s")
    t = node("t")
    path[1] |= 1 << s
    if t_in_flip is None:
        path[L] |= 1 << t
    else:
        flip[t_in_flip] |= 1 << t
    for k in range(1, L):
        if k == drop_y:
            continue
        y = node(("y", k))
        path[k] |= 1 << y
        path[k + 1] |= 1 << y
    for p in range(1, L + 1):
        for q in range(p + 1, L + 1):
            if (q - p) % 2 == 1:
                z = node(("z", p, q))
                flip[p] |= 1 << z
                path[q] |= 1 << z
            else:
                w = node(("w", p, q))
                flip[p] |= 1 << w
                flip[q] |= 1 << w
    E = [0] * L
    F = [0] * L
    for k in range(1, L + 1):
        if k % 2 == 1:
            E[k - 1], F[k - 1] = path[k], flip[k]
        else:
            F[k - 1], E[k - 1] = path[k], flip[k]
    return (len(nodes), E, F, s, t)


def run(name, inst):
    t0 = time.time()
    ex2 = exact_2ch(inst) is not None
    rel = relaxed_2ch(inst)
    z, _ = to_zz(inst)
    exz = zz.exact_dfs(z)[0]
    ac = zz.ac_answer(z)
    pc = zz.pc_numpy(z) if ac else False
    flag = "  <-- PC FALSE POSITIVE" if (pc and not exz) else ""
    print("%-14s P2=%s exact2CH=%s exactZZ=%s relaxed=%s AC=%s PC=%s  n=%d |R|=%d  %.1fs%s" % (
        name, p2_ok(inst[1], inst[2]), ex2, exz, rel, ac, pc, z.n, len(z.R), time.time() - t0, flag), flush=True)
    return ex2, exz, ac, pc


if __name__ == "__main__":
    LMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    for L in range(2, LMAX + 1):
        run("R_%d" % L, rigid_named(L))
        for k in range(1, L):
            run("cut(%d,%d)" % (L, k), rigid_named(L, drop_y=k))
        for k in range(1, L):
            run("tflip(%d,%d)" % (L, k), rigid_named(L, t_in_flip=k))
