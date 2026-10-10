"""Brute-force checks of Sections 2, 4 and 5 on small graphs.

cp(u,v) is computed in two independent ways:

  cp_definition   Definition 2.1 read literally: the smallest edge set S such that u and v are
                  connected in (V, S) and disconnected in G - S (all 2^|E| subsets; graphs with at
                  most six vertices)
  cp              the minimum of |P| + |B - P| over all simple u-v paths P and all edge boundaries B
                  of vertex sets that contain u and not v

and the two are compared on every graph with at most six vertices. The checks:

  Section 2    every minimum u-v cut is an edge boundary; Lemma 2.4; |C u P| <= 2 cp - 1
  Theorem 3.10 cp(u,v) = d(u,v) iff some shortest u-v path is separating
  Lemma 4.3    in a graph of diameter two, one side of every edge boundary has all its vertices
               incident to the boundary
  Lemma 4.4    a u-v path meets an edge boundary that separates u from v in an odd number of edges
  Theorem 4.5  cp = c + d - 1 in graphs of diameter (at most) two
  Remark 4.6   if cp = c + d - 1, every minimum cut together with every shortest path is a minimum cut-path
  Section 5    c(x,y) <= 2 for all pairs iff every block is an edge or a cycle (cactus); two cycles
               share at most one vertex; Theorem 5.1: cp = c + d - 1 in these graphs
  the class "d <= 2 or c <= 2 for every pair": the two graphs with cp < c + d - 1

Graphs: all graphs with at most seven vertices (the networkx atlas), random graphs of diameter two
on eight vertices, random cactus graphs on up to twelve vertices.

Run:  python check_cutpath.py     (a few minutes)
"""

import itertools
import random
import sys
import time

import networkx as nx
from networkx.generators.atlas import graph_atlas_g


class Failure(Exception):
    pass


def require(condition, message):
    if not condition:
        raise Failure(message)


class Small:
    """A graph on the vertices 0..n-1; edge sets and vertex sets are bit masks."""

    def __init__(self, G):
        nodes = sorted(G.nodes())
        index = {x: i for i, x in enumerate(nodes)}
        self.n = len(nodes)
        self.edges = sorted((min(index[a], index[b]), max(index[a], index[b])) for a, b in G.edges())
        self.m = len(self.edges)
        self.full = (1 << self.m) - 1
        self.adj = [[] for _ in range(self.n)]
        for e, (a, b) in enumerate(self.edges):
            self.adj[a].append((b, e))
            self.adj[b].append((a, e))
        # boundary[A]: the edges with exactly one end in the vertex set A
        self.boundary = [0] * (1 << self.n)
        for A in range(1 << self.n):
            mask = 0
            for e, (a, b) in enumerate(self.edges):
                if (A >> a ^ A >> b) & 1:
                    mask |= 1 << e
            self.boundary[A] = mask
        self.dist = [self._bfs(x) for x in range(self.n)]
        self._components = None

    def _bfs(self, source, removed=0):
        dist = [None] * self.n
        dist[source] = 0
        queue = [source]
        for x in queue:
            for y, e in self.adj[x]:
                if dist[y] is None and not removed >> e & 1:
                    dist[y] = dist[x] + 1
                    queue.append(y)
        return dist

    def connected(self):
        return all(d is not None for d in self.dist[0])

    def diameter(self):
        return max(d for row in self.dist for d in row)

    def sides(self, u, v):
        return [A for A in range(1 << self.n) if A >> u & 1 and not A >> v & 1]

    def paths(self, u, v):
        """All simple u-v paths as edge masks."""
        result = []

        def extend(x, visited, mask):
            if x == v:
                result.append(mask)
                return
            for y, e in self.adj[x]:
                if not visited >> y & 1:
                    extend(y, visited | 1 << y, mask | 1 << e)

        extend(u, 1 << u, 0)
        return result

    def c(self, u, v):
        return min(self.boundary[A].bit_count() for A in self.sides(u, v))

    def cp(self, u, v, paths=None):
        sides = self.sides(u, v)
        best = self.m + 1
        for P in (paths if paths is not None else self.paths(u, v)):
            size = P.bit_count()
            if size >= best:
                continue
            rest = self.full ^ P
            extra = min((self.boundary[A] & rest).bit_count() for A in sides)
            best = min(best, size + extra)
        return best

    # -- Definition 2.1 read literally -------------------------------------------------------

    def components(self):
        """components[S][x]: the smallest vertex of the component of x in (V, S), for every S."""
        if self._components is None:
            table = [None] * (1 << self.m)
            table[0] = tuple(range(self.n))
            for S in range(1, 1 << self.m):
                low = S & -S
                a, b = self.edges[low.bit_length() - 1]
                prev = table[S ^ low]
                ra, rb = prev[a], prev[b]
                if ra == rb:
                    table[S] = prev
                else:
                    keep, drop = min(ra, rb), max(ra, rb)
                    table[S] = tuple(keep if r == drop else r for r in prev)
            self._components = table
        return self._components

    def cp_definition(self, u, v):
        table = self.components()
        best = self.m + 1
        for S in range(1 << self.m):
            if S.bit_count() < best and table[S][u] == table[S][v]:
                rest = table[self.full ^ S]
                if rest[u] != rest[v]:
                    best = S.bit_count()
        return best

    def minimum_cuts_definition(self, u, v):
        """All smallest edge sets whose removal disconnects u from v."""
        table = self.components()
        cuts = [S for S in range(1 << self.m) if table[self.full ^ S][u] != table[self.full ^ S][v]]
        size = min(S.bit_count() for S in cuts)
        return size, [S for S in cuts if S.bit_count() == size]


