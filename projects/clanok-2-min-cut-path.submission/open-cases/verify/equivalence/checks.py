"""All checks of one small graph (n <= 16): theory-dc.md Lemma 1, Lemma 2, Corollary 3, Lemma 4,
Proposition 5, Proposition 11, Corollary 12, Theorem 13(a); dc-hardness.md Theorem 1.
check_graph(n, edges) returns (stats Counter, list of violations)."""
from collections import Counter
import numpy as np
from eqcore import (Small, adj_masks, all_dist, bit_list, bridges, component, cut_graph_adj, simple_paths,
                    pimc_from_cuts, cp_brute, lemma1_K, build_H, H_weights, restrict_mask,
                    preorder_from_cuts, leq, lt, is_downset, check_P2, zz_dfs, zz_downsets,
                    in_class_small, popcount)


def edgeset(adj_edges, A):
    return frozenset((a, b) for a, b in adj_edges if ((A >> a) & 1) != ((A >> b) & 1))


def lemma1(n, edges, adj, sm, dist, u, v, inDC, stats, viol, do_cp):
    """Lemma 1 for a pair with c(u,v) >= 2 in a connected graph with bridges."""
    K, Ke, idx = lemma1_K(n, edges, u)
    tag = ("L1", n, tuple(edges), u, v)
    if v not in idx:
        viol.append(tag + ("v not in K",))
        return None
    k = len(K)
    smK = Small(k, [(a, b, 1) for a, b in Ke])
    adjK = adj_masks(k, Ke)
    distK = all_dist(adjK)
    for i in range(k):
        for j in range(i + 1, k):
            x, y = K[i], K[j]
            if distK[i][j] != dist[x][y]:
                viol.append(tag + ("distance differs", x, y))
            if smK.conn(i, j) != sm.conn(x, y):
                viol.append(tag + ("connectivity differs", x, y))
    cG, cutsG = sm.min_cuts(u, v)
    cK, cutsK = smK.min_cuts(idx[u], idx[v])
    if cG != cK:
        viol.append(tag + ("c differs",))
    setsG = {edgeset(edges, A) for A in cutsG}
    setsK = {frozenset((min(K[a], K[b]), max(K[a], K[b])) for a, b in edgeset(Ke, A)) for A in cutsK}
    if setsG != setsK:
        viol.append(tag + ("minimum cut edge sets differ",))
    if do_cp:
        if cp_brute(sm, adj, u, v) != cp_brute(smK, adjK, idx[u], idx[v]):
            viol.append(tag + ("cp differs",))
        stats["L1 cp compared"] += 1
    if inDC and not in_class_small(smK, distK, k, 2):
        viol.append(tag + ("K not in DC",))
    stats["L1 pairs (graph with bridges, c>=2)"] += 1
    return K, Ke, idx


