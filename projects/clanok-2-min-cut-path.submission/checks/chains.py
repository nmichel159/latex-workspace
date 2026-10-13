"""Random instances with a long square decomposition (used by check_structure.py and check_algorithm.py).

random_dc_chain(rng)       a chain of 3-6 small blocks joined by pairs of paths, pendant parts attached;
                           returned only if it is verified to lie in DC and to have c(u,v) = 2
random_general_chain(rng)  the same with larger random blocks of unrestricted diameter; returned if c(u,v) = 2
                           and the graph is NOT in DC

Both return (Gr, u, v) or None.  The decomposition of the instance is computed later by the checks; the blocks
used here need not be the squares of the pair (a block whose terminals are cut by two edges is split further).
"""

import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp import Gr, bfs, edge_conn, in_dc, is_connected  # noqa: E402

NAMED = {
    "K1": (1, []),
    "K2": (2, [(0, 1)]),
    "P3": (3, [(0, 1), (1, 2)]),
    "K3": (3, [(0, 1), (1, 2), (0, 2)]),
    "C4": (4, [(0, 1), (1, 2), (2, 3), (0, 3)]),
    "K4-e": (4, [(0, 1), (0, 2), (0, 3), (1, 2), (2, 3)]),
    "K4": (4, [(a, b) for a in range(4) for b in range(a + 1, 4)]),
    "star3": (4, [(0, 1), (0, 2), (0, 3)]),
    "C5": (5, [(i, (i + 1) % 5) for i in range(5)]),
    "W4": (5, [(0, i) for i in range(1, 5)] + [(1, 2), (2, 3), (3, 4), (1, 4)]),
    "K23": (5, [(a, b) for a in (0, 1) for b in (2, 3, 4)]),
    "star4": (5, [(0, i) for i in range(1, 5)]),
}


def diameter_at_most_two(n, edges):
    g = Gr(n, edges)
    return is_connected(g) and all(d <= 2 for s in range(n) for d in bfs(g, s))


def random_small(rng, weights=None):
    """A connected graph with 1..5 vertices and diameter at most two."""
    names = list(NAMED)
    w = weights or [3, 3, 2, 3, 2, 2, 2, 1, 1, 2, 1, 1]
    if rng.random() < 0.25:
        while True:
            n = rng.randint(3, 5)
            es = [(a, b) for a in range(n) for b in range(a + 1, n) if rng.random() < rng.uniform(0.4, 0.8)]
            if diameter_at_most_two(n, es):
                return n, es
    return NAMED[rng.choices(names, w)[0]]


def random_link(rng):
    kind = rng.choices(["v", "K2", "K3", "P3", "K4"], [6, 2, 1, 1, 1])[0]
    if kind == "v":
        return 1, [], 0, 0
    n, es = NAMED[kind]
    return n, list(es), rng.randrange(n), rng.randrange(n)


class Builder:
    def __init__(self):
        self.n = 0
        self.edges = []
        self.present = set()

    def add_graph(self, n, es):
        off = self.n
        self.n += n
        for a, b in es:
            self.edge(a + off, b + off)
        return off

    def edge(self, a, b):
        self.edges.append((a, b))
        self.present.add((min(a, b), max(a, b)))

    def has(self, a, b):
        return (min(a, b), max(a, b)) in self.present


def build_chain(rng, k, square_fn, link_rounds=(0, 0, 1, 1, 2), pendants=True, crossing=0.0):
    B = Builder()
    squares = []
    for i in range(k):
        block = square_fn(rng)
        n_i, es_i = block[0], block[1]
        hint = block[2] if len(block) > 2 else None
        off = B.add_graph(n_i, es_i)
        verts = list(range(off, off + n_i))
        ent = (rng.choice(verts), rng.choice(verts))
        lea = (rng.choice(verts), rng.choice(verts))
        if hint == "ends":
            ent = (off, off + n_i - 1)
            lea = ent if rng.random() < 0.5 else ent[::-1]
        elif n_i >= 2 and rng.random() < crossing:
            # the pattern of the six-vertex example: entering and leaving terminals are the same two vertices
            a, b = rng.sample(verts, 2)
            ent = (a, b)
            lea = (a, b) if rng.random() < 0.5 else (b, a)
        if i == 0:
            u = rng.choice(verts)
            ent = (u, u)
        if i == k - 1:
            v = rng.choice(verts)
            lea = (v, v)
        squares.append((verts, ent, lea))
    join_edges = 0
    for i in range(k - 1):
        for side in (0, 1):
            cur = squares[i][2][side]
            target = squares[i + 1][1][side]
            rounds = rng.choice(link_rounds)
            if rounds == 0 and (cur == target or B.has(cur, target)):
                rounds = 1               # a direct edge would be a loop or repeat an edge of the other path
            for _ in range(rounds):
                ln, les, lx, ly = random_link(rng)
                off = B.add_graph(ln, les)
                B.edge(cur, off + lx)
                join_edges += 1
                cur = off + ly
            B.edge(cur, target)
            join_edges += 1
    if pendants:
        for _ in range(rng.choice((0, 0, 1, 1, 2, 3))):
            w = rng.randrange(B.n)
            z = B.add_graph(1, [])
            B.edge(w, z)
            kind = rng.choice(("vertex", "vertex", "triangle", "path", "edge"))
            if kind == "triangle":
                o = B.add_graph(2, [(0, 1)])
                B.edge(z, o)
                B.edge(z, o + 1)
            elif kind == "path":
                o = B.add_graph(1, [])
                B.edge(z, o)
            elif kind == "edge":
                o = B.add_graph(1, [])
                B.edge(z, o)
                o2 = B.add_graph(1, [])
                B.edge(z, o2)
    return B, u, v, join_edges


def random_dc_chain(rng, kmin=3, kmax=6):
    k = rng.randint(kmin, kmax)
    B, u, v, join_edges = build_chain(rng, k, random_small, crossing=rng.choice((0.0, 0.2, 0.4)))
    g = Gr(B.n, B.edges)
    if g.m != len(set((min(a, b), max(a, b)) for a, b in B.edges)) or g.m != len(B.edges):
        return None                      # a join edge duplicated another edge
    if not is_connected(g) or g.n > 40:
        return None
    if edge_conn(g, u, v) != 2:
        return None
    dc, _ = in_dc(g)
    if not dc:
        return None
    return g, u, v


def random_block(rng):
    """A block of unrestricted diameter.  With probability 1/2 a long path or cycle (terminals at its two ends
    when the block is placed with the hint "ends"): the crossed pattern then makes c(x,y) = 3 although
    d(x,y) >= 3, so the pair leaves DC."""
    if rng.random() < 0.5:
        n = rng.randint(4, 6)
        es = [(i, i + 1) for i in range(n - 1)]
        if n >= 5 and rng.random() < 0.4:
            es.append((1, n - 2))        # a chord between the second and the last-but-one vertex
        return n, es, "ends"
    n = rng.randint(4, 9)
    p = rng.uniform(0.35, 0.75)
    while True:
        es = [(a, b) for a in range(n) for b in range(a + 1, n) if rng.random() < p]
        if is_connected(Gr(n, es)):
            return n, es


def random_general_chain(rng, kmin=2, kmax=4):
    k = rng.randint(kmin, kmax)
    B, u, v, join_edges = build_chain(rng, k, random_block, link_rounds=(0, 0, 1), pendants=False)
    g = Gr(B.n, B.edges)
    if g.m != len(B.edges) or not is_connected(g) or g.n > 40:
        return None
    if edge_conn(g, u, v) != 2:
        return None
    dc, _ = in_dc(g)
    if dc:
        return None
    return g, u, v
