"""Shared library of the checks of article 2 (Min Cut-Path on the class DC).

Everything here is brute force and deliberately independent of algorithm.py.

Graphs are simple, undirected, connected, on the vertices 0..n-1; edges have ids 0..m-1 and are stored as
pairs (a, b) with a < b.  Edge sets are Python ints used as bit masks (bit e = edge e).

Contents
  Gr                  graph with adjacency lists and an edge-id table
  bfs, connected, components, edge_conn / maxflow (unit capacities, augmenting paths)
  simple_paths        all simple u-v paths, optionally of bounded length
  cp_brute            cp(u,v) = min over simple paths P of |P| + c_{G-P}(u,v)   (an optimal cut-path is returned)
  cp_subsets          cp(u,v) from article 1: min over P and vertex sets A of |P| + |boundary(A) - P|  (n <= 8)
  cp_definition       cp(u,v) from the literal definition (all edge sets of growing size)
  in_dc               membership in the class DC
  min_cuts2, Decomp   brute-force F, orientation, pieces, squares, links, terminals, general paths
  atlas_pairs         all connected graphs with 2..7 vertices (networkx atlas) as (n, edge list)
"""

import itertools
import os
import random
from collections import defaultdict

SCRATCH = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "tmp", "clanok-2-checks"))


class TooMany(Exception):
    """Raised when an enumeration exceeds its limit."""


# ---------------------------------------------------------------------------------------------------------
# graphs and basic searches
# ---------------------------------------------------------------------------------------------------------

class Gr:
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

    def has_edge(self, a, b):
        return ((a, b) if a < b else (b, a)) in self.eid

    def other(self, e, x):
        a, b = self.edges[e]
        return b if x == a else a

    def full(self):
        return (1 << self.m) - 1


def mask_of(es):
    m = 0
    for e in es:
        m |= 1 << e
    return m


def bits(mask):
    res = []
    while mask:
        low = mask & -mask
        res.append(low.bit_length() - 1)
        mask ^= low
    return res


def popcount(x):
    return x.bit_count()


def bfs(g, s, removed=0):
    dist = [None] * g.n
    dist[s] = 0
    queue = [s]
    for x in queue:
        dx = dist[x] + 1
        for y, e in g.adj[x]:
            if dist[y] is None and not (removed >> e) & 1:
                dist[y] = dx
                queue.append(y)
    return dist


def connected(g, u, v, removed=0):
    if u == v:
        return True
    seen = [False] * g.n
    seen[u] = True
    queue = [u]
    for x in queue:
        for y, e in g.adj[x]:
            if not seen[y] and not (removed >> e) & 1:
                if y == v:
                    return True
                seen[y] = True
                queue.append(y)
    return False


def component_mask(g, u, removed=0):
    seen = 1 << u
    queue = [u]
    for x in queue:
        for y, e in g.adj[x]:
            if not (seen >> y) & 1 and not (removed >> e) & 1:
                seen |= 1 << y
                queue.append(y)
    return seen


def components(g, removed=0):
    comp = [-1] * g.n
    count = 0
    for s in range(g.n):
        if comp[s] >= 0:
            continue
        comp[s] = count
        queue = [s]
        for x in queue:
            for y, e in g.adj[x]:
                if comp[y] < 0 and not (removed >> e) & 1:
                    comp[y] = count
                    queue.append(y)
        count += 1
    return comp, count


def dist_matrix(g):
    return [bfs(g, s) for s in range(g.n)]


def is_connected(g):
    return all(d is not None for d in bfs(g, 0))