def open_case_checks(n, edges, u, v, inDC, stats, viol, do_cp, tagbase):
    """G 2-edge-connected (here: K), c(u,v) >= 3. Lemma 2, Cor 3, Lemma 4, Prop 5, Prop 11, Cor 12, Thm 13(a)."""
    adj = adj_masks(n, edges)
    sm = Small(n, [(a, b, 1) for a, b in edges])
    dist = all_dist(adj)
    c, cuts = sm.min_cuts(u, v)
    d = dist[u][v]
    tag = tagbase + (u, v)
    H = build_H(n, edges, adj, u, lambda x: sm.conn(u, x))
    for b in H["bad"]:
        viol.append(tag + ("Lemma 4(3)",) + b)
    Q, qi, Qmask, ears = H["Q"], H["qi"], H["Qmask"], H["ears"]
    q = len(Q)
    stats["P5 pairs (c>=3)"] += 1
    if v not in qi:
        viol.append(tag + ("v not in Q",))
        return
    # Lemma 4 (1)-(3) by brute force over all ear sets
    full = (1 << n) - 1
    bits = sm.bits
    sel = np.ones(1 << n, dtype=bool)
    for x in Q:
        sel &= ~bits[x]
    sel[0] = False
    earsets = np.nonzero(sel & (sm.cut == 2))[0].astype(np.int64)
    covered = 0
    for X in earsets:
        covered |= int(X)
    if covered != full & ~Qmask:
        viol.append(tag + ("Lemma 4(1): a vertex outside Q in no ear set",))
    for e in ears:
        C = e["X"]
        if int(sm.cut[C]) != 2:
            viol.append(tag + ("component of G-Q is not an ear set",))
        inter = (earsets & C) != 0
        if np.any((earsets[inter] & ~np.int64(C)) != 0):
            viol.append(tag + ("Lemma 4(3): ear set meets a component and leaves it",))
    stats["L4 ears"] += len(ears)
    stats["L4 ears attached at u or v"] += sum(1 for e in ears if e["p"] in (u, v) or e["s"] in (u, v))
    stats["L4 ears with p = s"] += sum(1 for e in ears if e["p"] == e["s"])
    stats["L4 long ears (>= 2 vertices)"] += sum(1 for e in ears if popcount(e["X"]) >= 2)
    # Lemma 4(4) for every minimum cut
    for A in cuts:
        for e in ears:
            X, p, s = e["X"], e["p"], e["s"]
            pin, sin = (A >> p) & 1, (A >> s) & 1
            if pin and sin:
                if X & ~A:
                    viol.append(tag + ("Lemma 4(4): both attachments in A, ear not inside", A, X))
            elif not pin and not sin:
                if X & A:
                    viol.append(tag + ("Lemma 4(4): both attachments outside, ear meets A", A, X))
            else:
                EX = [(a, b) for a, b in edges if (X >> a) & 1 or (X >> b) & 1]
                cnt = sum(1 for a, b in EX if ((A >> a) & 1) != ((A >> b) & 1))
                if cnt != 1:
                    viol.append(tag + ("Lemma 4(4): split ear with != 1 cut edge", A, X, cnt))
                for B in (A | X, A & ~X):
                    if int(sm.cut[B]) != c:
                        viol.append(tag + ("Lemma 4(4): A+X or A-X not minimum", A, X))
                    out = lambda S: {(a, b) for (a, b) in edgeset(edges, S) if (a, b) not in EX}
                    if out(B) != out(A):
                        viol.append(tag + ("Lemma 4(4): differs outside E[X]", A, X))
    # Proposition 5
    W = H_weights(q, H["real"], H["earE"])
    smH = Small(q, [(a, b, w) for (a, b), w in W.items()])
    cH, cutsH = smH.min_cuts(qi[u], qi[v])
    if cH != c:
        viol.append(tag + ("P5: c_H != c_G", c, cH))
    images = set()
    for A in cuts:
        B = restrict_mask(A, Q)
        images.add(B)
        if int(smH.cut[B]) != c:
            viol.append(tag + ("P5: trace not of size c", A))
    if images != set(cutsH):
        viol.append(tag + ("P5: traces != minimum cuts of H",))
    ansG, witG = pimc_from_cuts(adj, cuts, u, v)
    realadj = adj_masks(q, H["real"])
    ansH, witH = pimc_from_cuts(realadj, cutsH, qi[u], qi[v])
    if ansG != ansH:
        viol.append(tag + ("P5: PIMC(G) != PIMC(H)", ansG, ansH))
    # distance clause
    shortpairs = set()
    for e in ears:
        if e["short"] and e["p"] != e["s"]:
            shortpairs.add((min(qi[e["p"]], qi[e["s"]]), max(qi[e["p"]], qi[e["s"]])))
    for i in range(q):
        for j in range(i + 1, q):
            x, y = Q[i], Q[j]
            rhs = ((realadj[i] >> j) & 1) or (realadj[i] & realadj[j]) or ((i, j) in shortpairs)
            if (dist[x][y] <= 2) != bool(rhs):
                viol.append(tag + ("P5: distance clause", x, y))
    # Proposition 11, preorder
    down = preorder_from_cuts(q, cutsH)
    downG = preorder_from_cuts(n, cuts)
    for i in range(q):
        if restrict_mask(downG[Q[i]], Q) != down[i]:
            viol.append(tag + ("preorder of H != preorder of G on Q", Q[i]))
            break
    for a, b in H["real"] + H["earE"]:
        if not (leq(down, a, b) or leq(down, b, a)):
            viol.append(tag + ("P11: edge of H joins incomparable", Q[a], Q[b]))
    for a, b in edges:
        if not (leq(downG, a, b) or leq(downG, b, a)):
            viol.append(tag + ("P11/L4.3(i): edge of G joins incomparable", a, b))
    # minimum cuts of H = down-sets containing u, not v
    dsets = {D for D in range(1 << q) if (D >> qi[u]) & 1 and not (D >> qi[v]) & 1 and is_downset(down, D)}
    if dsets != set(cutsH):
        viol.append(tag + ("13(a): down-sets != minimum cuts of H",))
    # Lemma 2, Cor 3 on all paths inside minimum cuts
    for A in witG:
        ca = cut_graph_adj(adj, A)
        for P in simple_paths(ca, u, v):
            stats["paths inside minimum cuts"] += 1
            if (len(P) - 1) % 2 == 0:
                viol.append(tag + ("even path inside a cut",))
            for x in P[1:-1]:
                if sm.min_boundary(x, [u, v]) <= 2:
                    viol.append(tag + ("Lemma 2", A, P, x))
                if not (Qmask >> x) & 1:
                    viol.append(tag + ("Cor 3", A, P, x))
    if d != 2:
        return
    # Theorem 13(a)
    stats["13a pairs (d=2,c>=3)"] += 1
    if inDC:
        stats["13a pairs in DC"] += 1
    R = [(a, b) for a, b in H["real"] if not (leq(down, a, b) and leq(down, b, a))]
    Radj = adj_masks(q, R)
    if (Radj[qi[u]] >> qi[v]) & 1:
        viol.append(tag + ("uv in R",))
    p2f = check_P2(q, down, Radj)
    if inDC and p2f:
        viol.append(tag + ("Cor 12: P2 fails in DC", [(Q[a], Q[b]) for a, b in p2f]))
    if not inDC and p2f:
        stats["13a non-DC pairs where P2 fails (expected possible)"] += 1
    z1, path = zz_dfs(q, down, Radj, qi[u], qi[v])
    z2, D = zz_downsets(q, down, Radj, qi[u], qi[v])
    if not (z1 == z2 == ansG):
        viol.append(tag + ("13(a): ZZ answer != PIMC", z1, z2, ansG))
    if z1 and path is not None:
        # the zigzag lies inside the minimum cut generated by its valleys
        val = [Q[x] for x in path[0::2]]
        A = 0
        for a in val:
            A |= downG[a]
        if int(sm.cut[A]) != c or (A >> v) & 1:
            viol.append(tag + ("13(a): cut generated by valleys not minimum",))
        for i in range(len(path) - 1):
            x, y = Q[path[i]], Q[path[i + 1]]
            if ((A >> x) & 1) == ((A >> y) & 1):
                viol.append(tag + ("13(a): zigzag edge not in generated cut",))
    key = "DC" if inDC else "nonDC"
    stats["13a %s answer %s" % (key, "yes" if ansG else "no")] += 1
    if ansG:
        L = max(len(P) - 1 for A in witG for P in simple_paths(cut_graph_adj(adj, A), u, v))
        stats["13a %s longest witness length %d" % (key, L)] += 1
    if do_cp:
        cp = cp_brute(sm, adj, u, v)
        if cp != (c if ansG else c + 1):
            viol.append(tag + ("cp != c iff PIMC", cp, c, ansG))
        stats["cp compared"] += 1


