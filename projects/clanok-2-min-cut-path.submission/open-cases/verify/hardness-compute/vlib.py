"""Exact routines of the independent verifier "verify-hardness-compute".

Written from scratch; nothing is imported from hardness/, theory-dc-scripts/ or experiments/.
Graphs are simple and undirected on the vertices 0..n-1; edges get ids 0..m-1.

Contents
  Gr                       graph with adjacency lists; duplicate edges or loops raise (catches construction errors)
  maxflow_py               unit-capacity max flow between vertex sets (augmenting paths, pure Python), returns flows
  flow_value               the same value with scipy's Dinic (fast, value only), optional removed edges
  min_cuts_residual        all minimum u-v cuts as closed sets of the residual digraph (SCC + ideal enumeration)
  min_cuts_brute           all minimum u-v cuts by enumerating every vertex set (numpy, n <= 25)
  min_cuts_branch          all minimum u-v cuts by naive branching on vertices with max-flow pruning
  cut_graph_connects       is u connected to v in H_A = (V, delta(A))
  cp_eq_c_bb               definition-based test of cp(u,v) = c(u,v): search over simple u-v paths P with
                           f(P) = |P| + c_{G-P}(u,v) = c, pruned by the monotonicity of f along prefixes
  cp_paths                 cp(u,v) = min over simple u-v paths P of |P| + c_{G-P}(u,v)   (small graphs)
  cp_definition            cp(u,v) from the literal definition (edge sets of growing size; tiny graphs)
  distances, diameter      BFS
  all_pairs_c              local edge connectivity of all pairs (Gomory-Hu tree of networkx)
"""

import itertools
from collections import deque

import networkx as nx
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import maximum_flow


class TooMany(Exception):
    pass


class Gr:
    def __init__(self, n, edges, allow_dup=False):
        es, seen = [], set()
        for a, b in edges:
            if a == b:
                raise ValueError("loop at %d" % a)
            key = (min(a, b), max(a, b))
            if key in seen:
                if allow_dup:
                    continue
                raise ValueError("duplicate edge %s" % (key,))
            seen.add(key)
            es.append(key)
        for a, b in es:
            if not (0 <= a < n and 0 <= b < n):
                raise ValueError("vertex out of range")
        self.n, self.edges, self.m = n, es, len(es)
        self.adj = [[] for _ in range(n)]
        for i, (a, b) in enumerate(es):
            self.adj[a].append((b, i))
            self.adj[b].append((a, i))
        self.eset = seen
        self._rows = np.array([a for a, b in es] + [b for a, b in es], dtype=np.int32)
        self._cols = np.array([b for a, b in es] + [a for a, b in es], dtype=np.int32)

    def has_edge(self, a, b):
        return (min(a, b), max(a, b)) in self.eset


# ------------------------------------------------------------------------------------------------
# max flow
# ------------------------------------------------------------------------------------------------

def maxflow_py(g, S, T, removed=frozenset()):
    """Unit-capacity undirected max flow from the set S to the set T (disjoint), edges in `removed` deleted.
    f[e] in {-1, 0, 1} is the net flow from edges[e][0] to edges[e][1].
    Returns (value, f, reach) with reach = vertices reachable from S in the final residual graph."""
    S, T = set(S), set(T)
    assert S and T and not (S & T)
    f = [0] * g.m
    value = 0
    while True:
        par = {x: None for x in S}
        dq = deque(S)
        hit = None
        while dq and hit is None:
            x = dq.popleft()
            for y, e in g.adj[x]:
                if y in par or e in removed:
                    continue
                a = g.edges[e][0]
                res = (1 - f[e]) if x == a else (1 + f[e])
                if res > 0:
                    par[y] = (x, e)
                    if y in T:
                        hit = y
                        break
                    dq.append(y)
        if hit is None:
            return value, f, set(par)
        y = hit
        while par[y] is not None:
            x, e = par[y]
            if x == g.edges[e][0]:
                f[e] += 1
            else:
                f[e] -= 1
            y = x
        value += 1


