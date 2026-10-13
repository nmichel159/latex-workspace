"""Exact routines for PATH-IN-MIN-CUT (does some minimum u-v cut contain a u-v path?).

Self-contained (no import of checks/).  Graphs are simple and undirected on the vertices 0..n-1; edges get ids
0..m-1 and are stored as pairs (a, b) with a < b.

Three independent ways to decide PATH-IN-MIN-CUT are implemented:
  1. min_cuts_branch:  all minimum u-v cuts by branching on the side of every vertex, pruned by a max-flow
                       between the vertex sets fixed so far (correct by definition of a minimum cut);
     then u-v connectivity in the graph (V, delta(A)) for each cut A.
  2. min_cuts_pq:      all minimum u-v cuts as the closed sets of the residual digraph of one maximum flow
                       (Picard-Queyranne); used only as a cross-check of 1.
  3. cp_equals_c_paths: the definition cp = min over u-v paths P of |P| + c_{G - P}(u,v), restricted to paths
                       whose edges each lie in some minimum cut (edge e lies in a minimum cut iff
                       c_{G-e}(u,v) = c(u,v) - 1); cp = c iff some such path P has |P| + c_{G-P}(u,v) = c.
  4. min_cuts_numpy:   all minimum cuts by enumerating all vertex sets (n <= 24), for the smallest instances.
"""

from collections import deque
import itertools


class UG:
    __slots__ = ("n", "edges", "m", "adj", "eid")

    def __init__(self, n, edges):
        es = sorted({(min(a, b), max(a, b)) for a, b in edges if a != b})
        self.n = n
        self.edges = es
        self.m = len(es)
        self.adj = [[] for _ in range(n)]
        self.eid = {}
        for i, (a, b) in enumerate(es):
            self.adj[a].append((b, i))
            self.adj[b].append((a, i))
            self.eid[(a, b)] = i

    def edge_id(self, a, b):
        return self.eid[(a, b) if a < b else (b, a)]


def maxflow_sets(g, S, T, removed=(), limit=None, want_flow=False):
    """Unit-capacity undirected maximum flow from the vertex set S to the disjoint vertex set T (edges with an end
    in S or T have capacity one as usual; S and T act as a super-source and a super-sink).
    Returns (value, reach, flow): reach = vertices reachable from S in the final residual graph (None if the
    search stopped at `limit`), flow[e] = +1 / -1 / 0 (from the smaller to the larger end / back / none)."""
    n = g.n
    inT = [False] * n
    for x in T:
        inT[x] = True
    rem = set(removed)
    flow = [0] * g.m
    edges = g.edges
    value = 0
    while True:
        if limit is not None and value >= limit:
            return value, None, (flow if want_flow else None)
        par = [None] * n
        q = deque()
        for s in S:
            par[s] = (-1, -1)
            q.append(s)
        hit = None
        while q and hit is None:
            x = q.popleft()
            for y, e in g.adj[x]:
                if par[y] is not None or e in rem:
                    continue
                a = edges[e][0]
                cap = (1 - flow[e]) if x == a else (1 + flow[e])
                if cap <= 0:
                    continue
                par[y] = (x, e)
                if inT[y]:
                    hit = y
                    break
                q.append(y)
        if hit is None:
            reach = {x for x in range(n) if par[x] is not None}
            return value, reach, (flow if want_flow else None)
        y = hit
        while par[y][0] != -1:
            x, e = par[y]
            flow[e] += 1 if x == edges[e][0] else -1
            y = x
        value += 1


def cut_value(g, u, v, removed=(), limit=None):
    return maxflow_sets(g, [u], [v], removed, limit)[0]


def boundary(g, A):
    return [e for e, (a, b) in enumerate(g.edges) if (a in A) != (b in A)]


def bfs_dist(g, s, allowed=None):
    """Distances from s; with `allowed` (a set of edge ids) only those edges are used."""
    dist = [None] * g.n
    dist[s] = 0
    q = deque([s])
    while q:
        x = q.popleft()
        for y, e in g.adj[x]:
            if dist[y] is None and (allowed is None or e in allowed):
                dist[y] = dist[x] + 1
                q.append(y)
    return dist


