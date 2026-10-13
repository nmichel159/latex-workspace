"""Points (g), (h): the two augmenting paths versus two edge-disjoint paths.

1. In G_a (ex:counterexamples) with the first augmenting path u,a,b,v, every second augmenting path traverses
   ab backwards: the two augmenting paths share the edge ab.
2. Whenever the first augmenting path is a separating u-v path (in particular a separating shortest path found
   by breadth-first search, the positive instances of the paper), the second augmenting path must cancel flow.
   Counted on all connected graphs with at most 7 vertices.
3. The net flow of two augmentations can contain a cycle beside the two paths (explicit example), so "follow the
   flow from u" can give a walk; two searches in the digraph of the net flow give two edge-disjoint simple paths.
   Tested with randomized depth-first augmentations.
4. The digraph D built from the two augmenting paths of item 1 instead of p_1, p_2 does not give F.
"""

import os
import random
import sys
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ref
from ref import E


def augment(adj, u, v, flow, rng=None, first=None):
    """One augmentation in the residual graph of `flow` (dict (x,y) -> 1).  Returns the augmenting path as a
    vertex list (it may traverse flow edges backwards) or None.  rng: randomized depth-first search;
    otherwise breadth-first search.  first: a prescribed path to push."""
    if first is not None:
        path = list(first)
    else:
        par = {u: None}
        if rng is None:
            q = deque([u])
            while q and v not in par:
                x = q.popleft()
                for y in sorted(adj[x], key=str):
                    if y not in par and flow.get((x, y), 0) == 0:
                        par[y] = x
                        q.append(y)
        else:
            stack = [u]
            while stack and v not in par:
                x = stack.pop()
                nb = sorted(adj[x], key=str)
                rng.shuffle(nb)
                for y in nb:
                    if y not in par and flow.get((x, y), 0) == 0:
                        par[y] = x
                        stack.append(y)
        if v not in par:
            return None
        path = [v]
        while par[path[-1]] is not None:
            path.append(par[path[-1]])
        path.reverse()
    for x, y in zip(path, path[1:]):
        if flow.get((y, x), 0) == 1:
            del flow[(y, x)]
        else:
            flow[(x, y)] = 1
    return path


def paths_from_flow(adj, u, v, flow):
    """Two searches in the digraph of the net flow: two edge-disjoint simple u-v paths."""
    arcs = dict(flow)
    res = []
    for _ in range(2):
        par = {u: None}
        q = deque([u])
        while q:
            x = q.popleft()
            for y in adj[x]:
                if arcs.get((x, y), 0) == 1 and y not in par:
                    par[y] = x
                    q.append(y)
        assert v in par
        p = [v]
        while par[p[-1]] is not None:
            p.append(par[p[-1]])
        p.reverse()
        for x, y in zip(p, p[1:]):
            del arcs[(x, y)]
        res.append(tuple(p))
    return res, arcs


def es(s):
    return [(w[0], w[1:]) for w in s.split()]


print("1. G_a, first augmenting path u,a,b,v")
Ga = ref.graph(es("ua us sb ab at tv bv"))
flow = {}
P1 = augment(Ga, "u", "v", flow, first=tuple("uabv"))
P2 = augment(Ga, "u", "v", flow)
print("   augmenting paths:", "".join(P1), "".join(P2))
print("   common edges:", sorted(ref.fmt_e(e) for e in set(ref.path_edges(P1)) & set(ref.path_edges(P2))))
(p1, p2), rest = paths_from_flow(Ga, "u", "v", flow)
print("   paths of the net flow:", "".join(p1), "".join(p2), "left over arcs:", rest)

print("4. D from the augmenting paths of item 1 (edge ab gets the arc b->a from P1 and a->b from P2)")
arcs = {x: set() for x in Ga}
trav = set()
for P in (P1, P2):
    for x, y in zip(P, P[1:]):
        trav.add((x, y))
for x in Ga:
    for y in Ga[x]:
        if (x, y) in trav and (y, x) not in trav:
            continue
        if (x, y) in trav and (y, x) in trav:
            arcs[x].add(y)            # traversed both ways: both reversed arcs
            continue
        arcs[x].add(y)