def flow_value(g, S, T, removed=()):
    """Max flow value from S to T with scipy (Dinic); `removed` = iterable of edge ids deleted."""
    S, T = list(S), list(T)
    n = g.n
    if removed:
        keep = np.ones(g.m, dtype=bool)
        keep[list(removed)] = False
        k2 = np.concatenate([keep, keep])
        rows, cols = g._rows[k2], g._cols[k2]
    else:
        rows, cols = g._rows, g._cols
    big = g.m + 1
    s, t = n, n + 1
    rows = np.concatenate([rows, np.full(len(S), s, dtype=np.int32), np.array(T, dtype=np.int32)])
    cols = np.concatenate([cols, np.array(S, dtype=np.int32), np.full(len(T), t, dtype=np.int32)])
    data = np.concatenate([np.ones(len(rows) - len(S) - len(T), dtype=np.int32),
                           np.full(len(S) + len(T), big, dtype=np.int32)])
    mat = csr_matrix((data, (rows, cols)), shape=(n + 2, n + 2))
    mat.sum_duplicates()
    return int(maximum_flow(mat, s, t, method="dinic").flow_value)


# ------------------------------------------------------------------------------------------------
# minimum cuts
# ------------------------------------------------------------------------------------------------

def _closure(nbrs, start):
    seen = set(start)
    dq = deque(start)
    while dq:
        x = dq.popleft()
        for y in nbrs[x]:
            if y not in seen:
                seen.add(y)
                dq.append(y)
    return seen


def min_cuts_residual(g, u, v, limit=1 << 20):
    """(c, list of frozensets A): all minimum u-v cuts delta(A), u in A, v not in A, as the closed sets of the
    residual digraph of one maximum flow."""
    c, f, _ = maxflow_py(g, [u], [v])
    succ = [[] for _ in range(g.n)]
    pred = [[] for _ in range(g.n)]
    for e, (a, b) in enumerate(g.edges):
        if 1 - f[e] > 0:
            succ[a].append(b)
            pred[b].append(a)
        if 1 + f[e] > 0:
            succ[b].append(a)
            pred[a].append(b)
    rmin = _closure(succ, [u])
    bv = _closure(pred, [v])
    assert not (rmin & bv), "flow not maximum"
    free = [x for x in range(g.n) if x not in rmin and x not in bv]
    fset = set(free)
    D = nx.DiGraph()
    D.add_nodes_from(free)
    D.add_edges_from((x, y) for x in free for y in succ[x] if y in fset)
    C = nx.condensation(D)
    members = {X: C.nodes[X]["members"] for X in C.nodes}
    desc = {X: nx.descendants(C, X) for X in C.nodes}
    anc = {X: nx.ancestors(C, X) for X in C.nodes}
    order = list(nx.topological_sort(C))
    out = []
    base = frozenset(rmin)

    def rec(inc, exc):
        X = next((Y for Y in order if Y not in inc and Y not in exc), None)
        if X is None:
            A = set(base)
            for Y in inc:
                A |= members[Y]
            out.append(frozenset(A))
            if len(out) > limit:
                raise TooMany
            return
        rec(inc | {X} | desc[X], exc)
        rec(inc, exc | {X} | anc[X])

    rec(frozenset(), frozenset())
    return c, out


def cut_size(g, A):
    return sum(1 for a, b in g.edges if (a in A) != (b in A))


def min_cuts_brute(g, u, v, chunk=1 << 20):
    """(c, list of frozensets): every vertex set A with u in A, v not in A is evaluated (n <= 25 or so)."""
    others = [x for x in range(g.n) if x not in (u, v)]
    k = len(others)
    total = 1 << k
    best, sols = None, []
    ea = np.array([a for a, b in g.edges])
    eb = np.array([b for a, b in g.edges])
    for start in range(0, total, chunk):
        idx = np.arange(start, min(total, start + chunk), dtype=np.int64)
        side = np.zeros((g.n, len(idx)), dtype=np.int8)
        side[u, :] = 1
        for i, x in enumerate(others):
            side[x, :] = (idx >> i) & 1
        cnt = np.zeros(len(idx), dtype=np.int32)
        for a, b in zip(ea, eb):
            cnt += side[a] ^ side[b]
        mn = int(cnt.min())
        if best is None or mn < best:
            best, sols = mn, []
        if mn == best:
            for t in idx[cnt == mn]:
                A = {u} | {others[i] for i in range(k) if (int(t) >> i) & 1}
                sols.append(frozenset(A))
    return best, sols