def min_cuts_branch(g, u, v, order=None):
    """(c, list of frozensets A): all minimum u-v cuts delta(A), u in A, v not in A, by branching on the side of
    every vertex in `order` (default: by index) and pruning when the minimum cut between the vertices fixed on
    the u side and those fixed on the v side exceeds c."""
    c = cut_value(g, u, v)
    if order is None:
        order = [x for x in range(g.n) if x != u and x != v]
    out = []

    def rec(i, S, T):
        val = maxflow_sets(g, S, T, limit=c + 1)[0]
        if val > c:
            return
        if i == len(order):
            out.append(frozenset(S))
            return
        w = order[i]
        S.append(w)
        rec(i + 1, S, T)
        S.pop()
        T.append(w)
        rec(i + 1, S, T)
        T.pop()

    rec(0, [u], [v])
    return c, out


def residual_arcs(g, flow):
    """Arcs of the residual digraph of a unit-capacity undirected flow: an edge without flow gives both arcs, an
    edge with flow from x to y gives only the arc (y, x)."""
    out = [[] for _ in range(g.n)]
    for e, (a, b) in enumerate(g.edges):
        f = flow[e]
        if f == 0:
            out[a].append(b)
            out[b].append(a)
        elif f > 0:            # flow a -> b
            out[b].append(a)
        else:                  # flow b -> a
            out[a].append(b)
    return out


def min_cuts_pq(g, u, v, max_free_classes=22):
    """(c, list of frozensets A): all minimum u-v cuts as the closed sets of the residual digraph that contain u
    and not v (Picard-Queyranne).  Enumerates subsets of the free strongly connected classes (at most
    `max_free_classes` of them) and keeps the closed ones."""
    c, _, flow = maxflow_sets(g, [u], [v], want_flow=True)
    out = residual_arcs(g, flow)
    n = g.n
    inn = [[] for _ in range(n)]
    for x in range(n):
        for y in out[x]:
            inn[y].append(x)

    def reach(starts, arcs):
        seen = set(starts)
        q = deque(starts)
        while q:
            x = q.popleft()
            for y in arcs[x]:
                if y not in seen:
                    seen.add(y)
                    q.append(y)
        return seen

    forced_in = reach([u], out)
    forced_out = reach([v], inn)
    assert not (forced_in & forced_out)
    free = [x for x in range(n) if x not in forced_in and x not in forced_out]
    # strongly connected classes of the free vertices: x ~ y iff each reaches the other within the free part
    fr = set(free)
    sub = [[y for y in out[x] if y in fr] for x in range(n)]
    classes = []
    assigned = {}
    for x in free:
        if x in assigned:
            continue
        fw = reach([x], sub)
        bw = reach([x], [[y for y in inn[z] if y in fr] for z in range(n)])
        cls = sorted(fw & bw)
        for y in cls:
            assigned[y] = len(classes)
        classes.append(cls)
    k = len(classes)
    if k > max_free_classes:
        raise ValueError("too many free classes: %d" % k)
    cuts = []
    for mask in range(1 << k):
        A = set(forced_in)
        for i in range(k):
            if (mask >> i) & 1:
                A.update(classes[i])
        closed = all(y in A for x in A for y in out[x])
        if closed:
            cuts.append(frozenset(A))
    return c, cuts


def cut_graph_path(g, A, u, v):
    """Shortest u-v path (vertex list) in the graph (V, delta(A)), or None."""
    allowed = set(boundary(g, A))
    par = {u: None}
    q = deque([u])
    while q:
        x = q.popleft()
        if x == v:
            break
        for y, e in g.adj[x]:
            if e in allowed and y not in par:
                par[y] = x
                q.append(y)
    if v not in par:
        return None
    path = [v]
    while par[path[-1]] is not None:
        path.append(par[path[-1]])
    return path[::-1]


def path_in_min_cut(g, u, v, cuts):
    """(answer, shortest length over all cuts or None, number of cuts containing a u-v path)."""
    best = None
    count = 0
    for A in cuts:
        p = cut_graph_path(g, A, u, v)
        if p is not None:
            count += 1
            if best is None or len(p) - 1 < best:
                best = len(p) - 1
    return best is not None, best, count