def is_cactus(G):
    """Every block is an edge or a cycle."""
    for block in nx.biconnected_components(G):
        k = len(block)
        if k > 2 and G.subgraph(block).number_of_edges() != k:
            return False
    return True


def cycles_share_at_most_one_vertex(G):
    cycles = [set(c) for c in nx.simple_cycles(G)]
    return all(len(a & b) <= 1 for a, b in itertools.combinations(cycles, 2))


class Counter(dict):
    def add(self, key, amount=1):
        self[key] = self.get(key, 0) + amount


def check_graph(G, stats, literal):
    """All checks for one graph; `literal` also runs the checks over all edge subsets."""
    H = Small(G)
    n = H.n
    connected = H.connected()
    diameter = H.diameter() if connected else None
    pairs = [(u, v) for u in range(n) for v in range(u + 1, n) if H.dist[u][v] is not None]
    cvalue = {}
    all_formula = True
    for u, v in pairs:
        paths = H.paths(u, v)
        d = H.dist[u][v]
        c = H.c(u, v)
        cp = H.cp(u, v, paths)
        cvalue[(u, v)] = c
        stats.add("pairs")
        require(d == min(P.bit_count() for P in paths), "distance")
        # Lemma 2.4 and the 2-approximation
        require(max(c, d) <= cp <= c + d - 1, "Lemma 2.4")
        require(c + d - 1 <= 2 * cp - 1, "|C u P| <= 2 cp - 1")
        if c == 1 or d == 1:
            require(cp == c + d - 1, "Lemma 2.4, c = 1 or d = 1")
        # Theorem 3.10: cp = d iff a shortest u-v path is separating (connectivity test on G - P)
        separating = any(H._bfs(u, removed=P)[v] is None for P in paths if P.bit_count() == d)
        require((cp == d) == separating, "cp = d iff a separating shortest path exists")
        stats.add("pairs with a separating shortest path", separating)
        if cp != c + d - 1:
            all_formula = False
        if literal:
            require(cp == H.cp_definition(u, v), "the two computations of cp differ")
            size, cuts = H.minimum_cuts_definition(u, v)
            boundaries = {H.boundary[A] for A in H.sides(u, v)}
            require(size == c, "c(u,v)")
            require(all(S in boundaries for S in cuts), "a minimum u-v cut is not an edge boundary")
            # Lemma 4.4
            for A in H.sides(u, v):
                require(all((H.boundary[A] & P).bit_count() % 2 == 1 for P in paths), "Lemma 4.4")
            # Remark 4.6
            if cp == c + d - 1:
                shortest = [P for P in paths if P.bit_count() == d]
                for S in cuts:
                    require(all((S | P).bit_count() == cp for P in shortest), "Remark 4.6")
    if connected and n >= 2:
        stats.add("connected graphs")
        # Theorem 4.5 and Lemma 4.3
        if diameter <= 2:
            stats.add("graphs of diameter at most two")
            stats.add("pairs in graphs of diameter at most two", len(pairs))
            require(all_formula, "Theorem 4.5")
            for A in range(1, (1 << n) - 1):
                incident = 0
                for e, (a, b) in enumerate(H.edges):
                    if H.boundary[A] >> e & 1:
                        incident |= 1 << a | 1 << b
                rest = ((1 << n) - 1) ^ incident
                require(not (rest & A and rest & ~A), "Lemma 4.3")
        # Section 5
        cut_two = max(cvalue.values()) <= 2
        require(cut_two == is_cactus(G), "c(x,y) <= 2 for all pairs iff cactus")
        if cut_two:
            stats.add("graphs with c(x,y) <= 2 for all pairs")
            stats.add("pairs in graphs with c(x,y) <= 2", len(pairs))
            require(cycles_share_at_most_one_vertex(G), "two cycles share two vertices")
            require(all_formula, "Theorem 5.1")
        # the class of the conclusion
        if all(H.dist[u][v] <= 2 or cvalue[(u, v)] <= 2 for u, v in pairs):
            stats.add("graphs with d <= 2 or c <= 2 for every pair")
            if not all_formula:
                stats.add("... of these, graphs with a pair cp < c + d - 1")
                if n <= 6:
                    stats.setdefault("failing graphs with at most six vertices", []).append(G)
    return H