def min_cuts_branch(g, u, v, c, order=None, limit=1 << 16):
    """All minimum u-v cuts by branching vertex by vertex; a node (S, T) is kept iff lambda(S, T) == c."""
    order = order if order is not None else [x for x in range(g.n) if x not in (u, v)]
    out = []
    calls = [0]

    def rec(i, S, T):
        calls[0] += 1
        val = flow_value(g, S, T)
        assert val >= c
        if val > c:
            return
        if i == len(order):
            out.append(frozenset(S))
            if len(out) > limit:
                raise TooMany
            return
        x = order[i]
        rec(i + 1, S + [x], T)
        rec(i + 1, S, T + [x])

    rec(0, [u], [v])
    return out, calls[0]


def cut_graph_connects(g, A, u, v):
    seen = {u}
    dq = deque([u])
    while dq:
        x = dq.popleft()
        if x == v:
            return True
        for y, e in g.adj[x]:
            if y not in seen and ((x in A) != (y in A)):
                seen.add(y)
                dq.append(y)
    return v in seen


def cut_graph_dist(g, A, u, v):
    dist = {u: 0}
    dq = deque([u])
    while dq:
        x = dq.popleft()
        for y, e in g.adj[x]:
            if y not in dist and ((x in A) != (y in A)):
                dist[y] = dist[x] + 1
                dq.append(y)
    return dist.get(v)


# ------------------------------------------------------------------------------------------------
# cp
# ------------------------------------------------------------------------------------------------

def cp_eq_c_bb(g, u, v, c=None, node_limit=None, want_all=False):
    """Decide cp(u,v) == c(u,v) from the identity cp = min_P (|P| + c_{G-P}(u,v)) over simple u-v paths P.
    f(P') = |P'| + c_{G-P'} never decreases when P' is extended and is always >= c, so only prefixes with
    f = c are extended. Returns (answer, path or None, nodes); with want_all, the list of all such paths.
    Raises TooMany when node_limit is exceeded."""
    if c is None:
        c = flow_value(g, [u], [v])
    path = [u]
    onpath = {u}
    removed = []
    nodes = [0]
    found = []

    def rec(x):
        nodes[0] += 1
        if node_limit is not None and nodes[0] > node_limit:
            raise TooMany
        for y, e in g.adj[x]:
            if y in onpath:
                continue
            removed.append(e)
            val = flow_value(g, [u], [v], removed)
            ok = (len(removed) + val == c)
            if ok:
                path.append(y)
                if y == v:
                    found.append(list(path))
                    if not want_all:
                        return True
                else:
                    onpath.add(y)
                    if rec(y) and not want_all:
                        return True
                    onpath.discard(y)
                path.pop()
            removed.pop()
        return False

    rec(u)
    if want_all:
        return bool(found), found, nodes[0]
    return bool(found), (found[0] if found else None), nodes[0]


def cp_paths(g, u, v, cutoff=None):
    """cp(u,v) = min over all simple u-v paths P of |P| + c_{G-P}(u,v)."""
    G = nx.Graph()
    G.add_nodes_from(range(g.n))
    G.add_edges_from(g.edges)
    best = None
    eid = {e: i for i, e in enumerate(g.edges)}
    for p in nx.all_simple_paths(G, u, v, cutoff=cutoff):
        rem = [eid[(min(a, b), max(a, b))] for a, b in zip(p, p[1:])]
        val = len(rem) + flow_value(g, [u], [v], rem)
        if best is None or val < best:
            best = val
    return best


def _connected_with(g, u, v, allowed):
    seen = {u}
    dq = deque([u])
    while dq:
        x = dq.popleft()
        for y, e in g.adj[x]:
            if allowed[e] and y not in seen:
                seen.add(y)
                dq.append(y)
    return v in seen


def cp_definition(g, u, v):
    """Smallest edge set S that contains a u-v path (u, v connected in (V, S)) and a u-v cut (u, v separated in G - S)."""
    for k in range(1, g.m + 1):
        for S in itertools.combinations(range(g.m), k):
            ins = [False] * g.m
            for e in S:
                ins[e] = True
            if not _connected_with(g, u, v, ins):
                continue
            if _connected_with(g, u, v, [not t for t in ins]):
                continue
            return k
    return None


