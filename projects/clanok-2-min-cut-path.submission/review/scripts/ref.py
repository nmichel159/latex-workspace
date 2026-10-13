"""Referee's own small library (independent of checks/mcp.py).

Graphs: dict vertex -> set of neighbours (simple, undirected).  An edge is a frozenset {x, y}.
Everything is brute force and written from the definitions of drafts/core.tex.
"""

import itertools
from collections import deque


def graph(edges):
    adj = {}
    for a, b in edges:
        if a == b:
            raise ValueError("loop")
        adj.setdefault(a, set()).add(b)
        adj.setdefault(b, set()).add(a)
    return adj


def E(a, b):
    return frozenset((a, b))


def edges_of(adj):
    return {E(a, b) for a in adj for b in adj[a]}


def path_edges(path):
    return [E(a, b) for a, b in zip(path, path[1:])]


def bfs(adj, s, removed=frozenset(), allowed=None):
    """Distances from s in (adj minus the edges in removed), optionally inside the vertex set `allowed`."""
    dist = {s: 0}
    q = deque([s])
    while q:
        x = q.popleft()
        for y in adj[x]:
            if y in dist or E(x, y) in removed:
                continue
            if allowed is not None and y not in allowed:
                continue
            dist[y] = dist[x] + 1
            q.append(y)
    return dist


def comp(adj, s, removed=frozenset(), allowed=None):
    return frozenset(bfs(adj, s, removed, allowed))


def components(adj, removed=frozenset()):
    seen = set()
    res = []
    for s in adj:
        if s not in seen:
            c = comp(adj, s, removed)
            seen |= c
            res.append(c)
    return res


def delta(adj, A):
    return {E(a, b) for a in A for b in adj[a] if b not in A}


def cutvalue(adj, s, t, limit=None):
    """Edge connectivity of s, t by unit augmenting paths (own implementation)."""
    flow = {}                                   # (x, y) -> 1 if one unit goes from x to y
    value = 0
    while limit is None or value < limit:
        par = {s: None}
        q = deque([s])
        while q and t not in par:
            x = q.popleft()
            for y in adj[x]:
                if y in par:
                    continue
                if flow.get((x, y), 0) == 1:    # edge saturated in this direction
                    continue
                par[y] = x
                q.append(y)
        if t not in par:
            break
        y = t
        while par[y] is not None:
            x = par[y]
            if flow.get((y, x), 0) == 1:
                del flow[(y, x)]
            else:
                flow[(x, y)] = 1
            y = x
        value += 1
    return value


def all_simple_paths(adj, s, t, removed=frozenset(), allowed=None, maxlen=None):
    res = []
    path = [s]
    on = {s}

    def rec(x):
        if x == t:
            res.append(tuple(path))
            return
        if maxlen is not None and len(path) - 1 >= maxlen:
            return
        for y in sorted(adj[x], key=str):
            if y in on or E(x, y) in removed:
                continue
            if allowed is not None and y not in allowed:
                continue
            on.add(y)
            path.append(y)
            rec(y)
            path.pop()
            on.discard(y)

    rec(s)
    return res


def connected(adj, s, t, removed=frozenset()):
    return t in bfs(adj, s, removed)


def cp_bruteforce(adj, u, v):
    """cp(u,v) from the definition, organised as min over u-v paths P of |P| + c_{G \\ P}(u,v)."""
    best = None
    for P in all_simple_paths(adj, u, v):
        pe = set(path_edges(P))
        rest = {x: {y for y in adj[x] if E(x, y) not in pe} for x in adj}
        val = len(pe) + cutvalue(rest, u, v)
        if best is None or val < best[0]:
            best = (val, P)
    return best


def cp_literal(adj, u, v):
    """cp(u,v) read literally: smallest edge set that contains a u-v path and whose removal separates u, v."""
    es = sorted(edges_of(adj), key=lambda e: sorted(map(str, e)))
    for size in range(1, len(es) + 1):
        for S in itertools.combinations(es, size):
            S = frozenset(S)
            sub = {x: {y for y in adj[x] if E(x, y) in S} for x in adj}
            if connected(sub, u, v) and not connected(adj, u, v, S):
                return size, S
    return None