def random_cactus(rng, size):
    G = nx.Graph()
    G.add_node(0)
    while G.number_of_nodes() < size:
        x = rng.randrange(G.number_of_nodes())
        k = rng.choice((1, 3, 3, 4, 5))
        k = min(k, size - G.number_of_nodes() + 1) if k > 1 else 1
        first = G.number_of_nodes()
        if k < 3:
            G.add_edge(x, first)
        else:
            cycle = [x] + list(range(first, first + k - 1))
            nx.add_cycle(G, cycle)
    return G


def counterexamples(small_failing):
    """The two graphs of the class "d <= 2 or c <= 2" in which the formula fails."""
    base = ["ta", "tv", "au", "ab", "vb", "us", "sb"]
    known = []
    for name, extra, expected in (("(a)", [], (2, 3, 3)), ("(b)", ["av", "ub"], (3, 2, 3))):
        G = nx.Graph([tuple(e) for e in base + extra])
        known.append(G)
        H = Small(G)
        index = {x: i for i, x in enumerate(sorted(G.nodes()))}
        u, v = index["u"], index["v"]
        values = (H.c(u, v), H.dist[u][v], H.cp(u, v))
        require(values == expected, "counterexample %s: (c, d, cp) = %s" % (name, values))
        pairs = itertools.combinations(range(H.n), 2)
        require(all(H.dist[x][y] <= 2 or H.c(x, y) <= 2 for x, y in pairs), "counterexample %s not in the class" % name)
        print("counterexample %s: c = %d, d = %d, cp = %d < c + d - 1 = %d; in the class" % ((name,) + values + (values[0] + values[1] - 1,)))
    # they are the only graphs with at most six vertices in the class in which the formula fails
    require(len(small_failing) == 2, "number of failing graphs with at most six vertices")
    require(all(any(nx.is_isomorphic(G, K) for K in known) for G in small_failing)
            and not nx.is_isomorphic(small_failing[0], small_failing[1]),
            "the failing graphs with at most six vertices are not the two counterexamples")
    print("the two counterexamples are the only failing graphs of the class with at most six vertices")


def run():
    started = time.time()
    rng = random.Random(20261010)
    stats = Counter()
    atlas = [G for G in graph_atlas_g() if G.number_of_nodes() >= 2]
    for G in atlas:
        check_graph(G, stats, literal=G.number_of_nodes() <= 6)
        stats.add("graphs")
    print("atlas: all %d graphs with 2..7 vertices  [%.0f s]" % (len(atlas), time.time() - started), flush=True)
    small_failing = stats.pop("failing graphs with at most six vertices", [])
    for key, value in stats.items():
        print("   %-52s %s" % (key, value))

    stats = Counter()
    count = 0
    while count < 60:
        G = nx.gnp_random_graph(8, rng.uniform(0.4, 0.75), seed=rng.randrange(10 ** 9))
        if nx.is_connected(G) and nx.diameter(G) == 2:
            check_graph(G, stats, literal=False)
            count += 1
    print("random graphs of diameter two on 8 vertices: %d graphs, %d pairs  [%.0f s]"
          % (count, stats["pairs"], time.time() - started), flush=True)

    stats = Counter()
    for _ in range(200):
        check_graph(random_cactus(rng, rng.randint(8, 12)), stats, literal=False)
    print("random cactus graphs on 8..12 vertices: 200 graphs, %d pairs  [%.0f s]"
          % (stats["pairs"], time.time() - started), flush=True)
    require(stats["graphs with c(x,y) <= 2 for all pairs"] == 200, "a random cactus is not in the class")

    counterexamples(small_failing)
    print("no check failed")


if __name__ == "__main__":
    try:
        run()
    except Failure as failure:
        print("CHECK FAILED:", failure)
        sys.exit(1)