# ------------------------------------------------------------------------------------------------
# distances, classes
# ------------------------------------------------------------------------------------------------

def distances(g):
    INF = 10 ** 9
    D = np.full((g.n, g.n), INF, dtype=np.int64)
    for s in range(g.n):
        D[s, s] = 0
        dq = deque([s])
        while dq:
            x = dq.popleft()
            for y, e in g.adj[x]:
                if D[s, y] == INF:
                    D[s, y] = D[s, x] + 1
                    dq.append(y)
    return D


def all_pairs_c(g):
    """n x n matrix of local edge connectivities (Gomory-Hu tree)."""
    G = nx.Graph()
    G.add_nodes_from(range(g.n))
    for a, b in g.edges:
        G.add_edge(a, b, capacity=1)
    T = nx.gomory_hu_tree(G)
    C = np.zeros((g.n, g.n), dtype=np.int64)
    for s in range(g.n):
        # min edge weight along tree paths from s
        best = {s: 10 ** 9}
        dq = deque([s])
        while dq:
            x = dq.popleft()
            for y in T[x]:
                if y not in best:
                    best[y] = min(best[x], T[x][y]["weight"])
                    dq.append(y)
        for y, w in best.items():
            if y != s:
                C[s, y] = w
    return C


def from_nx(G):
    mp = {x: i for i, x in enumerate(G.nodes())}
    return Gr(len(mp), [(mp[a], mp[b]) for a, b in G.edges()])


def flow_with_matrix(g, S, T, removed=()):
    """(value, flow csr) with scipy; flow[x, y] is the net flow from x to y (antisymmetric)."""
    S, T = list(S), list(T)
    n = g.n
    if removed:
        keep = np.ones(g.m, dtype=bool)
        keep[list(removed)] = False
        k2 = np.concatenate([keep, keep])
        rows, cols = g._rows[k2], g._cols[k2]
    else:
        rows, cols = g._rows, g._cols
    big = g.m + 1
    s, t = n, n + 1
    rows = np.concatenate([rows, np.full(len(S), s, dtype=np.int32), np.array(T, dtype=np.int32)])
    cols = np.concatenate([cols, np.array(S, dtype=np.int32), np.full(len(T), t, dtype=np.int32)])
    data = np.concatenate([np.ones(len(rows) - len(S) - len(T), dtype=np.int32),
                           np.full(len(S) + len(T), big, dtype=np.int32)])
    mat = csr_matrix((data, (rows, cols)), shape=(n + 2, n + 2))
    mat.sum_duplicates()
    res = maximum_flow(mat, s, t, method="dinic")
    return int(res.flow_value), res.flow.tocsr()


def cp_eq_c_bb2(g, u, v, c=None, node_limit=None, want_all=False):
    """Same search as cp_eq_c_bb, with a sound filter: at a node P (end x) one maximum flow F of G - P is computed,
    and only edges xy carrying flow in F are tried (if xy carries no flow in F, F stays feasible in G - P - xy,
    so c_{G-P-xy} = c_{G-P} and f does not stay at c)."""
    if c is None:
        c = flow_value(g, [u], [v])
    path = [u]
    onpath = {u}
    removed = []
    nodes = [0]
    found = []

    def rec(x):
        nodes[0] += 1
        if node_limit is not None and nodes[0] > node_limit:
            raise TooMany
        val0, F = flow_with_matrix(g, [u], [v], removed)
        assert len(removed) + val0 == c
        lo, hi = F.indptr[x], F.indptr[x + 1]
        carrying = {int(y) for y, w in zip(F.indices[lo:hi], F.data[lo:hi]) if w != 0}
        for y, e in g.adj[x]:
            if y in onpath or y not in carrying:
                continue
            removed.append(e)
            val = flow_value(g, [u], [v], removed)
            if len(removed) + val == c:
                path.append(y)
                if y == v:
                    found.append(list(path))
                    if not want_all:
                        return True
                else:
                    onpath.add(y)
                    if rec(y) and not want_all:
                        return True
                    onpath.discard(y)
                path.pop()
            removed.pop()
        return False

    rec(u)
    if want_all:
        return bool(found), found, nodes[0]
    return bool(found), (found[0] if found else None), nodes[0]
