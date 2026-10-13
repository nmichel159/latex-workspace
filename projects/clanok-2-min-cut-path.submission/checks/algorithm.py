"""Reference implementation of the linear-time algorithm of S11 (no brute force).

solve(g, u, v) for a pair with c(u,v) <= 2 returns a dict
    c, d, cp, cutpath (edge mask), case, and for c = 2 also
    F, tail, comp (piece of every vertex), squares, lam_minus, lam_plus, witness (the path found, or None)
and None if c(u,v) >= 3 (the algorithm does not apply).

Steps (all linear in |V| + |E| apart from the loop over the at most four (entering, leaving) pairs of every
square, whose cost is linear in the size of the square):
  1. two augmenting paths from u to v (unit capacities); a third one means c >= 3
  2. residual digraph: an edge with flow a->b has only the arc b->a, every other edge both arcs
  3. strongly connected components (iterative Kosaraju); F = edges with flow whose ends lie in different components
  4. pieces = components of G - F; squares = piece of u, piece of v, pieces with two entering edges
  5. lambda^- = breadth-first distances from u in G-vector, lambda^+ = distances to v (reverse search)
  6. for every square and every pair (entering g, leaving h): l = d - (count without |p|);
       l = 0: no;  l = 1: is xy an edge of the square whose removal separates alpha from beta;
       l = 2: one alpha-beta path q, candidates w = neighbours of x or y on q adjacent to both, test each;
       l >= 3 or l < 0: skipped (justified in the class DC only)
  7. cp = d if a path was found, d + 1 otherwise; the cut-path is the path found, or a shortest path plus a
     minimum cut (the edges leaving the set reachable from u in the residual digraph)

`mutation` breaks the algorithm on purpose (used by mutation_tests.py):
  "skip-l2"       never test l = 2
  "l1-nosep"      accept l = 1 whenever xy is an edge of the square (no separation test)
  "no-l1"         never test l = 1
  "swap-lambda"   use lambda^+ of the tail of g instead of lambda^- (wrong counts)
  "first-square"  look at the first square only
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp import Gr  # noqa: E402,F401  (only the graph container is shared with the brute force)


def _bfs_tree(g, s):
    dist = [None] * g.n
    par = [None] * g.n
    dist[s] = 0
    q = [s]
    for x in q:
        for y, e in g.adj[x]:
            if dist[y] is None:
                dist[y] = dist[x] + 1
                par[y] = (x, e)
                q.append(y)
    return dist, par


def _augment(g, flow, u, v):
    """One augmenting path in the residual graph (unit capacities, undirected edges)."""
    par = [None] * g.n
    par[u] = (-1, -1)
    q = [u]
    for x in q:
        if par[v] is not None:
            break
        for y, e in g.adj[x]:
            if par[y] is None:
                a = g.edges[e][0]
                cap = (1 - flow[e]) if x == a else (1 + flow[e])
                if cap > 0:
                    par[y] = (x, e)
                    q.append(y)
    if par[v] is None:
        return None, par
    y = v
    while y != u:
        x, e = par[y]
        flow[e] += 1 if x == g.edges[e][0] else -1
        y = x
    return True, par


def _scc(n, out):
    """Kosaraju, iterative.  out[x] = list of successors.  Returns component id per vertex."""
    order = []
    seen = [False] * n
    for s in range(n):
        if seen[s]:
            continue
        seen[s] = True
        stack = [(s, 0)]
        while stack:
            x, i = stack.pop()
            if i < len(out[x]):
                stack.append((x, i + 1))
                y = out[x][i]
                if not seen[y]:
                    seen[y] = True
                    stack.append((y, 0))
            else:
                order.append(x)
    rev = [[] for _ in range(n)]
    for x in range(n):
        for y in out[x]:
            rev[y].append(x)
    comp = [-1] * n
    c = 0
    for s in reversed(order):
        if comp[s] >= 0:
            continue
        comp[s] = c
        stack = [s]
        while stack:
            x = stack.pop()
            for y in rev[x]:
                if comp[y] < 0:
                    comp[y] = c
                    stack.append(y)
        c += 1
    return comp


def _mask(es, m):
    """Edge mask from a list of edge ids in time O(m) (bit operations on large integers are not constant time)."""
    buf = bytearray(m // 8 + 1)
    for e in es:
        buf[e >> 3] |= 1 << (e & 7)
    return int.from_bytes(buf, "little")


def _connected_without(g, inF, a, b, removed):
    """a, b connected in G - F - removed (that is inside one piece)?  `removed` is a tuple of edge ids.
    Visits only the piece of a, so the cost is linear in the size of the piece."""
    if a == b:
        return True
    seen = {a}
    q = [a]
    for x in q:
        for y, e in g.adj[x]:
            if y not in seen and not inF[e] and e not in removed:
                if y == b:
                    return True
                seen.add(y)
                q.append(y)
    return False


def _path_in_piece(g, inF, a, b):
    """One a-b path inside the piece (list of vertices) or None."""
    par = {a: None}
    q = [a]
    for x in q:
        for y, e in g.adj[x]:
            if y not in par and not inF[e]:
                par[y] = x
                q.append(y)
    if b not in par:
        return None
    path = [b]
    while path[-1] != a:
        path.append(par[path[-1]])
    path.reverse()
    return path


def solve(g, u, v, mutation=None, exhaustive=False, restrict_F=None):
    """exhaustive=True examines all squares and pairs even after a path has been found (the first one is kept);
    used only to time the worst case.
    restrict_F: a set of edge ids; only these edges of F are used (a coarser decomposition, S14 / Remark on
    coarser decompositions: F' = union of some minimum cuts)."""
    n, m = g.n, g.m
    d_dist, d_par = _bfs_tree(g, u)
    d = d_dist[v]
    flow = [0] * m
    ok1, _ = _augment(g, flow, u, v)
    if ok1 is None:
        return None            # disconnected
    ok2, _ = _augment(g, flow, u, v)
    if ok2 is None:
        # c = 1: cp = d (S0); a shortest path contains the bridge
        es = []
        y = v
        while y != u:
            x, e = d_par[y]
            es.append(e)
            y = x
        return dict(c=1, d=d, cp=d, cutpath=_mask(es, m), case="c=1", witness=None)
    ok3, _ = _augment(g, flow[:], u, v)
    if ok3 is not None:
        return None            # c >= 3
    # -- residual digraph ---------------------------------------------------------------------------
    out = [[] for _ in range(n)]
    for e, (a, b) in enumerate(g.edges):
        f = flow[e]
        if f <= 0:
            out[a].append(b)
        if f >= 0:
            out[b].append(a)
    scc = _scc(n, out)
    F = []
    tail = {}
    for e, (a, b) in enumerate(g.edges):
        if flow[e] != 0 and scc[a] != scc[b]:
            F.append(e)
            tail[e] = a if flow[e] > 0 else b
    if restrict_F is not None:
        F = [e for e in F if e in restrict_F]
        tail = {e: tail[e] for e in F}
    inF = [False] * m
    for e in F:
        inF[e] = True
    head = {e: g.other(e, tail[e]) for e in F}
    # -- pieces, squares ----------------------------------------------------------------------------
    comp = [-1] * n
    npieces = 0
    for s in range(n):
        if comp[s] >= 0:
            continue
        comp[s] = npieces
        q = [s]
        for x in q:
            for y, e in g.adj[x]:
                if comp[y] < 0 and not inF[e]:
                    comp[y] = npieces
                    q.append(y)
        npieces += 1
    ent = [[] for _ in range(npieces)]
    lea = [[] for _ in range(npieces)]
    for e in F:
        ent[comp[head[e]]].append(e)
        lea[comp[tail[e]]].append(e)
    pu, pv = comp[u], comp[v]
    squares = [p for p in range(npieces) if p == pu or p == pv or len(ent[p]) == 2]
    # -- G-vector distances -------------------------------------------------------------------------
    def arcs(x):
        for y, e in g.adj[x]:
            if inF[e] and tail[e] != x:
                continue
            yield y, e

    lam_minus = [None] * n
    parm = [None] * n
    lam_minus[u] = 0
    q = [u]
    for x in q:
        for y, e in arcs(x):
            if lam_minus[y] is None:
                lam_minus[y] = lam_minus[x] + 1
                parm[y] = (x, e)
                q.append(y)
    rarcs = [[] for _ in range(n)]
    for x in range(n):
        for y, e in arcs(x):
            rarcs[y].append((x, e))
    lam_plus = [None] * n
    nxt = [None] * n
    lam_plus[v] = 0
    q = [v]
    for x in q:
        for y, e in rarcs[x]:
            if lam_plus[y] is None:
                lam_plus[y] = lam_plus[x] + 1
                nxt[y] = (x, e)       # from y the first edge e of a shortest directed path leads to x
                q.append(y)
    dvec = lam_minus[v]
    # -- test the pairs ----------------------------------------------------------------------------
    witness = None
    for sq in squares:
        if mutation == "first-square" and sq != pu:
            continue
        ins = ent[sq] if sq != pu else [None]
        outs = lea[sq] if sq != pv else [None]
        for gg in ins:
            for hh in outs:
                x = u if gg is None else head[gg]
                y = v if hh is None else tail[hh]
                if gg is None:
                    alpha = u
                else:
                    other = [e for e in ent[sq] if e != gg]
                    alpha = head[other[0]] if other else x
                if hh is None:
                    beta = v
                else:
                    other = [e for e in lea[sq] if e != hh]
                    beta = tail[other[0]] if other else y
                base = 0
                if gg is not None:
                    base += (lam_plus[tail[gg]] if mutation == "swap-lambda" else lam_minus[tail[gg]]) + 1
                if hh is not None:
                    base += 1 + lam_plus[head[hh]]
                ell = dvec - base
                p_edges = None
                if ell == 1 and mutation != "no-l1":
                    if x != y and g.has_edge(x, y):
                        e = g.edge_id(x, y)
                        if not inF[e]:
                            if mutation == "l1-nosep" or not _connected_without(g, inF, alpha, beta, (e,)):
                                p_edges = [(x, y)]
                elif ell == 2 and mutation != "skip-l2":
                    if x != y and alpha != beta:
                        qpath = _path_in_piece(g, inF, alpha, beta)
                        cand = []
                        for z in (x, y):
                            if z in qpath:
                                i = qpath.index(z)
                                if i > 0:
                                    cand.append(qpath[i - 1])
                                if i + 1 < len(qpath):
                                    cand.append(qpath[i + 1])
                        for w in dict.fromkeys(cand):
                            if w == x or w == y or comp[w] != sq:
                                continue
                            if g.has_edge(x, w) and g.has_edge(w, y):
                                e1, e2 = g.edge_id(x, w), g.edge_id(w, y)
                                if inF[e1] or inF[e2]:
                                    continue
                                if not _connected_without(g, inF, alpha, beta, (e1, e2)):
                                    p_edges = [(x, w), (w, y)]
                                    break
                if p_edges is not None and witness is None:
                    es = []
                    # u -> tail(g)
                    if gg is not None:
                        t = tail[gg]
                        part = []
                        while t != u:
                            px, pe = parm[t]
                            part.append(pe)
                            t = px
                        es.extend(reversed(part))
                        es.append(gg)
                    for a, b in p_edges:
                        es.append(g.edge_id(a, b))
                    if hh is not None:
                        es.append(hh)
                        t = head[hh]
                        while t != v:
                            nx_, pe = nxt[t]
                            es.append(pe)
                            t = nx_
                    witness = (sq, gg, hh, p_edges, es)
                if witness and not exhaustive:
                    break
            if witness and not exhaustive:
                break
        if witness and not exhaustive:
            break
    res = dict(c=2, d=d, F=F, tail=tail, comp=comp, squares=squares, ent=ent, lea=lea, head=head,
               lam_minus=lam_minus, lam_plus=lam_plus, dvec=dvec, scc=scc)
    if witness:
        res.update(cp=d, cutpath=_mask(witness[4], m), case="path", witness=witness)
        return res
    # cp = d + 1: a shortest path plus a minimum cut (edges leaving the residual reach of u)
    reach = [False] * n
    reach[u] = True
    q = [u]
    for x in q:
        for y in out[x]:
            if not reach[y]:
                reach[y] = True
                q.append(y)
    es = [e for e, (a, b) in enumerate(g.edges) if reach[a] != reach[b]]       # a minimum cut
    y = v
    while y != u:                                                             # a shortest path
        x, e = d_par[y]
        es.append(e)
        y = x
    res.update(cp=d + 1, cutpath=_mask(es, m), case="shortest path + cut", witness=None)
    return res


# ---------------------------------------------------------------------------------------------------------
# the version without the promise "G in the class" (referee's version)
# ---------------------------------------------------------------------------------------------------------

def flow_paths(g, flow, u, v, mutation=None):
    """Two edge-disjoint u-v paths from a flow of value two by two searches in the digraph of the flow-carrying
    edges (arc a->b for an edge with flow from a to b): first a u-v path, then a u-v path after removing the arcs
    of the first.  Works also if the flow contains cycles.  Returns [(vertices, edges), (vertices, edges)] or None.
    Mutation "p2-no-removal": the second search does not remove the arcs of the first path."""
    n = g.n
    out = [[] for _ in range(n)]
    for e, (a, b) in enumerate(g.edges):
        f = flow[e]
        if f > 0:
            out[a].append((b, e))
        elif f < 0:
            out[b].append((a, e))
    used = set()
    paths = []
    for _ in range(2):
        par = {u: None}
        q = [u]
        for x in q:
            if v in par:
                break
            for y, e in out[x]:
                if y in par or (e in used and mutation != "p2-no-removal"):
                    continue
                par[y] = (x, e)
                q.append(y)
        if v not in par:
            return None
        vs, es = [v], []
        while par[vs[-1]] is not None:
            x, e = par[vs[-1]]
            es.append(e)
            vs.append(x)
        vs.reverse()
        es.reverse()
        used.update(es)
        paths.append((tuple(vs), tuple(es)))
    return paths


def solve_robust(g, u, v, mutation=None, exhaustive=False, flow=None):
    """The algorithm of the referee: correct (value d or d + 1, and a certificate when it may be wrong) for every
    connected graph and every pair with c(u,v) = 2, with no promise on the graph.

    For every square and every pair of an entering terminal x and a leaving terminal y with x != y
    (with (x, alpha) in {(a, b), (b, a)} and (y, beta) in {(c, d), (d, c)}), l = d(u,v) - d(u,x) - d(y,v):
      l >= 3        record the pair (x, y)   (whether or not alpha = beta)
      alpha != beta, l = 1: test the edge xy;  l = 2: test the paths x, w, y with xw or wy on the fixed
                    alpha-beta path q (at most four);  a tested path that separates alpha from beta in the
                    square: return d(u,v) and R_x u p u R_y   (outcome "path")
    If nothing was returned: d(u,v) + 1 with R u C (a shortest path and a minimum cut), outcome "certificate" if a
    pair was recorded (the pair is returned), else "value".
    p_1, p_2 come from the flow by flow_paths; D is the residual digraph of the flow along p_1 and p_2 (so a cycle
    in the net flow does no harm); F = edges of p_1 u p_2 whose ends lie in different strong components of D.

    exhaustive=True also collects all pairs with l >= 3 in res["pairs"] and does not stop at the first path (the
    outcome is the same).  `flow`: a given flow of value two (default: two augmentations; None is returned if
    c(u,v) >= 3; for c(u,v) = 1 the shortest path is returned).
    Mutations: "record-ge4", "record-ge2", "never-record", "skip-l2", "l1-nosep", "cut-missing", "p2-no-removal"."""
    n, m = g.n, g.m
    Du, parU = _bfs_tree(g, u)
    Dv, parV = _bfs_tree(g, v)
    d = Du[v]
    if flow is None:
        flow = [0] * m
        ok1, _ = _augment(g, flow, u, v)
        if ok1 is None:
            return None
        ok2, _ = _augment(g, flow, u, v)
        if ok2 is None:
            es, y = [], v
            while y != u:
                x, e = parU[y]
                es.append(e)
                y = x
            return dict(c=1, d=d, cp=d, cutpath=_mask(es, m), outcome="c=1", recorded=None, pairs=[])
        ok3, _ = _augment(g, flow[:], u, v)
        if ok3 is not None:
            return None
    paths = flow_paths(g, flow, u, v, mutation)
    res = dict(c=2, d=d, paths=paths, flow=flow)
    if paths is None:
        return res
    # -- D: the residual digraph of the flow along p_1 and p_2 ------------------------------------------
    trav = {}
    for vs, es in paths:
        for j, e in enumerate(es):
            trav[e] = (vs[j], vs[j + 1])
    out = [[] for _ in range(n)]
    for e, (a, b) in enumerate(g.edges):
        if e in trav:
            x, y = trav[e]
            out[y].append(x)
        else:
            out[a].append(b)
            out[b].append(a)
    scc = _scc(n, out)
    F, tail = [], {}
    for e, (x, y) in sorted(trav.items()):
        if scc[x] != scc[y]:
            F.append(e)
            tail[e] = x
    inF = [False] * m
    for e in F:
        inF[e] = True
    head = {e: g.other(e, tail[e]) for e in F}
    comp = [-1] * n
    npieces = 0
    for s in range(n):
        if comp[s] >= 0:
            continue
        comp[s] = npieces
        q = [s]
        for x in q:
            for y, e in g.adj[x]:
                if comp[y] < 0 and not inF[e]:
                    comp[y] = npieces
                    q.append(y)
        npieces += 1
    ent = [[] for _ in range(npieces)]
    lea = [[] for _ in range(npieces)]
    for e in F:
        ent[comp[head[e]]].append(e)
        lea[comp[tail[e]]].append(e)
    pu, pv = comp[u], comp[v]
    squares = [p for p in range(npieces) if p == pu or p == pv or len(ent[p]) == 2]
    res.update(F=F, tail=tail, comp=comp, squares=squares, scc=scc)
    for sq in squares:
        if (sq != pu and len(ent[sq]) != 2) or (sq != pv and len(lea[sq]) != 2):
            res["error"] = "a square does not have two entering and two leaving edges"
            return res
    # -- the loop -------------------------------------------------------------------------------------
    threshold = {"record-ge4": 4, "record-ge2": 2}.get(mutation, 3)
    recorded = None
    pairs = []
    found = None                                   # (edge list of R_x u p u R_y)
    for sq in squares:
        et = (u, u) if sq == pu else (head[ent[sq][0]], head[ent[sq][1]])
        lt = (v, v) if sq == pv else (tail[lea[sq][0]], tail[lea[sq][1]])
        for x, alpha in {(et[0], et[1]), (et[1], et[0])}:
            for y, beta in {(lt[0], lt[1]), (lt[1], lt[0])}:
                if x == y:
                    continue
                ell = d - Du[x] - Dv[y]
                if ell >= threshold and mutation != "never-record":
                    if recorded is None:
                        recorded = (x, y)
                    pairs.append((x, y))
                if alpha == beta or found is not None:
                    continue
                p_vertices = None
                if ell == 1:
                    if g.has_edge(x, y):
                        e = g.edge_id(x, y)
                        if not inF[e] and (mutation == "l1-nosep" or not _connected_without(g, inF, alpha, beta, (e,))):
                            p_vertices = [x, y]
                elif ell == 2 and mutation != "skip-l2":
                    qpath = _path_in_piece(g, inF, alpha, beta)
                    cand = []
                    for z in (x, y):
                        if z in qpath:
                            i = qpath.index(z)
                            if i > 0:
                                cand.append(qpath[i - 1])
                            if i + 1 < len(qpath):
                                cand.append(qpath[i + 1])
                    for w in dict.fromkeys(cand):
                        if w == x or w == y or comp[w] != sq or not (g.has_edge(x, w) and g.has_edge(w, y)):
                            continue
                        e1, e2 = g.edge_id(x, w), g.edge_id(w, y)
                        if inF[e1] or inF[e2]:
                            continue
                        if not _connected_without(g, inF, alpha, beta, (e1, e2)):
                            p_vertices = [x, w, y]
                            break
                if p_vertices is not None:
                    es = []
                    t = x
                    while t != u:                                  # R_x: a shortest u-x path of G
                        px, pe = parU[t]
                        es.append(pe)
                        t = px
                    for a, b in zip(p_vertices, p_vertices[1:]):
                        es.append(g.edge_id(a, b))
                    t = y
                    while t != v:                                  # R_y: a shortest y-v path of G
                        px, pe = parV[t]
                        es.append(pe)
                        t = px
                    found = es
                    if not exhaustive:
                        break
            if found is not None and not exhaustive:
                break
        if found is not None and not exhaustive:
            break
    res["pairs"] = pairs
    if found is not None:
        res.update(cp=d, cutpath=_mask(found, m), outcome="path", recorded=None)
        return res
    # nothing returned: d + 1 with a shortest path and a minimum cut (the edges leaving the set reachable from u in D)
    reach = [False] * n
    reach[u] = True
    q = [u]
    for x in q:
        for y in out[x]:
            if not reach[y]:
                reach[y] = True
                q.append(y)
    es = [] if mutation == "cut-missing" else [e for e, (a, b) in enumerate(g.edges) if reach[a] != reach[b]]
    y = v
    while y != u:
        x, e = parU[y]
        es.append(e)
        y = x
    res.update(cp=d + 1, cutpath=_mask(es, m), outcome="certificate" if recorded is not None else "value", recorded=recorded)
    return res