def dcprime_checks(n, edges, adj, sm, dist, u, v, stats, viol, tagbase):
    """dc-hardness.md Theorem 1 for a pair with d = 2, c >= 4 in a graph of the class d<=2 or c<=3."""
    tag = tagbase + ("DC'", u, v)
    c, cuts = sm.min_cuts(u, v)
    Q4 = [x for x in range(n) if x == u or sm.conn(u, x) >= 4]
    q = len(Q4)
    qi = {x: i for i, x in enumerate(Q4)}
    downG = preorder_from_cuts(n, cuts)
    for a, b in edges:
        if not (leq(downG, a, b) or leq(downG, b, a)):
            viol.append(tag + ("edge joins incomparable", a, b))
    ans, wit = pimc_from_cuts(adj, cuts, u, v)
    for A in wit:
        for P in simple_paths(cut_graph_adj(adj, A), u, v):
            for x in P:
                if x not in qi:
                    viol.append(tag + ("Cor 4.2(b): path vertex outside Q4", x))
    down = [restrict_mask(downG[x], Q4) for x in Q4]
    traces = {restrict_mask(A, Q4) for A in cuts}
    dsets = {D for D in range(1 << q) if (D >> qi[u]) & 1 and not (D >> qi[v]) & 1 and is_downset(down, D)}
    if traces != dsets:
        viol.append(tag + ("traces on Q4 != down-sets",))
    R = [(qi[a], qi[b]) for a, b in edges if a in qi and b in qi
         and not (leq(downG, a, b) and leq(downG, b, a))]
    Radj = adj_masks(q, R)
    p2f = check_P2(q, down, Radj)
    if p2f:
        viol.append(tag + ("P2 fails on Q4", [(Q4[a], Q4[b]) for a, b in p2f]))
    z1, _ = zz_dfs(q, down, Radj, qi[u], qi[v])
    z2, _ = zz_downsets(q, down, Radj, qi[u], qi[v])
    if not (z1 == z2 == ans):
        viol.append(tag + ("Thm 1: ZZ answer != PIMC", z1, z2, ans))
    stats["DC' pairs (d=2,c>=4)"] += 1
    stats["DC' answer %s" % ("yes" if ans else "no")] += 1


