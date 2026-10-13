"""Exact tools for the adversarial verification of theory-dc.md (Lemmas 1, 2, 4, Proposition 5, 11,
Corollary 12, Theorem 13) and dc-hardness.md Theorem 1.

Own implementation (agent verify-equivalence); imports no script of another agent.
Graphs are simple, on vertices 0..n-1, given by an edge list; vertex sets are bitmasks.
Two engines:
  * small graphs (n <= 18): the cut value of every vertex set is tabulated with numpy;
    minimum cuts, connectivities and PIMC are read off the table (brute force);
  * large graphs: unit-capacity max flow by augmenting paths, and a PIMC search that extends
    alternating prefixes and prunes with the separation test "E_P vs O_P + v has value c".
"""
import itertools
import numpy as np
from collections import deque

# ---------------------------------------------------------------- bit tables
_TAB = {}


def bits_table(n):
    if n not in _TAB:
        M = np.arange(1 << n, dtype=np.int64)
        _TAB[n] = [((M >> i) & 1).astype(bool) for i in range(n)]
    return _TAB[n]


def cut_array(n, wedges):
    """wedges: iterable of (a, b, w). Returns int32 array cut[mask] = total weight of edges crossing mask."""
    bits = bits_table(n)
    cut = np.zeros(1 << n, dtype=np.int32)
    for a, b, w in wedges:
        cut += np.int32(w) * (bits[a] ^ bits[b])
    return cut


def popcount(x):
    return bin(x).count("1")


def bit_list(x):
    out = []
    while x:
        low = x & -x
        out.append(low.bit_length() - 1)
        x ^= low
    return out


# ---------------------------------------------------------------- basic graph tools
def adj_masks(n, edges):
    adj = [0] * n
    for a, b in edges:
        adj[a] |= 1 << b
        adj[b] |= 1 << a
    return adj


def bfs_dist(adj, s):
    n = len(adj)
    dist = [-1] * n
    dist[s] = 0
    seen = 1 << s
    front = 1 << s
    d = 0
    while front:
        d += 1
        nxt = 0
        for x in bit_list(front):
            nxt |= adj[x]
        nxt &= ~seen
        for y in bit_list(nxt):
            dist[y] = d
        seen |= nxt
        front = nxt
    return dist


def all_dist(adj):
    return [bfs_dist(adj, s) for s in range(len(adj))]


def component(adj, s, allowed=None):
    if allowed is None:
        allowed = (1 << len(adj)) - 1
    seen = 1 << s
    front = 1 << s
    while front:
        nxt = 0
        for x in bit_list(front):
            nxt |= adj[x]
        nxt &= allowed & ~seen
        seen |= nxt
        front = nxt
    return seen


def bridges(n, edges):
    adj = adj_masks(n, edges)
    out = []
    for a, b in edges:
        adj[a] &= ~(1 << b)
        adj[b] &= ~(1 << a)
        if not (component(adj, a) >> b) & 1:
            out.append((a, b))
        adj[a] |= 1 << b
        adj[b] |= 1 << a
    return out


def is_connected(n, edges):
    return component(adj_masks(n, edges), 0) == (1 << n) - 1


# ---------------------------------------------------------------- small-graph engine
class Small:
    """Tabulated cut function of a simple graph or of a weighted multigraph."""

    def __init__(self, n, wedges):
        self.n = n
        self.wedges = [(a, b, w) for a, b, w in wedges if w]
        self.cut = cut_array(n, self.wedges)
        self.bits = bits_table(n)
        self._c = {}

    def conn(self, x, y):
        key = (x, y) if x < y else (y, x)
        if key not in self._c:
            sel = self.bits[x] & ~self.bits[y]
            self._c[key] = int(self.cut[sel].min())
        return self._c[key]

    def min_cuts(self, u, v):
        sel = self.bits[u] & ~self.bits[v]
        c = int(self.cut[sel].min())
        idx = np.nonzero(sel & (self.cut == c))[0]
        return c, [int(a) for a in idx]

    def min_boundary(self, x, avoid):
        """min |delta(X)| over X containing x and disjoint from the vertex list avoid."""
        sel = self.bits[x].copy()
        for a in avoid:
            sel &= ~self.bits[a]
        return int(self.cut[sel].min())


def cut_graph_adj(adj, A):
    """Adjacency (bitmasks) of the graph formed by the edges of delta(A)."""
    out = []
    for x, nb in enumerate(adj):
        out.append(nb & (~A if (A >> x) & 1 else A))
    return out


