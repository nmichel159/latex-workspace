"""Hub instances with ties: every E-side contains the hub node beta, so P2 holds for every two incomparable
elements (common bottom beta).  Entry classes A_1..A_k (member with E-side {a, beta}), exit classes B_1..B_k (member
with E-side {beta, t}); gadgets g_ij in series from s to a, gadget g_ij has two routes, the F-side of a member of A_i
and the F-side of a member of B_j (E-side {beta}).  No-instance: entry A_i and exit B_j in E-mode block g_ij.
Usage: python hubties.py KMAX"""
import sys
import time
import tieslib
import zz
import pcfast


def hubties(k, order=None):
    b = tieslib.Builder()
    b.node("s")
    b.node("t")
    pairs = [(i, j) for i in range(k) for j in range(k)] if order is None else order
    nodes = ["s"] + ["n%d" % p for p in range(1, len(pairs))] + ["a"]
    for p, (i, j) in enumerate(pairs):
        b.switch(("rA", i, j), ("A", i), ["beta"], [nodes[p], nodes[p + 1]])
        b.switch(("rB", i, j), ("B", j), ["beta"], [nodes[p], nodes[p + 1]])
    for i in range(k):
        b.switch(("entry", i), ("A", i), ["a", "beta"], [])
        b.switch(("exit", i), ("B", i), ["beta", "t"], [])
    return b.inst("s", "t")


def report(name, inst, L=None):
    t0 = time.time()
    z = tieslib.to_zz(inst)
    br = tieslib.brute(inst) is not None
    ex = zz.exact_dfs(z)[0]
    assert br == ex
    ac = zz.ac_answer(z, L)
    pc = pcfast.pc_answer(z, L) if ac else False
    flag = "  <-- PC FALSE POSITIVE" if (pc and not ex) else ""
    print("%-28s n=%3d |R|=%3d P2=%-5s exact=%-5s AC=%-5s PC=%-5s %6.1fs%s"
          % (name, z.n, len(z.R), not z.p2_bad(), ex, ac, pc, time.time() - t0, flag), flush=True)


if __name__ == "__main__":
    for k in range(1, int(sys.argv[1]) + 1):
        report("hubties k=%d" % k, hubties(k))
