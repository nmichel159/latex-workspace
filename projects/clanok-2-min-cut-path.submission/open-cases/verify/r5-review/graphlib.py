"""Own graph tools of the reviewer r5-verify: realisation of a ZZ instance (theory-dc.md Theorem 13(b)), BFS,
unit-capacity max-flow (Dinic), residual closures, and an exact search for a u-v path inside a minimum u-v cut that
does not use the order (prefix test by residual closures of one maximum flow, Picard-Queyranne).
No code of other agents is imported here."""
from collections import deque


class Graph:
    def __init__(self, nv):
        self.nv = nv
        self.adj = [[] for _ in range(nv)]
        self.edges = set()

    def add_vertex(self):
        self.adj.append([])
        self.nv += 1
        return self.nv - 1

    def add_edge(self, a, b):
        assert a != b
        k = (min(a, b), max(a, b))
        assert k not in self.edges, "multi-edge %s" % (k,)
        self.edges.add(k)
        self.adj[a].append(b)
        self.adj[b].append(a)

    def bfs(self, s):
        dist = [-1] * self.nv
        dist[s] = 0
        q = deque([s])
        while q:
            x = q.popleft()
            for y in self.adj[x]:
                if dist[y] < 0:
                    dist[y] = dist[x] + 1
                    q.append(y)
        return dist


def realise(inst):
    """Theorem 13(b) of theory-dc.md for instances without ties: every strict pair a < b carries a real edge (if in R)
    or an ear (a new vertex of degree 2); plus an ear u-a (a != u) and an ear b-v (b != v) for every such pair.
    Returns (graph, N = number of strictly comparable pairs, list of ear vertices with their attachments)."""
    assert not inst.has_ties()
    n = inst.n
    G = Graph(n)
    Rset = {frozenset(e) for e in inst.R}
    ears = []

    def ear(p, s):
        w = G.add_vertex()
        G.add_edge(p, w)
        G.add_edge(w, s)
        ears.append((w, p, s))
    N = 0
    for a in range(n):
        for b in range(n):
            if a != b and inst.lt(a, b):
                N += 1
                if frozenset((a, b)) in Rset:
                    G.add_edge(a, b)
                else:
                    ear(a, b)
                if a != inst.u:
                    ear(inst.u, a)
                if b != inst.v:
                    ear(b, inst.v)
    return G, N, ears


class Flow:
    """Unit-capacity undirected max-flow (each edge capacity 1 in both directions), Dinic."""

    def __init__(self, G):
        self.G = G
        self.nv = G.nv
        self.head = [[] for _ in range(G.nv)]
        self.to = []
        self.cap = []
        for a, b in G.edges:
            self._arc(a, b)

    def _arc(self, a, b):
        # one pair of arcs with capacity 1 each way (undirected edge)
        self.head[a].append(len(self.to))
        self.to.append(b)
        self.cap.append(1)
        self.head[b].append(len(self.to))
        self.to.append(a)
        self.cap.append(1)

    def maxflow(self, s, t):
        self.flow_value = 0
        to, cap, head = self.to, self.cap, self.head
        while True:
            level = [-1] * self.nv
            level[s] = 0
            q = deque([s])
            while q:
                x = q.popleft()
                for e in head[x]:
                    if cap[e] > 0 and level[to[e]] < 0:
                        level[to[e]] = level[x] + 1
                        q.append(to[e])
            if level[t] < 0:
                break
            it = [0] * self.nv

            def dfs(x, f):
                if x == t:
                    return f
                while it[x] < len(head[x]):
                    e = head[x][it[x]]
                    y = to[e]
                    if cap[e] > 0 and level[y] == level[x] + 1:
                        d = dfs(y, min(f, cap[e]))
                        if d:
                            cap[e] -= d
                            cap[e ^ 1] += d
                            return d
                    it[x] += 1
                return 0
            import sys
            sys.setrecursionlimit(max(10000, 4 * self.nv))
            while True:
                f = dfs(s, 1 << 30)
                if not f:
                    break
                self.flow_value += f
        return self.flow_value

    def closure(self, S, base=0):
        """Vertices reachable from S along arcs with positive residual capacity (bitmask), starting from `base`."""
        C = base
        stack = []
        for x in S:
            if not (C >> x) & 1:
                C |= 1 << x
                stack.append(x)
        to, cap, head = self.to, self.cap, self.head
        while stack:
            x = stack.pop()
            for e in head[x]:
                if cap[e] > 0:
                    y = to[e]
                    if not (C >> y) & 1:
                        C |= 1 << y
                        stack.append(y)
        return C


    def coclosure(self, S, base=0):
        """Vertices from which S is reachable along arcs with positive residual capacity (bitmask)."""
        C = base
        stack = []
        for x in S:
            if not (C >> x) & 1:
                C |= 1 << x
                stack.append(x)
        to, cap, head = self.to, self.cap, self.head
        while stack:
            x = stack.pop()
            for e in head[x]:
                if cap[e ^ 1] > 0:
                    y = to[e]
                    if not (C >> y) & 1:
                        C |= 1 << y
                        stack.append(y)
        return C


def cut_size(G, A):
    """|delta(A)| for a vertex bitmask A."""
    return sum(1 for a, b in G.edges if ((A >> a) & 1) != ((A >> b) & 1))


def pimc_search(G, F, u, v, c, max_states=2_000_000):
    """Is there a u-v walk (hence a path) all of whose edges lie in one minimum u-v cut?  F: Flow after maxflow(u,v)
    of value c.  State: (current vertex, parity, C = residual closure of the even vertices, U = residual
    co-closure (vertices that reach an odd vertex or v)); the prefix is feasible iff C and U are disjoint (then
    delta(C) is a minimum cut containing all its edges, since closed sets containing u and missing v are exactly the
    source sides of minimum cuts).  Exact for the existence question.  Returns (answer, number of states, walk)."""
    C0 = F.closure([u])
    U0 = F.coclosure([v])
    if C0 & U0:
        return False, 0, None
    start = (u, 0, C0, U0)
    seen = {start}
    front = {(u, 0): [(C0, U0)]}
    parent = {start: None}
    q = deque([start])
    while q:
        st = q.popleft()
        x, par, C, U = st
        for y in G.adj[x]:
            if par == 0:
                if (C >> y) & 1:
                    continue
                U2 = F.coclosure([y], U) if not (U >> y) & 1 else U
                if U2 & C:
                    continue
                if y == v:
                    walk = [y]
                    s = st
                    while s is not None:
                        walk.append(s[0])
                        s = parent[s]
                    return True, len(seen), walk[::-1]
                ns = (y, 1, C, U2)
            else:
                if (U >> y) & 1:
                    continue
                C2 = F.closure([y], C) if not (C >> y) & 1 else C
                if C2 & U:
                    continue
                ns = (y, 0, C2, U)
            if ns in seen:
                continue
            # dominance: a state with the same vertex and parity and smaller C, U allows every continuation of ns
            key = (ns[0], ns[1])
            lst = front.setdefault(key, [])
            if any((C1 & ~ns[2]) == 0 and (U1 & ~ns[3]) == 0 for C1, U1 in lst):
                continue
            lst.append((ns[2], ns[3]))
            seen.add(ns)
            parent[ns] = st
            if len(seen) > max_states:
                raise RuntimeError("state limit")
            q.append(ns)
    return False, len(seen), None