def cp_equals_c_paths(g, u, v, max_paths=2_000_000, alternating=True):
    """Decide cp(u,v) = c(u,v) from the definition, independently of the cut enumerations.

    cp = c iff some u-v path P has |P| + c_{G-P}(u,v) = c (then P plus a minimum cut of G - P is a minimum cut
    containing P).  Such a P lies in a minimum cut delta(A), so (i) every edge of P lies in some minimum cut, i.e.
    c_{G-e}(u,v) = c - 1, and it carries flow in every maximum flow f; (ii) with alternating=True: P alternates
    between A and V - A and every edge of delta(A) carries one unit of f from A to V - A (the net flow across
    delta(A) is c = |delta(A)|), so the i-th edge x_i x_{i+1} of P (i = 0, 1, ...) carries flow from x_i to
    x_{i+1} for even i and from x_{i+1} to x_i for odd i.  All simple u-v paths with at most c edges obeying
    (i) [and (ii)] are enumerated and tested.
    Returns (answer, c, number of candidate edges, number of paths tried, lengths of the successful paths)."""
    c, _, flow = maxflow_sets(g, [u], [v], want_flow=True)
    star = set()
    for e in range(g.m):
        if flow[e] != 0 and cut_value(g, u, v, removed=(e,), limit=c) == c - 1:
            star.add(e)
    lengths = set()
    tried = 0
    visited = [False] * g.n
    visited[u] = True
    es = []
    edges = g.edges

    def forward(x, e):
        """flow on e leaves x"""
        a = edges[e][0]
        return (flow[e] > 0) == (x == a)

    def rec(x):
        nonlocal tried
        if x == v:
            tried += 1
            if tried > max_paths:
                raise RuntimeError("too many paths")
            k = len(es)
            if cut_value(g, u, v, removed=es, limit=c - k + 1) == c - k:
                lengths.add(k)
            return
        if len(es) >= c:
            return
        want_out = (len(es) % 2 == 0)
        for y, e in g.adj[x]:
            if e in star and not visited[y]:
                if alternating and forward(x, e) != want_out:
                    continue
                visited[y] = True
                es.append(e)
                rec(y)
                es.pop()
                visited[y] = False

    rec(u)
    return bool(lengths), c, len(star), tried, sorted(lengths)


def min_cuts_numpy(g, u, v):
    """(c, list of frozensets A) by enumerating all 2^(n-2) vertex sets (n <= 24)."""
    import numpy as np
    others = [x for x in range(g.n) if x != u and x != v]
    k = len(others)
    assert k <= 22
    idx = np.arange(1 << k, dtype=np.int64)
    side = {u: np.ones(1 << k, dtype=bool), v: np.zeros(1 << k, dtype=bool)}
    for i, x in enumerate(others):
        side[x] = ((idx >> i) & 1).astype(bool)
    size = np.zeros(1 << k, dtype=np.int32)
    for a, b in g.edges:
        size += (side[a] ^ side[b])
    c = int(size.min())
    cuts = []
    for t in np.nonzero(size == c)[0]:
        A = {u}
        for i, x in enumerate(others):
            if (int(t) >> i) & 1:
                A.add(x)
        cuts.append(frozenset(A))
    return c, cuts


def diameter_and_classes(g, thresholds=(2, 3)):
    """(diameter, {t: number of pairs (x, y) with d(x,y) > t and c(x,y) > t}).

    A graph lies in DC iff the count for t = 2 is zero ("d <= 2 or c <= 2" for all pairs); the count for t = 3
    with distance threshold 2 is reported under key ('d2', 3): pairs with d > 2 and c > 3."""
    D = [bfs_dist(g, s) for s in range(g.n)]
    diam = max(max(d for d in row if d is not None) for row in D)
    res = {}
    far = [(x, y) for x in range(g.n) for y in range(x + 1, g.n) if D[x][y] is None or D[x][y] > 2]
    lam = {}
    for x, y in far:
        lam[(x, y)] = cut_value(g, x, y, limit=4)
    res["d>2,c>2 (not DC)"] = sum(1 for p in far if lam[p] > 2)
    res["d>2,c>3 (not 'd<=2 or c<=3')"] = sum(1 for p in far if lam[p] > 3)
    res["d>3,c>2 (not 'd<=3 or c<=2')"] = sum(1 for (x, y) in far if (D[x][y] is None or D[x][y] > 3) and lam[(x, y)] > 2)
    example = next((p for p in far if lam[p] > 2), None)
    return diam, res, example
