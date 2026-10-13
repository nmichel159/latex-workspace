"""Per-formula checks of the claims of theory-hardness.md, Sections 2.1-2.2, Theorem 2.5, Corollary 2.6, on the graph
built by vred.build. Every check is exact. Names of the checks:

  R0  |V| = 2M + L and |E| = M(M-1) + (m+1) + 4L + sum_i (|O_i| - 1); every occurrence vertex has exactly two
      neighbours in K_A and two in K_B; the graph is simple (vlib.Gr raises otherwise)
  R1  c(u,v) = c0 (scipy Dinic and the pure-Python augmenting-path flow)
  R2  d(u,v) = 2
  R3  diameter exactly 3, so every pair has d <= 3 (class "d <= 3 or c <= 2")
  R4  the minimum cuts found by residual-closure enumeration are exactly {A_tau}
  R5  certificate: lambda({u},{v,x}) > c0 for x in K_A - u, lambda({u,x},{v}) > c0 for x in K_B - v, and for each
      sync edge oo' lambda({u,o},{v,o'}) > c0 and lambda({u,o'},{v,o}) > c0; |delta(A_tau)| = c0 for every tau.
      (Together: the minimum cuts are exactly the A_tau, proved without any enumeration.)
  R6  brute force over all vertex sets (n <= BRUTE_N) or naive branching (n <= BRANCH_N): same family
  R7  [some minimum cut contains a u-v path] (cut graphs of the R4 cuts) == satisfiable (brute force)
  R7b for every assignment tau: u, v connected in H_tau iff tau satisfies phi (Lemma 2.4)
  R8  definition-based cp: [cp = c] by cp_eq_c_bb2 == satisfiable, and f(u h_m v) = 2 + c_{G - u h_m v} = c0 + 1
      (so cp <= c + 1 and cp = c + 1 = c + d - 1 iff unsatisfiable)               (when the node budget allows)
  R9  satisfiable: the shortest u-v path inside a path-containing minimum cut has odd length >= 2m + 1
  R10 |delta(A)| = c0 + s(A) for every A with K_A <= A <= V - K_B (L <= LEMMA23_L)
  R11 not in DC and not in "d <= 2 or c <= 3": a filler of K_A and a filler of K_B have d = 3 and c >= 4
      (recorded: c of the two fillers, expected c0 = M - 2 because delta(K_A) separates them; Remark (2) says M - 1)
"""

import itertools
import time

import vlib
import vred

BRUTE_N = 25
BRANCH_N = 70
LEMMA23_L = 12