def check_graph(n, edges, ordered=True, do_cp=None, pairs=None):
    stats = Counter()
    viol = []
    edges = [(min(a, b), max(a, b)) for a, b in edges]
    adj = adj_masks(n, edges)
    if component(adj, 0) != (1 << n) - 1:
        return stats, viol
    if do_cp is None:
        do_cp = n <= 9
    sm = Small(n, [(a, b, 1) for a, b in edges])
    dist = all_dist(adj)
    inDC = in_class_small(sm, dist, n, 2)
    inDCp = in_class_small(sm, dist, n, 3)
    hasbr = bool(bridges(n, edges))
    stats["graphs"] += 1
    stats["graphs in DC"] += inDC
    stats["graphs in DC'"] += inDCp
    tagbase = (n, tuple(edges))
    if pairs is None:
        pairs = [(u, v) for u in range(n) for v in range(n) if u != v and (ordered or u < v)]
    for u, v in pairs:
        if True:
            c = sm.conn(u, v)
            if c < 2:
                continue
            if hasbr:
                K, Ke, idx = lemma1(n, edges, adj, sm, dist, u, v, inDC, stats, viol, do_cp)
            else:
                K, Ke, idx = list(range(n)), edges, {x: x for x in range(n)}
            if c >= 3:
                open_case_checks(len(K), Ke, idx[u], idx[v], inDC, stats, viol, do_cp,
                                 tagbase + (("K", tuple(K)) if hasbr else ()))
            if inDCp and dist[u][v] == 2 and c >= 4:
                dcprime_checks(n, edges, adj, sm, dist, u, v, stats, viol, tagbase)
    return stats, viol
