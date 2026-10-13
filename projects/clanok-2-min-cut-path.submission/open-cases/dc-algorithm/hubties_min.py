"""Smallest PC false positives in the hub family with ties (hubties.py), and independent re-checks.

hub(m, mp, order, tside): entry classes A_0..A_{m-1}, exit classes B_0..B_{mp-1}; one gadget per pair (i, j) with
the routes A_i, B_j; gadgets in the given order, from s to a (tside = False) or the first half before the hub and the
rest after it (tside = True: s .. a, hub, b .. t).
Checks per instance: exact by exact_dfs and by all down-sets (zz.exact), brute force over class modes; P2; AC; PC by
three implementations (pcfast.pc_answer, zz.pc_numpy, zz.path_consistency); minimal L for which PC says yes.
Usage: python hubties_min.py"""
import itertools
import time
import tieslib
import zz
import pcfast


def hub(m, mp, order=None, tside=False):
    b = tieslib.Builder()
    b.node("s")
    b.node("t")
    pairs = [(i, j) for i in range(m) for j in range(mp)] if order is None else list(order)
    if tside:
        h = (len(pairs) + 1) // 2
        left, right = pairs[:h], pairs[h:]
    else:
        left, right = pairs, []
    nl = ["s"] + ["n%d" % p for p in range(1, len(left))] + ["a"]
    for p, (i, j) in enumerate(left):
        b.switch(("rA", i, j), ("A", i), ["beta"], [nl[p], nl[p + 1]])
        b.switch(("rB", i, j), ("B", j), ["beta"], [nl[p], nl[p + 1]])
    exit_node = "t"
    if right:
        exit_node = "b"
        nr = ["b"] + ["o%d" % p for p in range(1, len(right))] + ["t"]
        for p, (i, j) in enumerate(right):
            b.switch(("rA", i, j), ("A", i), ["beta"], [nr[p], nr[p + 1]])
            b.switch(("rB", i, j), ("B", j), ["beta"], [nr[p], nr[p + 1]])
    for i in range(m):
        b.switch(("entry", i), ("A", i), ["a", "beta"], [])
    for j in range(mp):
        b.switch(("exit", j), ("B", j), ["beta", exit_node], [])
    return b.inst("s", "t")


def full_check(name, inst, all_pc=True):
    t0 = time.time()
    z = tieslib.to_zz(inst)
    br = tieslib.brute(inst) is not None
    ex = zz.exact_dfs(z)[0]
    ex2 = zz.exact(z)[0] if z.n <= 26 else None
    p2 = not z.p2_bad()
    ac = zz.ac_answer(z)
    pc1 = pcfast.pc_answer(z) if ac else False
    pc2 = pc3 = None
    if all_pc and ac:
        pc2 = zz.pc_numpy(z)
        pc3 = zz.pc_answer(z)
    Lmin = None
    if pc1:
        for L in range(1, z.n + 1, 2):
            if zz.ac_answer(z, L) and pcfast.pc_answer(z, L):
                Lmin = L
                break
    print("%-34s classes=%d switches=%2d n=%3d |R|=%3d P2=%-5s brute=%-5s exact=%-5s exact2=%-5s AC=%-5s "
          "PC=%s/%s/%s Lmin=%s %5.1fs"
          % (name, len(set(inst[3])), len(inst[1]), z.n, len(z.R), p2, br, ex, ex2, ac, pc1, pc2, pc3, Lmin,
             time.time() - t0), flush=True)
    return z, ex, pc1


if __name__ == "__main__":
    for m, mp in [(1, 1), (1, 2), (2, 1), (2, 2), (1, 3), (3, 1)]:
        pairs = [(i, j) for i in range(m) for j in range(mp)]
        seen = set()
        for order in itertools.permutations(pairs):
            for tside in (False, True):
                if len(pairs) == 1 and tside:
                    continue
                full_check("hub m=%d m'=%d %s %s" % (m, mp, "".join("%d%d" % p for p in order),
                                                    "two-sided" if tside else "one-sided"),
                           hub(m, mp, order, tside), all_pc=(m * mp <= 2))
            if m * mp > 2:
                break