def maxflow(g, u, v, removed=0, limit=None):
    """Unit-capacity undirected max flow by augmenting paths.

    Returns (value, flow, par).  flow[e] = +1 if the flow runs from the smaller to the larger end of edge e,
    -1 for the other direction.  `par` is the search tree of the last (failed) search, so that
    {x : par[x] is not None} is the set reachable from u in the residual graph (a minimum cut); it is None
    if the search stopped because `limit` was reached."""
    flow = [0] * g.m
    value = 0
    edges = g.edges
    while True:
        if limit is not None and value >= limit:
            return value, flow, None
        par = [None] * g.n
        par[u] = (-1, -1)
        queue = [u]
        for x in queue:
            if par[v] is not None:
                break
            for y, e in g.adj[x]:
                if par[y] is None and not (removed >> e) & 1:
                    f = flow[e]
                    cap = (1 - f) if x == edges[e][0] else (1 + f)
                    if cap > 0:
                        par[y] = (x, e)
                        queue.append(y)
        if par[v] is None:
            return value, flow, par
        y = v
        while y != u:
            x, e = par[y]
            flow[e] += 1 if x == edges[e][0] else -1
            y = x
        value += 1


def edge_conn(g, u, v, removed=0, limit=None):
    return maxflow(g, u, v, removed, limit)[0]


def min_cut_mask(g, u, v, removed=0):
    """(value, edge mask of a minimum u-v cut of G - removed, vertex set A of the u side)."""
    value, flow, par = maxflow(g, u, v, removed)
    A = 0
    for x in range(g.n):
        if par[x] is not None:
            A |= 1 << x
    cut = 0
    for e, (a, b) in enumerate(g.edges):
        if (removed >> e) & 1:
            continue
        if ((A >> a) ^ (A >> b)) & 1:
            cut |= 1 << e
    return value, cut, A


def two_disjoint_paths(g, u, v):
    """Two edge-disjoint u-v paths (as vertex lists) from a flow of value 2; None if c(u,v) < 2."""
    value, flow, _ = maxflow(g, u, v, limit=2)
    if value < 2:
        return None
    out = defaultdict(list)
    for e, f in enumerate(flow):
        if f:
            a, b = g.edges[e]
            out[a if f > 0 else b].append(b if f > 0 else a)
    paths = []
    for _ in range(2):
        path = [u]
        x = u
        while x != v:
            y = out[x].pop()
            path.append(y)
            x = y
        paths.append(path)
    return paths


def simple_paths(g, u, v, maxlen=None, removed=0, limit=None):
    """All simple u-v paths as (vertex tuple, edge tuple); with maxlen only those of at most maxlen edges."""
    dv = bfs(g, v, removed) if maxlen is not None else None
    res = []
    visited = [False] * g.n
    vs = [u]
    es = []
    visited[u] = True

    def rec(x):
        if x == v:
            res.append((tuple(vs), tuple(es)))
            if limit is not None and len(res) > limit:
                raise TooMany()
            return
        for y, e in g.adj[x]:
            if visited[y] or (removed >> e) & 1:
                continue
            if dv is not None and (dv[y] is None or len(es) + 1 + dv[y] > maxlen):
                continue
            visited[y] = True
            vs.append(y)
            es.append(e)
            rec(y)
            vs.pop()
            es.pop()
            visited[y] = False

    rec(u)
    return res


# ---------------------------------------------------------------------------------------------------------
# cp(u,v): three independent computations
# ---------------------------------------------------------------------------------------------------------

def is_cutpath(g, u, v, S):
    """S (edge mask) contains a u-v path and a u-v cut."""
    full = g.full()
    return connected(g, u, v, removed=full ^ S) and not connected(g, u, v, removed=S)


def shortest_path_edges(g, u, v, removed=0):
    dist = [None] * g.n
    par = [None] * g.n
    dist[u] = 0
    queue = [u]
    for x in queue:
        for y, e in g.adj[x]:
            if dist[y] is None and not (removed >> e) & 1:
                dist[y] = dist[x] + 1
                par[y] = (x, e)
                queue.append(y)
    if dist[v] is None:
        return None
    es = []
    y = v
    while y != u:
        x, e = par[y]
        es.append(e)
        y = x
    es.reverse()
    return es