def check_formula(clauses, sync_order="natural", seed=0, bb_nodes=20000, do_branch=True, do_bb=True):
    t0 = time.time()
    R = vred.build(clauses, sync_order, seed)
    g, u, v, c0, M, m, L = R["g"], R["u"], R["v"], R["c0"], R["M"], R["m"], R["L"]
    fails = []
    info = dict(n=g.n, e=g.m, c0=c0, m=m, L=L)

    def fail(name, *data):
        fails.append((name,) + data)

    # R0
    if g.n != 2 * M + L:
        fail("R0-n", g.n, 2 * M + L)
    if g.m != vred.claimed_edge_count(R):
        fail("R0-e", g.m, vred.claimed_edge_count(R))
    KA, KB = set(R["KA"]), set(R["KB"])
    for o, k, j, lit in R["occ"]:
        na = sum(1 for y, e in g.adj[o] if y in KA)
        nb = sum(1 for y, e in g.adj[o] if y in KB)
        if na != 2 or nb != 2:
            fail("R0-occ", o, na, nb)
    # R1
    c = vlib.flow_value(g, [u], [v])
    info["c"] = c
    if c != c0:
        fail("R1", c, c0)
    # R2, R3
    D = vlib.distances(g)
    info["d"] = int(D[u, v])
    info["diam"] = int(D.max())
    if D[u, v] != 2:
        fail("R2", int(D[u, v]))
    if D.max() != 3:
        fail("R3", int(D.max()))
    # claimed family
    claimed = {}
    for tau in vred.assignments(R):
        claimed[vred.A_tau(R, tau)] = tau
    nvars = len(vred.variables(R))
    if len(claimed) != 2 ** nvars:
        fail("A_tau-not-distinct", len(claimed), 2 ** nvars)
    # R4
    cpy, cuts = vlib.min_cuts_residual(g, u, v)
    if cpy != c:
        fail("R1-py", cpy, c)
    info["cuts"] = len(cuts)
    if set(cuts) != set(claimed) or len(cuts) != len(set(cuts)):
        extra = [sorted(A) for A in set(cuts) - set(claimed)][:2]
        miss = len(set(claimed) - set(cuts))
        fail("R4", len(cuts), len(claimed), extra, miss)
    # R5
    for x in R["KA"]:
        if x != u and vlib.flow_value(g, [u], [v, x]) <= c0:
            fail("R5-KA", x)
    for x in R["KB"]:
        if x != v and vlib.flow_value(g, [u, x], [v]) <= c0:
            fail("R5-KB", x)
    for o1, o2 in R["sync"]:
        if vlib.flow_value(g, [u, o1], [v, o2]) <= c0 or vlib.flow_value(g, [u, o2], [v, o1]) <= c0:
            fail("R5-sync", o1, o2)
    for A in claimed:
        if vlib.cut_size(g, A) != c0:
            fail("R5-Atau", sorted(A), vlib.cut_size(g, A))
    # R6
    info["R6"] = "-"
    if g.n <= BRUTE_N:
        cb, bcuts = vlib.min_cuts_brute(g, u, v)
        info["R6"] = "brute"
        if cb != c or set(bcuts) != set(claimed):
            fail("R6-brute", cb, len(bcuts), len(claimed))
    elif do_branch and g.n <= BRANCH_N:
        brc, calls = vlib.min_cuts_branch(g, u, v, c)
        info["R6"] = "branch"
        if set(brc) != set(claimed):
            fail("R6-branch", len(brc), len(claimed))
    # R7, R7b, R9
    sat = vred.is_sat(clauses)
    info["sat"] = sat
    ans = False
    mind = None
    for A, tau in claimed.items():
        conn = vlib.cut_graph_connects(g, A, u, v)
        if conn != vred.satisfies(clauses, tau):
            fail("R7b", tau, conn)
        if conn:
            dd = vlib.cut_graph_dist(g, A, u, v)
            mind = dd if mind is None else min(mind, dd)
    for A in cuts:
        if vlib.cut_graph_connects(g, A, u, v):
            ans = True
    info["pimc"] = ans
    if ans != sat:
        fail("R7", ans, sat)
    info["minlen"] = mind
    if sat and (mind is None or mind < 2 * m + 1 or mind % 2 == 0):
        fail("R9", mind, 2 * m + 1)
    # R8
    info["R8"] = "-"
    hm = R["h"][m]
    eid = {e: i for i, e in enumerate(g.edges)}
    p0 = [eid[(min(u, hm), max(u, hm))], eid[(min(hm, v), max(hm, v))]]
    f0 = 2 + vlib.flow_value(g, [u], [v], p0)
    if f0 != c0 + 1:
        fail("R8-f0", f0, c0 + 1)
    if do_bb:
        try:
            a, path, nodes = vlib.cp_eq_c_bb2(g, u, v, c, node_limit=bb_nodes)
            info["R8"] = "bb(%d)" % nodes
            if a != sat:
                fail("R8", a, sat, path)
            if path is not None:
                # the path lies in delta(A) for some claimed A; its length is odd and >= 2m+1
                if len(path) - 1 < 2 * m + 1 or (len(path) - 1) % 2 == 0:
                    fail("R8-len", path)
                inside = [A for A in claimed if all((x in A) != (y in A) for x, y in zip(path, path[1:]))]
                if not inside:
                    fail("R8-notincut", path)
        except vlib.TooMany:
            info["R8"] = "budget"
    # R10
    info["R10"] = "-"
    if L <= LEMMA23_L:
        info["R10"] = "all"
        occs = [o for o, k, j, lit in R["occ"]]
        syncs = R["sync"]
        for bits in itertools.product([0, 1], repeat=L):
            A = set(R["KA"]) | {o for o, b in zip(occs, bits) if b}
            s = sum(1 for a, b in syncs if (a in A) != (b in A))
            if vlib.cut_size(g, A) != c0 + s:
                fail("R10", sorted(A))
                break
    # R11
    fa, fb = R["KA"][-1], R["KB"][-1]
    if not (fa >= m + 3 and fb >= M + m + 3):
        fail("R11-fillers", fa, fb)
    cff = vlib.flow_value(g, [fa], [fb])
    info["c_fillers"] = cff
    info["c_fillers_is_M-1"] = (cff == M - 1)      # Remark (2) of Section 2.2 claims c = M - 1
    if D[fa, fb] != 3 or cff < 4:
        fail("R11", int(D[fa, fb]), cff, M - 1)
    if cff != c0:                                   # delta(K_A) separates the fillers, so c <= c0 = M - 2
        fail("R11-c0", cff, c0)
    info["time"] = round(time.time() - t0, 2)
    return info, fails