def in_class(adj):
    """True iff every two distinct vertices have d <= 2 or c <= 2; else the first violating pair."""
    vs = sorted(adj, key=str)
    for i, x in enumerate(vs):
        dx = bfs(adj, x)
        for y in vs[i + 1:]:
            if dx[y] > 2 and cutvalue(adj, x, y, limit=3) >= 3:
                return False, (x, y)
    return True, None


def min_cuts2(adj, u, v):
    """All u-v cuts with two edges (as frozensets of two edges), for a pair with c(u,v) = 2."""
    es = sorted(edges_of(adj), key=lambda e: sorted(map(str, e)))
    res = []
    for e, f in itertools.combinations(es, 2):
        if not connected(adj, u, v, {e, f}):
            res.append(frozenset((e, f)))
    return res


class Decomposition:
    """Pieces, squares, links, terminals and general paths for a union Fp of minimum u-v cuts.

    cuts: the family of minimum cuts whose union is taken (all of them for the decomposition of the paper)."""

    def __init__(self, adj, u, v, cuts, p1, p2, allcuts=None):
        self.adj, self.u, self.v, self.p1, self.p2 = adj, u, v, p1, p2
        self.F = set().union(*cuts)
        self.tail, self.head = {}, {}
        self.tail_conflict = False
        if allcuts is None:
            allcuts = min_cuts2(adj, u, v)
        for e in self.F:
            tails = set()
            for C in allcuts:
                if e in C:
                    A = comp(adj, u, C)
                    inside = [x for x in e if x in A]
                    tails.add(inside[0] if len(inside) == 1 else None)
            if len(tails) != 1 or None in tails:
                self.tail_conflict = True
            t = next(iter(tails))
            self.tail[e] = t
            self.head[e] = next(x for x in e if x != t)
        self.pieces = components(adj, self.F)
        self.piece_of = {x: P for P in self.pieces for x in P}
        self.ent = {P: [e for e in self.F if self.head[e] in P] for P in self.pieces}
        self.lea = {P: [e for e in self.F if self.tail[e] in P] for P in self.pieces}
        self.is_square = {P: (u in P or v in P or len(self.ent[P]) == 2) for P in self.pieces}
        # order of the squares along p1
        self.squares = []
        for x in p1:
            P = self.piece_of[x]
            if self.is_square[P] and P not in self.squares:
                self.squares.append(P)
        self.links = [P for P in self.pieces if not self.is_square[P]]

    def terminals(self, i):
        """(a_i, b_i, c_i, d_i) of the i-th square (0-based) with respect to p1, p2."""
        S = self.squares[i]
        e1, e2 = set(path_edges(self.p1)), set(path_edges(self.p2))
        if self.u in S:
            a = b = self.u
        else:
            a = [self.head[e] for e in self.ent[S] if e in e1]
            b = [self.head[e] for e in self.ent[S] if e in e2]
            assert len(a) == 1 and len(b) == 1, (a, b)
            a, b = a[0], b[0]
        if self.v in S:
            c = d = self.v
        else:
            c = [self.tail[e] for e in self.lea[S] if e in e1]
            d = [self.tail[e] for e in self.lea[S] if e in e2]
            assert len(c) == 1 and len(d) == 1, (c, d)
            c, d = c[0], d[0]
        return a, b, c, d

    def general_path(self, e):
        """(edges, links, end piece) of the sequence that starts with the edge e of F."""
        es, ls = [e], []
        P = self.piece_of[self.head[e]]
        while not self.is_square[P]:
            assert len(self.lea[P]) == 1
            ls.append(P)
            e = self.lea[P][0]
            es.append(e)
            P = self.piece_of[self.head[e]]
        return es, ls, P


def two_disjoint_paths(adj, u, v):
    """Two edge-disjoint u-v paths by brute force (first pair found among all simple paths)."""
    ps = all_simple_paths(adj, u, v)
    for i, P in enumerate(ps):
        pe = set(path_edges(P))
        for Q in ps[i + 1:]:
            if not pe & set(path_edges(Q)):
                return P, Q
    return None


def fmt(S):
    return "{" + ",".join(sorted(map(str, S))) + "}"


def fmt_e(e):
    a, b = sorted(map(str, e))
    return a + b