def cp_brute(g, u, v, path_limit=None):
    """(cp, mask of an optimal cut-path).

    cp = min over simple u-v paths P of |P| + c_{G-P}(u,v) (the cheapest cut inside G - P).  Only paths with
    at most UB edges are enumerated, where UB = |P0 u C0| is the size of an explicit cut-path (a shortest path
    and a minimum cut), because an optimal cut-path with |S| <= UB contains a path of length <= UB."""
    P0 = shortest_path_edges(g, u, v)
    d = len(P0)
    c, C0, _ = min_cut_mask(g, u, v)
    S0 = mask_of(P0) | C0
    best = popcount(S0)
    best_set = S0
    lower = max(c, d)
    if best == lower:
        return best, best_set
    for vs, es in simple_paths(g, u, v, maxlen=best, limit=path_limit):
        size = len(es)
        if size >= best:
            continue
        P = mask_of(es)
        value, flow, par = maxflow(g, u, v, removed=P, limit=best - size)
        if par is None:          # value reached the limit: size + value >= best
            continue
        # a cheaper cut-path: P together with a minimum cut of G - P
        total = size + value
        if total < best:
            A = 0
            for x in range(g.n):
                if par[x] is not None:
                    A |= 1 << x
            cut = 0
            for e, (a, b) in enumerate(g.edges):
                if not (P >> e) & 1 and ((A >> a) ^ (A >> b)) & 1:
                    cut |= 1 << e
            best = total
            best_set = P | cut
            if best == lower:
                break
    return best, best_set


def cp_subsets(g, u, v):
    """Article 1's computation (small n): min over all simple paths P and vertex sets A of |P| + |bd(A) - P|."""
    n = g.n
    bnd = {}
    for A in range(1 << n):
        if (A >> u) & 1 and not (A >> v) & 1:
            mask = 0
            for e, (a, b) in enumerate(g.edges):
                if ((A >> a) ^ (A >> b)) & 1:
                    mask |= 1 << e
            bnd[A] = mask
    best = g.m + 1
    for vs, es in simple_paths(g, u, v):
        size = len(es)
        if size >= best:
            continue
        P = mask_of(es)
        extra = min(popcount(b & ~P) for b in bnd.values())
        best = min(best, size + extra)
    return best


def cp_definition(g, u, v):
    """Definition read literally: the smallest edge set S such that u, v are connected in (V, S) and
    disconnected in G - S (all subsets by growing size)."""
    full = g.full()
    for size in range(g.m + 1):
        for combo in itertools.combinations(range(g.m), size):
            S = mask_of(combo)
            if connected(g, u, v, removed=full ^ S) and not connected(g, u, v, removed=S):
                return size
    return None


def min_cuts_by_sets(g, u, v):
    """(c, sorted list of the edge masks of all minimum u-v cuts) by enumerating vertex sets (n <= ~14)."""
    others = [x for x in range(g.n) if x != u and x != v]
    best = None
    cuts = set()
    for r in range(len(others) + 1):
        for sub in itertools.combinations(others, r):
            A = 1 << u
            for x in sub:
                A |= 1 << x
            mask = 0
            for e, (a, b) in enumerate(g.edges):
                if ((A >> a) ^ (A >> b)) & 1:
                    mask |= 1 << e
            k = popcount(mask)
            if best is None or k < best:
                best = k
                cuts = {mask}
            elif k == best:
                cuts.add(mask)
    return best, sorted(cuts)


def in_dc(g, D=None):
    """(True, None) if every two distinct vertices have d <= 2 or c <= 2, else (False, (x, y))."""
    if D is None:
        D = dist_matrix(g)
    for x in range(g.n):
        for y in range(x + 1, g.n):
            if D[x][y] > 2 and edge_conn(g, x, y, limit=3) >= 3:
                return False, (x, y)
    return True, None


def bridges(g):
    res = []
    for e in range(g.m):
        a, b = g.edges[e]
        if not connected(g, a, b, removed=1 << e):
            res.append(e)
    return res


