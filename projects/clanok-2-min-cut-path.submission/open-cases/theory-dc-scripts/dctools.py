"""Tools of the agent theory-DC for the open case of the class DC (d(u,v) = 2, c(u,v) >= 3).

Imports the read-only library checks/mcp.py.  Everything is exact (no heuristics).

  analyse(n, edges, u, v)   c, d, DC membership, all minimum u-v cuts (vertex-set enumeration, n <= ~22),
                            for each minimum cut the lengths of the u-v paths inside it, cp by cp_brute
  path_in_some_min_cut      test of a given u-v path: max flow between its even- and odd-indexed vertices
  q_class, ears             3-edge-connectivity class of u and the ears (Lemma 2 of theory-dc.md)
"""

import os
import sys
import itertools
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
CHECKS = os.path.normpath(os.path.join(HERE, "..", "..", "checks"))
sys.path.insert(0, CHECKS)
import mcp  # noqa: E402


def gr(n, edges):
    return mcp.Gr(n, edges)


def adj_masks(g):
    am = [0] * g.n
    for a, b in g.edges:
        am[a] |= 1 << b
        am[b] |= 1 << a
    return am


def boundary_size(am, A):
    s = 0
    x = A
    while x:
        low = x & -x
        i = low.bit_length() - 1
        s += (am[i] & ~A).bit_count()
        x ^= low
    return s


def min_cut_sets(g, u, v):
    """(c, list of vertex masks A with u in A, v not in A, |delta(A)| = c).  Enumerates the closed sets of
    the residual digraph of a maximum flow (Picard-Queyranne), so it is fast also for larger n."""
    c, flow, _ = mcp.maxflow(g, u, v)
    n = g.n
    # residual arcs x -> y (capacity left)
    radj = [[] for _ in range(n)]
    for e, (a, b) in enumerate(g.edges):
        f = flow[e]
        # arc a->b has residual 1 - f, arc b->a has residual 1 + f
        if 1 - f > 0:
            radj[a].append(b)
        if 1 + f > 0:
            radj[b].append(a)
    # closure: A is a minimum cut iff u in A, v not in A, A closed under residual arcs
    reach = []
    for s in range(n):
        seen = 1 << s
        dq = [s]
        for x in dq:
            for y in radj[x]:
                if not (seen >> y) & 1:
                    seen |= 1 << y
                    dq.append(y)
        reach.append(seen)
    base = reach[u]
    if (base >> v) & 1:
        raise RuntimeError("v reachable from u in residual graph")
    # vertices that can be added: those whose closure avoids v
    cand = [x for x in range(n) if not (base >> x) & 1 and not (reach[x] >> v) & 1]
    # enumerate closed sets containing base by DFS over candidates in a fixed order
    res = set()
    cand.sort()

    def rec(i, A):
        if i == len(cand):
            res.add(A)
            return
        x = cand[i]
        if (A >> x) & 1:
            rec(i + 1, A)
            return
        # exclude x: A must stay without x; any later addition must not force x -- checked at the end
        rec(i + 1, A)
        rec(i + 1, A | reach[x])

    rec(0, base)
    # keep only sets that are closed and avoid v (closure of union is union of closures, so all are closed)
    out = []
    am = adj_masks(g)
    for A in res:
        if (A >> v) & 1:
            continue
        if boundary_size(am, A) == c:
            out.append(A)
    return c, sorted(out)


def cut_edges(g, A):
    return [e for e, (a, b) in enumerate(g.edges) if ((A >> a) ^ (A >> b)) & 1]


def paths_in_edge_set(g, u, v, emask, limit=100000):
    """All simple u-v paths using only edges of emask (vertex tuples)."""
    return [vs for vs, es in mcp.simple_paths(g, u, v, removed=g.full() ^ emask, limit=limit)]


def shortest_in_edge_set(g, u, v, emask):
    es = mcp.shortest_path_edges(g, u, v, removed=g.full() ^ emask)
    return None if es is None else len(es)


def flow_between_sets(g, S, T):
    """Maximum number of edge-disjoint paths between vertex sets S and T (disjoint), by adding two
    super-vertices joined to S and T by edges of capacity |E| (simulated by parallel edges)."""
    n = g.n
    s, t = n, n + 1
    big = g.m + 1
    # build an explicit capacity graph and run Edmonds-Karp
    cap = {}
    nbr = [set() for _ in range(n + 2)]

    def add(a, b, c):
        cap[(a, b)] = cap.get((a, b), 0) + c
        cap.setdefault((b, a), 0)
        nbr[a].add(b)
        nbr[b].add(a)

    for a, b in g.edges:
        add(a, b, 1)
        add(b, a, 1)
    for x in S:
        add(s, x, big)
    for x in T:
        add(x, t, big)
    value = 0
    while True:
        par = {s: None}
        dq = deque([s])
        while dq and t not in par:
            x = dq.popleft()
            for y in nbr[x]:
                if y not in par and cap[(x, y)] > 0:
                    par[y] = x
                    dq.append(y)
        if t not in par:
            return value
        y = t
        while par[y] is not None:
            x = par[y]
            cap[(x, y)] -= 1
            cap[(y, x)] += 1
            y = x
        value += 1


def path_in_some_min_cut(g, path, c):
    """A u-v path x0..xk lies in some minimum u-v cut iff k is odd and the even- and odd-indexed vertices
    are separated by c edges (Lemma O3/O6 of theory-dc.md)."""
    if len(path) % 2 == 1:
        return False
    S = path[0::2]
    T = path[1::2]
    return flow_between_sets(g, S, T) == c


def q_class(g, u):
    return [x for x in range(g.n) if x == u or mcp.edge_conn(g, u, x, limit=3) >= 3]


def analyse(n, edges, u, v, want_cp=True, path_limit=200000):
    g = gr(n, edges)
    D = mcp.dist_matrix(g)
    dc, bad = mcp.in_dc(g, D)
    c, cuts = min_cut_sets(g, u, v)
    info = {"n": n, "m": g.m, "u": u, "v": v, "c": c, "d": D[u][v], "in_dc": dc, "dc_witness": bad,
            "num_min_cuts": len(cuts)}
    lens_by_cut = []
    for A in cuts:
        em = mcp.mask_of(cut_edges(g, A))
        sh = shortest_in_edge_set(g, u, v, em)
        if sh is not None:
            lens = sorted({len(p) - 1 for p in paths_in_edge_set(g, u, v, em, limit=path_limit)})
            lens_by_cut.append((A, sh, lens))
    info["cuts_with_path"] = lens_by_cut
    info["min_len_over_cuts"] = min((sh for _, sh, _ in lens_by_cut), default=None)
    if want_cp:
        info["cp"] = mcp.cp_brute(g, u, v)[0]
    return g, info


def fmt(info):
    s = "n=%d m=%d u=%d v=%d c=%d d=%s inDC=%s #mincuts=%d" % (
        info["n"], info["m"], info["u"], info["v"], info["c"], info["d"], info["in_dc"], info["num_min_cuts"])
    if "cp" in info:
        s += " cp=%d" % info["cp"]
    s += " cuts-with-path=%d min-len=%s" % (len(info["cuts_with_path"]), info["min_len_over_cuts"])
    return s
