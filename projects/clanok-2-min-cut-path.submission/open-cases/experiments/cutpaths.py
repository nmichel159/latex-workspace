"""Exact routines for the open case of the class DC: u-v paths inside minimum u-v cuts.

Graphs are mcp.Gr objects (simple, undirected, vertices 0..n-1); vertex sets are bit masks.

Method (Picard-Queyranne, flow view).  Fix one maximum u-v flow f (unit capacities, an undirected edge is a pair of
opposite arcs of capacity one; mcp.maxflow keeps flow[e] in {-1, 0, +1}).  The residual digraph R has, for an edge
{a, b}, both arcs a->b and b->a if f(e) = 0, and only the arc b->a if one unit runs from a to b.  A vertex set A with
u in A, v not in A spans a minimum cut delta(A) iff A is closed in R (no arc of R leaves A), and then every edge
of delta(A) carries one unit of f from A to V - A.  Hence a u-v path x_0 = u, x_1, ..., x_k = v lies inside some
minimum cut iff
  (a) the flow runs x_{2i} -> x_{2i+1} and x_{2i+2} -> x_{2i+1} on its edges (directions alternate), and
  (b) the R-closure of the even-indexed vertices contains no odd-indexed vertex
(the smallest closed set containing the even vertices is their R-closure; closure is monotone).
Both conditions are inherited by prefixes, so a depth-first search over alternating flow paths with this pruning
enumerates exactly the u-v paths that lie inside some minimum cut ("cut paths" below).

Validated against brute force over all vertex sets (validate.py).
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CHECKS = os.path.normpath(os.path.join(HERE, "..", "..", "checks"))
if CHECKS not in sys.path:
    sys.path.insert(0, CHECKS)

import mcp  # noqa: E402  (read-only use)
from mcp import Gr, bfs, maxflow, edge_conn  # noqa: E402,F401


class Limit(Exception):
    pass


def residual_reach(g, flow):
    """reach[x] = bit mask of the vertices reachable from x in the residual digraph (x included)."""
    n = g.n
    out = [0] * n
    for e, (a, b) in enumerate(g.edges):
        f = flow[e]
        if f == 0:
            out[a] |= 1 << b
            out[b] |= 1 << a
        elif f > 0:          # a -> b carries flow: only b -> a is residual
            out[b] |= 1 << a
        else:
            out[a] |= 1 << b
    reach = [0] * n
    for s in range(n):
        seen = 1 << s
        stack = [s]
        while stack:
            x = stack.pop()
            new = out[x] & ~seen
            seen |= new
            while new:
                low = new & -new
                stack.append(low.bit_length() - 1)
                new ^= low
        reach[s] = seen
    return reach


def flow_out(g, flow):
    """fo[x] = list of y such that one unit of flow runs x -> y; fi[y] = list of x with x -> y."""
    fo = [[] for _ in range(g.n)]
    fi = [[] for _ in range(g.n)]
    for e, (a, b) in enumerate(g.edges):
        f = flow[e]
        if f > 0:
            fo[a].append(b)
            fi[b].append(a)
        elif f < 0:
            fo[b].append(a)
            fi[a].append(b)
    return fo, fi


class PairInfo:
    """c(u,v), one maximum flow, residual reach masks, and the cut paths of (u, v)."""

    def __init__(self, g, u, v):
        self.g, self.u, self.v = g, u, v
        self.c, self.flow, _ = maxflow(g, u, v)
        self.reach = residual_reach(g, self.flow)
        self.fo, self.fi = flow_out(g, self.flow)

    def cut_paths(self, maxlen=None, limit=None, first=False):
        """All u-v paths (vertex tuples) that lie inside some minimum u-v cut, of length <= maxlen.
        With first=True stop at the first one found (returns a list of at most one path)."""
        u, v = self.u, self.v
        reach, fo, fi = self.reach, self.fo, self.fi
        res = []
        path = [u]

        def rec(x, parity, clos, odd, used):
            # x is the last vertex; parity 0 means x is even-indexed (in A)
            if len(path) - 1 >= (maxlen if maxlen is not None else 1 << 30):
                return False
            if parity == 0:
                for y in fo[x]:
                    if (used >> y) & 1 or (clos >> y) & 1:
                        continue
                    path.append(y)
                    if y == v:
                        res.append(tuple(path))
                        if limit is not None and len(res) > limit:
                            raise Limit()
                        if first:
                            return True
                    else:
                        if rec(y, 1, clos, odd | (1 << y), used | (1 << y)):
                            return True
                    path.pop()
            else:
                for z in fi[x]:
                    if (used >> z) & 1:
                        continue
                    nc = clos | reach[z]
                    if nc & odd or (nc >> v) & 1:
                        continue
                    path.append(z)
                    if rec(z, 0, nc, odd, used | (1 << z)):
                        return True
                    path.pop()
            return False

        clos0 = reach[u]
        if (clos0 >> v) & 1:       # cannot happen for a maximum flow
            raise RuntimeError("v reachable from u in the residual graph")
        rec(u, 0, clos0, 0, 1 << u)
        return res

    def shortest_cut_path(self, maxlen=None):
        """Length of a shortest u-v path inside some minimum cut, and one such path; (None, None) if none.
        Iterative deepening over odd lengths 1, 3, 5, ..."""
        top = self.g.n - 1 if maxlen is None else maxlen
        L = 1
        while L <= top:
            ps = self.cut_paths(maxlen=L, first=True)
            if ps:
                return len(ps[0]) - 1, ps[0]
            L += 2
        return None, None

    def side_of_path(self, path):
        """The smallest u-side A of a minimum cut containing the path: R-closure of the even vertices."""
        A = 0
        for i in range(0, len(path), 2):
            A |= self.reach[path[i]]
        return A


def cut_mask_of_side(g, A):
    mask = 0
    for e, (a, b) in enumerate(g.edges):
        if ((A >> a) ^ (A >> b)) & 1:
            mask |= 1 << e
    return mask


# ---------------------------------------------------------------------------------------------------------
# set-to-set minimum cuts (capacity matrix, small n) for the test O3
# ---------------------------------------------------------------------------------------------------------

def set_cut(g, S, T, limit=None):
    """Minimum number of edges whose removal separates the vertex set S from the vertex set T (masks, disjoint).
    Super source/sink by merging; unit capacities; augmenting paths on the merged multigraph."""
    n = g.n
    # map vertices: all of S -> node n, all of T -> node n+1, others keep their index
    def node(x):
        if (S >> x) & 1:
            return n
        if (T >> x) & 1:
            return n + 1
        return x
    N = n + 2
    cap = [[0] * N for _ in range(N)]
    for a, b in g.edges:
        p, q = node(a), node(b)
        if p == q:
            continue
        cap[p][q] += 1
        cap[q][p] += 1
    s, t = n, n + 1
    adj = [[y for y in range(N) if cap[x][y] or cap[y][x]] for x in range(N)]
    value = 0
    while True:
        if limit is not None and value >= limit:
            return value
        par = [-1] * N
        par[s] = s
        queue = [s]
        for x in queue:
            if par[t] >= 0:
                break
            for y in adj[x]:
                if par[y] < 0 and cap[x][y] > 0:
                    par[y] = x
                    queue.append(y)
        if par[t] < 0:
            return value
        y = t
        while y != s:
            x = par[y]
            cap[x][y] -= 1
            cap[y][x] += 1
            y = x
        value += 1


def o3_paths(g, u, v, c=None):
    """All paths u-a-b-v of length 3 with min cut between {u,b} and {a,v} equal to c(u,v) (lead's O3)."""
    if c is None:
        c = edge_conn(g, u, v)
    res = []
    Nu = [a for a, _ in g.adj[u] if a != v]
    Nv = set(b for b, _ in g.adj[v] if b != u)
    for a in Nu:
        for b, _ in g.adj[a]:
            if b in Nv and b != u and b != a:
                k = set_cut(g, (1 << u) | (1 << b), (1 << a) | (1 << v), limit=c + 1)
                if k == c:
                    res.append((u, a, b, v))
    return res


def candidate_dc(g, u, v, c=None):
    """Candidate decision for a pair with d(u,v) = 2, c(u,v) >= 3: cp = c iff some u-a-b-v passes O3."""
    if c is None:
        c = edge_conn(g, u, v)
    for a, _ in g.adj[u]:
        if a == v:
            return True
    return bool(o3_paths(g, u, v, c))


# ---------------------------------------------------------------------------------------------------------
# class DC, 3-edge-connectivity class, distances
# ---------------------------------------------------------------------------------------------------------

def dc_violations(g, D=None, stop=None):
    """Pairs x < y with d(x,y) >= 3 and c(x,y) >= 3 (all of them, or the first `stop`)."""
    if D is None:
        D = [bfs(g, s) for s in range(g.n)]
    bad = []
    for x in range(g.n):
        Dx = D[x]
        for y in range(x + 1, g.n):
            if Dx[y] is None:
                continue
            if Dx[y] > 2 and edge_conn(g, x, y, limit=3) >= 3:
                bad.append((x, y))
                if stop is not None and len(bad) >= stop:
                    return bad
    return bad


def in_dc(g, D=None):
    return not dc_violations(g, D, stop=1)


def class3(g, u):
    """Mask of the vertices x with x = u or c(u,x) >= 3."""
    Q = 1 << u
    for x in range(g.n):
        if x != u and edge_conn(g, u, x, limit=3) >= 3:
            Q |= 1 << x
    return Q


def add_vertex(g, nbrs):
    n = g.n
    return Gr(n + 1, list(g.edges) + [(x, n) for x in nbrs])


def fmt(g):
    return " ".join("%d-%d" % e for e in g.edges)


def canon_key(g):
    """Canonical form for small graphs via networkx WL hash + exact check is left to callers; this returns the
    sorted degree sequence (cheap bucket key)."""
    return tuple(sorted(len(a) for a in g.adj))
