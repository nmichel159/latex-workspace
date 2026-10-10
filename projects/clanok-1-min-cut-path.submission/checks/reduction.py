"""Executable model of Algorithm 1 (reduction from 3-SAT to Separating Shortest Path).

The graph is built as the manuscript prescribes: BuildChain, the labelling of the chain links,
Thread (the threading operation of Definition 3.4 and connecting paths of one edge each) and
Calibrate. Two choices are left open by the text: which free edge of a path is subdivided by a
threading, and in which direction a thread runs through its crossing edge. Both are taken from a
seeded random generator (or fixed with choice="first"), so the checks cover different admissible
outputs of the algorithm.

A formula is a list of clauses; a clause is a tuple of three non-zero integers, +i for the literal
x_i and -i for its negation (variables are numbered from 1).
"""

import random
from collections import deque


def edge(a, b):
    return (a, b) if a < b else (b, a)


class Link:
    """A chain link: the cycle formed by two q-p paths, kept as vertex lists from q to p."""

    def __init__(self, idx, q, p, a, b):
        self.idx = idx
        self.q = q
        self.p = p
        self.paths = {"+": [q, a, p], "-": [q, b, p]}
        self.label = None  # ("I", i), ("T", i) or ("L", j, k)

    def path_edges(self, sign):
        path = self.paths[sign]
        return [edge(path[i], path[i + 1]) for i in range(len(path) - 1)]


class Thread:
    def __init__(self, kind, owner, spec):
        self.kind = kind          # "sync2", "sync3" or "clause"
        self.owner = owner        # variable index i, or clause index k for a clause thread
        self.spec = spec          # [(link index, sign), ...] as passed to Thread(...)
        self.crossings = []       # [(first vertex, second vertex)] in the direction of the thread
        self.connecting = []      # t + 1 vertex lists, from u to the first crossing edge, ..., to v

    def crossing_edges(self):
        return [edge(a, b) for a, b in self.crossings]

    def edges(self):
        result = self.crossing_edges()
        for path in self.connecting:
            result.extend(edge(path[i], path[i + 1]) for i in range(len(path) - 1))
        return result

    def vertex_sequence(self):
        seq = []
        for r, path in enumerate(self.connecting):
            seq.extend(path if r == 0 else path[1:])
            if r < len(self.crossings):
                seq.append(self.crossings[r][1])
        return seq


