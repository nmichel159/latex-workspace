"""Attempt to move the reduction of Section 2 into DC (theory-hardness.md, Section 6.1).

Variant G*: K_A and K_B are cliques on M' = m + 3 vertices (no fillers): K_A = {h_0..h_m, a_1, a_2},
K_B = {beta_0..beta_m, b_1, b_2}; F' = {h_k beta_k} + {a_1 b_1, a_2 b_2} (a perfect matching, so every vertex of K_B
has a neighbor in K_A and K_A-K_B distances are <= 2); forcing by t = 2L + 2 ears (new vertices of degree 2) between
u and every other vertex of K_A and between v and every other vertex of K_B; occurrence vertices and sync edges as in
Section 2.1.  Checked exactly: c(u,v), the minimum cuts (Picard-Queyranne) = the sets A_tau plus the ears of K_A,
answer = satisfiability; and every pair (x, y) with d(x,y) >= 3 and c(x,y) >= 3 (the DC violations), classified.
Output: results-dc-attempt.txt.
"""

import itertools
import os
import random
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import exact as ex  # noqa: E402
import reduction as rd  # noqa: E402


def build_star(phi):
    m = len(phi)
    L = sum(len(C) for C in phi)
    Mp = m + 3
    h = list(range(m + 1))
    a1, a2 = m + 1, m + 2
    KA = list(range(Mp))
    beta = [Mp + k for k in range(m + 1)]
    b1, b2 = Mp + m + 1, Mp + m + 2
    KB = list(range(Mp, 2 * Mp))
    u, v = h[0], beta[m]
    edges = []
    for grp in (KA, KB):
        edges += list(itertools.combinations(grp, 2))
    edges += [(h[k], beta[k]) for k in range(m + 1)] + [(a1, b1), (a2, b2)]
    nxt = 2 * Mp
    kind = {}
    occ_groups = {}
    for k, C in enumerate(phi, start=1):
        for lit in C:
            o = nxt
            nxt += 1
            kind[o] = ("pos" if lit > 0 else "neg", abs(lit), k)
            occ_groups.setdefault(abs(lit), []).append(o)
            if lit > 0:
                edges += [(o, beta[k - 1]), (o, beta[k]), (o, a1), (o, a2)]
            else:
                edges += [(o, h[k - 1]), (o, h[k]), (o, b1), (o, b2)]
    for os_ in occ_groups.values():
        edges += list(zip(os_, os_[1:]))
    t = 2 * L + 2
    ears_A = []
    for core, root in ((KA, u), (KB, v)):
        for x in core:
            if x == root:
                continue
            for _ in range(t):
                z = nxt
                nxt += 1
                edges += [(root, z), (z, x)]
                if core is KA:
                    ears_A.append(z)
    g = ex.UG(nxt, edges)
    return g, u, v, dict(KA=KA, KB=KB, kind=kind, groups=occ_groups, ears_A=ears_A, c0=Mp + 2 * L, t=t)


def run(phi):
    g, u, v, info = build_star(phi)
    c, cuts = ex.min_cuts_pq(g, u, v)
    vars_ = sorted(info["groups"])
    intended = set()
    for bits in itertools.product((False, True), repeat=len(vars_)):
        A = set(info["KA"]) | set(info["ears_A"])
        for var, val in zip(vars_, bits):
            if val:
                A.update(info["groups"][var])
        intended.add(frozenset(A))
    ans = any(ex.cut_graph_path(g, A, u, v) is not None for A in cuts)
    # DC violations among non-ear vertices (ears have degree 2, so c <= 2 for every pair with an ear)
    core = [x for x in range(g.n) if len(g.adj[x]) != 2 or x in (u, v)]
    D = {x: ex.bfs_dist(g, x) for x in core}
    viol = {}
    for x, y in itertools.combinations(core, 2):
        if D[x][y] > 2 and ex.cut_value(g, x, y, limit=3) >= 3:
            kx = info["kind"].get(x, ("core",))
            ky = info["kind"].get(y, ("core",))
            if kx[0] in ("pos", "neg") and ky[0] in ("pos", "neg"):
                key = "-".join(sorted((kx[0], ky[0]))) + (" same variable" if kx[1] == ky[1] else " different variables")
            else:
                key = "%s-%s" % (kx[0], ky[0])
            viol[key] = viol.get(key, 0) + 1
    return dict(phi=phi, n=g.n, m=g.m, c=c, c0=info["c0"], cuts_ok=(set(cuts) == intended and len(cuts) == len(intended)),
                ncuts=len(cuts), ans=ans, sat=rd.satisfiable(phi), viol=viol, d=ex.bfs_dist(g, u)[v])


def main():
    t0 = time.time()
    rng = random.Random(3)
    phis = [[[1], [1]], [[1], [2], [-3], [-4]], [[1], [-1]], [[1, -2, 3], [-1, 2, -3]], [[1, 2, 2], [-1, -2, -2], [1, -2, -2], [-1, 2, 2]]]
    phis += [rd.random_formula(rng, 3, 3) for _ in range(6)]
    lines = ["dc_attempt.py: the variant G* of the reduction (docstring)", ""]
    fails = 0
    for phi in phis:
        r = run(phi)
        ok = r["cuts_ok"] and r["ans"] == r["sat"] and r["c"] == r["c0"]
        fails += not ok
        lines.append("phi=%s |V|=%d |E|=%d c=%d (c0=%d) d=%d cuts=%d (= A_tau: %s) answer=%s sat=%s; DC violations: %s"
                     % (r["phi"], r["n"], r["m"], r["c"], r["c0"], r["d"], r["ncuts"], r["cuts_ok"], r["ans"], r["sat"],
                        r["viol"] if r["viol"] else "none (in DC)"))
    lines.append("")
    lines.append("formulas: %d, failures of (c = c0, cuts = A_tau, answer = sat): %d.  Time %.0f s." % (len(phis), fails, time.time() - t0))
    with open(os.path.join(HERE, "results-dc-attempt.txt"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