def reach(out, s):
    seen = {s}
    q = deque([s])
    while q:
        x = q.popleft()
        for y in out[x]:
            if y not in seen:
                seen.add(y)
                q.append(y)
    return seen


rs = {x: reach(arcs, x) for x in Ga}
Fwrong = {E(x, y) for (x, y) in trav if not (y in rs[x] and x in rs[y])}
Ftrue = set().union(*ref.min_cuts2(Ga, "u", "v"))
print("   edges of P1, P2 with ends in different strong components:", sorted(ref.fmt_e(e) for e in Fwrong))
print("   F:", sorted(ref.fmt_e(e) for e in Ftrue), "-> equal:", Fwrong == Ftrue)
print("   (here the result is still F because ab keeps both arcs; the lemma of the text does not cover this"
      " digraph, since P2 is not edge-disjoint from P1 and 'the path that contains xy' is not unique)")

print("2. all connected graphs with at most 7 vertices, ordered pairs with c(u,v) = 2")
import networkx as nx
from networkx.generators.atlas import graph_atlas_g
pairs = forced = bfs_shared = 0
for G in graph_atlas_g():
    n = G.number_of_nodes()
    if n < 2 or not nx.is_connected(G):
        continue
    adj = ref.graph(sorted(G.edges()))
    for u in range(n):
        du = ref.bfs(adj, u)
        for v in range(n):
            if u == v or ref.cutvalue(adj, u, v, limit=3) != 2:
                continue
            pairs += 1
            sp = [p for p in ref.all_simple_paths(adj, u, v, maxlen=du[v]) if len(p) - 1 == du[v]]
            if any(not ref.connected(adj, u, v, set(ref.path_edges(p))) for p in sp):
                forced += 1
            flow = {}
            A1 = augment(adj, u, v, flow)
            A2 = augment(adj, u, v, flow)
            if set(ref.path_edges(A1)) & set(ref.path_edges(A2)):
                bfs_shared += 1
            (p1, p2), rest = paths_from_flow(adj, u, v, flow)
            assert len(set(p1)) == len(p1) and len(set(p2)) == len(p2)
            assert not set(ref.path_edges(p1)) & set(ref.path_edges(p2))
print("   pairs: %d" % pairs)
print("   pairs with a separating shortest path (if it is the first augmenting path, cancellation is forced): %d" % forced)
print("   pairs where the two breadth-first augmenting paths (sorted adjacency lists) share an edge: %d" % bfs_shared)

print("3. net flow with a cycle: P1 = u,1,2,3,4,v and the augmenting path u,4,3,x,2,1,v")
H = ref.graph([("u", "1"), ("1", "2"), ("2", "3"), ("3", "4"), ("4", "v"), ("u", "4"), ("3", "x"), ("x", "2"), ("1", "v")])
flow = {}
augment(H, "u", "v", flow, first=("u", "1", "2", "3", "4", "v"))
augment(H, "u", "v", flow, first=("u", "4", "3", "x", "2", "1", "v"))
(p1, p2), rest = paths_from_flow(H, "u", "v", flow)
print("   paths:", "".join(p1), "".join(p2), " left over arcs (a cycle):", sorted(rest))

rng = random.Random(5)
tested = cyc = 0
for G in graph_atlas_g():
    n = G.number_of_nodes()
    if n < 5 or not nx.is_connected(G):
        continue
    adj = ref.graph(sorted(G.edges()))
    for _ in range(3):
        u, v = rng.sample(range(n), 2)
        if ref.cutvalue(adj, u, v, limit=3) != 2:
            continue
        flow = {}
        a1 = augment(adj, u, v, flow, rng=rng)
        a2 = augment(adj, u, v, flow, rng=rng)
        assert a1 and a2 and augment(adj, u, v, dict(flow), rng=rng) is None
        (p1, p2), rest = paths_from_flow(adj, u, v, flow)
        assert len(set(p1)) == len(p1) and len(set(p2)) == len(p2)
        assert not set(ref.path_edges(p1)) & set(ref.path_edges(p2))
        assert all(e in ref.edges_of(adj) for e in ref.path_edges(p1) + ref.path_edges(p2))
        tested += 1
        cyc += bool(rest)
print("   randomized depth-first augmentations: %d pairs, two simple edge-disjoint paths from the net flow in all;"
      " left-over flow cycles in %d" % (tested, cyc))