class Reduction:
    def __init__(self, n, clauses, choice="random", seed=0, calibrate=True, lengthen=True):
        # lengthen=False skips the second step of Calibrate: the connecting paths keep one edge.
        # Their inner vertices have degree two, so u-v connectivity after removing chain edges is
        # the same in both graphs; the short graph is used for exhaustive connectivity tests.
        self.lengthen = lengthen
        self.n = n
        self.clauses = [tuple(c) for c in clauses]
        self.m = len(self.clauses)
        self.rng = random.Random(seed)
        self.choice = choice
        self.adj = {}
        self.next_vertex = 0
        self.links = []
        self.singles = []
        self.threads = []
        self.crossing = set()
        self.Lambda = None
        self._build()
        if calibrate:
            self._calibrate()

    # -- graph primitives -------------------------------------------------------------------

    def _new_vertex(self):
        w = self.next_vertex
        self.next_vertex += 1
        self.adj[w] = set()
        return w

    def _add_edge(self, a, b):
        assert a != b and b not in self.adj[a], "the graph must stay simple"
        self.adj[a].add(b)
        self.adj[b].add(a)

    def _remove_edge(self, a, b):
        self.adj[a].remove(b)
        self.adj[b].remove(a)

    def _subdivide(self, path, pos, count):
        """Replace the edge path[pos] path[pos+1] by a path with `count` new inner vertices."""
        a, b = path[pos], path[pos + 1]
        self._remove_edge(a, b)
        inner = [self._new_vertex() for _ in range(count)]
        walk = [a] + inner + [b]
        for i in range(len(walk) - 1):
            self._add_edge(walk[i], walk[i + 1])
        path[pos + 1:pos + 1] = inner
        return inner

    # -- Algorithm 1 ------------------------------------------------------------------------

    def _build_chain(self, r):
        """BuildChain(u, v, r): single edges H_1..H_{r+1} and r chain links, each a 4-cycle."""
        self.u = self._new_vertex()
        p = self.u
        for idx in range(r):
            q = self._new_vertex()
            self._add_edge(p, q)
            self.singles.append(edge(p, q))
            a, b, p_next = self._new_vertex(), self._new_vertex(), self._new_vertex()
            for x, y in ((q, a), (a, p_next), (q, b), (b, p_next)):
                self._add_edge(x, y)
            self.links.append(Link(idx, q, p_next, a, b))
            p = p_next
        self.v = self._new_vertex()
        self._add_edge(p, self.v)
        self.singles.append(edge(p, self.v))

    def _thread(self, kind, owner, spec):
        """Thread(u, v, [(K_1, s_1), ..., (K_t, s_t)])."""
        thread = Thread(kind, owner, spec)
        for link_idx, sign in spec:
            path = self.links[link_idx].paths[sign]
            free = [i for i in range(len(path) - 1) if edge(path[i], path[i + 1]) not in self.crossing]
            pos = free[0] if self.choice == "first" else self.rng.choice(free)
            z1, z2 = self._subdivide(path, pos, 2)
            self.crossing.add(edge(z1, z2))
            if self.choice != "first" and self.rng.random() < 0.5:
                z1, z2 = z2, z1
            thread.crossings.append((z1, z2))
        ends = [self.u] + [w for pair in thread.crossings for w in pair] + [self.v]
        for r in range(len(spec) + 1):
            a, b = ends[2 * r], ends[2 * r + 1]
            self._add_edge(a, b)
            thread.connecting.append([a, b])
        self.threads.append(thread)

    def _build(self):
        n, m = self.n, self.m
        self._build_chain(2 * n + 3 * m)
        # M: variable -> list of its literals, each literal identified with its position (j, k)
        self.M = {i: [] for i in range(1, n + 1)}
        for k, clause in enumerate(self.clauses, start=1):
            assert len(clause) == 3
            for j, lit in enumerate(clause, start=1):
                self.M[abs(lit)].append((j, k))
        self.I, self.T, self.L, self.block = {}, {}, {}, {}
        free = 0
        for i in range(1, n + 1):
            lits = self.M[i]
            reserved = list(range(free, free + 2 + len(lits)))
            free += 2 + len(lits)
            self.block[i] = reserved
            self.I[i], self.T[i] = reserved[0], reserved[-1]
            self.links[reserved[0]].label = ("I", i)
            self.links[reserved[-1]].label = ("T", i)
            for idx, (j, k) in zip(reserved[1:-1], lits):
                self.L[(j, k)] = idx
                self.links[idx].label = ("L", j, k)
        assert free == 2 * n + 3 * m
        for i in range(1, n + 1):
            self._thread("sync2", i, [(self.I[i], "+"), (self.T[i], "-")])
            self._thread("sync2", i, [(self.I[i], "-"), (self.T[i], "+")])
            for jk in self.M[i]:
                self._thread("sync3", i, [(self.I[i], "+"), (self.L[jk], "-"), (self.T[i], "+")])
                self._thread("sync3", i, [(self.I[i], "-"), (self.L[jk], "+"), (self.T[i], "-")])
        for k, clause in enumerate(self.clauses, start=1):
            spec = [(self.L[(j, k)], "+" if lit > 0 else "-") for j, lit in enumerate(clause, start=1)]
            self._thread("clause", k, spec)

    def _calibrate(self):
        """Calibrate(G): balance the two paths of every chain link, then lengthen the connecting paths."""
        self.balancing_added = 0
        for link in self.links:
            plus, minus = link.paths["+"], link.paths["-"]
            short = plus if len(plus) < len(minus) else minus
            missing = abs(len(plus) - len(minus))
            if missing:
                free = [i for i in range(len(short) - 1) if edge(short[i], short[i + 1]) not in self.crossing]
                pos = free[0] if self.choice == "first" else self.rng.choice(free)
                self._subdivide(short, pos, missing)
                self.balancing_added += missing
        self.Lambda = len(self.singles) + sum(len(link.paths["+"]) - 1 for link in self.links)
        if not self.lengthen:
            return
        for thread in self.threads:
            for path in thread.connecting:
                assert len(path) == 2
                self._subdivide(path, 0, self.Lambda - 1)

    # -- derived objects --------------------------------------------------------------------

    def chain_edges(self):
        result = set(self.singles)
        for link in self.links:
            result.update(link.path_edges("+"))
            result.update(link.path_edges("-"))
        return result

    def all_edges(self):
        return {edge(a, b) for a in self.adj for b in self.adj[a]}

    def chain_path(self, signs):
        """Edge set of the chain path that takes the path signs[idx] in the chain link idx."""
        result = set(self.singles)
        for link, sign in zip(self.links, signs):
            result.update(link.path_edges(sign))
        return result

    def consistent_signs(self, tau):
        """Signs of the consistent chain path of the truth assignment tau (dict i -> bool)."""
        signs = [""] * len(self.links)
        for i, idxs in self.block.items():
            for idx in idxs:
                signs[idx] = "+" if tau[i] else "-"
        return signs

    def crossing_location(self, crossing_edge):
        """The chain link and the sign of the path on which a crossing edge lies."""
        found = [(link.idx, sign) for link in self.links for sign in "+-"
                 if crossing_edge in set(link.path_edges(sign))]
        assert len(found) == 1
        return found[0]

    def bfs(self, source, removed=frozenset()):
        dist = {source: 0}
        queue = deque([source])
        while queue:
            x = queue.popleft()
            for y in self.adj[x]:
                if y not in dist and edge(x, y) not in removed:
                    dist[y] = dist[x] + 1
                    queue.append(y)
        return dist

    def separates(self, path_edges):
        """True if G minus the given edges contains no u-v path."""
        return self.v not in self.bfs(self.u, removed=frozenset(path_edges))


def satisfies(tau, clauses):
    return all(any(tau[abs(lit)] == (lit > 0) for lit in clause) for clause in clauses)


def satisfiable(n, clauses):
    for bits in range(2 ** n):
        tau = {i: bool(bits >> (i - 1) & 1) for i in range(1, n + 1)}
        if satisfies(tau, clauses):
            return True
    return False