def simple_paths(adj, u, v, limit=100000):
    """All simple u-v paths (lists of vertices) of the graph given by bitmask adjacency."""
    res = []
    path = [u]
    onp = 1 << u

    def rec(x):
        if len(res) >= limit:
            return
        for y in bit_list(adj[x] & ~onp_holder[0]):
            if y == v:
                res.append(path + [v])
                continue
            path.append(y)
            onp_holder[0] |= 1 << y
            rec(y)
            onp_holder[0] &= ~(1 << y)
            path.pop()

    onp_holder = [onp]
    rec(u)
    return res


def pimc_from_cuts(adj, cuts, u, v):
    """Is there a minimum cut (from the list of u-sides) whose edges contain a u-v path?
    Returns (answer, list of witness sides)."""
    wit = []
    for A in cuts:
        ca = cut_graph_adj(adj, A)
        if (component(ca, u) >> v) & 1:
            wit.append(A)
    return bool(wit), wit


def cp_brute(sm, adj, u, v):
    """cp(u,v) = min over A (u in A, v not in A) of |delta(A)| + 0-1 distance from u to v
    with weight 0 on the edges of delta(A) and 1 on the other edges (direct from the definition:
    a cut-path S contains delta(A) for A = component of u in G - S and a u-v path)."""
    n = sm.n
    best = None
    sel = sm.bits[u] & ~sm.bits[v]
    for A in np.nonzero(sel)[0]:
        A = int(A)
        base = int(sm.cut[A])
        if best is not None and base >= best:
            continue
        # 0-1 BFS
        dist = [None] * n
        dist[u] = 0
        dq = deque([u])
        while dq:
            x = dq.popleft()
            inA = (A >> x) & 1
            for y in bit_list(adj[x]):
                w = 0 if ((A >> y) & 1) != inA else 1
                nd = dist[x] + w
                if dist[y] is None or nd < dist[y]:
                    dist[y] = nd
                    if w == 0:
                        dq.appendleft(y)
                    else:
                        dq.append(y)
        if dist[v] is None:
            continue
        val = base + dist[v]
        if best is None or val < best:
            best = val
    return best


# ---------------------------------------------------------------- large-graph engine (flows)
class Flow:
    """Unit-capacity undirected graph; max flow between vertex sets by augmenting paths."""

    def __init__(self, n, edges):
        self.n = n
        self.nbrs = [[] for _ in range(n)]
        for a, b in edges:
            self.nbrs[a].append(b)
            self.nbrs[b].append(a)
        self.edges = list(edges)

    def maxflow(self, S, T, cap=None):
        """Max number of edge-disjoint paths from the vertex set S to the vertex set T (disjoint),
        stopped once it exceeds cap (if given). Returns (value, flow dict) with flow[(x,y)] in {-1,0,1}."""
        S = set(S)
        T = set(T)
        if S & T:
            return float("inf"), None
        flow = {}
        val = 0
        while cap is None or val <= cap:
            par = {}
            dq = deque()
            for s in S:
                par[s] = None
                dq.append(s)
            hit = None
            while dq and hit is None:
                x = dq.popleft()
                for y in self.nbrs[x]:
                    if y in par:
                        continue
                    if flow.get((x, y), 0) < 1:
                        par[y] = x
                        if y in T:
                            hit = y
                            break
                        dq.append(y)
            if hit is None:
                break
            y = hit
            while par[y] is not None:
                x = par[y]
                flow[(x, y)] = flow.get((x, y), 0) + 1
                flow[(y, x)] = flow.get((y, x), 0) - 1
                y = x
            val += 1
        return val, flow

    def conn(self, x, y, cap=None):
        return self.maxflow([x], [y], cap)[0]


def pimc_flow_dfs(n, edges, u, v, c=None, node_limit=10 ** 7):
    """Exact PIMC by extending alternating prefixes x_0 = u, x_1, ..., pruned by the necessary and
    sufficient condition that {x_even} and {x_odd} + {v} can be separated by c edges
    (a set separating them separates u from v, so it has >= c edges; with exactly c it is a minimum
    u-v cut containing every prefix edge). Returns (answer, witness path or None, nodes)."""
    F = Flow(n, edges)
    if c is None:
        c = F.conn(u, v)
    path = [u]
    ev = {u}
    od = set()
    nodes = [0]

    def feasible():
        val, _ = F.maxflow(ev, od | {v}, cap=c)
        return val <= c

    found = [None]

    def rec():
        nodes[0] += 1
        if nodes[0] > node_limit:
            raise RuntimeError("node limit")
        x = path[-1]
        pos = len(path)  # position of the next vertex
        for y in F.nbrs[x]:
            if y in ev or y in od:
                continue
            if y == v and pos % 2 == 0:
                continue
            side = od if pos % 2 == 1 else ev
            side.add(y)
            path.append(y)
            ok = feasible()
            if ok:
                if y == v:
                    found[0] = list(path)
                    return True
                if rec():
                    return True
            path.pop()
            side.discard(y)
        return False

    ans = rec()
    return ans, found[0], nodes[0]