def induced(g, vertices, removed=0):
    """Subgraph on the given vertices (relabelled in the given order) without the edges in `removed`;
    returns (Gr, relabel dict old -> new, edge id map new -> old)."""
    idx = {x: i for i, x in enumerate(vertices)}
    es = []
    for e, (a, b) in enumerate(g.edges):
        if (removed >> e) & 1:
            continue
        if a in idx and b in idx:
            es.append((idx[a], idx[b]))
    h = Gr(len(vertices), es)
    emap = {new: g.edge_id(vertices[a], vertices[b]) for new, (a, b) in enumerate(h.edges)}
    return h, idx, emap


# ---------------------------------------------------------------------------------------------------------
# minimum cuts of a pair with c(u,v) = 2, orientation, pieces, squares
# ---------------------------------------------------------------------------------------------------------

def min_cuts2(g, u, v, fast=False):
    """All minimum u-v cuts for c(u,v) = 2 as (e, f, A) with A the vertex mask of the component of u in
    G - {e, f}.  Brute force over all pairs of edges; with fast=True only over the pairs (e on p1, f on p2)
    for two edge-disjoint paths p1, p2 (a 2-edge cut meets each of the two paths, hence has one edge on each)."""
    cuts = []
    if fast:
        p1, p2 = two_disjoint_paths(g, u, v)
        E1 = [g.edge_id(a, b) for a, b in zip(p1, p1[1:])]
        E2 = [g.edge_id(a, b) for a, b in zip(p2, p2[1:])]
        for e in E1:
            for f in E2:
                rem = (1 << e) | (1 << f)
                if not connected(g, u, v, removed=rem):
                    cuts.append((min(e, f), max(e, f), component_mask(g, u, rem)))
        return cuts
    for e in range(g.m):
        for f in range(e + 1, g.m):
            rem = (1 << e) | (1 << f)
            if not connected(g, u, v, removed=rem):
                cuts.append((e, f, component_mask(g, u, rem)))
    return cuts


def brute_orientation(g, cuts):
    """F and the tail of every edge of F computed from the cuts.  Returns (F, tail, problems) where
    `problems` lists the edges for which the cuts disagree on the tail (or an end pattern is impossible)."""
    tails = defaultdict(set)
    problems = []
    for e, f, A in cuts:
        for x in (e, f):
            a, b = g.edges[x]
            ina, inb = (A >> a) & 1, (A >> b) & 1
            if ina == inb:
                problems.append((x, "both or no end of the edge in the u-side"))
                continue
            tails[x].add(a if ina else b)
    F = sorted(tails)
    tail = {}
    for x in F:
        if len(tails[x]) != 1:
            problems.append((x, "two different tails %s" % sorted(tails[x])))
        tail[x] = min(tails[x])
    return F, tail, problems


class Decomp:
    """Pieces, squares, links, terminals and general paths for given F and tails."""

    def __init__(self, g, u, v, F, tail):
        self.g, self.u, self.v = g, u, v
        self.F = sorted(F)
        self.Fmask = mask_of(self.F)
        self.tail = {e: tail[e] for e in self.F}
        self.head = {e: g.other(e, self.tail[e]) for e in self.F}
        self.comp, self.np = components(g, self.Fmask)
        self.pieces = [[] for _ in range(self.np)]
        for x in range(g.n):
            self.pieces[self.comp[x]].append(x)
        self.ent = [[] for _ in range(self.np)]
        self.lea = [[] for _ in range(self.np)]
        for e in self.F:
            self.ent[self.comp[self.head[e]]].append(e)
            self.lea[self.comp[self.tail[e]]].append(e)
        self.pu, self.pv = self.comp[u], self.comp[v]
        self.is_square = [(p == self.pu or p == self.pv or len(self.ent[p]) == 2) for p in range(self.np)]
        self.inside_F = [e for e in self.F if self.comp[g.edges[e][0]] == self.comp[g.edges[e][1]]]
        self._order = "unset"

    # -- order of the squares -------------------------------------------------------------------------
    def piece_reach(self):
        succ = [set() for _ in range(self.np)]
        for e in self.F:
            succ[self.comp[self.tail[e]]].add(self.comp[self.head[e]])
        reach = []
        for p in range(self.np):
            seen = {p}
            stack = [p]
            while stack:
                x = stack.pop()
                for y in succ[x]:
                    if y not in seen:
                        seen.add(y)
                        stack.append(y)
            seen.discard(p)
            reach.append(seen)
        return reach

    def square_order(self):
        """Squares from u to v: ordered by reachability in the digraph of pieces; None if that is not a
        strict total order on the squares."""
        if self._order != "unset":
            return self._order
        reach = self.piece_reach()
        squares = [p for p in range(self.np) if self.is_square[p]]
        ok = True
        for a, b in itertools.combinations(squares, 2):
            if (b in reach[a]) == (a in reach[b]):
                ok = False
        for a in squares:
            if a in reach[a]:
                ok = False
        if ok:
            squares.sort(key=lambda p: -len(reach[p]))
            ok = squares and squares[0] == self.pu and squares[-1] == self.pv
        self._order = squares if ok else None
        return self._order

    # -- terminals ----------------------------------------------------------------------------------
    def entering_terminals(self, p):
        if p == self.pu:
            return (self.u, self.u)
        return tuple(self.head[e] for e in self.ent[p])

    def leaving_terminals(self, p):
        if p == self.pv:
            return (self.v, self.v)
        return tuple(self.tail[e] for e in self.lea[p])

    def terminals(self, p):
        return set(self.entering_terminals(p)) | set(self.leaving_terminals(p))

    # -- general paths ------------------------------------------------------------------------------
    def follow(self, e):
        """The sequence e_0, L_1, e_1, ..., L_r, e_r that starts with the F-edge e: (edges, links, end square)
        or None if the sequence is malformed."""
        edges = [e]
        links = []
        q = self.comp[self.head[e]]
        while not self.is_square[q]:
            if len(self.lea[q]) != 1 or len(edges) > self.np + 1:
                return None
            links.append(q)
            e2 = self.lea[q][0]
            edges.append(e2)
            q = self.comp[self.head[e2]]
        return edges, links, q

    def piece_paths(self, x, y, limit=None):
        """All simple x-y paths inside the piece of x (vertex tuple, edge tuple)."""
        if x == y:
            return [((x,), ())]
        return simple_paths(self.g, x, y, removed=self.Fmask, limit=limit)

    def sep_in_piece(self, a, b, Rmask):
        """a and b lie in different components of (piece) - E(R)."""
        return not connected(self.g, a, b, removed=self.Fmask | Rmask)

    def vec_arcs(self, x):
        """Out-neighbours of x in the digraph G-vector (F-edges only from tail to head): (y, e)."""
        for y, e in self.g.adj[x]:
            if (self.Fmask >> e) & 1 and self.tail[e] != x:
                continue
            yield y, e

    def vec_dist(self, source, reverse=False):
        n = self.g.n
        if reverse:
            radj = [[] for _ in range(n)]
            for x in range(n):
                for y, e in self.vec_arcs(x):
                    radj[y].append(x)
        dist = [None] * n
        dist[source] = 0
        queue = [source]
        for x in queue:
            nxt = radj[x] if reverse else [y for y, e in self.vec_arcs(x)]
            for y in nxt:
                if dist[y] is None:
                    dist[y] = dist[x] + 1
                    queue.append(y)
        return dist

    def vec_paths(self, limit=None):
        """All simple directed u-v paths of G-vector (as vertex tuples)."""
        res = []
        g = self.g
        visited = [False] * g.n
        vs = [self.u]
        visited[self.u] = True

        def rec(x):
            if x == self.v:
                res.append(tuple(vs))
                if limit is not None and len(res) > limit:
                    raise TooMany()
                return
            for y, e in self.vec_arcs(x):
                if not visited[y]:
                    visited[y] = True
                    vs.append(y)
                    rec(y)
                    vs.pop()
                    visited[y] = False

        rec(self.u)
        return res