# ---------------------------------------------------------------- reduction G -> K -> H
def lemma1_K(n, edges, u):
    """Component of u in G minus its bridges, relabelled. Returns (K vertex list, K edges in new labels, map)."""
    br = set(bridges(n, edges))
    rest = [e for e in edges if e not in br]
    adj = adj_masks(n, rest)
    K = bit_list(component(adj, u))
    idx = {x: i for i, x in enumerate(K)}
    Ke = [(idx[a], idx[b]) for a, b in rest if a in idx and b in idx]
    # edges of G with both ends in K must all be non-bridges
    for a, b in br:
        assert not (a in idx and b in idx), "bridge with both ends in K"
    return K, Ke, idx


def build_H(n, edges, adj, u, conn_u):
    """G 2-edge-connected (checked by caller). conn_u(x) = c(u,x).
    Returns dict with Q (list), ears (list of dicts), real edges (pairs of Q indices),
    ear edges (pairs, with multiplicity), and a list of violated statements of Lemma 4 (1)-(3)."""
    bad = []
    Qmask = 1 << u
    for x in range(n):
        if x != u and conn_u(x) >= 3:
            Qmask |= 1 << x
    Q = bit_list(Qmask)
    qi = {x: i for i, x in enumerate(Q)}
    rest = ((1 << n) - 1) & ~Qmask
    ears = []
    seen = 0
    for x in bit_list(rest):
        if (seen >> x) & 1:
            continue
        X = component(adj, x, rest)
        seen |= X
        bnd = []
        for y in bit_list(X):
            for z in bit_list(adj[y] & ~X):
                bnd.append((z, y))  # (outer, inner)
        if len(bnd) != 2:
            bad.append(("ear boundary size", X, len(bnd)))
            continue
        (p, a), (s, b) = bnd
        if not ((Qmask >> p) & 1 and (Qmask >> s) & 1):
            bad.append(("outer end not in Q", X))
        ears.append(dict(X=X, p=p, a=a, s=s, b=b, short=(a == b)))
    real = [(qi[a], qi[b]) for a, b in edges if (Qmask >> a) & 1 and (Qmask >> b) & 1]
    earE = [(qi[e["p"]], qi[e["s"]]) for e in ears if e["p"] != e["s"]]
    return dict(Q=Q, qi=qi, Qmask=Qmask, ears=ears, real=real, earE=earE, bad=bad)


def H_weights(q, real, earE):
    W = {}
    for a, b in real + earE:
        key = (min(a, b), max(a, b))
        W[key] = W.get(key, 0) + 1
    return W


def restrict_mask(A, Q):
    """Trace A cap Q, re-encoded in Q indices."""
    out = 0
    for i, x in enumerate(Q):
        if (A >> x) & 1:
            out |= 1 << i
    return out


# ---------------------------------------------------------------- preorders and ZZ
def preorder_from_cuts(q, cuts):
    """down[y] = intersection of the cuts containing y (all of 0..q-1 if none): x <= y iff bit x of down[y]."""
    full = (1 << q) - 1
    down = [full] * q
    for A in cuts:
        for y in bit_list(A):
            down[y] &= A
    return down


def leq(down, x, y):
    return (down[y] >> x) & 1 == 1


def lt(down, x, y):
    return leq(down, x, y) and not leq(down, y, x)


def is_downset(down, D):
    for y in bit_list(D):
        if down[y] & ~D:
            return False
    return True


def check_P2(q, down, Radj):
    """Returns list of incomparable pairs without a common R-neighbour above both or below both."""
    fails = []
    for x in range(q):
        for y in range(x + 1, q):
            if leq(down, x, y) or leq(down, y, x):
                continue
            ok = False
            for z in bit_list(Radj[x] & Radj[y]):
                if (leq(down, x, z) and leq(down, y, z)) or (leq(down, z, x) and leq(down, z, y)):
                    ok = True
                    break
            if not ok:
                fails.append((x, y))
    return fails