def brute_decomp(g, u, v, fast=False):
    """Decomposition from brute-force minimum cuts: returns (Decomp, cuts, problems) for c(u,v) = 2."""
    cuts = min_cuts2(g, u, v, fast=fast)
    F, tail, problems = brute_orientation(g, cuts)
    return Decomp(g, u, v, F, tail), cuts, problems


# ---------------------------------------------------------------------------------------------------------
# graph lists
# ---------------------------------------------------------------------------------------------------------

def atlas_pairs(nmin=2, nmax=7, connected_only=True):
    """All (n, edge list) of the networkx atlas with nmin..nmax vertices, in the atlas order
    (by vertices, then edges)."""
    import networkx as nx
    from networkx.generators.atlas import graph_atlas_g
    out = []
    for G in graph_atlas_g():
        n = G.number_of_nodes()
        if n < nmin or n > nmax:
            continue
        if connected_only and not nx.is_connected(G):
            continue
        out.append((n, sorted((min(a, b), max(a, b)) for a, b in G.edges())))
    return out


def _invariant(n, edges):
    adj = [set() for _ in range(n)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    deg = [len(s) for s in adj]
    tri = [sum(1 for y in adj[x] for z in adj[x] if y < z and z in adj[y]) for x in range(n)]
    return tuple(sorted((deg[x], tri[x], tuple(sorted(deg[y] for y in adj[x]))) for x in range(n)))


def extend_graphs(prev, n_prev):
    """All connected graphs on n_prev + 1 vertices up to isomorphism, from all connected graphs on n_prev
    vertices: every connected graph has a vertex whose removal leaves it connected, so it is a connected
    graph plus a new vertex joined to a non-empty set of old vertices."""
    import networkx as nx
    buckets = {}
    out = []
    for _, es in prev:
        for S in range(1, 1 << n_prev):
            edges = list(es) + [(i, n_prev) for i in range(n_prev) if (S >> i) & 1]
            key = _invariant(n_prev + 1, edges)
            lst = buckets.setdefault(key, [])
            G = None
            dup = False
            for H in lst:
                if G is None:
                    G = nx.Graph(edges)
                if nx.is_isomorphic(G, H):
                    dup = True
                    break
            if not dup:
                if G is None:
                    G = nx.Graph(edges)
                lst.append(G)
                out.append((n_prev + 1, sorted((min(a, b), max(a, b)) for a, b in edges)))
    out.sort(key=lambda t: (len(t[1]), t[1]))
    return out


def connected_graphs(n, cache_dir=None):
    """All connected graphs on n vertices up to isomorphism as (n, edge list).  n <= 7: the atlas; n >= 8 by
    vertex extension, cached as JSON in cache_dir (the count is checked against the known numbers)."""
    import json
    known = {2: 1, 3: 2, 4: 6, 5: 21, 6: 112, 7: 853, 8: 11117, 9: 261080}
    if n <= 7:
        return atlas_pairs(n, n)
    cache = os.path.join(cache_dir, "graphs%d.json" % n) if cache_dir else None
    if cache and os.path.exists(cache):
        with open(cache) as f:
            return [(n, [tuple(e) for e in es]) for es in json.load(f)]
    res = extend_graphs(connected_graphs(n - 1, cache_dir), n - 1)
    assert len(res) == known[n], (n, len(res))
    if cache:
        os.makedirs(cache_dir, exist_ok=True)
        with open(cache, "w") as f:
            json.dump([es for _, es in res], f)
    return res


def random_connected(rng, n, p):
    while True:
        es = [(a, b) for a in range(n) for b in range(a + 1, n) if rng.random() < p]
        g = Gr(n, es)
        if is_connected(g):
            return g


def fmt_edges(edges):
    return " ".join("%d-%d" % (a, b) for a, b in edges)