def zz_dfs(q, down, Radj, u, v):
    """Search for a consistent zigzag u = x_0 < x_1 > x_2 < ... > ... < x_L = v along R (simple path)."""
    path = [u]
    onp = [1 << u]
    valleys = [u]
    peaks = []

    def rec():
        x = path[-1]
        pos = len(path)  # position of next vertex: odd -> peak, even -> valley
        for y in bit_list(Radj[x] & ~onp[0]):
            if pos % 2 == 1:  # y is a peak: need x < y, and no valley >= y
                if not lt(down, x, y):
                    continue
                if any(leq(down, y, a) for a in valleys):
                    continue
                if y == v:
                    path.append(y)
                    return True
                peaks.append(y)
                path.append(y)
                onp[0] |= 1 << y
                if rec():
                    return True
                onp[0] &= ~(1 << y)
                path.pop()
                peaks.pop()
            else:  # y is a valley: need y < x, and y not >= any peak
                if y == v:
                    continue
                if not lt(down, y, x):
                    continue
                if any(leq(down, p, y) for p in peaks):
                    continue
                valleys.append(y)
                path.append(y)
                onp[0] |= 1 << y
                if rec():
                    return True
                onp[0] &= ~(1 << y)
                path.pop()
                valleys.pop()
        return False

    ok = rec()
    return ok, (list(path) if ok else None)


def zz_downsets(q, down, Radj, u, v):
    """For every down-set D containing u and not v: is v reachable from u along R-edges crossing D?"""
    for D in range(1 << q):
        if not (D >> u) & 1 or (D >> v) & 1:
            continue
        if not is_downset(down, D):
            continue
        ca = [Radj[x] & (~D if (D >> x) & 1 else D) for x in range(q)]
        if (component(ca, u) >> v) & 1:
            return True, D
    return False, None


# ---------------------------------------------------------------- Theorem 13(b) realisation
def realise(q, down, R, u, v, M=None):
    """Simple graph G(Pi) of Theorem 13(b). Elements 0..q-1 keep their labels; ear vertices follow.
    Every strict pair a < b: edge ab if {a,b} in R else an ear vertex; plus an ear u-a (a != u) and an
    ear b-v (b != v). Equivalent elements: M ears each (default N + 1).
    Returns (n, edges, N, info)."""
    Rset = {(min(a, b), max(a, b)) for a, b in R}
    pairs = [(a, b) for a in range(q) for b in range(q) if a != b and lt(down, a, b)]
    N = len(pairs)
    eqv = [(a, b) for a in range(q) for b in range(a + 1, q) if leq(down, a, b) and leq(down, b, a)]
    if M is None:
        M = N + 1
    edges = []
    nxt = [q]

    def ear(x, y):
        w = nxt[0]
        nxt[0] += 1
        edges.append((min(x, w), max(x, w)))
        edges.append((min(y, w), max(y, w)))

    for a, b in pairs:
        if (min(a, b), max(a, b)) in Rset:
            edges.append((min(a, b), max(a, b)))
        else:
            ear(a, b)
        if a != u:
            ear(u, a)
        if b != v:
            ear(b, v)
    for a, b in eqv:
        for _ in range(M):
            ear(a, b)
    return nxt[0], edges, N, dict(pairs=pairs, eqv=eqv, M=M)


def W_of_realisation(q, down, R, u, v, M):
    """Weighted graph W on the elements that the realisation induces (ear vertex between p, s -> weight on ps)."""
    n, edges, N, info = realise(q, down, R, u, v, M)
    W = {}
    deg = {}
    for a, b in edges:
        deg[a] = deg.get(a, 0) + 1
        deg[b] = deg.get(b, 0) + 1
    nb = {}
    for a, b in edges:
        nb.setdefault(a, []).append(b)
        nb.setdefault(b, []).append(a)
    for a, b in edges:
        if a < q and b < q:
            W[(a, b)] = W.get((a, b), 0) + 1
    for w in range(q, n):
        p, s = nb[w]
        key = (min(p, s), max(p, s))
        W[key] = W.get(key, 0) + 1
    return W, N


# ---------------------------------------------------------------- DC membership
def in_class_small(sm, dist, n, k):
    """Every pair has d <= 2 or c <= k (small engine)."""
    for x in range(n):
        for y in range(x + 1, n):
            if dist[x][y] == -1 or dist[x][y] > 2:
                if sm.conn(x, y) > k:
                    return False
    return True


def in_class_flow(n, edges, k):
    """Same for large graphs: degree bound first, flow otherwise."""
    adj = adj_masks(n, edges)
    deg = [popcount(a) for a in adj]
    F = Flow(n, edges)
    dist = all_dist(adj)
    for x in range(n):
        for y in range(x + 1, n):
            if dist[x][y] == -1 or dist[x][y] > 2:
                if min(deg[x], deg[y]) <= k:
                    continue
                if F.conn(x, y, cap=k) > k:
                    return False
    return True
